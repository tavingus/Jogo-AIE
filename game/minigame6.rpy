################################################################################
# MINIGAME6.RPY
# Minigame 6: "Transmissão por vetores" — clicar nas moscas hematófagas
#
# Como funciona:
#   - O cavalo fica parado no centro da tela (parte do fundo).
#   - As moscas aparecem UMA de cada vez, voando de fora da tela (de uma
#     borda aleatória) até um ponto de pouso perto do cavalo. Lá, ficam
#     PARADAS por um tempo e então somem sozinhas.
#   - Cada mosca tem uma "atitude certa": as HEMATÓFAGAS precisam ser
#     CLICADAS (a diferença visual entre elas é feita na própria arte, sem
#     texto); as SEM RISCO precisam ser IGNORADAS.
#   - Fazer a coisa certa (clicar na hematófaga, ou deixar a sem risco sumir
#     sozinha): +pontos. Fazer a coisa errada (deixar a hematófaga picar sem
#     clicar, ou clicar numa sem risco à toa): -pontos (nunca passa de 0).
#   - Acaba depois que um número fixo de moscas já apareceu.
#
# Pontuação (ver roadmap.rpy para o sistema de medalhas):
#   Tirar a pontuação máxima = acertar TODAS as moscas certas e nunca clicar
#   numa errada. "mg_report_score(6, pontos, MG6_MAX_SCORE)" registra o
#   placar e concede a medalha automaticamente quando for o caso.
#
# Este arquivo contém: dados/configuração, lógica, tela de instruções, tela
# do gameplay e o "label minigame_6_entry" — chamado pelo roadmap.rpy.
################################################################################


