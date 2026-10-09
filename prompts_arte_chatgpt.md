# Prompts de arte — Proteja Equinópolis (para o ChatGPT)

Prompts em **inglês** (o gerador de imagens obedece melhor) e instruções em português.
Todos seguem o mesmo **prompt mestre**, para a arte ficar consistente entre menu e minigames.

---

## 0. Como usar (leia antes)

1. **Use SEMPRE a mesma conversa** do ChatGPT para todas as imagens. Isso ajuda a manter o estilo.
2. **Cole o PROMPT MESTRE (seção 1) antes de cada prompt**, ou, na primeira mensagem, diga: "Memorize este estilo e aplique em todas as imagens que eu pedir". Mesmo assim, cole de novo de vez em quando.
3. **Comece pelas FICHAS DE PERSONAGEM (seção 2).** Depois, ao pedir cenas com o cavalo, o tratador ou o veterinário, **anexe a imagem da ficha** e escreva: *"Use the attached character sheet as the exact design reference."*
4. **Tamanho:** peça 1536x1024 (o ChatGPT não faz 16:9 exato). Os prompts já pedem "composição segura para recorte 16:9". No Aseprite, recorte para **1536x864** e redimensione para **960x540**.
5. **Sem texto na imagem.** O gerador erra o português. Todos os prompts pedem "no text"; o texto você coloca no Aseprite (ou o jogo escreve).
6. **Sprites (cavalo, tratador, moscas, ícones) em fundo sólido**, para você recortar fácil. Os prompts pedem fundo verde-chroma `#00FF00`. Depois, no Aseprite, apague a cor (varinha mágica, tolerância 0) para deixar transparente. Se o ChatGPT entregar já transparente, melhor ainda.
7. **Posição exata não é confiável.** A IA nem sempre coloca cada elemento onde você quer. Estratégia segura: gerar o **cenário** com a área central/direita vazia e gerar os **elementos separados** (sprites); depois você junta e posiciona no Aseprite, em 960x540, como já faz.
8. **Aparência de pixel art de verdade:** a IA faz "pixel art" com pixels irregulares. No Aseprite: reduza a imagem para 960x540 e use **Sprite → Color Mode → Indexed** (32 cores) para limpar a paleta. Se os pixels ficarem borrados, reduza a 480x270 com "nearest neighbor" e amplie 2x.
9. Gere 2 ou 3 variações de cada e escolha. Peça ajustes curtos: *"same image but the horse is smaller / the right side empty"*.

---

## 1. PROMPT MESTRE (cole antes de todo prompt)

```
STYLE MASTER — apply to every image:
Pixel art, 16-bit era look (SNES / GBA style), crisp hard pixel edges, NO anti-aliasing, NO blur, NO smooth gradients, NO photorealism, NO 3D render, NO painterly brush strokes. Limited palette of about 32 colors, flat shading with 3 tones per material (light, base, shadow), light coming from the top-left. A 1-pixel dark brown outline (#371F12) around characters and key objects. Warm, saturated, friendly colors of a sunny Brazilian countryside: grass greens (#568E48, #6AA052), sky blue (#5496DE to #B2DEF6), wood brown (#96693C), parchment (#ECDCB2), brick red (#A54A3E), soft blue (#486898). Cozy, educational, family-friendly mood. No gore: blood only as a few small clean red pixels. Chunky pixels, each pixel about 4x4 pixels in the generated image. ABSOLUTELY NO text, letters, numbers, logos or watermarks anywhere. Wide composition that survives a 16:9 crop (keep important content inside the central 16:9 area).
```

**Mundo do jogo (para citar quando precisar):** Equinópolis é uma cidade rural brasileira: casas brancas com telhado de telha vermelha, igreja com torre, caixa d'água, hospital veterinário com banner verde, pastos com cerca de madeira, lago, montanhas azuis ao fundo.

---

## 2. FICHAS DE PERSONAGEM (faça primeiro e guarde as imagens)

