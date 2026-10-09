################################################################################
# MINIGAME1.RPY
# Minigame 1: "Taxonomia e identificação do vírus" (AIE / EIAV)
#
# Como funciona:
#   - Esquerda: clicar na imagem troca a MORFOLOGIA (5 opções, só 1 correta).
#   - Direita: cada categoria taxonômica é um botão; cada clique passa para a
#     próxima opção, em ciclo. Cada opção é uma imagem própria (desenhada no
#     Aseprite, com o texto já embutido) — nenhum texto é desenhado pelo jogo.
#   - O minigame termina quando a morfologia E todas as categorias estão certas.
#
# Placeholders de arte:
#   Se o arquivo de imagem NÃO existir em game/images/minigame1/, o jogo mostra
#   automaticamente um retângulo colorido com texto no lugar. Quando você
#   colocar o PNG com o nome certo na pasta, ele passa a ser usado sozinho —
#   não precisa mexer no código.
#
# Pixel art (mesmo esquema do menu principal):
#   Todo PNG real é exibido com zoom 2.0 + nearest neighbor (ver MG1_ZOOM),
#   então cada arquivo deve ser exportado na METADE do tamanho final indicado
#   nos comentários "# IMAGEM:" abaixo. O placeholder já aparece no tamanho
#   final, sem zoom, então nunca fica maior/menor que a arte real.
#
# Este arquivo contém: dados/configuração, funções de lógica, a tela de
# instruções, a screen do gameplay e o "label minigame_1_entry" — o ponto de
# entrada chamado pelo roadmap.rpy quando o jogador clica no nó 1 do mapa.
################################################################################


