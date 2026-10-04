################################################################################
# MINIGAME3.RPY
# Minigame 3: "Coleta de exame" — coleta de sangue para o exame de AIE no
# cavalo campeão "Golias da Natureza", que será transportado para uma competição.
#
# O cavalo fica no lado ESQUERDO da tela (faz parte da arte de fundo); todas as
# opções ficam no lado DIREITO. O jogador segue 5 etapas, na ordem:
#
#   1. TUBO        — escolher o tubo certo (sem anticoagulante / EDTA / heparina)
#   2. VIA/LOCAL   — jugular (endovenosa) / garupa (intramuscular) / dorso (subcutânea)
#   3. ETIQUETA    — identificar a amostra: confere a FICHA do animal e preenche
#                    Identificação, Propriedade e Data da coleta (clicar no campo
#                    troca a opção, em ciclo) e confirma
#   4. RESENHA     — (opcional) preencher Idade, Sexo e Pelagem do animal
#   5. CAIXA       — colocar a amostra na caixa refrigerada e enviar ao laboratório
#
# Pontuação (ver roadmap.rpy para o sistema de medalhas):
#   + MG3_POINTS_HIT   por conduta correta (opção certa / campo certo)
#   - MG3_POINTS_MISS  por conduta errada (opção errada / campo errado confirmado)
#   Nas etapas de escolha (1, 2 e 5) o jogador só avança quando acerta; cada erro
#   mostra o motivo e custa pontos. Nas etapas 3 e 4 cada campo certo trava
#   (fica verde) e os errados ficam vermelhos até serem corrigidos. A resenha
#   pode ser PULADA (sem penalidade, mas perde os pontos dos campos).
#   O placar nunca fica abaixo de 0. Pontuação máxima = nenhum erro.
#   A pontuação aparece ao final, na tela de resultado.
#
# ARTE (mesmo esquema dos outros minigames):
#   Se o PNG não existir em game/images/minigame3/, aparece um retângulo
#   placeholder colorido com texto, já no tamanho final. Todo PNG real é
#   exibido com zoom 2.0 + nearest neighbor: exporte na METADE do tamanho
#   indicado em cada "# IMAGEM:" (arte a 960x540 = tela 1920x1080).
#   Os TEXTOS das opções e dos campos são escritos pelo jogo por cima das
#   molduras.
#
# Este arquivo contém: dados/configuração, lógica, tela de instruções, tela
# do gameplay e o "label minigame_3_entry" — chamado pelo roadmap.rpy.
################################################################################


