# Minigame 7 — Prompts de arte (ChatGPT): baia + 4 poses do cavalo

Use na MESMA conversa dos outros prompts e anexe a ficha do Golias (seção 2.1 do arquivo principal): *"Use the attached character sheet as the exact design reference."* Substitua `[STYLE MASTER]` pelo bloco abaixo.

## 1. PROMPT MESTRE (cole antes de todo prompt)

```
STYLE MASTER — apply to every image:
Pixel art, 16-bit era look (SNES / GBA style), crisp hard pixel edges, NO anti-aliasing, NO blur, NO smooth gradients, NO photorealism, NO 3D render, NO painterly brush strokes. Limited palette of about 32 colors, flat shading with 3 tones per material (light, base, shadow), light coming from the top-left. A 1-pixel dark brown outline (#371F12) around characters and key objects. Warm, saturated, friendly colors of a sunny Brazilian countryside: grass greens (#568E48, #6AA052), sky blue (#5496DE to #B2DEF6), wood brown (#96693C), parchment (#ECDCB2), brick red (#A54A3E), soft blue (#486898). Cozy, educational, family-friendly mood. No gore: blood only as a few small clean red pixels. Chunky pixels, each pixel about 4x4 pixels in the generated image. ABSOLUTELY NO text, letters, numbers, logos or watermarks anywhere. Wide composition that survives a 16:9 crop (keep important content inside the central 16:9 area).
```

---

## Arquivos que o jogo usa (`images/minigame7/`, canvas 960x540)

| Arquivo | O que é | Quando aparece |
|---|---|---|
| `mg7_bg.png` | fundo: **interior de uma baia** | sempre |
| `cavalo_calmo.png` | cavalo **normal** (é o botão que o jogador clica) | durante a tentativa |
| `cavalo_bravo.png` | cavalo **bravo** | o jogador reagiu à agulha (suja, ou cedo demais) |
| `cavalo_feliz.png` | cavalo **feliz** | agulha **nova** e o jogador deixou aplicar |
| `cavalo_triste.png` | cavalo **triste** | agulha **suja** foi aplicada (picada contaminada) |

**Posição:** os 4 cavalos são sprites de canvas inteiro com fundo **transparente**, no **mesmo lugar e mesmo tamanho**. O cavalo ocupa a caixa **x 180–480, y 150–470** (≈ 300x320). O tratador entra pela **direita** (x ≈ 510–770), então o cavalo fica virado para a direita.

---

## 1. Fundo — interior de uma baia (`mg7_bg.png`)
```
[STYLE MASTER]
Interior of a horse stall (baia) at a farm, pixel art, viewed from the front like a stage set: warm wooden plank walls on the back and sides, a dirt floor covered with a thick layer of golden straw bedding, a small barred window high on the back wall letting in soft warm sunlight, a hay net hanging in one corner, a metal water bucket and a wooden feed trough on the floor near the back wall, a wooden stall door frame on the right edge, a lantern on a beam. Clean, cozy, well-kept. The CENTER of the floor, roughly the middle 60% of the width and the lower middle of the image, is open, calm straw floor with no objects, because a horse (left-center) and a farmhand (right-center) will be placed there later. Keep the top-left corner, top-right corner and the bottom strip calm and low-detail (game text will be drawn there). No animals, no people, no text.
```

---

## 2. Os 4 cavalos (peça TODOS numa imagem, para ficarem consistentes)

Regra de design: **mesmo corpo, mesma escala, mesma linha dos cascos, virado para a DIREITA**. Só a expressão do rosto, as orelhas, a cauda e um detalhe pequeno mudam. Sem sangue, sem ferida.

```
Use the attached character sheet as the exact design reference (Golias, chestnut-bay coat, white blaze, ONE white sock on the front left leg).
[STYLE MASTER]
On a flat solid #00FF00 background, four versions of the SAME horse in a row, evenly spaced, no overlap, each fully visible with a little margin, all exactly the same body size, same standing pose, side view FACING RIGHT, hooves on the same ground line, no ground and no shadow. Only the face, ears, tail and a tiny effect differ:
(1) CALM: relaxed neutral, ears forward, eyes open and soft, mouth closed, tail resting.
(2) ANGRY: ears pinned flat back, eyes narrowed with angry eyebrows, nostrils flared, teeth slightly bared, head pulled a little up and back, one front hoof stomping, tail lashing up. Small red-orange anger spark marks near the head. Angry but cartoon-friendly.
(3) HAPPY: relaxed and content, eyes closed in a happy curve (smile), mouth gently smiling, ears forward and soft, tail swishing, a couple of small yellow sparkle pixels and one tiny heart near the head.
(4) SAD: head lowered, ears drooping to the sides, big sad eyes with a tiny blue tear drop, mouth turned down, shoulders slumped, tail hanging low, a small gray rain cloud above the head. No blood, no wound, no needle.
No text.
```

**Se o GPT mudar o tamanho/posição entre os 4:**
`Same four horses, but make them exactly the same size, same pose and with hooves on the exact same horizontal line. Change only the expression.`

**Prompt para refazer só uma pose** (anexe a imagem do cavalo calmo):
```
Use the attached horse as the exact reference: same design, size, pose and position. Redraw it as [ANGRY / HAPPY / SAD] with these changes only: [descrição da pose acima]. Flat solid #00FF00 background, no ground, no shadow, no text.
```

---

## Montagem no Aseprite
1. Para cada cavalo: apague o `#00FF00`, reduza para caber em **x 180–480, y 150–470** de um canvas **transparente** de 960x540, **no mesmo lugar nos 4** → `cavalo_calmo/bravo/feliz/triste.png`.
2. Fundo: reduza para 960x540 com *nearest neighbor* e depois **Sprite → Color Mode → Indexed** (~32 cores) → `mg7_bg.png`.
3. Confira os cantos do fundo: texto do jogo fica no **topo-esquerdo** (título), **topo-direito** (tentativa, pontos, picadas) e **faixa de baixo** (motivo). Deixe-os calmos ou ponha uma faixa escura atrás.

## Ajustes rápidos
- Estilo diferente do resto: `Match the exact art style, palette and outline of the previous images in this conversation.`
- Texto na imagem: `Same image with ALL text, letters and numbers removed.`
- Cavalo diferente da ficha: `You changed the design. Keep the horse identical to the attached reference and change only the expression.`

## Checklist
- [ ] 4 cavalos com o mesmo tamanho, a mesma posição e os cascos na mesma linha, virados para a direita
- [ ] Sem sangue, ferida ou agulha nos sprites
- [ ] Fundo com centro livre e cantos calmos
- [ ] Nomes de arquivo iguais aos da tabela
