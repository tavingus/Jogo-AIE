################################################################################
# MUSIC.RPY
# Músicas do jogo (todas em loop) e a função que toca com segurança.
#
#   audio/intro_1.ogg ... música da imagem 1 da introdução
#   audio/intro_2.ogg ... música da imagem 2 da introdução
#   audio/intro_3.ogg ... música da imagem 3 da introdução
#   audio/menu_theme.ogg  música do MENU PRINCIPAL e do MAPA (roadmap)
#
# Pode ser .ogg, .mp3, .opus ou .wav: o jogo procura o arquivo com qualquer
# dessas extensões. Se o arquivo ainda não existe, simplesmente não toca nada
# (sem erro). Renomeie suas músicas para esses nomes e coloque em game/audio/.
#
# A mesma música não reinicia: se o menu já está tocando menu_theme e você
# vai para o mapa, ela continua de onde estava.
################################################################################

init python:

    MUS_INTRO = ["audio/intro_1", "audio/intro_2", "audio/intro_3"]
    MUS_MENU = "audio/menu_theme"
    MUS_EXTS = [".ogg", ".mp3", ".opus", ".wav"]
    MUS_FADE = 1.0      # segundos de fade ao trocar de música

    def mus_find(base):
        for ext in MUS_EXTS:
            if renpy.loadable(base + ext):
                return base + ext
        return None

    def mus_play(base, fade=None):
        """Toca "base" em loop (com fade). Não faz nada se já estiver tocando
        ou se o arquivo não existir."""
        path = mus_find(base)
        if path is None:
            return
        if renpy.music.get_playing("music") == path:
            return
        f = MUS_FADE if fade is None else fade
        renpy.music.play(path, channel="music", loop=True, fadein=f, fadeout=f)

    def mus_menu():
        mus_play(MUS_MENU)

    def mus_stop(fade=None):
        renpy.music.stop(channel="music", fadeout=MUS_FADE if fade is None else fade)
