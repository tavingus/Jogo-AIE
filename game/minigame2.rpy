################################################################################
# MINIGAME2.RPY
# Minigame 2: "Exame clínico" — sinais compatíveis com a AIE
#
# Como funciona:
#   - O jogador examina o cavalo em 6 ÁREAS (abas à esquerda): Temperatura,
#     Mucosas, Linfonodos, Estado geral, Histórico e Hemograma.
#   - Cada área mostra 4 ACHADOS (cartas à direita). Alguns são compatíveis com
#     a AIE e outros não (distratores). A cada partida os achados são sorteados
#     de um banco maior, então o exame nunca é igual duas vezes.
#   - O jogador MARCA (clique) os achados que considera compatíveis com a AIE.
#     Clicar de novo desmarca.
#   - Só dá para concluir o exame depois de examinar TODAS as áreas.
#   - Ao concluir, entra a fase de REVISÃO: cada carta mostra se foi acerto,
#     erro ou sinal que faltou marcar, e o jogador pode navegar pelas abas para
#     ver onde errou. Depois clica em "Continuar" para voltar ao mapa.
#
# Pontuação (ver roadmap.rpy para o sistema de medalhas):
#   + MG2_POINTS_HIT   por achado compatível marcado (acerto)
#   - MG2_POINTS_MISS  por achado marcado que NÃO é compatível (erro)
#   - MG2_POINTS_MISS  por achado compatível que ficou sem marcar (faltou)
#   Achado não compatível e não marcado: neutro (0) — assim ninguém ganha
#   pontos de graça sem marcar nada. O placar nunca fica abaixo de 0.
#   Pontuação máxima = marcar exatamente todos os compatíveis.
#
# Placeholders de arte (mesmo esquema do minigame 1):
#   Se o PNG não existir em game/images/minigame2/, aparece um retângulo
#   colorido com texto, já no tamanho final. Quando você colocar o PNG com o
#   nome certo na pasta, ele passa a ser usado sozinho.
#   Todo PNG real é exibido com zoom 2.0 + nearest neighbor: exporte na METADE
#   do tamanho final indicado em cada "# IMAGEM:".
#   Os TEXTOS das abas e das cartas são desenhados pelo jogo (são muitos
#   achados), por cima de molduras que você só precisa desenhar uma vez.
#
# Este arquivo contém: dados/configuração, lógica, tela de instruções, tela
# do gameplay e o "label minigame_2_entry" — chamado pelo roadmap.rpy.
################################################################################


