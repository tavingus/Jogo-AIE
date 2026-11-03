################################################################################
# NOTEBOOK.RPY
# Caderno de anotações sobre a AIE (aberto pelo botão CADERNO do menu principal)
# e tela "Sobre" (créditos).
#
# Como funciona o caderno:
#   - Tem uma página por minigame. Cada página tem frases com LACUNAS
#     (ex.: "O vírus da AIE pertence à ordem ________").
#   - A página do minigame N só revela as respostas depois que o minigame N
#     foi CONCLUÍDO (independente da pontuação). Antes disso as lacunas ficam
#     em branco e aparece "Conclua o minigame N para preencher".
#   - Como no menu ainda não há jogo carregado, ele lê o progresso do save mais
#     recente (o mesmo do "Continuar"); o progresso é gravado no save (json),
#     igual às conquistas.
#
# COMO EDITAR O CONTEÚDO: mexa só na lista NOTEBOOK_PAGES abaixo.
#   Cada frase é (texto, resposta). Use %s no lugar da lacuna.
#   Para IMAGENS reais, coloque PNG/JPG em game/images/notebook/ com o nome
#   pagina_<N>_1.png, pagina_<N>_2.png (N = número do minigame). Elas aparecem
#   na coluna da direita, só depois de a página ser desbloqueada, encaixadas
#   em 600x300 (sem distorcer).
################################################################################

init python:

    NOTEBOOK_PAGES = [
        {"mg": 1, "title": _("O vírus"),
         "items": [
            (_("A AIE é causada pelo vírus da Anemia Infecciosa Equina (EIAV), da ordem %s."), "Ortervirales"),
            (_("Ele pertence à família %s, subfamília %s."), ("Retroviridae", "Orthoretrovirinae")),
            (_("O gênero é %s, o mesmo grupo do HIV, mas o EIAV não infecta humanos."), "Lentivirus"),
            (_("Afeta apenas %s: cavalos, asininos e muares."), "equídeos"),
         ]},
        {"mg": 2, "title": _("Sinais clínicos"),
         "items": [
            (_("Sinais clássicos: %s em episódios recorrentes, mucosas pálidas e petéquias."), "febre"),
            (_("Também há linfonodos aumentados, letargia, fraqueza e %s."), "perda de peso"),
            (_("No hemograma aparecem anemia e %s (plaquetas baixas)."), "trombocitopenia"),
            (_("Muitos animais não mostram sinal nenhum: são os %s."), "portadores inaparentes"),
         ]},
        {"mg": 3, "title": _("Coleta de sangue"),
         "items": [
            (_("Para a sorologia usa-se tubo %s, porque o exame precisa do soro."), "sem anticoagulante"),
            (_("O sangue é colhido da veia %s."), "jugular"),
            (_("A amostra deve ser identificada e seguir ao laboratório em caixa %s."), "refrigerada"),
         ]},
        {"mg": 4, "title": _("Diagnóstico"),
         "items": [
            (_("O teste oficial de referência é o %s, também chamado de teste de Coggins."), "IDGA"),
            (_("O IDGA detecta principalmente o anticorpo anti-%s, do capsídeo do vírus."), "p26"),
            (_("No IDGA, o resultado positivo aparece como uma linha de %s no gel de ágar."), "precipitação"),
            (_("O %s é um teste mais sensível, lido por densidade óptica, usado em triagem."), "ELISA"),
         ]},
        {"mg": 5, "title": _("Trânsito de animais"),
         "items": [
            (_("Só viaja cavalo com exame negativo dentro da validade de %s dias."), str(getattr(store, "MG5_VALIDITY_DAYS", 60))),
            (_("Exame negativo vencido: é preciso fazer uma %s."), "nova coleta"),
            (_("Cavalo positivo: é obrigatório %s ao serviço veterinário oficial (MAPA)."), "notificar"),
         ]},
        {"mg": 6, "title": _("Transmissão por insetos"),
         "items": [
            (_("O vírus é transmitido de forma %s, pelo sangue que fica na boca do inseto."), "mecânica"),
            (_("Os principais vetores são as %s e as moscas-dos-estábulos."), "mutucas"),
            (_("Só insetos %s (que picam e sugam sangue) transmitem a AIE."), "hematófagos"),
         ]},
        {"mg": 7, "title": _("Transmissão iatrogênica"),
         "items": [
            (_("Reutilizar %s e instrumentos contaminados passa o vírus de um cavalo para outro."), "agulhas"),
            (_("Essa forma de transmissão, causada por procedimentos veterinários, chama-se %s."), "iatrogênica"),
            (_("A AIE não tem cura nem vacina: a única defesa é a %s."), "prevenção"),
         ]},
    ]

    NOTEBOOK_BLANK = "________"

    def nb_completed():
        """Lista de minigames concluídos: do jogo em andamento ou, no menu
        principal, do save mais recente."""
        if getattr(store, "main_menu", False):
            slot = prog_newest_slot()
            info = renpy.slot_json(slot) if slot is not None else None
            return list((info or {}).get("completed", []))
        return [i + 1 for i, v in enumerate(store.mg_completed) if v]

    def nb_line(template, answer, unlocked):
        """Frase da página com a lacuna em branco ou preenchida."""
        if not isinstance(answer, tuple):
            answer = (answer,)
        if unlocked:
            fill = tuple("{b}{color=#1f3f8f}%s{/color}{/b}" % a for a in answer)
        else:
            fill = tuple(NOTEBOOK_BLANK for a in answer)
        return template % fill

    def nb_images(n, unlocked):
        """Imagens reais da página (opcional), só quando desbloqueada."""
        out = []
        if unlocked:
            for k in (1, 2):
                for ext in ("png", "jpg", "jpeg", "webp"):
                    p = "images/notebook/pagina_%d_%d.%s" % (n, k, ext)
                    if renpy.loadable(p):
                        out.append(Transform(Image(p), xysize=(600, 300), fit="contain"))
                        break
        return out

    NB_TAB_COLORS = ["#d9534f", "#e8a43a", "#e0c83a", "#58a55c", "#4a90c8", "#8a63c0", "#d8648e"]
    # IMAGEM: notebook_panel.png — o caderno aberto (canvas 960x540). O jogo
    # escreve os textos por cima: página esquerda x 96-932, direita x 948-1784
    # (tela 1920x1080), margens vermelhas em x 160 e 1012.
    NB_PANEL_ART = menu_opt_art("notebook_panel.png", (60, 48, 1760, 984), "CADERNO\n(notebook_panel.png)", "#ecdcb2")

    ABOUT_TITLE = _("Sobre")
    ABOUT_LINES = [
        _("Proteja Equinópolis"),
        _("Jogo educativo sobre a Anemia Infecciosa Equina (AIE)."),
        _("(texto dos créditos em breve)"),
    ]


