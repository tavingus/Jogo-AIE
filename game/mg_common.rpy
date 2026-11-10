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

## Cor do texto das telas de instruções de todos os minigames (escuro, para
## ler bem sobre a moldura clara de pergaminho). Se um dia a moldura for escura,
## troque aqui (ex.: "#ffffff") e vale para os 7 minigames.
define -2 MG_INSTR_TEXT_COLOR = "#372412"

init -10 python:

    def mg_canvas_art(path):
        """Arte em pixel art. Até 960x540: zoom 2 com nearest neighbor.
        MAIOR que isso (ex.: 1536x1024 direto do gerador de imagens): corta ao
        centro para 16:9 e ajusta a 1920x1080, para não ficar fora do lugar."""
        w, h = renpy.image_size(path)
        # 960x540 (canvas) ou MENOR (arte do tamanho do elemento, ex.: botões
        # e cartas do minigame 2, painéis do 6): zoom 2, como sempre foi.
        if w <= 960 and h <= 540:
            return Transform(Image(path, nearest_neighbor=True), zoom=2.0)
        # MAIOR que o canvas (direto do gerador de imagens): corta para 16:9.
        if w * 9 > h * 16:
            cw, ch = int(h * 16 / 9), h
        else:
            cw, ch = w, int(w * 9 / 16)
        x0, y0 = (w - cw) // 2, (h - ch) // 2
        return Transform(Image(path), crop=(x0, y0, cw, ch), zoom=1920.0 / cw)

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
            return mg_canvas_art(path)

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
## RESULTADO + REVISÃO (igual para todos os minigames)
##
## Durante o jogo só aparece um sinal curto (som, carimbo, cor). No FIM, esta
## tela mostra a pontuação, uma frase de feedback e a REVISÃO: tudo o que o
## jogador acertou e errou, com a resposta certa e o porquê. Dois botões:
## "Jogar de novo" e "Continuar".
##
## Como um minigame usa:
##   $ mg_review_clear()                         (no começo da partida)
##   $ mg_review_group("Título do bloco")        (opcional: cabeçalho)
##   $ mg_review_add("ok" | "bad" | "miss", "texto", "explicação (opcional)")
##   $ mg_review_note("texto solto")             (opcional)
##   call screen mg_result(pontos, maximo, frase)
##   -> retorna "replay" (jogar de novo) ou "continue".
##
## ARTE (canvas 960x540, em images/common/): mg_resultado_painel.png (painel
## com moldura da lista; SEM título nem textos), mg_resultado_jogar_idle/hover
## e mg_resultado_continuar_idle/hover (botões, textos já desenhados). Os
## retângulos abaixo (tela 1920x1080) só servem aos placeholders e às posições
## dos textos escritos pelo jogo.
## -----------------------------------------------------------------------
default mg_review = []

init python:

    MG_RESULT_PANEL_RECT = (200, 70, 1520, 940)
    MG_RESULT_TITLE_POS = (960, 126)            # título (centralizado)
    MG_RESULT_SCORE_POS = (960, 208)            # "Pontuação: N / M" (centralizado)
    MG_RESULT_VERDICT_POS = (960, 252)          # frase de feedback (centralizada, até 2 linhas)
    MG_RESULT_LIST = (268, 334, 1380, 468)      # área da revisão: x, y, largura, altura
    MG_RESULT_BAR = (1654, 334, 20, 468)        # barra de rolagem
    MG_RESULT_REPLAY_RECT = (340, 864, 460, 100)
    MG_RESULT_CONTINUE_RECT = (1120, 864, 460, 100)

    MG_RESULT_PANEL = mgc_art("mg_resultado_painel.png", MG_RESULT_PANEL_RECT, "", "#ead9a8")
    MG_RESULT_REPLAY_IDLE = mgc_art("mg_resultado_jogar_idle.png", MG_RESULT_REPLAY_RECT, "JOGAR DE NOVO", "#486898")
    MG_RESULT_REPLAY_HOVER = mgc_art("mg_resultado_jogar_hover.png", MG_RESULT_REPLAY_RECT, "JOGAR DE NOVO", "#6286bc")
    MG_RESULT_CONTINUE_IDLE = mgc_art("mg_resultado_continuar_idle.png", MG_RESULT_CONTINUE_RECT, "CONTINUAR", "#568e48")
    MG_RESULT_CONTINUE_HOVER = mgc_art("mg_resultado_continuar_hover.png", MG_RESULT_CONTINUE_RECT, "CONTINUAR", "#74b25c")

    MG_MARK_GLYPH = {"ok": u"\u2713", "bad": u"\u2717", "miss": "!"}
    MG_MARK_COLOR = {"ok": "#2e7d32", "bad": "#a02a22", "miss": "#b07a10"}

    def mg_review_clear():
        store.mg_review = []

    def mg_review_group(text):
        store.mg_review.append({"kind": "group", "text": text})

    def mg_review_note(text):
        store.mg_review.append({"kind": "note", "text": text})

    def mg_review_add(mark, text, why=""):
        store.mg_review.append({"kind": "item", "mark": mark, "text": text, "why": why})


