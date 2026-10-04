################################################################################
# MINIGAME7.RPY
# Minigame 7: "Impedir a reutilização de agulha" (contaminação iatrogênica)
#
# Como funciona:
#   - Um tratador vai aplicar injeções no cavalo, UMA tentativa de cada vez
#     (MG7_ATTEMPTS tentativas). Em algumas ele usa uma agulha NOVA; em outras
#     tenta REUTILIZAR uma agulha já usada (com sangue) — o que poderia
#     transmitir a AIE de um cavalo para outro.
#   - Cada tentativa tem 2 momentos:
#       1) O tratador CHEGA com a seringa, e a agulha ainda não dá para ver.
#          Clicar no cavalo agora é cedo demais (hora errada).
#       2) A agulha aparece (nova ou usada) e o tratador se aproxima para
#          picar. O jogador tem uma JANELA DE TEMPO curta (que diminui a cada
#          tentativa) antes da picada.
#   - O jogador clica no cavalo para TIRÁ-LO DO LUGAR. O cavalo faz uma
#     EXPRESSÃO BRAVA, mostrando que não aceita a reutilização de agulhas.
#
#   Resultado de cada tentativa:
#     - agulha USADA + clicou na janela ........ EVITOU a contaminação (+pontos)
#     - agulha USADA + não clicou .............. PICADA contaminada (-pontos)
#     - agulha NOVA + não clicou ............... aplicação segura (+pontos)
#     - agulha NOVA + clicou ................... hora errada: o cavalo não
#                                                 precisava recusar (-pontos)
#     - clicou ANTES de ver a agulha ........... hora errada (-pontos)
#
# Pontuação (ver roadmap.rpy para o sistema de medalhas):
#   Além dos pontos de cada tentativa, terminar SEM NENHUMA PICADA contaminada
#   dá um BÔNUS (MG7_BONUS_NO_PRICK). O placar nunca fica abaixo de 0.
#   Pontuação máxima = todas as tentativas certas + bônus.
#
# ARTE (mesmo esquema do menu, roadmap e minigames 2 a 5):
#   TODA arte real é um PNG de CANVAS INTEIRO (960x540), com o elemento já na
#   posição certa. O jogo amplia 2x (nearest neighbor) e desenha em (0, 0), sem
#   usar posição do código; focus_mask True faz só os pixels opacos do cavalo
#   responderem ao clique.
#   O tratador "entra" e "avança" deslocando o PNG inteiro na horizontal (por
#   isso as artes do tratador devem ter fundo transparente e ficar na posição
#   FINAL, de aplicação, dentro do canvas).
#   Enquanto o PNG não existe, aparece um placeholder colorido com texto, na
#   posição das constantes MG7_*_RECT abaixo (só servem aos placeholders).
#
# Este arquivo contém: dados/configuração, lógica, tela de instruções, telas
# do gameplay e o "label minigame_7_entry" — chamado pelo roadmap.rpy.
################################################################################