## -----------------------------------------------------------------------
## 1) CONFIGURAÇÃO, DADOS E LÓGICA
## -----------------------------------------------------------------------
init python:

    # ---- Pasta das artes ------------------------------------------------
    MG1_ART_DIR = "images/minigame1/"

    # ---- Pixel art: mesmo esquema do menu principal (arte a 960x540, ------
    # ---- exibida em 1920x1080 com zoom 2.0 + nearest neighbor) ----------
    # Todo PNG real (não placeholder) deve ser exportado na METADE do
    # tamanho final que ele ocupa na tela — o jogo aplica o zoom sozinho.
    # Ex.: um botão que ocupa 460x72 na tela final deve ser desenhado/exportado
    # a 230x36. O placeholder (enquanto o arquivo não existe) já aparece no
    # tamanho final, sem precisar de zoom.
    MG1_ZOOM = 2.0

    # ---- Posições e tamanhos (tela 1920x1080) — ajuste ao encaixar a arte --
    # Imagem de morfologia (página esquerda do livro). Suas PNGs são canvas
    # cheio (o vírus já vem posicionado dentro do canvas), então aqui NÃO
    # aplicamos nenhum deslocamento extra — a imagem cobre a tela toda e
    # o focus_mask garante que só os pixels coloridos do vírus respondem ao clique.
    MG1_MORPH_POS = (0, 0)
    MG1_MORPH_SIZE = (1920, 1080)

    # Linhas de categorias (página direita do livro).
    # ATENÇÃO: estas 4 constantes só posicionam os PLACEHOLDERS e a marca de
    # teste (MG1_MARK_CORRECT). A arte real das opções é canvas inteiro
    # (960x540, já na posição certa) e IGNORA estes valores. Os nomes das
    # categorias ("Ordem", "Família"...) já estão desenhados no fundo.
    MG1_ROWS_Y0 = 300          # y da primeira linha
    MG1_ROWS_STEP = 100        # distância vertical entre linhas
    MG1_BTN_X = 1400           # x do placeholder que mostra a opção atual
    MG1_BTN_SIZE = (460, 72)   # tamanho do placeholder de cada opção

    # ---- Comportamento --------------------------------------------------
    MG1_MARK_CORRECT = False   # True = pinta de verde a categoria já correta (bom p/ testar)
    MG1_WIN_DELAY = 1.5        # segundos mostrando "correto" antes de encerrar

    # ---- Pontuação (sem timers) -----------------------------------------
    # ERRO = clicar numa opção (ou na morfologia) que JÁ ESTAVA CERTA, tirando-a
    # do lugar. Acertou tudo sem nenhum erro = pontuação máxima (medalha).
    #   0 erros = 100 | 1 = 80 | 2 = 60 | 3 = 40
    #   4 ou mais erros = "Muitos erros!": a rodada acaba na hora e o minigame
    #   NÃO é concluído (nem "done"), é preciso tentar de novo.
    MG1_MAX_SCORE = 100
    MG1_ERROR_PENALTY = 20     # pontos perdidos por erro
    MG1_MAX_ERRORS = 3         # com o 4º erro a rodada falha
    MG1_ERRORS_POS = (900, 60) # contador "Erros: n/3" (texto escrito pelo jogo)
    MG1_FAIL_DELAY = 2.0       # segundos mostrando "muitos erros" antes de sair

    # ---- Morfologia -----------------------------------------------------
    # Arquivos em game/images/minigame1/ (a ordem é a ordem do ciclo de cliques)
    MG1_MORPH_FILES = [
        "morfologia_1.png",
        "morfologia_2.png",
        "morfologia_3.png",
        "morfologia_4.png",
        "morfologia_5.png",
    ]
    MG1_MORPH_CORRECT = 2  # índice (começa em 0) da morfologia correta => morfologia_3.png

    # ---- Categorias taxonômicas ----------------------------------------
    # Cada opção é uma imagem própria (desenhada no Aseprite, já com o texto
    # embutido), em CANVAS INTEIRO 960x540 com a opção já na posição da linha.
    # O nome da categoria ("Ordem", "Família"...) fica no fundo (mg1_bg.png).
    #
    # "files"        = nome dos 5 arquivos PNG, um por opção, nesta ordem.
    # "options_debug" = só o texto que aparece no retângulo placeholder
    #                    enquanto o arquivo .png correspondente não existe
    #                    (não aparece mais quando a arte real estiver lá).
    # "correct"      = índice (começa em 0) da opção certa.
    # (a ordem das categorias aqui é a ordem das linhas na tela)
    MG1_CATEGORIES = [
        {
            "files": ["cat_ordem_1.png", "cat_ordem_2.png", "cat_ordem_3.png", "cat_ordem_4.png", "cat_ordem_5.png"],
            "options_debug": ["Mononegavirales", "Nidovirales", "Ortervirales", "Picornavirales", "Herpesvirales"],
            "correct": 2,
        },
        {
            "files": ["cat_familia_1.png", "cat_familia_2.png", "cat_familia_3.png", "cat_familia_4.png", "cat_familia_5.png"],
            "options_debug": ["Paramyxoviridae", "Flaviviridae", "Herpesviridae", "Retroviridae", "Coronaviridae"],
            "correct": 3,
        },
        {
            "files": ["cat_subfamilia_1.png", "cat_subfamilia_2.png", "cat_subfamilia_3.png", "cat_subfamilia_4.png", "cat_subfamilia_5.png"],
            "options_debug": ["Orthoparamyxovirinae", "Spumaretrovirinae", "Orthoretrovirinae", "Orthocoronavirinae", "Alphaherpesvirinae"],
            "correct": 2,
        },
        {
            "files": ["cat_genero_1.png", "cat_genero_2.png", "cat_genero_3.png", "cat_genero_4.png", "cat_genero_5.png"],
            "options_debug": ["Morbillivirus", "Alpharetrovirus", "Deltaretrovirus", "Lentivirus", "Betaretrovirus"],
            "correct": 3,
        },
        {
            "files": ["cat_especie_1.png", "cat_especie_2.png", "cat_especie_3.png", "cat_especie_4.png", "cat_especie_5.png"],
            "options_debug": ["Equine arteritis virus", "West Nile virus", "Equine infectious anemia virus", "Equine influenza virus", "Human immunodeficiency virus 1"],
            "correct": 2,
        },
        {
            "files": ["cat_afetadas_1.png", "cat_afetadas_2.png", "cat_afetadas_3.png", "cat_afetadas_4.png", "cat_afetadas_5.png"],
            "options_debug": ["Equídeos e bovinos", "Equídeos e suínos", "Equídeos e humanos", "Todos os mamíferos", "Apenas equídeos"],
            "correct": 4,
        },
    ]

    # ---- Placeholders de arte ------------------------------------------
    def mg1_art(filename, size, label, color):
        """Devolve a imagem real (se o arquivo existir), já ampliada 2x com
        nearest neighbor (igual ao menu principal — a arte deve ser exportada
        na metade de "size"), ou um retângulo colorido com texto (placeholder)
        já no tamanho final indicado, caso o arquivo ainda não exista."""
        path = MG1_ART_DIR + filename
        if renpy.loadable(path):
            return Transform(Image(path, nearest_neighbor=True), zoom=MG1_ZOOM)
        return Fixed(
            Solid(color, xysize=size),
            Text(label, size=28, color="#ffffff", xalign=0.5, yalign=0.5,
                 text_align=0.5, xmaximum=size[0] - 20),
            xysize=size,
        )

    def mg1_full_art(filename, rect, label, color):
        """Arte de CANVAS INTEIRO (960x540 → 1920x1080, nearest neighbor,
        desenhada em (0, 0), sem usar posição do código) se o PNG existir.
        Senão, um placeholder: retângulo colorido com texto na posição
        "rect" = (x, y, largura, altura), dentro de um canvas transparente
        de 1920x1080 (assim ele se comporta igual à arte real)."""
        path = MG1_ART_DIR + filename
        if renpy.loadable(path):
            return Transform(Image(path, nearest_neighbor=True), zoom=MG1_ZOOM)
        x, y, w, h = rect
        box = Fixed(
            Solid(color, xysize=(w, h)),
            Text(label, size=28, color="#ffffff", xalign=0.5, yalign=0.5,
                 text_align=0.5, xmaximum=w - 20),
            xysize=(w, h),
        )
        return Fixed(Transform(box, pos=(x, y)), xysize=(1920, 1080))

    def mg1_build_morph_art():
        """Monta a lista de displayables das 5 morfologias (arte real ou placeholder)."""
        colors = ["#7a3b3b", "#3b6a7a", "#5b7a3b", "#6a3b7a", "#7a6a3b"]
        result = []
        for i, filename in enumerate(MG1_MORPH_FILES):
            result.append(mg1_art(filename, MG1_MORPH_SIZE,
                                  "MORFOLOGIA %d\n(%s)" % (i + 1, filename),
                                  colors[i % len(colors)]))
        return result

    def mg1_build_category_art(cat, row):
        """Monta a lista de displayables das 5 opções da categoria da linha
        "row" (arte real de canvas inteiro, com texto já desenhado no Aseprite,
        ou placeholder na posição da linha enquanto o arquivo não existir)."""
        colors = ["#2c4a63", "#3a5a3a", "#5a3a4a", "#5a4a2a", "#3a3a5a"]
        rect = (MG1_BTN_X, MG1_ROWS_Y0 + row * MG1_ROWS_STEP, MG1_BTN_SIZE[0], MG1_BTN_SIZE[1])
        result = []
        for i, filename in enumerate(cat["files"]):
            label = "%s\n(%s)" % (cat["options_debug"][i], filename)
            result.append(mg1_full_art(filename, rect, label, colors[i % len(colors)]))
        return result

    # IMAGEM: minigame1/mg1_bg.png — fundo cheio: livro aberto, mesa, cenário.
    # Tamanho final na tela: 1920x1080 → exporte o PNG a 960x540 (a arte
    # é ampliada 2x automaticamente).
    MG1_BG = mg1_art("mg1_bg.png", (1920, 1080), "FUNDO: livro aberto\n(mg1_bg.png)", "#3b2a1a")

    # IMAGEM: minigame1/mg1_title_panel.png — painel de título no canto superior
    # esquerdo. CANVAS INTEIRO 960x540, com o painel já na posição dele (o
    # retângulo (60, 40, 820, 170) abaixo só posiciona o placeholder).
    MG1_TITLE_PANEL = mg1_full_art("mg1_title_panel.png", (60, 40, 820, 170), "PAINEL DE TÍTULO\n(mg1_title_panel.png)", "#5a3a1c")

    # IMAGEM: minigame1/morfologia_1.png ... morfologia_5.png — imagens que alternam
    # na página esquerda (uma delas é a correta, definida em MG1_MORPH_CORRECT).
    # Tamanho final: 700x700 → exporte cada PNG a 350x350.
    MG1_MORPH_ART = mg1_build_morph_art()

    # IMAGEM: minigame1/cat_<categoria>_1.png ... cat_<categoria>_5.png — as 5
    # opções de CADA categoria (ordem, familia, subfamilia, genero, especie,
    # afetadas), já com o texto da opção desenhado na própria arte.
    # Cada PNG é um CANVAS INTEIRO de 960x540 com a opção já na posição da
    # linha dela (como a morfologia): o jogo amplia 2x e desenha em (0, 0), e
    # focus_mask True faz só os pixels opacos responderem ao clique.
    # O nome da categoria NÃO é desenhado pelo jogo (está no fundo).
    # Nenhum texto é desenhado por cima pelo jogo, nem existe estado de hover
    # separado — o clique só alterna entre as 5 imagens (igual à morfologia).
    MG1_CATEGORY_ART = [mg1_build_category_art(cat, row) for row, cat in enumerate(MG1_CATEGORIES)]

    # IMAGEM: minigame1/mg1_success.png — selo/banner exibido ao acertar tudo.
    # CANVAS INTEIRO 960x540, com o selo já na posição dele (o retângulo
    # (510, 390, 900, 300) só posiciona o placeholder, no centro da tela).
    MG1_SUCCESS = mg1_full_art("mg1_success.png", (510, 390, 900, 300), "CLASSIFICAÇÃO CORRETA!\n(mg1_success.png)", "#2e7d32")

    # IMAGEM: minigame1/mg1_fail.png — banner exibido quando o jogador erra
    # demais (4 erros ou mais). CANVAS INTEIRO 960x540, banner já na posição
    # (o retângulo (510, 390, 900, 300) só posiciona o placeholder).
    MG1_FAIL = mg1_full_art("mg1_fail.png", (510, 390, 900, 300), "MUITOS ERROS!\nTente de novo\n(mg1_fail.png)", "#8a2c2c")

    # ---- Efeitos sonoros (só tocam se o arquivo existir) ---------------
    def mg1_sfx(kind):
        # AUDIO: audio/sfx_hover.ogg, audio/sfx_click.ogg (já usados no menu)
        # AUDIO: audio/sfx_win.ogg — som de acerto final (opcional)
        files = {
            "hover": "audio/sfx_hover.ogg",
            "click": "audio/sfx_click.ogg",
            "win": "audio/sfx_win.ogg",
            "wrong": "audio/sfx_wrong.ogg",
        }
        path = files.get(kind)
        if path and renpy.loadable(path):
            renpy.sound.play(path)


