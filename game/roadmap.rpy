################################################################################
# ROADMAP.RPY
# Mapa de desafios ("roadmap"): trilha com os 10 minigames e desbloqueio
# sequencial. O PROGRESSO (liberado / concluído / medalha) é POR SAVE e mora
# em progress.rpy; as conquistas são globais. Minigames já concluídos
# continuam clicáveis (rejogáveis).
#
# Fluxo:
#   Menu -> Novo jogo -> Introdução (intro.rpy) -> label roadmap (este arquivo)
#     -> jogador clica num nó desbloqueado
#     -> chama "label minigame_N_entry" (dentro de minigameN.rpy)
#     -> ao voltar, o roadmap é redesenhado com o progresso atualizado
#
# Cada minigameN.rpy é responsável por, ao concluir, chamar:
#     $ mg_complete(N)
# que marca o minigame N como concluído e desbloqueia o N+1 (se ainda não
# estava desbloqueado). Essa função mora aqui para não repetir a lógica em
# cada um dos 10 arquivos.
################################################################################


## -----------------------------------------------------------------------
## 1) PROGRESSO
##    Agora mora em progress.rpy (por save): mg_complete, mg_report_score,
##    mg_node_state ("locked" / "unlocked" / "done" / "perfect"), conquistas
##    e autosave. Os minigames continuam chamando as mesmas funções.
## -----------------------------------------------------------------------
init python:

    import math