## -----------------------------------------------------------------------
## 1) CONFIGURAÇÃO, DADOS E LÓGICA
## -----------------------------------------------------------------------
init python:

    MG2_ART_DIR = "images/minigame2/"
    MG2_ZOOM = 2.0  # arte a 960x540, exibida em 1920x1080

    # ---- Layout (tela 1920x1080) — ajuste ao encaixar a arte ---------------
    # Abas das áreas do exame (coluna da esquerda)
    MG2_TABS_X = 60
    MG2_TABS_Y0 = 260
    MG2_TABS_STEP = 120
    MG2_TAB_SIZE = (520, 100)        # exporte a 260x50

    # Cartas de achados (painel da direita)
    MG2_CARDS_X = 1000
    MG2_CARDS_Y0 = 280
    MG2_CARDS_STEP = 150
    MG2_CARD_SIZE = (820, 130)       # exporte a 410x65

    # Botão "Concluir exame" / "Continuar"
    MG2_SUBMIT_POS = (1000, 920)
    MG2_SUBMIT_SIZE = (400, 90)      # exporte a 200x45

    # ---- Regras ------------------------------------------------------------
    MG2_CARDS_PER_AREA = 4       # achados mostrados em cada área
    MG2_POINTS_HIT = 10          # acerto: compatível marcado
    MG2_POINTS_MISS = 5          # erro: perde isto (marcou errado OU deixou de marcar)

    # ---- Banco de achados por área -----------------------------------------
    # Cada achado é ("id", texto): "id" forma o nome do PNG da arte do achado
    # (images/minigame2/achado_<id>.png, com o texto já desenhado nela); o
    # texto só aparece no placeholder enquanto o PNG não existe.
    # "id" da área forma os PNGs das abas: aba_<id>_idle.png / aba_<id>_active.png
    #
    # "correct"   = achados COMPATÍVEIS com a AIE (vêm da sua lista de sinais).
    # "wrong"     = distratores (NÃO compatíveis) — inventei estes; revise!
    # "n_correct" = quantos compatíveis aparecem por partida (sorteados do
    #               banco "correct"). O resto das 4 cartas vem de "wrong".
    #               Precisa de len(wrong) >= 4 - n_correct.
    MG2_AREAS = [
        {
            "id": "temperatura",
            "label": _("Temperatura"),
            "correct": [("febre", _("Febre (temperatura elevada)")),
                        ("febre_recorrente", _("Febre em episódios recorrentes"))],
            "wrong": [("hipotermia", _("Hipotermia (temperatura baixa)")),
                      ("temp_abaixo", _("Temperatura sempre abaixo do normal")),
                      ("calafrios", _("Calafrios com temperatura baixa"))],
            "n_correct": 2,
        },
        {
            "id": "mucosas",
            "label": _("Mucosas"),
            "correct": [("mucosas_palidas", _("Mucosas pálidas")),
                        ("petequias", _("Petéquias nas mucosas"))],
            "wrong": [("mucosas_rosadas", _("Mucosas rosadas e úmidas")),
                      ("mucosas_cianoticas", _("Mucosas cianóticas (azuladas)")),
                      ("mucosas_congestas", _("Mucosas congestas e muito avermelhadas"))],
            "n_correct": 2,
        },
        {
            "id": "linfonodos",
            "label": _("Linfonodos"),
            "correct": [("linfonodos_aumentados", _("Linfonodos aumentados"))],
            "wrong": [("linfonodos_abscesso", _("Linfonodos com abscesso drenando")),
                      ("linfonodos_atrofiados", _("Linfonodos atrofiados")),
                      ("linfonodos_normais", _("Ausência de qualquer alteração palpável"))],
            "n_correct": 1,
        },
        {
            "id": "estado_geral",
            "label": _("Estado geral"),
            "correct": [("letargia", _("Letargia")),
                        ("fraqueza", _("Fraqueza")),
                        ("perda_peso", _("Perda de peso")),
                        ("queda_desempenho", _("Queda de desempenho"))],
            "wrong": [("hiperexcitabilidade", _("Hiperexcitabilidade e agitação")),
                      ("ganho_peso", _("Ganho de peso acentuado")),
                      ("desempenho_acima", _("Desempenho acima do esperado"))],
            "n_correct": 2,
        },
        {
            "id": "historico",
            "label": _("Histórico"),
            "correct": [("hist_febre", _("Febre recorrente")),
                        ("hist_sangue", _("Exposição a sangue (agulhas ou instrumentos)")),
                        ("hist_insetos", _("Contato com insetos hematófagos")),
                        ("hist_infectados", _("Contato com animais infectados"))],
            "wrong": [("hist_vacinado", _("Vacinação em dia, sem outros achados")),
                      ("hist_isolado", _("Animal isolado, sem insetos nem outros equídeos")),
                      ("hist_colica", _("Cólica leve resolvida há semanas"))],
            "n_correct": 2,
        },
        {
            "id": "hemograma",
            "label": _("Hemograma"),
            "correct": [("anemia", _("Anemia")),
                        ("hb_baixa", _("Hemoglobina (Hb) baixa")),
                        ("ht_baixo", _("Hematócrito (Ht) baixo")),
                        ("trombocitopenia", _("Trombocitopenia (plaquetas baixas)"))],
            "wrong": [("policitemia", _("Policitemia (Ht alto)")),
                      ("hb_alta", _("Hemoglobina (Hb) acima do normal")),
                      ("plaquetas_altas", _("Plaquetas muito aumentadas"))],
            "n_correct": 2,
        },
    ]

    # ---- Placeholders de arte ----------------------------------------------
    def mg2_art(filename, size, label, color):
        """Imagem real (ampliada 2x, nearest neighbor; exporte na metade de
        "size") se o arquivo existir, senão um retângulo colorido com texto
        já no tamanho final."""
        path = MG2_ART_DIR + filename
        if renpy.loadable(path):
            return Transform(Image(path, nearest_neighbor=True), zoom=MG2_ZOOM)
        return Fixed(
            Solid(color, xysize=size),
            Text(label, size=26, color="#ffffff", xalign=0.5, yalign=0.5,
                 text_align=0.5, xmaximum=size[0] - 20),
            xysize=size,
        )

    # IMAGEM: minigame2/mg2_bg.png — fundo cheio: baia/consultório com o cavalo.
    # Tamanho final: 1920x1080 → exporte a 960x540. (Deixe livre a coluna da
    # esquerda para as abas e a da direita para as cartas.)
    MG2_BG = mg2_art("mg2_bg.png", (1920, 1080), "FUNDO: cavalo em exame\n(mg2_bg.png)", "#2f3a3a")

    # IMAGEM: minigame2/mg2_title_panel.png — painel de título (canto superior
    # esquerdo). Tamanho final: 820x170 → exporte a 410x85.
    MG2_TITLE_PANEL = mg2_art("mg2_title_panel.png", (820, 170), "PAINEL DE TÍTULO\n(mg2_title_panel.png)", "#4a3a20")

    def mg2_layer(filename, size, label):
        """Camada de arte transparente por cima de uma moldura (ex.: o texto de
        um achado já desenhado no Aseprite). Placeholder = só o texto, sem fundo."""
        path = MG2_ART_DIR + filename
        if renpy.loadable(path):
            return Transform(Image(path, nearest_neighbor=True), zoom=MG2_ZOOM)
        return Fixed(
            Text(label, size=28, color="#ffffff", xpos=40, yalign=0.5,
                 xmaximum=size[0] - 80),
            xysize=size,
        )

    # IMAGEM: minigame2/aba_<area>_idle.png e aba_<area>_active.png — a ABA de
    # cada área, com o nome da área já desenhado (12 arquivos: 6 áreas x 2
    # estados). <area> = temperatura, mucosas, linfonodos, estado_geral,
    # historico, hemograma. Tamanho final: 520x100 → exporte a 260x50.
    def mg2_build_tab_art():
        result = []
        for area in MG2_AREAS:
            entry = {}
            for state, color in (("idle", "#4a4a4a"), ("active", "#2c6e8a")):
                fname = "aba_%s_%s.png" % (area["id"], state)
                entry[state] = mg2_art(fname, MG2_TAB_SIZE,
                                       "%s\n(%s)" % (area["label"], fname), color)
            result.append(entry)
        return result

    MG2_TAB_ART = mg2_build_tab_art()

    # IMAGEM: minigame2/mg2_tab_visited.png — marca de "área já examinada"
    # (ex.: um check). Canvas do tamanho da aba, transparente, com a marca já
    # na posição certa. Tamanho final: 520x100 → exporte a 260x50.
    MG2_TAB_VISITED = mg2_layer("mg2_tab_visited.png", MG2_TAB_SIZE, "")
    if not renpy.loadable(MG2_ART_DIR + "mg2_tab_visited.png"):
        MG2_TAB_VISITED = Text("\u2713", size=34, color="#ffffff", xalign=0.95, yalign=0.5)

    # IMAGEM: minigame2/mg2_card_<estado>.png — MOLDURA de uma carta de achado
    # (sem texto; compartilhada por todos os achados). Tamanho final: 820x130
    # → exporte a 410x65. Estados:
    #   idle     = não marcada            selected = marcada (antes de concluir)
    #   right    = marcada e correta      wrong    = marcada e ERRADA
    #   missed   = compatível que faltou marcar (mostrada só na revisão)
    MG2_CARD_COLORS = {
        "idle": "#4a4a4a", "selected": "#2c6e8a", "right": "#2e7d32",
        "wrong": "#8a2c2c", "missed": "#9a7a1c",
    }
    MG2_CARD_ART = dict(
        (state, mg2_art("mg2_card_%s.png" % state, MG2_CARD_SIZE, "", color))
        for state, color in MG2_CARD_COLORS.items()
    )

    # IMAGEM: minigame2/achado_<id>.png — o TEXTO de cada achado, já desenhado,
    # em fundo TRANSPARENTE (é colocado por cima da moldura da carta). Um
    # arquivo por achado; os ids estão em MG2_AREAS (ex.: achado_febre.png,
    # achado_petequias.png). Tamanho final: 820x130 → exporte a 410x65.
    def mg2_finding_art(card):
        return mg2_layer("achado_%s.png" % card["id"], MG2_CARD_SIZE,
                         "%s\n(achado_%s.png)" % (card["text"], card["id"]))

    # IMAGEM: minigame2/mg2_submit_idle.png, mg2_submit_hover.png,
    # mg2_submit_disabled.png — botão "Concluir exame", com o texto desenhado.
    # Tamanho final: 400x90 → exporte a 200x45.
    MG2_SUBMIT_IDLE = mg2_art("mg2_submit_idle.png", MG2_SUBMIT_SIZE, "CONCLUIR EXAME\n(mg2_submit_idle.png)", "#3a5a3a")
    MG2_SUBMIT_HOVER = mg2_art("mg2_submit_hover.png", MG2_SUBMIT_SIZE, "CONCLUIR EXAME\n(mg2_submit_hover.png)", "#4f7a4f")
    MG2_SUBMIT_DISABLED = mg2_art("mg2_submit_disabled.png", MG2_SUBMIT_SIZE, "CONCLUIR EXAME\n(mg2_submit_disabled.png)", "#2a2a2a")

    # IMAGEM: minigame2/mg2_continue_idle.png e mg2_continue_hover.png — botão
    # "Continuar" da revisão, com o texto desenhado. Tamanho final: 400x90 →
    # exporte a 200x45.
    MG2_CONTINUE_IDLE = mg2_art("mg2_continue_idle.png", MG2_SUBMIT_SIZE, "CONTINUAR\n(mg2_continue_idle.png)", "#3a5a3a")
    MG2_CONTINUE_HOVER = mg2_art("mg2_continue_hover.png", MG2_SUBMIT_SIZE, "CONTINUAR\n(mg2_continue_hover.png)", "#4f7a4f")

    # ---- Efeitos sonoros (só tocam se o arquivo existir) -------------------
    def mg2_sfx(kind):
        files = {
            "hover": "audio/sfx_hover.ogg",
            "click": "audio/sfx_click.ogg",
            "correct": "audio/sfx_correct.ogg",
            "wrong": "audio/sfx_wrong.ogg",
        }
        path = files.get(kind)
        if path and renpy.loadable(path):
            renpy.sound.play(path)