## Estado do minigame (guardado no save / rollback)
default mg1_morph_index = 0   # morfologia atualmente exibida
default mg1_cat_indices = []  # opção atual de cada categoria (mesma ordem de MG1_CATEGORIES)
default mg1_won = False       # True quando tudo estiver correto
default mg1_errors = 0        # erros desta rodada (clicar em algo que já estava certo)
default mg1_failed = False    # True quando errou demais (rodada perdida)


init python:

    def mg1_reset():
        """Prepara uma nova partida: sorteia um ponto de partida ERRADO para
        a morfologia e para cada categoria (o jogador nunca começa já certo)."""
        global mg1_morph_index, mg1_cat_indices, mg1_won, mg1_errors, mg1_failed

        mg1_won = False
        mg1_errors = 0
        mg1_failed = False

        wrong_morphs = [i for i in range(len(MG1_MORPH_FILES)) if i != MG1_MORPH_CORRECT]
        mg1_morph_index = renpy.random.choice(wrong_morphs)

        mg1_cat_indices = []
        for cat in MG1_CATEGORIES:
            wrong = [i for i in range(len(cat["files"])) if i != cat["correct"]]
            mg1_cat_indices.append(renpy.random.choice(wrong))

    def mg1_is_correct(i):
        """A categoria de índice i está na opção certa?"""
        return mg1_cat_indices[i] == MG1_CATEGORIES[i]["correct"]

    def mg1_check_win():
        """Marca vitória se a morfologia e TODAS as categorias estiverem certas."""
        global mg1_won
        if mg1_morph_index != MG1_MORPH_CORRECT:
            return
        for i in range(len(MG1_CATEGORIES)):
            if not mg1_is_correct(i):
                return
        mg1_won = True
        mg1_sfx("win")

    def mg1_register_error():
        """Conta um erro; com o (MG1_MAX_ERRORS + 1)º erro a rodada falha."""
        global mg1_errors, mg1_failed
        mg1_errors += 1
        mg1_sfx("wrong")
        if mg1_errors > MG1_MAX_ERRORS:
            mg1_failed = True

    def mg1_score():
        """Pontuação desta rodada (0 erros = máxima)."""
        return max(0, MG1_MAX_SCORE - mg1_errors * MG1_ERROR_PENALTY)

    def mg1_click_morph():
        """Clique na imagem da esquerda: passa para a próxima morfologia."""
        global mg1_morph_index
        if mg1_won or mg1_failed:
            return
        if mg1_morph_index == MG1_MORPH_CORRECT:
            mg1_register_error()      # tirou do lugar uma morfologia que já estava certa
        mg1_morph_index = (mg1_morph_index + 1) % len(MG1_MORPH_FILES)
        mg1_sfx("click")
        mg1_check_win()

    def mg1_click_category(i):
        """Clique em uma categoria: passa para a próxima opção dela (em ciclo)."""
        if mg1_won or mg1_failed:
            return
        if mg1_is_correct(i):
            mg1_register_error()      # tirou do lugar uma opção que já estava certa
        total = len(MG1_CATEGORIES[i]["files"])
        mg1_cat_indices[i] = (mg1_cat_indices[i] + 1) % total
        mg1_sfx("click")
        mg1_check_win()