### 2.1 Golias da Natureza (o cavalo campeão)
```
[STYLE MASTER]
Character reference sheet on a flat solid #00FF00 background. A champion horse named Golias: chestnut-bay coat, a white blaze down the middle of the face, dark brown mane and tail, ONE white sock on the front left leg only, strong athletic build, kind dark eyes. Show it in 6 poses in one sheet, same design in all: (1) calm standing, side view facing right; (2) calm standing, 3/4 front view; (3) ANGRY face close-up (flared nostrils, narrowed eyes, ears pinned back); (4) startled/pained reaction (eyes wide, ears up, head thrown back); (5) head down grazing; (6) head close-up neutral. Clean, evenly spaced, no overlapping, no text.
```

### 2.2 Tratador (o funcionário da fazenda)
```
[STYLE MASTER]
Character reference sheet on a flat solid #00FF00 background. A friendly farmhand ("tratador"): straw hat, blue work shirt with rolled sleeves, brown trousers, boots, short mustache, holding a syringe. Show 5 poses, same design: (1) walking to the right carrying a syringe, needle hidden by the hand; (2) holding the syringe up, needle clearly visible, side view; (3) lunging forward to inject; (4) recoiling in fear, arms up; (5) injecting a horse (arm extended, needle in). No text.
```

### 2.3 Veterinário(a)
```
[STYLE MASTER]
Character reference sheet on a flat solid #00FF00 background. A friendly adult veterinarian: white lab coat with a small green cross badge, teal cap, blue medical gloves, stethoscope around the neck, clipboard. Show 4 poses, same design: (1) standing front view; (2) examining with stethoscope, side view; (3) holding a blood tube up to the light; (4) holding a clipboard and pointing. No text.
```

### 2.4 Os 5 cavalos da triagem (outras pelagens)
```
[STYLE MASTER]
Reference sheet on a flat solid #00FF00 background. Five DIFFERENT horses, side view facing right, standing calmly, all with the same pixel-art style and proportions as Golias, evenly spaced in one row: (1) black with a small white star, (2) pure white-grey (dapple grey), (3) palomino (golden coat, pale mane), (4) dark bay brown, (5) pinto (brown and white patches). No text.
```

---

## 3. MENU E INTERFACE

### 3.1 Fundo do menu principal
```
[STYLE MASTER]
Main-menu background scene for a horse-veterinary game, Equinópolis, a small rural Brazilian town. Sunny blue sky with white clouds, blue mountains in the distance, a small town with white houses and red tile roofs and a church tower and a water tower, a lake, green pastures with wooden fences, a dirt road coming from the bottom center toward the town. A veterinary hospital building with a green banner on the right side, with a horse and a vet visible in its open door. A large leafy tree framing the top-left corner and a hanging lantern on a wooden post at the top-right. A brown horse behind a wooden fence at the bottom-left, a second horse grazing far away. IMPORTANT: keep the top-center area and the central vertical strip EMPTY and calm (sky, road) because a title and three buttons will be placed there. No text, no signs with writing.
```

### 3.2 Título (placa de madeira SEM texto)
```
[STYLE MASTER]
A big wooden signboard for a game title, hanging on a flat solid #00FF00 background. Warm wood planks with visible grain, 4 metal nails/rivets in the corners, a slightly irregular border, subtle bevel. The sign is EMPTY (blank wood), wide format about 3:1, centered. No text.
```
(O texto "Proteja Equinópolis" você coloca no Aseprite. Se quiser tentar o texto na própria IA, adicione: `Write "Proteja Equinópolis" in thick white pixel letters with a dark outline`, mas confira a acentuação.)