screen notebook_screen():

    modal True
    zorder 150

    default page_n = 0

    add Solid("#000000bb")
    key "game_menu" action [Function(sfx, "window_close"), Hide("notebook_screen")]
    key "K_LEFT" action [SetScreenVariable("page_n", max(0, page_n - 1)), Function(sfx, "click")]
    key "K_RIGHT" action [SetScreenVariable("page_n", min(len(NOTEBOOK_PAGES) - 1, page_n + 1)), Function(sfx, "click")]

    # O caderno aberto (arte: images/notebook_panel.png; canvas 960x540)
    add NB_PANEL_ART

    $ done = nb_completed()
    $ got_n = len([q for q in NOTEBOOK_PAGES if q["mg"] in done])
    $ tot_n = len(NOTEBOOK_PAGES)
    $ pg = NOTEBOOK_PAGES[page_n]
    $ unlocked = pg["mg"] in done
    $ pg_title = pg["title"]
    $ pg_mg = pg["mg"]
    $ pg_no = page_n + 1

    # ---- Página da ESQUERDA: título, imagens ------------------------------
    text "Minigame [pg_mg]":
        pos (190, 112)
        size 24
        color "#8a5a30"
    if unlocked:
        text "[pg_title!t]":
            pos (190, 144)
            size 50
            bold True
            color "#1f3f8f"
            xmaximum 700
        text _("ANOTADO!"):
            pos (640, 880)
            size 54
            bold True
            color "#2e7d32"
            outlines [(2, "#ffffff88", 0, 0)]
            at Transform(rotate=-10)
        $ imgs = nb_images(pg_mg, True)
        vbox:
            pos (190, 250)
            spacing 24
            for im in imgs:
                add im
        if not imgs and config.developer:
            text _("(coloque aqui as imagens: images/notebook/pagina_[pg_mg]_1.png)"):
                pos (190, 300)
                size 22
                italic True
                color "#8a5a30"
                xmaximum 700
    else:
        text "???":
            pos (190, 144)
            size 60
            bold True
            color "#9a9078"
        text _("Página em branco.\nConclua o minigame [pg_mg] para anotar aqui o que você aprendeu."):
            pos (190, 300)
            size 30
            italic True
            color "#6a5a40"
            xmaximum 640

    # ---- Página da DIREITA: as anotações com lacunas -----------------------
    text _("Anotações [got_n]/[tot_n]"):
        pos (1030, 100)
        size 22
        color "#8a5a30"
    vbox:
        pos (1030, 180)
        spacing 30
        for template, answer in pg["items"]:
            $ line = u"\u2022 " + nb_line(template, answer, unlocked)
            text line:
                size 30
                color "#2a2a3a"
                xmaximum 700

    if not unlocked:
        text _("Conclua o minigame [pg_mg] para preencher as lacunas."):
            pos (1030, 900)
            size 24
            italic True
            color "#b04a3a"
            xmaximum 700

    # ---- Virar página -------------------------------------------------------
    if page_n > 0:
        button:
            pos (170, 940)
            xysize (200, 56)
            background Solid("#7a5a3a")
            hover_background Solid("#9a7448")
            action [SetScreenVariable("page_n", page_n - 1), Function(sfx, "click")]
            hovered Function(sfx, "hover")
            text _("< Anterior"):
                align (0.5, 0.5)
                size 26
                color "#ffffff"
    if page_n < tot_n - 1:
        button:
            pos (1560, 940)
            xysize (200, 56)
            background Solid("#7a5a3a")
            hover_background Solid("#9a7448")
            action [SetScreenVariable("page_n", page_n + 1), Function(sfx, "click")]
            hovered Function(sfx, "hover")
            text _("Próxima >"):
                align (0.5, 0.5)
                size 26
                color "#ffffff"
    text "[pg_no]/[tot_n]":
        xalign 0.5
        ypos 960
        size 26
        color "#6a5a40"

    # ---- Marcadores (abas coloridas na borda direita) ----------------------
    for i, q in enumerate(NOTEBOOK_PAGES):
        $ tab_unl = q["mg"] in done
        $ tab_no = q["mg"]
        $ tab_col = NB_TAB_COLORS[i % len(NB_TAB_COLORS)] if tab_unl else "#9a9484"
        button:
            pos ((1790 if i == page_n else 1822), 130 + i * 92)
            xysize ((100 if i == page_n else 68), 76)
            background Solid("#371f12")
            action [SetScreenVariable("page_n", i), Function(sfx, "click")]
            hovered Function(sfx, "hover")
            add Solid(tab_col) pos (3, 3) xysize ((94 if i == page_n else 62), 70)
            text "[tab_no]":
                align (0.5, 0.5)
                size 34
                bold True
                color "#ffffff"
                outlines [(2, "#371f12", 0, 0)]

    # ---- Fechar ---------------------------------------------------------------
    button:
        pos (1822, 940)
        xysize (68, 68)
        background Solid("#371f12")
        action [Function(sfx, "window_close"), Hide("notebook_screen")]
        hovered Function(sfx, "hover")
        add Solid("#a54a3e") pos (3, 3) xysize (62, 62)
        text "X":
            align (0.5, 0.5)
            size 38
            bold True
            color "#ffffff"


screen about_screen():

    modal True
    zorder 150

    add Solid("#000000bb")
    key "game_menu" action [Function(sfx, "window_close"), Hide("about_screen")]

    add Solid("#371f12") pos (460, 200) xysize (1000, 680)
    add Solid("#ecdcb2") pos (466, 206) xysize (988, 668)

    text ABOUT_TITLE:
        xalign 0.5
        ypos 240
        size 52
        bold True
        color "#3a2410"

    vbox:
        xalign 0.5
        ypos 360
        spacing 30
        for ln in ABOUT_LINES:
            text ln:
                xalign 0.5
                text_align 0.5
                size 32
                color "#3a2410"
                xmaximum 880

    imagebutton:
        idle ACH_BACK_IDLE
        hover ACH_BACK_HOVER
        focus_mask True
        action [Function(sfx, "window_close"), Hide("about_screen")]
        hovered Play("sound", "audio/sfx_hover.ogg")
