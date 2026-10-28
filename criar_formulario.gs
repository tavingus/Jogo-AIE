/**
 * CRIA O FORMULÁRIO DE TESTE DO JOGO "PROTEJA EQUINÓPOLIS" (versão completa, anônima).
 *
 * Como usar:
 *   1. Abra https://script.google.com e clique em "Novo projeto".
 *   2. Apague o código que aparece e cole TODO este arquivo.
 *   3. Clique em "Executar" (função criarFormulario) e autorize quando o Google pedir
 *      (é a sua própria conta; o script só cria o formulário e a planilha de respostas).
 *   4. Veja o resultado em "Execuções" ou no registro (Ctrl+Enter): ficam os links para
 *      EDITAR o formulário e para ENVIAR às pessoas.
 *
 * Anônimo: não coleta e-mail, nome nem contato. Para isso o formulário também
 * NÃO deve exigir login (veja a nota no fim do arquivo).
 */

var CRIAR_PLANILHA_DE_RESPOSTAS = true;   // false = não cria a planilha

function criarFormulario() {
  var form = FormApp.create('Proteja Equinópolis — Formulário de teste');

  form.setDescription(
    'Obrigado por testar o jogo!\n\n' +
    'Esta é uma versão de teste de um jogo sobre a Anemia Infecciosa Equina (AIE). ' +
    'As suas respostas ajudam a melhorar a jogabilidade, o conteúdo e o aprendizado. ' +
    'Não existem respostas certas ou erradas: queremos a sua opinião sincera, inclusive as críticas.\n\n' +
    'O formulário é ANÔNIMO e leva cerca de 10 a 15 minutos.'
  );
  form.setCollectEmail(false);
  form.setProgressBar(true);
  form.setAllowResponseEdits(false);
  form.setShowLinkToRespondAgain(false);
  form.setConfirmationMessage('Obrigado pela sua participação! As suas respostas vão ajudar a melhorar o jogo.');

  var ESC = {
    conc: ['Discordo totalmente', 'Concordo totalmente'],
    muitoRuimBom: ['Muito ruim', 'Muito boa'],
    nadaMuito: ['Nada', 'Muito']
  };

  // ---------------------------------------------------------------- auxiliares
  function secao(titulo, descricao) {
    var s = form.addPageBreakItem().setTitle(titulo);
    if (descricao) s.setHelpText(descricao);
  }
  function unica(titulo, opcoes, obrig, ajuda) {
    var q = form.addMultipleChoiceItem().setTitle(titulo).setChoiceValues(opcoes).setRequired(!!obrig);
    if (ajuda) q.setHelpText(ajuda);
    return q;
  }
  function varias(titulo, opcoes, obrig, comOutro, ajuda) {
    var q = form.addCheckboxItem().setTitle(titulo).setChoiceValues(opcoes).setRequired(!!obrig);
    if (comOutro) q.showOtherOption(true);
    if (ajuda) q.setHelpText(ajuda);
    return q;
  }
  function escala(titulo, minimo, maximo, rotEsq, rotDir, obrig, ajuda) {
    var q = form.addScaleItem().setTitle(titulo).setBounds(minimo, maximo)
      .setLabels(rotEsq, rotDir).setRequired(!!obrig);
    if (ajuda) q.setHelpText(ajuda);
    return q;
  }
  function conc(titulo, obrig, ajuda) {          // escala 1–5 "discordo / concordo"
    return escala(titulo, 1, 5, ESC.conc[0], ESC.conc[1], obrig, ajuda);
  }
  function curta(titulo, obrig, ajuda) {
    var q = form.addTextItem().setTitle(titulo).setRequired(!!obrig);
    if (ajuda) q.setHelpText(ajuda);
    return q;
  }
  function longa(titulo, obrig, ajuda) {
    var q = form.addParagraphTextItem().setTitle(titulo).setRequired(!!obrig);
    if (ajuda) q.setHelpText(ajuda);
    return q;
  }
  function grade(titulo, linhas, colunas, obrig, ajuda) {
    var q = form.addGridItem().setTitle(titulo).setRows(linhas).setColumns(colunas).setRequired(!!obrig);
    if (ajuda) q.setHelpText(ajuda);
    return q;
  }

  var MINIGAMES = [
    'Minigame 1 — Taxonomia',
    'Minigame 2 — Exame clínico',
    'Minigame 3 — Coleta de exame',
    'Minigame 4 — Diagnóstico (IDGA e ELISA)',
    'Minigame 5 — Triagem de cavalos',
    'Minigame 6 — Moscas hematófagas',
    'Minigame 7 — Impedir a reutilização de agulha'
  ];
  var MG_CURTO = ['Minigame 1 (Taxonomia)', 'Minigame 2 (Exame clínico)', 'Minigame 3 (Coleta)',
    'Minigame 4 (IDGA e ELISA)', 'Minigame 5 (Triagem)', 'Minigame 6 (Moscas)', 'Minigame 7 (Agulha)'];

  // ---------------------------------------------------------------- 1. SOBRE VOCÊ
  secao('1. Sobre você', 'Perguntas gerais, sem identificação.');
  unica('Você já conhecia a AIE antes de jogar?',
    ['Nunca ouvi falar', 'Já ouvi falar', 'Conheço o básico', 'Trabalho ou estudo a AIE'], true);
  unica('Com que frequência você joga videogames?',
    ['Nunca', 'Raramente', 'Algumas vezes por mês', 'Toda semana', 'Quase todo dia'], false);
  unica('Em que dispositivo você jogou?',
    ['Computador (Windows)', 'Computador (outro sistema)', 'Outro'], true);
  unica('Quanto tempo você jogou?',
    ['Menos de 10 minutos', 'De 10 a 30 minutos', 'De 30 a 60 minutos', 'Mais de 1 hora'], true);
  varias('Quais minigames você completou?',
    MINIGAMES.concat(['Nenhum completo']), true, false);

  // ---------------------------------------------------------------- 2. PRIMEIRA IMPRESSÃO
  secao('2. Primeira impressão');
  escala('Qual foi a sua primeira impressão do jogo?', 1, 5, ESC.muitoRuimBom[0], ESC.muitoRuimBom[1], true);
  conc('Você entendeu logo de cara qual é o objetivo do jogo?', true);
  unica('A introdução (3 imagens com texto) foi...',
    ['Interessante', 'Boa, mas longa', 'Curta demais', 'Desnecessária', 'Não vi a introdução'], false);
  varias('O que você sentiu ao começar a jogar?',
    ['Curiosidade', 'Empolgação', 'Confusão', 'Tédio', 'Pressão', 'Nada em especial'], false, true);

  // ---------------------------------------------------------------- 3. TUTORIAIS
  secao('3. Entendimento e tutoriais');
  escala('As telas de instruções (antes de cada minigame) foram claras?', 1, 5, 'Nada claras', 'Muito claras', true,
    '1 = nada claras: não entendi o que fazer; 3 = razoáveis: entendi, mas com dúvidas; 5 = muito claras: entendi na hora.');
  unica('Em qual minigame as instruções foram mais confusas?',
    MG_CURTO.concat(['Nenhum']), false);
  longa('O que faltou nas instruções?', false);
  conc('Você soube o que fazer em cada tela sem precisar de ajuda?', true);
  longa('Houve algum momento em que você não sabia o que clicar ou o que fazer? Onde?', false);

  // ---------------------------------------------------------------- 4. MINIGAMES
  secao('4. Os minigames', 'Avalie cada minigame que você jogou. Se não jogou algum, pode deixar essa linha em branco (se o Google exigir, escolha a opção do meio).');
  var colDiv = ['Nada divertido', 'Pouco divertido', 'Razoável', 'Divertido', 'Muito divertido'];
  var colCla = ['Nada claro', 'Pouco claro', 'Razoável', 'Claro', 'Muito claro'];
  var colDif = ['Muito fácil', 'Fácil', 'Adequada', 'Difícil', 'Muito difícil'];
  var colApr = ['Nada', 'Pouco', 'Algum', 'Bastante', 'Muito'];
  grade('Diversão: cada minigame foi divertido?', MG_CURTO, colDiv, true);
  grade('Clareza: deu para entender o que fazer?', MG_CURTO, colCla, true);
  grade('Dificuldade: como foi o nível de dificuldade?', MG_CURTO, colDif, true);
  grade('Aprendizado: você sente que aprendeu ou revisou algo?', MG_CURTO, colApr, true);

  unica('Qual minigame foi o seu favorito?', MG_CURTO.concat(['Nenhum']), false);
  curta('Por que esse foi o seu favorito?', false);
  unica('Qual minigame foi o menos interessante ou mais frustrante?', MG_CURTO.concat(['Nenhum']), false);
  longa('Por que ele foi o menos interessante ou mais frustrante?', false);
  longa('Algum minigame ficou repetitivo ou longo demais? Qual e por quê?', false);
  longa('Algum minigame ficou curto demais? Qual?', false);

  form.addSectionHeaderItem().setTitle('Perguntas específicas (opcionais, mas muito úteis)');
  conc('Minigame 1 (Taxonomia): clicar para trocar as respostas foi intuitivo?', false);
  longa('Minigame 1 (Taxonomia): você prefere outra forma de jogar (por exemplo, arrastar)? Qual?', false);
  unica('Minigame 2 (Exame clínico): a quantidade de achados por área foi...', ['Pouca', 'Adequada', 'Muita'], false);
  conc('Minigame 3 (Coleta): as etapas e opções representam bem o que se faz de verdade?', false);
  longa('Minigame 3 (Coleta): o que você mudaria?', false);
  conc('Minigame 4 (IDGA e ELISA): o conteúdo ficou correto e fácil de interpretar?', false);
  longa('Minigame 4 (IDGA e ELISA): ficou alguma dúvida sobre a leitura das placas?', false);
  unica('Minigame 5 (Triagem): o tempo por cavalo (15 segundos) foi...', ['Curto demais', 'Adequado', 'Longo demais'], false);
  conc('Minigame 6 (Moscas): foi fácil distinguir a mosca hematófaga da inofensiva?', false);
  unica('Minigame 6 (Moscas): a velocidade das moscas foi...', ['Lenta', 'Adequada', 'Rápida'], false);
  conc('Minigame 7 (Agulha): você entendeu a diferença entre agulha nova e usada e quando reagir?', false);
  unica('Minigame 7 (Agulha): o tempo para reagir foi...', ['Curto demais', 'Adequado', 'Longo demais'], false);

  // ---------------------------------------------------------------- 5. CONTEÚDO CIENTÍFICO
  secao('5. Conteúdo científico', 'Para quem conhece o tema. Se não souber avaliar, escolha "Não sei avaliar".');
  unica('O conteúdo apresentado é cientificamente correto?',
    ['Totalmente correto', 'Em geral correto, com pequenas imprecisões', 'Parcialmente correto',
     'Tem erros importantes', 'Não sei avaliar'], true);
  longa('Você encontrou algum erro, imprecisão ou simplificação excessiva? Qual (minigame e trecho)?', false);
  unica('O nível de detalhe do conteúdo está...',
    ['Superficial demais', 'Adequado', 'Detalhado demais'], false);
  varias('Faltou algum tema importante sobre a AIE?',
    ['Transmissão', 'Sinais clínicos', 'Diagnóstico', 'Controle e prevenção', 'Legislação (MAPA)',
     'Epidemiologia', 'Manejo da propriedade'], false, true);
  conc('A revisão no final (o que você acertou e errou, com a explicação) ajudou a entender?', true);
  conc('As explicações da revisão foram claras e corretas?', false);
  longa('Alguma explicação ficou confusa ou incorreta? Qual?', false);
  conc('O jogo conseguiria ajudar um estudante a aprender sobre a AIE?', true);
  unica('Você usaria este jogo em aula, treinamento ou divulgação?',
    ['Sim', 'Talvez, com ajustes', 'Não'], false);
  curta('Se respondeu "Talvez" ou "Não", por quê?', false);
  escala('Como você avalia o seu conhecimento sobre a AIE ANTES de jogar?', 1, 5, 'Nenhum', 'Muito alto', false);
  escala('E DEPOIS de jogar?', 1, 5, 'Nenhum', 'Muito alto', false);

  // ---------------------------------------------------------------- 6. INTERFACE E VISUAL
  secao('6. Jogabilidade, interface e visual');
  conc('A interface (botões, menus, mapa) é fácil de usar?', true);
  conc('O mapa de desafios ficou claro (o que está liberado e o que já foi feito)?', false);
  conc('As medalhas e conquistas motivam a jogar de novo?', false);
  unica('O botão "Jogar de novo" ajudou a melhorar o seu resultado?',
    ['Sim', 'Não usei', 'Não ajudou'], false);
  escala('Como você avalia o visual (pixel art)?', 1, 5, 'Muito ruim', 'Muito bom', true);
  longa('O que você mais gostou ou mudaria no visual?', false);
  unica('A música e os efeitos sonoros...',
    ['Gostei muito', 'Gostei', 'Indiferente', 'Atrapalharam', 'Estavam desligados'], false);
  conc('O texto na tela era fácil de ler (tamanho, cor, contraste)?', false);
  longa('Onde você teve dificuldade para ler?', false);
  unica('Você usou o botão de pausa (embaixo, à esquerda) ou o controle de volume?',
    ['Sim, funcionou bem', 'Sim, com dificuldade', 'Não usei'], false);
  longa('Algum elemento da tela ficou fora do lugar, cortado ou difícil de ver? Qual?', false);

  // ---------------------------------------------------------------- 7. DIFICULDADE E MOTIVAÇÃO
  secao('7. Dificuldade, ritmo e motivação');
  unica('A dificuldade geral do jogo foi...',
    ['Fácil demais', 'Fácil', 'Adequada', 'Difícil', 'Difícil demais'], true);
  conc('A pontuação fez sentido (perda por erro, ganho por acerto)?', false);
  unica('Você teve vontade de repetir algum minigame para melhorar o resultado?',
    ['Sim', 'Talvez', 'Não'], false);
  longa('Em algum momento você quis parar de jogar? Por quê?', false);
  unica('O ritmo do jogo (do começo ao fim) foi...', ['Lento', 'Bom', 'Rápido'], false);

  // ---------------------------------------------------------------- 8. BUGS
  secao('8. Problemas técnicos (bugs)');
  unica('O jogo travou, fechou sozinho ou apresentou erro?',
    ['Não', 'Sim, uma vez', 'Sim, várias vezes'], true);
  longa('Se sim: o que você estava fazendo? Cole o texto do erro, se aparecer.', false);
  unica('Você teve problemas de desempenho (lentidão ou travadinhas)?',
    ['Não', 'Um pouco', 'Muito'], false);
  unica('O botão "Continuar" (retomar o jogo) funcionou como esperado?',
    ['Sim', 'Não', 'Não usei'], false);
  curta('Algum texto apareceu em inglês? Onde?', false);
  longa('Mais algum problema que você encontrou?', false);

  // ---------------------------------------------------------------- 9. SUS
  secao('9. Usabilidade geral',
    'Responda de acordo com a sua experiência: 1 = discordo totalmente, 5 = concordo totalmente.');
  conc('Acho que gostaria de jogar este jogo com frequência.', true);
  conc('Achei o jogo desnecessariamente complexo.', true);
  conc('Achei o jogo fácil de usar.', true);
  conc('Acho que precisaria de ajuda de uma pessoa para conseguir jogá-lo.', true);
  conc('Achei que as várias partes do jogo estavam bem integradas.', true);
  conc('Achei que havia inconsistência demais no jogo.', true);
  conc('Imagino que a maioria das pessoas aprenderia a jogar rapidamente.', true);
  conc('Achei o jogo muito pesado ou trabalhoso de jogar.', true);
  conc('Senti confiança ao jogar.', true);
  conc('Precisei aprender muitas coisas antes de conseguir jogar.', true);

  // ---------------------------------------------------------------- 10. AVALIAÇÃO GERAL
  secao('10. Avaliação geral e comentários livres');
  escala('De 0 a 10, o quanto você recomendaria este jogo a um colega?', 0, 10, 'Não recomendaria', 'Recomendaria muito', true);
  curta('Em uma palavra ou frase, como você descreve o jogo?', true);
  longa('O que você mais gostou?', true);
  longa('O que você menos gostou?', true);
  longa('Se você pudesse mudar UMA coisa no jogo, qual seria?', true);
  longa('Que funcionalidades ou minigames você gostaria de ver? (três desafios ainda estão por vir)', false);
  longa('Que outras doenças ou temas você gostaria de ver em um jogo assim?', false);
  longa('Você tem alguma crítica que não coube nas outras perguntas? Pode ser sincero(a).', false);

  // ---------------------------------------------------------------- planilha de respostas
  if (CRIAR_PLANILHA_DE_RESPOSTAS) {
    var planilha = SpreadsheetApp.create('Respostas — Proteja Equinópolis (teste)');
    form.setDestination(FormApp.DestinationType.SPREADSHEET, planilha.getId());
    Logger.log('Planilha de respostas: ' + planilha.getUrl());
  }

  Logger.log('EDITAR o formulário:  ' + form.getEditUrl());
  Logger.log('ENVIAR às pessoas:    ' + form.getPublishedUrl());
}

/*
 * NOTAS
 * - Anônimo: o script não cria perguntas de nome, e-mail ou contato e desliga a coleta de
 *   e-mail. No Google Forms, em Configurações > Respostas, deixe DESLIGADO "Exigir login"
 *   e "Limitar a 1 resposta" (que exige login). Contas de Google Workspace da instituição
 *   podem ter "Coletar e-mails" ligado por padrão: confira.
 * - Pontuação do SUS (seção 9): itens 1, 3, 5, 7 e 9 = resposta − 1; itens 2, 4, 6, 8 e 10 =
 *   5 − resposta; some tudo e multiplique por 2,5 (nota de 0 a 100; acima de 68 é bom).
 * - Notas na grade (seção 4): o Google exige uma resposta por linha quando a grade é
 *   obrigatória. Se muita gente não jogou todos os minigames, troque "true" por "false" nas
 *   quatro chamadas de grade(...).
 */
