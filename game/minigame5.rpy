################################################################################
# MINIGAME5.RPY
# Minigame 5: "Triagem de cavalos recém-chegados"
#
# Como funciona:
#   - 5 cavalos chegam, UM DE CADA VEZ. Para cada um aparecem os PAPÉIS: nome,
#     resultado do exame de AIE e data da coleta, junto com a DATA DE HOJE.
#   - O jogador confere os papéis (resultado + validade do exame) e manda o
#     cavalo para o destino certo, DENTRO DE UM LIMITE DE TEMPO por cavalo
#     (barra de tempo). Se o tempo acabar, conta como erro.
#
#   Cada caso tem um destino certo:
#     - Exame NEGATIVO e RECENTE (dentro da validade) ........ ESTÁBULO
#     - Exame NEGATIVO e VENCIDO (passou da validade) ........ NOVA COLETA
#     - Exame POSITIVO (qualquer data) ........................ NOTIFICAR O MAPA
#     - Exame EM PROCESSAMENTO (ainda sem resultado) .......... QUARENTENA
#       (o 4º caso vem do seu texto: "em processamento" -> quarentena; se não
#       quiser, tire "processamento" da lista MG5_KINDS)
#
#   Os cavalos e os casos são sorteados a cada partida (todo tipo de caso
#   aparece pelo menos uma vez), e as datas variam.
#
# Pontuação (ver roadmap.rpy para o sistema de medalhas):
#   + MG5_POINTS_HIT por acerto. Erro ou tempo esgotado = 0 (a pontuação é
#   o número de acertos). Máximo = 5 acertos = medalha. Depois de cada cavalo
#   aparece o motivo do acerto/erro.
#
# ARTE (mesmo esquema do menu, roadmap e minigames 2, 3 e 4):
#   TODA arte real é um PNG de CANVAS INTEIRO (960x540), com o elemento já na
#   posição certa. O jogo amplia 2x (nearest neighbor) e desenha em (0, 0), sem
#   usar posição do código; focus_mask True faz só os pixels opacos de cada
#   botão responderem ao mouse.
#   Enquanto o PNG não existe, aparece um placeholder colorido com texto, na
#   posição das constantes MG5_*_RECT abaixo (só servem aos placeholders).
#   Textos fixos vêm DESENHADOS na arte; o jogo só escreve o que muda: nome,
#   resultado e datas nos papéis, contador, pontos, motivo e resultado final.
#
# ATENÇÃO — conteúdo: a validade do exame (MG5_VALIDITY_DAYS) é um valor de
# exemplo; use o prazo correto da norma que o seu jogo segue.
#
# Este arquivo contém: dados/configuração, lógica, tela de instruções, telas
# do gameplay e o "label minigame_5_entry" — chamado pelo roadmap.rpy.
################################################################################


