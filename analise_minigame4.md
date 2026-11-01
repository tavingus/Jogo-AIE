# Análise completa do minigame 4 (IDGA e ELISA)

> **Aviso importante sobre esta análise:** eu **não sou fonte científica**. Tudo o que está aqui sobre IDGA e ELISA vem do meu conhecimento geral e de como o jogo foi escrito, **e pode conter erros**. Para um conteúdo que "não pode estar errado", cada item marcado como **VERIFICAR** precisa ser conferido pelo pessoal do laboratório contra uma fonte oficial (ver seção 7). O objetivo aqui é achar os pontos de risco e propor correções, não dar a palavra final.

---

## 1. A crítica recebida: "Erro no IDGA, fraco positivo como negativo"

**O que provavelmente aconteceu (e a minha parte nisso).**
- O jogo tem uma regra de 2 respostas para cada poço do IDGA (**positivo** ou **negativo**), e o gabarito fixo é: poço 1 positivo, **poço 2 negativo (Golias)**, poço 3 positivo.
- A arte da placa que você desenhou seguiu o **esquema de leitura que eu fiz**, a partir do que eu lembrava: no poço negativo, as linhas dos controles terminam **se curvando levemente em direção ao poço**, sem se ligar a ele.
- **Esse esquema veio da minha memória e não foi verificado.** Em IDGA, **a curvatura (deflexão) das linhas dos controles é justamente um dos sinais usados para identificar um "fraco positivo"** (do meu conhecimento geral; VERIFICAR). Ou seja: provavelmente eu desenhei como "negativo" um padrão que quem conhece IDGA lê como "fraco positivo". É a causa mais provável da crítica, e a responsabilidade pelo esquema foi minha.

**Dois problemas, não um:**
1. **A arte do negativo pode estar tecnicamente errada** (ver acima).
2. **O jogo não tem a categoria "fraco positivo" (nem "inconclusivo")**. Na rotina real, a leitura do IDGA costuma ter pelo menos: positivo, negativo e uma categoria intermediária (fraco positivo/duvidoso/inconclusivo) com conduta própria (repetir, retestar). Forçar tudo em 2 opções faz qualquer padrão intermediário parecer "erro do jogo".

**O que eu recomendo (precisa de validação do laboratório):**
- **Pedir ao laboratório uma imagem de referência real** de cada padrão: positivo forte, fraco positivo e negativo verdadeiro (do manual do kit/POP interno). Redesenhar a placa seguindo essas imagens, não o meu esquema.
- **Decidir o escopo do jogo:** (a) manter só positivo/negativo, mas usando apenas casos **inequívocos** (positivo forte e negativo verdadeiro, sem deflexão nem linha tênue); ou (b) incluir "fraco positivo" como terceira opção, com a explicação e a conduta (por exemplo, "repetir o teste / confirmar").
- Até isso ser validado, **retirar do jogo qualquer padrão ambíguo** (o negativo com pontas curvas).

---

## 2. Auditoria do conteúdo, fase por fase

Legenda: ✅ coerente com o que eu sei (ainda assim, confirmar) · ⚠️ **VERIFICAR** (risco de estar errado ou simplificado demais) · ❌ provável problema.

### Fase 1 — Imunocomplexo (antígeno + anticorpos)
| Afirmação no jogo | Avaliação |
|---|---|
| p26 = proteína do capsídeo do EIAV | ✅ |
| gp90 = glicoproteína do envelope; gp45 = glicoproteína transmembrana | ✅ (VERIFICAR a nomenclatura que o laboratório usa: gp90/SU e gp45/TM) |
| Anticorpos "errados": anti-hemaglutinina (influenza equina), anti-glicoproteína (herpesvírus equino), anti-proteína E (vírus do Nilo Ocidental) | ✅ conceitualmente; ⚠️ "anti-glicoproteína" é vago: o herpesvírus tem várias glicoproteínas |
| "O IDGA detecta principalmente o anti-p26" | ✅ ⚠️ VERIFICAR com o antígeno do kit usado |
| Os 3 anticorpos "se encaixam no vírus" | ⚠️ **Simplificação didática.** O jogador pode concluir que o IDGA detecta os três. No IDGA o antígeno é sobretudo a p26; gp45 aparece em alguns ELISAs; gp90 não é o alvo de rotina. O feedback já diz isso, mas o enunciado da fase não |
| "Imunocomplexo" como base dos testes | ✅ conceito geral (antígeno + anticorpo) |