## -----------------------------------------------------------------------
## 1.5) TELA DE INSTRUÇÕES
##    Uso: call screen minigame1_instructions
##    Modal: bloqueia qualquer clique no que estiver atrás até "Entendi".
## -----------------------------------------------------------------------
init python:

    # IMAGEM: minigame1/mg1_instructions_bg.png — fundo cheio da tela de
    # instruções. Tamanho final: 1920x1080 → exporte o PNG a 960x540.
    MG1_INSTR_BG = mg1_art("mg1_instructions_bg.png", (1920, 1080),
                            "FUNDO: instruções\n(mg1_instructions_bg.png)", "#2a2418")

    # IMAGEM: minigame1/mg1_instructions_panel.png — moldura do texto de regras,
    # sem texto (o texto é escrito pelo jogo, centralizado em (960, 490), com
    # até 1000 px de largura). CANVAS INTEIRO 960x540, moldura já na posição
    # (o retângulo (360, 190, 1200, 600) só posiciona o placeholder).
    MG1_INSTR_PANEL = mg1_full_art("mg1_instructions_panel.png", (360, 190, 1200, 600),
                                   "MOLDURA DE TEXTO\n(mg1_instructions_panel.png)", "#4a3a20")

    # IMAGEM: minigame1/mg1_close_idle.png e mg1_close_hover.png — botão
    # "Entendi" (texto desenhado). CANVAS INTEIRO 960x540, botão já na posição
    # (o retângulo (840, 860, 240, 80) só posiciona o placeholder).
    MG1_CLOSE_IDLE = mg1_full_art("mg1_close_idle.png", (840, 860, 240, 80), "ENTENDI\n(mg1_close_idle.png)", "#3a5a3a")
    MG1_CLOSE_HOVER = mg1_full_art("mg1_close_hover.png", (840, 860, 240, 80), "ENTENDI\n(mg1_close_hover.png)", "#4f7a4f")