## -----------------------------------------------------------------------
## 1) CONFIGURAÇÃO, DADOS E LÓGICA
## -----------------------------------------------------------------------
init python:

    import datetime

    MG5_ART_DIR = "images/minigame5/"
    MG5_ZOOM = 2.0  # arte a 960x540, exibida em 1920x1080

    # ---- Posições dos PLACEHOLDERS (tela 1920x1080): (x, y, largura, altura)
    # Esquerda = cavalo; direita = papéis, tempo e destinos.
    MG5_TITLE_RECT = (1000, 30, 880, 100)
    MG5_TIMER_RECT = (1000, 140, 880, 24)             # barra de tempo
    MG5_PAPERS_RECT = (1000, 180, 880, 340)           # papéis do cavalo
    MG5_HORSE_RECT = (60, 240, 860, 700)              # cavalo (esquerda)

    def mg5_dest_rect(i):                             # 4 destinos em 2x2
        return (1000 + (i % 2) * 450, 560 + (i // 2) * 200, 430, 180)

    MG5_STAMP_RECT = (60, 160, 860, 140)              # carimbo certo/errado
    MG5_NEXT_RECT = (1000, 880, 880, 100)             # botão Próximo (feedback)
    MG5_RESULT_RECT = (460, 330, 1000, 420)
    MG5_CONTINUE_RECT = (750, 800, 420, 90)
    MG5_INSTR_PANEL_RECT = (360, 190, 1200, 600)
    MG5_CLOSE_RECT = (840, 860, 240, 80)

    # Barra de tempo: ela encolhe da direita para a esquerda entre estes x
    # (em pixels da tela 1920). Com a arte real, coloque aqui o x onde a barra
    # começa e termina no seu PNG.
    MG5_TIMER_X0 = MG5_TIMER_RECT[0]
    MG5_TIMER_X1 = MG5_TIMER_RECT[0] + MG5_TIMER_RECT[2]

    # Textos escritos pelo jogo (mudam durante a partida). Posições = canto
    # superior esquerdo do texto; ajuste ao encaixar a arte dos papéis.
    MG5_NAME_POS = (1300, 215)                        # nome do cavalo
    MG5_RESULT_POS = (1300, 285)                      # resultado do exame
    MG5_EXAMDATE_POS = (1300, 355)                    # data da coleta
    MG5_TODAY_POS = (1300, 425)                       # data de hoje
    MG5_RULE_POS = (1020, 478)                        # regra de validade
    MG5_COUNTER_POS = (60, 40)                        # "Cavalo n/5"
    MG5_SCORE_POS = (60, 90)                          # "Pontos: N"
    MG5_REASON_POS = (60, 330)                        # motivo (tela de feedback)
    MG5_REASON_W = 860
    MG5_RESULT_SCORE_POS = (960, 470)                 # "Pontuação: N / M" (centralizado)
    MG5_RESULT_VERDICT_POS = (960, 560)               # frase final (centralizada)

    # ---- Regras ------------------------------------------------------------
    MG5_POINTS_HIT = 10
    MG5_TIME_PER_HORSE = 15.0         # segundos para decidir cada cavalo
    MG5_VALIDITY_DAYS = 60            # validade do exame negativo (exemplo!)
    MG5_TODAY = datetime.date(2025, 5, 20)            # "data de hoje" do jogo

    # Tipos de caso e o destino certo de cada um
    MG5_KINDS = ["recente", "vencido", "positivo", "processamento"]
    MG5_KIND_DEST = {
        "recente": "estabulo",
        "vencido": "coleta",
        "positivo": "mapa",
        "processamento": "quarentena",
    }

    # Destinos (a ordem define o slot 0-3 do botão e das artes destino_<id>_*)
    MG5_DESTS = [
        ("estabulo", _("Estábulo")),
        ("quarentena", _("Quarentena")),
        ("coleta", _("Nova coleta")),
        ("mapa", _("Notificar o MAPA")),
    ]

    # Os 5 cavalos: (nome, número da arte cavalo_<n>.png)
    MG5_HORSES = [
        ("Trovão", 1), ("Pérola", 2), ("Relâmpago", 3), ("Aurora", 4), ("Bandeirante", 5),
    ]
    MG5_TOTAL = len(MG5_HORSES)

    # Pontuação máxima: todos os cavalos no destino certo
    MG5_MAX_SCORE = MG5_TOTAL * MG5_POINTS_HIT

    # ---- Placeholders de arte ----------------------------------------------
    def mg5_art(filename, rect, label, color, fill=True):
        """Arte de canvas inteiro (960x540 → 1920x1080, nearest neighbor,
        desenhada em (0, 0)) se o PNG existir. Senão, um placeholder: retângulo
        colorido com texto na posição "rect" = (x, y, largura, altura).
        fill=False = só o texto, sem retângulo."""
        path = MG5_ART_DIR + filename
        if renpy.loadable(path):
            return Transform(Image(path, nearest_neighbor=True), zoom=MG5_ZOOM)

        x, y, w, h = rect
        text = Text(label, size=26, color="#ffffff", xalign=0.5, yalign=0.5,
                    text_align=0.5, xmaximum=w - 20)
        if fill:
            box = Fixed(Solid(color, xysize=(w, h)), text, xysize=(w, h))
        else:
            box = Fixed(text, xysize=(w, h))
        return Fixed(Transform(box, pos=(x, y)), xysize=(1920, 1080))

    # IMAGEM: minigame5/mg5_bg.png — fundo cheio: área de triagem da fazenda, com
    # espaço para o cavalo à ESQUERDA; a coluna da direita (x >= 1000) fica livre
    # para papéis, tempo e destinos. Canvas 960x540.
    MG5_BG = mg5_art("mg5_bg.png", (0, 0, 1920, 1080), "FUNDO: triagem\n(mg5_bg.png)", "#4a4a36")

    # IMAGEM: minigame5/mg5_titulo.png — painel de título ("5 - TRIAGEM DE
    # CAVALOS", com o texto desenhado). Canvas 960x540.
    MG5_TITLE_PANEL = mg5_art("mg5_titulo.png", MG5_TITLE_RECT, "5 - TRIAGEM DE CAVALOS\n(mg5_titulo.png)", "#4a3a20")

    # IMAGEM: minigame5/cavalo_<n>.png — cada cavalo (<n> = 1 a 5), na posição
    # dele à esquerda, em fundo transparente. Canvas 960x540. 5 arquivos.
    MG5_HORSE_ART = dict(
        (num, mg5_art("cavalo_%d.png" % num, MG5_HORSE_RECT,
                      "CAVALO %d: %s\n(cavalo_%d.png)" % (num, name, num), "#6b5a43"))
        for name, num in MG5_HORSES
    )

    # IMAGEM: minigame5/mg5_papeis.png — a ficha/papéis do cavalo, com os
    # RÓTULOS fixos já desenhados ("Nome:", "Exame de AIE:", "Data da coleta:",
    # "Hoje:"); o jogo escreve os valores por cima, em MG5_NAME_POS,
    # MG5_RESULT_POS, MG5_EXAMDATE_POS e MG5_TODAY_POS. Canvas 960x540.
    MG5_PAPERS = mg5_art("mg5_papeis.png", MG5_PAPERS_RECT,
                         "PAPÉIS\nNome / Exame de AIE / Data da coleta / Hoje\n(mg5_papeis.png)", "#d8cfa8")

    # IMAGEM: minigame5/mg5_tempo_moldura.png — moldura da barra de tempo.
    # IMAGEM: minigame5/mg5_tempo_barra.png — a barra CHEIA (ela é "recortada" da
    # direita para a esquerda durante a contagem; ajuste MG5_TIMER_X0/X1 para os
    # x onde a barra começa e termina). Canvas 960x540.
    MG5_TIMER_FRAME = mg5_art("mg5_tempo_moldura.png", MG5_TIMER_RECT, "", "#222222")
    MG5_TIMER_FILL = mg5_art("mg5_tempo_barra.png", MG5_TIMER_RECT, "", "#e0b030")

    # IMAGEM: minigame5/destino_<id>_idle.png e destino_<id>_hover.png — os 4
    # botões de destino (moldura + texto já desenhados). <id> = estabulo,
    # quarentena, coleta, mapa. Canvas 960x540. 8 arquivos.
    MG5_DEST_IDLE = {}
    MG5_DEST_HOVER = {}
    for _i, (_id, _label) in enumerate(MG5_DESTS):
        MG5_DEST_IDLE[_id] = mg5_art("destino_%s_idle.png" % _id, mg5_dest_rect(_i),
                                     "%s\n(destino_%s_idle.png)" % (_label, _id), "#3a5a3a")
        MG5_DEST_HOVER[_id] = mg5_art("destino_%s_hover.png" % _id, mg5_dest_rect(_i),
                                      "%s\n(destino_%s_hover.png)" % (_label, _id), "#4f7a4f")

    # IMAGEM: minigame5/mg5_certo.png e mg5_errado.png — carimbo/aviso que
    # aparece na tela de feedback (ex.: "CORRETO!" verde / "ERRADO!" vermelho).
    # Canvas 960x540, fundo transparente.
    MG5_STAMP_OK = mg5_art("mg5_certo.png", MG5_STAMP_RECT, "CORRETO!\n(mg5_certo.png)", "#2e7d32")
    MG5_STAMP_BAD = mg5_art("mg5_errado.png", MG5_STAMP_RECT, "ERRADO!\n(mg5_errado.png)", "#8a2c2c")

    # IMAGEM: minigame5/mg5_proximo_idle.png e mg5_proximo_hover.png — botão
    # "Próximo cavalo" da tela de feedback (texto desenhado). Canvas 960x540.
    MG5_NEXT_IDLE = mg5_art("mg5_proximo_idle.png", MG5_NEXT_RECT, "PRÓXIMO CAVALO\n(mg5_proximo_idle.png)", "#3a5a3a")
    MG5_NEXT_HOVER = mg5_art("mg5_proximo_hover.png", MG5_NEXT_RECT, "PRÓXIMO CAVALO\n(mg5_proximo_hover.png)", "#4f7a4f")

    # IMAGEM: minigame5/mg5_resultado.png — painel do resultado final, com o
    # texto fixo desenhado; o jogo escreve a pontuação e a frase final em
    # MG5_RESULT_SCORE_POS e MG5_RESULT_VERDICT_POS. Canvas 960x540.
    MG5_RESULT_PANEL = mg5_art("mg5_resultado.png", MG5_RESULT_RECT, "TRIAGEM CONCLUÍDA!\n(mg5_resultado.png)", "#2e5a3a")

    # IMAGEM: minigame5/mg5_continuar_idle.png e mg5_continuar_hover.png —
    # botão "Continuar" do resultado (texto desenhado). Canvas 960x540.
    MG5_CONTINUE_IDLE = mg5_art("mg5_continuar_idle.png", MG5_CONTINUE_RECT, "CONTINUAR\n(mg5_continuar_idle.png)", "#3a5a3a")
    MG5_CONTINUE_HOVER = mg5_art("mg5_continuar_hover.png", MG5_CONTINUE_RECT, "CONTINUAR\n(mg5_continuar_hover.png)", "#4f7a4f")

    # ---- Efeitos sonoros (só tocam se o arquivo existir) -------------------
    def mg5_sfx(kind):
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
default mg5_horses = []       # os 5 casos desta partida (dicts, ver mg5_reset)
default mg5_index = 0         # cavalo atual (0 a 4)
default mg5_score = 0
default mg5_last_ok = False   # a última decisão foi certa?
default mg5_last_reason = ""  # motivo da última decisão


init python:

    def mg5_fmt_date(d):
        return d.strftime("%d/%m/%Y")

    def mg5_make_case(kind):
        """Sorteia as datas/resultado de um caso do tipo "kind"."""
        v = MG5_VALIDITY_DAYS
        if kind == "recente":
            days, result = renpy.random.randint(5, v - 10), "negativo"
        elif kind == "vencido":
            days, result = renpy.random.randint(v + 6, v + 60), "negativo"
        elif kind == "positivo":
            days, result = renpy.random.randint(5, v + 30), "positivo"
        else:
            days, result = renpy.random.randint(1, 5), "processamento"
        exam_date = MG5_TODAY - datetime.timedelta(days=days)
        return {"kind": kind, "result": result, "days": days,
                "date": mg5_fmt_date(exam_date)}

    def mg5_reset():
        """Nova partida: sorteia os 5 casos (todo tipo aparece pelo menos uma
        vez) e a ordem em que os cavalos chegam."""
        kinds = list(MG5_KINDS)
        while len(kinds) < MG5_TOTAL:
            kinds.append(renpy.random.choice(MG5_KINDS))
        kinds = kinds[:MG5_TOTAL]
        renpy.random.shuffle(kinds)

        horses = list(MG5_HORSES)
        renpy.random.shuffle(horses)

        cases = []
        for (name, num), kind in zip(horses, kinds):
            case = mg5_make_case(kind)
            case["name"] = name
            case["art"] = num
            cases.append(case)

        store.mg5_horses = cases
        store.mg5_index = 0
        store.mg5_score = 0
        store.mg5_last_ok = False
        store.mg5_last_reason = ""

    def mg5_result_text(case):
        return {"negativo": _("Negativo"),
                "positivo": _("Positivo"),
                "processamento": _("Em processamento")}[case["result"]]

    def mg5_correct_text(case):
        """Explicação da conduta certa para o caso."""
        kind, days = case["kind"], case["days"]
        if kind == "recente":
            return _("Exame negativo de %d dias atrás, dentro da validade de %d dias: o cavalo vai para o ESTÁBULO.") % (days, MG5_VALIDITY_DAYS)
        elif kind == "vencido":
            return _("Exame negativo de %d dias atrás, passou da validade de %d dias: é preciso uma NOVA COLETA.") % (days, MG5_VALIDITY_DAYS)
        elif kind == "positivo":
            return _("Resultado POSITIVO para AIE: a conduta é a NOTIFICAÇÃO ao MAPA, qualquer que seja a data do exame.")
        else:
            return _("O exame ainda está EM PROCESSAMENTO: o cavalo fica em QUARENTENA até sair o resultado.")

    def mg5_resolve(choice):
        """Aplica a decisão do jogador ("estabulo", "quarentena", "coleta",
        "mapa" ou "timeout") ao cavalo atual."""
        case = store.mg5_horses[store.mg5_index]
        correct = MG5_KIND_DEST[case["kind"]]
        reason = mg5_correct_text(case)
        if choice == correct:
            store.mg5_score += MG5_POINTS_HIT
            store.mg5_last_ok = True
            store.mg5_last_reason = _("Correto! ") + reason
            mg5_sfx("correct")
        else:
            store.mg5_last_ok = False
            if choice == "timeout":
                store.mg5_last_reason = _("Tempo esgotado! ") + reason
            else:
                store.mg5_last_reason = _("Destino errado! ") + reason
            mg5_sfx("wrong")

    def mg5_verdict():
        """Frase final conforme o desempenho."""
        ratio = float(store.mg5_score) / max(1, MG5_MAX_SCORE)
        if ratio >= 1.0:
            return _("Triagem perfeita! Todos os cavalos foram para o destino certo.")
        elif ratio >= 0.6:
            return _("Boa triagem! Mas alguns cavalos foram para o destino errado.")
        else:
            return _("Revise as regras de triagem do exame de AIE e tente de novo.")


## -----------------------------------------------------------------------
## 1.5) TELA DE INSTRUÇÕES
##    Uso: call screen minigame5_instructions
##    Modal: bloqueia qualquer clique no que estiver atrás até "Entendi".
## -----------------------------------------------------------------------
init python:

    # IMAGEM: minigame5/mg5_instructions_bg.png — fundo cheio. Canvas 960x540.
    MG5_INSTR_BG = mg5_art("mg5_instructions_bg.png", (0, 0, 1920, 1080),
                           "FUNDO: instruções\n(mg5_instructions_bg.png)", "#2a2418")

    # IMAGEM: minigame5/mg5_instructions_panel.png — moldura do texto de regras,
    # sem texto (o texto é escrito pelo jogo, centralizado em (960, 490), com
    # até 1000 px de largura). Canvas 960x540.
    MG5_INSTR_PANEL = mg5_art("mg5_instructions_panel.png", MG5_INSTR_PANEL_RECT,
                              "MOLDURA DE TEXTO\n(mg5_instructions_panel.png)", "#4a3a20")

    # IMAGEM: minigame5/mg5_close_idle.png e mg5_close_hover.png — botão
    # "Entendi" (texto desenhado). Canvas 960x540.
    MG5_CLOSE_IDLE = mg5_art("mg5_close_idle.png", MG5_CLOSE_RECT, "ENTENDI\n(mg5_close_idle.png)", "#3a5a3a")
    MG5_CLOSE_HOVER = mg5_art("mg5_close_hover.png", MG5_CLOSE_RECT, "ENTENDI\n(mg5_close_hover.png)", "#4f7a4f")

style mg5_instructions_text:
    text_align 0.5
    color "#ffffff"
    size 28
    xsize 1000


screen minigame5_instructions():

    modal True  # impede qualquer clique/interação com o jogo por trás

    add MG5_INSTR_BG
    add MG5_INSTR_PANEL

    # Texto de regras de exemplo — edite como quiser (os números vêm das constantes)
    $ instr_text = _("Chegaram %d cavalos para a triagem!\n\nConfira os papéis de cada um e compare a data do exame com a data de hoje (a validade é de %d dias). Você tem %d segundos por cavalo:\n\n• Negativo e recente: Estábulo\n• Negativo e vencido: Nova coleta\n• Positivo: Notificar o MAPA\n• Em processamento: Quarentena\n\nCada acerto marca pontos.") % (MG5_TOTAL, MG5_VALIDITY_DAYS, int(MG5_TIME_PER_HORSE))

    text "[instr_text]" style "mg5_instructions_text" pos (960, 490) anchor (0.5, 0.5)

    imagebutton:
        idle MG5_CLOSE_IDLE
        hover MG5_CLOSE_HOVER
        focus_mask True
        action [
            Play("sound", "audio/sfx_click.ogg"),
            Return(True),  # devolve o controle ao "call screen" que a chamou
        ]
        hovered Play("sound", "audio/sfx_hover.ogg")


## -----------------------------------------------------------------------
## 2) TELAS DO MINIGAME
##    Todo botão é uma arte de canvas inteiro (1920x1080 na tela), desenhada
##    em (0, 0); focus_mask True limita o clique aos pixels opacos da arte.
##    Cada cavalo é uma chamada própria de "call screen": o timer e a barra de
##    tempo sempre começam do zero.
## -----------------------------------------------------------------------

# Barra de tempo: encolhe da direita para a esquerda (recorta a arte cheia)
transform mg5_timer_crop(x1, x0, duration):
    crop (0, 0, x1, 1080)
    linear duration crop (0, 0, x0, 1080)


# Fundo + cavalo + título + contador + pontos (comum às telas do cavalo/feedback)
screen mg5_scene():

    $ case = mg5_horses[mg5_index]
    $ horse_number = mg5_index + 1

    add MG5_BG
    add MG5_HORSE_ART[case["art"]]
    add MG5_TITLE_PANEL

    text _("Cavalo [horse_number]/[MG5_TOTAL]"):
        pos MG5_COUNTER_POS
        size 36
        color "#ffffff"

    text _("Pontos: [mg5_score]"):
        pos MG5_SCORE_POS
        size 32
        color "#ffffff"


# Um cavalo: papéis, tempo e destinos. Retorna o destino ("estabulo",
# "quarentena", "coleta", "mapa") ou "timeout".
screen minigame5_horse():

    modal True  # bloqueia qualquer interação com o que estiver atrás

    use mg5_scene

    $ case = mg5_horses[mg5_index]
    $ case_name = case["name"]
    $ case_result = mg5_result_text(case)
    $ case_date = case["date"]
    $ today_text = mg5_fmt_date(MG5_TODAY)
    $ rule_text = _("Exame negativo válido por %d dias") % MG5_VALIDITY_DAYS

    # Papéis: rótulos desenhados na arte; valores escritos pelo jogo
    add MG5_PAPERS

    text "[case_name]":
        pos MG5_NAME_POS
        size 36
        bold True
        color "#3a2410"

    text "[case_result!t]":
        pos MG5_RESULT_POS
        size 36
        bold True
        color ("#8a1c1c" if case["result"] == "positivo" else "#3a2410")

    text "[case_date]":
        pos MG5_EXAMDATE_POS
        size 36
        color "#3a2410"

    text "[today_text]":
        pos MG5_TODAY_POS
        size 36
        color "#3a2410"

    text "[rule_text!t]":
        pos MG5_RULE_POS
        size 24
        color "#3a2410"

    # Barra de tempo: moldura fixa + barra que encolhe em MG5_TIME_PER_HORSE s
    add MG5_TIMER_FRAME
    add MG5_TIMER_FILL at mg5_timer_crop(MG5_TIMER_X1, MG5_TIMER_X0, MG5_TIME_PER_HORSE)

    # Destinos
    for dest_id, dest_label in MG5_DESTS:
        imagebutton:
            idle MG5_DEST_IDLE[dest_id]
            hover MG5_DEST_HOVER[dest_id]
            focus_mask True
            action [Play("sound", "audio/sfx_click.ogg"), Return(dest_id)]
            hovered Function(mg5_sfx, "hover")

    # Acabou o tempo deste cavalo
    timer MG5_TIME_PER_HORSE action Return("timeout")


# Feedback depois de cada cavalo: carimbo + motivo + botão Próximo
screen minigame5_feedback():

    modal True

    use mg5_scene

    add (MG5_STAMP_OK if mg5_last_ok else MG5_STAMP_BAD)

    text "[mg5_last_reason!t]":
        pos MG5_REASON_POS
        size 28
        xmaximum MG5_REASON_W
        color ("#b9f5b9" if mg5_last_ok else "#ffb3b3")

    imagebutton:
        idle MG5_NEXT_IDLE
        hover MG5_NEXT_HOVER
        focus_mask True
        action [Play("sound", "audio/sfx_click.ogg"), Return(True)]
        hovered Function(mg5_sfx, "hover")


# Resultado final
screen minigame5_result():

    modal True

    $ verdict = mg5_verdict()

    add MG5_BG

    button:
        xfill True
        yfill True
        background "#000000aa"
        action NullAction()

    add MG5_RESULT_PANEL

    text _("Pontuação: [mg5_score] / [MG5_MAX_SCORE]"):
        pos MG5_RESULT_SCORE_POS
        anchor (0.5, 0.5)
        size 40
        color "#ffffff"

    text "[verdict!t]":
        pos MG5_RESULT_VERDICT_POS
        anchor (0.5, 0.0)
        text_align 0.5
        size 28
        color "#ffffff"
        xmaximum 880

    imagebutton:
        idle MG5_CONTINUE_IDLE
        hover MG5_CONTINUE_HOVER
        focus_mask True
        action [Play("sound", "audio/sfx_click.ogg"), Return(True)]
        hovered Function(mg5_sfx, "hover")


## -----------------------------------------------------------------------
## 3) LABEL DO GAMEPLAY (motor do minigame em si)
## -----------------------------------------------------------------------
label minigame_5_gameplay:

    $ quick_menu = False       # esconde os botões rápidos do rodapé durante o minigame
    $ renpy.block_rollback()   # impede que o rollback (roda do mouse) bagunce o estado
    $ mg5_reset()              # sorteia os casos (permite rejogar do zero)

    scene black

    # Um cavalo por vez: decisão (com tempo) -> feedback
    while mg5_index < MG5_TOTAL:
        call screen minigame5_horse
        $ mg5_resolve(_return)
        call screen minigame5_feedback
        $ mg5_index += 1

    call screen minigame5_result   # só retorna quando o jogador clica em "Continuar"

    $ quick_menu = True
    return


## -----------------------------------------------------------------------
## 4) PONTO DE ENTRADA (chamado pelo roadmap.rpy: "call expression 'minigame_5_entry'")
##    Mostra as instruções, roda o gameplay e avisa o mapa que terminou.
## -----------------------------------------------------------------------
label minigame_5_entry:

    call screen minigame5_instructions
    call minigame_5_gameplay

    $ mg_report_score(5, mg5_score, MG5_MAX_SCORE)  # registra o placar e a medalha, se for o caso
    $ mg_complete(5)                                 # marca como concluído e libera o 6

    return
