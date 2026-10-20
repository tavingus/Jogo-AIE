# Introdução — 3 prompts de arte (ChatGPT)

Use na MESMA conversa dos outros prompts (a do menu principal, se possível, para manter o estilo). Anexe também: a **imagem do fundo do menu** (como referência de estilo da cidade) e as fichas do **Golias** e do **veterinário(a)** (seção 2 do arquivo principal) quando indicado. Escreva sempre: *"Use the attached images as the exact style and character reference."* Substitua `[STYLE MASTER]` pelo bloco abaixo.

## 1. PROMPT MESTRE (cole antes de todo prompt)

```
STYLE MASTER — apply to every image:
Pixel art, 16-bit era look (SNES / GBA style), crisp hard pixel edges, NO anti-aliasing, NO blur, NO smooth gradients, NO photorealism, NO 3D render, NO painterly brush strokes. Limited palette of about 32 colors, flat shading with 3 tones per material (light, base, shadow), light coming from the top-left. A 1-pixel dark brown outline (#371F12) around characters and key objects. Warm, saturated, friendly colors of a sunny Brazilian countryside: grass greens (#568E48, #6AA052), sky blue (#5496DE to #B2DEF6), wood brown (#96693C), parchment (#ECDCB2), brick red (#A54A3E), soft blue (#486898). Cozy, educational, family-friendly mood. No gore: blood only as a few small clean red pixels. Chunky pixels, each pixel about 4x4 pixels in the generated image. ABSOLUTELY NO text, letters, numbers, logos or watermarks anywhere. Wide composition that survives a 16:9 crop (keep important content inside the central 16:9 area).
```

---

## Como as imagens são usadas

| Arquivo | Texto da cena (o jogo escreve na caixa de baixo) |
|---|---|
| `images/intro/intro_1.png` | "Equinópolis é uma cidade que respira cavalos. Aqui, eles trabalham, competem e fazem parte de cada família." |
| `images/intro/intro_2.png` | "Mas um inimigo invisível chegou: a Anemia Infecciosa Equina. Ela passa por insetos e agulhas contaminadas, e não tem cura nem vacina." |
| `images/intro/intro_3.png` | "Cabe a você, veterinário(a) da cidade, identificar, testar e conter a doença antes que ela se espalhe." |

**Regras para as 3 (importante):**
- Peça **1536x1024**, recorte em 16:9 e reduza para **960x540** (nearest neighbor), depois Indexed ~32 cores.
- **A faixa de baixo (≈ 25% da altura) precisa ser calma e sem detalhes importantes**: a caixa de texto do jogo fica ali (x 80–880, y 390–510 do canvas).
- **O canto superior direito** também fica calmo (botão PULAR).
- **Sem texto nas imagens.**
- **Mesmo lugar nas 3 cenas** (a cidade de Equinópolis), com a **luz contando a história**: dourada e feliz → sombria e ameaçadora → amanhecer de esperança.

**Paleta por cena**
1. Quente e saturada: dourado, verde, azul-céu (igual ao menu).
2. Fria e dessaturada: roxos, verdes doentios, cinzas; sensação de ameaça (mas família-friendly).
3. Aurora: laranja-rosa no horizonte, azul-claro, verdes frescos.

---

## Cena 1 — A cidade que respira cavalos (`intro_1.png`)
```
[STYLE MASTER]
Wide establishing shot of the rural Brazilian town of Equinópolis at golden hour, pixel art, same style and palette as the attached main-menu background. Whitewashed houses with red-tile roofs, a church with a bell tower, a water tower, a veterinary hospital with a green banner and a white cross, wooden-fenced pastures, a small lake and blue mountains in the distance, warm sunlight and soft clouds. The town is full of horses and everyday life: a girl petting a bay horse over a fence in the foreground, a rider on a chestnut horse trotting on a dirt road, a horse pulling a small cart, a family with a foal in a paddock, a few horses grazing. Joyful, lively, welcoming mood. IMPORTANT: keep the bottom 25% of the image calm and low in detail (plain grass and dirt road), and keep the top-right corner calm sky. No text.
```

