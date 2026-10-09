# Minigame 5 — Prompt para dar uma pose diferente a cada cavalo

Use na MESMA conversa em que o ChatGPT gerou os 5 cavalos consistentes. **Anexe a imagem com os 5 cavalos** (a que ficou boa) e cole o prompt abaixo. Se ele só entregar 1 imagem com os 5 de uma vez, ótimo; se não, peça um por vez com o prompt individual (mais abaixo), anexando sempre a imagem original.

## Prompt (os 5 de uma vez)
```
Use the attached image as the exact design reference for all five horses. Keep each horse's design 100% identical: same coat color, markings, mane, tail, body proportions, pixel-art style, palette and 1-pixel dark outline. Do NOT redesign them.

Now redraw the same five horses, each in a DIFFERENT natural, relaxed pose, so they look alive instead of copy-pasted. Keep all five in a row on a flat solid #00FF00 background, evenly spaced, with no overlap, each fully visible with a little margin, all the same scale (same body size) and all standing on the same invisible ground line (hooves at the same height). No ground, no shadows, no props, no text.

Poses (all side view or slight 3/4 view, facing right, healthy and calm):
(1) black horse with a small white star: standing alert, head raised high, ears forward;
(2) dapple grey horse: head lowered, grazing or sniffing the ground;
(3) palomino horse: one front hoof lifted, a gentle step, head slightly turned toward the viewer;
(4) dark bay horse: relaxed, head at medium height, looking back over its shoulder, tail slightly swishing;
(5) pinto horse: resting one hind leg (hip cocked), neck low and calm, ears relaxed.

The poses must NOT hide the coat color or the markings, and must NOT show any sign of illness (no drooping, no sweating, no wounds). Chunky pixels, crisp hard edges, no anti-aliasing, no blur.
```

## Prompt individual (se precisar refazer só um)
```
Use the attached image as the exact design reference. Redraw ONLY horse number [N] (the [coat description]) in this pose: [pose]. Keep the design, colors, markings, size, pixel-art style and outline exactly the same. Flat solid #00FF00 background, no ground, no shadow, no text. Same scale and same hoof-line height as the original.
```
Troque `[N]`, `[coat description]` e `[pose]` (use as poses da lista acima).

## Dicas de ajuste
- Se a escala variar: `Same image, but make all five horses exactly the same size and put all hooves on the exact same horizontal line.`
- Se a pose esconder a pelagem: `Change the pose so the coat markings are clearly visible.`
- Se ele mudar o desenho: `You changed the design. Keep every horse identical to the attached reference and change only the pose.`
- Prefira todos virados para o MESMO lado (direita), porque o jogo só troca a imagem e a posição fica fixa na esquerda do canvas.

## Para o jogo (arquivos)
Cada cavalo vira `minigame5/cavalo_<n>.png` (n = 1 a 5), canvas 960x540, com o cavalo dentro da caixa x=30–460, y=120–470 e o chão na **mesma altura** nos 5.
