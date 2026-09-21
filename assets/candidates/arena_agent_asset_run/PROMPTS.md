# Starlight Acre — Arena Agent Asset Run: Generation Prompts

Complete, verbatim prompts used for every slot in this run. The **shared identity block**
is prepended to every candidate prompt; per-candidate prompts = shared block + slot base
prompt + that candidate's variant sentence. Reuse them to regenerate or iterate.

Status note: candidates marked `[generated]` have source.png on disk; `[pending]` slots/candidates
were not yet generated at the time of this file's last rebuild (per-turn image-generation cap).

---

## Shared identity block (prepended to every prompt)

```
Starlight Acre visual identity: polished orbital mythic farming-station game; the player restores a decaying space station by cultivating impossible mythic plants. Mood: atmospheric, luminous, calm but purposeful, slightly uncanny, mysterious, lived-in, restrained wonder; machinery that has survived too long; hopeful but never cheerful children's art. NOT generic cozy farming, NOT chibi, NOT glossy mobile art, NOT military sci-fi, NOT cyberpunk city, NOT isometric or top-down, NOT photorealistic. PIXEL ART LAW: deliberate GBA/SNES-era pixel art; hard pixel edges; deliberate pixel clusters; limited shading; strong silhouettes; restrained highlights; dark subtle outlines around gameplay objects; consistent pixel density; nearest-neighbor-compatible structure; absolutely no anti-aliasing, no blur, no soft painted edges, no photographic detail, no depth of field, no AI-smear pseudo-pixels, no checkerboard patterns, no text or lettering. PALETTE ANCHORS: deep space navy #0A0E1A, dusk blue #1E2D4A, hydroponic teal #2E8B8B, moss green #4F7942, mythic warm gold #D4AF37, maintenance copper #B87333, station gray #708090, bone highlight #F5F5DC (use as anchors, not all at once). Hardware: used, repaired, modular, industrial. Mythic biology: luminous, precious, uncanny. 
```

## A01_GARDENER_DRONE — Priority A — target 32x32 — 3 candidates

**Expected layout:** single sprite, 32x32, bottom-center/hover-center anchor

**Base prompt (all candidates):**

```
A small automated orbital gardener maintenance drone for a 2D side-view pixel game, single sprite centered on a solid flat pure magenta #FF00FF background (flat single color, no checkerboard, no gradient). Strict side view. Compact utility machine: worn station-metal hull in station gray and dusk blue, hydroponic teal and moss green accents, a small clipped tool arm with tender-claw or nozzle for tending plants, a subtle teal sensor slit instead of eyes, small thruster nozzles beneath (hover center anchor). Clearly non-human, helper not enemy, botanical tending function visible in silhouette, readable at very small scale, dark subtle outline. No weapons, no combat language, no giant antennae, no cartoon mascot face, no huge expressive eyes, no humanoid body.
```
### A01_C001 [generated]

```
Variant 1: boxy utility chassis with rounded corners, tool arm folded low, single underside thruster glow.
```
### A01_C002 [generated]

```
Variant 2: compact pod drone with a visible small planter-clay pot cradle clip and misting nozzle, twin mini thrusters.
```
### A01_C003 [generated]

```
Variant 3: low wide hexagonal maintenance drone with side-mounted clipper arm and tiny top beacon in moss green.
```

## T02_RESEARCH_TERMINAL — Priority A — target 64x80 — 3 candidates

**Expected layout:** single sprite, 64x80 canvas, body ~56x72, bottom-center anchor at floor line

**Base prompt (all candidates):**

```
Engineering Bay research terminal for a 2D side-view pixel game, single prop sprite centered on a solid flat pure magenta #FF00FF background (flat, no checkerboard). Strict side view. Tall dark station shell in deep space navy and dusk blue with worn station-gray trim and copper bolts; research function readable without text: a tilted scan-hood, a floating holographic data lattice in cyan-teal glow with small violet orbiting glyphs (abstract shapes only, NO readable text, no letters), thin violet accent strips, subtle cable runs into the base plate. Slightly strange and functional rather than decorative; same civilization design language as worn industrial repair and replenish terminals but visibly distinct: more instruments, an antenna-less sensor ring, a specimen-slot on the side. Bottom edge sits on the canvas floor line. Dark subtle outline, readable silhouette.
```
### T02_C001 [generated]