style mg1_instructions_text:
    text_align 0.5
    color "#ffffff"
    size 30
    xsize 1000


screen minigame1_instructions():

    modal True  # impede qualquer clique/interação com o jogo por trás

    add MG1_INSTR_BG

    add MG1_INSTR_PANEL

    # Texto de regras de exemplo — edite conforme as regras reais do minigame
    text _("Regras do Minigame 1:\n\n- Explique aqui o objetivo.\n- Explique aqui os controles.\n- Explique aqui a condição de vitória/derrota.") style "mg1_instructions_text" pos (960, 490) anchor (0.5, 0.5)

    # Botão "Entendi" / "Fechar" — libera o jogador para o minigame (arte de
    # canvas inteiro, ver MG1_CLOSE_IDLE/HOVER acima).
    imagebutton:
        idle MG1_CLOSE_IDLE
        hover MG1_CLOSE_HOVER
        focus_mask True
        action [
            Play("sound", "audio/sfx_click.ogg"),
            Return(True),  # devolve o controle ao "call screen" que a chamou
        ]
        hovered Play("sound", "audio/sfx_hover.ogg")


## -----------------------------------------------------------------------
## 2) TELA DO MINIGAME
## -----------------------------------------------------------------------
screen minigame1_gameplay():

    modal True  # bloqueia qualquer interação com o que estiver atrás

    # Fundo cheio
    add MG1_BG

    # ---- Painel de título / objetivo (canto superior esquerdo) ----------
    # Se a sua arte do painel já tiver o texto desenhado, apague os 2 textos abaixo.
    add MG1_TITLE_PANEL
    text _("1 - TAXONOMIA E IDENTIFICAÇÃO DO VÍRUS"):
        xpos 90
        ypos 65
        size 34
        color "#ffffff"
    text _("Complete todas as características corretas do vírus da AIE."):
        xpos 90
        ypos 135
        size 24
        color "#ffffff"
        xmaximum 760

    # ---- Página esquerda: morfologia (clique para trocar) ---------------
    button:
        pos MG1_MORPH_POS
        xysize MG1_MORPH_SIZE
        background None
        focus_mask True  # só pixels coloridos respondem (útil se a PNG tiver áreas transparentes)
        action Function(mg1_click_morph)
        hovered Function(mg1_sfx, "hover")
        add MG1_MORPH_ART[mg1_morph_index]

    # Posição própria (fixa), já que a morfologia agora é tela cheia e não dá
    # mais pra calcular esta dica "logo abaixo" da imagem. Ajuste livremente.
    text _("Clique na imagem para trocar a morfologia"):
        xpos 260
        ypos 980
        size 24
        color "#ffffff"

    # ---- Página direita: categorias taxonômicas -------------------------
    for i, cat in enumerate(MG1_CATEGORIES):

        $ row_y = MG1_ROWS_Y0 + i * MG1_ROWS_STEP
        $ cat_ok = MG1_MARK_CORRECT and mg1_is_correct(i)

        # (O nome da categoria já está desenhado no fundo — o jogo não escreve.)
        # Botão de CANVAS INTEIRO que mostra a imagem da opção atual (já com o
        # texto desenhado nela, na posição da linha); cada clique avança para a
        # próxima opção, em ciclo — igual à morfologia.
        button:
            xysize (1920, 1080)
            background None
            focus_mask True  # só pixels opacos da arte respondem ao clique
            action Function(mg1_click_category, i)
            hovered Function(mg1_sfx, "hover")
            add MG1_CATEGORY_ART[i][mg1_cat_indices[i]]

        # Marca de "já correto" só para você testar (ative em MG1_MARK_CORRECT).
        # Fica ao lado do botão, sem sobrepor a arte da opção.
        if cat_ok:
            text "✓":
                xpos MG1_BTN_X + MG1_BTN_SIZE[0] + 12
                ypos row_y + 14
                size 34
                color "#1f8f2f"

    # ---- Contador de erros (texto escrito pelo jogo) --------------------
    $ errors_now = mg1_errors
    $ errors_max = MG1_MAX_ERRORS
    text _("Erros: [errors_now]/[errors_max]"):
        pos MG1_ERRORS_POS
        size 32
        color ("#ffb3b3" if mg1_errors > 0 else "#ffffff")

    # ---- Vitória: bloqueia cliques, mostra o selo e encerra sozinho -----
    if mg1_won:
        $ final_score = mg1_score()
        $ final_max = MG1_MAX_SCORE
        button:
            xfill True
            yfill True
            background "#00000088"
            action NullAction()

        add MG1_SUCCESS

        text _("Pontuação: [final_score] / [final_max]"):
            xalign 0.5
            ypos 780
            size 40
            color "#ffffff"

        timer MG1_WIN_DELAY action Return(True)

    # ---- Derrota: erros demais, a rodada acaba e o minigame não conclui ---
    if mg1_failed:
        button:
            xfill True
            yfill True
            background "#00000099"
            action NullAction()

        add MG1_FAIL

        timer MG1_FAIL_DELAY action Return(True)