## -----------------------------------------------------------------------
## 1) CONFIGURAÇÃO, DADOS E LÓGICA
## -----------------------------------------------------------------------
init python:

    MG3_ART_DIR = "images/minigame3/"
    MG3_ZOOM = 2.0  # arte a 960x540, exibida em 1920x1080

    # ---- Layout (tela 1920x1080) — tudo na coluna da DIREITA ----------------
    # (o cavalo ocupa a esquerda, na arte de fundo)
    MG3_COL_X = 1000                  # x da coluna de opções
    MG3_COL_W = 880                   # largura da coluna

    MG3_TITLE_POS = (MG3_COL_X, 30)
    MG3_TITLE_SIZE = (MG3_COL_W, 130)             # exporte a 440x65

    MG3_STEP_Y = 175                  # y do cabeçalho da etapa
    MG3_PROMPT_Y = 222                # y do enunciado da etapa

    # Etapas de ESCOLHA (3 opções empilhadas)
    MG3_OPT_Y0 = 300
    MG3_OPT_STEP = 150
    MG3_OPT_SIZE = (MG3_COL_W, 130)               # exporte a 440x65

    # Etapas de CAMPOS (etiqueta e resenha): ficha + 3 campos
    MG3_FICHA_POS = (MG3_COL_X, 280)
    MG3_FICHA_SIZE = (MG3_COL_W, 240)             # exporte a 440x120
    MG3_FIELD_Y0 = 545
    MG3_FIELD_STEP = 110
    MG3_FIELD_SIZE = (MG3_COL_W, 100)             # exporte a 440x50

    MG3_FEEDBACK_Y = 868              # mensagem de feedback (acerto/erro)
    MG3_BTN_Y = 940
    MG3_BTN_SIZE = (420, 90)                      # exporte a 210x45

    # ---- Regras ------------------------------------------------------------
    MG3_POINTS_HIT = 10
    MG3_POINTS_MISS = 5
    MG3_END_BTN_SIZE = MG3_BTN_SIZE

    # ---- Ficha do animal (dados que o jogador deve conferir) ----------------
    # Edite à vontade: as opções das etapas 3 e 4 usam estes dados.
    MG3_PROFILE = {
        "name": "Golias da Natureza",
        "farm": "Haras Vale Verde",
        "date": "12/03/2025",
        "age": "8 anos",
        "sex": "Macho",
        "coat": "Castanha",
    }

    # ---- Etapas ------------------------------------------------------------
    # kind "choice": "options" = (texto, correta?, feedback).
    # kind "fields": cada campo tem "options" e a PRIMEIRA opção é a correta
    #                (a ordem é embaralhada a cada partida).
    MG3_STEPS = [
        {
            "id": "tubo",
            "kind": "choice",
            "title": _("Escolha do tubo"),
            "prompt": _("Qual tubo usar para colher o sangue do exame sorológico?"),
            "options": [
                (_("Tubo sem anticoagulante"), True,
                 _("Correto! Sem anticoagulante o sangue coagula e permite obter o soro, necessário para o exame sorológico.")),
                (_("Tubo com EDTA"), False,
                 _("O EDTA é um anticoagulante: o sangue não coagula e não se obtém soro para a sorologia.")),
                (_("Tubo com heparina"), False,
                 _("A heparina também é um anticoagulante e impede a formação do soro.")),
            ],
        },
        {
            "id": "via",
            "kind": "choice",
            "title": _("Local e via de coleta"),
            "prompt": _("Onde e como colher o sangue do cavalo?"),
            "options": [
                (_("Coleta endovenosa na veia jugular"), True,
                 _("Correto! O sangue para análise é colhido da veia jugular.")),
                (_("Aplicação intramuscular na garupa"), False,
                 _("A via intramuscular serve para aplicar medicamentos, não para colher sangue.")),
                (_("Aplicação subcutânea no dorso"), False,
                 _("A via subcutânea também é de aplicação; não permite colher sangue para o exame.")),
            ],
        },
        {
            "id": "etiqueta",
            "kind": "fields",
            "title": _("Identificação da amostra"),
            "prompt": _("Confira a ficha do animal e preencha a etiqueta do tubo."),
            "show_profile": True,
            "skippable": False,
            "fields": [
                {"label": _("Cavalo"),
                 "options": [MG3_PROFILE["name"], "Golias do Vale", "Gigante da Natureza"]},
                {"label": _("Propriedade"),
                 "options": [MG3_PROFILE["farm"], "Haras Campo Verde", "Fazenda Vale Verde"]},
                {"label": _("Data da coleta"),
                 "options": [MG3_PROFILE["date"], "11/03/2025", "21/03/2025"]},
            ],
        },
        {
            "id": "resenha",
            "kind": "fields",
            "title": _("Resenha do animal"),
            "prompt": _("Preencha a resenha com os dados da ficha (opcional)."),
            "show_profile": True,
            "skippable": True,
            "fields": [
                {"label": _("Idade"),
                 "options": [MG3_PROFILE["age"], "3 anos", "15 anos"]},
                {"label": _("Sexo"),
                 "options": [MG3_PROFILE["sex"], "Fêmea", "Macho castrado"]},
                {"label": _("Pelagem"),
                 "options": [MG3_PROFILE["coat"], "Alazã", "Tordilha"]},
            ],
        },
        {
            "id": "caixa",
            "kind": "choice",
            "title": _("Transporte da amostra"),
            "prompt": _("Onde colocar a amostra para enviá-la ao laboratório?"),
            "options": [
                (_("Caixa isotérmica refrigerada (com gelo)"), True,
                 _("Correto! A amostra deve seguir refrigerada até o laboratório.")),
                (_("Caixa de papelão em temperatura ambiente"), False,
                 _("Sem refrigeração a amostra pode se deteriorar e comprometer o resultado.")),
                (_("Porta-luvas do carro, ao sol"), False,
                 _("O calor degrada a amostra: ela precisa ir refrigerada.")),
            ],
        },
    ]

    def mg3_count_hits():
        n = 0
        for st in MG3_STEPS:
            n += 1 if st["kind"] == "choice" else len(st["fields"])
        return n

    # Pontuação máxima: todas as condutas certas, sem nenhum erro
    MG3_MAX_SCORE = mg3_count_hits() * MG3_POINTS_HIT

    # ---- Placeholders de arte ----------------------------------------------
    def mg3_art(filename, size, label, color):
        """Imagem real (ampliada 2x, nearest neighbor; exporte na metade de
        "size") se o arquivo existir, senão um retângulo colorido com texto
        já no tamanho final."""
        path = MG3_ART_DIR + filename
        if renpy.loadable(path):
            return Transform(Image(path, nearest_neighbor=True), zoom=MG3_ZOOM)
        return Fixed(
            Solid(color, xysize=size),
            Text(label, size=26, color="#ffffff", xalign=0.5, yalign=0.5,
                 text_align=0.5, xmaximum=size[0] - 20),
            xysize=size,
        )

    # IMAGEM: minigame3/mg3_bg.png — fundo cheio: área de atendimento com o
    # "Golias da Natureza" no lado ESQUERDO (a coluna da direita, x>=1000, fica
    # livre para as opções). Tamanho final: 1920x1080 → exporte a 960x540.
    MG3_BG = mg3_art("mg3_bg.png", (1920, 1080), "FUNDO: cavalo à esquerda\n(mg3_bg.png)", "#3a4a3a")

    # IMAGEM: minigame3/mg3_title_panel.png — painel de título (topo da coluna
    # direita). Tamanho final: 880x130 → exporte a 440x65.
    MG3_TITLE_PANEL = mg3_art("mg3_title_panel.png", MG3_TITLE_SIZE, "PAINEL DE TÍTULO\n(mg3_title_panel.png)", "#4a3a20")

    # IMAGEM: minigame3/mg3_opt_idle.png e mg3_opt_wrong.png — moldura de uma
    # opção das etapas de escolha (sem texto: o texto é escrito pelo jogo).
    # idle = disponível; wrong = opção errada já tentada (vermelha).
    # Tamanho final: 880x130 → exporte a 440x65.
    MG3_OPT_ART = {
        "idle": mg3_art("mg3_opt_idle.png", MG3_OPT_SIZE, "", "#4a4a4a"),
        "wrong": mg3_art("mg3_opt_wrong.png", MG3_OPT_SIZE, "", "#8a2c2c"),
    }

    # IMAGEM: minigame3/mg3_field_idle.png, mg3_field_right.png e
    # mg3_field_wrong.png — moldura de um campo (etiqueta/resenha).
    # idle = a preencher; right = campo certo (travado, verde); wrong = campo
    # errado após confirmar (vermelho). Tamanho final: 880x100 → exporte a 440x50.
    MG3_FIELD_ART = {
        "idle": mg3_art("mg3_field_idle.png", MG3_FIELD_SIZE, "", "#4a4a4a"),
        "right": mg3_art("mg3_field_right.png", MG3_FIELD_SIZE, "", "#2e7d32"),
        "wrong": mg3_art("mg3_field_wrong.png", MG3_FIELD_SIZE, "", "#8a2c2c"),
    }

    # IMAGEM: minigame3/mg3_ficha.png — a "ficha do animal" (prancheta/papel)
    # sobre a qual o jogo escreve os dados. Tamanho final: 880x240 → exporte
    # a 440x120.
    MG3_FICHA = mg3_art("mg3_ficha.png", MG3_FICHA_SIZE, "", "#d8cfa8")

    # IMAGEM: minigame3/mg3_btn_idle.png e mg3_btn_hover.png — botão genérico
    # (Confirmar / Pular resenha / Continuar); o texto é escrito pelo jogo.
    # Tamanho final: 420x90 → exporte a 210x45.
    MG3_BTN_IDLE = mg3_art("mg3_btn_idle.png", MG3_BTN_SIZE, "", "#3a5a3a")
    MG3_BTN_HOVER = mg3_art("mg3_btn_hover.png", MG3_BTN_SIZE, "", "#4f7a4f")

    # IMAGEM: minigame3/mg3_result_panel.png — painel do resultado final.
    # Tamanho final: 1000x420 → exporte a 500x210.
    MG3_RESULT_PANEL = mg3_art("mg3_result_panel.png", (1000, 420), "PAINEL DE RESULTADO\n(mg3_result_panel.png)", "#2e5a3a")

    # ---- Efeitos sonoros (só tocam se o arquivo existir) -------------------
    def mg3_sfx(kind):
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
default mg3_step = 0          # etapa atual (índice em MG3_STEPS)
default mg3_score = 0
default mg3_finished = False  # True depois da última etapa
default mg3_order = []        # por etapa: ordem embaralhada das opções (choice) ou por campo (fields)
default mg3_tried = []        # etapa de escolha: opções erradas já tentadas
default mg3_values = []       # por etapa de campos: posição atual de cada campo (-1 = vazio)
default mg3_locked = []       # por etapa de campos: campo já correto (travado)?
default mg3_wrong = []        # por etapa de campos: campo marcado como errado?
default mg3_feedback = ""     # última mensagem de feedback
default mg3_feedback_ok = True