## Cena 2 — O inimigo invisível (`intro_2.png`)
```
[STYLE MASTER]
The SAME town and pasture as the previous image (same buildings, fence and mountains), but now ominous, pixel art. The sky is stormy and dusky in desaturated purple, sickly green and grey. In the foreground a chestnut horse stands uneasy in the pasture with ears back, and a small swarm of large dark horseflies with green eyes buzzes around it. On a wooden fence post nearby rests a used syringe with a dull, bent needle with dark red-brown residue. Faint translucent purple virus particles with tiny spikes drift in the mist above the pasture like an invisible threat (subtle, not cartoonish-scary). Other horses in the background look restless. Tense, worrying mood, still family-friendly: NO blood on animals, no wounds, no gore, no dead animals. IMPORTANT: keep the bottom 25% of the image calm and low in detail (dark grass and dirt), and the top-right corner calm sky. No text.
```

## Cena 3 — A veterinária(o) entra em ação (`intro_3.png`)
```
Use the attached character sheets as the exact design reference for the veterinarian (white lab coat with green cross badge, teal cap, blue gloves, stethoscope, clipboard) and for the chestnut-bay horse Golias.
[STYLE MASTER]
Same town of Equinópolis at sunrise, pixel art, hopeful and determined mood. The veterinarian stands in the foreground on the left, seen from the side or three-quarter back view, looking toward the town with a clipboard in one hand and a sealed blood-sample tube with a red cap in the other. Golias stands calm beside them. Behind them the veterinary hospital with its green banner glows in the first light, and the town and pastures spread out under a pink-orange dawn sky with clearing clouds, fresh green grass and dew sparkles. The storm of the previous scene is breaking up in the distance. Small friendly details: a microscope on a stand and a cooler box by the hospital door. No blood, no wounds. IMPORTANT: keep the bottom 25% of the image calm and low in detail (plain grass and dirt path), and the top-right corner calm sky. No text.
```

---

## Cavalo torto ou esquisito na imagem (como corrigir)

O gerador erra a anatomia do cavalo quando ele está numa pose complicada (de frente, em escorço, com a cabeça virada) ou quando a cena tem coisas demais. Do mais simples ao mais seguro:

**1. Corrigir só o cavalo** (anexe a imagem gerada e a ficha do Golias):
```
Redraw ONLY the horse in this image. Keep everything else exactly the same (sky, mist, flies, syringe, fence, background, composition). The horse must have correct, natural horse anatomy: a clean SIDE VIEW standing pose, four straight legs with proper joints, a long arched neck, deep chest, strong hindquarters, correct proportions. Use the attached Golias character sheet as the exact design reference (chestnut-bay coat, white blaze, ONE white sock on the front left leg). Uneasy expression: ears pinned back. Do not change anything else.
```
No ChatGPT você também pode **selecionar só a região do cavalo** com a ferramenta de seleção da imagem e pedir a correção apenas ali.

**2. Simplificar a pose no prompt original:** troque a descrição do cavalo por `a chestnut horse standing in simple side profile, calm silhouette, ears back` e deixe-o **menor e mais ao fundo** (cavalos pequenos erram menos). Evite "head turned", "three-quarter view" e "rearing".

**3. Sem cavalo na cena, e você coloca o sprite (o mais seguro):**
```
Same image, but REMOVE the horse completely and leave the pasture empty (grass, fence and mist only). Keep everything else exactly the same.
```
Depois, no Aseprite, cole o cavalo do seu **sprite do Golias** (ou um dos 5 cavalos da triagem) na posição, na escala certa, com sombra no chão. Assim a anatomia fica garantida e o cavalo fica igual ao do resto do jogo.

**4. Gerar variações:** peça 3 ou 4 versões da mesma cena e escolha a melhor, ou troque só o cavalo de uma versão pela de outra.

---

## Dicas de consistência
- **Gere as 3 em sequência na mesma conversa** e, para a 2 e a 3, anexe a imagem da cena 1 e escreva: `Keep the exact same town layout, buildings and mountains as the attached image.`
- Se a cena 2 ficar "feia" demais: `Same image, less scary, more atmospheric, softer colors, keep it family-friendly.`
- Se a faixa de baixo ficar cheia: `Same image, but remove all details from the bottom 25% so it is plain ground.`
- Se aparecer texto: `Same image with ALL text, letters and numbers removed.`
- Se o veterinário(a) sair diferente da ficha: `The veterinarian must match the attached character sheet exactly.`

## Checklist
- [ ] 3 imagens em 960x540, mesma cidade, luz: dourada → sombria → aurora
- [ ] Faixa de baixo calma e canto superior direito calmo
- [ ] Sem texto, sem sangue/ferida
- [ ] Salvas como `intro_1.png`, `intro_2.png`, `intro_3.png` em `game/images/intro/`
