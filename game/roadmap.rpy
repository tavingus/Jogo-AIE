################################################################################
# ROADMAP.RPY
# Mapa de desafios ("roadmap"): trilha com os 10 minigames, progresso GLOBAL
# (tipo conquista — independe de qual save você carrega) e desbloqueio
# sequencial. Minigames já concluídos continuam clicáveis (rejogáveis).
#
# Fluxo:
#   Menu -> Introdução -> label roadmap (este arquivo)
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
## 1) PROGRESSO (persistent = global, sobrevive a qualquer save/novo jogo)
## -----------------------------------------------------------------------
init python:

    import math

    MG_TOTAL = 10  # total de minigames no mapa

    # persistent.mg_unlocked = número do minigame mais avançado já liberado.
    # Começa em 1 (só o primeiro nó liberado) na primeiríssima vez que o
    # jogo roda nesta máquina; depois disso o valor já salvo é reaproveitado.
    if persistent.mg_unlocked is None:
        persistent.mg_unlocked = 1

    # persistent.mg_completed[i] = True se o minigame (i+1) já foi concluído
    # ao menos uma vez (controla o selo de "concluído" no nó, não o bloqueio).
    if persistent.mg_completed is None:
        persistent.mg_completed = [False] * MG_TOTAL

    def mg_complete(n):
        """Chame ao final de cada minigame: '$ mg_complete(N)'.
        Marca o minigame N como concluído e libera o N+1, se for o caso."""
        persistent.mg_completed[n - 1] = True
        if persistent.mg_unlocked == n:
            persistent.mg_unlocked = min(persistent.mg_unlocked + 1, MG_TOTAL)

    def mg_node_state(n):
        """'locked' / 'unlocked' / 'done' para o nó do minigame n."""
        if n > persistent.mg_unlocked:
            return "locked"
        elif persistent.mg_completed[n - 1]:
            return "done"
        else:
            return "unlocked"