### Fase 2 — Leitura do IDGA
| Item | Avaliação |
|---|---|
| Layout: poço central de antígeno, controles positivos e amostras alternados em hexágono | ✅ (padrão da técnica; VERIFICAR nº de poços e disposição do kit) |
| Positivo = linha de precipitação que se une (identidade) à dos controles | ✅ |
| **Negativo = "não se forma linha"** | ⚠️ A explicação do jogo é incompleta: um negativo também se reconhece pelo **comportamento das linhas dos controles** (continuidade/forma), não só pela "ausência de linha" |
| **Fraco positivo / inconclusivo** | ❌ **Ausente.** Principal fonte da crítica |
| Gabarito fixo (1 positivo, 2 negativo, 3 positivo) | ⚠️ Sempre igual: o jogador decora. Se mais casos forem adicionados, sortear entre imagens diferentes |
| Tempo de leitura (24 a 48 h) | ⚠️ VERIFICAR (em muitas referências a leitura é feita em 24 h e 48 h; alguns protocolos citam até 72 h) |

### Fase 3 — Leitura do ELISA
| Item | Avaliação |
|---|---|
| Leitor de placas mede a **densidade óptica (DO)** | ✅ |
| **Ponto de corte = DO do controle negativo + 0,20** | ❌ **Regra inventada por mim, como exemplo.** Cada kit define o seu critério (por exemplo, cutoff por controles, razão amostra/controle positivo, índice S/P, faixa "suspeita"). Apresentar isso como regra geral é **cientificamente arriscado** |
| Controles C− e C+ | ⚠️ O jogo não pede para **validar a placa** (conferir se os controles estão dentro do esperado) antes de interpretar. Na prática, se os controles falham, a placa inteira é invalidada |
| Só dois resultados (positivo ou negativo) | ⚠️ Muitos kits têm uma **zona cinzenta/suspeita** perto do corte. Aqui os valores sorteados ficam longe do corte (de propósito), o que é seguro, mas não ensina a lidar com o caso limítrofe |
| Valores fixos (0,08 / 1,41 / 0,05 / 1,15 / 0,78 / 0,09) | ✅ coerentes entre si; ⚠️ são **valores de exemplo**, não de um kit real |

### Fase 4 — "IDGA ou ELISA?"
| Afirmação | Avaliação |
|---|---|
| "Teste oficial de referência, leitura visual das linhas" → IDGA | ✅ no contexto brasileiro (MAPA); ⚠️ em termos internacionais o **ELISA também é um teste reconhecido** (VERIFICAR o texto da norma e dizer "no Brasil") |
| "Reação de cor lida em espectrofotômetro (DO)" → ELISA | ✅ |
| "Mais sensível e automatizável, ideal para triagem" → ELISA | ✅ (VERIFICAR) |
| "Resultado em 24 a 48 horas em gel de ágar" → IDGA | ⚠️ VERIFICAR (ver acima) |
| "Positivo na triagem deve ser confirmado por este teste (IDGA)" | ⚠️ VERIFICAR na **norma vigente do MAPA** (programa de controle da AIE) |

---

## 3. Sobre colocar o ELISA antes do IDGA (sugestão que você recebeu)

**Eu concordo, por 3 motivos:**
1. **Coerência com a prática (no Brasil):** o ELISA costuma ser o teste de **triagem** e o IDGA o de **confirmação** (isso aparece na própria fase 4: "positivo na triagem deve ser confirmado pelo IDGA"). Ensinar na ordem em que se usa evita contradição.
2. **Curva de dificuldade:** o ELISA é **numérico** (comparar DO com o corte) e mais fácil; o IDGA é **visual** e o mais difícil e polêmico. Começar pelo mais fácil dá confiança e deixa a parte arriscada para depois que o jogador já entendeu "positivo/negativo".
3. **Narrativa:** a amostra do Golias passa primeiro pela triagem e, se houver suspeita, é confirmada. Dá para ligar os casos: amostras **positivas** no ELISA seguem para o IDGA.

