################################################################################
# PROGRESS.RPY
# Progresso do jogo e conquistas (AMBOS POR SAVE) e aviso de conquista.
#
# Modelo de dados:
#   - PROGRESSO e CONQUISTAS são por save: quais minigames estão liberados /
#     concluídos, a melhor pontuação de cada um, as medalhas (nó "perfect") e as
#     conquistas. São variáveis "default" normais, então vão para dentro do
#     arquivo de save. "Novo jogo" começa TUDO do zero (inclusive as
#     conquistas); "Continuar" carrega o save mais recente.
#   - No MENU PRINCIPAL ainda não há jogo carregado, então a tela "Conquistas"
#     mostra as conquistas do save mais recente (o mesmo do "Continuar"). Para
#     isso, a lista de conquistas também é gravada dentro do save (json).
#
# API usada pelos minigames (NÃO mudou):
#     $ mg_report_score(N, pontos, pontos_maximos)   # minigames com pontuação
#     $ mg_complete(N)                                # marca concluído, libera N+1
#
# Saves: o jogo salva sozinho (autosave) toda vez que o mapa é mostrado — nunca
# dentro de um minigame (isso evita salvar no meio de timers e telas modais).
################################################################################


## -----------------------------------------------------------------------
## 1) CONFIGURAÇÃO GERAL
## -----------------------------------------------------------------------
init python:

    MG_TOTAL = 10        # nós no mapa
    MG_IMPLEMENTED = 7   # minigames que já existem; os nós 8 a 10 ficam
                         # bloqueados ("em breve") até você aumentar este número

    # Só salvamos de propósito (no mapa), então desligamos o autosave por
    # frequência de interações do Ren'Py.
    config.autosave_frequency = None


## -----------------------------------------------------------------------
## 2) PROGRESSO POR SAVE
## -----------------------------------------------------------------------
default mg_unlocked = 1                   # minigame mais avançado já liberado
default mg_completed = [False] * MG_TOTAL # concluído ao menos uma vez
default mg_scores = [0] * MG_TOTAL        # MELHOR pontuação neste save
default mg_max_scores = [0] * MG_TOTAL    # pontuação máxima possível (informada pelo minigame)
default mg_medals = [False] * MG_TOTAL    # tirou a pontuação máxima neste save (nó "perfect")

init python:

    def mg_complete(n):
        """Chame ao final de cada minigame: '$ mg_complete(N)'.
        Marca o minigame N como concluído e libera o N+1 (até MG_IMPLEMENTED)."""
        store.mg_completed[n - 1] = True
        if store.mg_unlocked == n:
            store.mg_unlocked = min(n + 1, MG_IMPLEMENTED)

    def mg_report_score(n, score, max_score):
        """Chame ao final de um minigame COM pontuação, antes de mg_complete(n).
        Guarda a melhor pontuação do save e, se for a máxima, concede a medalha
        (nó "perfect") e as conquistas correspondentes. A medalha, uma vez
        conquistada, nunca se perde."""
        store.mg_max_scores[n - 1] = max_score
        store.mg_scores[n - 1] = max(store.mg_scores[n - 1], score)

        if max_score > 0 and score >= max_score:
            store.mg_medals[n - 1] = True
            new = []
            if ach_unlock("mg%d" % n):
                new.append("mg%d" % n)
            if ach_all_perfect() and ach_unlock("final"):
                new.append("final")
            ach_notify(new)

    def mg_has_medal(n):
        return store.mg_medals[n - 1]

    def mg_medal_count():
        return sum(1 for n in range(1, MG_IMPLEMENTED + 1) if store.mg_medals[n - 1])

    def mg_node_state(n):
        """'locked' / 'unlocked' / 'done' / 'perfect' para o nó do minigame n."""
        if n > MG_IMPLEMENTED or n > store.mg_unlocked:
            return "locked"
        if store.mg_medals[n - 1]:
            return "perfect"
        if store.mg_completed[n - 1]:
            return "done"
        return "unlocked"


## -----------------------------------------------------------------------
## 3) CONQUISTAS (GLOBAIS)
## -----------------------------------------------------------------------
default ach_unlocked = {}   # conquistas deste save: {"mg1": True, ...}