## -----------------------------------------------------------------------
## 1.5) PONTUAÇÃO E MEDALHAS (também persistent = global)
##
## A pontuação é individual por minigame, NÃO cumulativa no jogo todo.
## Cada minigame com pontuação chama "mg_report_score(N, pontos, max_pontos)"
## ANTES de "mg_complete(N)". Minigames sem pontuação (ex.: o 1, por enquanto)
## continuam chamando só "mg_complete(N)" normalmente — nada muda para eles.
##
## Medalha de minigame = tirou a pontuação máxima dele ALGUMA VEZ (mesmo que
## uma partida depois seja pior, a medalha já conquistada não é perdida).
## Medalha de maestria = as 10 medalhas de minigame foram conquistadas.
## -----------------------------------------------------------------------
init python:

    # persistent.mg_scores[i]     = pontuação da ÚLTIMA partida do minigame (i+1)
    # persistent.mg_max_scores[i] = pontuação máxima possível do minigame (i+1)
    #                               (cada minigame informa a sua própria, pode
    #                               mudar se você rebalancear o jogo depois)
    # persistent.mg_medals[i]     = True = já tirou nota máxima no minigame (i+1)
    # persistent.mg_mastery       = True = as 10 medalhas de minigame foram conquistadas
    if persistent.mg_scores is None:
        persistent.mg_scores = [0] * MG_TOTAL
    if persistent.mg_max_scores is None:
        persistent.mg_max_scores = [0] * MG_TOTAL
    if persistent.mg_medals is None:
        persistent.mg_medals = [False] * MG_TOTAL
    if persistent.mg_mastery is None:
        persistent.mg_mastery = False

    def mg_report_score(n, score, max_score):
        """Chame ao final de um minigame COM pontuação, antes de mg_complete(n):
        '$ mg_report_score(N, pontos_obtidos, pontos_maximos_possiveis)'.
        Registra o placar da última partida e concede a medalha de perfeição
        (e, se for o caso, a de maestria) quando a pontuação é máxima."""
        persistent.mg_scores[n - 1] = score
        persistent.mg_max_scores[n - 1] = max_score

        if max_score > 0 and score >= max_score:
            persistent.mg_medals[n - 1] = True
            if all(persistent.mg_medals):
                persistent.mg_mastery = True

    def mg_has_medal(n):
        """A medalha de pontuação perfeita do minigame n já foi conquistada?"""
        return persistent.mg_medals[n - 1]


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

    MAP_NODE_COLORS = {"locked": "#3a3a3a", "unlocked": "#2c6e8a", "done": "#2e7d32"}

    def map_node_file(n, state):
        """Nome do PNG a usar para o nó n no estado dado, ou None se não há
        arte real (aí o nó usa o placeholder). 'done' sem arte própria
        reaproveita a 'unlocked'."""
        candidates = [state]
        if state == "done":
            candidates.append("unlocked")
        for st in candidates:
            filename = "node_%d_%s.png" % (n, st)
            if renpy.loadable(MAP_ART_DIR + filename):
                return filename
        return None

    def map_node_image(filename):
        """Arte real de um nó (canvas inteiro 960x540 -> 1920x1080)."""
        return Transform(Image(MAP_ART_DIR + filename, nearest_neighbor=True), zoom=MAP_ZOOM)

    def map_node_placeholder(n, state):
        """Retângulo provisório do nó n (sem colchetes "[...]" no texto: o
        Ren'Py os interpretaria como substituição de variável)."""
        label = "MINIGAME %d\n(%s)" % (n, state.upper())
        return Fixed(
            Solid(MAP_NODE_COLORS[state], xysize=MAP_NODE_SIZE),
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

    def mg_map_sanitize():
        """Garante que o progresso salvo tem o formato esperado (evita erro se
        o persistent foi mexido à mão ou veio de uma versão antiga)."""
        if not isinstance(persistent.mg_unlocked, int) or persistent.mg_unlocked < 1:
            persistent.mg_unlocked = 1
        persistent.mg_unlocked = min(persistent.mg_unlocked, MG_TOTAL)
        for name, default in (("mg_completed", False), ("mg_scores", 0),
                              ("mg_max_scores", 0), ("mg_medals", False)):
            lst = getattr(persistent, name)
            if not isinstance(lst, list):
                lst = []
            lst = list(lst)[:MG_TOTAL] + [default] * (MG_TOTAL - len(lst))
            setattr(persistent, name, lst)


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

    if MAP_SHOW_CONNECTORS:
        for i in range(MG_TOTAL - 1):
            add mg_map_connector(MAP_NODE_POS[i], MAP_NODE_POS[i + 1])

    # Os 10 nós da trilha
    for i in range(MG_TOTAL):

        $ n = i + 1
        $ node_state = mg_node_state(n)
        $ node_file = map_node_file(n, node_state)
        $ node_x, node_y = MAP_NODE_POS[i]
        $ clickable = (node_state != "locked")

        if node_file is not None:
            # ---- Arte real: canvas inteiro, desenhada em (0, 0) ----
            if clickable:
                button:
                    xysize (1920, 1080)
                    background None
                    focus_mask True   # só os pixels opacos do nó respondem
                    action [Play("sound", "audio/sfx_click.ogg"), Return(n)]
                    hovered Function(mg_map_sfx, "hover")
                    add map_node_image(node_file)
            else:
                add map_node_image(node_file)

        else:
            # ---- Placeholder provisório, na posição MAP_NODE_POS ----
            if clickable:
                button:
                    pos (node_x, node_y)
                    anchor (0.5, 0.5)
                    xysize MAP_NODE_SIZE
                    background None
                    action [Play("sound", "audio/sfx_click.ogg"), Return(n)]
                    hovered Function(mg_map_sfx, "hover")
                    add map_node_placeholder(n, node_state)
            else:
                add map_node_placeholder(n, node_state):
                    pos (node_x, node_y)
                    anchor (0.5, 0.5)


## -----------------------------------------------------------------------
## 4) LABEL DO MAPA
##    Ponto de entrada: "jump roadmap" (chamado pelo script.rpy após a intro).
## -----------------------------------------------------------------------
label roadmap:

    $ mg_map_sanitize()

    call screen roadmap_screen
    $ chosen = _return

    # Trava extra: nó bloqueado nunca abre
    if chosen and chosen <= persistent.mg_unlocked:
        # Chama "label minigame_<chosen>_entry" dinamicamente.
        # Esse label mora dentro de minigame<chosen>.rpy e é responsável por
        # mostrar as instruções, rodar o gameplay e chamar mg_complete(chosen).
        call expression ("minigame_%d_entry" % chosen)

    # Volta a mostrar o mapa (com o progresso já atualizado).
    jump roadmap