## -----------------------------------------------------------------------
## 1) CONFIGURAÇÃO, DADOS E LÓGICA
## -----------------------------------------------------------------------
init python:

    MG7_ART_DIR = "images/minigame7/"
    MG7_ZOOM = 2.0  # arte a 960x540, exibida em 1920x1080

    # ---- Posições dos PLACEHOLDERS (tela 1920x1080): (x, y, largura, altura)
    MG7_TITLE_RECT = (60, 30, 760, 100)
    MG7_HORSE_RECT = (360, 300, 600, 640)             # cavalo (à esquerda do centro)
    MG7_HANDLER_RECT = (1020, 300, 520, 640)          # tratador (posição FINAL)
    MG7_STAMP_RECT = (560, 130, 800, 140)             # carimbo certo/errado
    MG7_RESULT_RECT = (460, 330, 1000, 420)
    MG7_CONTINUE_RECT = (750, 800, 420, 90)
    MG7_INSTR_PANEL_RECT = (360, 190, 1200, 600)
    MG7_CLOSE_RECT = (840, 860, 240, 80)

    # Textos escritos pelo jogo (mudam durante a partida)
    MG7_ATTEMPT_POS = (1500, 40)                      # "Tentativa n/N"
    MG7_SCORE_POS = (1500, 90)                        # "Pontos: N"
    MG7_PRICKS_POS = (1500, 140)                      # "Picadas: N"
    MG7_REASON_POS = (60, 960)                        # motivo (tela de resultado da tentativa)
    MG7_REASON_W = 1800
    MG7_RESULT_SCORE_POS = (960, 450)                 # "Pontuação: N / M" (centralizado)
    MG7_RESULT_BONUS_POS = (960, 520)                 # linha do bônus (centralizada)
    MG7_RESULT_VERDICT_POS = (960, 590)               # frase final (centralizada)

    # ---- Regras ------------------------------------------------------------
    MG7_REUSED_COUNT = 5              # tentativas com agulha USADA
    MG7_NEW_COUNT = 3                 # tentativas com agulha NOVA
    MG7_ATTEMPTS = MG7_REUSED_COUNT + MG7_NEW_COUNT

    MG7_ARRIVE_TIME = 1.2             # s do tratador chegando (agulha ainda oculta)
    MG7_WINDOW_FIRST = 1.8            # s de janela na 1ª tentativa
    MG7_WINDOW_LAST = 1.0             # s de janela na última (fica mais rápido)
    MG7_SLIDE_FROM = 700              # px: de onde o tratador entra (à direita)
    MG7_LUNGE = 60                    # px: quanto ele avança até a picada
    MG7_OUTCOME_TIME = 2.2            # s mostrando o resultado de cada tentativa

    MG7_POINTS_DODGE = 10             # agulha usada evitada
    MG7_POINTS_SAFE = 5               # agulha nova aceita
    MG7_PENALTY_WRONG = 5             # clique na hora errada
    MG7_PENALTY_PRICK = 10            # picada com agulha usada
    MG7_BONUS_NO_PRICK = 20           # terminar sem nenhuma picada contaminada

    # Pontuação máxima: tudo certo + bônus
    MG7_MAX_SCORE = (MG7_REUSED_COUNT * MG7_POINTS_DODGE
                     + MG7_NEW_COUNT * MG7_POINTS_SAFE
                     + MG7_BONUS_NO_PRICK)

    def mg7_window_for(i):
        """Janela de reação (s) da tentativa i (0-based): encurta aos poucos."""
        if MG7_ATTEMPTS <= 1:
            return MG7_WINDOW_FIRST
        t = float(i) / (MG7_ATTEMPTS - 1)
        return MG7_WINDOW_FIRST + (MG7_WINDOW_LAST - MG7_WINDOW_FIRST) * t

    # ---- Placeholders de arte ----------------------------------------------
    def mg7_art(filename, rect, label, color, fill=True):
        """Arte de canvas inteiro (960x540 → 1920x1080, nearest neighbor,
        desenhada em (0, 0)) se o PNG existir. Senão, um placeholder: retângulo
        colorido com texto na posição "rect" = (x, y, largura, altura).
        fill=False = só o texto, sem retângulo."""
        path = MG7_ART_DIR + filename
        if renpy.loadable(path):
            return Transform(Image(path, nearest_neighbor=True), zoom=MG7_ZOOM)

        x, y, w, h = rect
        text = Text(label, size=26, color="#ffffff", xalign=0.5, yalign=0.5,
                    text_align=0.5, xmaximum=w - 20)
        if fill:
            box = Fixed(Solid(color, xysize=(w, h)), text, xysize=(w, h))
        else:
            box = Fixed(text, xysize=(w, h))
        return Fixed(Transform(box, pos=(x, y)), xysize=(1920, 1080))

    # IMAGEM: minigame7/mg7_bg.png — fundo cheio: área de atendimento / baia.
    # Canvas 960x540.
    MG7_BG = mg7_art("mg7_bg.png", (0, 0, 1920, 1080), "FUNDO: área de atendimento\n(mg7_bg.png)", "#4a5a3a")

    # IMAGEM: minigame7/mg7_titulo.png — painel de título ("7 - AGULHA NOVA
    # SEMPRE", com o texto desenhado). Canvas 960x540.
    MG7_TITLE_PANEL = mg7_art("mg7_titulo.png", MG7_TITLE_RECT, "7 - IMPEDIR REUTILIZAÇÃO DE AGULHA\n(mg7_titulo.png)", "#4a3a20")

    # IMAGEM: minigame7/cavalo_calmo.png, cavalo_bravo.png e cavalo_picado.png —
    # o cavalo (canvas 960x540, na posição dele, fundo transparente):
    #   calmo  = normal (também usado quando a agulha é nova e aceita)
    #   bravo  = EXPRESSÃO BRAVA ao ser clicado (recusando a agulha)
    #   picado = reação à picada com agulha usada
    # O cavalo calmo é o BOTÃO clicável (focus_mask: só os pixels dele).
    MG7_HORSE_ART = {
        "calmo": mg7_art("cavalo_calmo.png", MG7_HORSE_RECT, "CAVALO CALMO\n(cavalo_calmo.png)", "#7a5a3a"),
        "bravo": mg7_art("cavalo_bravo.png", MG7_HORSE_RECT, "CAVALO BRAVO!\n(cavalo_bravo.png)", "#a03a2a"),
        "picado": mg7_art("cavalo_picado.png", MG7_HORSE_RECT, "CAVALO PICADO\n(cavalo_picado.png)", "#6a2a2a"),
    }

    # IMAGEM: minigame7/tratador_<estado>.png — o tratador (canvas 960x540,
    # fundo transparente, na posição FINAL de aplicação, ao lado do cavalo).
    # O jogo o desloca para entrar em cena e avançar. Estados:
    #   chegando  = chegando com a seringa, agulha escondida / não dá para ver
    #   nova      = agulha NOVA visível (ex.: embalagem aberta, brilhando)
    #   usada     = agulha USADA visível (ex.: com sangue, torta, tampa suja)
    #   recuo     = recuando assustado (cavalo recusou)
    #   aplicando = aplicando a injeção com agulha nova (tudo certo)
    #   picou     = agulha usada espetou o cavalo (contaminação!)
    MG7_HANDLER_ART = dict(
        (state, mg7_art("tratador_%s.png" % state, MG7_HANDLER_RECT,
                        "TRATADOR: %s\n(tratador_%s.png)" % (state.upper(), state), color))
        for state, color in (
            ("chegando", "#3a5a8a"), ("nova", "#2e7d32"), ("usada", "#8a2c2c"),
            ("recuo", "#5a5a5a"), ("aplicando", "#2c6e8a"), ("picou", "#6a1a1a"),
        )
    )

    # IMAGEM: minigame7/mg7_certo.png e mg7_errado.png — carimbo/aviso da tela
    # de resultado de cada tentativa (ex.: "BOA!" verde / "OPS!" vermelho).
    # Canvas 960x540, fundo transparente.
    MG7_STAMP_OK = mg7_art("mg7_certo.png", MG7_STAMP_RECT, "BOA!\n(mg7_certo.png)", "#2e7d32")
    MG7_STAMP_BAD = mg7_art("mg7_errado.png", MG7_STAMP_RECT, "OPS!\n(mg7_errado.png)", "#8a2c2c")

    # IMAGEM: minigame7/mg7_resultado.png — painel do resultado final, com o
    # texto fixo desenhado; o jogo escreve a pontuação, o bônus e a frase final
    # em MG7_RESULT_SCORE_POS, MG7_RESULT_BONUS_POS e MG7_RESULT_VERDICT_POS.
    # Canvas 960x540.
    MG7_RESULT_PANEL = mg7_art("mg7_resultado.png", MG7_RESULT_RECT, "ATIVIDADE CONCLUÍDA!\n(mg7_resultado.png)", "#2e5a3a")

    # IMAGEM: minigame7/mg7_continuar_idle.png e mg7_continuar_hover.png —
    # botão "Continuar" do resultado (texto desenhado). Canvas 960x540.
    MG7_CONTINUE_IDLE = mg7_art("mg7_continuar_idle.png", MG7_CONTINUE_RECT, "CONTINUAR\n(mg7_continuar_idle.png)", "#3a5a3a")
    MG7_CONTINUE_HOVER = mg7_art("mg7_continuar_hover.png", MG7_CONTINUE_RECT, "CONTINUAR\n(mg7_continuar_hover.png)", "#4f7a4f")

    # ---- Efeitos sonoros (só tocam se o arquivo existir) -------------------
    def mg7_sfx(kind):
        # AUDIO: audio/sfx_horse_angry.ogg — relincho bravo (opcional)
        files = {
            "hover": "audio/sfx_hover.ogg",
            "click": "audio/sfx_click.ogg",
            "correct": "audio/sfx_correct.ogg",
            "wrong": "audio/sfx_wrong.ogg",
            "angry": "audio/sfx_horse_angry.ogg",
        }
        path = files.get(kind)
        if path and renpy.loadable(path):
            renpy.sound.play(path)


