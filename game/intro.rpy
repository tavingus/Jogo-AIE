################################################################################
# INTRO.RPY
# "Novo jogo" + cutscene de introdução: 3 imagens, cada uma com uma caixa de
# texto, dissolve entre as imagens e fade out para o mapa.
#
# Fluxo:
#   Menu -> JOGAR -> label novo_jogo (este arquivo) -> label roadmap (roadmap.rpy)
#
# A introdução só passa em "Novo jogo" (quem usa "Continuar" vai direto ao
# mapa). Clicar (ou Enter/Espaço) avança; o botão PULAR vai direto ao mapa.
#
# O botão Jogar do menu usa Start("novo_jogo"): isso começa um jogo NOVO, com
# todo o progresso zerado (as variáveis "default" voltam ao valor inicial).
# O "label intro" antigo do script.rpy deixa de ser usado.
#
# ARTE (todas em canvas inteiro 960x540, como no resto do jogo):
#   images/intro/intro_1.png, intro_2.png, intro_3.png — as 3 cenas (sem texto)
#   images/intro_box.png ......... caixa de texto do rodapé (sem texto)
#   images/intro_skip_idle.png / intro_skip_hover.png — botão PULAR
# Enquanto o PNG não existe, aparece um placeholder colorido.
################################################################################

init python:

    # Os 3 atos da história (um por imagem). Edite à vontade; mantenha curtos.
    INTRO_TEXTS = [
        _("Equinópolis é uma cidade que respira cavalos. Aqui, eles trabalham, competem e fazem parte de cada família."),
        _("Mas um inimigo invisível chegou: a Anemia Infecciosa Equina. Ela passa por insetos e agulhas contaminadas, e não tem cura nem vacina."),
        _("Cabe a você, veterinário(a) da cidade, identificar, testar e conter a doença antes que ela se espalhe."),
    ]

    # Tempos (segundos)
    INTRO_DISSOLVE = 1.0        # dissolve entre as imagens
    INTRO_FADE_OUT = 1.2        # fade para preto no fim (e/ou ao pular)

    # Posições dos PLACEHOLDERS (tela 1920x1080): (x, y, largura, altura)
    INTRO_BOX_RECT = (160, 780, 1600, 240)
    INTRO_SKIP_RECT = (1620, 30, 260, 70)
    INTRO_TEXT_POS = (230, 815)         # texto dentro da caixa
    INTRO_TEXT_W = 1460
    INTRO_ARROW_POS = (1770, 970)       # "▼" de "clique para continuar"

    INTRO_ART = [
        menu_opt_art("intro/intro_%d.png" % (i + 1), (0, 0, 1920, 1080),
                     "INTRO %d\n(intro/intro_%d.png)" % (i + 1, i + 1), c)
        for i, c in enumerate(["#2f5a3a", "#5a3a2f", "#2f3a5a"])
    ]
    INTRO_BOX = menu_opt_art("intro_box.png", INTRO_BOX_RECT, "CAIXA DE TEXTO\n(intro_box.png)", "#7a5a3a")
    INTRO_SKIP_IDLE = menu_opt_art("intro_skip_idle.png", INTRO_SKIP_RECT, "PULAR", "#6a6a6a")
    INTRO_SKIP_HOVER = menu_opt_art("intro_skip_hover.png", INTRO_SKIP_RECT, "PULAR", "#8a8a8a")


default intro_i = 0
default intro_skip = False


## Caixa de texto de um ato. Retorna True (avançar) ou "skip" (pular).
screen intro_textbox(txt):

    modal True

    # Clicar em qualquer lugar (ou Enter/Espaço) avança
    button:
        xfill True
        yfill True
        background None
        action Return(True)
    key "dismiss" action Return(True)

    add INTRO_BOX

    $ intro_text = txt
    text "[intro_text!t]":
        pos INTRO_TEXT_POS
        xmaximum INTRO_TEXT_W
        size 38
        color "#3a2410"

    text "▼":
        font "DejaVuSans.ttf"
        pos INTRO_ARROW_POS
        size 36
        color "#6a4a22"

    imagebutton:
        idle INTRO_SKIP_IDLE
        hover INTRO_SKIP_HOVER
        focus_mask True
        action [Play("sound", "audio/sfx_click.ogg"), Return("skip")]
        hovered Play("sound", "audio/sfx_hover.ogg")


label novo_jogo:

    $ quick_menu = False
    $ intro_i = 0
    $ intro_skip = False

    # (opcional) música da introdução, se o arquivo existir
    if renpy.loadable("audio/intro_theme.ogg"):
        play music "audio/intro_theme.ogg" fadein 1.0

    scene black

    while intro_i < len(INTRO_TEXTS) and not intro_skip:
        $ intro_art = INTRO_ART[intro_i]
        scene expression intro_art with Dissolve(INTRO_DISSOLVE)
        call screen intro_textbox(INTRO_TEXTS[intro_i])
        if _return == "skip":
            $ intro_skip = True
        $ intro_i += 1

    # Fade out: some a imagem e a música, e então aparece o mapa
    $ renpy.music.stop(channel="music", fadeout=INTRO_FADE_OUT)
    scene black with Dissolve(INTRO_FADE_OUT)

    $ quick_menu = True
    jump roadmap
