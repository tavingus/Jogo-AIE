# Minigame 4 — Direção de arte + prompts (IDGA e ELISA)

Consistência: use a **mesma conversa** do ChatGPT dos outros prompts, cole o **PROMPT MESTRE** (arquivo `prompts_arte_chatgpt.md`, seção 1) no lugar de `[STYLE MASTER]`, e anexe a ficha do Golias e do veterinário quando eles aparecerem.
Coordenadas abaixo são do canvas final **960x540**. O jogo escreve por cima: pontos (30,20), números de DO, ponto de corte (30,420) e feedback (30,465, largura ~430). Esses cantos precisam ficar **calmos/sem detalhes**. A coluna da direita (x > 500) é das opções: sempre vazia.

---

## 1. Direção de arte (o conceito)

O minigame tem 4 fases e **2 "mundos"**:

| Fase | Mundo | Sensação |
|---|---|---|
| 1. Imunocomplexo | **Microscópico** ("zoom na amostra do Golias") | Lúdico, brilhante, cores mais frias/azuladas |
| 2. Ler o IDGA | **Bancada**, placa de ágar de cima | Científico, limpo, translúcido |
| 3. Ler o ELISA | **Bancada**, leitor de placas | Digital, números (o jogo escreve) |
| 4. IDGA ou ELISA? | **Bancada**, as duas placas lado a lado | Comparação |

Regras visuais para tudo ficar da mesma família:
- **Mesmo laboratório** nas fases 2, 3 e 4: mesmos azulejos claros, mesma bancada de madeira/inox, mesma luz de cima à esquerda.
- **Linguagem de cores dos exames:** IDGA = gel **amarelo-pálido** com linhas **brancas**; ELISA = cor **amarelo → laranja**; amostra do Golias = **tubo de tampa vermelha** (o mesmo do minigame 3); antígeno/vírus = **roxo**; anticorpos = **azul-claro/branco** em forma de **Y**.
- **Lúdico, não gore:** o vírus é um "monstrinho" redondo com espinhos e uma carinha neutra (olhos pequenos) ou sem rosto, nunca assustador.
- **Sprites e fundos separados** (a IA erra posições exatas): gere fundos vazios e sprites em fundo verde `#00FF00`; você posiciona no Aseprite pelas coordenadas.

### A mecânica "chave e fechadura" da fase 1 (ideia de design)
O vírus (antígeno) tem **3 encaixes de formas diferentes**: ▲ triângulo, ● círculo, ■ quadrado. Cada anticorpo tem uma **ponta colorida com uma forma**. Os 3 anticorpos corretos (os nº 2, 3 e 5) têm as pontas **▲ ● ■** que **combinam** com os encaixes; os 3 errados (nº 1, 4 e 6) têm formas que **não existem no vírus** (estrela ★, losango ◆, meia-lua ☾). Assim o jogador descobre a ideia de especificidade antígeno–anticorpo brincando. **Cada cartão leva o NOME do anticorpo** (ex.: "Anticorpo anti-p26"), mas **sem a doença/vírus** entre parênteses (nada de "EIAV", "influenza", "herpesvírus"): o jogador aprende o nome e a forma, e a explicação (de qual vírus é cada proteína) vem depois do clique.

Mapeamento (a ordem dos encaixes é de cima para baixo):

| Encaixe do vírus | Forma | Anticorpo que encaixa |
|---|---|---|
| 1 (alto) | ▲ triângulo | `anticorpo_2` (anti-p26) |
| 2 (meio) | ● círculo | `anticorpo_3` (anti-gp90) |
| 3 (baixo) | ■ quadrado | `anticorpo_5` (anti-gp45) |
| — | ★ estrela | `anticorpo_1` (errado) |
| — | ◆ losango | `anticorpo_4` (errado) |
| — | ☾ meia-lua | `anticorpo_6` (errado) |

**Cores das pontas (as mesmas dos cartões de teste do jogo):** 1 ★ amarelo · 2 ▲ roxo · 3 ● laranja · 4 ◆ verde · 5 ■ vermelho · 6 ☾ rosa. Corpo do Y: azul-claro `#cfe4f5` com sombra `#8fb8dc`.

---

## 2. FASE 1 — Imunocomplexo (mundo microscópico)

### 2.1 Fundo (`mg4_bg_dock.png`) — a "lente do microscópio"
```
[STYLE MASTER]
A magnified microscope view of a blood serum sample, pixel art: a deep soft-blue (#486898) background with a subtle darker vignette like a microscope lens, tiny pale floating particles and a few small round blood-cell silhouettes drifting in the background, very low contrast so sprites stand out. The RIGHT 48% of the image is calmer and slightly lighter with almost no particles, reserved for menu cards. Bottom-left and top-left corners are calm and plain (text will be added there). No virus, no antibodies, no text.
```