## -----------------------------------------------------------------------
## 1) CONFIGURAÇÃO, DADOS E ARTE
## -----------------------------------------------------------------------
init python:

    MG6_ART_DIR = "images/minigame6/"
    MG6_ZOOM = 2.0  # mesmo esquema de pixel art do resto do jogo

    def mg6_art(filename, size, label, color):
        """Imagem real (ampliada 2x, nearest neighbor) se o arquivo existir,
        senão um retângulo colorido com texto no tamanho final indicado."""
        path = MG6_ART_DIR + filename
        if renpy.loadable(path):
            return Transform(Image(path, nearest_neighbor=True), zoom=MG6_ZOOM)
        return Fixed(
            Solid(color, xysize=size),
            Text(label, size=24, color="#ffffff", xalign=0.5, yalign=0.5,
                 text_align=0.5, xmaximum=size[0] - 16),
            xysize=size,
        )

    # IMAGEM: minigame6/mg6_bg.png — fundo cheio (cenário + cavalo já desenhado
    # no centro). Tamanho final: 1920x1080 → exporte o PNG a 960x540.
    MG6_BG = mg6_art("mg6_bg.png", (1920, 1080), "FUNDO: cavalo no centro\n(mg6_bg.png)", "#3a4a2a")

    # Tamanho de exibição de cada mosca. Tamanho final: 140x140 → exporte
    # cada PNG a 70x70.
    MG6_FLY_SIZE = (140, 140)

    # IMAGEM: minigame6/fly_correct_1.png, fly_correct_2.png — moscas
    # HEMATÓFAGAS (as que pontuam ao clicar). Use 2+ variações visuais.
    MG6_CORRECT_FILES = ["fly_correct_1.png", "fly_correct_2.png"]

    # IMAGEM: minigame6/fly_wrong_1.png, fly_wrong_2.png — moscas SEM risco
    # (clicar nelas penaliza). A diferença visual das hematófagas deve estar
    # na própria arte (cor, formato etc.), sem nenhum texto desenhado pelo jogo.
    MG6_WRONG_FILES = ["fly_wrong_1.png", "fly_wrong_2.png"]

    def mg6_fly_colors(ftype):
        return "#8a2c2c" if ftype == "correct" else "#4a4a4a"

    def mg6_fly_art(ftype, filename):
        label = "MOSCA %s\n(%s)" % ("CORRETA" if ftype == "correct" else "ERRADA", filename)
        return mg6_art(filename, MG6_FLY_SIZE, label, mg6_fly_colors(ftype))

    # Área (x_min, y_min, x_max, y_max) onde as moscas pousam, perto do
    # cavalo — ajuste para cobrir a região certa na sua arte de fundo.
    # (elas começam fora da tela e voam até um ponto sorteado aqui dentro)
    MG6_SPAWN_AREA = (520, 260, 1400, 820)

    # ---- Regras da partida ------------------------------------------------
    MG6_TOTAL_FLIES = 12         # quantas moscas aparecem, ao todo, numa partida
    MG6_CORRECT_COUNT = 8        # quantas dessas são hematófagas (o resto, "erradas")
    MG6_FLY_TRAVEL_TIME = 1.0    # segundos voando da borda até o ponto de pouso
    MG6_FLY_LANDED_TIME = 2.0    # segundos PARADA no pouso antes de sumir sozinha
    # tempo total que a mosca fica na tela (voando + pousada), usado pelo timer:
    MG6_FLY_TOTAL_TIME = MG6_FLY_TRAVEL_TIME + MG6_FLY_LANDED_TIME
    MG6_END_DELAY = 2.0          # segundos mostrando o placar final antes de voltar ao mapa

    # A "atitude certa" para cada mosca:
    #   - hematófaga (correct): tem que CLICAR nela. Clicar = acerto. Deixar
    #     sumir sozinha (ela "pousou e picou" sem ser notada) = erro.
    #   - sem risco (wrong): tem que IGNORAR. Deixar sumir sozinha = acerto.
    #     Clicar nela (sem necessidade) = erro.
    # Ou seja: toda mosca rende pontos ou desconta, dependendo só de você ter
    # feito a coisa certa com ela — clicando ou não clicando.
    MG6_POINTS_CORRECT = 10  # pontos por ter feito a atitude certa com a mosca
    MG6_POINTS_WRONG = -5    # pontos por ter feito a atitude errada (placar nunca < 0)

    # Pontuação máxima possível: acertar a atitude certa nas 12 moscas.
    MG6_MAX_SCORE = MG6_TOTAL_FLIES * MG6_POINTS_CORRECT

    # ---- Efeitos sonoros (tocam só se o arquivo existir) ------------------
    def mg6_sfx(kind):
        # AUDIO: audio/sfx_hover.ogg, audio/sfx_click.ogg (já usados em outras telas)
        # AUDIO: audio/sfx_correct.ogg, audio/sfx_wrong.ogg (opcionais, específicos deste minigame)
        files = {
            "hover": "audio/sfx_hover.ogg",
            "click": "audio/sfx_click.ogg",
            "correct": "audio/sfx_correct.ogg",
            "wrong": "audio/sfx_wrong.ogg",
        }
        path = files.get(kind)
        if path and renpy.loadable(path):
            renpy.sound.play(path)


## Estado da partida (guardado no save / rollback)
default mg6_flies_sequence = []  # ordem embaralhada ("correct"/"wrong") desta partida
default mg6_fly_index = 0        # quantas moscas já apareceram (inclui a atual)
default mg6_score = 0            # pontuação atual
default mg6_current_fly = None   # dict da mosca na tela agora: type/file/posições