## -----------------------------------------------------------------------
## 2) ARTE DO MAPA
##
## Toda a arte é exportada do Aseprite em 960x540 e ampliada 2x (zoom 2.0 +
## nearest neighbor) para a tela de 1920x1080.
##
##   images/roadmap/map_bg.png            fundo cheio do mapa
##   images/roadmap/node_N_locked.png     nó N bloqueado   (N = 1 a 10)
##   images/roadmap/node_N_unlocked.png   nó N jogável
##   images/roadmap/node_N_done.png       nó N concluído (OPCIONAL: se não
##                                        existir, usa node_N_unlocked.png)
##   images/roadmap/node_N_perfect.png    nó N com PONTUAÇÃO MÁXIMA / medalha
##                                        (OPCIONAL: se não existir, usa
##                                        node_N_done.png e depois _unlocked)
##   (cada um aceita também a versão "_hover": node_N_perfect_hover.png etc.)
##
## Cada PNG de nó é um canvas INTEIRO de 960x540 com o nó já desenhado na
## posição certa (como no menu principal). Por isso a arte real é desenhada em
## (0, 0), sem usar posição do código.
##
## Enquanto a arte de um nó não existe, aparece um retângulo provisório
## (placeholder) na posição MAP_NODE_POS_ART.
## -----------------------------------------------------------------------
init python:

    MAP_ART_DIR = "images/roadmap/"
    MAP_ZOOM = 2.0  # igual ao menu principal e ao minigame1

    def map_art(filename, size, label, color):
        """Imagem real (ampliada 2x) se o arquivo existir, senão um
        retângulo colorido com texto no tamanho final indicado."""
        path = MAP_ART_DIR + filename
        if renpy.loadable(path):
            return Transform(Image(path, nearest_neighbor=True), zoom=MAP_ZOOM)
        return Fixed(
            Solid(color, xysize=size),
            Text(label, size=24, color="#ffffff", xalign=0.5, yalign=0.5,
                 text_align=0.5, xmaximum=size[0] - 16),
            xysize=size,
        )

    # Fundo do mapa. Tamanho final: 1920x1080 → exporte o PNG a 960x540.
    MAP_BG = map_art("map_bg.png", (1920, 1080), "FUNDO DO MAPA\n(map_bg.png)", "#2a2418")

    # ---- Placeholders dos nós (só usados enquanto a arte real não existe) ----
    MAP_NODE_SIZE = (160, 160)

    # Centro de cada placeholder, em coordenadas da ARTE (960x540); o código
    # multiplica por MAP_ZOOM. Trilha em zigzag: linha de baixo (1 a 5,
    # esquerda->direita) e linha de cima (6 a 10, direita->esquerda).
    MAP_NODE_POS_ART = [
        (150, 390), (315, 390), (480, 390), (645, 390), (810, 390),   # 1 a 5
        (810, 150), (645, 150), (480, 150), (315, 150), (150, 150),   # 6 a 10
    ]
    MAP_NODE_POS = [(x * MAP_ZOOM, y * MAP_ZOOM) for (x, y) in MAP_NODE_POS_ART]

    # Linhas guia entre os placeholders; somem sozinhas quando a arte real
    # dos nós já existe (a trilha provavelmente já vem desenhada no map_bg).
    MAP_SHOW_CONNECTORS = not renpy.loadable(MAP_ART_DIR + "node_1_unlocked.png")

    MAP_NODE_COLORS = {"locked": "#3a3a3a", "unlocked": "#2c6e8a", "done": "#2e7d32", "perfect": "#b8860b"}
    MAP_NODE_COLORS_HOVER = {"locked": "#3a3a3a", "unlocked": "#3f93b8", "done": "#3fa845", "perfect": "#e0a820"}

    def map_node_file(n, state):
        """Nome do PNG a usar para o nó n no estado dado, ou None se não há
        arte real (aí o nó usa o placeholder). 'perfect' sem arte própria
        reaproveita a 'done', e 'done' reaproveita a 'unlocked'."""
        candidates = [state]
        if state == "perfect":
            candidates += ["done", "unlocked"]
        elif state == "done":
            candidates.append("unlocked")
        for st in candidates:
            filename = "node_%d_%s.png" % (n, st)
            if renpy.loadable(MAP_ART_DIR + filename):
                return filename
        return None

    def map_node_hover_file(n, state):
        """PNG de HOVER do nó (o mesmo nome da arte parada + "_hover"): ex.
        node_3_unlocked_hover.png, node_3_done_hover.png. None se não existir
        (aí o nó não muda ao passar o mouse, só toca o som)."""
        idle = map_node_file(n, state)
        if idle is None:
            return None
        hover = idle.replace(".png", "_hover.png")
        return hover if renpy.loadable(MAP_ART_DIR + hover) else None

    def map_node_image(filename):
        """Arte real de um nó (canvas inteiro 960x540 -> 1920x1080)."""
        return Transform(Image(MAP_ART_DIR + filename, nearest_neighbor=True), zoom=MAP_ZOOM)

    def map_node_placeholder(n, state, hover=False):
        """Retângulo provisório do nó n (sem colchetes "[...]" no texto: o
        Ren'Py os interpretaria como substituição de variável). hover=True =
        versão mais clara, para quando o mouse está em cima."""
        label = "MINIGAME %d\n(%s)" % (n, state.upper())
        colors = MAP_NODE_COLORS_HOVER if hover else MAP_NODE_COLORS
        return Fixed(
            Solid(colors[state], xysize=MAP_NODE_SIZE),
            Text(label, size=24, color="#ffffff", xalign=0.5, yalign=0.5,
                 text_align=0.5, xmaximum=MAP_NODE_SIZE[0] - 16),
            xysize=MAP_NODE_SIZE,
        )

    def mg_map_connector(p1, p2, color="#ffffff55", thickness=6):
        """Barra fina ligando o centro de p1 ao centro de p2 (só guia visual
        para os placeholders)."""
        x1, y1 = p1
        x2, y2 = p2
        length = math.hypot(x2 - x1, y2 - y1)
        angle = math.degrees(math.atan2(y2 - y1, x2 - x1))
        bar = Solid(color, xysize=(int(length), thickness))
        return Transform(bar, rotate=angle, xanchor=0.0, yanchor=0.5, xpos=x1, ypos=y1)

    def mg_map_sfx(kind):
        files = {"hover": "audio/sfx_hover.ogg", "click": "audio/sfx_click.ogg"}
        path = files.get(kind)
        if path and renpy.loadable(path):
            renpy.sound.play(path)