```
Variant 1: monolith terminal with curved top hood and one large tilted holographic display plane, violet rim light.
```
### T02_C002 [generated]

```
Variant 2: twin-column terminal with central data core column, small orbiting hologram rings in cyan and violet.
```
### T02_C003 [generated]

```
Variant 3: squat wide console with tall thin sensor mast, holo-lattice hovering above, specimen slot glowing faintly violet.
```

## W01_SECTOR_DOOR — Priority A — target 64x112 — 3 candidates

**Expected layout:** single prop, 64x112 canvas, ~4x7 tiles of 16px, bottom-center anchor, no surrounding wall

**Base prompt (all candidates):**

```
Reusable orbital station sector door for a 2D side-view pixel game, single prop on a solid flat pure magenta #FF00FF background (flat, no checkerboard), no surrounding wall scenery. Strict side view, frontal frame of a sliding bulkhead. Approximately four 16px tiles wide and seven 16px tiles tall: strong mechanical rectangular silhouette in worn dusk-blue and station-gray hull plating with copper reinforcing ribs, central vertical seam showing it slides open into two panels, teal status light strip near the top, small warning chevrons in hydroponic teal, heavy floor threshold plate, subtle scuffs and old repair seams. Obviously traversable and openable; old station hardware; usable in both a greenhouse sector and an engineering bay. No readable text. Dark subtle outline.
```
### W01_C001 [generated]

```
Variant 1: two-panel vertical-lift door with exposed copper piston columns on both sides and teal status band on top.
```
### W01_C002 [generated]

```
Variant 2: horizontal split double-panel bulkhead with central teal seal light and riveted corner brackets.
```
### W01_C003 [generated]

```
Variant 3: rounded-top pressure door with teal circular lock indicator and thick segmented frame.
```

## B02_ENGINEERING_BACKGROUND — Priority A — target 640x360 — 3 candidates

**Expected layout:** single full-frame background, 640x360, 16:9, opaque

**Base prompt (all candidates):**

```
Wide 16:9 far background environment art in deliberate GBA/SNES pixel-art style for a 2D side-view game: the far interior of an orbital engineering bay of a decaying mythic farming station. Distant industrial architecture: colossal machinery silhouettes, conduit bundles running along walls, catwalks and maintenance scaffolding far away, a restrained reactor core glow in teal-cyan deep in the composition, copper repair patches on navy and dusk-blue structural ribs, exposed aged plating, subtle mythic strangeness such as one impossible glowing filament vine far in the back. Base colors deep space navy #0A0E1A and dusk blue #1E2D4A with teal/cyan energy accents and copper details. Quiet negative space in the middle band where foreground gameplay will happen; calm, atmospheric, slightly uncanny, lived-in. No characters, no UI, no doors, no foreground floors or platforms, not a level screenshot. Flat full-frame illustration, no border, no text.
```
### B02_C001 [pending]

```
Variant 1: symmetric hall composition with a huge reactor ring glowing teal at center distance.
```
### B02_C002 [pending]

```
Variant 2: asymmetric collapsed machinery slope on one side, hanging cables, faint cyan vapor columns.
```
### B02_C003 [pending]

```
Variant 3: deep vertical shaft view with stacked distant galleries and thin copper light lines.
```

## E02_ENGINEERING_TILESET — Priority A — target 256x256 — 3 candidates

**Expected layout:** tileset sheet 256x256, strict 16x16 grid, 16 columns x 16 rows, 256 tiles, no spacing

**Base prompt (all candidates):**