init python:

    def mg6_offscreen_point(margin=220):
        """Um ponto fora da tela (1920x1080), numa borda aleatória — de onde
        a mosca começa a voar até o ponto de pouso perto do cavalo."""
        edge = renpy.random.choice(["left", "right", "top", "bottom"])
        if edge == "left":
            return (-margin, renpy.random.randint(0, 1080))
        elif edge == "right":
            return (1920 + margin, renpy.random.randint(0, 1080))
        elif edge == "top":
            return (renpy.random.randint(0, 1920), -margin)
        else:
            return (renpy.random.randint(0, 1920), 1080 + margin)

    def mg6_reset():
        """Prepara uma nova partida: embaralha a ordem das moscas."""
        seq = (["correct"] * MG6_CORRECT_COUNT) + (["wrong"] * (MG6_TOTAL_FLIES - MG6_CORRECT_COUNT))
        renpy.random.shuffle(seq)

        store.mg6_flies_sequence = seq
        store.mg6_fly_index = 0
        store.mg6_score = 0
        store.mg6_current_fly = None

    def mg6_next_fly():
        """Prepara a próxima mosca da lista, em posição aleatória. Devolve
        False quando não há mais moscas (fim da partida)."""
        if store.mg6_fly_index >= len(store.mg6_flies_sequence):
            store.mg6_current_fly = None
            return False

        ftype = store.mg6_flies_sequence[store.mg6_fly_index]
        store.mg6_fly_index += 1

        # Ponto de pouso (perto do cavalo) — onde a mosca fica parada e clicável
        # depois de chegar.
        x_min, y_min, x_max, y_max = MG6_SPAWN_AREA
        target_x = renpy.random.randint(x_min, max(x_min, x_max - MG6_FLY_SIZE[0]))
        target_y = renpy.random.randint(y_min, max(y_min, y_max - MG6_FLY_SIZE[1]))

        # Ponto de partida, fora da tela, numa borda aleatória.
        start_x, start_y = mg6_offscreen_point()

        art_file = renpy.random.choice(MG6_CORRECT_FILES if ftype == "correct" else MG6_WRONG_FILES)

        store.mg6_current_fly = {
            "type": ftype,
            "file": art_file,
            "start_x": start_x,
            "start_y": start_y,
            "target_x": target_x,
            "target_y": target_y,
        }
        return True

    def mg6_resolve_fly(result):
        """Aplica a pontuação da mosca atual e toca o som correspondente.
        result = "clicked" (o jogador clicou) ou "expired" (sumiu sozinha).
          - Hematófaga clicada = acerto. Não clicada (picou o cavalo) = erro.
          - Sem risco ignorada (sumiu sozinha) = acerto. Clicada = erro."""
        if store.mg6_current_fly["type"] == "correct":
            acted_correctly = (result == "clicked")
        else:
            acted_correctly = (result == "expired")

        if acted_correctly:
            store.mg6_score += MG6_POINTS_CORRECT
            mg6_sfx("correct")
        else:
            store.mg6_score = max(0, store.mg6_score + MG6_POINTS_WRONG)
            mg6_sfx("wrong")


## -----------------------------------------------------------------------
## 2) TELA DE INSTRUÇÕES
##    Uso: call screen minigame6_instructions
## -----------------------------------------------------------------------
init python:

    # IMAGEM: minigame6/mg6_instructions_bg.png — fundo cheio das instruções.
    # Tamanho final: 1920x1080 → exporte o PNG a 960x540.
    MG6_INSTR_BG = mg6_art("mg6_instructions_bg.png", (1920, 1080),
                            "FUNDO: instruções\n(mg6_instructions_bg.png)", "#2a2418")

    # IMAGEM: minigame6/mg6_instructions_panel.png — moldura do texto de regras.
    # Tamanho final: 1200x600 → exporte o PNG a 600x300.
    MG6_INSTR_PANEL = mg6_art("mg6_instructions_panel.png", (1200, 600),
                               "MOLDURA DE TEXTO\n(mg6_instructions_panel.png)", "#4a3a20")

style mg6_instructions_text:
    xalign 0.5
    yalign 0.5
    text_align 0.5
    color "#ffffff"
    size 30
    xsize 1000


screen minigame6_instructions():

    modal True

    add MG6_INSTR_BG

    fixed:
        xalign 0.5
        yalign 0.45
        xysize (1200, 600)
        add MG6_INSTR_PANEL

        # Texto de regras de exemplo — edite como quiser
        text _("Moscas estão atacando o cavalo!\n\nClique apenas nas moscas hematófagas (que podem transmitir doenças). Clicar na mosca certa marca pontos; clicar na errada tira pontos.\n\nFique atento: elas somem rápido!") style "mg6_instructions_text" xalign 0.5 yalign 0.5

    # Botão "Entendi" / "Fechar". Tamanho final: 240x80 → exporte a 120x40.
    imagebutton:
        xalign 0.5
        yalign 0.85
        idle mg6_art("mg6_close_idle.png", (240, 80), "ENTENDI\n(mg6_close_idle.png)", "#3a5a3a")
        hover mg6_art("mg6_close_hover.png", (240, 80), "ENTENDI\n(mg6_close_hover.png)", "#4f7a4f")
        focus_mask True
        action [Play("sound", "audio/sfx_click.ogg"), Return(True)]
        hovered Play("sound", "audio/sfx_hover.ogg")