## Estado do minigame (guardado no save / rollback)
default mg2_cards = []        # por área: lista de {"text": ..., "correct": bool}
default mg2_selected = []     # por área: lista de bool (carta marcada?)
default mg2_visited = []      # por área: já foi examinada?
default mg2_area = 0          # área aberta agora
default mg2_phase = "exam"    # "exam" (jogando) ou "review" (revisão após concluir)
default mg2_score = 0
default mg2_max_score = 0


init python:

    def mg2_reset():
        """Nova partida: sorteia os achados de cada área e zera as marcações."""
        cards = []
        for area in MG2_AREAS:
            correct_pool = list(area["correct"])
            wrong_pool = list(area["wrong"])
            renpy.random.shuffle(correct_pool)
            renpy.random.shuffle(wrong_pool)

            n_correct = area["n_correct"]
            area_cards = [{"id": i, "text": t, "correct": True} for (i, t) in correct_pool[:n_correct]]
            area_cards += [{"id": i, "text": t, "correct": False}
                           for (i, t) in wrong_pool[:MG2_CARDS_PER_AREA - n_correct]]
            renpy.random.shuffle(area_cards)
            cards.append(area_cards)

        store.mg2_cards = cards
        store.mg2_selected = [[False] * len(c) for c in cards]
        store.mg2_visited = [False] * len(cards)
        store.mg2_visited[0] = True
        store.mg2_area = 0
        store.mg2_phase = "exam"
        store.mg2_score = 0
        store.mg2_max_score = sum(1 for c in cards for card in c if card["correct"]) * MG2_POINTS_HIT

    def mg2_select_area(i):
        """Abre a área i (e a marca como examinada)."""
        store.mg2_area = i
        store.mg2_visited[i] = True
        mg2_sfx("click")

    def mg2_toggle(area, j):
        """Marca/desmarca a carta j da área. Travado na fase de revisão."""
        if store.mg2_phase != "exam":
            return
        store.mg2_selected[area][j] = not store.mg2_selected[area][j]
        mg2_sfx("click")

    def mg2_all_visited():
        return all(store.mg2_visited)

    def mg2_marked_count(area):
        return sum(1 for s in store.mg2_selected[area] if s)

    def mg2_card_state(area, j):
        """Estado visual da carta: idle/selected (jogando) ou
        right/wrong/missed (revisão)."""
        selected = store.mg2_selected[area][j]
        correct = store.mg2_cards[area][j]["correct"]
        if store.mg2_phase == "exam":
            return "selected" if selected else "idle"
        if selected and correct:
            return "right"
        if selected and not correct:
            return "wrong"
        if correct:
            return "missed"
        return "idle"

    def mg2_submit():
        """Conclui o exame: calcula a pontuação e entra na fase de revisão."""
        if store.mg2_phase != "exam" or not mg2_all_visited():
            return
        score = 0
        for area in range(len(store.mg2_cards)):
            for j, card in enumerate(store.mg2_cards[area]):
                selected = store.mg2_selected[area][j]
                if card["correct"]:
                    score += MG2_POINTS_HIT if selected else -MG2_POINTS_MISS
                elif selected:
                    score -= MG2_POINTS_MISS
        store.mg2_score = max(0, score)
        store.mg2_phase = "review"
        store.mg2_area = 0
        mg2_sfx("correct" if store.mg2_score >= store.mg2_max_score else "wrong")

    def mg2_verdict():
        """Frase de feedback conforme o desempenho."""
        ratio = float(store.mg2_score) / max(1, store.mg2_max_score)
        if ratio >= 1.0:
            return _("Exame perfeito! Todos os sinais de AIE foram identificados.")
        elif ratio >= 0.7:
            return _("Bom exame! Mas alguns sinais passaram despercebidos.")
        else:
            return _("Revise os sinais clínicos da AIE e tente de novo.")


