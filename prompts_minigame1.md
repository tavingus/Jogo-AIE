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

## 2. Duas novas morfologias de vírus zoonóticos (opções do jogo)

Hoje a opção correta é a do **EIAV** (lentivírus): partícula **esférica e envelopada, com um cerne em forma de cone (cônico)** por dentro. Para o jogador distinguir só pela forma, as outras opções precisam ter silhuetas **bem diferentes** entre si. A morfologia "filamentosa" já existe (lembra o Ebola/Marburg), então sugiro estas duas:

### Sugestão A — Vírus da RAIVA (*Lyssavirus*, família Rhabdoviridae)
- **Forma:** "bala de revólver": um cilindro alongado com **uma ponta arredondada e a outra reta**.
- **Característica:** espículas curtas cobrindo a superfície, e dentro um fio enrolado (o RNA com a nucleoproteína) em espiral.
- **Zoonose clássica:** cães, morcegos e herbívoros (inclusive equinos) transmitem raiva ao ser humano.
- **Como desenhar no seu estilo (corpo verde com pontos vermelhos):** um "projétil" deitado, ponta redonda à direita e base reta à esquerda, pontos vermelhos de espículas por toda a superfície.

### Sugestão B — CORONAVÍRUS (família Coronaviridae)
- **Forma:** esfera com **uma "coroa" de espículas grandes em forma de clava** (daí o nome *corona*).
- **Característica:** espículas claramente maiores e mais espaçadas que as de outros vírus, com a ponta bulbosa.
- **Zoonose:** SARS-CoV, MERS-CoV e SARS-CoV-2 vieram de animais (morcegos, camelos).
- **Atenção:** é redondo como o EIAV, mas as espículas em clava por fora e o interior liso o diferenciam do cone do EIAV.
- **No seu estilo:** esfera verde com **bastões vermelhos de ponta arredondada** saindo ao redor (como um sol ou uma coroa).

### Alternativa C — POXVÍRUS (ex.: *Monkeypox/Mpox*, família Poxviridae)
- **Forma:** "**tijolo**" retangular com cantos arredondados, bem diferente de todos os outros.
- **Característica:** corpo de dentro em formato de haltere (halteres) e superfície com filamentos enrolados.
- **Zoonose:** o Mpox passa de animais para pessoas.
- **No seu estilo:** retângulo verde de cantos arredondados, com pontos vermelhos e um "haltere" claro no meio.

**Minha recomendação:** use **A (Raiva)** e **B (Coronavírus)**: são os mais conhecidos pelos estudantes e têm silhuetas muito diferentes do EIAV e do filamentoso.

---

## 3. Prompts para gerar as duas morfologias

Anexe uma das morfologias que você já tem (para copiar o estilo: corpo verde, pontos vermelhos, contorno branco e roxo) e use:

**A — Raiva (bala):**
```
Use the attached image as the exact style reference: same pixel-art style, same palette (green body, red spots, white outline), same size and framing, on a flat solid #00FF00 background, no text.
Draw a RABIES VIRUS particle (a rhabdovirus): a BULLET-SHAPED capsule lying horizontally, one end rounded and the other end flat, with short red spikes dotted over its whole surface, and a faint coiled strand visible inside. Centered, large and clear.
```

**B — Coronavírus (coroa):**
```
Use the attached image as the exact style reference: same pixel-art style, same palette (green body, red spots, white outline), same size and framing, on a flat solid #00FF00 background, no text.
Draw a CORONAVIRUS particle: a round green sphere with a CROWN of large club-shaped red spikes with rounded bulb tips radiating all around it, evenly spaced and clearly bigger than the spots of the attached image. Centered, large and clear.
```

**Montagem:** cada morfologia vira `morfologia_N.png` (canvas 960x540, vírus já na posição da página esquerda do livro, rótulo roxo com o nome embaixo, como as outras). A **correta** continua a nº 3 (`MG1_MORPH_CORRECT`); se você adicionar morfologias novas, me diga quantas são e eu atualizo a lista do código (`MG1_MORPH_FILES`).