init python:

    # "fact" = frase "Você sabia?" mostrada quando a conquista é desbloqueada.
    # Para criar as conquistas dos minigames 8 a 10: acrescente aqui um item
    # {"id": "mg8", ...} e aumente MG_IMPLEMENTED.
    ACH_LIST = [
        {"id": "mg1", "name": _("Nome e Sobrenome"),
         "desc": _("Classificou o vírus da AIE sem errar nada."),
         "fact": _("A AIE é causada por um lentivírus da família Retroviridae.")},
        {"id": "mg2", "name": _("Olho Clínico"),
         "desc": _("Marcou todos os sinais certos no exame clínico."),
         "fact": _("Febre recorrente, anemia e perda de peso são sinais clássicos, mas há portadores sem nenhum sinal.")},
        {"id": "mg3", "name": _("Mão Firme"),
         "desc": _("Fez a coleta de sangue sem nenhum erro."),
         "fact": _("Para a sorologia usa-se tubo sem anticoagulante: o soro é a amostra do exame.")},
        {"id": "mg4", "name": _("Mestre do Coggins"),
         "desc": _("Leu o IDGA e o ELISA com pontuação máxima."),
         "fact": _("O IDGA (teste de Coggins) é o teste oficial de referência; o ELISA é mais sensível e usado em triagem.")},
        {"id": "mg5", "name": _("Porteira Fechada"),
         "desc": _("Mandou todos os cavalos para o destino certo."),
         "fact": _("Cavalo positivo exige notificação ao serviço veterinário oficial (MAPA).")},
        {"id": "mg6", "name": _("Zumbido Zero"),
         "desc": _("Não errou nenhuma mosca."),
         "fact": _("Mutucas e mosca-dos-estábulos transmitem o vírus de forma mecânica, pelo sangue na picada.")},
        {"id": "mg7", "name": _("Uma Agulha por Cavalo"),
         "desc": _("Nenhuma picada com agulha reutilizada."),
         "fact": _("Reutilizar agulha pode passar o vírus de um animal para outro: é a transmissão iatrogênica.")},
        {"id": "final", "name": _("Salvou Equinópolis"),
         "desc": _("Pontuação máxima em todos os desafios."),
         "fact": _("Sem cura e sem vacina, a prevenção é a única defesa contra a AIE.")},
    ]
    ACH_BY_ID = dict((a["id"], a) for a in ACH_LIST)

    def ach_state():
        """Conquistas a mostrar: as do jogo em andamento ou, no menu principal
        (sem jogo carregado), as do save mais recente."""
        if getattr(store, "main_menu", False):
            slot = prog_newest_slot()
            info = renpy.slot_json(slot) if slot is not None else None
            return dict((aid, True) for aid in (info or {}).get("achievements", []))
        return store.ach_unlocked

    def ach_is_unlocked(aid):
        return bool(ach_state().get(aid))

    def ach_count():
        return sum(1 for a in ACH_LIST if ach_is_unlocked(a["id"]))

    def ach_all_perfect():
        """Todas as conquistas de minigame (mg1..mgN) já foram desbloqueadas?"""
        return all(ach_is_unlocked("mg%d" % n) for n in range(1, MG_IMPLEMENTED + 1))

    def ach_unlock(aid):
        """Desbloqueia a conquista. Devolve True só na PRIMEIRA vez."""
        if store.ach_unlocked.get(aid):
            return False
        store.ach_unlocked[aid] = True
        return True

    def ach_notify(ids):
        """Mostra o aviso 'Conquista desbloqueada!' (tela ach_toast)."""
        if ids:
            renpy.show_screen("ach_toast", ids=list(ids))
            renpy.sound.play("audio/sfx_correct.ogg") if renpy.loadable("audio/sfx_correct.ogg") else None

    def ach_icon(aid, unlocked):
        """Ícone da conquista: images/ach/ach_<id>.png (a arte) ou None."""
        path = "images/ach/ach_%s%s.png" % (aid, "" if unlocked else "_locked")
        if renpy.loadable(path):
            return Transform(Image(path, nearest_neighbor=True), zoom=2.0)
        return None

    # ---- Posições dos PLACEHOLDERS / textos (tela 1920x1080) ---------------
    # Aviso discreto no canto inferior DIREITO (estilo Steam/PlayStation):
    # pequeno, entra deslizando, some sozinho. Só mostra o nome da conquista
    # (a descrição está na tela Conquistas).
    ACH_TOAST_RECT = (1480, 968, 400, 72)      # (x, y, largura, altura) do placeholder
    ACH_TOAST_NAME_POS = (1566, 998)           # onde o jogo escreve o nome
    ACH_TOAST_NAME_W = 300
    ACH_TOAST_STEP = 84                        # distância entre avisos empilhados (para cima)
    ACH_TOAST_TIME = 4.0                       # segundos na tela
    ACH_PANEL_RECT = (200, 90, 1520, 900)      # janela de conquistas
    ACH_BACK_RECT = (760, 892, 400, 70)
    ACH_COUNTER_POS = (1480, 120)
    ACH_GRID_X = 250
    ACH_GRID_Y = 190
    ACH_ROW_DX = 740                           # distância entre as 2 colunas
    ACH_ROW_DY = 175                           # distância entre as linhas
    ACH_ROW_SIZE = (700, 160)

    # IMAGEM: ach_toast.png — moldura do aviso de conquista, pequena (com o
    #   ícone e o texto fixo "CONQUISTA DESBLOQUEADA" já desenhados; o nome da
    #   conquista é escrito pelo jogo). Canvas 960x540.
    # IMAGEM: ach_panel.png — janela de conquistas (título "CONQUISTAS" já
    #   desenhado). Canvas 960x540.
    # IMAGEM: ach_back_idle.png / ach_back_hover.png — botão VOLTAR. Canvas 960x540.
    # IMAGEM (opcional): ach/ach_<id>.png e ach/ach_<id>_locked.png — ícone de
    #   cada conquista (<id> = mg1 ... mg7, final), 96x96 (ampliado 2x: 48x48
    #   na arte), posicionado pelo código no canto esquerdo de cada linha.
    ACH_TOAST_ART = menu_opt_art("ach_toast.png", ACH_TOAST_RECT, "CONQUISTA DESBLOQUEADA\n(ach_toast.png)", "#2a2f3a")
    ACH_PANEL_ART = menu_opt_art("ach_panel.png", ACH_PANEL_RECT, "CONQUISTAS\n(ach_panel.png)", "#7a5a3a")
    ACH_BACK_IDLE = menu_opt_art("ach_back_idle.png", ACH_BACK_RECT, "VOLTAR", "#a54a3e")
    ACH_BACK_HOVER = menu_opt_art("ach_back_hover.png", ACH_BACK_RECT, "VOLTAR", "#c8604f")