## -----------------------------------------------------------------------
## 1.5) TELA DE INSTRUÇÕES
##    Uso: call screen minigame2_instructions
##    Modal: bloqueia qualquer clique no que estiver atrás até "Entendi".
## -----------------------------------------------------------------------
init python:

    # IMAGEM: minigame2/mg2_instructions_bg.png — fundo cheio das instruções.
    # Tamanho final: 1920x1080 → exporte o PNG a 960x540.
    MG2_INSTR_BG = mg2_art("mg2_instructions_bg.png", (1920, 1080),
                           "FUNDO: instruções\n(mg2_instructions_bg.png)", "#2a2418")

    # IMAGEM: minigame2/mg2_instructions_panel.png — moldura do texto de regras.
    # Tamanho final: 1200x600 → exporte o PNG a 600x300.
    MG2_INSTR_PANEL = mg2_art("mg2_instructions_panel.png", (1200, 600),
                              "MOLDURA DE TEXTO\n(mg2_instructions_panel.png)", "#4a3a20")

style mg2_instructions_text:
    xalign 0.5
    yalign 0.5
    text_align 0.5
    color "#ffffff"
    size 30
    xsize 1000


screen minigame2_instructions():

    modal True  # impede qualquer clique/interação com o jogo por trás

    add MG2_INSTR_BG

    fixed:
        xalign 0.5
        yalign 0.45
        xysize (1200, 600)
        add MG2_INSTR_PANEL

        # Texto de regras de exemplo — edite como quiser
        text _("Um cavalo chegou para exame clínico!\n\nEm cada área do exame, marque os achados COMPATÍVEIS com a Anemia Infecciosa Equina e deixe sem marcar os que não combinam. Examine todas as áreas antes de concluir.\n\nMarcar um sinal certo dá pontos; marcar um errado, ou deixar passar um sinal da doença, tira pontos.") style "mg2_instructions_text" xalign 0.5 yalign 0.5

    # Botão "Entendi" / "Fechar" — libera o jogador para o minigame.
    # IMAGEM: minigame2/mg2_close_idle.png e mg2_close_hover.png.
    # Tamanho final: 240x80 → exporte cada PNG a 120x40.
    imagebutton:
        xalign 0.5
        yalign 0.85
        idle mg2_art("mg2_close_idle.png", (240, 80), "ENTENDI\n(mg2_close_idle.png)", "#3a5a3a")
        hover mg2_art("mg2_close_hover.png", (240, 80), "ENTENDI\n(mg2_close_hover.png)", "#4f7a4f")
        focus_mask True
        action [
            Play("sound", "audio/sfx_click.ogg"),
            Return(True),  # devolve o controle ao "call screen" que a chamou
        ]
        hovered Play("sound", "audio/sfx_hover.ogg")


