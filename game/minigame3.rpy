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
#                    Cavalo, Propriedade e Data da coleta (clicar no campo troca
#                    a opção, em ciclo) e confirma
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
# ARTE (mesmo esquema do menu, do roadmap e do minigame 2):
#   TODA arte real é um PNG de CANVAS INTEIRO (960x540), com o elemento já na
#   posição certa. O jogo amplia 2x (nearest neighbor) e desenha em (0, 0), sem
#   usar posição do código; focus_mask True faz só os pixels opacos de cada
#   botão responderem ao mouse. A ORDEM das opções é fixa (a posição está
#   dentro de cada PNG).
#   Enquanto o PNG não existe, aparece um retângulo placeholder colorido com
#   texto, na posição definida pelas constantes MG3_*_RECT abaixo. (Essas
#   constantes só servem aos placeholders: a arte real ignora todas elas.)
#   Os textos das opções, dos campos e dos enunciados já vêm DESENHADOS nas
#   artes; o jogo só escreve textos que mudam (pontos, feedback, resultado).
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

    # ---- Posições dos PLACEHOLDERS (tela 1920x1080): (x, y, largura, altura)
    # Tudo na coluna da DIREITA (o cavalo ocupa a esquerda, no fundo).
    MG3_TITLE_RECT = (1000, 30, 880, 130)
    MG3_STEP_RECT = (1000, 175, 880, 100)           # enunciado da etapa
    MG3_FICHA_RECT = (1000, 280, 880, 240)

    def mg3_opt_rect(k):                            # etapas de escolha
        return (1000, 300 + k * 150, 880, 130)

    def mg3_field_rect(f):                          # etapas de campos
        return (1000, 545 + f * 110, 880, 100)

    MG3_CONFIRM_RECT = (1000, 940, 420, 90)
    MG3_SKIP_RECT = (1460, 940, 420, 90)
    MG3_RESULT_RECT = (460, 330, 1000, 420)
    MG3_CONTINUE_RECT = (750, 800, 420, 90)
    MG3_INSTR_PANEL_RECT = (360, 190, 1200, 600)
    MG3_CLOSE_RECT = (840, 860, 240, 80)

    # Textos escritos pelo jogo (mudam durante a partida)
    MG3_SCORE_POS = (60, 40)                        # "Pontos: N"
    MG3_FEEDBACK_POS = (1000, 868)                  # motivo do acerto/erro
    MG3_FEEDBACK_W = 880
    MG3_RESULT_SCORE_POS = (960, 470)               # "Pontuação: N / M" (centralizado)
    MG3_RESULT_VERDICT_POS = (960, 560)             # frase de feedback (centralizada)

    # ---- Regras ------------------------------------------------------------
    MG3_POINTS_HIT = 10
    MG3_POINTS_MISS = 5

    # ---- Ficha do animal (dados que o jogador confere) ----------------------
    # Estes valores precisam bater com o que estiver DESENHADO na ficha
    # (mg3_ficha.png) e com a opção correta de cada campo abaixo.
    MG3_PROFILE = {
        "name": "Golias da Natureza",
        "farm": "Haras Vale Verde",
        "date": "12/03/2025",
        "age": "8 anos",
        "sex": "Macho",
        "coat": "Castanha",
    }

    # ---- Etapas ------------------------------------------------------------
    # kind "choice": "options" = (texto, correta?, feedback), na ordem EXATA
    #                das artes opcao_<id>_1, _2, _3 (de cima para baixo).
    # kind "fields": cada campo tem "id" e "options" = (texto, correta?), na
    #                ordem das artes campo_<id>_1, _2, _3 (ordem do ciclo).
    # O "texto" só aparece no placeholder enquanto o PNG não existe.
    MG3_STEPS = [
        {
            "id": "tubo",
            "kind": "choice",
            "title": _("Escolha do tubo"),
            "options": [
                (_("Tubo com EDTA"), False,
                 _("O EDTA é um anticoagulante: o sangue não coagula e não se obtém soro para a sorologia.")),
                (_("Tubo sem anticoagulante"), True,
                 _("Correto! Sem anticoagulante o sangue coagula e permite obter o soro, necessário para o exame sorológico.")),
                (_("Tubo com heparina"), False,
                 _("A heparina também é um anticoagulante e impede a formação do soro.")),
            ],
        },
        {
            "id": "via",
            "kind": "choice",
            "title": _("Local e via de coleta"),
            "options": [
                (_("Aplicação intramuscular na garupa"), False,
                 _("A via intramuscular serve para aplicar medicamentos, não para colher sangue.")),
                (_("Aplicação subcutânea no dorso"), False,
                 _("A via subcutânea também é de aplicação; não permite colher sangue para o exame.")),
                (_("Coleta endovenosa na veia jugular"), True,
                 _("Correto! O sangue para análise é colhido da veia jugular.")),
            ],
        },
        {
            "id": "etiqueta",
            "kind": "fields",
            "title": _("Identificação da amostra"),
            "skippable": False,
            "fields": [
                {"id": "cavalo", "label": _("Cavalo"),
                 "options": [("Golias do Vale", False),
                             (MG3_PROFILE["name"], True),
                             ("Gigante da Natureza", False)]},
                {"id": "propriedade", "label": _("Propriedade"),
                 "options": [("Haras Campo Verde", False),
                             ("Fazenda Vale Verde", False),
                             (MG3_PROFILE["farm"], True)]},
                {"id": "data", "label": _("Data da coleta"),
                 "options": [(MG3_PROFILE["date"], True),
                             ("11/03/2025", False),
                             ("21/03/2025", False)]},
            ],
        },
        {
            "id": "resenha",
            "kind": "fields",
            "title": _("Resenha do animal"),
            "skippable": True,
            "fields": [
                {"id": "idade", "label": _("Idade"),
                 "options": [("3 anos", False),
                             (MG3_PROFILE["age"], True),
                             ("15 anos", False)]},
                {"id": "sexo", "label": _("Sexo"),
                 "options": [("Fêmea", False),
                             ("Macho castrado", False),
                             (MG3_PROFILE["sex"], True)]},
                {"id": "pelagem", "label": _("Pelagem"),
                 "options": [(MG3_PROFILE["coat"], True),
                             ("Alazã", False),
                             ("Tordilha", False)]},
            ],
        },
        {
            "id": "caixa",
            "kind": "choice",
            "title": _("Transporte da amostra"),
            "options": [
                (_("Caixa de papelão em temperatura ambiente"), False,
                 _("Sem refrigeração a amostra pode se deteriorar e comprometer o resultado.")),
                (_("Porta-luvas do carro, ao sol"), False,
                 _("O calor degrada a amostra: ela precisa ir refrigerada.")),
                (_("Caixa isotérmica refrigerada (com gelo)"), True,
                 _("Correto! A amostra deve seguir refrigerada até o laboratório.")),
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
    def mg3_art(filename, rect, label, color, fill=True):
        """Arte de canvas inteiro (960x540 → 1920x1080, nearest neighbor,
        desenhada em (0, 0)) se o PNG existir. Senão, um placeholder: retângulo
        colorido com texto na posição "rect" = (x, y, largura, altura).
        fill=False = só o texto, sem retângulo."""
        path = MG3_ART_DIR + filename
        if renpy.loadable(path):
            return Transform(Image(path, nearest_neighbor=True), zoom=MG3_ZOOM)

        x, y, w, h = rect
        text = Text(label, size=26, color="#ffffff", xalign=0.5, yalign=0.5,
                    text_align=0.5, xmaximum=w - 20)
        if fill:
            box = Fixed(Solid(color, xysize=(w, h)), text, xysize=(w, h))
        else:
            box = Fixed(text, xysize=(w, h))
        return Fixed(Transform(box, pos=(x, y)), xysize=(1920, 1080))

    def mg3_overlay(filename, rect, color):
        """Camada transparente de estado (certo/errado) sobre uma opção. Arte
        real = canvas inteiro com a marca já na posição; placeholder = faixa
        colorida semitransparente sobre o retângulo "rect"."""
        path = MG3_ART_DIR + filename
        if renpy.loadable(path):
            return Transform(Image(path, nearest_neighbor=True), zoom=MG3_ZOOM)
        x, y, w, h = rect
        return Fixed(Transform(Solid(color, xysize=(w, h)), pos=(x, y)),
                     xysize=(1920, 1080))

    # IMAGEM: minigame3/mg3_bg.png — fundo cheio: área de atendimento com o
    # "Golias da Natureza" no lado ESQUERDO (a coluna da direita fica livre
    # para as opções). Canvas 960x540.
    MG3_BG = mg3_art("mg3_bg.png", (0, 0, 1920, 1080), "FUNDO: cavalo à esquerda\n(mg3_bg.png)", "#3a4a3a")

    # IMAGEM: minigame3/mg3_title_panel.png — painel de título ("3 - COLETA DE
    # EXAME", com o texto desenhado). Canvas 960x540.
    MG3_TITLE_PANEL = mg3_art("mg3_title_panel.png", MG3_TITLE_RECT, "3 - COLETA DE EXAME\n(mg3_title_panel.png)", "#4a3a20")

    # IMAGEM: minigame3/mg3_etapa_<id>.png — cabeçalho + enunciado de cada etapa,
    # já desenhados (ex.: "Etapa 1/5 — Escolha do tubo: qual tubo usar...?").
    # <id> = tubo, via, etiqueta, resenha, caixa. Canvas 960x540. 5 arquivos.
    MG3_STEP_ART = [
        mg3_art("mg3_etapa_%s.png" % st["id"], MG3_STEP_RECT,
                "ETAPA %d/%d — %s\n(mg3_etapa_%s.png)" % (i + 1, len(MG3_STEPS), st["title"], st["id"]),
                "#33363a")
        for i, st in enumerate(MG3_STEPS)
    ]

    # IMAGEM: minigame3/opcao_<id>_<n>.png — cada opção das etapas de ESCOLHA
    # (moldura + texto já desenhados), na posição dela. <id> = tubo, via, caixa;
    # <n> = 1, 2, 3 (de cima para baixo). Canvas 960x540. 9 arquivos.
    # IMAGEM: minigame3/mg3_errada_<n>.png — camada que marca uma opção errada
    # já tentada (ex.: moldura vermelha), na posição do slot <n> = 1, 2, 3
    # (vale para as 3 etapas de escolha). Canvas 960x540, fundo transparente.
    MG3_OPTION_ART = {}
    for _st in MG3_STEPS:
        if _st["kind"] == "choice":
            MG3_OPTION_ART[_st["id"]] = [
                mg3_art("opcao_%s_%d.png" % (_st["id"], k + 1), mg3_opt_rect(k),
                        "%s\n(opcao_%s_%d.png)" % (opt[0], _st["id"], k + 1), "#4a4a4a")
                for k, opt in enumerate(_st["options"])
            ]
    MG3_TRIED_OVERLAY = [
        mg3_overlay("mg3_errada_%d.png" % (k + 1), mg3_opt_rect(k), "#cc222266")
        for k in range(3)
    ]

    # IMAGEM: minigame3/mg3_ficha.png — a "ficha do animal" já com os dados
    # desenhados (precisam bater com MG3_PROFILE). Canvas 960x540.
    MG3_FICHA = mg3_art("mg3_ficha.png", MG3_FICHA_RECT,
                        "FICHA DO ANIMAL\n%s | %s | %s\n%s | %s | %s" % (
                            MG3_PROFILE["name"], MG3_PROFILE["farm"], MG3_PROFILE["date"],
                            MG3_PROFILE["age"], MG3_PROFILE["sex"], MG3_PROFILE["coat"]),
                        "#d8cfa8")

    # IMAGEM: minigame3/campo_<id>_<n>.png — cada opção de um CAMPO (etiqueta e
    # resenha), moldura + texto já desenhados, na posição do campo. <id> =
    # cavalo, propriedade, data, idade, sexo, pelagem; <n> = 1, 2, 3 (a ordem do
    # ciclo de cliques). Canvas 960x540. 18 arquivos.
    # IMAGEM: minigame3/campo_<id>_vazio.png — o campo ainda sem escolha
    # (ex.: "clique para escolher"). Canvas 960x540. 6 arquivos.
    # IMAGEM: minigame3/mg3_campo_certo_<n>.png e mg3_campo_errado_<n>.png —
    # camadas transparentes (verde / vermelha) sobre o campo de posição <n> = 1,
    # 2, 3 (valem para a etiqueta e para a resenha). Canvas 960x540. 6 arquivos.
    MG3_FIELD_ART = {}
    for _st in MG3_STEPS:
        if _st["kind"] == "fields":
            for _f, _field in enumerate(_st["fields"]):
                _rect = mg3_field_rect(_f)
                MG3_FIELD_ART[_field["id"]] = [
                    mg3_art("campo_%s_vazio.png" % _field["id"], _rect,
                            "%s: (clique para escolher)\n(campo_%s_vazio.png)" % (_field["label"], _field["id"]),
                            "#4a4a4a")
                ] + [
                    mg3_art("campo_%s_%d.png" % (_field["id"], n + 1), _rect,
                            "%s: %s\n(campo_%s_%d.png)" % (_field["label"], opt[0], _field["id"], n + 1),
                            "#4a4a4a")
                    for n, opt in enumerate(_field["options"])
                ]
    MG3_FIELD_RIGHT = [mg3_overlay("mg3_campo_certo_%d.png" % (f + 1), mg3_field_rect(f), "#2e7d3277") for f in range(3)]
    MG3_FIELD_WRONG = [mg3_overlay("mg3_campo_errado_%d.png" % (f + 1), mg3_field_rect(f), "#cc222277") for f in range(3)]

    # IMAGEM: minigame3/mg3_confirmar_idle.png, mg3_confirmar_hover.png e
    # mg3_confirmar_disabled.png — botão "Confirmar" (texto desenhado).
    # disabled = enquanto algum campo ainda está vazio. Canvas 960x540.
    MG3_CONFIRM_IDLE = mg3_art("mg3_confirmar_idle.png", MG3_CONFIRM_RECT, "CONFIRMAR\n(mg3_confirmar_idle.png)", "#3a5a3a")
    MG3_CONFIRM_HOVER = mg3_art("mg3_confirmar_hover.png", MG3_CONFIRM_RECT, "CONFIRMAR\n(mg3_confirmar_hover.png)", "#4f7a4f")
    MG3_CONFIRM_DISABLED = mg3_art("mg3_confirmar_disabled.png", MG3_CONFIRM_RECT, "CONFIRMAR\n(mg3_confirmar_disabled.png)", "#2a2a2a")

    # IMAGEM: minigame3/mg3_pular_idle.png e mg3_pular_hover.png — botão
    # "Pular resenha" (texto desenhado). Canvas 960x540.
    MG3_SKIP_IDLE = mg3_art("mg3_pular_idle.png", MG3_SKIP_RECT, "PULAR RESENHA\n(mg3_pular_idle.png)", "#5a4a2a")
    MG3_SKIP_HOVER = mg3_art("mg3_pular_hover.png", MG3_SKIP_RECT, "PULAR RESENHA\n(mg3_pular_hover.png)", "#7a6a3a")

    # IMAGEM: minigame3/mg3_resultado.png — painel do resultado final, com o
    # texto fixo desenhado (ex.: "Amostra enviada ao laboratório!"); o jogo
    # escreve a pontuação e a frase de feedback por cima, em
    # MG3_RESULT_SCORE_POS e MG3_RESULT_VERDICT_POS. Canvas 960x540.
    MG3_RESULT_PANEL = mg3_art("mg3_resultado.png", MG3_RESULT_RECT, "AMOSTRA ENVIADA AO LABORATÓRIO!\n(mg3_resultado.png)", "#2e5a3a")

    # IMAGEM: minigame3/mg3_continuar_idle.png e mg3_continuar_hover.png —
    # botão "Continuar" do resultado (texto desenhado). Canvas 960x540.
    MG3_CONTINUE_IDLE = mg3_art("mg3_continuar_idle.png", MG3_CONTINUE_RECT, "CONTINUAR\n(mg3_continuar_idle.png)", "#3a5a3a")
    MG3_CONTINUE_HOVER = mg3_art("mg3_continuar_hover.png", MG3_CONTINUE_RECT, "CONTINUAR\n(mg3_continuar_hover.png)", "#4f7a4f")

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
default mg3_tried = []        # etapa de escolha: opções erradas já tentadas
default mg3_values = []       # por etapa de campos: posição atual de cada campo (-1 = vazio)
default mg3_locked = []       # por etapa de campos: campo já correto (travado)?
default mg3_wrong = []        # por etapa de campos: campo marcado como errado?
default mg3_feedback = ""     # última mensagem de feedback
default mg3_feedback_ok = True


init python:

    def mg3_reset():
        """Nova partida: zera o estado."""
        values, locked, wrong = [], [], []
        for st in MG3_STEPS:
            n = len(st["fields"]) if st["kind"] == "fields" else 0
            values.append([-1] * n)
            locked.append([False] * n)
            wrong.append([False] * n)

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
        """Clique na opção opt (0, 1, 2) de uma etapa de escolha."""
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
    def mg3_field_art(f):
        """Arte atual do campo f da etapa atual (vazio ou a opção escolhida)."""
        field = MG3_STEPS[store.mg3_step]["fields"][f]
        return MG3_FIELD_ART[field["id"]][store.mg3_values[store.mg3_step][f] + 1]

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
        any_wrong = False
        for f, field in enumerate(MG3_STEPS[s]["fields"]):
            if store.mg3_locked[s][f]:
                continue
            pos = store.mg3_values[s][f]
            if pos < 0:
                continue
            if field["options"][pos][1]:
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
## -----------------------------------------------------------------------
init python:

    # IMAGEM: minigame3/mg3_instructions_bg.png — fundo cheio. Canvas 960x540.
    MG3_INSTR_BG = mg3_art("mg3_instructions_bg.png", (0, 0, 1920, 1080),
                           "FUNDO: instruções\n(mg3_instructions_bg.png)", "#2a2418")

    # IMAGEM: minigame3/mg3_instructions_panel.png — moldura do texto de regras,
    # sem texto (o texto é escrito pelo jogo, centralizado em (960, 490), com
    # até 1000 px de largura; deixe a moldura grande o bastante). Canvas 960x540.
    MG3_INSTR_PANEL = mg3_art("mg3_instructions_panel.png", MG3_INSTR_PANEL_RECT,
                              "MOLDURA DE TEXTO\n(mg3_instructions_panel.png)", "#4a3a20")

    # IMAGEM: minigame3/mg3_close_idle.png e mg3_close_hover.png — botão
    # "Entendi" (texto desenhado). Canvas 960x540.
    MG3_CLOSE_IDLE = mg3_art("mg3_close_idle.png", MG3_CLOSE_RECT, "ENTENDI\n(mg3_close_idle.png)", "#3a5a3a")
    MG3_CLOSE_HOVER = mg3_art("mg3_close_hover.png", MG3_CLOSE_RECT, "ENTENDI\n(mg3_close_hover.png)", "#4f7a4f")

style mg3_instructions_text:
    text_align 0.5
    color "#ffffff"
    size 30
    xsize 1000


screen minigame3_instructions():

    modal True  # impede qualquer clique/interação com o jogo por trás

    add MG3_INSTR_BG
    add MG3_INSTR_PANEL

    # Texto de regras de exemplo — edite como quiser
    text _("O campeão \"Golias da Natureza\" vai viajar para uma competição e precisa do exame de AIE!\n\nRealize a coleta passo a passo: escolha o tubo, a via de coleta, identifique a amostra, preencha a resenha e coloque a amostra na caixa refrigerada.\n\nCada conduta correta marca pontos; cada erro tira pontos.") style "mg3_instructions_text" pos (960, 490) anchor (0.5, 0.5)

    imagebutton:
        idle MG3_CLOSE_IDLE
        hover MG3_CLOSE_HOVER
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
screen minigame3_gameplay():

    modal True  # bloqueia qualquer interação com o que estiver atrás

    # Fundo cheio (cavalo à esquerda) e painel de título
    add MG3_BG
    add MG3_TITLE_PANEL

    # Pontuação atual (texto que muda)
    text _("Pontos: [mg3_score]"):
        pos MG3_SCORE_POS
        size 36
        color "#ffffff"

    if not mg3_finished:

        $ step = MG3_STEPS[mg3_step]

        # Cabeçalho + enunciado da etapa (arte própria de cada etapa)
        add MG3_STEP_ART[mg3_step]

        # ---- Etapa de ESCOLHA: 3 opções empilhadas ----------------------
        if step["kind"] == "choice":

            for k in range(len(step["options"])):

                $ opt_tried = k in mg3_tried

                button:
                    xysize (1920, 1080)
                    background None
                    focus_mask True
                    sensitive not opt_tried
                    action Function(mg3_choose, k)
                    hovered Function(mg3_sfx, "hover")
                    add MG3_OPTION_ART[step["id"]][k]
                    if opt_tried:
                        add MG3_TRIED_OVERLAY[k]

        # ---- Etapa de CAMPOS: ficha do animal + campos ------------------
        else:

            add MG3_FICHA

            for f in range(len(step["fields"])):

                $ field_locked = mg3_locked[mg3_step][f]
                $ field_wrong = mg3_wrong[mg3_step][f]

                button:
                    xysize (1920, 1080)
                    background None
                    focus_mask True
                    sensitive not field_locked
                    action Function(mg3_cycle, f)
                    hovered Function(mg3_sfx, "hover")
                    add mg3_field_art(f)
                    if field_locked:
                        add MG3_FIELD_RIGHT[f]
                    elif field_wrong:
                        add MG3_FIELD_WRONG[f]

            imagebutton:
                idle MG3_CONFIRM_IDLE
                hover MG3_CONFIRM_HOVER
                insensitive MG3_CONFIRM_DISABLED
                sensitive mg3_all_filled()
                focus_mask True
                action Function(mg3_confirm)
                hovered Function(mg3_sfx, "hover")

            if step["skippable"]:
                imagebutton:
                    idle MG3_SKIP_IDLE
                    hover MG3_SKIP_HOVER
                    focus_mask True
                    action Function(mg3_skip)
                    hovered Function(mg3_sfx, "hover")

        # ---- Feedback da última ação (texto que muda) -------------------
        if mg3_feedback:
            text "[mg3_feedback!t]":
                pos MG3_FEEDBACK_POS
                size 24
                xmaximum MG3_FEEDBACK_W
                color ("#b9f5b9" if mg3_feedback_ok else "#ffb3b3")

    # ---- Fim: resultado final --------------------------------------------
    else:

        $ verdict = mg3_verdict()

        button:
            xfill True
            yfill True
            background "#000000aa"
            action NullAction()

        add MG3_RESULT_PANEL

        text _("Pontuação: [mg3_score] / [MG3_MAX_SCORE]"):
            pos MG3_RESULT_SCORE_POS
            anchor (0.5, 0.5)
            size 40
            color "#ffffff"

        text "[verdict!t]":
            pos MG3_RESULT_VERDICT_POS
            anchor (0.5, 0.0)
            text_align 0.5
            size 28
            color "#ffffff"
            xmaximum 880

        imagebutton:
            idle MG3_CONTINUE_IDLE
            hover MG3_CONTINUE_HOVER
            focus_mask True
            action [Play("sound", "audio/sfx_click.ogg"), Return(True)]
            hovered Function(mg3_sfx, "hover")


## -----------------------------------------------------------------------
## 3) LABEL DO GAMEPLAY (motor do minigame em si)
## -----------------------------------------------------------------------
label minigame_3_gameplay:

    $ quick_menu = False       # esconde os botões rápidos do rodapé durante o minigame
    $ renpy.block_rollback()   # impede que o rollback (roda do mouse) bagunce o estado
    $ mg3_reset()              # zera o estado (permite rejogar do zero)

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