### 2.2 Vírus / antígeno (sprite)
```
[STYLE MASTER]
On a flat solid #00FF00 background, a single cute-but-neutral virus particle seen from the side, large and centered: a round purple body (#7a4a9a, light #a070c0, shadow #4f2d68) with small spikes all around, no mouth, two small simple eyes optional. On the RIGHT edge of its body, three clear notches (docking sockets) stacked vertically and evenly spaced, each with a DIFFERENT shape, from top to bottom: (1) a triangle socket, (2) a circle socket, (3) a square socket. The three sockets must be large, clear, high-contrast (dark interior) and about the same size. Do not draw any antibody. No text.
```
Posição final: centro do vírus ≈ (95, 262); os encaixes ficam em x≈150 e y≈192 (▲), 262 (●), 332 (■). Ajuste no Aseprite.

### 2.3 Os 6 anticorpos (sprites)
```
[STYLE MASTER]
On a flat solid #00FF00 background, six antibody molecules in a 3 columns x 2 rows grid, evenly spaced, identical Y shape and size, all with the same pale-blue-and-white body (#cfe4f5 base, #8fb8dc shadow, 1-pixel dark outline), simple and cute, no faces. The only difference is the colored TIP of the two arms (the part that binds), each tip has a different clearly readable shape and color, shown pointing to the right:
row 1: (1) a yellow STAR tip, (2) a purple TRIANGLE tip, (3) an orange CIRCLE tip;
row 2: (4) a green DIAMOND tip, (5) a red SQUARE tip, (6) a pink CRESCENT-MOON tip.
Tips must be large and crisp. No text.
```
Observação: **a numeração da grade = números dos arquivos** `anticorpo_1…6`. As cores das pontas dos corretos (2,3,5) precisam combinar com a "cor interna" dos encaixes do vírus; se não combinarem, repinte no Aseprite (use as mesmas formas ▲ ● ■).

### 2.4 Anticorpo encaixado e imunocomplexo (sprites)
```
[STYLE MASTER]
Using the attached virus and antibody designs exactly, on a flat solid #00FF00 background: the purple virus on the left with THREE pale-blue Y antibodies attached to its three right-side sockets (top: triangle tip fitted in the triangle socket, middle: circle tip in the circle socket, bottom: square tip in the square socket), the antibody bodies extending to the right. Small happy sparkle pixels and a soft golden glow around the junctions to show the immune complex is formed. Clean, centered, no text.
```
Use essa imagem para montar o **fundo inteiro** `mg4_bg_complexo.png` (960x540: a mesma cena do `mg4_bg_dock`, só que com o vírus e os 3 anticorpos acoplados e o brilho; ele substitui o fundo da fase 1 quando o complexo se forma). E **recorte um anticorpo de cada vez** do mesmo desenho para `acoplado_2/3/5.png` (cada um na posição do seu encaixe: x 150–260; y 165, 235, 305).

---

## 3. FASE 2 — Ler o IDGA (`mg4_bg_idga.png`)

**Layout exato** (olhando a placa de cima; o jogo e a arte precisam bater):
- Poço central = **antígeno**.
- 6 poços periféricos em hexágono, alternando **controle positivo (C+)** e **amostra**: topo = C+, depois sentido horário: **amostra 1**, C+, **amostra 2**, C+, **amostra 3**. Os números 1, 2, 3 nas amostras (e "C+" nos controles) você escreve no Aseprite.
- **Linhas de precipitação** (finos arcos brancos), exatamente assim:
  - Amostra 1 (**positiva**) e amostra 3 (**positiva**): o arco do antígeno até a amostra **se une ao arco dos controles vizinhos**, formando uma linha contínua (linha de identidade).
  - Amostra 2 (**negativa**): **nenhum arco** chega até ela; os arcos dos controles vizinhos só se curvam em direção à amostra sem se ligar.

**Passo 1 — Placa sem linhas (prompt):**
```
[STYLE MASTER]
Top-down close-up of an agar-gel immunodiffusion Petri dish on a clean lab bench, pixel art. A round glass dish with a translucent pale-yellow gel. ONE central well and SIX peripheral wells in a perfect hexagon around it, all wells the same size, slightly darker than the gel with a thin outline. NO precipitation lines, NO writing. The dish fills the left 52% of the image and its center sits at about 28% from the left and 50% from the top. Soft light from the top-left, glass highlight on the rim. Left and bottom edges calm. The RIGHT 48% is plain light wooden/stainless bench, EMPTY. A red-capped serum tube (Golias sample) and a pipette rest at the bottom edge, small. No text.
```
**Passo 2 — Linhas (você faz no Aseprite, 3 minutos):** pincel de 1 px, cor `#fff6dc`, desenhe 3 arcos fininhos do poço central em direção a cada amostra/controle, seguindo o layout acima. (A IA não acerta esse padrão; manualmente fica correto e é isso que o jogador precisa ler.) Se quiser tentar com a IA mesmo assim, use só como referência de estilo:
```
Same image, add thin white arcs in the gel following this exact pattern: ... [descreva a lista acima]. Keep everything else unchanged.
```