```
A modular 16x16 pixel tileset sheet for a 2D side-view orbital engineering bay, arranged as a strict clean grid of 16 columns by 16 rows of 16x16 pixel tiles on a 256x256 pixel sheet, tiles touching with no gaps and no labels. Every tile in crisp GBA/SNES pixel-art style, side-view orientation, identical pixel scale, one coherent light direction from upper left, coherent industrial material language: dark navy floor plates with station-gray beveled edges, outer and inner corner pieces, wall panels in dusk blue with copper rivets, structural beams, conduit runs, pipes with joints, vents, grilles, service panel doors, a few damaged/cracked variants, small maintenance light strips in teal, industrial trim strips, junction fittings, framed energy containment glass tiles glowing faint cyan, and a few small noncollision decorative details (bolts, stains, tiny status LEDs). Worn, repaired, modular station hardware. Flat uniform very dark navy sheet background behind tiles; no text, no labels, no grid lines drawn, no isometric perspective.
```
### E02_C001 [pending]

```
Variant 1: emphasize heavy plated industrial look, thick bevels, generous copper ribs.
```
### E02_C002 [pending]

```
Variant 2: emphasize conduit-and-cabling density with teal status LEDs on many panels.
```
### E02_C003 [pending]

```
Variant 3: emphasize aged repair patches, mismatched panel generations, subtle moss-green residue tiles.
```

## C02_TRICKSTER_VINE — Priority A — target 128x32 — 3 candidates

**Expected layout:** growth sheet 128x32, four consecutive 32x32 cells left-to-right: empty planter / seedling / growing / ready; identical planter in all frames

**Base prompt (all candidates):**

```
Four-stage crop growth sprite sheet for a 2D side-view pixel game: ONE row, four consecutive 32x32 cells on a 128x32 canvas, left to right, on a solid flat pure magenta #FF00FF background (flat, no checkerboard). The same small worn hydroponic planter box (station gray with teal rim, identical position, identical design) appears in all four cells at the bottom. Stage 1: empty planter. Stage 2: planted seedling, first unruly curl of vine sprouting. Stage 3: growing, tangled mischievous vine with directional curls trying to escape the planter. Stage 4 READY: fully grown trickster vine, luminous, unmistakably harvest-ready with bright glowing buds in mythic warm gold with a slight violet-green iridescence, vines coiling outward past the planter edges. The plant is inspired by mythic trickster traditions (Loki-like spirit) without depicting any person: subtly unruly, asymmetric directional curls, implied desire to escape, unstable, strange but not goofy, luminous accent, NO cartoon face on the plant. GBA/SNES pixel art, dark subtle outline, consistent planter alignment across cells.
```
### C02_C001 [pending]

```
Variant 1: vine with hook-shaped curls and small gold bell-like seed pods, ready state leaning visibly to one side.
```
### C02_C002 [pending]

```
Variant 2: vine with zigzag kinked stems, teal-luminous sap dots, ready state with one bold oversized gold bud.
```
### C02_C003 [pending]

```
Variant 3: vine with spiraling tendrils that exit the planter and re-enter the soil, ready state haloed by tiny gold motes.
```

## D01_DEXTER_VENDOR — Priority A — target 64x64 — 3 candidates

**Expected layout:** single character sprite, 64x64 canvas, bottom-center anchor, strict side view

**Base prompt (all candidates):**

```
A tiny elderly tricolor Phalene dog game sprite for a 2D side-view pixel game, single sprite centered on a solid flat pure magenta #FF00FF background (flat, no checkerboard). Dexter is a VERY SMALL compact Phalene (the drop-eared variant of the Papillon, NOT a Papillon with upright ears): long silky butterfly-spaniel coat, FLOPPY EARS HANGING DOWN beside his head, black/dark and white and warm tan tricolor markings, small elderly dog with slightly grayed muzzle, compact body, calm unimpressed demeanor, half-lidded small dark eyes, closed mouth, no grin, no giant cute eyes, not puppy-like, no excessive cuteness. Strict side view standing pose, bottom of paws on the canvas floor line, dark subtle outline. A tiny restrained cargo accessory is allowed: a small worn satchel strap across the flank or a tiny seed pouch. Visual thesis: a tiny ancient authority who happens to sell you things. No humanoid clothes beyond the strap, no fantasy merchant caricature.
```
### D01_C001 [generated]

