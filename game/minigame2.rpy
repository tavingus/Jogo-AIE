################################################################################
# MINIGAME2.RPY
# Minigame 2: "Exame clínico" — sinais compatíveis com a AIE
#
# Como funciona:
#   - O jogador examina o cavalo em 6 ÁREAS (abas): Temperatura, Mucosas,
#     Linfonodos, Estado geral, Histórico e Hemograma.
#   - Cada área mostra uma lista fixa de ACHADOS (cartas). Alguns são
#     compatíveis com a AIE e outros não (distratores).
#   - O jogador MARCA (clique) os achados que considera compatíveis com a AIE.
#     Clicar de novo desmarca.
#   - Só dá para concluir o exame depois de examinar TODAS as áreas.
#   - Ao concluir, entra a fase de REVISÃO: cada carta fica VERDE (acerto),
#     VERMELHA (marcou errado) ou AMARELA (era compatível e faltou marcar). O
#     jogador navega pelas abas para ver onde errou e clica em "Continuar".
#
# Pontuação (ver roadmap.rpy para o sistema de medalhas):
#   + MG2_POINTS_HIT   por achado compatível marcado (acerto)
#   - MG2_POINTS_MISS  por achado marcado que NÃO é compatível (erro)
#   - MG2_POINTS_MISS  por achado compatível que ficou sem marcar (faltou)
#   Achado não compatível e não marcado: neutro (0). O placar nunca fica
#   abaixo de 0. Pontuação máxima = marcar exatamente todos os compatíveis.
#
# ARTE (mesmo esquema do menu e do roadmap):
#   TODA arte real é um PNG de CANVAS INTEIRO (960x540), com o elemento já na
#   posição certa. O jogo amplia 2x (nearest neighbor) e desenha em (0, 0), sem
#   usar posição do código; focus_mask True faz só os pixels opacos do botão
#   responderem ao mouse.
#   Enquanto o PNG não existe, aparece um retângulo placeholder colorido com
#   texto, na posição definida pelas constantes MG2_*_RECT abaixo. (Essas
#   constantes só servem aos placeholders: a arte real ignora todas elas.)
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

    # ---- Posições dos PLACEHOLDERS (tela 1920x1080): (x, y, largura, altura)
    MG2_MAX_SLOTS = 6                       # máximo de cartas por área

    def mg2_tab_rect(i):                    # abas, coluna da esquerda
        return (60, 240 + i * 105, 520, 90)

    def mg2_slot_rect(k):                   # cartas, painel da direita
        return (1000, 260 + k * 115, 820, 100)

    MG2_SUBMIT_RECT = (60, 900, 520, 100)   # botão Concluir exame / Continuar

    # ---- Regras ------------------------------------------------------------
    MG2_POINTS_HIT = 10          # acerto: compatível marcado
    MG2_POINTS_MISS = 5          # erro: perde isto (marcou errado OU deixou de marcar)

    # ---- Achados por área --------------------------------------------------
    # Cada achado é ("id", texto, compatível?). A ORDEM define o slot (1º achado
    # = slot 1 etc.), já que a arte de cada carta tem a posição fixa no canvas.
    # "id" forma o nome do PNG do texto do achado: achado_<id>.png.
    # O texto só aparece no placeholder enquanto o PNG não existe.
    # Os achados COMPATÍVEIS vêm da sua lista de sinais; os distratores eu
    # inventei — revise! (máximo MG2_MAX_SLOTS achados por área)
    MG2_AREAS = [
        {
            "id": "temperatura",
            "label": _("Temperatura"),
            "findings": [
                ("febre", _("Febre (temperatura elevada)"), True),
                ("hipotermia", _("Hipotermia (temperatura baixa)"), False),
                ("febre_recorrente", _("Febre em episódios recorrentes"), True),
                ("temp_abaixo", _("Temperatura sempre abaixo do normal"), False),
            ],
        },
        {
            "id": "mucosas",
            "label": _("Mucosas"),
            "findings": [
                ("mucosas_rosadas", _("Mucosas rosadas e úmidas"), False),
                ("mucosas_palidas", _("Mucosas pálidas"), True),
                ("mucosas_cianoticas", _("Mucosas cianóticas (azuladas)"), False),
                ("petequias", _("Petéquias nas mucosas"), True),
            ],
        },
        {
            "id": "linfonodos",
            "label": _("Linfonodos"),
            "findings": [
                ("linfonodos_abscesso", _("Linfonodos com abscesso drenando"), False),
                ("linfonodos_aumentados", _("Linfonodos aumentados"), True),
                ("linfonodos_atrofiados", _("Linfonodos atrofiados"), False),
                ("linfonodos_normais", _("Ausência de qualquer alteração palpável"), False),
            ],
        },
        {
            "id": "estado_geral",
            "label": _("Estado geral"),
            "findings": [
                ("letargia", _("Letargia"), True),
                ("hiperexcitabilidade", _("Hiperexcitabilidade e agitação"), False),
                ("perda_peso", _("Perda de peso"), True),
                ("ganho_peso", _("Ganho de peso acentuado"), False),
                ("fraqueza", _("Fraqueza"), True),
                ("queda_desempenho", _("Queda de desempenho"), True),
            ],
        },
        {
            "id": "historico",
            "label": _("Histórico"),
            "findings": [
                ("hist_vacinado", _("Vacinação em dia, sem outros achados"), False),
                ("hist_febre", _("Febre recorrente"), True),
                ("hist_sangue", _("Exposição a sangue (agulhas ou instrumentos)"), True),
                ("hist_isolado", _("Animal isolado, sem insetos nem outros equídeos"), False),
                ("hist_insetos", _("Contato com insetos hematófagos"), True),
                ("hist_infectados", _("Contato com animais infectados"), True),
            ],
        },
        {
            "id": "hemograma",
            "label": _("Hemograma"),
            "findings": [
                ("anemia", _("Anemia"), True),
                ("policitemia", _("Policitemia (Ht alto)"), False),
                ("hb_baixa", _("Hemoglobina (Hb) baixa"), True),
                ("hb_alta", _("Hemoglobina (Hb) acima do normal"), False),
                ("ht_baixo", _("Hematócrito (Ht) baixo"), True),
                ("trombocitopenia", _("Trombocitopenia (plaquetas baixas)"), True),
            ],
        },
    ]

    # Pontuação máxima: todos os achados compatíveis marcados
    MG2_MAX_SCORE = MG2_POINTS_HIT * sum(
        1 for area in MG2_AREAS for f in area["findings"] if f[2])

    # ---- Placeholders de arte ----------------------------------------------
    def mg2_art(filename, rect, label, color, fill=True):
        """Arte de canvas inteiro (960x540 → 1920x1080, nearest neighbor,
        desenhada em (0, 0)) se o PNG existir. Senão, um placeholder: retângulo
        colorido com texto na posição "rect" = (x, y, largura, altura).
        fill=False = placeholder só com o texto, sem retângulo (para camadas
        de texto sobre uma moldura)."""
        path = MG2_ART_DIR + filename
        if renpy.loadable(path):
            return Transform(Image(path, nearest_neighbor=True), zoom=MG2_ZOOM)

        x, y, w, h = rect
        text = Text(label, size=26, color="#ffffff", xalign=0.5, yalign=0.5,
                    text_align=0.5, xmaximum=w - 20)
        if fill:
            box = Fixed(Solid(color, xysize=(w, h)), text, xysize=(w, h))
        else:
            box = Fixed(text, xysize=(w, h))
        return Fixed(Transform(box, pos=(x, y)), xysize=(1920, 1080))

    # IMAGEM: minigame2/mg2_bg.png — fundo cheio: baia/consultório com o cavalo.
    # Canvas 960x540. (Deixe livres a coluna das abas e a das cartas.)
    MG2_BG = mg2_art("mg2_bg.png", (0, 0, 1920, 1080), "FUNDO: cavalo em exame\n(mg2_bg.png)", "#2f3a3a")

    # IMAGEM: minigame2/mg2_title_panel.png — painel de título (canto superior
    # esquerdo). Canvas 960x540, painel já na posição.
    MG2_TITLE_PANEL = mg2_art("mg2_title_panel.png", (60, 40, 820, 170), "PAINEL DE TÍTULO\n(mg2_title_panel.png)", "#4a3a20")

    # IMAGEM: minigame2/aba_<area>_<estado>.png — as ABAS, com o nome da área
    # já desenhado. Canvas 960x540, a aba já na posição dela. 18 arquivos
    # (6 áreas x 3 estados). <area> = temperatura, mucosas, linfonodos,
    # estado_geral, historico, hemograma. Estados:
    #   idle    = aba ainda não examinada
    #   active  = aba aberta agora
    #   visited = aba já examinada (e não é a aberta)
    def mg2_build_tab_art():
        colors = {"idle": "#4a4a4a", "active": "#2c6e8a", "visited": "#3a5a3a"}
        result = []
        for i, area in enumerate(MG2_AREAS):
            entry = {}
            for state, color in colors.items():
                fname = "aba_%s_%s.png" % (area["id"], state)
                entry[state] = mg2_art(fname, mg2_tab_rect(i),
                                       "%s\n(%s)" % (area["label"], fname), color)
            result.append(entry)
        return result

    MG2_TAB_ART = mg2_build_tab_art()

    # IMAGEM: minigame2/mg2_carta_<slot>_<estado>.png — a MOLDURA (botão) de
    # cada carta, sem texto. Canvas 960x540, a moldura já na posição do slot
    # (<slot> = 1 a 6; as molduras valem para todas as áreas). 30 arquivos.
    # Estados:
    #   idle      = carta não marcada
    #   selected  = carta marcada (durante o exame)
    #   verde     = revisão: marcou e era compatível (ACERTO)
    #   amarelo   = revisão: era compatível e FALTOU marcar
    #   vermelho  = revisão: marcou e NÃO era compatível (ERRO)
    MG2_CARD_COLORS = {
        "idle": "#4a4a4a", "selected": "#2c6e8a", "verde": "#2e7d32",
        "amarelo": "#9a7a1c", "vermelho": "#8a2c2c",
    }

    def mg2_build_card_art():
        result = []
        for k in range(MG2_MAX_SLOTS):
            entry = {}
            for state, color in MG2_CARD_COLORS.items():
                fname = "mg2_carta_%d_%s.png" % (k + 1, state)
                entry[state] = mg2_art(fname, mg2_slot_rect(k), "", color)
            result.append(entry)
        return result

    MG2_CARD_ART = mg2_build_card_art()

    # IMAGEM: minigame2/achado_<id>.png — o TEXTO de cada achado, já desenhado
    # e em fundo TRANSPARENTE (fica por cima da moldura). Canvas 960x540, texto
    # já na posição do slot em que o achado aparece. Um arquivo por achado; os
    # ids estão em MG2_AREAS (ex.: achado_febre.png, achado_petequias.png).
    def mg2_build_finding_art():
        result = []
        for area in MG2_AREAS:
            row = []
            for k, (fid, text, ok) in enumerate(area["findings"]):
                fname = "achado_%s.png" % fid
                row.append(mg2_art(fname, mg2_slot_rect(k),
                                   "%s\n(%s)" % (text, fname), "#000000", fill=False))
            result.append(row)
        return result

    MG2_FINDING_ART = mg2_build_finding_art()

    # IMAGEM: minigame2/mg2_concluir_idle.png, mg2_concluir_hover.png e
    # mg2_concluir_disabled.png — botão "Concluir exame", com o texto desenhado.
    # Canvas 960x540, botão já na posição. (disabled = antes de examinar tudo)
    MG2_SUBMIT_IDLE = mg2_art("mg2_concluir_idle.png", MG2_SUBMIT_RECT, "CONCLUIR EXAME\n(mg2_concluir_idle.png)", "#3a5a3a")
    MG2_SUBMIT_HOVER = mg2_art("mg2_concluir_hover.png", MG2_SUBMIT_RECT, "CONCLUIR EXAME\n(mg2_concluir_hover.png)", "#4f7a4f")
    MG2_SUBMIT_DISABLED = mg2_art("mg2_concluir_disabled.png", MG2_SUBMIT_RECT, "CONCLUIR EXAME\n(mg2_concluir_disabled.png)", "#2a2a2a")

    # IMAGEM: minigame2/mg2_continuar_idle.png e mg2_continuar_hover.png — botão
    # "Continuar" da revisão, com o texto desenhado. Canvas 960x540, botão já na
    # posição (pode ser a mesma do Concluir).
    MG2_CONTINUE_IDLE = mg2_art("mg2_continuar_idle.png", MG2_SUBMIT_RECT, "CONTINUAR\n(mg2_continuar_idle.png)", "#3a5a3a")
    MG2_CONTINUE_HOVER = mg2_art("mg2_continuar_hover.png", MG2_SUBMIT_RECT, "CONTINUAR\n(mg2_continuar_hover.png)", "#4f7a4f")

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
default mg2_selected = []     # por área: lista de bool (carta marcada?)
default mg2_visited = []      # por área: já foi examinada?
default mg2_area = 0          # área aberta agora
default mg2_phase = "exam"    # "exam" (jogando) ou "review" (revisão após concluir)
default mg2_score = 0