## Entrada/saída do aviso: desliza da direita com fade (e sai do mesmo jeito).
## "delay" escalona os avisos quando há mais de um ao mesmo tempo.
transform ach_toast_slide(delay=0.0):
    on show:
        xoffset 460
        alpha 0.0
        pause delay
        easeout 0.35 xoffset 0 alpha 1.0
    on hide:
        easein 0.3 xoffset 460 alpha 0.0


## Aviso de conquista desbloqueada (discreto, some sozinho).
## "ids" = conquistas novas; se houver mais de uma, empilham para cima.
screen ach_toast(ids):

    zorder 250

    for i, aid in enumerate(ids):
        $ a_name = ACH_BY_ID[aid]["name"]
        fixed at ach_toast_slide(i * 0.25):
            add Transform(ACH_TOAST_ART, yoffset=-i * ACH_TOAST_STEP)
            text "[a_name!t]":
                pos (ACH_TOAST_NAME_POS[0], ACH_TOAST_NAME_POS[1] - i * ACH_TOAST_STEP)
                size 26
                bold True
                color "#ffe9a3"
                xmaximum ACH_TOAST_NAME_W

    timer ACH_TOAST_TIME action Hide("ach_toast")


## Tela "Conquistas" (aberta pelo botão do menu principal).
screen achievements_screen():

    modal True
    zorder 150

    add Solid("#000000bb")

    # Esc / botão direito = voltar
    key "game_menu" action [Function(sfx, "window_close"), Hide("achievements_screen")]

    add ACH_PANEL_ART

    $ ach_got = ach_count()
    $ ach_total = len(ACH_LIST)

    text "[ach_got]/[ach_total]":
        pos ACH_COUNTER_POS
        size 36
        bold True
        color "#3a2410"

    for idx, a in enumerate(ACH_LIST):

        $ got = ach_is_unlocked(a["id"])
        $ rx = ACH_GRID_X + (idx % 2) * ACH_ROW_DX
        $ ry = ACH_GRID_Y + (idx // 2) * ACH_ROW_DY
        $ a_name = a["name"]
        $ a_desc = a["desc"]
        $ a_fact = a["fact"]
        $ a_icon = ach_icon(a["id"], got)

        fixed:
            pos (rx, ry)
            xysize ACH_ROW_SIZE

            add Solid("#371f12", xysize=ACH_ROW_SIZE)
            add Solid(("#ecdcb2" if got else "#9a8f7a"), xysize=(ACH_ROW_SIZE[0] - 6, ACH_ROW_SIZE[1] - 6)) pos (3, 3)

            # Ícone: arte (se existir) ou uma estrela / interrogação provisória
            if a_icon is not None:
                add a_icon pos (24, 32)
            else:
                text ("★" if got else "?"):
                    font "DejaVuSans.ttf"
                    pos (32, 28)
                    size 84
                    color ("#d9a520" if got else "#5c5444")

            text "[a_name!t]":
                pos (150, 12)
                size 30
                bold True
                color ("#3a2410" if got else "#4a4234")

            text "[a_desc!t]":
                pos (150, 52)
                size 22
                color ("#3a2410" if got else "#4a4234")
                xmaximum 530

            if got:
                text "[a_fact!t]":
                    pos (150, 100)
                    size 18
                    italic True
                    color "#6a4a22"
                    xmaximum 530

    imagebutton:
        idle ACH_BACK_IDLE
        hover ACH_BACK_HOVER
        focus_mask True
        action [Function(sfx, "window_close"), Hide("achievements_screen")]
        hovered Play("sound", "audio/sfx_hover.ogg")


## -----------------------------------------------------------------------
## 4) CONTINUAR / AUTOSAVE
##
## O botão CONTINUAR só considera saves criados por ESTA versão do jogo (eles
## levam uma marca "prog_version"). Isso evita o crash de carregar saves
## antigos/incompatíveis ou os slots internos do Ren'Py (ex.: "_reload-1",
## criado ao recarregar o jogo com Shift+R no modo desenvolvedor).
## -----------------------------------------------------------------------
init python:

    PROG_VERSION = 2   # aumente se mudar a estrutura do save e quiser invalidar os antigos
    PROG_SLOT_RE = r"(auto-\d+|quick-\d+|\d+-\d+)$"   # só autosaves, quicksaves e saves manuais

    def _prog_save_json(d):
        """Marca todo save criado por esta versão do jogo e guarda a lista de
        conquistas dele (para a tela Conquistas do menu principal)."""
        d["prog_version"] = PROG_VERSION
        d["achievements"] = sorted(k for k, v in store.ach_unlocked.items() if v)

    config.save_json_callbacks.append(_prog_save_json)

    def prog_newest_slot():
        """Slot do save válido mais recente, ou None se não houver nenhum."""
        best, best_time = None, -1
        for slot in renpy.list_slots(PROG_SLOT_RE):
            info = renpy.slot_json(slot)
            if not info or info.get("prog_version") != PROG_VERSION:
                continue
            t = renpy.slot_mtime(slot) or 0
            if t > best_time:
                best, best_time = slot, t
        return best

    def prog_has_save():
        """Existe algum save válido para o botão 'Continuar'?"""
        return prog_newest_slot() is not None

    def prog_continue():
        """Carrega o save válido mais recente (o autosave do mapa, ou um manual)."""
        slot = prog_newest_slot()
        if slot is None:
            renpy.notify(_("Nenhum jogo salvo encontrado."))
            return
        renpy.load(slot)

    def prog_autosave():
        """Salva o jogo (chamado sempre que o mapa aparece)."""
        renpy.force_autosave(take_screenshot=False)
