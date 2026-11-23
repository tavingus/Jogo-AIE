################################################################################
# STORY.RPY
# A HISTÓRIA que costura os desafios: o caso do Golias da Natureza.
#
#   - Antes de cada desafio (só na PRIMEIRA vez que o jogador entra nele)
#     aparece uma cena curta, com a mesma caixa de texto da introdução, sobre
#     o fundo do próprio minigame. Ao CONCLUIR o desafio, uma cena de
#     fechamento aparece quando o jogador volta ao mapa.
#   - O nó 8 do mapa (troféu) é o FINAL: libera ao concluir o desafio 7 e
#     mostra o epílogo, o resumo do desempenho e os créditos.
#   - No menu principal, o botão HISTÓRIA abre a galeria de cenas já vistas,
#     para rever (cada cena aparece como um ícone; as não vistas ficam com "?").
#
# COMO EDITAR: os textos estão em STORY_TEXTS (cada item = uma fala do
# narrador, uma "página" da caixa de texto). Mantenha as falas curtas.
################################################################################

default story_seen = {}     # cenas já vistas NESTE jogo: {"mg1_pre": True, ...}
default final_seen = False  # o jogador já viu o final?

init python:

    MG_FINAL = MG_IMPLEMENTED + 1     # nó do mapa que abre o final (8)

    STORY_TEXTS = {
        "mg1_pre": [
            _("Um alerta chegou à prefeitura de Equinópolis: casos de Anemia Infecciosa Equina nas cidades vizinhas."),
            _("Antes de agir, é preciso conhecer o inimigo. Que vírus é esse?"),
        ],
        "mg1_post": [
            _("Um lentivírus que fica no cavalo para sempre. Agora você sabe com quem está lidando."),
        ],
        "mg2_pre": [
            _("O telefone toca: o Trovão, cavalo do sítio vizinho ao haras do Golias da Natureza, está abatido e com febre."),
            _("Hora do exame clínico. O que nele combina com a AIE?"),
        ],
        "mg2_post": [
            _("Os sinais levantam a suspeita, mas só o laboratório confirma."),
            _("E o Golias, o campeão da cidade, que divide a cerca com o Trovão?"),
        ],
        "mg3_pre": [
            _("O Golias vai viajar para uma competição. Com um caso suspeito ao lado, o exame de AIE é obrigatório."),
            _("Você vai colher a amostra. Cada detalhe conta."),
        ],
        "mg3_post": [
            _("Amostra identificada e enviada ao laboratório. Agora é esperar o resultado."),
        ],
        "mg4_pre": [
            _("As amostras do Golias e dos animais vizinhos chegaram ao laboratório."),
            _("Hora de ler os testes."),
        ],
        "mg4_post": [
            _("O Golias está negativo e pode viajar. O Trovão, não: a doença chegou a Equinópolis."),
        ],
        "mg5_pre": [
            _("Dia de embarque para a competição. Nenhum animal sai sem a documentação certa."),
        ],
        "mg5_post": [
            _("Só viajou quem podia. O caso positivo foi notificado ao serviço veterinário oficial."),
        ],
        "mg6_pre": [
            _("Com um positivo na região, as mutucas passam a ser o maior perigo."),
            _("Proteja os cavalos que ficaram."),
        ],
        "mg6_post": [
            _("Menos insetos, menos risco. Mas o vírus ainda tem outra porta de entrada..."),
        ],
        "mg7_pre": [
            _("Dia de vacinar o plantel, e alguém quer economizar agulhas."),
        ],
        "mg7_post": [
            _("Uma agulha por cavalo. A cadeia de transmissão foi quebrada."),
            _("Siga até a bandeira no mapa: Equinópolis espera por você."),
        ],
        "final": [
            _("Semanas depois, o Golias da Natureza voltou da competição com o troféu, e com o exame em dia."),
            _("O Trovão foi notificado e o surto não passou da cerca: nenhum outro cavalo de Equinópolis adoeceu."),
            _("Sem cura e sem vacina, a AIE só é vencida com conhecimento, exame e prevenção. Equinópolis está protegida, graças a você."),
        ],
    }

    def story_bg(n):
        """Fundo da cena do capítulo n (0 = introdução, 1..7 = desafios,
        MG_FINAL = final)."""
        if n == 0 or n == MG_FINAL:
            return INTRO_ART[0]
        return {1: MG1_BG, 2: MG2_BG, 3: MG3_BG, 4: MG4_BG["dock"],
                5: MG5_BG, 6: MG6_BG, 7: MG7_BG}[n]

    def story_mark(sid):
        store.story_seen[sid] = True

    def story_pending_post():
        """Primeiro desafio concluído cuja cena de fechamento ainda não foi vista."""
        for n in range(1, MG_IMPLEMENTED + 1):
            if store.mg_completed[n - 1] and not store.story_seen.get("mg%d_post" % n):
                return n
        return None

    # ---- Galeria (menu principal) ------------------------------------------
    STORY_CHAPTERS = [(0, _("Introdução"))] + \
        [(n, _("Desafio %d") % n) for n in range(1, MG_IMPLEMENTED + 1)] + \
        [(MG_FINAL, _("Final"))]

    def story_chapter_ids(n):
        if n == 0:
            return ["intro"]
        if n == MG_FINAL:
            return ["final"]
        return ["mg%d_pre" % n, "mg%d_post" % n]

    def story_seen_menu():
        """Cenas vistas: do jogo em andamento ou, no menu, do save mais recente."""
        if getattr(store, "main_menu", False):
            slot = prog_newest_slot()
            info = renpy.slot_json(slot) if slot is not None else None
            return set((info or {}).get("story_seen", []))
        return set(k for k, v in store.story_seen.items() if v)


