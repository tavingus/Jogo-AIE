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

### Regra de ouro da fase 1: a arte NÃO pode entregar a resposta
O desafio é **saber** quais anticorpos reconhecem o vírus da AIE (anti-p26, anti-gp90, anti-gp45), lendo o nome. Por isso:
- **Os 6 anticorpos são visualmente IDÊNTICOS** (mesmo Y, mesmas cores, mesmas pontas). Só o **texto** do cartão diferencia.
- **O vírus tem 3 encaixes iguais** (todos do mesmo formato), sem formas diferentes.
- O "encaixar" só aparece **depois** do clique, nas artes `acoplado_*` e `mg4_complexo` (e, se errar, no overlay vermelho `mg4_errado_*`).

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
On a flat solid #00FF00 background, a single cute-but-neutral virus particle seen from the side, large and centered: a round purple body (#7a4a9a, light #a070c0, shadow #4f2d68) with small spikes all around, no mouth, two small simple eyes optional. On the RIGHT edge of its body, exactly three identical rounded notches (docking sockets) stacked vertically and evenly spaced, all the SAME shape and size, with a dark interior. Do not draw any antibody. No text.
```
Posição final: centro do vírus ≈ (95, 262); os encaixes ficam em x≈150 e y≈192, 262 e 332. Ajuste no Aseprite.

### 2.3 Os 6 anticorpos (sprite) — todos IGUAIS
```
[STYLE MASTER]
On a flat solid #00FF00 background, ONE antibody molecule, a simple cute Y shape, pale-blue-and-white body (#cfe4f5 base, #8fb8dc shadow, 1-pixel dark outline), no face, with two small round blue tips (#4880c8) at the ends of the two arms. Centered, large and clear, no text.
```
Gere **uma vez** e use a mesma imagem nos 6 cartões (`anticorpo_1…6`), só mudando o texto do nome. Nada de cor ou forma diferente por anticorpo.

### 2.4 Anticorpo encaixado e imunocomplexo (sprites)
```
[STYLE MASTER]
Using the attached virus and antibody designs exactly, on a flat solid #00FF00 background: the purple virus on the left with THREE pale-blue Y antibodies attached to its three right-side sockets (each blue round tip fitted into a socket), the antibody bodies extending to the right. Small happy sparkle pixels and a soft golden glow around the junctions to show the immune complex is formed. Clean, centered, no text.
```
Use essa imagem para `mg4_complexo.png` (região ≈ x 70–380, y 140–380) e **recorte um anticorpo de cada vez** do mesmo desenho para `acoplado_2/3/5.png` (cada um na posição do seu encaixe: x 150–260; y 165, 235, 305).

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
- `anticorpo_<n>.png` — cartão (moldura madeira) com o anticorpo da seção 2.3 + texto do nome; 2 colunas × 3 linhas na coluna da direita (cada cartão ≈ 215x90).
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
- [ ] Vírus com 3 encaixes iguais; os 6 anticorpos IDÊNTICOS (a arte não revela os corretos)
- [ ] IDGA: linhas conforme o layout (amostras 1 e 3 positivas, 2 negativa)
- [ ] ELISA: 6 poços neutros nas posições x = 80…430, y = 350
- [ ] Tudo em 960x540, nomes de arquivo como na tabela acima