init python:

    def mg2_reset():
        """Nova partida: zera as marcações."""
        store.mg2_selected = [[False] * len(a["findings"]) for a in MG2_AREAS]
        store.mg2_visited = [False] * len(MG2_AREAS)
        store.mg2_visited[0] = True
        store.mg2_area = 0
        store.mg2_phase = "exam"
        store.mg2_score = 0

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

    def mg2_tab_state(i):
        if i == store.mg2_area:
            return "active"
        return "visited" if store.mg2_visited[i] else "idle"

    def mg2_card_state(area, j):
        """Estado visual da carta: idle/selected (jogando) ou
        verde/amarelo/vermelho (revisão)."""
        selected = store.mg2_selected[area][j]
        correct = MG2_AREAS[area]["findings"][j][2]
        if store.mg2_phase == "exam":
            return "selected" if selected else "idle"
        if selected and correct:
            return "verde"
        if selected and not correct:
            return "vermelho"
        if correct:
            return "amarelo"
        return "idle"

    def mg2_submit():
        """Conclui o exame: calcula a pontuação e entra na fase de revisão."""
        if store.mg2_phase != "exam" or not mg2_all_visited():
            return
        score = 0
        for a, area in enumerate(MG2_AREAS):
            for j, (fid, text, correct) in enumerate(area["findings"]):
                selected = store.mg2_selected[a][j]
                if correct:
                    score += MG2_POINTS_HIT if selected else -MG2_POINTS_MISS
                elif selected:
                    score -= MG2_POINTS_MISS
        store.mg2_score = max(0, score)
        store.mg2_phase = "review"
        store.mg2_area = 0
        mg2_sfx("correct" if store.mg2_score >= MG2_MAX_SCORE else "wrong")

    def mg2_verdict():
        """Frase de feedback conforme o desempenho."""
        ratio = float(store.mg2_score) / max(1, MG2_MAX_SCORE)
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
##    (mesma estrutura do minigame 1)
## -----------------------------------------------------------------------
init python:

    # Estas 4 artes seguem o esquema do minigame 1 (peças exportadas na METADE
    # do tamanho final e posicionadas pelo código).
    def mg2_instr_art(filename, size, label, color):
        path = MG2_ART_DIR + filename
        if renpy.loadable(path):
            return Transform(Image(path, nearest_neighbor=True), zoom=MG2_ZOOM)
        return Fixed(
            Solid(color, xysize=size),
            Text(label, size=28, color="#ffffff", xalign=0.5, yalign=0.5,
                 text_align=0.5, xmaximum=size[0] - 20),
            xysize=size,
        )

    # IMAGEM: minigame2/mg2_instructions_bg.png — fundo cheio das instruções.
    # Tamanho final: 1920x1080 → exporte o PNG a 960x540.
    MG2_INSTR_BG = mg2_instr_art("mg2_instructions_bg.png", (1920, 1080),
                                 "FUNDO: instruções\n(mg2_instructions_bg.png)", "#2a2418")

    # IMAGEM: minigame2/mg2_instructions_panel.png — moldura do texto de regras.
    # Tamanho final: 1200x600 → exporte o PNG a 600x300.
    MG2_INSTR_PANEL = mg2_instr_art("mg2_instructions_panel.png", (1200, 600),
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
        idle mg2_instr_art("mg2_close_idle.png", (240, 80), "ENTENDI\n(mg2_close_idle.png)", "#3a5a3a")
        hover mg2_instr_art("mg2_close_hover.png", (240, 80), "ENTENDI\n(mg2_close_hover.png)", "#4f7a4f")
        focus_mask True
        action [
            Play("sound", "audio/sfx_click.ogg"),
            Return(True),  # devolve o controle ao "call screen" que a chamou
        ]
        hovered Play("sound", "audio/sfx_hover.ogg")


## -----------------------------------------------------------------------
## 2) TELA DO MINIGAME
##    Todo botão é uma arte de canvas inteiro (1920x1080 na tela), desenhada
##    em (0, 0); focus_mask True limita o clique aos pixels opacos da arte.
## -----------------------------------------------------------------------
screen minigame2_gameplay():

    modal True  # bloqueia qualquer interação com o que estiver atrás

    # Fundo cheio
    add MG2_BG

    # Painel de título / objetivo
    add MG2_TITLE_PANEL
    # Se a sua arte do painel já tiver o texto desenhado, apague os 2 textos abaixo.
    text _("2 - EXAME CLÍNICO"):
        xpos 90
        ypos 65
        size 34
        color "#ffffff"
    text _("Marque os achados compatíveis com a AIE em cada área do exame."):
        xpos 90
        ypos 135
        size 24
        color "#ffffff"
        xmaximum 760

    # ---- Abas: as 6 áreas do exame --------------------------------------
    for i, area in enumerate(MG2_AREAS):

        $ tab_state = mg2_tab_state(i)

        button:
            xysize (1920, 1080)
            background None
            focus_mask True
            action Function(mg2_select_area, i)
            hovered Function(mg2_sfx, "hover")
            add MG2_TAB_ART[i][tab_state]

    # ---- Cartas de achados da área aberta -------------------------------
    for j in range(len(MG2_AREAS[mg2_area]["findings"])):

        $ card_state = mg2_card_state(mg2_area, j)

        button:
            xysize (1920, 1080)
            background None
            focus_mask True
            action Function(mg2_toggle, mg2_area, j)
            hovered Function(mg2_sfx, "hover")
            add MG2_CARD_ART[j][card_state]
            add MG2_FINDING_ART[mg2_area][j]

    # ---- Concluir (jogando) ou resultado + continuar (revisão) -----------
    if mg2_phase == "exam":

        imagebutton:
            idle MG2_SUBMIT_IDLE
            hover MG2_SUBMIT_HOVER
            insensitive MG2_SUBMIT_DISABLED
            sensitive mg2_all_visited()
            focus_mask True
            action Function(mg2_submit)
            hovered Function(mg2_sfx, "hover")

        if not mg2_all_visited():
            text _("Examine todas as áreas para poder concluir."):
                xpos 60
                ypos 1010
                size 24
                color "#ffffff"

    else:

        $ verdict = mg2_verdict()

        imagebutton:
            idle MG2_CONTINUE_IDLE
            hover MG2_CONTINUE_HOVER
            focus_mask True
            action [Play("sound", "audio/sfx_click.ogg"), Return(True)]
            hovered Function(mg2_sfx, "hover")

        text _("Pontuação: [mg2_score] / [MG2_MAX_SCORE]"):
            xpos 1000
            ypos 960
            size 40
            color "#ffffff"

        text "[verdict!t]":
            xpos 1000
            ypos 1015
            size 26
            color "#ffffff"
            xmaximum 820

        # Legenda das cores da revisão
        text _("Verde = acerto   Vermelho = marcou errado   Amarelo = faltou marcar"):
            xpos 60
            ypos 1010
            size 24
            color "#ffffff"


## -----------------------------------------------------------------------
## 3) LABEL DO GAMEPLAY (motor do minigame em si)
## -----------------------------------------------------------------------
label minigame_2_gameplay:

    $ quick_menu = False       # esconde os botões rápidos do rodapé durante o minigame
    $ renpy.block_rollback()   # impede que o rollback (roda do mouse) bagunce o estado
    $ mg2_reset()              # zera as marcações (permite rejogar do zero)

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

    $ mg_report_score(2, mg2_score, MG2_MAX_SCORE)  # registra o placar e a medalha, se for o caso
    $ mg_complete(2)                                 # marca como concluído e libera o 3

    return