## Toca uma cena (lista de falas) sobre o fundo dado. "PULAR" encerra a cena.
label story_play(sid, bg):

    $ story_mark(sid)
    $ _st_lines = STORY_TEXTS.get(sid, [])
    $ _st_i = 0
    scene expression bg with Dissolve(0.6)
    while _st_i < len(_st_lines):
        call screen intro_textbox(_st_lines[_st_i])
        if _return == "skip":
            $ _st_i = len(_st_lines)
        $ _st_i += 1
    scene black with Dissolve(0.4)
    return


## O final: epílogo + resumo do desempenho + créditos (+ QR da versão de testes).
label final_sequence:

    $ mg_float_clear()
    call story_play("final", story_bg(MG_FINAL)) from _story_final_call
    call screen game_summary with Dissolve(0.3)
    hide screen notebook_screen
    call screen about_screen(True) with Dissolve(0.3)
    $ final_seen = True

    # Versão de testes: agradecimento + QR code do formulário (test_build.rpy)
    if TEST_BUILD:
        call screen test_form_qr with Dissolve(0.3)
    return


## Rever cenas pela galeria do menu principal (modo "Replay" do Ren'Py).
label story_replay:

    $ quick_menu = False
    python:
        for _sid in replay_ids:
            if _sid == "intro":
                for _k in range(len(INTRO_TEXTS)):
                    renpy.scene()
                    renpy.show("intro_bg_replay", what=INTRO_ART[_k])
                    renpy.with_statement(Dissolve(0.6))
                    if renpy.call_screen("intro_textbox", INTRO_TEXTS[_k]) == "skip":
                        break
            else:
                _bg = story_bg(replay_chapter)
                renpy.scene()
                renpy.show("story_bg_replay", what=_bg)
                renpy.with_statement(Dissolve(0.6))
                for _line in STORY_TEXTS.get(_sid, []):
                    if renpy.call_screen("intro_textbox", _line) == "skip":
                        break
    $ renpy.end_replay()
    return


## Galeria de cenas (botão HISTÓRIA do menu principal)
screen story_gallery():

    modal True
    zorder 150

    add Solid("#000000bb")
    key "game_menu" action [Function(sfx, "window_close"), Hide("story_gallery")]

    add Solid("#371f12") pos (200, 70) xysize (1520, 940)
    add Solid("#ead9a8") pos (206, 76) xysize (1508, 928)

    text _("HISTÓRIA"):
        xalign 0.5
        ypos 96
        size 48
        bold True
        color MG_INSTR_TEXT_COLOR

    text _("Clique numa cena já vista para revê-la."):
        xalign 0.5
        ypos 158
        size 24
        color "#5a4a38"

    $ seen = story_seen_menu()

    for k, (n, title) in enumerate(STORY_CHAPTERS):
        $ ids = [i for i in story_chapter_ids(n) if i in seen]
        $ cx = 389 + (k % 3) * 394
        $ cy = 206 + (k // 3) * 222
        $ ch_title = title

        if ids:
            button:
                pos (cx, cy)
                xysize (354, 202)
                background Solid("#371f12")
                hover_background Solid("#f2c230")
                action [Function(sfx, "click"),
                        Replay("story_replay", scope={"replay_ids": ids, "replay_chapter": n}, locked=False)]
                hovered Function(sfx, "hover")
                add Transform(story_bg(n), zoom=0.18, xpos=4, ypos=4)
                add Solid("#000000aa", xysize=(346, 44)) pos (4, 154)
                text "[ch_title!t]":
                    pos (177, 176)
                    anchor (0.5, 0.5)
                    size 28
                    bold True
                    color "#ffffff"
        else:
            fixed:
                pos (cx, cy)
                xysize (354, 202)
                add Solid("#5c5444")
                add Solid("#9a8f7a", xysize=(346, 194)) pos (4, 4)
                text "?":
                    align (0.5, 0.42)
                    size 90
                    bold True
                    color "#5c5444"
                text "[ch_title!t]":
                    pos (177, 176)
                    anchor (0.5, 0.5)
                    size 26
                    color "#4a4234"

    imagebutton:
        idle ACH_BACK_IDLE
        hover ACH_BACK_HOVER
        focus_mask True
        action [Function(sfx, "window_close"), Hide("story_gallery")]
        hovered Play("sound", "audio/sfx_hover.ogg")
