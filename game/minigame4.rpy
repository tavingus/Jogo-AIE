################################################################################
# MINIGAME4.RPY
# Minigame 4: "Diagnóstico" — depois da coleta: IDGA e ELISA
# Como os exames funcionam, como interpretá-los e quais são as diferenças.
#
# O minigame tem 4 FASES, na ordem:
#
#   1. IMUNOCOMPLEXO (lúdica) — o vírus (antígeno) aparece à esquerda, com 3
#      "encaixes". À direita há 6 anticorpos candidatos: 3 são específicos do
#      vírus da AIE (encaixam e formam o imunocomplexo) e 3 são de outras
#      doenças (não encaixam). O jogador clica nos que acha que encaixam. Ao
#      acoplar os 3 certos, o imunocomplexo se forma — e a fase explica que é
#      ele que o IDGA e o ELISA enxergam, cada um do seu jeito.
#   2. LER O IDGA — a placa de gel de ágar (arte de fundo) mostra 3 poços de
#      amostra ao redor do poço de antígeno. O jogador classifica cada amostra
#      como Positivo ou Negativo olhando as linhas de precipitação.
#   3. LER O ELISA — a placa lida no espectrofotômetro: o jogo escreve a
#      densidade óptica (DO) de cada poço (controles + 4 amostras, valores
#      sorteados a cada partida) e o ponto de corte. O jogador compara a DO de
#      cada amostra com o ponto de corte.
#   4. DIFERENÇAS — 5 afirmações; o jogador diz se cada uma descreve o IDGA ou o
#      ELISA.
#
# Nas fases 2, 3 e 4 o jogador clica no campo para alternar a resposta
# (? → opção 1 → opção 2 → ...) e clica em Confirmar: os campos certos travam
# (verde) e os errados ficam vermelhos, com a explicação, até serem corrigidos.
#
# Pontuação (ver roadmap.rpy para o sistema de medalhas):
#   + MG4_POINTS_HIT   por conduta correta (anticorpo que encaixou / campo certo)
#   - MG4_POINTS_MISS  por conduta errada (anticorpo que não encaixa / campo errado)
#   O placar nunca fica abaixo de 0. Pontuação máxima = nenhum erro.
#
# ARTE (mesmo esquema do menu, roadmap, minigames 2 e 3):
#   TODA arte real é um PNG de CANVAS INTEIRO (960x540), com o elemento já na
#   posição certa. O jogo amplia 2x (nearest neighbor) e desenha em (0, 0), sem
#   usar posição do código; focus_mask True faz só os pixels opacos de cada
#   botão responderem ao mouse. A ORDEM das opções é fixa.
#   Enquanto o PNG não existe, aparece um placeholder colorido com texto, na
#   posição das constantes MG4_*_RECT abaixo (só servem aos placeholders).
#   Textos fixos vêm DESENHADOS na arte; o jogo só escreve o que muda (pontos,
#   feedback, valores de DO e ponto de corte do ELISA, resultado).
#
# ATENÇÃO — conteúdo científico: revise as afirmações e explicações com o seu
# material (principalmente a fase 4).
#
# Este arquivo contém: dados/configuração, lógica, tela de instruções, tela
# do gameplay e o "label minigame_4_entry" — chamado pelo roadmap.rpy.
################################################################################