---

## 4. FASE 3 — Ler o ELISA (`mg4_bg_elisa.png`)

O jogo escreve **6 valores de DO** alinhados em y=350, em x = **80, 150, 220, 290, 360, 430** (C−, C+, Amostras 1 a 4) e o **ponto de corte** em (30, 420). Por isso: 6 poços em fila nessas posições e 6 "mostradores" em branco logo abaixo.

**Importante:** como os valores mudam a cada partida, a cor dos poços **não pode ser mostrada** no fundo (senão contradiz o número). Desenhe os 6 poços em tom **neutro/pálido**.

```
[STYLE MASTER]
Front view of a microplate reader (spectrophotometer) on a clean lab bench, pixel art. The reader is a boxy gray-blue device filling the left 52% of the image. A slide-out tray holds ONE straight row of exactly SIX round microplate wells, evenly spaced, centered horizontally from about 8% to 45% of the image width and at about 45% of the image height. The six wells are all the SAME pale neutral color (light clear/pale amber, no color gradient). Directly below the row, a dark digital display strip with SIX empty blank slots aligned under each well (screen glass, no digits, no text). Small buttons and a status LED on the reader are fine. The bottom-left 25% of the image is calm and plain. The RIGHT 48% of the image is plain bench/tiled wall, EMPTY. A pipette and a red-capped tube sit small at the far left edge. No text, no numbers.
```

---

## 5. FASE 4 — IDGA ou ELISA? (`mg4_bg_teste.png`)

Cena de comparação: os dois exames lado a lado (você escreve "IDGA" e "ELISA" nos rótulos).
```
[STYLE MASTER]
Lab bench scene, pixel art, front view, in the left 50% of the image: on the upper left a Petri dish with pale-yellow agar gel and thin white arcs (agar-gel immunodiffusion), on the lower left a microplate reader device with a plate of orange-yellow wells (ELISA). Two empty blank wooden label plates, one under each, no text. Clean tiled wall and bench consistent with the previous lab images. The bottom-left corner is calm and plain. The RIGHT 48% of the image is plain tiled wall, EMPTY, reserved for menu options. No text.
```

---

## 6. Telas comuns do minigame 4 (consistência com o resto do jogo)

Essas você faz no Aseprite com o kit de UI (botões e painéis madeira/pergaminho dos outros minigames) para ficar igual:
- `mg4_fase_<dock|idga|elisa|teste>.png` — título + enunciado (painel pergaminho no canto superior direito, ≈ x 500–940, y 85–140).
- `anticorpo_<n>.png` — cartão (moldura madeira) com o anticorpo da seção 2.3 à esquerda + o nome (só "Anticorpo anti-…") à direita; 2 colunas × 3 linhas na coluna da direita (cada cartão ≈ 215x90).
- `idga_<1-3>_*`, `elisa_<1-4>_*`, `teste_<1-5>_*` — campos de resposta (`vazio`, `positivo`/`negativo`, `idga`/`elisa`).
- `mg4_ligado_n`, `mg4_errado_n`, `mg4_campo_certo_n`, `mg4_campo_errado_n` — overlays verde/vermelho.
- Botões `mg4_confirmar_*`, `mg4_seguir_*`, `mg4_continuar_*`, `mg4_close_*`, painéis `mg4_resultado`, `mg4_instructions_*`: reaproveite o estilo dos minigames 1–3 (já gerei os placeholders no kit de UI).

## 7. Ajustes rápidos
- Se o laboratório mudar de estilo entre as imagens: `Match the exact lab style, tiles, bench and palette of the previous lab image in this conversation.`
- Se aparecer texto: `Same image with ALL text, letters and numbers removed (blank surfaces).`
- Se a placa sair torta: `Same image, but make the dish a perfect circle and the six wells a perfect regular hexagon around the center well.`
- Se o vírus assustar: `Make the virus rounder, cuter and friendlier, simple shapes, no teeth.`
- Para recortar: apague `#00FF00` no Aseprite (varinha, tolerância 0).

## 8. Checklist
- [ ] Fundos sem texto; cantos esquerdos calmos; coluna direita vazia
- [ ] Vírus com os 3 encaixes ▲ ● ■ visíveis; anticorpos 2, 3, 5 com as pontas que combinam
- [ ] IDGA: linhas conforme o layout (amostras 1 e 3 positivas, 2 negativa)
- [ ] ELISA: 6 poços neutros nas posições x = 80…430, y = 350
- [ ] Tudo em 960x540, nomes de arquivo como na tabela acima