## Estado do minigame (guardado no save / rollback)
default mg7_seq = []          # agulha de cada tentativa: "reused" / "new"
default mg7_index = 0         # tentativa atual (0-based)
default mg7_score = 0
default mg7_pricks = 0        # picadas contaminadas sofridas
default mg7_bonus = 0         # bônus de "sem picadas" (calculado no fim)
default mg7_window = 1.5      # janela de reação da tentativa atual (s)
default mg7_outcome = ""      # resultado da tentativa: dodge/prick/safe/unneeded/early
default mg7_reason = ""       # motivo do resultado


init python:

    def mg7_reset():
        """Nova partida: sorteia a ordem das agulhas e zera o estado."""
        seq = ["reused"] * MG7_REUSED_COUNT + ["new"] * MG7_NEW_COUNT
        renpy.random.shuffle(seq)
        store.mg7_seq = seq
        store.mg7_index = 0
        store.mg7_score = 0
        store.mg7_pricks = 0
        store.mg7_bonus = 0
        store.mg7_window = MG7_WINDOW_FIRST
        store.mg7_outcome = ""
        store.mg7_reason = ""

    def mg7_start_attempt():
        """Prepara a tentativa atual (janela de reação desta rodada)."""
        store.mg7_window = mg7_window_for(store.mg7_index)
        store.mg7_outcome = ""
        store.mg7_reason = ""

    def mg7_needle():
        return store.mg7_seq[store.mg7_index]

    def mg7_add(points):
        store.mg7_score = max(0, store.mg7_score + points)

    def mg7_resolve(action):
        """Aplica o resultado da tentativa. action:
          "early" = clicou no cavalo antes de a agulha aparecer
          "dodge" = clicou no cavalo durante a janela de reação
          "prick" = a janela acabou sem clique."""
        needle = mg7_needle()

        if action == "early":
            outcome = "early"
            mg7_add(-MG7_PENALTY_WRONG)
            reason = _("Cedo demais! Você tirou o cavalo antes de ver a agulha. Espere a agulha aparecer para saber se ela é nova ou usada.")
        elif action == "dodge" and needle == "reused":
            outcome = "dodge"
            mg7_add(MG7_POINTS_DODGE)
            reason = _("Boa! Aquela agulha já tinha sido usada. Reutilizar agulha pode passar o vírus da AIE de um cavalo para outro: contaminação iatrogênica.")
        elif action == "dodge":
            outcome = "unneeded"
            mg7_add(-MG7_PENALTY_WRONG)
            reason = _("Hora errada! A agulha era NOVA e a aplicação era segura. Recuse só quando a agulha for reutilizada.")
        elif needle == "reused":
            outcome = "prick"
            store.mg7_pricks += 1
            mg7_add(-MG7_PENALTY_PRICK)
            reason = _("Picada! A agulha usada espetou o cavalo: risco de contaminação iatrogênica pela reutilização de agulha.")
        else:
            outcome = "safe"
            mg7_add(MG7_POINTS_SAFE)
            reason = _("Aplicação segura: agulha nova, sem risco de transmitir o vírus. Agulha nova e descartável para cada animal.")

        store.mg7_outcome = outcome
        store.mg7_reason = reason
        # Cavalo brabo relincha (se o áudio existir); senão toca o som de acerto/erro
        if outcome in ("dodge", "unneeded", "early") and renpy.loadable("audio/sfx_horse_angry.ogg"):
            mg7_sfx("angry")
        else:
            mg7_sfx("correct" if outcome in ("dodge", "safe") else "wrong")

    def mg7_ok():
        return store.mg7_outcome in ("dodge", "safe")

    def mg7_horse_state():
        """Pose do cavalo na tela de resultado da tentativa."""
        if store.mg7_outcome in ("dodge", "unneeded", "early"):
            return "bravo"
        if store.mg7_outcome == "prick":
            return "picado"
        return "calmo"

    def mg7_handler_state():
        """Pose do tratador na tela de resultado da tentativa."""
        return {"dodge": "recuo", "unneeded": "recuo", "early": "recuo",
                "prick": "picou", "safe": "aplicando"}.get(store.mg7_outcome, "chegando")

    def mg7_finish():
        """Fim da partida: concede o bônus de "sem picadas"."""
        if store.mg7_pricks == 0:
            store.mg7_bonus = MG7_BONUS_NO_PRICK
            store.mg7_score += MG7_BONUS_NO_PRICK

    def mg7_verdict():
        """Frase final conforme o desempenho."""
        if store.mg7_pricks == 0 and store.mg7_score >= MG7_MAX_SCORE:
            return _("Perfeito! Nenhuma agulha foi reutilizada e o cavalo ficou protegido.")
        elif store.mg7_pricks == 0:
            return _("Nenhuma picada contaminada! Mas ainda dá para acertar mais o momento de reagir.")
        else:
            return _("Houve picadas com agulha usada. Lembre: agulha nova e descartável para cada animal.")


