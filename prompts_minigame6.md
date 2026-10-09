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
| `minigame6/fly_correct_1.png`, `fly_correct_2.png` | moscas **hematófagas** (o jogador clica) | 70x70 cada |
| `minigame6/fly_wrong_1.png`, `fly_wrong_2.png` | moscas **inofensivas** (o jogador ignora) | 70x70 cada |

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

## 2. Os dois tipos de mosca

Regra de design: o jogador precisa distinguir **só pela arte** em ~1 segundo. Hematófagas = cores escuras e opacas, olhar ameaçador, probóscide/ferrão visível. Inofensivas = cores vivas e simpáticas, formato arredondado e fofo. Mesmo tamanho e mesma vista (de cima, asas abertas) nas quatro.

**2a. Hematófagas (`fly_correct_1` e `fly_correct_2`):**
```
[STYLE MASTER]
Two small flying insects on a flat solid #00FF00 background, side by side, same size, seen from above with wings spread, each centered with equal margin, no text. Both look menacing and BLOOD-SUCKING, dark and dull colors:
(1) a horsefly (tabanid): stocky grey-brown body, huge green iridescent striped eyes, smoky wings;
(2) a stable fly (Stomoxys): slim dark grey body with striped thorax, red-brown eyes, and a clearly visible sharp black proboscis pointing forward.
Each fits a square; simple readable silhouette even at tiny size.
```
**2b. Inofensivas (`fly_wrong_1` e `fly_wrong_2`):**
```
[STYLE MASTER]
Two small flying insects on a flat solid #00FF00 background, side by side, same size, seen from above with wings spread, each centered with equal margin, no text. Both look friendly and HARMLESS, bright cheerful colors:
(1) a honeybee: round yellow and black body, translucent white wings;
(2) a butterfly: orange and blue wings with simple clean pattern.
Each fits a square; simple readable silhouette even at tiny size.
```
**2c. Se quiser mais variação (opcional):** peça `Same style: a ladybug and a dragonfly` (inofensivas) ou `a black fly (simulid), small and hunched, and a second horsefly in a different pose` (hematófagas), e eu adiciono mais arquivos ao código.

---

## Montagem no Aseprite

1. Cavalo: apague o `#00FF00`, reduza e cole no centro do cenário vazio (960x540) → exporte `mg6_bg.png`.
2. Moscas: apague o verde, corte justo, redimensione para **70x70** (nearest neighbor) → `fly_correct_1/2.png`, `fly_wrong_1/2.png`.
3. Teste em tamanho real: as moscas aparecem a 70x70 no canvas 960x540, então precisam ser legíveis assim, em especial a diferença entre os dois grupos.