screen mg_result(score, max_score, verdict, title=None):

    modal True
    zorder 150

    add Solid("#000000bb")
    add MG_RESULT_PANEL

    $ title_text = title if title else _("RESULTADO")
    $ score_line = _("Pontuação: %d / %d") % (score, max_score)

    text "[title_text!t]":
        pos MG_RESULT_TITLE_POS
        anchor (0.5, 0.5)
        size 46
        bold True
        color MG_INSTR_TEXT_COLOR

    text "[score_line!t]":
        pos MG_RESULT_SCORE_POS
        anchor (0.5, 0.5)
        size 38
        color MG_INSTR_TEXT_COLOR

    text "[verdict!t]":
        pos MG_RESULT_VERDICT_POS
        anchor (0.5, 0.0)
        text_align 0.5
        size 26
        xmaximum 1300
        color "#5a3a14"

    viewport:
        id "mg_review_vp"
        pos (MG_RESULT_LIST[0], MG_RESULT_LIST[1])
        xysize (MG_RESULT_LIST[2], MG_RESULT_LIST[3])
        mousewheel True
        draggable True

        vbox:
            spacing 10
            xsize MG_RESULT_LIST[2] - 20

            for it in mg_review:

                $ it_kind = it["kind"]
                $ it_text = it["text"]

                if it_kind == "group":
                    text it_text:
                        substitute False
                        size 30
                        bold True
                        color "#6a3a10"
                        xmaximum 1340
                elif it_kind == "note":
                    text it_text:
                        substitute False
                        size 24
                        italic True
                        color "#5a4a38"
                        xmaximum 1340
                else:
                    $ it_mark = it["mark"]
                    $ it_why = it["why"]
                    $ it_glyph = MG_MARK_GLYPH[it_mark]
                    $ it_color = MG_MARK_COLOR[it_mark]
                    hbox:
                        spacing 14
                        text it_glyph:
                            font "DejaVuSans.ttf"
                            size 30
                            bold True
                            color it_color
                            min_width 34
                            substitute False
                        vbox:
                            spacing 2
                            text it_text:
                                substitute False
                                size 26
                                color MG_INSTR_TEXT_COLOR
                                xmaximum 1280
                            if it_why:
                                text it_why:
                                    substitute False
                                    size 22
                                    color "#5a4a38"
                                    xmaximum 1280

    text _("✓ acertou     ✗ errou     ! faltou fazer"):
        font "DejaVuSans.ttf"
        pos (960, 822)
        anchor (0.5, 0.0)
        size 22
        color "#5a4a38"

    vbar:
        value YScrollValue("mg_review_vp")
        pos (MG_RESULT_BAR[0], MG_RESULT_BAR[1])
        xysize (MG_RESULT_BAR[2], MG_RESULT_BAR[3])
        top_bar Solid("#00000000")
        bottom_bar Solid("#00000000")
        thumb Solid("#6a4a22", xysize=(18, 80))
        unscrollable "hide"

    imagebutton:
        idle MG_RESULT_REPLAY_IDLE
        hover MG_RESULT_REPLAY_HOVER
        focus_mask True
        action [Function(sfx, "click"), Return("replay")]
        hovered Function(sfx, "hover")

    imagebutton:
        idle MG_RESULT_CONTINUE_IDLE
        hover MG_RESULT_CONTINUE_HOVER
        focus_mask True
        action [Function(sfx, "click"), Return("continue")]
        hovered Function(sfx, "hover")