### 3.3 Kit de interface (botões, painel, barras)
```
[STYLE MASTER]
A pixel-art UI kit sheet on a flat solid #00FF00 background, evenly spaced, no text on any element: (a) three wide rectangular buttons in green, blue and red, each in 3 states side by side (idle, hover brighter, pressed darker), dark brown outline and a light top highlight; (b) a parchment panel/window with a dark wood frame and an inner thin gold line, wide format; (c) a horizontal slider: dark brown empty track, green filled part, and a small cream square handle; (d) a small square pause button (two vertical bars) in 2 states; (e) a small round close "X" button in 2 states; (f) a check mark badge and a padlock icon.
```

### 3.4 Mapa de desafios (fundo)
```
[STYLE MASTER]
Overhead-oblique adventure-map background, parchment style, of the countryside around Equinópolis, with a winding dirt road that zigzags: a bottom row going left to right and a top row going right to left, connected on the right side, with 10 clear circular empty clearings along the road where level markers will be placed later (5 on the bottom row, 5 on the top row). Fields, trees, a lake, a red barn at the bottom-left start, a red flag at the top-left end. Parchment border frame. The clearings must be empty and evenly spaced. No text, no icons on the clearings.
```

### 3.5 Ícones dos 10 desafios
```
[STYLE MASTER]
A set of 10 round medallion icons on a flat solid #00FF00 background, in two rows of five, evenly spaced, same size and same frame (dark brown ring, cream inner circle), each with a simple pixel-art symbol and NO text: (1) a spiky virus particle, (2) a stethoscope, (3) a syringe with blood, (4) a petri dish with wells, (5) a clipboard with a green check, (6) a fly, (7) a needle inside a red prohibition sign, (8) a hoof, (9) a red alarm bell, (10) a gold trophy. Also draw a small gold padlock badge and a small green check badge separately below.
```

### 3.6 Telas de instruções e resultado (reaproveitar nos 7 minigames)
```
[STYLE MASTER]
A calm tutorial background for a game: a wooden veterinary desk seen from the front with soft lighting, a green desk lamp, a stethoscope and papers at the edges, and a large EMPTY area in the middle for a text window. Slightly darker and blurred-free (no blur) so the center is easy to read. No text.
```
```
[STYLE MASTER]
A large empty parchment panel with a dark wood frame and small corner ornaments, on a flat solid #00FF00 background, wide format 3:2, completely blank inside, for placing text. No text.
```
```
[STYLE MASTER]
Three small celebratory pixel-art badges on a flat solid #00FF00 background, evenly spaced, no text: a gold medal with a ribbon, a silver rosette, a green check seal. Plus a sad grey "try again" cross badge.
```

---

## 4. MINIGAMES

> Dica: em **todos**, anexe a ficha do Golias / tratador / veterinário quando o personagem aparecer.

### 4.1 Minigame 1 — Taxonomia e identificação do vírus
**Fundo (livro aberto):**
```
[STYLE MASTER]
Top-down view of an old open book lying on a dark wooden desk in a veterinary library, a quill and a magnifying glass at the edges, warm lamplight. The LEFT page is completely EMPTY and clean (a virus drawing will be placed there), the RIGHT page has six faint horizontal ruled rows on the right half (for taxonomy lines), no writing. The book fills most of the frame. No text.
```
**As 5 morfologias de vírus (sprites):**
```
[STYLE MASTER]
Five different microscopic virus particles on a flat solid #00FF00 background, in one row, evenly spaced, each about the same size, no text: (1) a round particle covered with club-shaped spikes, (2) a long filament-shaped particle, (3) a round particle with a thick envelope and small short spikes plus an inner dense core (this is the correct "retrovirus" one), (4) a bullet-shaped particle, (5) a hexagonal icosahedral particle with no envelope. Colorful but readable, each with a dark outline.
```