init python:

    def mg3_reset():
        """Nova partida: embaralha a ordem das opções e zera o estado."""
        order, values, locked, wrong = [], [], [], []
        for st in MG3_STEPS:
            if st["kind"] == "choice":
                perm = list(range(len(st["options"])))
                renpy.random.shuffle(perm)
                order.append(perm)
                values.append([])
                locked.append([])
                wrong.append([])
            else:
                perms = []
                for f in st["fields"]:
                    perm = list(range(len(f["options"])))
                    renpy.random.shuffle(perm)
                    perms.append(perm)
                order.append(perms)
                values.append([-1] * len(st["fields"]))
                locked.append([False] * len(st["fields"]))
                wrong.append([False] * len(st["fields"]))

        store.mg3_order = order
        store.mg3_values = values
        store.mg3_locked = locked
        store.mg3_wrong = wrong
        store.mg3_tried = []
        store.mg3_step = 0
        store.mg3_score = 0
        store.mg3_finished = False
        store.mg3_feedback = ""
        store.mg3_feedback_ok = True

    def mg3_set_feedback(text, ok):
        store.mg3_feedback = text
        store.mg3_feedback_ok = ok

    def mg3_advance():
        """Passa para a próxima etapa (ou encerra a partida)."""
        store.mg3_step += 1
        store.mg3_tried = []
        if store.mg3_step >= len(MG3_STEPS):
            store.mg3_finished = True

    def mg3_hit():
        store.mg3_score += MG3_POINTS_HIT
        mg3_sfx("correct")

    def mg3_miss():
        store.mg3_score = max(0, store.mg3_score - MG3_POINTS_MISS)
        mg3_sfx("wrong")

    # ---- Etapas de escolha ---------------------------------------------------
    def mg3_choose(opt):
        """Clique numa opção (índice em "options") de uma etapa de escolha."""
        if store.mg3_finished or opt in store.mg3_tried:
            return
        text, correct, feedback = MG3_STEPS[store.mg3_step]["options"][opt]
        if correct:
            mg3_hit()
            mg3_set_feedback(feedback, True)
            mg3_advance()
        else:
            store.mg3_tried.append(opt)
            mg3_miss()
            mg3_set_feedback(feedback, False)

    # ---- Etapas de campos (etiqueta e resenha) -----------------------------
    def mg3_field_text(f):
        """Texto exibido no campo f da etapa atual ("" se ainda vazio)."""
        step = MG3_STEPS[store.mg3_step]
        pos = store.mg3_values[store.mg3_step][f]
        if pos < 0:
            return _("(clique para escolher)")
        opt = store.mg3_order[store.mg3_step][f][pos]
        return step["fields"][f]["options"][opt]

    def mg3_cycle(f):
        """Clique num campo: passa para a próxima opção dele (em ciclo)."""
        s = store.mg3_step
        if store.mg3_finished or store.mg3_locked[s][f]:
            return
        n = len(MG3_STEPS[s]["fields"][f]["options"])
        store.mg3_values[s][f] = (store.mg3_values[s][f] + 1) % n
        store.mg3_wrong[s][f] = False
        mg3_sfx("click")

    def mg3_confirm():
        """Confirma os campos da etapa: trava os certos (+pontos), marca os
        errados (-pontos) e só avança quando todos estiverem certos."""
        s = store.mg3_step
        if store.mg3_finished:
            return
        any_empty = False
        any_wrong = False
        for f in range(len(MG3_STEPS[s]["fields"])):
            if store.mg3_locked[s][f]:
                continue
            pos = store.mg3_values[s][f]
            if pos < 0:
                any_empty = True
                continue
            if store.mg3_order[s][f][pos] == 0:     # a 1ª opção é a correta
                store.mg3_locked[s][f] = True
                store.mg3_wrong[s][f] = False
                mg3_hit()
            else:
                store.mg3_wrong[s][f] = True
                any_wrong = True
                mg3_miss()

        if all(store.mg3_locked[s]):
            mg3_set_feedback(_("Tudo certo! Etapa concluída."), True)
            mg3_advance()
        elif any_wrong:
            mg3_set_feedback(_("Há campos errados (em vermelho). Confira a ficha do animal e corrija."), False)
        elif any_empty:
            mg3_set_feedback(_("Preencha todos os campos antes de confirmar."), False)

    def mg3_all_filled():
        """Todos os campos da etapa atual já foram escolhidos?"""
        s = store.mg3_step
        return all(store.mg3_locked[s][f] or store.mg3_values[s][f] >= 0
                   for f in range(len(MG3_STEPS[s]["fields"])))

    def mg3_skip():
        """Pula uma etapa opcional (a resenha): sem penalidade, sem pontos."""
        if store.mg3_finished or not MG3_STEPS[store.mg3_step].get("skippable"):
            return
        mg3_set_feedback(_("Resenha não preenchida."), False)
        mg3_advance()

    def mg3_verdict():
        """Frase de feedback conforme o desempenho."""
        ratio = float(store.mg3_score) / max(1, MG3_MAX_SCORE)
        if ratio >= 1.0:
            return _("Coleta perfeita! Golias está liberado para viajar com o exame em dia.")
        elif ratio >= 0.7:
            return _("Boa coleta! Mas algumas condutas poderiam ter sido melhores.")
        else:
            return _("Revise o procedimento de coleta para o exame de AIE e tente de novo.")


