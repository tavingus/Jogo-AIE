################################################################################
# MINIGAME6.RPY
# Moscas atacando o cavalo central. Uma mosca por vez voa até perto do cavalo,
# pousa e fica ali por MG6_FLY_LANDED_TIME segundos.
#
#   - tipo "correct": mosca hematófaga -> o certo é CLICAR nela.
#       clicou = acerto | sumiu sozinha (picou o cavalo) = erro
#   - tipo "wrong": mosca sem risco -> o certo é IGNORAR.
#       sumiu sozinha = acerto | clicou = erro
#
# Cada mosca é mostrada por uma chamada própria de "call screen", e o prazo dela
# é um "timer ... action Return(...)" dessa tela. Como a tela é recriada a cada
# mosca, o timer sempre começa do zero e dispara sozinho (antes, um timer único
# fixo na tela era cacheado pelo Ren'Py e a mosca só sumia ao clicar).
################################################################################


## -----------------------------------------------------------------------
## 1) ARTE
## -----------------------------------------------------------------------
init python:

    MG6_ART_DIR = "images/minigame6/"
    MG6_ZOOM = 2.0  # pixel art exportada a 960x540 -> 1920x1080

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

    MG6_BG = mg6_art("mg6_bg.png", (1920, 1080), "FUNDO: cavalo no centro\n(mg6_bg.png)", "#3a4a2a")

    MG6_FLY_SIZE = (140, 140)

    MG6_CORRECT_FILES = ["fly_correct_1.png", "fly_correct_2.png"]  # hematófagas
    MG6_WRONG_FILES = ["fly_wrong_1.png", "fly_wrong_2.png"]        # sem risco

    def mg6_fly_colors(ftype):
        return "#8a2c2c" if ftype == "correct" else "#4a4a4a"

    def mg6_fly_art(ftype, filename):
        label = "MOSCA %s\n(%s)" % ("CORRETA" if ftype == "correct" else "ERRADA", filename)
        return mg6_art(filename, MG6_FLY_SIZE, label, mg6_fly_colors(ftype))


## -----------------------------------------------------------------------
## 2) REGRAS / BALANCEAMENTO
## -----------------------------------------------------------------------
init python:

    # Área (x_min, y_min, x_max, y_max) onde as moscas pousam, ao redor do cavalo
    MG6_SPAWN_AREA = (520, 260, 1400, 820)

    MG6_TOTAL_FLIES = 12
    MG6_CORRECT_COUNT = 8        # quantas das 12 são hematófagas
    MG6_FLY_TRAVEL_TIME = 1.0    # segundos voando até pousar
    MG6_FLY_LANDED_TIME = 2.0    # segundos pousada até sumir sozinha

    MG6_FLY_TOTAL_TIME = MG6_FLY_TRAVEL_TIME + MG6_FLY_LANDED_TIME
    MG6_END_DELAY = 2.0          # tempo da tela "Fim de partida" antes de sair

    MG6_POINTS_CORRECT = 10
    MG6_POINTS_WRONG = -5

    # Pontuação máxima: todas as moscas tratadas corretamente
    MG6_MAX_SCORE = MG6_TOTAL_FLIES * MG6_POINTS_CORRECT

    def mg6_sfx(kind):
        files = {
            "hover": "audio/sfx_hover.ogg",
            "click": "audio/sfx_click.ogg",
            "correct": "audio/sfx_correct.ogg",
            "wrong": "audio/sfx_wrong.ogg",
        }
        path = files.get(kind)
        if path and renpy.loadable(path):
            renpy.sound.play(path)