```
Variant 1: standing proud, small worn leather seed satchel, faint warm gold clasp.
```
### D01_C002 [pending]

```
Variant 2: sitting regally beside a tiny cargo crate corner entering the frame, ears perfectly floppy.
```
### D01_C003 [pending]

```
Variant 3: standing with one slight head-tilt of judgment, thin teal collar tag instead of satchel.
```

## D02_DEXTER_VENDOR_KIOSK — Priority A — target 96x64 — 3 candidates

**Expected layout:** single prop, 96x64 canvas, bottom-center anchor, clear space left for Dexter beside/within the composition, NO dog in this asset

**Base prompt (all candidates):**

```
A compact improvised orbital trading kiosk prop for a 2D side-view pixel game, single prop centered on a solid flat pure magenta #FF00FF background (flat, no checkerboard). A small repaired old station hardware counter: mismatched hull panels in dusk blue and station gray with copper brackets, a low trade shelf holding small seed containers, sealed rare biological goods canisters with faint teal and warm gold glow, one or two small cargo cases, a few unusual salvaged station components stacked at one end, a small canopy of salvaged strut and cloth in muted gold. Subtle teal/gold lighting, worn and lived-in. Deliberately leave clear empty space at one side of the counter where a very small dog vendor will later stand. NO animals, NO characters, NO readable text. Dark subtle outline, bottom edge on the canvas floor line.
```
### D02_C001 [pending]

```
Variant 1: kiosk arranged as a low L-shaped counter with hanging seed pouches on the left and open floor at right.
```
### D02_C002 [pending]

```
Variant 2: kiosk built from a repurposed cargo pod with flip-open lid displaying goods, open space in front.
```
### D02_C003 [pending]

```
Variant 3: kiosk as a scaffold table with glowing canister rack and a small awning, open space on the left.
```

## P01_PLAYER_SHEET — Priority B — target 192x192 — 2 candidates

**Expected layout:** animation sheet 192x192, 6 columns x 4 rows of 32x48 frames; row1: idle x4 then 2 empty; row2: walk x6; row3: jump, fall, land then 3 empty; row4: interact x2 then 4 empty

**Base prompt (all candidates):**

```
Character animation sprite sheet for a 2D side-view pixel game: strict grid of 6 columns x 4 rows of 32x48 pixel frames on a 192x192 canvas, frames touching, on a solid flat pure magenta #FF00FF background (flat, no checkerboard). Character: orbital technician-cultivator, an adult maintenance gardener of a decaying space station. NOT a soldier, NOT a space marine, NOT a fantasy warrior. Design: slim practical jumpsuit in dusk blue with moss green panel accents, teal hydroponic gloves, bone-white trim, small tool harness, dark boots, short practical hair under a slim cap or headband, calm purposeful face kept tiny and simple, dark subtle outline. Keep proportions, clothing, palette, scale, ground contact, facing direction and silhouette IDENTICAL in every frame. Row 1: 4 idle frames (subtle breathing bob) then 2 completely empty cells. Row 2: 6-frame walk cycle. Row 3: jump pose, fall pose, landing pose, then 3 completely empty cells. Row 4: 2-frame interact reach (arming reaching forward at waist height) then 4 completely empty cells. Empty cells must be left as the flat background color only. GBA/SNES pixel art, feet aligned to the same baseline in every frame.
```
### P01_C001 [pending]

```
Variant 1: slightly bulkier harness and rolled sleeves, cap with tiny gold emblem.
```
### P01_C002 [pending]

```
Variant 2: slimmer frame, open collar, teal knit cap, more silhouette contrast.
```

## C01_WISDOM_FRUIT — Priority B — target 128x32 — 2 candidates

