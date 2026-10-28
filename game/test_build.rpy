################################################################################
# TEST_BUILD.RPY
# Recursos da VERSÃO DE TESTES do jogo:
#   1) Aviso ao entrar no mapa pela primeira vez ("esta é uma versão de testes").
#   2) No fim do minigame 7: tela de agradecimento com o QR code do formulário.
#
# Para lançar a versão final, basta trocar TEST_BUILD para False: o aviso e o
# QR code deixam de aparecer (os arquivos continuam aqui, sem uso).
#
# ARTE: images/qr_formulario.png (o seu QR code; qualquer tamanho quadrado).
# O painel e o botão usam a mesma arte da tela de resultado (mg_common.rpy).
################################################################################

define TEST_BUILD = True

# O aviso aparece uma vez por jogo (cada "Novo jogo" mostra de novo).
default test_notice_seen = False

init python:

    TEST_QR_FILE = "images/qr_formulario.png"
    TEST_QR_POS = (300, 328)       # posição do QR (tela 1920x1080)
    TEST_QR_SIZE = 474             # lado do QR em pixels da tela

    if renpy.loadable(TEST_QR_FILE):
        TEST_QR_ART = Transform(Image(TEST_QR_FILE), xysize=(TEST_QR_SIZE, TEST_QR_SIZE))
    else:
        TEST_QR_ART = Fixed(Solid("#ffffff", xysize=(TEST_QR_SIZE, TEST_QR_SIZE)),
                            Text("QR CODE\n(images/qr_formulario.png)", size=28, color="#000000",
                                 xalign=0.5, yalign=0.5, text_align=0.5),
                            xysize=(TEST_QR_SIZE, TEST_QR_SIZE))


## -----------------------------------------------------------------------
## Aviso: versão de testes (uma vez, ao entrar no mapa)
## -----------------------------------------------------------------------
screen test_notice():

    modal True
    zorder 160

    add Solid("#000000bb")
    add MG_RESULT_PANEL

    text _("VERSÃO DE TESTES"):
        pos MG_RESULT_TITLE_POS
        anchor (0.5, 0.5)
        size 46
        bold True
        color MG_INSTR_TEXT_COLOR

    text _("Bem-vindo(a) a Proteja Equinópolis!"):
        pos MG_RESULT_SCORE_POS
        anchor (0.5, 0.5)
        size 36
        color MG_INSTR_TEXT_COLOR

    $ notice_text = _("Este jogo ainda está em fase de testes. Você pode encontrar erros, textos incompletos e artes provisórias, e os desafios 8 a 10 do mapa ainda não estão prontos.\n\nJogue com calma, anote o que achar estranho ou confuso e, quando terminar o minigame 7, responda ao formulário de feedback (vai aparecer um QR code). A sua opinião vai ajudar a melhorar o jogo!\n\nObrigado por participar.")

    text "[notice_text!t]":
        pos (960, 340)
        anchor (0.5, 0.0)
        text_align 0.5
        size 30
        xmaximum 1250
        color MG_INSTR_TEXT_COLOR

    imagebutton:
        idle MG_RESULT_CONTINUE_IDLE
        hover MG_RESULT_CONTINUE_HOVER
        focus_mask True
        action [Function(sfx, "click"), Return(True)]
        hovered Function(sfx, "hover")


## -----------------------------------------------------------------------
## Fim do minigame 7: agradecimento + QR code do formulário
## -----------------------------------------------------------------------
screen test_form_qr():

    modal True
    zorder 160

    add Solid("#000000bb")
    add MG_RESULT_PANEL

    text _("OBRIGADO POR TESTAR!"):
        pos MG_RESULT_TITLE_POS
        anchor (0.5, 0.5)
        size 46
        bold True
        color MG_INSTR_TEXT_COLOR

    text _("Você chegou ao fim da versão de testes."):
        pos MG_RESULT_SCORE_POS
        anchor (0.5, 0.5)
        size 36
        color MG_INSTR_TEXT_COLOR

    add TEST_QR_ART pos TEST_QR_POS

    $ qr_text = _("Aponte a câmera do celular para o QR code ao lado para abrir o formulário de feedback.\n\nLeva cerca de 10 minutos e é anônimo. Conte o que gostou, o que achou confuso e o que mudaria: a sua opinião é muito importante!")

    text "[qr_text!t]":
        pos (820, 360)
        size 30
        xmaximum 780
        color MG_INSTR_TEXT_COLOR

    imagebutton:
        idle MG_RESULT_CONTINUE_IDLE
        hover MG_RESULT_CONTINUE_HOVER
        focus_mask True
        action [Function(sfx, "click"), Return(True)]
        hovered Function(sfx, "hover")
