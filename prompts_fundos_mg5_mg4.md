# Prompts de fundo — Minigame 5 (triagem/viagem) e Minigame 4 (última fase: IDGA ou ELISA?)

Use a mesma conversa do ChatGPT; cole o PROMPT MESTRE (prompts_arte_chatgpt.md, seção 1) no lugar de `[STYLE MASTER]`.
Peça sempre **960x540, 16:9, pixel art, sem texto**. Depois, no Aseprite, confira se as áreas "calmas" estão vazias.

## 1. Minigame 5 — `minigame5/mg5_bg.png` (960x540)

Layout (o jogo desenha por cima):
- ESQUERDA (x 30–460, y 120–470): o cavalo. Fundo calmo, sem objetos grandes.
- DIREITA (x 500–940): título (y 15–65), barra de tempo (y ~70), papéis do cavalo (y 90–260), 3 botões de destino (y 280–540). Essa coluna precisa ser uma **mesa/superfície lisa e escura** para os papéis e botões aparecerem; decoração só nas bordas.

```
[STYLE MASTER]
Pixel art, 16:9, front view. A farm quarantine/triage checkpoint beside a horse stable. LEFT HALF: a dirt-and-straw ground in front of a wooden fence and an open gate, a few hay bales and a bucket far in the background, calm and EMPTY in the center so a horse sprite can be placed there. RIGHT HALF: a large dark-brown wooden desk seen from the front filling the whole right side, with a smooth, plain, EMPTY surface in its middle. Decorations only at the very edges of the desk: a pen cup and a small stack of folders at the top-right corner, a clipboard hanging on a nail on the wall above the desk, a rubber stamp and an ink pad at the bottom-left of the desk, a small stopwatch in the top-left edge of the desk. No papers on the middle of the desk. No horse, no people, no text, no letters, no numbers.
```

Dica: se a IA encher a mesa, peça "make the center of the desk completely plain and empty".

## 2. Minigame 4, última fase — `minigame4/mg4_bg_teste.png` (960x540) — "IDGA ou ELISA?"

Layout:
- ESQUERDA (x < 480): cena de comparação dos dois exames. O jogo escreve **pontos em (30,20)**, **feedback em (30,465)**; esses cantos ficam calmos.
- DIREITA (x > 500): 5 afirmações (y 150–450). **Totalmente vazia**, parede lisa.
- Duas "metades" bem separadas: IDGA em cima, ELISA embaixo. As duas placas **devem ser reconhecíveis** (e iguais às das fases 2 e 3).

```
[STYLE MASTER]
Pixel art lab bench scene, 16:9, same laboratory as the previous images (light tiled wall, wooden-and-steel bench, light from top left). LEFT HALF ONLY, split into two clearly separated zones: UPPER-LEFT zone (y 60-220): a round Petri dish seen from above with pale-yellow agar gel, one central well and six small wells around it, with thin white precipitation arcs between wells (agar-gel immunodiffusion), and a small blank wooden label plate under it. LOWER-LEFT zone (y 250-420): a microplate reader device with a 96-well plate of yellow-to-orange wells, and a small blank wooden label plate under it. A thin vertical divider line is NOT needed; just keep a gap between the two zones. The top-left corner and the bottom-left corner (y 440-540) are plain bench and calm, no objects. The RIGHT 48% of the image is a plain tiled wall, completely EMPTY, no objects, no shelves, reserved for menu options. No text, no letters, no numbers.
```

Rótulos: o jogo/arte final escreve "IDGA" e "ELISA" nas plaquinhas (ou você escreve no Aseprite).
Observação científica: no IDGA real as linhas são de precipitação **retas ou levemente curvas entre poços**; se a referência do laboratório for diferente, siga a do laboratório.
