# Minigame 6 — Prompts de arte (ChatGPT)

Use na MESMA conversa dos outros prompts. Anexe a ficha do Golias (seção 2.1 do arquivo principal) e escreva: *"Use the attached character sheet as the exact design reference."* Substitua `[STYLE MASTER]` pelo bloco abaixo.

## 1. PROMPT MESTRE (cole antes de todo prompt)

```
STYLE MASTER — apply to every image:
Pixel art, 16-bit era look (SNES / GBA style), crisp hard pixel edges, NO anti-aliasing, NO blur, NO smooth gradients, NO photorealism, NO 3D render, NO painterly brush strokes. Limited palette of about 32 colors, flat shading with 3 tones per material (light, base, shadow), light coming from the top-left. A 1-pixel dark brown outline (#371F12) around characters and key objects. Warm, saturated, friendly colors of a sunny Brazilian countryside: grass greens (#568E48, #6AA052), sky blue (#5496DE to #B2DEF6), wood brown (#96693C), parchment (#ECDCB2), brick red (#A54A3E), soft blue (#486898). Cozy, educational, family-friendly mood. No gore: blood only as a few small clean red pixels. Chunky pixels, each pixel about 4x4 pixels in the generated image. ABSOLUTELY NO text, letters, numbers, logos or watermarks anywhere. Wide composition that survives a 16:9 crop (keep important content inside the central 16:9 area).
```

---

## O que o jogo precisa (arquivos)

| Arquivo | O que é | Tamanho final |
|---|---|---|
| `minigame6/mg6_bg.png` | fundo cheio com o cavalo central já posicionado | 960x540 |
| `minigame6/fly_correct_1.png`, `fly_correct_2.png` | moscas **hematófagas** (o jogador clica) — mutuca | 70x70 cada |
| `minigame6/fly_wrong_1.png`, `fly_wrong_2.png` | moscas **inofensivas** (o jogador ignora) — mosca-doméstica | 70x70 cada |

As moscas são sprites individuais com fundo transparente (não são canvas inteiro). O fundo (cenário + cavalo) você monta no Aseprite juntando o cenário vazio com o cavalo, nos 960x540 de sempre.

---

## 1. Cavalo central (sprite) — Golias relaxado

Dois prompts: um sprite isolado e, se quiser, o cenário vazio para você montar a composição.

**1a. Cavalo sozinho (fundo verde para recortar):**
```
[STYLE MASTER]
The chestnut-bay horse Golias (attached reference) standing relaxed, perfectly SIDE VIEW facing right, full body visible with a little margin around, head slightly lowered, one ear flicking, tail swishing to one side as if shooing a fly. Large and clear, centered, on a flat solid #00FF00 background. No ground, no shadow, no other objects. No text.
```
**1b. (opcional) Mesma pose, 2 variações para dar vida (cauda para cima e cauda para baixo):**
```
[STYLE MASTER]
Same horse, same pose and size as the attached image, two versions side by side on a flat solid #00FF00 background: (left) tail raised mid-swish, (right) tail down and still, head a little higher. Identical body, only tail and head differ. No text.
```
**1c. Cenário vazio (onde você coloca o cavalo no centro):**
```
[STYLE MASTER]
A peaceful farm pasture at golden hour, wide landscape, tall grass, a few wildflowers, a wooden fence and blue mountains in the distance, soft warm light. The CENTER of the image is open, calm and empty (nothing in the middle 40%), so a horse can be placed there later. No animals, no people, no text.
```

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