## -----------------------------------------------------------------------
## 1.5) TELA DE INSTRUÇÕES
##    Uso: call screen minigame3_instructions
##    Modal: bloqueia qualquer clique no que estiver atrás até "Entendi".
##    (mesma estrutura do minigame 1)
## -----------------------------------------------------------------------
init python:

    # IMAGEM: minigame3/mg3_instructions_bg.png — fundo cheio das instruções.
    # Tamanho final: 1920x1080 → exporte o PNG a 960x540.
    MG3_INSTR_BG = mg3_art("mg3_instructions_bg.png", (1920, 1080),
                           "FUNDO: instruções\n(mg3_instructions_bg.png)", "#2a2418")

    # IMAGEM: minigame3/mg3_instructions_panel.png — moldura do texto de regras.
    # Tamanho final: 1200x600 → exporte o PNG a 600x300.
    MG3_INSTR_PANEL = mg3_art("mg3_instructions_panel.png", (1200, 600),
                              "MOLDURA DE TEXTO\n(mg3_instructions_panel.png)", "#4a3a20")

style mg3_instructions_text:
    xalign 0.5
    yalign 0.5
    text_align 0.5
    color "#ffffff"
    size 30
    xsize 1000


screen minigame3_instructions():

    modal True  # impede qualquer clique/interação com o jogo por trás

    add MG3_INSTR_BG

    fixed:
        xalign 0.5
        yalign 0.45
        xysize (1200, 600)
        add MG3_INSTR_PANEL

        # Texto de regras de exemplo — edite como quiser
        text _("O campeão \"Golias da Natureza\" vai viajar para uma competição e precisa do exame de AIE!\n\nRealize a coleta passo a passo: escolha o tubo, a via de coleta, identifique a amostra, preencha a resenha e coloque a amostra na caixa refrigerada.\n\nCada conduta correta marca pontos; cada erro tira pontos.") style "mg3_instructions_text" xalign 0.5 yalign 0.5

    # Botão "Entendi" / "Fechar" — libera o jogador para o minigame.
    # IMAGEM: minigame3/mg3_close_idle.png e mg3_close_hover.png.
    # Tamanho final: 240x80 → exporte cada PNG a 120x40.
    imagebutton:
        xalign 0.5
        yalign 0.85
        idle mg3_art("mg3_close_idle.png", (240, 80), "ENTENDI\n(mg3_close_idle.png)", "#3a5a3a")
        hover mg3_art("mg3_close_hover.png", (240, 80), "ENTENDI\n(mg3_close_hover.png)", "#4f7a4f")
        focus_mask True
        action [
            Play("sound", "audio/sfx_click.ogg"),
            Return(True),  # devolve o controle ao "call screen" que a chamou
        ]
        hovered Play("sound", "audio/sfx_hover.ogg")