**Expected layout:** growth sheet 128x32, four consecutive 32x32 cells: empty planter / seedling / growing / ready; identical planter in all frames

**Base prompt (all candidates):**

```
Four-stage crop growth sprite sheet for a 2D side-view pixel game: ONE row, four consecutive 32x32 cells on a 128x32 canvas, left to right, on a solid flat pure magenta #FF00FF background (flat, no checkerboard). The same small worn hydroponic planter box (station gray with teal rim, identical position and design) in all four cells. Stage 1: empty planter. Stage 2: planted seedling. Stage 3: growing slender plant. Stage 4 READY: unmistakably harvest-ready with a subtly brain-like botanical fruit in warm mythic gold #D4AF37 with restrained teal luminescence between its gentle folds, precious, intelligent-looking, uncanny but NOT grotesque, Athena-inspired wisdom without depicting any goddess or person. GBA/SNES pixel art, dark subtle outline, consistent planter alignment.
```
### C01_C001 [pending]

```
Variant 1: fruit as a golden bulbous pod with soft folded lobes and a short teal-glowing stem collar.
```
### C01_C002 [pending]

```
Variant 2: fruit slightly elongated with delicate gold leaves like a laurel and faint teal veins.
```

## T01_REPAIR_REPLENISH_TERMINALS — Priority B — target 64x64 — 2 candidates

**Expected layout:** two-terminal sheet 64x64: LEFT cell 32x64 repair terminal, RIGHT cell 32x64 replenish terminal, bottom-center anchors

**Base prompt (all candidates):**

```
Two-terminal sprite sheet for a 2D side-view pixel game: a 64x64 canvas on a solid flat pure magenta #FF00FF background (flat, no checkerboard) containing exactly two props side by side, each 32 pixels wide and 64 tall, feet on the canvas bottom line. LEFT: Repair Terminal in maintenance copper #B87333 and warm orange accents, power and hardware theme: a worn upright station pedestal with a small hatched panel, a copper coil or breaker element, a small amber status lamp, thick cable into the base. RIGHT: Replenish Terminal in hydroponic teal #2E8B8B and cool blue accents, water/nutrient/fluid theme: same station design language and same silhouette family as the repair terminal but visibly distinct, with a small transparent fluid window, a dripping nutrient nozzle, a teal status lamp. Same civilization, used and repaired hardware, no readable text, dark subtle outlines, GBA/SNES pixel art.
```
### T01_C001 [pending]

```
Variant 1: rounded-top pedestal family with a single central lamp and side gauges.
```
### T01_C002 [pending]

```
Variant 2: boxy industrial pedestal family with angled console faces and base cable stubs.
```

## U01_HUD_ICONS — Priority B — target 80x16 — 2 candidates

**Expected layout:** icon strip 80x16, five 16x16 icons in a row: water / nutrients / power / wisdom fruit / interaction E

**Base prompt (all candidates):**

```
HUD resource icon strip for a 2D pixel game: ONE row of five 16x16 pixel icons on an 80x16 canvas, on a solid flat pure magenta #FF00FF background (flat, no checkerboard). Icon 1 WATER: a droplet, cool blue and teal. Icon 2 NUTRIENTS: a small flask or granule pouch with a moss green accent. Icon 3 POWER: a lightning bolt or plug, warm amber-gold. Icon 4 WISDOM FRUIT: a small warm-gold subtly folded fruit with a teal glint. Icon 5 INTERACTION PROMPT: the literal capital letter E in bone white inside a small dark rounded key cap. Strong tiny-scale readability, bold single-pixel outlines, high contrast, GBA/SNES pixel art, no other letters anywhere, no text besides the single E.
```
### U01_C001 [pending]

```
Variant 1: flat two-tone icons with one highlight pixel cluster each.
```
### U01_C002 [pending]

```
Variant 2: icons with subtle dark key-cap backing tiles behind each glyph.
```

## E01_GREENHOUSE_TILESET — Priority B — target 256x256 — 2 candidates