## -----------------------------------------------------------------------
## 1.5) TELA DE INSTRUÇÕES
##    Uso: call screen minigame7_instructions
##    Modal: bloqueia qualquer clique no que estiver atrás até "Entendi".
## -----------------------------------------------------------------------
init python:

    # IMAGEM: minigame7/mg7_instructions_bg.png — fundo cheio. Canvas 960x540.
    MG7_INSTR_BG = mg7_art("mg7_instructions_bg.png", (0, 0, 1920, 1080),
                           "FUNDO: instruções\n(mg7_instructions_bg.png)", "#2a2418")

    # IMAGEM: minigame7/mg7_instructions_panel.png — moldura do texto de regras,
    # sem texto (o texto é escrito pelo jogo, centralizado em (960, 490), com
    # até 1000 px de largura). Canvas 960x540.
    MG7_INSTR_PANEL = mg7_art("mg7_instructions_panel.png", MG7_INSTR_PANEL_RECT,
                              "MOLDURA DE TEXTO\n(mg7_instructions_panel.png)", "#4a3a20")

    # IMAGEM: minigame7/mg7_close_idle.png e mg7_close_hover.png — botão
    # "Entendi" (texto desenhado). Canvas 960x540.
    MG7_CLOSE_IDLE = mg7_art("mg7_close_idle.png", MG7_CLOSE_RECT, "ENTENDI\n(mg7_close_idle.png)", "#3a5a3a")
    MG7_CLOSE_HOVER = mg7_art("mg7_close_hover.png", MG7_CLOSE_RECT, "ENTENDI\n(mg7_close_hover.png)", "#4f7a4f")

