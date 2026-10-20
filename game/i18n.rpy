################################################################################
# I18N.RPY
# Define o idioma do jogo como português. Os textos em inglês do Ren'Py (menu
# rápido, opções, confirmações como "Tem certeza de que quer sair?") são
# traduzidos em game/tl/portuguese/strings.rpy.
#
# "config.default_language" só vale na primeira vez que o jogo abre (depois o
# Ren'Py usa o idioma guardado nas preferências do jogador). Por isso há também
# o trecho abaixo, que troca para o português uma vez por sessão, na primeira
# interação, se o idioma ainda não for o português.
################################################################################

define config.default_language = "portuguese"

init python:

    _pt_forced = [False]

    def _ensure_portuguese():
        if _pt_forced[0]:
            return
        _pt_forced[0] = True
        if renpy.game.preferences.language != "portuguese":
            renpy.change_language("portuguese")

    config.interact_callbacks.append(_ensure_portuguese)