## -----------------------------------------------------------------------
## 3) TELA DO MAPA
## -----------------------------------------------------------------------
screen roadmap_screen():

    modal True

    add MAP_BG

    text _("MAPA DE DESAFIOS"):
        xalign 0.5
        ypos 40
        size 40
        color "#ffffff"

    # Medalhas (pontuação máxima) conquistadas neste save
    $ medals_now = mg_medal_count()
    $ medals_total = MG_IMPLEMENTED
    text _("Medalhas: [medals_now]/[medals_total]"):
        xalign 0.97
        ypos 40
        size 34
        color "#ffffff"

    # Botão "Menu principal" (arte em mg_common.rpy: common/mapa_menu_*.png).
    # Pede confirmação antes de sair; o progresso fica no save (use Continuar).
    # (Não usa MainMenu(): o jogo é iniciado no menu com Jump("intro"), e por
    # isso roda dentro do contexto do menu principal, onde MainMenu() não faz
    # nada. renpy.full_restart funciona em qualquer contexto.)
    imagebutton:
        idle MGC_MAP_MENU_IDLE
        hover MGC_MAP_MENU_HOVER
        focus_mask True
        action [Function(mg_map_sfx, "click"),
                Confirm(_("Voltar ao menu principal?"), yes=Function(renpy.full_restart))]
        hovered Function(mg_map_sfx, "hover")

    if MAP_SHOW_CONNECTORS:
        for i in range(MG_TOTAL - 1):
            add mg_map_connector(MAP_NODE_POS[i], MAP_NODE_POS[i + 1])

    # Os 10 nós da trilha
    for i in range(MG_TOTAL):

        $ n = i + 1
        $ node_state = mg_node_state(n)
        $ node_file = map_node_file(n, node_state)
        $ node_hover_file = map_node_hover_file(n, node_state)
        $ node_x, node_y = MAP_NODE_POS[i]
        $ clickable = (node_state != "locked")

        if node_file is not None:
            # ---- Arte real: canvas inteiro, desenhada em (0, 0) ----
            if clickable:
                # idle = node_N_<estado>.png; hover = node_N_<estado>_hover.png
                # (se o hover não existir, a imagem não muda)
                $ node_idle_img = map_node_image(node_file)
                $ node_hover_img = map_node_image(node_hover_file or node_file)
                imagebutton:
                    idle node_idle_img
                    hover node_hover_img
                    focus_mask True   # só os pixels opacos do nó respondem
                    action [Play("sound", "audio/sfx_click.ogg"), Return(n)]
                    hovered Function(mg_map_sfx, "hover")
            else:
                add map_node_image(node_file)

        else:
            # ---- Placeholder provisório, na posição MAP_NODE_POS ----
            if clickable:
                $ ph_idle = map_node_placeholder(n, node_state)
                $ ph_hover = map_node_placeholder(n, node_state, True)
                imagebutton:
                    pos (node_x, node_y)
                    anchor (0.5, 0.5)
                    idle ph_idle
                    hover ph_hover
                    action [Play("sound", "audio/sfx_click.ogg"), Return(n)]
                    hovered Function(mg_map_sfx, "hover")
            else:
                add map_node_placeholder(n, node_state):
                    pos (node_x, node_y)
                    anchor (0.5, 0.5)


## -----------------------------------------------------------------------
## 4) LABEL DO MAPA
##    Ponto de entrada: "jump roadmap" (chamado pelo script.rpy após a intro).
## -----------------------------------------------------------------------
label roadmap:

    $ quick_menu = True

    # Salva sozinho toda vez que o mapa aparece (é o "Continuar" do menu)
    $ prog_autosave()

    call screen roadmap_screen with Dissolve(0.5)
    $ chosen = _return

    # Trava extra: nó bloqueado ou ainda sem minigame nunca abre
    if chosen and chosen <= mg_unlocked and chosen <= MG_IMPLEMENTED:
        # Chama "label minigame_<chosen>_entry" dinamicamente.
        # Esse label mora dentro de minigame<chosen>.rpy e é responsável por
        # mostrar as instruções, rodar o gameplay e chamar mg_complete(chosen).
        # O botão de pausa (mg_common.rpy) fica por cima do minigame; ao
        # terminar normalmente ele é escondido aqui (se o jogador sair pelo
        # menu de pausa, quem esconde é o label mg_exit_to_map).
        show screen mg_pause_button
        call expression ("minigame_%d_entry" % chosen)
        hide screen mg_pause_button

    # Volta a mostrar o mapa (com o progresso já atualizado).
    jump roadmap