style mg7_instructions_text:
    text_align 0.5
    color "#ffffff"
    size 28
    xsize 1000


screen minigame7_instructions():

    modal True  # impede qualquer clique/interação com o jogo por trás

    add MG7_INSTR_BG
    add MG7_INSTR_PANEL

    # Texto de regras de exemplo — edite como quiser (os números vêm das constantes)
    $ instr_text = _("Um tratador vai aplicar %d injeções no cavalo, mas às vezes tenta REUTILIZAR uma agulha já usada!\n\nQuando a agulha aparecer, se ela for USADA (suja de sangue), clique no cavalo para tirá-lo do lugar antes da picada. Se a agulha for NOVA, deixe a aplicação acontecer. Não clique antes de ver a agulha!\n\nHora errada tira pontos, e terminar sem nenhuma picada contaminada dá um bônus.") % MG7_ATTEMPTS

    text "[instr_text]" style "mg7_instructions_text" pos (960, 490) anchor (0.5, 0.5)

    imagebutton:
        idle MG7_CLOSE_IDLE
        hover MG7_CLOSE_HOVER
        focus_mask True
        action [
            Play("sound", "audio/sfx_click.ogg"),
            Return(True),  # devolve o controle ao "call screen" que a chamou
        ]
        hovered Play("sound", "audio/sfx_hover.ogg")