## -----------------------------------------------------------------------
## 2.5) MOVIMENTO DA MOSCA (de fora da tela até o ponto de pouso)
## -----------------------------------------------------------------------

transform mg6_fly_move(start_x, start_y, target_x, target_y, duration):
    pos (start_x, start_y)
    linear duration pos (target_x, target_y)


## -----------------------------------------------------------------------
## 3) TELAS DO GAMEPLAY
##    Cada mosca é uma chamada própria de "call screen minigame6_fly". O prazo
##    dela é o timer DESTA tela: como a tela é recriada a cada mosca, o timer
##    sempre começa do zero e dispara sozinho. (Antes, um timer único e fixo
##    dentro da mesma tela acabava cacheado pelo Ren'Py e a mosca só sumia ao
##    clicar.)
## -----------------------------------------------------------------------

# HUD: pontuação atual e progresso (quantas moscas já passaram)
screen minigame6_hud():

    text _("Pontos: [mg6_score]"):
        xpos 60
        ypos 40
        size 36
        color "#ffffff"

    text "[mg6_fly_index]/[MG6_TOTAL_FLIES]":
        xalign 0.97
        ypos 40
        size 30
        color "#ffffff"


# Uma mosca. Retorna "clicked" se o jogador clicou, ou "expired" quando o
# tempo dela (voo + pousada) acaba.
screen minigame6_fly():

    modal True

    add MG6_BG

    use minigame6_hud

    $ fly = mg6_current_fly

    button:
        # A animação dura só o tempo de VOO — ao terminar, a mosca fica
        # parada no ponto de pouso (comportamento padrão do ATL: sem mais
        # instruções, ele simplesmente mantém a última posição).
        at mg6_fly_move(fly["start_x"], fly["start_y"], fly["target_x"], fly["target_y"], MG6_FLY_TRAVEL_TIME)
        xysize MG6_FLY_SIZE
        background None
        focus_mask True  # só pixels coloridos da mosca respondem ao clique
        action Return("clicked")
        add mg6_fly_art(fly["type"], fly["file"])

    timer MG6_FLY_TOTAL_TIME action Return("expired")


# Fim de partida: mostra o placar final e volta ao mapa sozinho
screen minigame6_end():

    modal True

    add MG6_BG

    use minigame6_hud

    button:
        xfill True
        yfill True
        background "#000000aa"
        action NullAction()

    vbox:
        xalign 0.5
        yalign 0.5
        spacing 20

        text _("Fim de partida!"):
            xalign 0.5
            size 48
            color "#ffffff"

        text "[_('Pontuação final')]: [mg6_score] / [MG6_MAX_SCORE]":
            xalign 0.5
            size 36
            color "#ffffff"

    timer MG6_END_DELAY action Return(True)


## -----------------------------------------------------------------------
## 4) LABELS: GAMEPLAY E PONTO DE ENTRADA
## -----------------------------------------------------------------------
label minigame_6_gameplay:

    $ quick_menu = False
    $ renpy.block_rollback()
    $ mg6_reset()

    scene black

    # Uma mosca por vez, até acabarem
    while mg6_next_fly():
        call screen minigame6_fly
        $ mg6_resolve_fly(_return)

    call screen minigame6_end   # placar final; volta sozinho após MG6_END_DELAY

    $ quick_menu = True
    return


label minigame_6_entry:

    call screen minigame6_instructions
    call minigame_6_gameplay

    $ mg_report_score(6, mg6_score, MG6_MAX_SCORE)  # registra o placar e a medalha, se for o caso
    $ mg_complete(6)                                 # marca como concluído e libera o próximo

    return
