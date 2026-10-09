# Minigame 3 — Prompts de arte (ChatGPT)

Use na MESMA conversa dos outros prompts. Anexe a ficha do Golias e do veterinário (seção 2 do arquivo principal) e escreva: *"Use the attached character sheet as the exact design reference."* Substitua `[STYLE MASTER]` pelo bloco abaixo.

## 1. PROMPT MESTRE (cole antes de todo prompt)

```
STYLE MASTER — apply to every image:
Pixel art, 16-bit era look (SNES / GBA style), crisp hard pixel edges, NO anti-aliasing, NO blur, NO smooth gradients, NO photorealism, NO 3D render, NO painterly brush strokes. Limited palette of about 32 colors, flat shading with 3 tones per material (light, base, shadow), light coming from the top-left. A 1-pixel dark brown outline (#371F12) around characters and key objects. Warm, saturated, friendly colors of a sunny Brazilian countryside: grass greens (#568E48, #6AA052), sky blue (#5496DE to #B2DEF6), wood brown (#96693C), parchment (#ECDCB2), brick red (#A54A3E), soft blue (#486898). Cozy, educational, family-friendly mood. No gore: blood only as a few small clean red pixels. Chunky pixels, each pixel about 4x4 pixels in the generated image. ABSOLUTELY NO text, letters, numbers, logos or watermarks anywhere. Wide composition that survives a 16:9 crop (keep important content inside the central 16:9 area).
```

---

## Minigame 3 — Cena da coleta na jugular + ícones das opções

**Contornar a restrição de "gore":** descreva como *rotina veterinária, ilustração de livro didático*, mostre o procedimento limpo (tubo a vácuo + porta-agulha), esconda o ponto da punção com as mãos enluvadas e use "dark red liquid in a sealed tube" em vez de "blood". Nunca peça ferida, sangramento ou close da agulha entrando.

**Cena (fundo do minigame 3, veterinário colhendo na jugular, tudo na ESQUERDA):**
```
[STYLE MASTER]
Educational veterinary textbook illustration, pixel art. Outdoor treatment area of a farm, side view. On the LEFT 45% of the image: the chestnut horse Golias (attached reference) stands calm and relaxed, head slightly raised, held by a farmhand with a lead rope. A veterinarian in a white lab coat, teal cap and blue gloves (attached reference) stands beside the horse's neck, calmly performing a routine, clean sample collection from the jugular groove of the neck: gloved hands pressed to the lower neck, a small vacuum collection tube holder attached, a sealed tube with a little dark red liquid inside. The needle and the puncture point are hidden by the veterinarian's hands. No wound, no bleeding, no blood on the horse or on the ground. Professional, calm, friendly mood. The RIGHT 55% of the image is a simple clean wooden fence and grass, EMPTY, reserved for menu options. No text.
```
Se o ChatGPT recusar: troque por `a veterinarian examining the neck of a calm horse and holding a sealed sample tube next to it` (sem o ato da punção) e, no Aseprite, ajuste a posição das mãos. Outra saída: gerar o cavalo + veterinário em pé e a mão com o tubo separados.

**Ícones das opções** (3 folhas, 3 ícones por folha, fundo `#00FF00`; depois você cola cada ícone dentro da moldura `opcao_*` no Aseprite):

*Etapa 1 — Tubo (tubo, EDTA, heparina):*
```
[STYLE MASTER]
Three blood collection tubes (sealed glass tubes with a little dark red liquid), standing upright, evenly spaced, large and clear, on a flat solid #00FF00 background, no text, no labels with writing:
(1) tube with a RED stopper (no anticoagulant, dry tube, the liquid has clotted at the bottom);
(2) tube with a PURPLE / LAVENDER stopper (EDTA);
(3) tube with a GREEN stopper (heparin).
Same tube shape, only the stopper color differs. Icon style, centered.
```
*Etapa 2 — Via/local de coleta (intramuscular na garupa, subcutânea no dorso, endovenosa na jugular):*
```
[STYLE MASTER]
Three simple educational diagram icons on a flat solid #00FF00 background, evenly spaced, no text. Each shows a small side-view horse silhouette (chestnut) with ONE body area highlighted by a yellow glowing circle and a small clean syringe icon pointing at it. No wounds, no blood.
(1) highlighted area: the RUMP (hindquarters), syringe angled deep into the muscle;
(2) highlighted area: the BACK (withers/dorsum), syringe angled shallow, a small pinched skin fold;
(3) highlighted area: the lower NECK along the jugular groove, a small collection tube next to it.
Equal framing and size in all three.
```
*Etapa 5 — Transporte (caixa de papelão, porta-luvas ao sol, caixa isotérmica):*
```
[STYLE MASTER]
Three simple icons on a flat solid #00FF00 background, evenly spaced, no text:
(1) a plain cardboard box with a sample tube rack sticking out, ambient temperature, dull brown;
(2) the open glove compartment of a car dashboard with a sample tube inside and bright sun rays and little heat waves hitting it;
(3) a blue insulated cooler box, open, with ice cubes inside and a tube rack with sealed tubes.
Same framing and size in all three.
```
**Dicas:** peça sempre 3 variações; se um ícone sair ruim, peça só ele: `Redo only icon (2), same style, same size, centered on #00FF00.` Os ícones são *dentro* da moldura de cada opção: os arquivos finais continuam `opcao_<etapa>_<n>.png` em 960x540, com moldura + ícone + texto desenhados por você.