## -----------------------------------------------------------------------
## 2) TELAS DO MINIGAME
##    Cada tentativa tem até 3 telas (chegada, decisão e resultado), cada uma
##    com seus próprios timers — assim os timers sempre começam do zero.
## -----------------------------------------------------------------------

# O tratador entra deslizando da direita até a posição final
transform mg7_slide_in(duration, offset):
    xoffset offset
    linear duration xoffset 0

# O tratador avança em direção ao cavalo até o momento da picada
transform mg7_lunge(duration, offset):
    xoffset 0
    linear duration xoffset -offset


# Fundo + título + contadores (comum a todas as telas do jogo)
screen mg7_hud():

    $ attempt_number = min(mg7_index + 1, MG7_ATTEMPTS)

    add MG7_BG
    add MG7_TITLE_PANEL

    text _("Tentativa [attempt_number]/[MG7_ATTEMPTS]"):
        pos MG7_ATTEMPT_POS
        size 32
        color "#ffffff"

    text _("Pontos: [mg7_score]"):
        pos MG7_SCORE_POS
        size 32
        color "#ffffff"

    text _("Picadas: [mg7_pricks]"):
        pos MG7_PRICKS_POS
        size 32
        color ("#ffb3b3" if mg7_pricks > 0 else "#ffffff")


# O cavalo como botão: clicar nele o tira do lugar. focus_mask = só os pixels
# do cavalo respondem. Retorna "dodge" (ou o valor dado em "result").
screen mg7_horse_button(result):

    button:
        xysize (1920, 1080)
        background None
        focus_mask True
        action Return(result)
        add MG7_HORSE_ART["calmo"]


# 1) Chegada: o tratador entra, a agulha ainda não aparece. Clicar = cedo demais.
# Retorna "early" ou "reveal" (o timer acabou).
screen minigame7_approach():

    modal True

    use mg7_hud

    add MG7_HANDLER_ART["chegando"] at mg7_slide_in(MG7_ARRIVE_TIME, MG7_SLIDE_FROM)
    use mg7_horse_button("early")

    timer MG7_ARRIVE_TIME action Return("reveal")


# 2) Decisão: a agulha aparece (nova ou usada) e o tratador se aproxima.
# Retorna "dodge" (clicou no cavalo) ou "prick" (a janela acabou).
screen minigame7_decision():

    modal True

    use mg7_hud

    $ needle_art = "usada" if mg7_needle() == "reused" else "nova"

    add MG7_HANDLER_ART[needle_art] at mg7_lunge(mg7_window, MG7_LUNGE)
    use mg7_horse_button("dodge")

    timer mg7_window action Return("prick")