### 4.2 Minigame 2 — Exame clínico
```
[STYLE MASTER]
Interior of a wooden horse stall used for a clinical examination, side view. A horse (use the attached Golias reference) stands calmly in the CENTER of the image, with a veterinarian (attached reference) beside it holding a stethoscope. Hay on the floor, a bucket, a window with sunlight. IMPORTANT: leave the left 25% and right 30% of the image as plain wall/wood so menu columns can be placed over them. No text.
```
**Props opcionais:**
```
[STYLE MASTER]
Small clinical props on a flat solid #00FF00 background, evenly spaced, no text: a mercury-free digital thermometer, a pale-pink horse gum close-up icon, a pale-white (anemic) horse gum close-up icon, a swollen lymph node icon on a horse's neck, a notebook with a pencil, a blood-sample tube icon.
```

### 4.3 Minigame 3 — Coleta de exame (cavalo à esquerda)
```
[STYLE MASTER]
Outdoor horse handling area at a farm (treatment area), side view. Golias (attached reference) stands on the LEFT third of the image, tied to a wooden post, calm, being held by a farmhand. The RIGHT 45% of the image is a clean, simple wall/fence/ground area, EMPTY, reserved for menu options. Sunny afternoon. No text.
```
**Tubos de coleta (sprites):**
```
[STYLE MASTER]
Three blood collection tubes standing upright on a flat solid #00FF00 background, evenly spaced, no text: one with a RED cap (no anticoagulant), one with a PURPLE cap (EDTA), one with a GREEN cap (heparin). Glass tubes with a little red blood inside each, a plain white label with no writing.
```
**Ficha, etiqueta e caixa refrigerada:**
```
[STYLE MASTER]
Three items on a flat solid #00FF00 background, evenly spaced, no text: (1) a clipboard with a blank animal registration form (empty lines only), (2) a small blank adhesive tube label with a pencil, (3) a blue insulated cooler box, open, with ice cubes inside and a small tube rack.
```

### 4.4 Minigame 4 — Diagnóstico (IDGA e ELISA)
**Fundo — bancada de laboratório:**
```
[STYLE MASTER]
Veterinary laboratory bench seen from the front: shelves with glass flasks, a microscope, a pipette stand, an incubator, bright clean tiles, a window. The center is a clear empty bench surface. The RIGHT 45% of the image is plain tiled wall, EMPTY, for menu options. No text.
```
**Placa de IDGA (gel de ágar) — para fundo da fase 2:**
```
[STYLE MASTER]
Close-up top-down view of an agar gel Petri dish for an immunodiffusion test on a lab bench: translucent pale-yellow gel with ONE central well and SIX peripheral wells arranged in a hexagon. Thin white precipitation lines (arcs) are visible between the central well and wells 1 and 3, and NO line toward well 2. The dish fills the left 55% of the image; the right side is plain bench. No text.
```
**Placa de ELISA e leitor — fundo da fase 3:**
```
[STYLE MASTER]
Top-down view of a 96-well ELISA microplate on a lab bench, a column of wells showing a color gradient: two clear/pale wells, then wells in light yellow, strong yellow and deep orange, and a microplate reader (spectrophotometer) device at the left. The plate fills the left 55% of the image; the right side is plain bench. No text.
```
**Antígeno e anticorpos (sprites da fase 1):**
```
[STYLE MASTER]
On a flat solid #00FF00 background: (1) a large round virus particle (antigen) with three clearly visible Y-shaped binding sockets on its right side, centered at left; (2) six different Y-shaped antibodies in a 2x3 grid at the right, each with a different colored tip shape (triangle, circle, square, star, diamond, hexagon), three of which match the three sockets' shapes. No text.
```

### 4.5 Minigame 5 — Triagem de cavalos recém-chegados
```
[STYLE MASTER]
Farm entrance gate area in the morning: an open wooden gate, a horse trailer parked at the left, a dirt yard, a wooden fence, a small stable in the background. A clear open space at the LEFT-center for a horse sprite; the RIGHT 45% of the image is plain fence/ground, EMPTY, for menu panels. No text.
```
**Papéis e carimbos (sprites):**
```
[STYLE MASTER]
On a flat solid #00FF00 background, evenly spaced, no text: (1) a clipboard with a blank "exam result" paper (lines only) and a small red wax-seal stamp area, (2) a large rubber stamp, (3) a calendar page with a blank face and a red circle, (4) a stable door icon, (5) a syringe-and-tube "new sample" icon, (6) a sealed official envelope with a red seal (notification).
```
Os 5 cavalos: use a ficha **2.4**.

