################################################################################
# MG_COMMON.RPY
# Botão de PAUSA global dos minigames + menu de pausa + botão "Menu principal"
# do mapa.
#
# Como funciona (sem mexer nos arquivos dos minigames):
#   - O roadmap.rpy mostra a tela "mg_pause_button" antes de abrir qualquer
#     minigame e a esconde quando ele termina. Ela fica por cima de TUDO
#     (zorder alto), então funciona sobre as telas modais dos minigames,
#     inclusive a de instruções.
#   - Clicar no botão (ou apertar Esc / botão direito) abre o MENU DE PAUSA num
#     "novo contexto" do Ren'Py (o mesmo mecanismo do menu de jogo padrão):
#     o minigame fica congelado e só reaparece quando o jogador volta.
#       * Continuar ........ volta ao minigame de onde parou
#       * Sair para o mapa .. abandona o minigame (sem pontuação e sem marcar
#                             como concluído) e volta ao mapa
#   - O mapa também ganha um botão "Menu principal" (com confirmação).
#
# ARTE (mesmo esquema do resto do jogo): todo PNG é de CANVAS INTEIRO (960x540),
# com o elemento já na posição certa; o jogo amplia 2x (nearest neighbor) e
# desenha em (0, 0); focus_mask True limita o clique aos pixels opacos.
# Enquanto o PNG não existe, aparece um placeholder colorido na posição das
# constantes MGC_*_RECT abaixo (só servem aos placeholders; a arte real ignora).
################################################################################

init python:

    MGC_ART_DIR = "images/common/"
    MGC_ZOOM = 2.0  # arte a 960x540, exibida em 1920x1080

    # ---- Posições dos PLACEHOLDERS (tela 1920x1080): (x, y, largura, altura)
    MGC_PAUSE_BTN_RECT = (20, 980, 80, 80)        # botão de pausa: canto inferior ESQUERDO
    MGC_PAUSE_PANEL_RECT = (610, 250, 700, 580)   # painel de pausa, no meio da tela
    MGC_RESUME_RECT = (710, 540, 500, 90)         # botão "Continuar"
    MGC_QUIT_RECT = (710, 660, 500, 90)           # botão "Sair para o mapa"

    # Barras de VOLUME dentro do painel de pausa (tela 1920x1080).
    # O rótulo ("Música", "Efeitos") e a moldura das barras ficam desenhados
    # no PNG do painel; o jogo só coloca a barra interativa por cima.
    MGC_BAR_X = 900                  # início das barras
    MGC_BAR_W = 340                  # largura das barras
    MGC_BAR_Y = [395, 465]           # y do centro: música, efeitos
    MGC_LABEL_X = 650                # só para o placeholder (rótulos)
    MGC_MAP_MENU_RECT = (30, 30, 260, 80)         # botão "Menu principal" (no mapa)

    def mgc_art(filename, rect, label, color):
        """Arte de canvas inteiro (960x540 → 1920x1080, nearest neighbor,
        desenhada em (0, 0)) se o PNG existir. Senão, um placeholder:
        retângulo colorido com texto na posição "rect" = (x, y, largura, altura)."""
        path = MGC_ART_DIR + filename
        if renpy.loadable(path):
            return Transform(Image(path, nearest_neighbor=True), zoom=MGC_ZOOM)

        x, y, w, h = rect
        text = Text(label, size=24, color="#ffffff", xalign=0.5, yalign=0.5,
                    text_align=0.5, xmaximum=w - 12)
        box = Fixed(Solid(color, xysize=(w, h)), text, xysize=(w, h))
        return Fixed(Transform(box, pos=(x, y)), xysize=(1920, 1080))

    # IMAGEM: common/mg_pausa_idle.png e mg_pausa_hover.png — botão de PAUSA
    # (ex.: ícone de pausa ou de menu). Canvas 960x540, botão no canto inferior
    # esquerdo (ou onde preferir: a posição é a do próprio PNG).
    MGC_PAUSE_IDLE = mgc_art("mg_pausa_idle.png", MGC_PAUSE_BTN_RECT, "II", "#3a3a3a")
    MGC_PAUSE_HOVER = mgc_art("mg_pausa_hover.png", MGC_PAUSE_BTN_RECT, "II", "#5a5a5a")

    # IMAGEM: common/mg_pausa_painel.png — painel do MENU DE PAUSA, no meio da
    # tela, com o título já desenhado (ex.: "JOGO PAUSADO"). Os botões ficam por
    # cima, então deixe espaço para eles. Canvas 960x540. (Pode incluir um
    # escurecimento do resto da tela.)
    # Deixe também desenhados os rótulos "Música" e "Efeitos" à esquerda das
    # barras de volume (linhas em y=395 e y=465 da tela 1920x1080, barras de
    # x=900 a x=1240; no canvas 960x540: y=197 e 232, x=450 a 620).
    MGC_PAUSE_PANEL = mgc_art("mg_pausa_painel.png", MGC_PAUSE_PANEL_RECT, "JOGO PAUSADO\n(mg_pausa_painel.png)", "#3a2e1c")
    MGC_PANEL_IS_ART = renpy.loadable(MGC_ART_DIR + "mg_pausa_painel.png")

    # IMAGEM: common/mg_pausa_continuar_idle.png e _hover.png — botão
    # "Continuar" (texto desenhado). Canvas 960x540.
    MGC_RESUME_IDLE = mgc_art("mg_pausa_continuar_idle.png", MGC_RESUME_RECT, "CONTINUAR\n(mg_pausa_continuar_idle.png)", "#3a5a3a")
    MGC_RESUME_HOVER = mgc_art("mg_pausa_continuar_hover.png", MGC_RESUME_RECT, "CONTINUAR\n(mg_pausa_continuar_hover.png)", "#4f7a4f")

    # IMAGEM: common/mg_pausa_sair_idle.png e _hover.png — botão "Sair para o
    # mapa" (texto desenhado). Canvas 960x540.
    MGC_QUIT_IDLE = mgc_art("mg_pausa_sair_idle.png", MGC_QUIT_RECT, "SAIR PARA O MAPA\n(mg_pausa_sair_idle.png)", "#6a3a3a")
    MGC_QUIT_HOVER = mgc_art("mg_pausa_sair_hover.png", MGC_QUIT_RECT, "SAIR PARA O MAPA\n(mg_pausa_sair_hover.png)", "#8a4a4a")

    # IMAGEM: common/mapa_menu_idle.png e mapa_menu_hover.png — botão "Menu
    # principal" do MAPA (texto desenhado). Canvas 960x540.
    MGC_MAP_MENU_IDLE = mgc_art("mapa_menu_idle.png", MGC_MAP_MENU_RECT, "MENU PRINCIPAL\n(mapa_menu_idle.png)", "#3a3a5a")
    MGC_MAP_MENU_HOVER = mgc_art("mapa_menu_hover.png", MGC_MAP_MENU_RECT, "MENU PRINCIPAL\n(mapa_menu_hover.png)", "#4f4f7a")

    def mgc_sfx(kind):
        files = {"hover": "audio/sfx_hover.ogg", "click": "audio/sfx_click.ogg"}
        path = files.get(kind)
        if path and renpy.loadable(path):
            renpy.sound.play(path)