## -----------------------------------------------------------------------
## TUTORIAL COM IMAGENS (igual para todos os minigames)
##
## Tela "Como jogar": à esquerda, uma MINIATURA da própria tela do minigame
## (a mesma arte, a 40%), com selos numerados apontando as partes importantes;
## à direita, os 3 passos. Cada minigame monta a sua miniatura e chama:
##
##   use mg_tutorial(bg, subtitulo, miniatura, [(x, y), ...], [passo1, ...],
##                   nota, close_idle, close_hover, close_align)
##
## Os selos (x, y) são em coordenadas da TELA DO JOGO (1920x1080); a tela
## converte para a miniatura. close_align = None (arte de canvas inteiro) ou
## (xalign, yalign) para o botão antigo de peça solta (minigames 2 e 6).
## -----------------------------------------------------------------------
init python:

    MG_TUT_SCALE = 0.4
    MG_TUT_POS = (290, 350)          # canto da miniatura na tela (768x432)

    def mg_tut_font_sizes(steps, note):
        """Tamanho da fonte dos passos e da nota do tutorial, conforme a
        quantidade de texto (a área tem ~560 x 500 px)."""
        n = sum(len(renpy.translate_string(s)) for s in steps) + len(renpy.translate_string(note))
        if n <= 330:
            return 26, 22
        if n <= 430:
            return 24, 20
        if n <= 530:
            return 22, 19
        return 20, 18

    def mg_tut_preview(layers):
        """Miniatura (40%) de uma lista de camadas desenhadas em 1920x1080."""
        return Transform(Fixed(*layers, xysize=(1920, 1080)), zoom=MG_TUT_SCALE)

    def mg_tut_at(displayable, x, y):
        """Posiciona uma camada na miniatura (coordenadas da tela do jogo)."""
        return Transform(displayable, pos=(x, y))

    def mg_tut_text(txt, x, y, size=30, color="#ffffff", bold=False):
        """Texto do jogo (placar, rótulos) como camada da miniatura."""
        return Transform(Text(txt, size=size, color=color, bold=bold,
                              outlines=[(3, "#2a1a0c", 0, 0)]), pos=(x, y))


screen mg_badge(n, x, y):
    fixed:
        pos (x - 24, y - 24)
        xysize (48, 48)
        add Solid("#372412", xysize=(48, 48))
        add Solid("#f2c230", xysize=(42, 42)) pos (3, 3)
        text "[n]":
            xalign 0.5
            yalign 0.5
            size 34
            bold True
            color "#372412"


screen mg_badge_inline(n):
    fixed:
        xysize (48, 48)
        add Solid("#372412", xysize=(48, 48))
        add Solid("#f2c230", xysize=(42, 42)) pos (3, 3)
        text "[n]":
            xalign 0.5
            yalign 0.5
            size 34
            bold True
            color "#372412"


screen mg_step(n, txt, y):
    use mg_badge(n, 1124, y + 24)
    text "[txt!t]":
        pos (1166, y)
        size 26
        xmaximum 470
        color MG_INSTR_TEXT_COLOR


screen mg_tutorial(bg, subtitle, preview, badges, steps, note, close_idle, close_hover, close_align=None):

    modal True

    add bg
    add Solid("#000000aa")
    add MG_RESULT_PANEL

    text _("COMO JOGAR"):
        pos MG_RESULT_TITLE_POS
        anchor (0.5, 0.5)
        size 46
        bold True
        color MG_INSTR_TEXT_COLOR

    text "[subtitle!t]":
        pos MG_RESULT_SCORE_POS
        anchor (0.5, 0.5)
        size 34
        color MG_INSTR_TEXT_COLOR

    # Miniatura da tela do minigame + selos numerados
    add Solid("#372412", xysize=(776, 440)) pos (MG_TUT_POS[0] - 4, MG_TUT_POS[1] - 4)
    add preview pos MG_TUT_POS

    for i, b in enumerate(badges):
        $ badge_x = MG_TUT_POS[0] + int(b[0] * MG_TUT_SCALE)
        $ badge_y = MG_TUT_POS[1] + int(b[1] * MG_TUT_SCALE)
        use mg_badge(i + 1, badge_x, badge_y)

    # Passos (até 3) e nota, empilhados (cada um ocupa só a altura que
    # precisa) e com a fonte ajustada ao tamanho do texto: nada transborda.
    $ tut_fs, tut_note_fs = mg_tut_font_sizes(steps, note)
    vbox:
        pos (1100, 336)
        xsize 560
        spacing (18 if tut_fs >= 24 else 12)
        for i, st in enumerate(steps):
            hbox:
                spacing 14
                use mg_badge_inline(i + 1)
                text "[st!t]":
                    size tut_fs
                    xmaximum 490
                    color MG_INSTR_TEXT_COLOR
        null height 4
        text "[note!t]":
            size tut_note_fs
            italic True
            xmaximum 540
            color "#5a4a38"

    if close_align:
        imagebutton:
            xalign close_align[0]
            yalign close_align[1]
            idle close_idle
            hover close_hover
            focus_mask True
            action [Function(sfx, "click"), Return(True)]
            hovered Function(sfx, "hover")
    else:
        imagebutton:
            idle close_idle
            hover close_hover
            focus_mask True
            action [Function(sfx, "click"), Return(True)]
            hovered Function(sfx, "hover")


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
    $ mg_active = False
    $ quick_menu = True

    # limpa a pilha de "call" deixada pelo minigame (entry/gameplay)
    python:
        while renpy.call_stack_depth() > 0:
            renpy.pop_call()

    jump roadmap