### 4.6 Minigame 6 — Moscas hematófagas
**Fundo (cavalo no centro):**
```
[STYLE MASTER]
A peaceful pasture at dusk-golden-hour with Golias (attached reference) standing in the exact CENTER of the image, side view, relaxed, tail swishing. Tall grass, a few wildflowers, a wooden fence in the distance, soft warm light. The area around the horse is open so flying sprites can be placed over it. No text.
```
**Moscas (sprites) — hematófagas vs. inofensivas:**
```
[STYLE MASTER]
On a flat solid #00FF00 background, 8 tiny flying insects in a 4x2 grid, evenly spaced, each about the same size, top-down or side view with wings spread, no text. Top row (BLOOD-SUCKING, menacing look, dark colors, banded eyes): (1) a horsefly (tabanid) with big green-striped eyes and a stocky grey body, (2) a stable fly (Stomoxys) with a visible sharp proboscis, (3) a second horsefly in a different pose, (4) a black fly (simulid), small and hunched. Bottom row (HARMLESS, friendly bright colors): (5) a honeybee, (6) a butterfly, (7) a ladybug, (8) a dragonfly.
```

### 4.7 Minigame 7 — Impedir a reutilização de agulha
**Fundo:**
```
[STYLE MASTER]
Farm treatment area, side view: wooden fence, a hay bale, a medicine cabinet on a post, bright morning light. Open ground in the center for a horse (left of center) and a farmhand (right of center) to be placed later. No characters in this image. No text.
```
**Agulha nova vs. usada (para a arte do tratador):**
```
[STYLE MASTER]
On a flat solid #00FF00 background, two large syringes side by side, close-up, no text: LEFT = a brand-new sterile syringe with a clear protective cap being removed, a clean sparkling needle and a sealed blister package nearby (bright, friendly colors). RIGHT = a USED syringe with a bent needle, a few red blood pixels on the tip and a dirty cap (duller, slightly sinister colors). The difference must be obvious at a glance.
```
**Cena do cavalo bravo / picado (opcional, para as poses):**
```
[STYLE MASTER]
Golias (attached reference) shown from the side in 3 separate poses on a flat solid #00FF00 background, evenly spaced: calm, ANGRY (nostrils flared, ears pinned, one front hoof stomping, cartoon "refusing" attitude), and startled/hurt (eyes wide, ears up). Same design in all 3. No text.
```

---

### 4.3b Minigame 3 — Cena da coleta na jugular + ícones das opções

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

## 5. Pedidos de ajuste rápidos (copie e cole)

- Mais legível: `Same image, but simplify the shapes, reduce the number of colors to 24, and make the outlines darker and cleaner.`
- Menos detalhe no centro: `Same image, but remove all details from the central 40% so it is a calm, empty area.`
- Estilo mais consistente: `Match the exact art style, palette and outline of the previous images in this conversation.`
- Recorte e tamanho: `Recompose this image so that the important content stays inside a centered 16:9 area.`
- Corrigir texto indesejado: `Same image with ALL text, letters and numbers removed (replace with blank wood/paper).`

---

## 6. Checklist final de cada imagem

- [ ] Sem texto/letras na arte (o texto vai no Aseprite)
- [ ] Recortada em 16:9 e redimensionada para **960x540**
- [ ] Paleta limpa (Indexed, ~32 cores)
- [ ] Sprites com fundo transparente (apagar o verde `#00FF00`)
- [ ] Posições conferidas com as áreas livres do jogo (coluna direita livre nos minigames 3, 4, 5; cavalo ao centro no 2 e no 6)
- [ ] Nome do arquivo igual ao que o código espera (me peça a lista se precisar)