**Expected layout:** tileset sheet 256x256, strict 16x16 grid, 16 columns x 16 rows, 256 tiles, no spacing

**Base prompt (all candidates):**

```
A modular 16x16 pixel tileset sheet for a 2D side-view orbital greenhouse sector, arranged as a strict clean grid of 16 columns by 16 rows of 16x16 pixel tiles on a 256x256 pixel sheet, tiles touching with no gaps and no labels. GBA/SNES pixel art, side-view orientation, identical pixel scale, coherent light from upper left. Tile families: worn navy-gray floor plates with edges and corners, wall panels in dusk blue, structural beams, hydroponic planter rim tiles, crates, small ceiling light strips in warm bone-white, vents, pipes with joints, hydroponic machinery blocks with teal reservoir windows, glass framing tiles with faint green tint, moss green residue and worn variants, and a few small noncollision station props (bolts, tiny status LEDs, hazard notch strip). Used orbital hardware plus a hint of strange living greenhouse: one tile with a tiny luminous teal sprout. Flat uniform very dark navy sheet background; no text, no labels, no grid lines, no isometric.
```
### E01_C001 [pending]

```
Variant 1: emphasize bright clean hydroponic machinery and glass framing with strong teal glow.
```
### E01_C002 [pending]

```
Variant 2: emphasize aged patched plating with moss overgrowth creeping on several tiles.
```

## B01_GREENHOUSE_BACKGROUND — Priority B — target 640x360 — 2 candidates

**Expected layout:** single full-frame background, 640x360, 16:9, opaque

**Base prompt (all candidates):**

```
Wide 16:9 far background environment art in deliberate GBA/SNES pixel-art style for a 2D side-view game: the far interior of a deteriorating orbital greenhouse where something impossible and precious is being cultivated. Include: the station shell ribs in dusk blue, tall greenhouse glazing panels with worn seal seams, deep space beyond the glass with distant stars and a restrained nebular wash of teal and faint warm gold, distant hydroponic infrastructure racks and pipes, quiet teal biological light, warm-gold mythic highlights from a far canopy of impossible plants, evidence of age and repeated repair (patched panels, copper weld seams). Calm atmospheric middle band with negative space for foreground gameplay. No characters, no UI, no doors, no foreground floors or platforms. Flat full-frame illustration, no border, no text.
```
### B01_C001 [pending]

```
Variant 1: huge glazed dome curve with a distant impossible tree silhouette glowing gold.
```
### B01_C002 [pending]

```
Variant 2: long horizontal window band with a nebula outside and stacked hydroponic racks in silhouette.
```

## V01_CORE_VFX — Priority B — target 128x32 — 2 candidates

**Expected layout:** vfx strip 128x32, four consecutive 32x32 cells: harvest burst / repair spark / growth glow / interaction ping, each isolated in its cell

**Base prompt (all candidates):**

```
VFX sprite strip for a 2D pixel game: ONE row of four consecutive 32x32 cells on a 128x32 canvas, each effect isolated and centered in its own cell, on a solid flat pure magenta #FF00FF background (flat, no checkerboard). Cell 1 HARVEST BURST: a small radiating burst of warm gold shard particles. Cell 2 REPAIR SPARK: a compact copper-orange spark cluster with tiny bolt lines. Cell 3 GROWTH GLOW: a soft-ish but pixel-clustered teal-green upward glow motes rising like spores. Cell 4 INTERACTION PING: a bone-white capital E-free ping: a small hollow diamond or ring pulse with four tick marks. GBA/SNES pixel art, hard pixel clusters, no smooth gradients, no text, no letters.
```
### V01_C001 [pending]

```
Variant 1: denser particle clusters, stronger contrast.
```
### V01_C002 [pending]

```
Variant 2: lighter sparser effects, thinner strokes, more negative space.
```

## C03_LIGHTNING_VINE — Priority C — target 128x32 — 2 candidates

**Expected layout:** growth sheet 128x32, four consecutive 32x32 cells: empty planter / seedling / growing / ready; identical planter in all frames