## -----------------------------------------------------------------------
## Botão de pausa: fica por cima de qualquer minigame (zorder alto).
## Mostrado/escondido pelo roadmap.rpy ao redor de "call expression minigame_N_entry".
## -----------------------------------------------------------------------
screen mg_pause_button():

    zorder 200

    imagebutton:
        idle MGC_PAUSE_IDLE
        hover MGC_PAUSE_HOVER
        focus_mask True
        action [Function(sfx, "window_open"), Function(renpy.call_in_new_context, "mg_pause_label")]
        hovered Function(mgc_sfx, "hover")

    # Esc / botão direito também pausam (em vez do menu de jogo padrão)
    key "game_menu" action Function(renpy.call_in_new_context, "mg_pause_label")


## -----------------------------------------------------------------------
## Menu de pausa (aberto num novo contexto: o minigame fica congelado).
## Retorna "resume" ou "quit".
## -----------------------------------------------------------------------
screen mg_pause_screen():

    modal True
    zorder 300

    add Solid("#000000bb")
    add MGC_PAUSE_PANEL

    # Rótulos só aparecem no placeholder (a arte real já os traz desenhados)
    if not MGC_PANEL_IS_ART:
        text _("Música") pos (MGC_LABEL_X, MGC_BAR_Y[0] - 16) size 28 color "#ffffff"
        text _("Efeitos") pos (MGC_LABEL_X, MGC_BAR_Y[1] - 16) size 28 color "#ffffff"

    # Volume durante o jogo (mesmos valores das Opções do menu)
    bar:
        style "opt_bar"
        value Preference("music volume")
        pos (MGC_BAR_X, MGC_BAR_Y[0] - 12)
        xsize MGC_BAR_W

    bar:
        style "opt_bar"
        value Preference("sound volume")
        pos (MGC_BAR_X, MGC_BAR_Y[1] - 12)
        xsize MGC_BAR_W

    imagebutton:
        idle MGC_RESUME_IDLE
        hover MGC_RESUME_HOVER
        focus_mask True
        action [Function(sfx, "window_close"), Return("resume")]
        hovered Function(mgc_sfx, "hover")

    imagebutton:
        idle MGC_QUIT_IDLE
        hover MGC_QUIT_HOVER
        focus_mask True
        action [Function(sfx, "back"), Return("quit")]
        hovered Function(mgc_sfx, "hover")

    # Esc / botão direito = continuar
    key "game_menu" action Return("resume")


label mg_pause_label:

    $ pause_choice = renpy.call_screen("mg_pause_screen")

    if pause_choice == "quit":
        # sai deste contexto e continua no contexto do minigame, em mg_exit_to_map
        $ renpy.jump_out_of_context("mg_exit_to_map")

    return


## Abandona o minigame atual e volta ao mapa (sem pontuação, sem concluir).
label mg_exit_to_map:

    hide screen mg_pause_button
    $ quick_menu = True

    # limpa a pilha de "call" deixada pelo minigame (entry/gameplay)
    python:
        while renpy.call_stack_depth() > 0:
            renpy.pop_call()

    jump roadmap