## -----------------------------------------------------------------------
## 2) TELA DO MINIGAME
## -----------------------------------------------------------------------

# Botão de ação genérico (Confirmar / Pular / Continuar): moldura de arte +
# texto escrito pelo jogo. Uso: use mg3_button(texto, x, ação, habilitado)
screen mg3_button(label, x, act, enabled=True):

    imagebutton:
        pos (x, MG3_BTN_Y)
        idle MG3_BTN_IDLE
        hover MG3_BTN_HOVER
        insensitive MG3_BTN_IDLE
        focus_mask True
        sensitive enabled
        action act
        hovered Function(mg3_sfx, "hover")

    text "[label!t]":
        pos (x + MG3_BTN_SIZE[0] // 2, MG3_BTN_Y + MG3_BTN_SIZE[1] // 2)
        anchor (0.5, 0.5)
        size 32
        color ("#ffffff" if enabled else "#999999")


screen minigame3_gameplay():

    modal True  # bloqueia qualquer interação com o que estiver atrás

    # Fundo cheio (cavalo à esquerda)
    add MG3_BG

    # ---- Painel de título (topo da coluna da direita) --------------------
    # Se a sua arte do painel já tiver o texto desenhado, apague os 2 textos abaixo.
    fixed:
        pos MG3_TITLE_POS
        xysize MG3_TITLE_SIZE
        add MG3_TITLE_PANEL
        text _("3 - COLETA DE EXAME"):
            xpos 30
            ypos 20
            size 34
            color "#ffffff"
        text _("Faça a coleta para o exame de AIE do cavalo campeão."):
            xpos 30
            ypos 78
            size 24
            color "#ffffff"
            xmaximum MG3_COL_W - 60

    # ---- Pontuação (canto superior esquerdo, sobre a arte) --------------
    text _("Pontos: [mg3_score]"):
        xpos 60
        ypos 40
        size 36
        color "#ffffff"

    if not mg3_finished:

        $ step = MG3_STEPS[mg3_step]
        $ step_title = step["title"]
        $ step_prompt = step["prompt"]
        $ step_number = mg3_step + 1
        $ step_total = len(MG3_STEPS)

        text _("Etapa [step_number]/[step_total] — [step_title!t]"):
            xpos MG3_COL_X
            ypos MG3_STEP_Y
            size 34
            bold True
            color "#ffffff"

        text "[step_prompt!t]":
            xpos MG3_COL_X
            ypos MG3_PROMPT_Y
            size 26
            color "#ffffff"
            xmaximum MG3_COL_W

        # ---- Etapa de ESCOLHA: 3 opções empilhadas ----------------------
        if step["kind"] == "choice":

            for k in range(len(step["options"])):

                $ opt = mg3_order[mg3_step][k]
                $ opt_text = step["options"][opt][0]
                $ opt_tried = opt in mg3_tried

                button:
                    pos (MG3_COL_X, MG3_OPT_Y0 + k * MG3_OPT_STEP)
                    xysize MG3_OPT_SIZE
                    background None
                    focus_mask True
                    sensitive not opt_tried
                    action Function(mg3_choose, opt)
                    hovered Function(mg3_sfx, "hover")
                    add MG3_OPT_ART["wrong" if opt_tried else "idle"]
                    text "[opt_text!t]":
                        xpos 40
                        yalign 0.5
                        size 32
                        color "#ffffff"
                        xmaximum MG3_OPT_SIZE[0] - 80

        # ---- Etapa de CAMPOS: ficha do animal + campos ------------------
        else:

            if step["show_profile"]:

                $ pf_name = MG3_PROFILE["name"]
                $ pf_farm = MG3_PROFILE["farm"]
                $ pf_date = MG3_PROFILE["date"]
                $ pf_age = MG3_PROFILE["age"]
                $ pf_sex = MG3_PROFILE["sex"]
                $ pf_coat = MG3_PROFILE["coat"]

                fixed:
                    pos MG3_FICHA_POS
                    xysize MG3_FICHA_SIZE
                    add MG3_FICHA
                    vbox:
                        xpos 40
                        ypos 20
                        spacing 8
                        text _("FICHA DO ANIMAL") size 26 bold True color "#3a2410"
                        text _("Nome: [pf_name]") size 26 color "#3a2410"
                        text _("Propriedade: [pf_farm]") size 26 color "#3a2410"
                        text _("Data da coleta: [pf_date]") size 26 color "#3a2410"
                        text _("Idade: [pf_age]   Sexo: [pf_sex]   Pelagem: [pf_coat]") size 26 color "#3a2410"

            for f in range(len(step["fields"])):

                $ field_label = step["fields"][f]["label"]
                $ field_value = mg3_field_text(f)
                $ field_state = "right" if mg3_locked[mg3_step][f] else ("wrong" if mg3_wrong[mg3_step][f] else "idle")

                button:
                    pos (MG3_COL_X, MG3_FIELD_Y0 + f * MG3_FIELD_STEP)
                    xysize MG3_FIELD_SIZE
                    background None
                    focus_mask True
                    sensitive not mg3_locked[mg3_step][f]
                    action Function(mg3_cycle, f)
                    hovered Function(mg3_sfx, "hover")
                    add MG3_FIELD_ART[field_state]
                    text "[field_label!t]:":
                        xpos 40
                        yalign 0.5
                        size 30
                        bold True
                        color "#ffffff"
                    text "[field_value!t]":
                        xpos 320
                        yalign 0.5
                        size 30
                        color "#ffffff"
                        xmaximum MG3_FIELD_SIZE[0] - 360

            use mg3_button(_("Confirmar"), MG3_COL_X, Function(mg3_confirm), mg3_all_filled())

            if step["skippable"]:
                use mg3_button(_("Pular resenha"), MG3_COL_X + MG3_COL_W - MG3_BTN_SIZE[0], Function(mg3_skip))

        # ---- Feedback da última ação ------------------------------------
        if mg3_feedback:
            text "[mg3_feedback!t]":
                xpos MG3_COL_X
                ypos MG3_FEEDBACK_Y
                size 24
                xmaximum MG3_COL_W
                color ("#b9f5b9" if mg3_feedback_ok else "#ffb3b3")

    # ---- Fim: resultado final --------------------------------------------
    else:

        $ verdict = mg3_verdict()

        button:
            xfill True
            yfill True
            background "#000000aa"
            action NullAction()

        fixed:
            xalign 0.5
            yalign 0.5
            xysize (1000, 420)
            add MG3_RESULT_PANEL

            vbox:
                xalign 0.5
                ypos 40
                spacing 20

                text _("Amostra enviada ao laboratório!"):
                    xalign 0.5
                    size 44
                    color "#ffffff"

                text _("Pontuação: [mg3_score] / [MG3_MAX_SCORE]"):
                    xalign 0.5
                    size 40
                    color "#ffffff"

                text "[verdict!t]":
                    xalign 0.5
                    text_align 0.5
                    size 28
                    color "#ffffff"
                    xmaximum 880

        # Botão Continuar (sob o painel)
        button:
            xalign 0.5
            ypos 800
            xysize MG3_END_BTN_SIZE
            background None
            focus_mask True
            action [Play("sound", "audio/sfx_click.ogg"), Return(True)]
            hovered Function(mg3_sfx, "hover")
            add MG3_BTN_IDLE
            text _("Continuar"):
                xalign 0.5
                yalign 0.5
                size 32
                color "#ffffff"


## -----------------------------------------------------------------------
## 3) LABEL DO GAMEPLAY (motor do minigame em si)
## -----------------------------------------------------------------------
label minigame_3_gameplay:

    $ quick_menu = False       # esconde os botões rápidos do rodapé durante o minigame
    $ renpy.block_rollback()   # impede que o rollback (roda do mouse) bagunce o estado
    $ mg3_reset()              # embaralha as opções e zera o estado (permite rejogar)

    scene black
    call screen minigame3_gameplay   # só retorna quando o jogador clica em "Continuar"

    $ quick_menu = True
    return


## -----------------------------------------------------------------------
## 4) PONTO DE ENTRADA (chamado pelo roadmap.rpy: "call expression 'minigame_3_entry'")
##    Mostra as instruções, roda o gameplay e avisa o mapa que terminou.
## -----------------------------------------------------------------------
label minigame_3_entry:

    call screen minigame3_instructions
    call minigame_3_gameplay

    $ mg_report_score(3, mg3_score, MG3_MAX_SCORE)  # registra o placar e a medalha, se for o caso
    $ mg_complete(3)                                 # marca como concluído e libera o 4

    return