## -----------------------------------------------------------------------
## 3) ESTADO DA PARTIDA
## -----------------------------------------------------------------------
default mg6_flies_sequence = []
default mg6_fly_index = 0
default mg6_score = 0
default mg6_current_fly = None


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
        store.mg6_flies_sequence = (["correct"] * MG6_CORRECT_COUNT) + \
                                   (["wrong"] * (MG6_TOTAL_FLIES - MG6_CORRECT_COUNT))
        renpy.random.shuffle(store.mg6_flies_sequence)
        store.mg6_fly_index = 0
        store.mg6_score = 0
        store.mg6_current_fly = None

    def mg6_next_fly():
        """Prepara a próxima mosca da lista (posição aleatória). Devolve
        False quando não há mais moscas."""
        if store.mg6_fly_index >= len(store.mg6_flies_sequence):
            store.mg6_current_fly = None
            return False

        ftype = store.mg6_flies_sequence[store.mg6_fly_index]
        store.mg6_fly_index += 1

        x_min, y_min, x_max, y_max = MG6_SPAWN_AREA
        target_x = renpy.random.randint(x_min, max(x_min, x_max - MG6_FLY_SIZE[0]))
        target_y = renpy.random.randint(y_min, max(y_min, y_max - MG6_FLY_SIZE[1]))
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
        """Aplica a pontuação da mosca atual. result = "clicked" (jogador
        clicou) ou "expired" (sumiu sozinha após MG6_FLY_LANDED_TIME)."""
        ftype = store.mg6_current_fly["type"]
        if ftype == "correct":
            acted_correctly = (result == "clicked")   # hematófaga: tinha que clicar
        else:
            acted_correctly = (result == "expired")   # sem risco: tinha que ignorar

        if acted_correctly:
            store.mg6_score += MG6_POINTS_CORRECT
            mg6_sfx("correct")
        else:
            store.mg6_score = max(0, store.mg6_score + MG6_POINTS_WRONG)
            mg6_sfx("wrong")


## -----------------------------------------------------------------------
## 4) TELA DE INSTRUÇÕES
## -----------------------------------------------------------------------
init python:

    MG6_INSTR_BG = mg6_art("mg6_instructions_bg.png", (1920, 1080),
                           "FUNDO: instruções\n(mg6_instructions_bg.png)", "#2a2418")

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

        text _("Moscas estão atacando o cavalo!\n\nClique apenas nas moscas hematófagas (que podem transmitir doenças). Clicar na mosca certa marca pontos; clicar na errada tira pontos.\n\nFique atento: elas somem rápido!") style "mg6_instructions_text" xalign 0.5 yalign 0.5

    imagebutton:
        xalign 0.5
        yalign 0.85
        idle mg6_art("mg6_close_idle.png", (240, 80), "ENTENDI\n(mg6_close_idle.png)", "#3a5a3a")
        hover mg6_art("mg6_close_hover.png", (240, 80), "ENTENDI\n(mg6_close_hover.png)", "#4f7a4f")
        focus_mask True
        action [Play("sound", "audio/sfx_click.ogg"), Return(True)]
        hovered Play("sound", "audio/sfx_hover.ogg")


## -----------------------------------------------------------------------
## 5) TELAS DO JOGO
## -----------------------------------------------------------------------
transform mg6_fly_move(start_x, start_y, target_x, target_y, duration):
    pos (start_x, start_y)
    linear duration pos (target_x, target_y)


## HUD comum (placar e contador), usado pela tela da mosca e pela tela final.
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


## Uma mosca. Retorna "clicked" (clique) ou "expired" (o timer estourou).
screen minigame6_fly():

    modal True

    add MG6_BG

    use minigame6_hud

    $ fly = mg6_current_fly

    button:
        at mg6_fly_move(fly["start_x"], fly["start_y"], fly["target_x"], fly["target_y"], MG6_FLY_TRAVEL_TIME)
        xysize MG6_FLY_SIZE
        background None
        focus_mask True
        action Return("clicked")
        add mg6_fly_art(fly["type"], fly["file"])

    # Some sozinha: voo + tempo pousada. A tela é nova a cada mosca,
    # então este timer sempre começa do zero.
    timer MG6_FLY_TOTAL_TIME action Return("expired")


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
## 6) LABELS
## -----------------------------------------------------------------------
label minigame_6_gameplay:

    $ quick_menu = False
    $ renpy.block_rollback()
    $ mg6_reset()

    scene black

    while mg6_next_fly():
        call screen minigame6_fly
        $ mg6_resolve_fly(_return)

    call screen minigame6_end

    $ quick_menu = True
    return


label minigame_6_entry:

    call screen minigame6_instructions
    call minigame_6_gameplay

    $ mg_report_score(6, mg6_score, MG6_MAX_SCORE)
    $ mg_complete(6)

    return