## -----------------------------------------------------------------------
## PLACAR COM FUNDO + "+N" / "−N" FLUTUANTES (feedback imediato de pontos)
##
##   use mg_score_hud(pontos, (x, y))     — placar legível sobre qualquer fundo
##   $ mg_float(+10)                       — "+10" verde que sobe e some, onde
##   $ mg_float(-5, x, y, _("Errado!"))      o jogador clicou (ou em x, y),
##                                           com um rótulo curto opcional
## O sinal (+/−) e a cor andam juntos: quem não distingue verde de vermelho
## ainda lê o sinal.
## -----------------------------------------------------------------------
init python:

    MG_FLOAT_TIME = 1.6       # s na tela
    _mg_float_counter = [0]

    def mg_float(delta, x=None, y=None, label="", ok=None):
        """Mostra "+N" (verde) ou "−N" (vermelho) subindo e sumindo.
        ok=None: a cor segue o sinal de delta; ok=True/False força a cor
        (ex.: erro que não tira pontos mostra "+0" vermelho)."""
        if x is None or y is None:
            x, y = renpy.get_mouse_pos()
        x = max(90, min(1830, int(x)))
        y = max(70, min(1000, int(y)))
        if ok is None:
            ok = delta > 0
        _mg_float_counter[0] = (_mg_float_counter[0] + 1) % 12
        tag = "mg_float_%d" % _mg_float_counter[0]
        sign = "+" if delta >= 0 else u"−"
        renpy.show_screen("mg_float", "%s%d" % (sign, abs(delta)), x, y, label, ok, tag, _tag=tag)
        renpy.restart_interaction()


    def mg_float_clear():
        """Some com todos os "+N/−N" ainda na tela. Chamado ao voltar ao mapa,
        antes do autosave e depois de carregar um save, para um popup antigo
        nunca reaparecer (era o "Correto! +10" ao clicar em Continuar)."""
        for k in range(12):
            renpy.hide_screen("mg_float_%d" % k)

    def _mg_float_after_load():
        mg_float_clear()

    config.after_load_callbacks.append(_mg_float_after_load)


transform mg_float_rise:
    alpha 0.0 zoom 0.5 yoffset 0
    easein 0.14 alpha 1.0 zoom 1.15
    easeout 0.10 zoom 1.0
    linear 1.0 yoffset -80
    easein 0.3 alpha 0.0 yoffset -100


screen mg_float(value, x, y, label, ok, tag):

    zorder 260

    vbox:
        pos (x, y)
        anchor (0.5, 1.0)
        at mg_float_rise
        text value:
            xalign 0.5
            size 64
            bold True
            color ("#6dff7a" if ok else "#ff5d4d")
            outlines [(5, "#1e1208", 0, 0)]
        if label:
            text label:
                xalign 0.5
                size 32
                bold True
                color ("#d8ffd8" if ok else "#ffd6d0")
                outlines [(4, "#1e1208", 0, 0)]

    timer MG_FLOAT_TIME action Hide(tag)


screen mg_score_hud(score, hud_pos):

    frame:
        pos hud_pos
        background Solid("#f2c230")
        padding (4, 4)
        frame:
            background Solid("#2a1a0ce8")
            padding (22, 8)
            hbox:
                spacing 14
                text _("Pontos"):
                    yalign 0.5
                    size 30
                    color "#ffe9a8"
                text "[score]":
                    yalign 0.5
                    size 44
                    bold True
                    color "#ffffff"
