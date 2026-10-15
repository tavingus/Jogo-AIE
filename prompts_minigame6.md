# Minigame 6 — Prompts de arte (ChatGPT)

Use na MESMA conversa dos outros prompts. Anexe a ficha do Golias (seção 2.1 do arquivo principal) e escreva: *"Use the attached character sheet as the exact design reference."* Substitua `[STYLE MASTER]` pelo bloco abaixo.

## 1. PROMPT MESTRE (cole antes de todo prompt)

```
STYLE MASTER — apply to every image:
Pixel art, 16-bit era look (SNES / GBA style), crisp hard pixel edges, NO anti-aliasing, NO blur, NO smooth gradients, NO photorealism, NO 3D render, NO painterly brush strokes. Limited palette of about 32 colors, flat shading with 3 tones per material (light, base, shadow), light coming from the top-left. A 1-pixel dark brown outline (#371F12) around characters and key objects. Warm, saturated, friendly colors of a sunny Brazilian countryside: grass greens (#568E48, #6AA052), sky blue (#5496DE to #B2DEF6), wood brown (#96693C), parchment (#ECDCB2), brick red (#A54A3E), soft blue (#486898). Cozy, educational, family-friendly mood. No gore: blood only as a few small clean red pixels. Chunky pixels, each pixel about 4x4 pixels in the generated image. ABSOLUTELY NO text, letters, numbers, logos or watermarks anywhere. Wide composition that survives a 16:9 crop (keep important content inside the central 16:9 area).
```

---

## O que o jogo precisa (arquivos, pasta `images/minigame6/`)

| Arquivo | O que é | Tamanho final |
|---|---|---|
| `mg6_bg.png` | **só o cenário** (haras, feno no chão), centro livre | 960x540 |
| `mg6_cavalo.png` | cavalo pastando, visão 3/4, **no centro**, fundo transparente | 960x540 (canvas inteiro, cavalo já posicionado) |
| `mg6_cavalo_picada.png` | o mesmo cavalo **surpreso com a picada**, mesma posição e tamanho | 960x540 (canvas inteiro) |
| `fly_correct_1.png`, `fly_correct_2.png` | mosca **hematófaga** (mutuca), clicar | **70x70** cada |
| `fly_wrong_1.png`, `fly_wrong_2.png` | mosca **inofensiva** (doméstica), ignorar | **70x70** cada |

Se `mg6_cavalo.png` não existir, o jogo usa o esquema antigo (cavalo já dentro do `mg6_bg.png`). A imagem de picada só toca se existir.

### Tamanho das moscas e onde elas pousam
- Cada mosca é um PNG de **70x70** (o jogo amplia 2x para 140x140 na tela).
- Elas pousam numa área do **centro** do canvas: o **centro** de cada mosca cai em **x 295 a 665, y 165 a 375** (no canvas 960x540).
- Por isso o **corpo do cavalo deve cobrir mais ou menos essa caixa**: **x ≈ 290 a 670, y ≈ 160 a 380** (≈ 380x220). Assim as moscas sempre pousam em cima do cavalo.
- Se o cavalo ficar menor ou maior que isso, me diga o tamanho e eu ajusto a área de pouso no código (`MG6_SPAWN_AREA`).

---

## 1. Cena: fundo + cavalo pastando + cavalo surpreso

Mantenha a mesma conversa e anexe a ficha do Golias (seção 2.1 do arquivo principal).

### 1a. Fundo — haras com feno no chão (`mg6_bg.png`)
```
[STYLE MASTER]
A peaceful horse farm (haras) paddock at golden hour, wide landscape, pixel art. Wooden fences, a red-roofed stable building and a few trees in the background, a dirt-and-grass ground, and on the ground in the CENTER area a scatter of golden hay, a half-open hay bale, a feed bucket and a small manure-free dirt patch (things that attract flies). A few wildflowers at the edges. The CENTER of the image, about the middle 45% width and middle 50% height, is open and calm with only the ground and loose hay, because a horse sprite will be placed there later. No animals, no people, no text.
```