## -----------------------------------------------------------------------
## 2) TELA DO MINIGAME
## -----------------------------------------------------------------------
screen minigame2_gameplay():

    modal True  # bloqueia qualquer interação com o que estiver atrás

    add MG2_BG

    # ---- Painel de título / objetivo (canto superior esquerdo) ----------
    # Se a sua arte do painel já tiver o texto desenhado, apague os 2 textos abaixo.
    fixed:
        pos (60, 40)
        xysize (820, 170)
        add MG2_TITLE_PANEL
        text _("2 - EXAME CLÍNICO"):
            xpos 30
            ypos 25
            size 34
            color "#ffffff"
        text _("Marque os achados compatíveis com a AIE em cada área do exame."):
            xpos 30
            ypos 95
            size 24
            color "#ffffff"
            xmaximum 760

    # ---- Abas: as 6 áreas do exame (cada aba é uma imagem própria, com o ----
    # ---- nome já desenhado; nenhum texto do Ren'Py) -----------------------
    for i, area in enumerate(MG2_AREAS):

        $ tab_art = MG2_TAB_ART[i]["active"] if i == mg2_area else MG2_TAB_ART[i]["idle"]
        $ tab_visited = mg2_visited[i]

        button:
            pos (MG2_TABS_X, MG2_TABS_Y0 + i * MG2_TABS_STEP)
            xysize MG2_TAB_SIZE
            background None
            focus_mask True
            action Function(mg2_select_area, i)
            hovered Function(mg2_sfx, "hover")
            add tab_art
            if tab_visited:
                add MG2_TAB_VISITED

    # ---- Cartas de achados da área aberta --------------------------------
    $ area_label = MG2_AREAS[mg2_area]["label"]

    text "[area_label!t]":
        xpos MG2_CARDS_X
        ypos 200
        size 44
        bold True
        color "#ffffff"

    for j, card in enumerate(mg2_cards[mg2_area]):

        $ card_state = mg2_card_state(mg2_area, j)

        button:
            pos (MG2_CARDS_X, MG2_CARDS_Y0 + j * MG2_CARDS_STEP)
            xysize MG2_CARD_SIZE
            background None
            focus_mask True
            action Function(mg2_toggle, mg2_area, j)
            hovered Function(mg2_sfx, "hover")
            add MG2_CARD_ART[card_state]
            add mg2_finding_art(card)

    # ---- Rodapé: concluir (jogando) ou resultado + continuar (revisão) ---
    if mg2_phase == "exam":

        imagebutton:
            pos MG2_SUBMIT_POS
            idle MG2_SUBMIT_IDLE
            hover MG2_SUBMIT_HOVER
            insensitive MG2_SUBMIT_DISABLED
            sensitive mg2_all_visited()
            focus_mask True
            action Function(mg2_submit)
            hovered Function(mg2_sfx, "hover")

        if not mg2_all_visited():
            text _("Examine todas as áreas para poder concluir."):
                xpos MG2_SUBMIT_POS[0] + MG2_SUBMIT_SIZE[0] + 30
                ypos MG2_SUBMIT_POS[1] + 25
                size 24
                color "#ffffff"

    else:

        $ verdict = mg2_verdict()

        text _("Pontuação: [mg2_score] / [mg2_max_score]"):
            xpos 60
            ypos 980
            size 40
            color "#ffffff"

        text "[verdict!t]":
            xpos 60
            ypos 1030
            size 26
            color "#ffffff"
            xmaximum 900

        imagebutton:
            pos MG2_SUBMIT_POS
            idle MG2_CONTINUE_IDLE
            hover MG2_CONTINUE_HOVER
            focus_mask True
            action [Play("sound", "audio/sfx_click.ogg"), Return(True)]
            hovered Function(mg2_sfx, "hover")

        # Legenda das cores da revisão
        text _("Verde = acerto   Vermelho = marcou errado   Amarelo = faltou marcar"):
            xpos MG2_SUBMIT_POS[0]
            ypos MG2_SUBMIT_POS[1] - 50
            size 24
            color "#ffffff"


## -----------------------------------------------------------------------
## 3) LABEL DO GAMEPLAY (motor do minigame em si)
## -----------------------------------------------------------------------
label minigame_2_gameplay:

    $ quick_menu = False       # esconde os botões rápidos do rodapé durante o minigame
    $ renpy.block_rollback()   # impede que o rollback (roda do mouse) bagunce o estado
    $ mg2_reset()              # sorteia os achados (permite rejogar do zero)

    scene black
    call screen minigame2_gameplay   # só retorna quando o jogador clica em "Continuar"

    $ quick_menu = True
    return


## -----------------------------------------------------------------------
## 4) PONTO DE ENTRADA (chamado pelo roadmap.rpy: "call expression 'minigame_2_entry'")
##    Mostra as instruções, roda o gameplay e avisa o mapa que terminou.
## -----------------------------------------------------------------------
label minigame_2_entry:

    call screen minigame2_instructions
    call minigame_2_gameplay

    $ mg_report_score(2, mg2_score, mg2_max_score)  # registra o placar e a medalha, se for o caso
    $ mg_complete(2)                                 # marca como concluído e libera o 3

    return
