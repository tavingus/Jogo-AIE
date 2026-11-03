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
#   em 500x340 (sem distorcer).
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
            fill = tuple("{b}{color=#1f6b2a}%s{/color}{/b}" % a for a in answer)
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
                        out.append(Transform(Image(p), xysize=(500, 340), fit="contain"))
                        break
        return out

    NB_TAB_W, NB_TAB_H, NB_TAB_X, NB_TAB_Y0, NB_TAB_STEP = 360, 84, 210, 210, 98

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

    # Folha do caderno
    add Solid("#371f12") pos (160, 80) xysize (1600, 920)
    add Solid("#ecdcb2") pos (166, 86) xysize (1588, 908)
    add Solid("#c9a96e") pos (580, 100) xysize (4, 880)

    text _("Caderno da AIE"):
        pos (210, 110)
        size 48
        bold True
        color "#3a2410"

    $ done = nb_completed()
    $ got_n = len([p for p in NOTEBOOK_PAGES if p["mg"] in done])
    $ tot_n = len(NOTEBOOK_PAGES)
    text "[got_n]/[tot_n]":
        pos (1560, 118)
        size 36
        bold True
        color "#3a2410"

    # Abas (uma por página)
    for i, pg in enumerate(NOTEBOOK_PAGES):
        $ unl = pg["mg"] in done
        $ tab_title = pg["title"] if unl else "???"
        $ tab_no = pg["mg"]
        button:
            pos (NB_TAB_X, NB_TAB_Y0 + i * NB_TAB_STEP)
            xysize (NB_TAB_W, NB_TAB_H)
            background Solid("#568e48" if i == page_n else ("#8a7a5a" if unl else "#a39a85"))
            hover_background Solid("#74b25c" if unl or i == page_n else "#b3aa95")
            action [SetScreenVariable("page_n", i), Function(sfx, "click")]
            hovered Function(sfx, "hover")
            text "[tab_no]. [tab_title!t]":
                xpos 20
                yalign 0.5
                size 28
                color ("#ffffff" if i == page_n else ("#3a2410" if unl else "#5c5444"))

    # Conteúdo da página aberta
    $ pg = NOTEBOOK_PAGES[page_n]
    $ unlocked = pg["mg"] in done
    $ pg_title = pg["title"]
    $ pg_mg = pg["mg"]

    text "[pg_mg]. [pg_title!t]":
        pos (630, 190)
        size 44
        bold True
        color "#3a2410"

    vbox:
        pos (630, 280)
        xmaximum 640
        spacing 26
        for template, answer in pg["items"]:
            $ line = u"\u2022 " + nb_line(template, answer, unlocked)
            text line:
                size 30
                color "#3a2410"
                xmaximum 640

    if not unlocked:
        text _("Conclua o minigame [pg_mg] para preencher esta página."):
            pos (630, 860)
            size 26
            italic True
            color "#6a4a22"
            xmaximum 640

    # Imagens reais (opcional)
    $ imgs = nb_images(pg_mg, unlocked)
    vbox:
        pos (1230, 280)
        spacing 24
        for im in imgs:
            add im

    imagebutton:
        idle ACH_BACK_IDLE
        hover ACH_BACK_HOVER
        focus_mask True
        action [Function(sfx, "window_close"), Hide("notebook_screen")]
        hovered Play("sound", "audio/sfx_hover.ogg")


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