### 1b. Cavalo pastando, visão 3/4 (`mg6_cavalo.png`)
```
[STYLE MASTER]
The chestnut-bay horse Golias (attached reference), full body, three-quarter view (3/4 view, body angled slightly toward the viewer, head toward the lower left), head lowered grazing on hay on the ground, relaxed, tail resting. Large and clear, centered. Flat solid #00FF00 background, no ground, no shadow, no other objects. No text.
```
O cavalo deve caber em ≈ 380x220 px do canvas 960x540 (veja o tamanho acima).

### 1c. Cavalo surpreso com a picada (`mg6_cavalo_picada.png`)
Peça **na mesma conversa**, anexando a imagem do cavalo pastando:
```
Use the attached image as the exact reference: same horse, same 3/4 body angle, same size and same position in the frame, same colors and pixel-art style. Change ONLY the reaction: the horse has just been bitten by a fly, startled. Head snapped up and turned toward its flank, eyes wide, ears pinned back, nostrils flared, the front hoof slightly lifted, the tail flicking up. A tiny white "pop" burst near the flank (a few small white pixels), NO blood, no wound, no gore. Flat solid #00FF00 background, no ground, no shadow, no text. The silhouette must stay within the same bounding box as the attached image.
```
Dicas:
- Para o efeito "tocar rapidinho" funcionar, o cavalo da picada precisa ficar **no mesmo lugar e na mesma escala** do cavalo pastando (o jogo só troca uma imagem pela outra por 0,7 s).
- Se o GPT mudar o tamanho: `Same image, but keep the horse exactly the same size and position as the attached reference.`

---

## 2. Os dois tipos de mosca (os dois são MOSCAS)

- **Hematófaga:** mutuca (tabanídeo) — corpo robusto, olhos enormes verdes, probóscide cortante.
- **Inofensiva:** mosca-doméstica (*Musca domestica*) — não pica, só lambe. Menor, cinza clara, olhos vermelhos pequenos e **sem probóscide pontuda**.

Cada tipo vira 2 arquivos (duas poses da mesma mosca: asas abertas e asas mais fechadas). Mesmo tamanho e mesma vista (de cima) nas quatro. O jogador precisa distinguir só pela arte: hematófaga = escura, grande, ameaçadora; inofensiva = clara, pequena, "bobinha".

**2a. Hematófaga — mutuca (`fly_correct_1` e `fly_correct_2`):**
```
[STYLE MASTER]
Two versions of the SAME insect on a flat solid #00FF00 background, side by side, same size, seen from above, each centered with equal margin, no text. A horsefly (tabanid), a BLOOD-SUCKING fly: stocky dark grey-brown body, huge iridescent green eyes with stripes, smoky dark wings, and a clearly visible short sharp black proboscis. Menacing look. Version 1: wings spread wide. Version 2: wings half-folded over the body (wing-flap pose). Simple readable silhouette even at tiny size.
```
**2b. Inofensiva — mosca-doméstica (`fly_wrong_1` e `fly_wrong_2`):**
```
[STYLE MASTER]
Two versions of the SAME insect on a flat solid #00FF00 background, side by side, same size (slightly smaller than a horsefly), seen from above, each centered with equal margin, no text. A common housefly, a HARMLESS non-biting fly: slim light grey body with four faint dark stripes on the back, small red eyes, clear transparent pale wings, NO sharp proboscis (only a tiny soft tip), neutral friendly look. Version 1: wings spread wide. Version 2: wings half-folded over the body. Simple readable silhouette even at tiny size.
```
**Se a diferença ficar pouco clara em 70x70:** peça `Make the horsefly darker and bigger, with exaggerated green eyes, and the housefly lighter and smaller with clearly transparent wings.`

**Mais variedade (opcional):** mosca-dos-estábulos (*Stomoxys*, hematófaga, parecida com a doméstica mas com probóscide pontuda) e mosca-varejeira verde ou mosca-da-fruta (inofensivas). Me diga se quer e eu adiciono arquivos no código.

---

## Montagem no Aseprite

1. Cavalo: apague o `#00FF00`, reduza e cole no centro do cenário vazio (960x540) → exporte `mg6_bg.png`.
2. Moscas: apague o verde, corte justo, redimensione para **70x70** (nearest neighbor) → `fly_correct_1/2.png`, `fly_wrong_1/2.png`.
3. Teste em tamanho real: as moscas aparecem a 70x70 no canvas 960x540, então precisam ser legíveis assim, em especial a diferença entre os dois grupos.
