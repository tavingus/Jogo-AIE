# Minigame 1 — Fundo atrás do livro e novas morfologias

Use na MESMA conversa dos outros prompts. Substitua `[STYLE MASTER]` pelo prompt mestre (arquivo `prompts_arte_chatgpt.md`, seção 1).

---

## 1. Fundo (no lugar do vermelho) — `mg1_bg.png`

O livro aberto fica no centro (ocupa mais ou menos x 150–810, y 110–475 do canvas 960x540). O fundo tem que **combinar com o livro** (páginas creme, borda azul-escura) e **não brigar com ele**: um tampo de mesa de madeira escura, com objetos só nas bordas. O vermelho atual compete com o livro.

```
[STYLE MASTER]
Top-down view of a wooden study desk in a veterinary school library, pixel art. Warm dark-brown wooden planks with subtle grain, soft warm lamplight from the top-left with a gentle darker vignette toward the corners. Scattered ONLY near the borders of the image, small and tidy: a brass magnifying glass at the bottom-left, a wooden test-tube rack with three glass tubes (one with a red cap) at the top-right, an inkwell with a quill pen at the bottom-right, a small stack of closed old books at the right edge, a stethoscope curled at the left edge. The CENTER of the image, about the middle 70% of the width and middle 70% of the height, is plain empty wooden desk surface with no objects, because an open book will be placed there later. Keep the top-left area (a title panel goes there) and the top-center and bottom-left strips calm and low in detail. No text, no people, no animals.
```

**Ajustes rápidos**
- Muito detalhe no centro: `Same image, but remove every object from the central 70% so it is plain wood.`
- Escuro demais: `Same image, a bit lighter and warmer, keep the vignette subtle.`
- Estilo diferente do resto: `Match the exact art style, palette and outline of the previous images in this conversation.`

---

## 2. As 5 morfologias (3 já definidas + 2 sugestões novas)

Já definidas: **esférico** (EIAV, a resposta correta), **Ebola** (filamentoso) e **raiva** (bala). Para as outras duas, as silhuetas precisam ser **bem diferentes** das três (esfera, fio e bala) para o jogador distinguir só pela forma. Minhas duas sugestões de vírus zoonóticos:

### Sugestão 1 — POXVÍRUS (ex.: *Monkeypox/Mpox*, família Poxviridae): o "TIJOLO"
- **Forma:** um **retângulo de cantos arredondados** (tijolo), a única opção "quadrada".
- **Característica:** por dentro, um núcleo em formato de **haltere** (duas pontas largas ligadas por uma cintura) e na superfície filamentos enrolados.
- **Zoonose:** o Mpox passa de roedores e primatas para as pessoas.
- **No seu estilo:** retângulo verde de cantos arredondados, pontos vermelhos e um haltere claro no meio.

### Sugestão 2 — FLAVIVÍRUS (ex.: **vírus do Nilo Ocidental**, família Flaviviridae): o "POLIEDRO"
- **Forma:** partícula **icosaédrica**, ou seja, um **polígono de lados retos** (hexágono) com faces geométricas, sem espículas grandes.
- **Característica:** superfície lisa e facetada, parecida com uma bola de futebol/cristal.
- **Zoonose e relevância:** o vírus do Nilo Ocidental passa de aves para cavalos e humanos (por mosquitos). É um vírus de equinos, então combina com o tema do jogo.
- **No seu estilo:** hexágono verde com linhas internas formando triângulos e pequenos pontos vermelhos nos vértices.

**Por que esses dois:** o coronavírus (esfera com coroa de espículas) também é famoso, mas é redondo como o EIAV e poderia confundir. O tijolo e o poliedro são formas únicas.

---

## 3. Prompts para gerar as duas morfologias

Anexe uma das morfologias que você já tem (para copiar o estilo: corpo verde, pontos vermelhos, contorno branco e roxo) e use:

**Poxvírus (tijolo):**
```
Use the attached image as the exact style reference: same pixel-art style, same palette (green body, red spots, white outline), same size and framing, on a flat solid #00FF00 background, no text.
Draw a POXVIRUS particle (Mpox): a BRICK-SHAPED rounded rectangle, wider than tall, green with red spots on the surface and a pale DUMBBELL-shaped core (two wide ends joined by a narrow waist) visible in the middle. Centered, large and clear.
```

**Flavivírus (poliedro):**
```
Use the attached image as the exact style reference: same pixel-art style, same palette (green body, red spots, white outline), same size and framing, on a flat solid #00FF00 background, no text.
Draw a FLAVIVIRUS particle (West Nile virus): an ICOSAHEDRAL particle seen as a green HEXAGON with straight geometric faces, thin lighter lines forming triangular facets inside, a smooth surface with small red dots only at the corners. Centered, large and clear.
```

**Montagem:** cada morfologia vira `morfologia_N.png` (canvas 960x540, vírus já na posição da página esquerda do livro, com o rótulo roxo embaixo, como as outras). A **correta** (esférica, EIAV) é a nº 3.