**Base prompt (all candidates):**

```
Four-stage crop growth sprite sheet for a 2D side-view pixel game: ONE row, four consecutive 32x32 cells on a 128x32 canvas, left to right, on a solid flat pure magenta #FF00FF background (flat, no checkerboard). The same small worn hydroponic planter box (station gray with teal rim, identical position and design) in all four cells. A living vine that hosts contained electrical phenomena, Zeus-inspired storm plant without depicting any god or person: Stage 1 empty planter. Stage 2 seedling with a first tiny arcing filament. Stage 3 growing vine with kinked stems and small contained sparks in pale electric blue-white. Stage 4 READY unmistakable: charged vine with tightly coiled capacitor-like bulb fruits crackling with contained lightning, strongly suggesting harvested station energy use. Luminous, precise, slightly dangerous, not goofy. GBA/SNES pixel art, dark subtle outline, consistent planter alignment.
```
### C03_C001 [pending]

```
Variant 1: rounded storm-bulb fruits with forked micro-arcs between them.
```
### C03_C002 [pending]

```
Variant 2: tall thin stems ending in bud spires that spark at their tips.
```

## C04_SHADOW_ROOT — Priority C — target 128x32 — 2 candidates

**Expected layout:** growth sheet 128x32, four consecutive 32x32 cells: empty planter / seedling / growing / ready; identical planter in all frames

**Base prompt (all candidates):**

```
Four-stage crop growth sprite sheet for a 2D side-view pixel game: ONE row, four consecutive 32x32 cells on a 128x32 canvas, left to right, on a solid flat pure magenta #FF00FF background (flat, no checkerboard). The same small worn hydroponic planter box (station gray with teal rim, identical position and design) in all four cells. A root-dominant mythic plant, Hades-inspired underworld botany without depicting any god or person, mystical rather than evil: growth happens mostly BELOW and AT the soil line with deep unusual silhouettes, dark purple-black root bulges partially hidden by the planter soil, sparse pale bone-white and faint violet foliage above, the READY state showing one heavy knotted root crown lifted slightly above the soil with a cool violet underside glow. Partially hidden growth language, mysterious, calm, uncanny but not monstrous. GBA/SNES pixel art, dark subtle outline, consistent planter alignment.
```
### C04_C001 [pending]

```
Variant 1: root crown like a gnarled subdued tuber cluster with thin pale sprouts.
```
### C04_C002 [pending]

```
Variant 2: near-leafless form, deep descending root visible through a transparent soil cutaway hint, tiny violet flowers.
```

## C05_GOLDEN_BLOSSOM — Priority C — target 128x32 — 2 candidates

**Expected layout:** growth sheet 128x32, four consecutive 32x32 cells: empty planter / seedling / growing / ready; identical planter in all frames

**Base prompt (all candidates):**

```
Four-stage crop growth sprite sheet for a 2D side-view pixel game: ONE row, four consecutive 32x32 cells on a 128x32 canvas, left to right, on a solid flat pure magenta #FF00FF background (flat, no checkerboard). The same small worn hydroponic planter box (station gray with teal rim, identical position and design) in all four cells. A warm-gold flowering mythic plant, Freya-inspired without depicting any goddess or person: elegant but NOT ornate, clean generous silhouette implying efficiency, attraction and abundance. Stage 1 empty planter. Stage 2 seedling with rounded paired leaves. Stage 3 growing stem with closed gold buds. Stage 4 READY unmistakable: an open radiant warm-gold blossom like a stylized sunflower-poppy hybrid with a soft mythic glow, a few drifting gold petal motes. Precious, calm, welcoming. GBA/SNES pixel art, dark subtle outline, consistent planter alignment.
```
### C05_C001 [pending]

```
Variant 1: single large open bloom on a sturdy stem with broad moss-green leaves.
```
### C05_C002 [pending]

```
Variant 2: three modest blooms clustered, more restrained, slightly taller stem.
```
