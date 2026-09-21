# STARLIGHT ACRE VISUAL CANON

**Status:** authoritative art-direction reference for all future asset generation.
**Supersedes for generation purposes:** the broader `assets/docs/style_guide.md`
(which remains valid as the project's original style summary).

## Method & Authority (read first)

This canon was produced by an art-direction consolidation pass over the complete
**136-candidate** library (original 44 + ALT 44 + additional 24 + additional-ALT 24).
Every candidate's `game_ready.png` — the actual in-game representation — was measured
deterministically: palette-anchor usage, outline-ring darkness and dark-edge band,
edge (detail) density, cluster run length, lighting bias, glow ratio, silhouette
coverage, quantized color count. Combined evidence: those measurements + the recorded
generation prompts + technical flags + run-verification history.

**Honesty note:** the analysis environment has no image-viewing capability. No
human-style aesthetic viewing was performed. Every number below is a reproducible
pixel measurement (`tools_canon_analyze.py` → `MASTER_ASSET_INDEX.json`).
Selections in `VISUAL_CANON_SELECTIONS.json` are art-direction **drafts grounded in
measurement**; the pair-review tools remain the place where humans ratify them.
No candidate file was modified.

---

# Visual Thesis

Starlight Acre is a worn orbital farm station rendered in deliberate GBA/SNES pixel
art: machinery that has survived too long — dusk-blue panels over station-gray
structure, patched with maintenance copper — quietly tending luminous, impossible
plants that glow teal and gold under soft overhead light. The player reads the world
through **strong dark-keylined silhouettes on calm, dark, low-detail backgrounds**;
wonder is delivered by restrained emissive accents (a reactor's teal heart, a crop's
gold bloom), never by global brightness. Everything looks manufactured by one
practical civilization and grown in one impossible garden.

Measured identity of the current library (medians): detail-edge density **0.36**,
cluster run **1.04** (chunky single-pixel clusters), outline-ring darkness **0.71**,
glow ratio **5%**, dark pixels **30%**, saturation **0.52**, mild top-light bias
**+0.02**, palette-anchor adherence **78%**.

---

# Pixel Density

The detail-frequency ladder (measured median edge density per family) is the game's
depth cue. **Keep it.**

| layer | edge density | cluster run | rule |
|---|---|---|---|
| environment backgrounds | 0.112 | 1.12 | calmest; large flat value fields |
| environment tilesets | 0.243 | 1.06 | calm; 16px tile rhythm |
| crops / mythic biology | 0.309 | 1.05 | calm-gentle; biology breathes |
| VFX / glows | 0.337 | 1.04 | sparse clusters, dither steps |
| terminals | 0.333 | 1.03 | moderate |
| HUD icons | 0.392 | 1.05 | dense but chunky |
| large machinery | 0.398 | 1.04 | moderate-dense |
| archive tech | 0.471 | 1.05 | dense (precision hardware) |
| drones / agents | 0.456 | 1.01 | densest gameplay sprites |
| environment props | 0.614 | 1.02 | densest (small busy props) |

Laws:
- **Foreground density ≈ 2.5–4× background density.** Never let a background reach
  gameplay-level detail (measured ratio today: 0.362/0.112 ≈ 3.2).
- **Cluster run stays ≈ 1.0–1.1** at native game scale: deliberate pixel clusters,
  not texture noise. A mean horizontal run below ~0.95 means noise; above ~1.3 means
  mushy flat fills.
- **16×16 (HUD icons):** one glyph per cell, 1px keyline, ≤ ~10 quantized colors per
  glyph, one highlight cluster. No dithering at this size.
- **32×32 (drones, crop cells, prop cells, VFX cells):** one readable subject; major
  forms in 2–4px blocks; interior detail limited to one accent zone (readout, lamp,
  seam); single-pixel highlights only.
- **64px-class (terminals, rigs, archive stacks, cargo sheets, reactor):** panel
  architecture readable at 50%; 2–3 material zones max; wear as 2–4 deliberate
  scuffs/patches, not uniform grime.
- **Backgrounds (640×360-class):** value composition in 5+ large masses; horizon
  machinery as silhouette bands; **zero** pixel-level storytelling in the far field.
- **Anti "shrunk high-res" rule:** if a downscaled candidate shows edge density
  > 0.55 at 32px class or > 0.45 at 64px class with cluster run < 0.95, it is
  faux-pixel shrink — reject as style reference (this exact profile is what got
  `P01_C001/C002` and `P01_ALT_C001` rejected: frame residue pushed glow to 76–82%
  and saturation to 0.90+).

---

# Outline Law

- **Every gameplay object carries a dark keyline** at its silhouette boundary.
  Measured boundary-ring darkness: global median **0.71**; doors/fixtures **0.89**,
  greenhouse machinery **0.87**, docking **0.86**, tilesets **0.89**, drones **0.70**,
  crops **0.59** (lightest — biology), props **0.80**.
- **Keyline weight: 1px at game scale.** Measured dark-edge bands run 1.8–5px because
  dark hulls extend the band; the *drawn* outline is the darkest 1px step inside it.
  Never draw 2px cartoon outlines on 32px sprites.
- **Internal edges do NOT get full outlines:** panel seams are 1px value steps
  (dusk-blue vs station-gray), not black lines. Outlines are for separating object
  from background, not for interior drawing.
- **Glowing objects may break the outline:** VFX/glow family ring darkness is only
  **0.33** — light emits through the boundary. Emissive cores (reactor hearts,
  crop blooms) may punch past the keyline as bright pixels.
- **Botanical outline behavior:** crops use the lightest, softest keylines (0.59):
  dark enough to read, thin and incomplete — leaves may lose the outline where glow
  passes through. Machinery keeps the strict ring; biology relaxes it.

---

# Lighting Law

- **Dominant light: soft, from above.** Global median top-vs-bottom bias **+0.02**;
  crops **+0.13** (strongest — grow lights overhead), machinery **+0.09**, drones
  **+0.07**. Highlights live on upper faces and top edges; shadows pool at bases
  (bottom-center anchors ground machinery).
- **Shadow:** value drops, not black. Dark-pixel budget: ~30% of a gameplay sprite;
  backgrounds run 65% dark. Never fill interiors with large pure-black fields except
  deep-space background voids.
- **Emissive behavior:** emissive pixels are bright AND saturated (measured glow
  definition) — reactor 19%, docking guides 13%, Dexter's stall lantern 18%, drones
  **2%** (near-zero: drones do not glow; only tiny readouts). Emissive light does
  not cast visible light onto neighbors at this art scale; it is a local accent.
- **Rim lighting:** permitted only as a 1px bone-white or teal upper-edge tick on
  machinery (seen on reactor/docking references). No full rim halos.
- **Flat-lit exceptions:** Dexter/kiosk (bias ≈ 0.0 — evenly lantern-lit vendor
  scenes) and VFX (self-luminous). Bottom-lit uplight exists only as a deliberate
  rare accent (e.g. `A04_C002` scoop-tram at −0.09); do not default to it.

---

# Palette Law

Anchors (unchanged): `#0A0E1A` navy · `#1E2D4A` dusk blue · `#2E8B8B` teal ·
`#4F7942` moss green · `#D4AF37` warm gold · `#B87333` copper · `#708090` station
gray · `#F5F5DC` bone.

How the library actually uses them (median share of visible pixels per family):

| anchor | where it belongs | measured center of gravity |
|---|---|---|
| deep space navy | background voids, deep shadow | backgrounds 39%, tilesets 34%, HUD chips 37% |
| dusk blue | machine panel mid-tones | every hardware family 14–34% |
| station gray | structural frames, hulls, floors | drones 24%, doors 21%, docking 21% |
| maintenance copper | **repairs and plumbing only**: pipes, clamps, brackets, seams, spools | 3–7% in every hardware family; ~0 on player/crops |
| hydroponic teal | station tech glow (terminals 10%) **and** plant biology (crops 8%) | terminals, rigs, drones' readouts |
| moss green | living plant tissue | crops 7%, greenhouse machinery 5% |
| mythic warm gold | **reserved for mythic importance** — harvest produce, core VFX, precious accents | crops 1%, VFX 9%; effectively 0 elsewhere |
| bone highlight | tiny bright ticks: lamps, indicators, Dexter's coat, UI rims | Dexter 8%, HUD 4%, ≤1% elsewhere |

Laws:
- **Copper is never a body color.** Hulls are dusk-blue/gray; copper is what holds
  them together and repairs them.
- **Teal is dual-coded and context resolves it:** on machinery = controlled station
  technology; on plants = living bioluminescence. A teal pipe and a teal leaf may
  share the hue — the outline law (strict ring vs soft ring) separates them.
- **Gold is precious.** If it appears, the object matters to the myth. No gold on
  generic hardware.
- **Bone-white budget: ≤ ~8% of any sprite**, as single-pixel ticks and small lamps.
- **Backgrounds desaturate *in effect* by value, not hue:** they live in navy/dusk
  (77% combined) at 65% darkness with 0.9% glow — chroma stays anchored but detail
  frequency and value keep them receding. Foreground pops by density + keyline +
  glow, not by out-saturating the room.
- **Anchor adherence targets:** HUD ≥ 90% (measured 91%), hardware 74–86%,
  VFX 72% (glow colors may leave anchor space), backgrounds 90%.

---

# Material Language

- **Station steel/structure (station gray + dusk blue):** flat 2-tone panels, 1px
  seam steps, occasional rivet dots. Reads as thick, old, industrial.
- **Painted panels (dusk blue):** the station's "brand" color — large flat panels
  with corner bolts; chips and scratches reveal gray underneath (1–2px nicks only).
- **Copper repairs:** pipes with elbow joints, strap bands, clamp petals, patch
  plates with 2 visible bolts. Copper is always slightly warmer in the light.
- **Glass:** dusk-blue tinted, 1px lighter top edge, no reflections; contents (water,
  crystals, vials) glow through with teal/cyan.
- **Energy:** teal-cyan plasma, dither-stepped clusters, hard edges — never smooth
  gradients. Contained by hardware everywhere except VFX cells.
- **Hydroponic equipment:** glass tubes + copper manifolds + teal water + one moss-
  green living trace; water surfaces are calm horizontal 2px lines.
- **Archive technology:** dusk-blue monolith with copper trim; knowledge as glowing
  cyan-teal crystals/vials with restrained violet secondary; glow 1.7% — precious,
  not flashy.
- **Docking hardware:** the heaviest construction language — thick collar rings,
  tension arms, worn seal lips, teal guide lights (12.7% glow: the most illuminated
  fixture family, still calm).
- **Mythic organic material:** luminous moss/gold/teal tissue with soft incomplete
  outlines; internal glow brighter at growth tips; never veiny horror texture.

---

# Machinery Grammar

All station machinery is built from the same civilizational kit:

- **Panel shapes:** rectangles with chamfered (45°) corners; octagonal fixtures for
  premium interfaces (docking). No bare right-angle boxes without a chamfer or bolt.
- **Corners:** bolt heads as 1px darker dots with 1px bone highlight tick.
- **Fasteners:** visible bolts on every removable panel (2–4 per panel).
- **Brackets:** copper L-straps and diagonal braces at load-bearing joints.
- **Vents:** 3–5 short horizontal slits, dusk-blue shadow fill.
- **Pipes:** copper, with visible elbows and flange rings; never perfectly straight
  runs — one jog or sag per pipe shows age.
- **Conduits:** gray/dusk surface channels with 1px highlight along the top.
- **Maintenance patches:** 2–4 per large machine; slightly hue-shifted panel
  rectangles with bolt pairs — the "repair history" signature.
- **Screens:** dark navy fill, NO readable text; state shown by 1–2px teal/amber
  indicator bars or dot clusters.
- **Glow indicators:** teal (nominal), amber (attention), bone (inspection lamps);
  single pixels or 2px dots, ringed in dark.
- **Bases/feet/mountings:** every floor-standing machine ends in a visible base —
  splayed feet, cradle saddles or bolted base plates — grounding the bottom-center
  anchor. Nothing floats except drones and VFX.

**Reference chain:** reactor `A02_ALT_C002` (hex-cell core) → hydroponics `B04_C001`
(twin-tank rig) → archive `B05_C002` (data-drum) → docking `B03_C001` (octagonal
berth ring). Same civilization, four functions.

---

# Drone Family Grammar

Gardener `A01_C003` · Engineer `A03_ALT_C001` (keel-busbar) · Harvester `A04_C001`
(basket-drone) · Maintenance `A05_C001` (brush puck).

Measured family profile: 32×32, edge density 0.456 (densest sprite family), glow
2.3% (near-zero), ring 0.70, top-light +0.07, anchors 83%, hull = station gray 24%
+ dusk blue 20% + navy 22%.

- **Shared proportions:** compact hover silhouette filling ~60–80% of the 32×32 cell;
  body mass in the upper half, hardware slung beneath.
- **Shared materials:** gray + dusk hull, copper accents only on functional hardware
  (busbars, nozzles, spools).
- **Shared propulsion:** small caged thrusters / ducted fans / annular rings —
  always visibly mechanical, emitting nothing (no flame glow).
- **Shared sensor vocabulary:** one small light — amber readout (engineer),
  bone lamp (maintenance), none/green accent (harvester). No faces, no eyes.
- **Role differentiation is carried by the under-slung tool, not the body:**
  cable spool/probe = engineer; produce basket/pincer = harvester; brushes/sealant
  = maintenance; sprayer/tender arm = gardener. A new drone = new tool + same body
  language.

---

# Terminal Family Grammar

Repair/Replenish `T01_ALT_C001` (64×64, two 32×64 pedestals) · Research
`T02_ALT_C003`. Measured: teal 10% of pixels (the glow family signature), ring
0.744, edge 0.333.

- Related, not interchangeable: **same pedestal silhouette family, same screen
  treatment (navy fill, no text), same keyline**; differentiated by crown hardware —
  repair = clamp arms + warm amber accents; replenish = water bracket + teal;
  research = crystal mount + taller mast.
- The active-glow overlays (`T03_C001`, warm-left / cool-right) are the only
  permitted screen-state language; glows never draw machinery.

---

# Mythic Biology Grammar

Wisdom Fruit `C01_ALT_C001` · Trickster Vine `C02_ALT_C002` · Lightning Vine
`C03_C001` · Shadow Root `C04_C001` · Golden Blossom `C05_ALT_C001`.

Measured family: lightest outlines (0.59), strongest overhead light (+0.13), calm
density (0.309), gold+teal emissives, planter trays present.

- **Shared universe:** every crop grows from the **same planter construction** —
  a consistent dusk-gray tray band with copper rim clips at the same height band in
  frame 1 of every 4-stage strip. (Planter inconsistency is a flagged defect — see
  repair queue.)
- **Lifecycle strips:** 4 horizontal 32×32 states, occupancy monotonically
  increasing (Empty→Planted→Growing→Ready); the Ready state and only it carries the
  emissive identity (gold fruit, teal spark-leaves…).
- **Distinct mythic identities:** Wisdom Fruit = gold orb + halo ticks; Trickster
  Vine = curling teal-green spiral; Lightning Vine = zigzag gold-teal arcs; Shadow
  Root = dark navy-violet taproot with bone flecks; Golden Blossom = chalice bloom.
- **Contrast law:** biology glows (soft outlines, internal light); machinery that
  tends it does not.

---

# Environment Grammar

- **Foreground interactables** (crops, terminals, props): keylined, dense, glow-
  capable — the readable layer.
- **Tiles** (`E01_C002` greenhouse — repair-queued; `E02_C001` engineering): 16px
  grid, heaviest keylines in the game (ring 0.887) so architecture reads as
  structure; 47% dark values.
- **Props** (`E03_C001` cargo sheet): densest family (0.614) — small objects carry
  the most detail per pixel; must sit ON tiles with shared base shadow.
- **Background machinery** (`B01_C001`, `B02_C002`): silhouette bands only —
  edge density 0.112, 65% dark, navy+dusk 77%; no readable panels, no glow beyond
  1% distant window dots.
- **Distant background:** value fields; the farthest layer is 2–3 flat masses.
- **Law:** detail decreases monotonically with depth. Any background element that
  competes with gameplay density is a defect.

---

# UI Grammar

`U01_ALT_C001` (core HUD) · `U02_C002` (extension icons). Measured: anchor
adherence 91% (strictest), ring 0.609, glow 8%, 16×16 cells.

- **Line weight:** 1px dark keyline per glyph; interior strokes 1px.
- **Internal density:** glyph + at most one interior accent cluster; no dithering.
- **Symbol simplicity:** each icon = ONE object silhouette (canister, leaf, crystal,
  flask, gear-chip, seed, droplet…), readable at 100%.
- **Highlight behavior:** one 1px bone-white tick per glyph, upper-left bias.
- **Palette constraints:** icons live on the anchor grid (91%); glyph body uses its
  semantic anchor (teal data, green biomass, gold produce); chip backgrounds navy.
- **No letters, words, or numbers anywhere** — the single exception in the whole
  project is the literal "E" interaction prompt in `U01` icon 5.

---

# VFX Grammar

Core `V01_ALT_C002` · terminal glow `T03_C001` · hazard `V02_ALT_C001`.

Measured: no outlines (ring 0.334), glow 29%, saturation 0.66, cluster run 1.04.

- **Maximum complexity:** 3 concentric zones per effect (core cluster, mid dither
  step, sparse outlier motes). Nothing denser.
- **Cell occupancy:** every required cell contains clear effect pixels (measured
  occupancy 12–100% across reference cells; an empty expected cell is a defect).
- **Glow shape:** dither-stepped clusters, hard pixel edges — never airbrush
  gradients; brightness peaks where the effect touches machinery.
- **Particle density:** sparse — motes are 1–2px, countable (≤ ~12 per 32×32 cell).
- **Color-role conventions:** teal/cyan = station tech working; warm gold-red =
  solar/energy hazard; violet = mythic anomaly; copper-orange = malfunction sparks;
  bone-white = failing/dying light. Never reuse a hazard's color for its opposite
  meaning.
- **Terminal glow halves never mix:** warm strictly left, cool strictly right
  (verified 100% separation on references).

---

# Dexter Lock

Dexter is a **very small, elderly tricolor Phalène** (Papillon with dropped ears):
long coat, **floppy ears DOWN** — never upright Papillon ears — and an unimpressed,
tired dignity rather than mascot cuteness.

- **Authority asset:** `D01_ALT_C001` (primary reference). Secondary `D01_C003`.
  `D01_C002` is rejected as a style reference (recorded duplicate-subject defect:
  two dogs in one sprite).
- Any future Dexter imagery must match this reference's proportions, coat
  tricoloring, ear carriage and expression before any other consideration.
- Vendor kiosk `D02_ALT_C002` shares his lantern-lit material language.
- **Scale caveat (logged in the continuity report):** Dexter's reference canvas is
  64×64 while the player frame is 32×48 — at integration, display-scale Dexter down
  so the dog reads clearly smaller than the player.

---

# Forbidden Drift

Concrete failure profiles — any of these disqualifies a candidate as a style
reference:

1. **Glossy gradients / bloom:** smooth value ramps (measured glow > ~20% on non-
   VFX machinery, or any blur), halo bloom around sprites.
2. **Faux-pixel shrink:** high-res painting downscaled — profile: edge density
   > 0.55 at 32px class, cluster run < 0.95, saturation > 0.85 (the rejected
   framed player sheets measured sat 0.90+, glow 76–82%).
3. **Generic cyberpunk:** neon signage, magenta/cyan city glow, holograms, rain
   streaks.
4. **Thick modern vector outlines:** 2px+ uniform outlines, rounded corner strokes.
5. **Inconsistent pixel scales:** mixed pixel densities inside one sprite or between
   sprite and its tile floor.
6. **Perspective drift:** isometric, top-down, or ¾ RPG views anywhere (strict 2D
   side view; UI strips are the only flat-on exception).
7. **Photoreal detail:** painted textures, DOF, photographic noise, AI-smear pixels.
8. **Overdesigned machinery:** greebles without function, more than 3 material
   zones, asymmetry without purpose.
9. **Cute mascot proportions:** chibi heads, big expressive eyes on drones/terminals.
10. **Oversaturated backgrounds:** background edge density approaching gameplay
    (> 0.2), bright background fields (glow > 2%), background anchor drift.
11. **UI-looking machinery:** readable text, labels, logos, gauge numerals on props
    (state is shown by indicator dots/bars only).
12. **Presentation-board framing:** caption panels, borders, staged floors, drop
    shadows behind isolated assets — the exact defects that got the flagged
    candidates queued for repair.

---

## Reference quick-index

Primary references per slot live in `VISUAL_CANON_SELECTIONS.json` and are visualized
in `reference_atlas.html` (with the GAME SCALE board). The future-generation contract
(`FUTURE_ASSET_GENERATION_CONTRACT.md`) defines which references must be inspected
before generating any new asset.
