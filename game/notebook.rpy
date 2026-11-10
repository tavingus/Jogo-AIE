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

    # ------------------------------------------------------------------
    # CONTEÚDO DO CADERNO (edite à vontade)
    #   "items"   = PONTOS-CHAVE: frases com lacuna (%s), o que é preciso
    #               saber para terminar o minigame. Ficam em destaque na
    #               página da esquerda; as lacunas só são preenchidas depois
    #               de concluir o minigame.
    #   "explain" = PARA ENTENDER MELHOR: texto explicativo (nível de
    #               graduação), na página da direita, com rolagem.
    #               Linha começando com "# " = subtítulo.
    #               **texto** = trecho em destaque (o que cai no minigame).
    # ------------------------------------------------------------------
    NOTEBOOK_PAGES = [
        {"mg": 1, "title": _("O vírus"),
         "items": [
            (_("A AIE é causada pelo vírus da anemia infecciosa equina (EIAV), da ordem %s."), "Ortervirales"),
            (_("Ele pertence à família %s, subfamília %s."), ("Retroviridae", "Orthoretrovirinae")),
            (_("O gênero é %s, o mesmo do HIV, mas o EIAV não infecta humanos."), "Lentivirus"),
            (_("É um vírus envelopado de forma %s."), "esférica"),
            (_("Afeta apenas %s: cavalos, jumentos e muares."), "equídeos"),
         ],
         "explain": [
            _("# O que é o EIAV"),
            _("O vírus da anemia infecciosa equina (EIAV, sigla em inglês) é um **retrovírus**: seu genoma é de **RNA de fita simples**, e ele carrega a enzima **transcriptase reversa**, que copia esse RNA em DNA. Esse DNA (o **provírus**) é inserido no genoma das células do hospedeiro, principalmente **monócitos e macrófagos**."),
            _("Por isso a infecção é **persistente**: uma vez infectado, o equídeo carrega o vírus **pela vida toda**, mesmo sem sinais clínicos, e continua sendo fonte de infecção para outros animais."),
            _("# Taxonomia"),
            _("Ordem **Ortervirales** → família **Retroviridae** → subfamília **Orthoretrovirinae** → gênero **Lentivirus** → espécie **Equine infectious anemia virus**. \"Lenti\" vem do latim lento: são vírus de infecções longas, que evoluem devagar."),
            _("# Estrutura"),
            _("É um vírus **envelopado**, de forma aproximadamente **esférica**, com cerca de 100 nm. Dentro do envelope há um capsídeo cônico formado pela proteína **p26** (a principal proteína detectada nos exames). No envelope ficam as glicoproteínas **gp90** e **gp45**."),
            _("A gp90 sofre **variação antigênica**: ao longo da infecção o vírus muda essa proteína e escapa dos anticorpos já produzidos. Cada nova variante pode causar uma nova crise de febre, e é por isso que a doença tem episódios **recorrentes**."),
            _("# Quem a AIE afeta"),
            _("Só **equídeos** (cavalos, jumentos e muares). Apesar de ser parente do HIV, o EIAV **não infecta pessoas**: a AIE **não é zoonose**."),
         ]},
        {"mg": 2, "title": _("Sinais clínicos"),
         "items": [
            (_("Sinais clássicos: %s em episódios recorrentes, mucosas pálidas e petéquias."), "febre"),
            (_("Também há linfonodos aumentados, letargia, fraqueza e %s."), "perda de peso"),
            (_("No hemograma aparecem anemia e %s (plaquetas baixas)."), "trombocitopenia"),
            (_("Muitos animais não mostram sinal nenhum: são os %s."), "portadores inaparentes"),
         ],
         "explain": [
            _("# As três formas da doença"),
            _("**Aguda**: surge cerca de 1 a 4 semanas após a infecção, com **febre**, apatia, falta de apetite e **trombocitopenia**. Pode ser tão branda que passa despercebida. Nessa fase há **muito vírus no sangue**, e o animal é muito infectante."),
            _("**Crônica**: **episódios recorrentes** de febre, anemia, perda de peso, edema na barriga e nos membros e **petéquias** nas mucosas, intercalados com períodos sem sinais. Com o tempo, as crises ficam mais espaçadas."),
            _("**Inaparente**: é como a maioria dos infectados termina: **sem sinais**, mas com o vírus para sempre. Estresse, trabalho pesado ou corticoides podem reativar a doença. São os **portadores inaparentes**, a principal fonte de vírus nos rebanhos."),
            _("# Por que o cavalo fica anêmico?"),
            _("Principalmente por **destruição das hemácias**: proteínas do vírus e anticorpos se ligam a elas, ativam o complemento, e os macrófagos as retiram da circulação. Soma-se a isso uma produção menor de hemácias na medula óssea. No hemograma: **hematócrito e hemoglobina baixos**."),
            _("A **trombocitopenia** (plaquetas baixas) também é imunomediada e explica as **petéquias** (pontinhos de sangramento) nas mucosas."),
            _("# Na prática"),
            _("Os sinais **não são exclusivos** da AIE: lembram outras doenças, como piroplasmose, anaplasmose e púrpura hemorrágica. E muitos infectados não têm sinal nenhum. Por isso **o exame clínico levanta a suspeita, mas só o exame de laboratório confirma**. Não há tratamento que elimine o vírus nem vacina aprovada no Brasil."),
         ]},
        {"mg": 3, "title": _("Coleta de sangue"),
         "items": [
            (_("Para a sorologia usa-se tubo %s, porque o exame precisa do soro."), "sem anticoagulante"),
            (_("O sangue é colhido da veia %s."), "jugular"),
            (_("A amostra é identificada com nome, propriedade e %s."), "data da coleta"),
            (_("A %s (idade, sexo e pelagem) identifica o animal e é obrigatória."), "resenha"),
            (_("A amostra segue ao laboratório em caixa %s."), "refrigerada"),
         ],
         "explain": [
            _("# Por que tubo sem anticoagulante?"),
            _("Os exames de AIE (IDGA e ELISA) procuram **anticorpos no soro**. Sem anticoagulante (tubo seco, geralmente de tampa vermelha), o sangue **coagula**: o coágulo fica embaixo e o **soro**, a parte líquida, fica em cima. Com **EDTA** ou **heparina** o sangue não coagula e não se obtém soro."),
            _("# Como colher"),
            _("A coleta é feita na **veia jugular**, no pescoço, depois da **antissepsia** do local, com **agulha e tubo novos e descartáveis** para cada animal (agulha reutilizada transmite a AIE!). Vias intramuscular e subcutânea servem para aplicar medicamentos, não para colher sangue."),
            _("No Brasil, a coleta para o exame oficial é feita por **médico veterinário** cadastrado no serviço veterinário oficial, e o exame é feito em **laboratório credenciado** pelo MAPA."),
            _("# Identificação e resenha"),
            _("Amostra mal identificada não serve: uma troca pode liberar um animal positivo. A requisição traz **nome do animal, propriedade e data da coleta**, e a **resenha** descreve o animal (espécie, sexo, idade, pelagem e marcas particulares) para que o resultado fique ligado ao animal certo. Por isso ela é **obrigatória**."),
            _("# Transporte"),
            _("A amostra deve ir **refrigerada** (caixa térmica com gelo, sem congelar o sangue) e chegar logo ao laboratório. Calor e demora causam **hemólise** e deterioração, que podem invalidar o exame."),
         ]},
        {"mg": 4, "title": _("Diagnóstico: IDGA e ELISA"),
         "items": [
            (_("Os exames procuram %s contra o vírus no soro do cavalo."), "anticorpos"),
            (_("O IDGA detecta principalmente o anticorpo anti-%s, do capsídeo do vírus."), "p26"),
            (_("No IDGA, o positivo forma uma linha de %s que se une à linha do controle positivo."), "precipitação"),
            (_("O teste oficial de referência é o %s, também chamado de teste de Coggins."), "IDGA"),
            (_("No ELISA, amostra com densidade óptica acima do %s é positiva."), "ponto de corte"),
            (_("O ELISA é mais sensível e serve de triagem; um positivo nele é confirmado pelo %s."), "IDGA"),
         ],
         "explain": [
            _("# O que os exames procuram"),
            _("IDGA e ELISA são exames **sorológicos**: não procuram o vírus, e sim os **anticorpos** que o cavalo produziu contra ele. Como a infecção dura a vida toda, **anticorpo presente = animal infectado** (com exceções, veja no fim da página). O alvo principal é o anticorpo contra a **p26**, proteína do capsídeo."),
            _("# IDGA: imunodifusão em gel de ágar (teste de Coggins)"),
            _("Criado por Leroy Coggins nos anos 1970. Numa placa de **gel de ágar** abrem-se pequenos poços: no **central** vai o **antígeno** (p26), e nos poços em volta vão os **soros testados**, alternados com o **soro controle positivo**."),
            _("Antígeno e anticorpos **se difundem** pelo gel. Onde se encontram na proporção certa, formam um complexo insolúvel que aparece como uma **linha branca de precipitação**. A leitura é feita a olho nu, contra a luz, depois de **24 a 48 horas**."),
            _("**Positivo**: a amostra forma uma linha que **se une à linha do controle positivo** (linha de identidade), num arco contínuo. **Negativo**: a amostra não forma linha, e a linha do controle segue reta até o poço da amostra. **Fraco positivo**: a amostra não forma uma linha clara, mas faz a ponta da linha do controle **se curvar** em direção ao poço central. Também é positivo e exige atenção na leitura."),
            _("O IDGA é o **teste oficial de referência**: muito específico, porém menos sensível que o ELISA e dependente da experiência de quem lê."),
            _("# ELISA: ensaio imunoenzimático"),
            _("O antígeno do vírus fica preso no fundo dos poços de uma placa. Coloca-se o soro: se houver anticorpos contra o EIAV, eles se ligam ao antígeno. Depois entra um **anticorpo secundário ligado a uma enzima** e, por fim, um **substrato** que **muda de cor** quando a enzima está presente."),
            _("Quanto **mais anticorpo, mais cor**. O **espectrofotômetro** (leitor de placas) mede essa cor como **densidade óptica (DO)**, e o resultado é comparado a um **ponto de corte** calculado a partir dos controles do kit: **DO acima do ponto de corte = positivo**. Cada kit tem a sua regra de corte; a do jogo é um exemplo."),
            _("É **mais sensível** e mais rápido (horas), bom para **triagem** de muitos animais. Em troca, pode dar **falso-positivo**: por isso um positivo no ELISA é **confirmado pelo IDGA**."),
            _("# Armadilhas na interpretação"),
            _("**Infecção recente**: o cavalo leva algumas semanas (em geral até cerca de 45 dias) para produzir anticorpos detectáveis. Um negativo logo após uma exposição de risco pode precisar ser **repetido**."),
            _("**Potros** de éguas positivas recebem anticorpos pelo **colostro** e podem dar positivo até cerca de **6 meses** de idade sem estarem infectados. Devem ser testados de novo depois disso."),
         ]},
        {"mg": 5, "title": _("Trânsito de animais"),
         "items": [
            (_("Só viaja cavalo com exame negativo dentro da validade de %s dias (valor do jogo)."), str(getattr(store, "MG5_VALIDITY_DAYS", 60))),
            (_("Exame negativo vencido: é preciso fazer uma %s antes de viajar."), "nova coleta"),
            (_("Cavalo positivo: é obrigatório %s o serviço veterinário oficial (MAPA)."), "notificar"),
            (_("Para transportar equídeos é preciso a %s, emitida com o exame em dia."), "GTA (Guia de Trânsito Animal)"),
         ],
         "explain": [
            _("# Por que exigir exame para viajar?"),
            _("Os **portadores inaparentes** parecem saudáveis. Exigir **exame negativo recente** para trânsito, provas, exposições e leilões impede que um portador leve o vírus a outros rebanhos. O exame em dia é exigido para emitir a **GTA**."),
            _("# Validade do exame"),
            _("O negativo vale por um **período limitado**, porque o animal pode se infectar depois da coleta. A validade conta a partir da **data da coleta**. Neste jogo usamos **60 dias** como exemplo: o prazo oficial é definido pelas normas do MAPA e do serviço veterinário do estado, e pode variar com a finalidade. Confira sempre a norma vigente."),
            _("# Negativo vencido"),
            _("Não é um resultado positivo: o animal só precisa de **nova coleta** e novo exame antes de poder viajar."),
            _("# Exame positivo"),
            _("A AIE é de **notificação obrigatória** ao serviço veterinário oficial. A propriedade é **interditada**, os outros equídeos são testados, e o animal positivo **não pode transitar**. A norma brasileira determina o **sacrifício** do positivo, com regras especiais em algumas regiões, como o Pantanal."),
         ]},
        {"mg": 6, "title": _("Transmissão por insetos"),
         "items": [
            (_("O vírus é transmitido de forma %s, pelo sangue que fica na boca do inseto."), "mecânica"),
            (_("Os principais vetores são as %s (família Tabanidae)."), "mutucas"),
            (_("A mosca-dos-estábulos (Stomoxys calcitrans) tem papel %s."), "secundário"),
            (_("Só insetos %s (que picam e sugam sangue) transmitem a AIE."), "hematófagos"),
         ],
         "explain": [
            _("# Transmissão mecânica"),
            _("O vírus **não se multiplica** dentro do inseto (não é transmissão biológica, como na dengue). O inseto apenas **carrega sangue contaminado nas peças bucais** de um animal para outro, como uma \"agulha voadora\". O vírus sobrevive pouco tempo ali (de minutos a poucas horas), então o risco é maior quando os animais estão **próximos**."),
            _("# Mutucas (Tabanidae): as principais vetoras"),
            _("Mutucas, dos gêneros **Tabanus**, **Chrysops** e **Hybomitra**, entre outros, são grandes, têm peças bucais cortantes e a **picada é dolorosa**. Só as **fêmeas** sugam sangue."),
            _("Como dói, o cavalo reage e a mutuca é **interrompida no meio da alimentação**. Ela então **voa para o animal mais próximo** para terminar, levando o sangue do primeiro. É esse comportamento que faz dela a vetora mais importante."),
            _("São mais ativas em dias **quentes, ensolarados e úmidos**, na estação chuvosa, perto de matas, rios e áreas alagadas, onde as larvas se desenvolvem."),
            _("# Mosca-dos-estábulos (Stomoxys calcitrans)"),
            _("Parece a mosca-doméstica, mas tem uma **probóscide rígida** que pica, e machos e fêmeas se alimentam de sangue. Tem papel **secundário** na AIE. Cria-se em **matéria orgânica em decomposição**: esterco misturado com palha, restos de feno e de silagem."),
            _("# E os outros insetos?"),
            _("Moscas que **não picam**, como a mosca-doméstica, e insetos que não se alimentam de sangue **não transmitem** a AIE. Mosquitos picam, mas carregam pouquíssimo sangue e têm importância mínima."),
            _("# Manejo para reduzir o risco"),
            _("• **Exame periódico** de todo o plantel e retirada dos positivos: sem fonte de vírus, o inseto não tem o que carregar."),
            _("• **Distância**: mutucas interrompidas raramente voam longe; programas de controle recomendam manter animais positivos isolados a cerca de **200 metros** dos demais, quando a norma permite o isolamento."),
            _("• **Baias com tela** e animais **recolhidos nas horas mais quentes do dia**, quando as mutucas mais atacam."),
            _("• **Repelentes e inseticidas** nos animais e nas instalações, e **armadilhas** para mutucas."),
            _("• **Manejo do esterco e da matéria orgânica** (recolher e compostar) contra a mosca-dos-estábulos, e **drenagem** de áreas encharcadas contra as larvas de mutuca."),
            _("• Não **aglomerar** animais de origens diferentes sem exame em dia."),
         ]},
        {"mg": 7, "title": _("Transmissão iatrogênica"),
         "items": [
            (_("Reutilizar %s passa o vírus de um cavalo para outro."), "agulhas"),
            (_("A transmissão causada por procedimentos humanos chama-se %s."), "iatrogênica"),
            (_("Use agulha e seringa %s para cada animal."), "novas e descartáveis"),
            (_("A AIE não tem cura nem vacina: a única defesa é a %s."), "prevenção"),
         ],
         "explain": [
            _("# O que é"),
            _("**Iatrogênico** (do grego iatros, médico) é o que é causado por **procedimentos feitos por pessoas**: injeções, coletas de sangue, cirurgias, transfusões."),
            _("# Por que é tão eficiente"),
            _("Uma agulha usada num portador pode carregar sangue suficiente para infectar outro animal, principalmente se o primeiro estiver na **fase aguda**, com muito vírus no sangue. Ao contrário do inseto, a agulha leva o sangue **direto para dentro** do vaso ou do músculo."),
            _("# Fontes de risco"),
            _("• **Agulhas e seringas reutilizadas**, como em vacinação ou medicação \"uma agulha para o lote\"."),
            _("• **Instrumentos** mal higienizados: material cirúrgico, odontológico, de identificação e sondas."),
            _("• **Sangue e plasma** de doador não testado. Em 2006, um surto de AIE na **Irlanda** foi ligado a **plasma contaminado** aplicado em potros."),
            _("• **Arreios** sujos de sangue, como esporas e freios, também são citados como possibilidade."),
            _("# Prevenção"),
            _("• **Uma agulha e uma seringa novas para cada animal**, sempre, inclusive na vacinação."),
            _("• Limpar e **esterilizar** instrumentos entre um animal e outro."),
            _("• **Testar os doadores** de sangue e plasma e usar produtos de origem confiável."),
            _("• Como **não há vacina nem cura**, a prevenção (exame em dia, controle de insetos e boas práticas) é a única defesa contra a AIE."),
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

    import re as _re
    NB_KEY_COLOR = "#b0441f"     # cor dos trechos em destaque (**texto**)

    def nb_fmt(paragraph):
        """Converte **texto** em destaque (negrito colorido)."""
        return _re.sub(r"\*\*(.+?)\*\*",
                       r"{b}{color=%s}\1{/color}{/b}" % NB_KEY_COLOR,
                       renpy.translate_string(paragraph))

    def nb_images(n, unlocked):
        """Imagens reais da página (opcional), só quando desbloqueada."""
        out = []
        if unlocked:
            for k in (1, 2):
                for ext in ("png", "jpg", "jpeg", "webp"):
                    p = "images/notebook/pagina_%d_%d.%s" % (n, k, ext)
                    if renpy.loadable(p):
                        out.append(Transform(Image(p), xysize=(700, 360), fit="contain"))
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
    zorder 170

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

    # ---- Página da ESQUERDA: título + PONTOS-CHAVE (lacunas) --------------
    text "Minigame [pg_mg]":
        pos (190, 104)
        size 24
        color "#8a5a30"
    if unlocked:
        text "[pg_title!t]":
            pos (190, 132)
            size 44
            bold True
            color "#1f3f8f"
            xmaximum 560
        text _("ANOTADO!"):
            pos (712, 112)
            size 36
            bold True
            color "#2e7d32"
            outlines [(2, "#ffffff88", 0, 0)]
            at Transform(rotate=-10)
    else:
        text "???":
            pos (190, 132)
            size 52
            bold True
            color "#9a9078"

    # Faixa "marca-texto" atrás do cabeçalho
    add Solid("#f6e05e99") pos (182, 214) xysize (300, 40)
    text _("PONTOS-CHAVE"):
        pos (190, 216)
        size 28
        bold True
        color "#3a2410"

    vbox:
        pos (190, 270)
        spacing 20
        for template, answer in pg["items"]:
            $ line = u"\u2022 " + nb_line(template, answer, unlocked)
            text line:
                size 26
                color "#2a2a3a"
                xmaximum 700

    if not unlocked:
        text _("Conclua o minigame [pg_mg] para preencher as lacunas e liberar as anotações."):
            pos (190, 860)
            size 24
            italic True
            color "#b04a3a"
            xmaximum 700

    text _("Anotações [got_n]/[tot_n]"):
        pos (720, 966)
        size 22
        color "#8a5a30"

    # ---- Página da DIREITA: PARA ENTENDER MELHOR (texto com rolagem) -------
    add Solid("#9fd8f099") pos (1022, 98) xysize (420, 40)
    text _("PARA ENTENDER MELHOR"):
        pos (1030, 100)
        size 28
        bold True
        color "#3a2410"

    if unlocked:
        viewport id "nb_vp":
            pos (1030, 156)
            xysize (720, 770)
            mousewheel True
            draggable True
            vbox:
                xsize 700
                spacing 14
                for par in pg.get("explain", []):
                    if par.startswith("# "):
                        null height 6
                        text nb_fmt(par[2:]):
                            size 27
                            bold True
                            color "#1f3f8f"
                            xmaximum 700
                    else:
                        text nb_fmt(par):
                            size 24
                            color "#2a2a3a"
                            xmaximum 700
                # Imagens reais (opcional): images/notebook/pagina_<N>_1.png ...
                $ imgs = nb_images(pg_mg, True)
                for im in imgs:
                    null height 6
                    add im
                if not imgs and config.developer:
                    text _("(dev) imagens desta página: images/notebook/pagina_[pg_mg]_1.png e _2.png"):
                        size 20
                        italic True
                        color "#8a5a30"
                null height 20
        vbar value YScrollValue("nb_vp"):
            pos (1756, 156)
            xysize (14, 770)
            base_bar Solid("#d9cfae")
            thumb Solid("#8a5a30")
    else:
        text _("Página bloqueada.\n\nConclua o minigame [pg_mg] para liberar aqui uma explicação completa do assunto, com os pontos que caem no desafio em destaque."):
            pos (1030, 200)
            size 28
            italic True
            color "#6a5a40"
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


## -----------------------------------------------------------------------
## Apresentação do caderno: aparece uma vez por jogo, na primeira vez que o
## mapa é mostrado (depois do aviso de versão de testes, se houver).
## -----------------------------------------------------------------------
default nb_intro_seen = False

screen notebook_intro():

    modal True
    zorder 160

    # O mapa continua visível atrás (só um leve escurecimento)
    add Solid("#00000066")

    # Painel compacto, à direita do botão do caderno
    add Solid("#371f12") pos (520, 210) xysize (1080, 600)
    add Solid("#ead9a8") pos (526, 216) xysize (1068, 588)

    text _("NOVO: CADERNO DA AIE"):
        xpos 1060
        ypos 262
        anchor (0.5, 0.5)
        size 46
        bold True
        color MG_INSTR_TEXT_COLOR

    $ nb_intro_text = _("Você ganhou um caderno de anotações sobre a Anemia Infecciosa Equina!\n\nCada página é de um desafio. Ao CONCLUIR um desafio (com qualquer pontuação), a página dele é preenchida, e você pode consultá-la quando quiser, aqui no mapa ou no menu principal.\n\nExperimente agora: clique no CADERNO, no canto da tela.")

    text "[nb_intro_text!t]":
        xpos 1060
        ypos 320
        xanchor 0.5
        text_align 0.5
        size 30
        xmaximum 980
        color MG_INSTR_TEXT_COLOR

    # O botão do caderno funciona aqui mesmo (abre o caderno por cima)
    imagebutton:
        idle MENU_BTN["notebook"]["idle"]
        hover MENU_BTN["notebook"]["hover"]
        focus_mask True
        action [Function(sfx, "window_open"), Show("notebook_screen")]
        hovered Function(sfx, "hover")

    text _("Clique aqui!"):
        pos (70, 900)
        size 32
        bold True
        color "#ffe9a8"
        outlines [(3, "#2a1a0c", 0, 0)]
        at nb_intro_bounce

    button:
        xpos 1060
        ypos 720
        anchor (0.5, 0.5)
        xysize (360, 80)
        background Solid("#371f12")
        hover_background Solid("#1e1208")
        action [Function(sfx, "click"), Return(True)]
        hovered Function(sfx, "hover")
        frame:
            pos (4, 4)
            xysize (352, 72)
            padding (0, 0)
            background Solid("#568e48")
            text _("ENTENDI"):
                align (0.5, 0.5)
                size 34
                bold True
                color "#fffaeb"
                outlines [(0, "#2a1a0c", 2, 2)]


transform nb_intro_bounce:
    yoffset 0
    easein 0.5 yoffset 10
    easeout 0.5 yoffset 0
    repeat