**Como seria (é uma mudança pequena no código):** ordem das fases = imunocomplexo → **ELISA** → **IDGA** → "IDGA ou ELISA?". Eu ajustaria também o tutorial e os textos ("leia o ELISA e depois o IDGA"). As artes não mudam (cada fundo é indicado pelo nome da fase).

**Ideia melhor ainda (opcional):** fazer os poços do IDGA corresponderem às **amostras positivas do ELISA**, para o jogador acompanhar uma mesma amostra nas duas técnicas.

---

## 4. Análise de jogo (não só de ciência)

**O que funciona**
- A fase 1 (anticorpos) dá a intuição do imunocomplexo e é lúdica.
- A revisão final com explicação por item é um bom recurso de aprendizado.

**Problemas de design**
1. **Gabarito fixo no IDGA:** a placa é sempre a mesma → memorização, não aprendizado. Ideal: 3 a 5 placas diferentes sorteadas.
2. **O ELISA tem números sorteados/fixos, mas uma única regra de corte** → o jogador aprende "compare com 0,28", não o raciocínio (validar controles, aplicar o critério do kit).
3. **Duas respostas só (positivo/negativo)** para um exame que tem casos intermediários.
4. **A fase 1 não conversa com as fases 2 e 3** (os 3 anticorpos somem; o IDGA e o ELISA aparecem sem ligação). Sugestão: ligar com um texto de transição ("o soro positivo contém esses anticorpos").
5. **Pontuação:** 30 pontos na fase 1 e 5 em cada campo → o jogador pode errar vários itens das fases difíceis e ainda ir bem por causa das fáceis. Considerar pesos.
6. **Quantidade de texto:** a fase 4 tem 5 afirmações longas; no celular/tela pequena fica pesado (e o jogo é em tela de PC; revisar a legibilidade).

---

## 5. Plano de correção (em ordem de prioridade)

**URGENTE (conteúdo)**
1. **Retirar ou corrigir a arte do negativo** com a imagem de referência do laboratório.
2. **Corrigir/rotular a regra do ELISA:** substituir "controle negativo + 0,20" pela regra de um kit real **ou** deixar explícito no jogo: "Neste jogo, o ponto de corte é o **exemplo** abaixo; cada kit define o seu" (o texto atual não diz isso).
3. **Acrescentar a validação dos controles** no ELISA (uma pergunta antes: "a placa é válida?"), se o laboratório achar relevante.
4. **Revisar as afirmações marcadas ⚠️ VERIFICAR** na fase 4 (tempo de leitura, "oficial", confirmação pelo IDGA) com a norma do MAPA.

**IMPORTANTE (jogo)**
5. **Inverter a ordem: ELISA primeiro.**
6. **Decidir sobre "fraco positivo/inconclusivo"** (nova opção com explicação e conduta) ou manter apenas casos inequívocos.
7. **Mais de uma placa de IDGA e mais de um conjunto de ELISA** sorteados.

**DESEJÁVEL**
8. Ligar a fase 1 às fases 2 e 3 com texto de transição.
9. Rebalancear a pontuação por fase.

---

## 6. O que eu preciso de você (para fazer as correções)
1. **Imagens de referência** do laboratório: IDGA positivo, fraco positivo e negativo; e (se existir) o POP/manual do kit de ELISA.
2. **A regra de corte e de validação** do ELISA que o laboratório usa (ou o nome do kit).
3. **A norma do MAPA** (ou o texto de referência) que o laboratório segue para a confirmação e o tempo de leitura.
4. **Decisão:** ELISA primeiro? "Fraco positivo" entra como opção?
5. **Qual poço** (1, 2 ou 3) foi o alvo da crítica (se os críticos disseram).

## 7. Onde conferir (fontes que eu recomendo, sem citar páginas de memória)
- **WOAH (OIE) Terrestrial Manual**, capítulo "Equine infectious anaemia": descreve AGID/IDGA e ELISA e a interpretação (positivo, fraco positivo, negativo).
- **Norma vigente do MAPA** para o diagnóstico e o controle da AIE (testes oficiais, confirmação, prazos).
- **Manual do kit** de IDGA e do kit de ELISA usados no laboratório (critério de corte e validação).
- **POP interno do laboratório.**

*Como eu não consigo abrir essas fontes daqui nem validar uma imagem real, qualquer afirmação científica acima deve passar pela revisão de quem trabalha com o diagnóstico.*