# 3) Resultado da tentativa: cavalo bravo / picado / calmo + carimbo + motivo.
# Avança sozinho depois de MG7_OUTCOME_TIME s (ou ao clicar em qualquer lugar).
screen minigame7_outcome():

    modal True

    use mg7_hud

    $ handler_key = mg7_handler_state()
    $ horse_key = mg7_horse_state()
    $ outcome_ok = mg7_ok()

    add MG7_HANDLER_ART[handler_key]
    add MG7_HORSE_ART[horse_key]
    add (MG7_STAMP_OK if outcome_ok else MG7_STAMP_BAD)

    text "[mg7_reason!t]":
        pos MG7_REASON_POS
        size 28
        xmaximum MG7_REASON_W
        color ("#b9f5b9" if outcome_ok else "#ffb3b3")

    button:
        xfill True
        yfill True
        background None
        action Return(True)

    timer MG7_OUTCOME_TIME action Return(True)


# Resultado final
screen minigame7_result():

    modal True

    $ verdict = mg7_verdict()
    $ bonus_value = mg7_bonus

    add MG7_BG

    button:
        xfill True
        yfill True
        background "#000000aa"
        action NullAction()

    add MG7_RESULT_PANEL

    text _("Pontuação: [mg7_score] / [MG7_MAX_SCORE]"):
        pos MG7_RESULT_SCORE_POS
        anchor (0.5, 0.5)
        size 40
        color "#ffffff"

    if mg7_bonus > 0:
        text _("Sem picadas: +[bonus_value] pontos de bônus!"):
            pos MG7_RESULT_BONUS_POS
            anchor (0.5, 0.5)
            size 30
            color "#b9f5b9"

    text "[verdict!t]":
        pos MG7_RESULT_VERDICT_POS
        anchor (0.5, 0.0)
        text_align 0.5
        size 28
        color "#ffffff"
        xmaximum 880

    imagebutton:
        idle MG7_CONTINUE_IDLE
        hover MG7_CONTINUE_HOVER
        focus_mask True
        action [Play("sound", "audio/sfx_click.ogg"), Return(True)]
        hovered Function(mg7_sfx, "hover")


## -----------------------------------------------------------------------
## 3) LABEL DO GAMEPLAY (motor do minigame em si)
## -----------------------------------------------------------------------
label minigame_7_gameplay:

    $ quick_menu = False       # esconde os botões rápidos do rodapé durante o minigame
    $ renpy.block_rollback()   # impede que o rollback (roda do mouse) bagunce o estado
    $ mg7_reset()              # sorteia as agulhas (permite rejogar do zero)

    scene black

    # Uma tentativa por vez: chegada -> (decisão) -> resultado
    while mg7_index < MG7_ATTEMPTS:
        $ mg7_start_attempt()

        call screen minigame7_approach
        if _return == "early":
            $ mg7_resolve("early")
        else:
            call screen minigame7_decision
            $ mg7_resolve(_return)

        call screen minigame7_outcome
        $ mg7_index += 1

    $ mg7_finish()             # bônus de "sem picadas", se for o caso
    call screen minigame7_result   # só retorna quando o jogador clica em "Continuar"

    $ quick_menu = True
    return


## -----------------------------------------------------------------------
## 4) PONTO DE ENTRADA (chamado pelo roadmap.rpy: "call expression 'minigame_7_entry'")
##    Mostra as instruções, roda o gameplay e avisa o mapa que terminou.
## -----------------------------------------------------------------------
label minigame_7_entry:

    call screen minigame7_instructions
    call minigame_7_gameplay

    $ mg_report_score(7, mg7_score, MG7_MAX_SCORE)  # registra o placar e a medalha, se for o caso
    $ mg_complete(7)                                 # marca como concluído e libera o 8

    return