## -----------------------------------------------------------------------
## 1) CONFIGURAÇÃO, DADOS E LÓGICA
## -----------------------------------------------------------------------
init python:

    MG4_ART_DIR = "images/minigame4/"
    MG4_ZOOM = 2.0  # arte a 960x540, exibida em 1920x1080

    # ---- Posições dos PLACEHOLDERS (tela 1920x1080): (x, y, largura, altura)
    # Esquerda = cena (placa / antígeno); direita = interação.
    MG4_HEADER_RECT = (1000, 170, 880, 110)          # título + enunciado da fase

    def mg4_cand_rect(n):                            # fase 1: 6 anticorpos (2 colunas x 3)
        return (1000 + (n % 2) * 450, 300 + (n // 2) * 200, 430, 180)

    MG4_SITE_RECTS = [(300, 330, 220, 110), (300, 470, 220, 110), (300, 610, 220, 110)]  # encaixes
    MG4_COMPLEX_RECT = (140, 280, 620, 480)          # imunocomplexo formado

    def mg4_field_rect(f):                           # fases 2-4: até 5 campos
        return (1000, 300 + f * 120, 880, 100)

    MG4_CONFIRM_RECT = (1000, 940, 420, 90)
    MG4_RESULT_RECT = (460, 330, 1000, 420)
    MG4_CONTINUE_RECT = (750, 800, 420, 90)
    MG4_INSTR_PANEL_RECT = (360, 190, 1200, 600)
    MG4_CLOSE_RECT = (840, 860, 240, 80)

    # Textos escritos pelo jogo (mudam durante a partida)
    MG4_SCORE_POS = (60, 40)                         # "Pontos: N"
    MG4_FEEDBACK_POS = (60, 930)                     # explicação do acerto/erro
    MG4_FEEDBACK_W = 860
    MG4_CUTOFF_POS = (60, 840)                       # ELISA: ponto de corte
    # ELISA: centro do valor de DO de cada poço (C-, C+, A1, A2, A3, A4)
    MG4_OD_POS = [(160 + i * 140, 700) for i in range(6)]
    MG4_RESULT_SCORE_POS = (960, 470)                # "Pontuação: N / M" (centralizado)
    MG4_RESULT_VERDICT_POS = (960, 560)              # frase final (centralizada)

    # ---- Regras ------------------------------------------------------------
    MG4_POINTS_HIT = 10
    MG4_POINTS_MISS = 5

    # ---- Fase 1: anticorpos candidatos --------------------------------------
    # (texto, encaixa?, feedback), na ordem EXATA das artes anticorpo_1 ... _6
    # (esquerda->direita, cima->baixo). "encaixa" = específico do vírus da AIE.
    MG4_CANDIDATES = [
        (_("Anticorpo anti-hemaglutinina"), False,
         _("Não encaixa: a hemaglutinina é uma proteína do vírus da influenza equina, outro vírus, e não do vírus da AIE.")),
        (_("Anticorpo anti-p26"), True,
         _("Encaixou! O anti-p26 reconhece a p26, proteína do capsídeo do vírus da AIE (EIAV).")),
        (_("Anticorpo anti-gp90"), True,
         _("Encaixou! O anti-gp90 reconhece a gp90, glicoproteína do envelope do vírus da AIE.")),
        (_("Anticorpo anti-glicoproteína"), False,
         _("Não encaixa: essa glicoproteína é do herpesvírus equino, outro vírus, e o anticorpo não reconhece o antígeno da AIE.")),
        (_("Anticorpo anti-gp45"), True,
         _("Encaixou! O anti-gp45 reconhece a gp45, glicoproteína transmembrana do vírus da AIE.")),
        (_("Anticorpo anti-proteína E"), False,
         _("Não encaixa: a proteína E é do vírus do Nilo Ocidental, não do vírus da AIE.")),
    ]
    MG4_DOCK_TOTAL = sum(1 for c in MG4_CANDIDATES if c[1])
    MG4_COMPLEX_FEEDBACK = _("Imunocomplexo formado! É ele que os testes detectam: no IDGA ele aparece como uma linha de precipitação no gel; no ELISA, é revelado por uma reação de cor.")

    # ---- Fases 2, 3 e 4: campos ---------------------------------------------
    # Cada campo: "id", "label" (só no placeholder), "answer" (índice da opção
    # correta; None = definido por sorteio no ELISA) e "hint" (explicação).
    MG4_OPT_KEYS = {"result": ["positivo", "negativo"], "test": ["idga", "elisa"]}
    MG4_OPT_LABELS = {"result": ["Positivo", "Negativo"], "test": ["IDGA", "ELISA"]}

    # IDGA — ordem fixa dos poços; precisa BATER com a placa desenhada no
    # fundo mg4_bg_idga.png. Poço 2 = amostra do Golias (negativa).
    MG4_IDGA_TRUTH = [0, 1, 0]       # 0 = positivo, 1 = negativo
    MG4_IDGA_HINT = [
        _("Há uma linha de precipitação que se une à linha do controle positivo (linha de identidade): resultado POSITIVO."),
        _("Não se forma linha de precipitação entre o poço da amostra e o do antígeno: resultado NEGATIVO."),
    ]

    MG4_STEPS = [
        {
            "id": "dock",
            "kind": "dock",
            "title": _("Formação do imunocomplexo"),
        },
        {
            "id": "idga",
            "kind": "fields",
            "type": "result",
            "title": _("Lendo o IDGA"),
            "fields": [
                {"id": "idga_1", "label": "Poço 1", "answer": MG4_IDGA_TRUTH[0], "hint": MG4_IDGA_HINT[MG4_IDGA_TRUTH[0]]},
                {"id": "idga_2", "label": "Poço 2 (Golias)", "answer": MG4_IDGA_TRUTH[1], "hint": MG4_IDGA_HINT[MG4_IDGA_TRUTH[1]]},
                {"id": "idga_3", "label": "Poço 3", "answer": MG4_IDGA_TRUTH[2], "hint": MG4_IDGA_HINT[MG4_IDGA_TRUTH[2]]},
            ],
        },
        {
            "id": "elisa",
            "kind": "fields",
            "type": "result",
            "title": _("Lendo o ELISA"),
            # answer/hint são calculados a cada partida (ver mg4_reset)
            "fields": [
                {"id": "elisa_1", "label": "Amostra 1 (Golias)", "answer": None, "hint": ""},
                {"id": "elisa_2", "label": "Amostra 2", "answer": None, "hint": ""},
                {"id": "elisa_3", "label": "Amostra 3", "answer": None, "hint": ""},
                {"id": "elisa_4", "label": "Amostra 4", "answer": None, "hint": ""},
            ],
        },
        {
            "id": "teste",
            "kind": "fields",
            "type": "test",
            "title": _("IDGA ou ELISA?"),
            "fields": [
                {"id": "teste_1", "label": "Teste oficial de referência, com leitura visual das linhas de precipitação",
                 "answer": 0, "hint": _("É o IDGA (Coggins): teste oficial de referência, lido a olho nu pelas linhas de precipitação.")},
                {"id": "teste_2", "label": "Reação de cor lida em espectrofotômetro (densidade óptica)",
                 "answer": 1, "hint": _("É o ELISA: a cor da reação enzimática é medida em espectrofotômetro (leitor de placas), em densidade óptica.")},
                {"id": "teste_3", "label": "Mais sensível e automatizável: ideal para triagem de muitas amostras",
                 "answer": 1, "hint": _("É o ELISA: mais sensível, mais rápido e automatizável, bom para triagem de muitas amostras.")},
                {"id": "teste_4", "label": "Resultado após 24 a 48 horas, em placa de gel de ágar",
                 "answer": 0, "hint": _("É o IDGA: as linhas de precipitação levam de 24 a 48 horas para se formar no gel de ágar.")},
                {"id": "teste_5", "label": "Resultado positivo na triagem deve ser confirmado por este teste",
                 "answer": 0, "hint": _("É o IDGA: um positivo no ELISA é confirmado pelo teste oficial, o IDGA.")},
            ],
        },
    ]

    def mg4_count_hits():
        n = 0
        for st in MG4_STEPS:
            n += MG4_DOCK_TOTAL if st["kind"] == "dock" else len(st["fields"])
        return n

    # Pontuação máxima: todas as condutas certas, sem nenhum erro
    MG4_MAX_SCORE = mg4_count_hits() * MG4_POINTS_HIT

    # ---- Placeholders de arte ----------------------------------------------
    def mg4_art(filename, rect, label, color, fill=True):
        """Arte de canvas inteiro (960x540 → 1920x1080, nearest neighbor,
        desenhada em (0, 0)) se o PNG existir. Senão, um placeholder: retângulo
        colorido com texto na posição "rect" = (x, y, largura, altura).
        fill=False = só o texto, sem retângulo."""
        path = MG4_ART_DIR + filename
        if renpy.loadable(path):
            return Transform(Image(path, nearest_neighbor=True), zoom=MG4_ZOOM)

        x, y, w, h = rect
        text = Text(label, size=26, color="#ffffff", xalign=0.5, yalign=0.5,
                    text_align=0.5, xmaximum=w - 20)
        if fill:
            box = Fixed(Solid(color, xysize=(w, h)), text, xysize=(w, h))
        else:
            box = Fixed(text, xysize=(w, h))
        return Fixed(Transform(box, pos=(x, y)), xysize=(1920, 1080))

    def mg4_overlay(filename, rect, color):
        """Camada transparente de estado sobre uma opção. Arte real = canvas
        inteiro com a marca na posição; placeholder = faixa colorida
        semitransparente sobre o retângulo "rect"."""
        path = MG4_ART_DIR + filename
        if renpy.loadable(path):
            return Transform(Image(path, nearest_neighbor=True), zoom=MG4_ZOOM)
        x, y, w, h = rect
        return Fixed(Transform(Solid(color, xysize=(w, h)), pos=(x, y)),
                     xysize=(1920, 1080))

    # IMAGEM: minigame4/mg4_bg_<fase>.png — fundo cheio de cada fase (laboratório),
    # <fase> = dock (vírus/antígeno à esquerda com 3 encaixes), idga (placa de
    # gel de ágar com o poço de antígeno e 3 poços de amostra, linhas de
    # precipitação já desenhadas: poço 1 positivo, poço 2 NEGATIVO = Golias,
    # poço 3 positivo — ver MG4_IDGA_TRUTH), elisa (placa de 96 poços com 6
    # poços usados: C-, C+, A1, A2, A3, A4, com a cor da reação, ver
    # MG4_OD_POS) e teste (laboratório). A coluna da direita (x >= 1000) fica
    # livre para a interação. Canvas 960x540. 4 arquivos.
    MG4_BG = dict(
        (st["id"], mg4_art("mg4_bg_%s.png" % st["id"], (0, 0, 1920, 1080),
                           "FUNDO: %s\n(mg4_bg_%s.png)" % (st["id"].upper(), st["id"]), "#33403a"))
        for st in MG4_STEPS
    )

    # IMAGEM: minigame4/mg4_fase_<fase>.png — título + enunciado de cada fase,
    # já desenhados (ex.: "Fase 1/4 — Formação do imunocomplexo: clique nos
    # anticorpos que se encaixam no vírus"). Canvas 960x540. 4 arquivos.
    MG4_HEADER_ART = [
        mg4_art("mg4_fase_%s.png" % st["id"], MG4_HEADER_RECT,
                "FASE %d/%d — %s\n(mg4_fase_%s.png)" % (i + 1, len(MG4_STEPS), st["title"], st["id"]),
                "#33363a")
        for i, st in enumerate(MG4_STEPS)
    ]

    # IMAGEM: minigame4/anticorpo_<n>.png — cada anticorpo candidato da fase 1
    # (moldura + desenho + nome), na posição dele. <n> = 1 a 6 (esquerda->direita,
    # cima->baixo). Canvas 960x540. 6 arquivos.
    # IMAGEM: minigame4/mg4_ligado_<n>.png — camada transparente que marca um
    # anticorpo já acoplado (ex.: esmaecido). 6 arquivos.
    # IMAGEM: minigame4/mg4_errado_<n>.png — camada transparente vermelha que
    # marca um anticorpo errado já tentado. 6 arquivos.
    # IMAGEM: minigame4/acoplado_<n>.png — o anticorpo <n> ENCAIXADO no antígeno
    # (à esquerda), só para os 3 que encaixam: <n> = 2, 3 e 5. Fundo transparente.
    # (O imunocomplexo formado agora é um FUNDO inteiro: mg4_bg_complexo.png, abaixo.)
    MG4_CAND_ART = [
        mg4_art("anticorpo_%d.png" % (n + 1), mg4_cand_rect(n),
                "%s\n(anticorpo_%d.png)" % (c[0], n + 1), "#4a4a4a")
        for n, c in enumerate(MG4_CANDIDATES)
    ]
    MG4_CAND_BOUND = [mg4_overlay("mg4_ligado_%d.png" % (n + 1), mg4_cand_rect(n), "#00000099") for n in range(len(MG4_CANDIDATES))]
    MG4_CAND_WRONG = [mg4_overlay("mg4_errado_%d.png" % (n + 1), mg4_cand_rect(n), "#cc222266") for n in range(len(MG4_CANDIDATES))]
    MG4_DOCKED_ART = {}
    _site = 0
    for _n, _c in enumerate(MG4_CANDIDATES):
        if _c[1]:
            MG4_DOCKED_ART[_n] = mg4_art("acoplado_%d.png" % (_n + 1), MG4_SITE_RECTS[_site],
                                         "ENCAIXADO\n(acoplado_%d.png)" % (_n + 1), "#2c6e8a")
            _site += 1
    # IMAGEM: minigame4/mg4_bg_complexo.png — FUNDO CHEIO da fase 1 com o
    # imunocomplexo já formado (vírus + os 3 anticorpos acoplados, brilho etc.).
    # Quando o jogador acopla o último anticorpo certo, este fundo SUBSTITUI o
    # mg4_bg_dock.png (e os acoplado_N deixam de ser desenhados). Canvas 960x540,
    # com a mesma cena do mg4_bg_dock (só o vírus acoplado muda). Se o PNG não
    # existir, vale o esquema antigo: acoplado_N + um aviso placeholder.
    MG4_BG_COMPLEX_REAL = renpy.loadable(MG4_ART_DIR + "mg4_bg_complexo.png")
    MG4_BG_COMPLEX = mg4_art("mg4_bg_complexo.png", (0, 0, 1920, 1080),
                             "FUNDO: IMUNOCOMPLEXO FORMADO\n(mg4_bg_complexo.png)", "#2e5a3a")
    MG4_COMPLEX_ART = mg4_art("mg4_bg_complexo.png", MG4_COMPLEX_RECT, "IMUNOCOMPLEXO FORMADO\n(mg4_bg_complexo.png)", "#2e7d32", fill=False)

    # IMAGEM: minigame4/<campo>_<estado>.png — cada campo das fases 2, 3 e 4
    # (moldura + texto já desenhados), na posição do campo. <campo> = idga_1,
    # idga_2, idga_3, elisa_1 ... elisa_4, teste_1 ... teste_5 (ver MG4_STEPS).
    # Estados: vazio (ainda sem resposta, "?") e as opções em ordem de ciclo:
    #   idga_* e elisa_*: positivo, negativo     teste_*: idga, elisa
    # Canvas 960x540. 12 campos x 3 = 36 arquivos.
    MG4_FIELD_ART = {}
    for _st in MG4_STEPS:
        if _st["kind"] == "fields":
            _keys = MG4_OPT_KEYS[_st["type"]]
            _labels = MG4_OPT_LABELS[_st["type"]]
            for _f, _field in enumerate(_st["fields"]):
                _rect = mg4_field_rect(_f)
                MG4_FIELD_ART[_field["id"]] = [
                    mg4_art("%s_vazio.png" % _field["id"], _rect,
                            "%s: ?\n(%s_vazio.png)" % (_field["label"], _field["id"]), "#4a4a4a")
                ] + [
                    mg4_art("%s_%s.png" % (_field["id"], _keys[o]), _rect,
                            "%s: %s\n(%s_%s.png)" % (_field["label"], _labels[o], _field["id"], _keys[o]), "#4a4a4a")
                    for o in range(len(_keys))
                ]

    # IMAGEM: minigame4/mg4_campo_certo_<n>.png e mg4_campo_errado_<n>.png —
    # camadas transparentes (verde / vermelha) sobre o campo de posição <n> =
    # 1 a 5 (valem para as fases 2, 3 e 4). Canvas 960x540. 10 arquivos.
    MG4_FIELD_RIGHT = [mg4_overlay("mg4_campo_certo_%d.png" % (f + 1), mg4_field_rect(f), "#2e7d3277") for f in range(5)]
    MG4_FIELD_WRONG = [mg4_overlay("mg4_campo_errado_%d.png" % (f + 1), mg4_field_rect(f), "#cc222277") for f in range(5)]

    # IMAGEM: minigame4/mg4_confirmar_idle.png, _hover.png e _disabled.png —
    # botão "Confirmar" (texto desenhado). disabled = enquanto houver campo
    # vazio. Canvas 960x540.
    MG4_CONFIRM_IDLE = mg4_art("mg4_confirmar_idle.png", MG4_CONFIRM_RECT, "CONFIRMAR\n(mg4_confirmar_idle.png)", "#3a5a3a")
    MG4_CONFIRM_HOVER = mg4_art("mg4_confirmar_hover.png", MG4_CONFIRM_RECT, "CONFIRMAR\n(mg4_confirmar_hover.png)", "#4f7a4f")
    MG4_CONFIRM_DISABLED = mg4_art("mg4_confirmar_disabled.png", MG4_CONFIRM_RECT, "CONFIRMAR\n(mg4_confirmar_disabled.png)", "#2a2a2a")

    # IMAGEM: minigame4/mg4_seguir_idle.png e mg4_seguir_hover.png — botão
    # "Continuar" da fase 1, depois que o imunocomplexo se forma (texto
    # desenhado), mesma posição do Confirmar. Canvas 960x540.
    MG4_NEXT_IDLE = mg4_art("mg4_seguir_idle.png", MG4_CONFIRM_RECT, "CONTINUAR\n(mg4_seguir_idle.png)", "#3a5a3a")
    MG4_NEXT_HOVER = mg4_art("mg4_seguir_hover.png", MG4_CONFIRM_RECT, "CONTINUAR\n(mg4_seguir_hover.png)", "#4f7a4f")

    # IMAGEM: minigame4/mg4_resultado.png — painel do resultado final, com o
    # texto fixo desenhado; o jogo escreve a pontuação e a frase final em
    # MG4_RESULT_SCORE_POS e MG4_RESULT_VERDICT_POS. Canvas 960x540.
    MG4_RESULT_PANEL = mg4_art("mg4_resultado.png", MG4_RESULT_RECT, "DIAGNÓSTICO CONCLUÍDO!\n(mg4_resultado.png)", "#2e5a3a")

    # IMAGEM: minigame4/mg4_continuar_idle.png e mg4_continuar_hover.png —
    # botão "Continuar" do resultado (texto desenhado). Canvas 960x540.
    MG4_CONTINUE_IDLE = mg4_art("mg4_continuar_idle.png", MG4_CONTINUE_RECT, "CONTINUAR\n(mg4_continuar_idle.png)", "#3a5a3a")
    MG4_CONTINUE_HOVER = mg4_art("mg4_continuar_hover.png", MG4_CONTINUE_RECT, "CONTINUAR\n(mg4_continuar_hover.png)", "#4f7a4f")

    # ---- Efeitos sonoros (só tocam se o arquivo existir) -------------------
    def mg4_sfx(kind):
        files = {
            "hover": "audio/sfx_hover.ogg",
            "click": "audio/sfx_click.ogg",
            "correct": "audio/sfx_correct.ogg",
            "wrong": "audio/sfx_wrong.ogg",
        }
        path = files.get(kind)
        if path and renpy.loadable(path):
            renpy.sound.play(path)

    def mg4_num(x):
        """Número com vírgula decimal e 2 casas (ex.: 0,35)."""
        return ("%.2f" % x).replace(".", ",")


## Estado do minigame (guardado no save / rollback)
default mg4_step = 0          # fase atual (índice em MG4_STEPS)
default mg4_score = 0
default mg4_finished = False  # True depois da última fase
default mg4_docked = []       # fase 1: candidatos já acoplados (índices)
default mg4_tried = []        # fase 1: candidatos errados já tentados (índices)
default mg4_values = []       # por fase de campos: posição atual de cada campo (-1 = vazio)
default mg4_locked = []       # por fase de campos: campo já correto (travado)?
default mg4_wrong = []        # por fase de campos: campo marcado como errado?
default mg4_answers = []      # por fase de campos: índice da opção correta de cada campo
default mg4_hints = []        # por fase de campos: explicação de cada campo
default mg4_od = []           # ELISA: ["0,08", ...] DO dos 6 poços (C-, C+, A1..A4)
default mg4_cutoff = ""       # ELISA: texto do ponto de corte
default mg4_feedback = ""     # última mensagem de feedback
default mg4_feedback_ok = True


init python:

    def mg4_reset():
        """Nova partida: zera o estado e sorteia os valores do ELISA."""
        values, locked, wrong, answers, hints = [], [], [], [], []
        for st in MG4_STEPS:
            n = len(st["fields"]) if st["kind"] == "fields" else 0
            values.append([-1] * n)
            locked.append([False] * n)
            wrong.append([False] * n)
            answers.append([f["answer"] for f in st["fields"]] if n else [])
            hints.append([f["hint"] for f in st["fields"]] if n else [])

        # ---- ELISA: DO sorteadas; a amostra 1 (Golias) é sempre negativa ----
        c_neg = round(renpy.random.uniform(0.04, 0.10), 2)
        c_pos = round(renpy.random.uniform(1.00, 1.60), 2)
        cutoff = round(c_neg + 0.20, 2)
        positives = [False, True, False, True]        # amostras 1..4 (1 = Golias)
        extra = [renpy.random.choice([True, False]) for k in range(2)]
        positives[2], positives[3] = extra
        if not any(positives):
            positives[3] = True
        ods = []
        for pos in positives:
            if pos:
                ods.append(round(renpy.random.uniform(0.55, 1.40), 2))
            else:
                ods.append(round(renpy.random.uniform(0.05, 0.15), 2))

        es = [s["id"] for s in MG4_STEPS].index("elisa")
        for f, od in enumerate(ods):
            is_pos = od >= cutoff
            answers[es][f] = 0 if is_pos else 1
            if is_pos:
                hints[es][f] = _("DO %s é maior ou igual ao ponto de corte (%s): resultado POSITIVO.") % (mg4_num(od), mg4_num(cutoff))
            else:
                hints[es][f] = _("DO %s é menor que o ponto de corte (%s): resultado NEGATIVO.") % (mg4_num(od), mg4_num(cutoff))

        store.mg4_od = [mg4_num(c_neg), mg4_num(c_pos)] + [mg4_num(o) for o in ods]
        store.mg4_cutoff = _("Ponto de corte = DO do controle negativo (%s) + 0,20 = %s") % (mg4_num(c_neg), mg4_num(cutoff))

        store.mg4_values = values
        store.mg4_locked = locked
        store.mg4_wrong = wrong
        store.mg4_answers = answers
        store.mg4_hints = hints
        store.mg4_docked = []
        store.mg4_tried = []
        store.mg4_step = 0
        store.mg4_score = 0
        store.mg4_finished = False
        store.mg4_feedback = ""
        store.mg4_feedback_ok = True

    def mg4_set_feedback(text, ok):
        store.mg4_feedback = text
        store.mg4_feedback_ok = ok

    def mg4_advance():
        """Passa para a próxima fase (ou encerra a partida)."""
        store.mg4_step += 1
        if store.mg4_step >= len(MG4_STEPS):
            store.mg4_finished = True

    def mg4_hit():
        store.mg4_score += MG4_POINTS_HIT
        mg4_sfx("correct")

    def mg4_miss():
        store.mg4_score = max(0, store.mg4_score - MG4_POINTS_MISS)
        mg4_sfx("wrong")

    # ---- Fase 1: acoplar anticorpos ---------------------------------------
    def mg4_dock_done():
        return len(store.mg4_docked) >= MG4_DOCK_TOTAL

    def mg4_dock(n):
        """Clique no anticorpo candidato n."""
        if store.mg4_finished or mg4_dock_done() or n in store.mg4_docked or n in store.mg4_tried:
            return
        text, fits, feedback = MG4_CANDIDATES[n]
        if fits:
            store.mg4_docked.append(n)
            mg4_hit()
            if mg4_dock_done():
                mg4_set_feedback(MG4_COMPLEX_FEEDBACK, True)
            else:
                mg4_set_feedback(feedback, True)
        else:
            store.mg4_tried.append(n)
            mg4_miss()
            mg4_set_feedback(feedback, False)

    def mg4_dock_continue():
        if mg4_dock_done():
            mg4_advance()

    # ---- Fases de campos ---------------------------------------------------
    def mg4_field_art(f):
        """Arte atual do campo f da fase atual (vazio ou a opção escolhida)."""
        field = MG4_STEPS[store.mg4_step]["fields"][f]
        return MG4_FIELD_ART[field["id"]][store.mg4_values[store.mg4_step][f] + 1]

    def mg4_cycle(f):
        """Clique num campo: passa para a próxima opção dele (em ciclo)."""
        s = store.mg4_step
        if store.mg4_finished or store.mg4_locked[s][f]:
            return
        n = len(MG4_OPT_KEYS[MG4_STEPS[s]["type"]])
        store.mg4_values[s][f] = (store.mg4_values[s][f] + 1) % n
        store.mg4_wrong[s][f] = False
        mg4_sfx("click")

    def mg4_confirm():
        """Confirma os campos da fase: trava os certos (+pontos), marca os
        errados (-pontos, com a explicação) e só avança quando todos estiverem
        certos."""
        s = store.mg4_step
        if store.mg4_finished:
            return
        first_hint = None
        for f in range(len(MG4_STEPS[s]["fields"])):
            if store.mg4_locked[s][f]:
                continue
            pos = store.mg4_values[s][f]
            if pos < 0:
                continue
            if pos == store.mg4_answers[s][f]:
                store.mg4_locked[s][f] = True
                store.mg4_wrong[s][f] = False
                mg4_hit()
            else:
                store.mg4_wrong[s][f] = True
                mg4_miss()
                if first_hint is None:
                    first_hint = store.mg4_hints[s][f]

        if all(store.mg4_locked[s]):
            mg4_set_feedback(_("Tudo certo! Fase concluída."), True)
            mg4_advance()
        elif first_hint is not None:
            mg4_set_feedback(first_hint, False)

    def mg4_all_filled():
        """Todos os campos da fase atual já foram escolhidos?"""
        s = store.mg4_step
        return all(store.mg4_locked[s][f] or store.mg4_values[s][f] >= 0
                   for f in range(len(MG4_STEPS[s]["fields"])))

    def mg4_verdict():
        """Frase final conforme o desempenho."""
        ratio = float(store.mg4_score) / max(1, MG4_MAX_SCORE)
        if ratio >= 1.0:
            return _("Diagnóstico perfeito! Você domina o IDGA e o ELISA.")
        elif ratio >= 0.7:
            return _("Bom trabalho! Revise os pontos que errou sobre o IDGA e o ELISA.")
        else:
            return _("Revise como o IDGA e o ELISA funcionam e tente de novo.")


## -----------------------------------------------------------------------
## 1.5) TELA DE INSTRUÇÕES
##    Uso: call screen minigame4_instructions
##    Modal: bloqueia qualquer clique no que estiver atrás até "Entendi".
## -----------------------------------------------------------------------
init python:

    # IMAGEM: minigame4/mg4_instructions_bg.png — fundo cheio. Canvas 960x540.
    MG4_INSTR_BG = mg4_art("mg4_instructions_bg.png", (0, 0, 1920, 1080),
                           "FUNDO: instruções\n(mg4_instructions_bg.png)", "#2a2418")

    # IMAGEM: minigame4/mg4_instructions_panel.png — moldura do texto de regras,
    # sem texto (o texto é escrito pelo jogo, centralizado em (960, 490), com
    # até 1000 px de largura). Canvas 960x540.
    MG4_INSTR_PANEL = mg4_art("mg4_instructions_panel.png", MG4_INSTR_PANEL_RECT,
                              "MOLDURA DE TEXTO\n(mg4_instructions_panel.png)", "#4a3a20")

    # IMAGEM: minigame4/mg4_close_idle.png e mg4_close_hover.png — botão
    # "Entendi" (texto desenhado). Canvas 960x540.
    MG4_CLOSE_IDLE = mg4_art("mg4_close_idle.png", MG4_CLOSE_RECT, "ENTENDI\n(mg4_close_idle.png)", "#3a5a3a")
    MG4_CLOSE_HOVER = mg4_art("mg4_close_hover.png", MG4_CLOSE_RECT, "ENTENDI\n(mg4_close_hover.png)", "#4f7a4f")

style mg4_instructions_text:
    text_align 0.5
    color "#ffffff"
    size 30
    xsize 1000


screen minigame4_instructions():

    modal True  # impede qualquer clique/interação com o jogo por trás

    add MG4_INSTR_BG
    add MG4_INSTR_PANEL

    # Texto de regras de exemplo — edite como quiser
    text _("A amostra do Golias chegou ao laboratório!\n\nPrimeiro, forme o imunocomplexo: clique nos anticorpos que se encaixam no vírus da AIE. Depois, leia os resultados do IDGA e do ELISA e descubra qual é qual.\n\nCada conduta correta marca pontos; cada erro tira pontos.") style "mg4_instructions_text" pos (960, 490) anchor (0.5, 0.5)

    imagebutton:
        idle MG4_CLOSE_IDLE
        hover MG4_CLOSE_HOVER
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
screen minigame4_gameplay():

    modal True  # bloqueia qualquer interação com o que estiver atrás

    $ step = MG4_STEPS[min(mg4_step, len(MG4_STEPS) - 1)]

    # Fundo da fase atual (cena à esquerda). Na fase 1, com o imunocomplexo
    # formado, entra o fundo mg4_bg_complexo (se existir).
    $ complex_bg = (step["id"] == "dock" and len(mg4_docked) >= MG4_DOCK_TOTAL and MG4_BG_COMPLEX_REAL)
    if complex_bg:
        add MG4_BG_COMPLEX
    else:
        add MG4_BG[step["id"]]

    # Pontuação atual (texto que muda)
    text _("Pontos: [mg4_score]"):
        pos MG4_SCORE_POS
        size 36
        color "#ffffff"

    if not mg4_finished:

        # Título + enunciado da fase (arte própria de cada fase)
        add MG4_HEADER_ART[mg4_step]

        # ---- Fase 1: anticorpos candidatos ------------------------------
        if step["kind"] == "dock":

            for n in range(len(MG4_CANDIDATES)):

                $ cand_bound = n in mg4_docked
                $ cand_tried = n in mg4_tried

                button:
                    xysize (1920, 1080)
                    background None
                    focus_mask True
                    sensitive not (cand_bound or cand_tried or len(mg4_docked) >= MG4_DOCK_TOTAL)
                    action Function(mg4_dock, n)
                    hovered Function(mg4_sfx, "hover")
                    add MG4_CAND_ART[n]
                    if cand_bound:
                        add MG4_CAND_BOUND[n]
                    elif cand_tried:
                        add MG4_CAND_WRONG[n]

            # Anticorpos já encaixados no antígeno (à esquerda)
            if not complex_bg:
                for n in mg4_docked:
                    add MG4_DOCKED_ART[n]

            # Imunocomplexo formado + botão Continuar
            if len(mg4_docked) >= MG4_DOCK_TOTAL:
                if not complex_bg:
                    add MG4_COMPLEX_ART
                imagebutton:
                    idle MG4_NEXT_IDLE
                    hover MG4_NEXT_HOVER
                    focus_mask True
                    action [Play("sound", "audio/sfx_click.ogg"), Function(mg4_dock_continue)]
                    hovered Function(mg4_sfx, "hover")

        # ---- Fases de campos: IDGA, ELISA e diferenças -----------------
        else:

            # ELISA: valores de DO e ponto de corte escritos pelo jogo
            if step["id"] == "elisa":
                for i in range(len(mg4_od)):
                    $ od_text = mg4_od[i]
                    text "[od_text]":
                        pos MG4_OD_POS[i]
                        anchor (0.5, 0.5)
                        size 32
                        bold True
                        color "#ffffff"
                text "[mg4_cutoff!t]":
                    pos MG4_CUTOFF_POS
                    size 28
                    color "#ffe9a3"

            for f in range(len(step["fields"])):

                $ field_locked = mg4_locked[mg4_step][f]
                $ field_wrong = mg4_wrong[mg4_step][f]

                button:
                    xysize (1920, 1080)
                    background None
                    focus_mask True
                    sensitive not field_locked
                    action Function(mg4_cycle, f)
                    hovered Function(mg4_sfx, "hover")
                    add mg4_field_art(f)
                    if field_locked:
                        add MG4_FIELD_RIGHT[f]
                    elif field_wrong:
                        add MG4_FIELD_WRONG[f]

            imagebutton:
                idle MG4_CONFIRM_IDLE
                hover MG4_CONFIRM_HOVER
                insensitive MG4_CONFIRM_DISABLED
                sensitive mg4_all_filled()
                focus_mask True
                action Function(mg4_confirm)
                hovered Function(mg4_sfx, "hover")

        # ---- Feedback da última ação (texto que muda) -------------------
        if mg4_feedback:
            text "[mg4_feedback!t]":
                pos MG4_FEEDBACK_POS
                size 24
                xmaximum MG4_FEEDBACK_W
                color ("#b9f5b9" if mg4_feedback_ok else "#ffb3b3")

    # ---- Fim: resultado final --------------------------------------------
    else:

        $ verdict = mg4_verdict()

        button:
            xfill True
            yfill True
            background "#000000aa"
            action NullAction()

        add MG4_RESULT_PANEL

        text _("Pontuação: [mg4_score] / [MG4_MAX_SCORE]"):
            pos MG4_RESULT_SCORE_POS
            anchor (0.5, 0.5)
            size 40
            color "#ffffff"

        text "[verdict!t]":
            pos MG4_RESULT_VERDICT_POS
            anchor (0.5, 0.0)
            text_align 0.5
            size 28
            color "#ffffff"
            xmaximum 880

        imagebutton:
            idle MG4_CONTINUE_IDLE
            hover MG4_CONTINUE_HOVER
            focus_mask True
            action [Play("sound", "audio/sfx_click.ogg"), Return(True)]
            hovered Function(mg4_sfx, "hover")


## -----------------------------------------------------------------------
## 3) LABEL DO GAMEPLAY (motor do minigame em si)
## -----------------------------------------------------------------------
label minigame_4_gameplay:

    $ quick_menu = False       # esconde os botões rápidos do rodapé durante o minigame
    $ renpy.block_rollback()   # impede que o rollback (roda do mouse) bagunce o estado
    $ mg4_reset()              # zera o estado e sorteia o ELISA (permite rejogar)

    scene black
    call screen minigame4_gameplay   # só retorna quando o jogador clica em "Continuar"

    $ quick_menu = True
    return


## -----------------------------------------------------------------------
## 4) PONTO DE ENTRADA (chamado pelo roadmap.rpy: "call expression 'minigame_4_entry'")
##    Mostra as instruções, roda o gameplay e avisa o mapa que terminou.
## -----------------------------------------------------------------------
label minigame_4_entry:

    call screen minigame4_instructions
    call minigame_4_gameplay

    $ mg_report_score(4, mg4_score, MG4_MAX_SCORE)  # registra o placar e a medalha, se for o caso
    $ mg_complete(4)                                 # marca como concluído e libera o 5

    return