## -----------------------------------------------------------------------
## 3) LABEL DO GAMEPLAY (motor do minigame em si)
## -----------------------------------------------------------------------
label minigame_1_gameplay:

    $ quick_menu = False       # esconde os botões rápidos do rodapé durante o minigame
    $ renpy.block_rollback()   # impede que o rollback (roda do mouse) bagunce o estado
    $ mg1_reset()              # sorteia o estado inicial (permite rejogar do zero)

    scene black
    call screen minigame1_gameplay   # só retorna quando tudo estiver correto

    $ quick_menu = True
    return


## -----------------------------------------------------------------------
## 4) PONTO DE ENTRADA (chamado pelo roadmap.rpy: "call expression 'minigame_1_entry'")
##    Mostra as instruções, roda o gameplay e avisa o mapa que terminou.
## -----------------------------------------------------------------------
label minigame_1_entry:

    call screen minigame1_instructions
    call minigame_1_gameplay

    # Errou demais (4 ou mais erros): não conclui, volta ao mapa e é só tentar de novo
    if not mg1_failed:
        $ mg_report_score(1, mg1_score(), MG1_MAX_SCORE)  # pontuação máxima = medalha (definido em progress.rpy)
        $ mg_complete(1)  # marca o minigame 1 como concluído e libera o 2

    return
