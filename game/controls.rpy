################################################################################
# CONTROLS.RPY
# Controles globais do jogo (fora do que cada minigame já trata):
#
#   - Sem a barra inferior padrão do Ren'Py (Voltar, Histórico, Pular, Auto...).
#   - Sem ROLLBACK: a roda do mouse (e Page Up) não "volta no tempo". Antes,
#     rolar para cima numa tela de tutorial ou na introdução voltava para a
#     tela anterior e depois avançava de novo.
#   - Esc / botão direito abrem o MENU DE PAUSA do jogo (o mesmo visual da
#     pausa dos minigames) em vez do menu padrão do Ren'Py (salvar/carregar).
#       * Dentro de um minigame: a pausa dos minigames (mg_common.rpy), com
#         "Continuar" e "Sair para o mapa" (não mudou).
#       * No mapa, na introdução e nas outras telas: "Continuar" e "Menu
#         principal" (com confirmação), mais o volume.
################################################################################

init 999 python:

    # Barra inferior do Ren'Py (quick menu): tira do jogo inteiro.
    config.overlay_screens = [s for s in config.overlay_screens if s != "quick_menu"]

    # Rollback desligado (roda do mouse para cima / Page Up não voltam mais).
    config.rollback_enabled = False
    config.hard_rollback_limit = 0
    config.keymap["rollback"] = []
    config.keymap["rollforward"] = []

    # Esc / botão direito abrem a nossa pausa (screen game_pause, abaixo).
    _game_menu_screen = "game_pause"


init python:

    # IMAGEM: common/mg_pausa_menu_idle.png e _hover.png — botão "Menu
    # principal" da pausa geral (mesma posição do "Sair para o mapa").
    MGC_MAINMENU_IDLE = mgc_art("mg_pausa_menu_idle.png", MGC_QUIT_RECT, "MENU PRINCIPAL", "#6a3a3a")
    MGC_MAINMENU_HOVER = mgc_art("mg_pausa_menu_hover.png", MGC_QUIT_RECT, "MENU PRINCIPAL", "#8a4a4a")


## Pausa geral (fora dos minigames). Aberta pelo Ren'Py num novo contexto
## (o jogo atrás fica congelado e visível). Return() volta ao jogo.
screen game_pause():

    modal True
    zorder 300

    # No menu principal o Esc não faz nada
    if main_menu:
        timer 0.01 action Return()

    add Solid("#000000bb")
    add MGC_PAUSE_PANEL

    if not MGC_PANEL_IS_ART:
        text _("Música") pos (MGC_LABEL_X, MGC_BAR_Y[0] - 16) size 28 color "#ffffff"
        text _("Efeitos") pos (MGC_LABEL_X, MGC_BAR_Y[1] - 16) size 28 color "#ffffff"

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
        action [Function(sfx, "window_close"), Return()]
        hovered Function(mgc_sfx, "hover")

    imagebutton:
        idle MGC_MAINMENU_IDLE
        hover MGC_MAINMENU_HOVER
        focus_mask True
        action [Function(sfx, "back"),
                Confirm(_("Voltar ao menu principal? O progresso fica salvo (use Continuar)."),
                        yes=Function(renpy.full_restart))]
        hovered Function(mgc_sfx, "hover")

    # Esc / botão direito = continuar
    key "game_menu" action Return()
