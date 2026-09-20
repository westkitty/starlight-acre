#!/usr/bin/env python3
"""Starlight Acre ALTERNATE (challenger) run — challenger specs & prompts.

One alternate per original candidate (A01_C001 -> A01_ALT_C001 ...).
Each entry defines challenger_axes (the 2-4 design axes that change vs the incumbent)
and a complete generation prompt = SHARED identity + slot contract + challenger design.
The slot contract preserves every technical/semantic requirement of the original slot
(canvas, view, anchor, background rules, subject identity, palette relationships);
only the design directions inside the challenger paragraph differ.
"""
import os, sys

ORIG_ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "arena_agent_asset_run"))
if ORIG_ROOT not in sys.path:
    sys.path.insert(0, ORIG_ROOT)

from run_spec import SHARED, SLOTS  # style lock: identical Starlight Acre identity block

# Slot contracts: required identity + technical rules (adapted from run_spec bases),
# hardened with the anti-failure directives learned from the original run.
SLOT_CONTRACT = {
    "A01_GARDENER_DRONE": (
        "A small automated orbital gardener maintenance drone for a 2D side-view pixel game: "
        "exactly ONE drone, single sprite centered on a solid flat pure magenta #FF00FF background "
        "(one flat single color edge to edge, no checkerboard, no gradient, no border, no frame, "
        "no caption panel). Square 1:1 composition. Strict side view. Worn station-metal hull in "
        "station gray and dusk blue with hydroponic teal and moss green accents; a botanical tending "
        "function clearly readable in the silhouette at very small scale; hover center anchor; clearly "
        "a non-human helper, not an enemy. Dark subtle outline, clean hard edges against the background "
        "(no glow bleeding into the magenta). No weapons, no combat language, no giant antennae, no "
        "cartoon mascot face, no huge expressive eyes, no humanoid body, no second drone or duplicate, "
        "no floor, no stage, no drop shadow on the background."
    ),
    "T02_RESEARCH_TERMINAL": (
        "Engineering Bay research terminal for a 2D side-view pixel game: exactly ONE terminal prop "
        "centered on a solid flat pure magenta #FF00FF background (one flat color edge to edge, no "
        "border, no frame, no captions). Slightly tall portrait composition (about 4:5). Strict side "
        "view. Dark station shell in deep space navy and dusk blue with worn station-gray trim and "
        "copper bolts; research function readable without any text: abstract holographic data shapes "
        "in cyan-teal glow with small violet accents (abstract shapes only, absolutely no readable "
        "text or letters); a scan-hood element and a specimen containment element somewhere in the "
        "design; cable runs into the base plate; bottom edge sits on the canvas floor line. Dark "
        "subtle outline, readable silhouette. No readable text, no second terminal, no floor plate, "
        "no scenery, no drop shadow on the background."
    ),
    "W01_SECTOR_DOOR": (
        "Reusable orbital station sector door for a 2D side-view pixel game: exactly ONE door prop on "
        "a solid flat pure magenta #FF00FF background (one flat color edge to edge, no border, no "
        "frame), no surrounding wall scenery. Strict side view, frontal frame of a mechanical bulkhead. "
        "Tall portrait composition about four tiles wide and seven tiles tall (roughly 4:7). Strong "
        "mechanical rectangular silhouette in worn dusk-blue and station-gray hull plating with copper "
        "reinforcing elements; teal status lighting; heavy floor threshold plate; subtle scuffs and old "
        "repair seams; obviously traversable and openable; old station hardware usable in both a "
        "greenhouse sector and an engineering bay. Dark subtle outline. No readable text, no second "
        "door, no floor, no drop shadow on the background."
    ),
    "B02_ENGINEERING_BACKGROUND": (
        "Wide 16:9 far background environment art in deliberate GBA/SNES pixel-art style for a 2D "
        "side-view game: the far interior of an orbital engineering bay of a decaying mythic farming "
        "station. Opaque flat full-frame illustration, no border, no letterboxing, no vignette frame. "
        "Distant industrial architecture; base colors deep space navy #0A0E1A and dusk blue #1E2D4A "
        "with teal/cyan energy accents and copper details; subtle mythic strangeness such as one "
        "impossible glowing filament vine far in the back. Quiet negative space in the middle band "
        "where foreground gameplay will happen; calm, atmospheric, slightly uncanny, lived-in. No "
        "characters, no UI, no doors, no foreground floors or platforms, no readable text, not a "
        "level screenshot, no isometric or top-down view."
    ),
    "E02_ENGINEERING_TILESET": (
        "A modular 16x16 pixel tileset sheet for a 2D side-view orbital engineering bay, arranged as "
        "a strict clean grid of 16 columns by 16 rows of 16x16 pixel tiles on a square 256x256-"
        "proportioned sheet: tiles touching with no gaps, and the sheet extends fully to all four "
        "canvas edges with NO outer margin, NO border, NO frame, NO caption panel, no labels, no "
        "drawn grid lines. Crisp GBA/SNES pixel-art, side-view orientation, identical pixel scale, "
        "one coherent light direction from upper left; coherent industrial material language (dark "
        "navy floor plates, dusk-blue wall panels, structural beams, conduit runs, pipes with "
        "joints, vents, grilles, service panels, framed energy-containment glass tiles glowing faint "
        "cyan, small noncollision decorative details such as bolts, stains, tiny status LEDs). Worn, "
        "repaired, modular station hardware. Flat uniform very dark navy sheet background behind "
        "tiles; no text, no letters, no isometric perspective."
    ),
    "C02_TRICKSTER_VINE": (
        "Four-stage crop growth sprite sheet for a 2D side-view pixel game: ONE row of four "
        "consecutive 32x32 cells on a wide 4:1 strip (128x32 proportion), left to right: stage 1 "
        "empty planter, stage 2 seedling, stage 3 growing, stage 4 READY harvest. The same small "
        "worn hydroponic planter box (station gray with teal rim, IDENTICAL position and design) "
        "appears at the bottom of all four cells. The pure flat magenta #FF00FF background is one "
        "single flat color across the whole strip - between cells, around the plants, edge to edge - "
        "with absolutely no grid lines, no separating borders, no frame, no caption panel. The plant "
        "is a mythic trickster vine (Loki-like spirit, no person depicted): subtly unruly, "
        "asymmetric, implying a desire to escape; stage 4 is unmistakably harvest-ready with glowing "
        "buds in mythic warm gold with a slight violet-green iridescence. NO cartoon face on the "
        "plant. GBA/SNES pixel art, dark subtle outline, consistent planter alignment."
    ),
    "D02_DEXTER_VENDOR_KIOSK": (
        "A compact improvised orbital trading kiosk prop for a 2D side-view pixel game: exactly ONE "
        "kiosk prop (no characters, no animals) centered on a solid flat pure magenta #FF00FF "
        "background (one flat color edge to edge, no checkerboard, no border, no frame). Slightly "
        "wide landscape composition (about 3:2). Repaired old station hardware: mismatched hull "
        "panels in dusk blue and station gray with copper brackets, a trade surface holding small "
        "seed containers, sealed rare biological goods canisters with faint teal and warm gold glow, "
        "one or two small cargo cases, a few unusual salvaged station components, a small canopy of "
        "salvaged strut and cloth in muted gold. Subtle teal/gold lighting, worn and lived-in. "
        "Deliberately leave clear empty space at one side of the counter where a very small dog "
        "vendor will later stand. NO animals, NO characters, NO readable text, no floor, no stage, "
        "no drop shadow on the background. Dark subtle outline, bottom edge on the canvas floor line."
    ),
    "P01_PLAYER_SHEET": (
        "Character animation sprite sheet for a 2D side-view pixel game: a strict square grid of 6 "
        "columns x 4 rows of 32x48 pixel frames on a square 192x192-proportioned canvas, frames "
        "touching, on a solid flat pure magenta #FF00FF background. THE MAGENTA BACKGROUND MUST "
        "REACH ALL FOUR EDGES OF THE CANVAS: absolutely NO border, NO frame, NO dark margin, NO "
        "caption panel, NO vignette, no drawn grid lines. Empty cells contain ONLY flat magenta - "
        "no props, no marks, no glow. Character: orbital technician-cultivator, an adult maintenance "
        "gardener of a decaying space station; NOT a soldier, NOT a space marine, NOT a fantasy "
        "warrior; slim practical jumpsuit in dusk blue with moss green panel accents, teal "
        "hydroponic gloves, bone-white trim, small tool harness, dark boots, short practical hair "
        "under headwear, calm purposeful face kept tiny and simple, dark subtle outline. Keep "
        "proportions, clothing, palette, scale, ground contact, facing direction and silhouette "
        "IDENTICAL in every frame; feet aligned to the same baseline in every frame. Row 1: 4 idle "
        "frames (subtle breathing bob) then 2 completely empty cells. Row 2: 6-frame walk cycle. "
        "Row 3: jump pose, fall pose, landing pose, then 3 completely empty cells. Row 4: 2-frame "
        "interact reach (arm reaching forward at waist height) then 4 completely empty cells. "
        "GBA/SNES pixel art."
    ),
    "C01_WISDOM_FRUIT": (
        "Four-stage crop growth sprite sheet for a 2D side-view pixel game: ONE row of four "
        "consecutive 32x32 cells on a wide 4:1 strip (128x32 proportion), left to right: stage 1 "
        "empty planter, stage 2 seedling, stage 3 growing slender plant, stage 4 READY harvest. The "
        "same small worn hydroponic planter box (station gray with teal rim, IDENTICAL position and "
        "design) appears at the bottom of all four cells. The pure flat magenta #FF00FF background "
        "is one single flat color across the whole strip - between cells, around the plants, edge "
        "to edge - with absolutely no grid lines, no separating borders, no frame, no caption "
        "panel. Stage 4 is unmistakably harvest-ready with a subtly brain-like botanical fruit in "
        "warm mythic gold #D4AF37 with restrained teal luminescence, precious, intelligent-looking, "
        "uncanny but NOT grotesque, Athena-inspired wisdom without depicting any goddess or person. "
        "GBA/SNES pixel art, dark subtle outline, consistent planter alignment."
    ),
    "T01_REPAIR_REPLENISH_TERMINALS": (
        "Two-terminal sprite sheet for a 2D side-view pixel game: a square 64x64-proportioned "
        "canvas on a solid flat pure magenta #FF00FF background (one flat color edge to edge, no "
        "border, no frame, no captions) containing exactly TWO props side by side, each 32 pixels "
        "wide and 64 tall, feet on the canvas bottom line, no other scenery. LEFT: Repair Terminal "
        "in maintenance copper #B87333 and warm orange accents, power and hardware theme: a worn "
        "upright station pedestal with a small hatched panel, a copper coil or breaker element, a "
        "small amber status lamp, thick cable into the base. RIGHT: Replenish Terminal in "
        "hydroponic teal #2E8B8B and cool blue accents, water/nutrient/fluid theme: same station "
        "design language and same silhouette family as the repair terminal but visibly distinct, "
        "with a small transparent fluid window, a dripping nutrient nozzle, a teal status lamp. "
        "Same civilization, used and repaired hardware, no readable text, no labels, dark subtle "
        "outlines, GBA/SNES pixel art."
    ),
    "U01_HUD_ICONS": (
        "HUD resource icon strip for a 2D pixel game: ONE row of five 16x16 pixel icons on a very "
        "wide thin strip (80x16 proportion), on a solid flat pure magenta #FF00FF background that "
        "is ONE single flat color edge to edge - between icons, around glyphs, across the whole "
        "strip - with no border, no frame, no caption panel, no drawn dividing lines. Icon 1 WATER: "
        "a droplet, cool blue and teal. Icon 2 NUTRIENTS: a small flask or granule pouch with a "
        "moss green accent. Icon 3 POWER: a lightning bolt or plug, warm amber-gold. Icon 4 WISDOM "
        "FRUIT: a small warm-gold subtly folded fruit with a teal glint. Icon 5 INTERACTION PROMPT: "
        "the literal capital letter E in bone white inside a small dark rounded key cap. Each icon "
        "is complete and centered inside its own 16x16 cell; strong tiny-scale readability, bold "
        "single-pixel outlines, high contrast, GBA/SNES pixel art; no other letters anywhere, no "
        "text besides the single E."
    ),
    "E01_GREENHOUSE_TILESET": (
        "A modular 16x16 pixel tileset sheet for a 2D side-view orbital greenhouse sector, arranged "
        "as a strict clean grid of 16 columns by 16 rows of 16x16 pixel tiles on a square "
        "256x256-proportioned sheet: tiles touching with no gaps, and the sheet extends fully to "
        "all four canvas edges with NO outer margin, NO border, NO frame, NO caption panel, no "
        "labels, no drawn grid lines. GBA/SNES pixel art, side-view orientation, identical pixel "
        "scale, coherent light from upper left. Tile families: worn navy-gray floor plates with "
        "edges and corners, wall panels, structural beams, hydroponic planter rim tiles, crates, "
        "small ceiling light strips in warm bone-white, vents, pipes with joints, hydroponic "
        "machinery blocks, glass framing tiles, and a few small noncollision station props; one "
        "tile with a tiny luminous teal sprout. Worn orbital hardware plus a hint of strange "
        "living greenhouse. Flat uniform very dark navy sheet background behind tiles; no text, "
        "no letters, no isometric perspective."
    ),
    "B01_GREENHOUSE_BACKGROUND": (
        "Wide 16:9 far background environment art in deliberate GBA/SNES pixel-art style for a 2D "
        "side-view game: the far interior of a deteriorating orbital greenhouse where something "
        "impossible and precious is being cultivated. Opaque flat full-frame illustration, no "
        "border, no letterboxing, no vignette frame. Include: station shell ribs in dusk blue, "
        "tall greenhouse glazing panels with worn seal seams, deep space beyond the glass with "
        "distant stars and a restrained nebular wash of teal and faint warm gold, distant "
        "hydroponic infrastructure racks and pipes, quiet teal biological light, warm-gold mythic "
        "highlights from a far canopy of impossible plants, evidence of age and repeated repair "
        "(patched panels, copper weld seams). Calm atmospheric middle band with negative space "
        "for foreground gameplay. No characters, no UI, no doors, no foreground floors or "
        "platforms, no readable text, not a level screenshot, no isometric or top-down view."
    ),
    "V01_CORE_VFX": (
        "VFX sprite strip for a 2D pixel game: ONE row of four consecutive 32x32 cells on a wide "
        "4:1 strip (128x32 proportion), each effect isolated and centered in its own cell, on a "
        "solid flat pure magenta #FF00FF background that is ONE single flat color edge to edge - "
        "between cells, around effects, across the whole strip - with no border, no frame, no "
        "caption panel, no drawn dividing lines. EVERY one of the four cells must actually "
        "contain its effect, fully inside the cell, nothing crossing cell boundaries. Cell 1 "
        "HARVEST BURST: a small radiating burst of warm gold shard particles. Cell 2 REPAIR "
        "SPARK: a compact copper-orange spark cluster with tiny bolt lines. Cell 3 GROWTH GLOW: "
        "pixel-clustered teal-green upward glow motes rising like spores. Cell 4 INTERACTION "
        "PING: a bone-white ping with NO letterforms: a small hollow diamond or ring pulse with "
        "four tick marks. GBA/SNES pixel art, hard pixel clusters, no smooth gradients, no text, "
        "no letters anywhere."
    ),
    "C03_LIGHTNING_VINE": (
        "Four-stage crop growth sprite sheet for a 2D side-view pixel game: ONE row of four "
        "consecutive 32x32 cells on a wide 4:1 strip (128x32 proportion), left to right: stage 1 "
        "empty planter, stage 2 seedling, stage 3 growing, stage 4 READY harvest. The same small "
        "worn hydroponic planter box (station gray with teal rim, IDENTICAL position and design) "
        "appears at the bottom of all four cells. The pure flat magenta #FF00FF background is one "
        "single flat color across the whole strip - between cells, around the plants, edge to "
        "edge - with absolutely no grid lines, no separating borders, no frame, no caption "
        "panel. The plant is a living vine hosting contained electrical phenomena (Zeus-inspired "
        "storm plant, no god or person depicted): stage 2 seedling with a first tiny arcing "
        "filament, stage 3 vine with small contained sparks in pale electric blue-white, stage 4 "
        "READY unmistakable with charged capacitor-like bulb fruits crackling with contained "
        "lightning; luminous, precise, slightly dangerous, not goofy. GBA/SNES pixel art, dark "
        "subtle outline, consistent planter alignment."
    ),
    "D01_DEXTER_VENDOR": (
        "A tiny elderly tricolor Phalene dog game sprite for a 2D side-view pixel game: exactly ONE "
        "dog, single sprite centered on a solid flat pure magenta #FF00FF background (one flat color "
        "edge to edge, no checkerboard, no border). Square 1:1 composition. Dexter is a VERY SMALL "
        "compact Phalene (the drop-eared variant of the Papillon, NOT a Papillon with upright ears): "
        "long silky butterfly-spaniel coat, FLOPPY EARS HANGING DOWN beside his head, black/dark and "
        "white and warm tan tricolor markings, small elderly dog with slightly grayed muzzle, compact "
        "body, calm unimpressed demeanor, half-lidded small dark eyes, closed mouth, no grin, no giant "
        "cute eyes, not puppy-like, no excessive cuteness. Strict side view, bottom of paws on the "
        "canvas floor line, dark subtle outline. A tiny restrained cargo accessory is allowed. Visual "
        "thesis: a tiny ancient authority who happens to sell you things. No humanoid clothes, no "
        "fantasy merchant caricature, no second dog, no crate, no floor, no drop shadow on the background."
    ),
}

# Challenger designs, keyed by alternate candidate id. Each is the materially different
# design paragraph appended after the slot contract.
CHALLENGER = {
    "A01_ALT_C001": (
        "CHALLENGER DESIGN (materially different from the incumbent boxy rounded chassis with one "
        "folded tool arm): a tall narrow lantern-spine drone: slim vertical spine chassis with three "
        "stacked hexagonal sensor rings, station gray with dusk-blue plating and one moss-green accent "
        "band; THREE delicate articulated care arms fanned out and raised high - a micro-pruner, a "
        "single-drop dispenser, and a soft dusting brush - giving an elegant multi-tending silhouette; "
        "locomotion by a single annular ducted thruster ring worn at the waist like a hoop with a faint "
        "teal glow inside the ring; no top mast, no underside nozzle. High negative space between the "
        "raised arms; reads as a precise botanical butler, not a toy."
    ),
    "A01_ALT_C002": (
        "CHALLENGER DESIGN (materially different from the incumbent round pod with clay-pot cradle and "
        "misting nozzle): a low flat wedge-shaped skimmer drone in dusk blue with bone-white "
        "pin-striping and a hydroponic-teal belly sensor strip; a transparent-front seed hopper mounted "
        "forward like a cargo jaw, and a needle-fine watering spout extending ahead of it; locomotion "
        "by two rear tilt-fans in copper cages angled downward; small folded magnet-clamp feet tucked "
        "under the belly for docking. Reads as a patient seed-sowing machine."
    ),
    "A01_ALT_C003": (
        "CHALLENGER DESIGN (materially different from the incumbent low wide hexagonal chassis with "
        "side clipper arm and top beacon): a spherical gimbal-core drone: a softly glowing "
        "hydroponic-teal core sphere suspended inside a rotating station-gray protective cage ring with "
        "four flat spokes; two small pincer tenders mounted on the cage equator, one holding a tiny "
        "moss cutting; motion implied by the cage's offset rotation; no thruster nozzles visible, hover "
        "implied by the calm core glow. Reads as a gentle self-stabilizing seed curator."
    ),
    "T02_ALT_C001": (
        "CHALLENGER DESIGN (materially different from the incumbent monolith with one large tilted "
        "display plane): a cantilevered research console: a heavy single base pillar anchored to the "
        "floor plate, with an off-balance instrument head overhanging far to one side like a "
        "draughtsman's lamp; the scan-hood reinterpreted as a slim angled visor on the head's leading "
        "edge; research data shown as a rising helix thread of small cyan glyph-shapes spiraling up "
        "from an open specimen dish set into the pillar's shoulder; a side rack of three tiny analog "
        "instruments; one thin violet accent strip under the head; cables looping from head to base in "
        "a long catenary."
    ),
    "T02_ALT_C002": (
        "CHALLENGER DESIGN (materially different from the incumbent twin-column terminal with orbiting "
        "holo rings): a low sweeping arc console that wraps around a central open cradle; the "
        "scan-hood forms an overhead arch spanning the arc's ends; a prism specimen floats in the "
        "cradle while a soft cone of cyan-teal data light projects DOWN onto it from the arch; small "
        "violet tick-marks along the arc's inner edge; a specimen slot at the cradle's front; wide "
        "stable stance, calm and instrumental."
    ),
    "T02_ALT_C003": (
        "CHALLENGER DESIGN (materially different from the incumbent squat console with tall thin "
        "sensor mast): a vertical elevator-rack terminal: three offset instrument shelves stacked on a "
        "slim central column like a goods lift, each shelf carrying its own small glowing readout dial "
        "of a different size; the scan-hood integrated flush into the top shelf; small cyan "
        "glyph-shapes spiraling slowly around the column between shelves; a row of specimen vial slots "
        "on the middle shelf; a copper counterweight cable running down the back."
    ),
    "W01_ALT_C001": (
        "CHALLENGER DESIGN (materially different from the incumbent vertical-lift door with piston "
        "columns): a counterweighted double swing-gate: two heavy half-doors hanging on visible pivot "
        "hinges, each with a small reinforced round viewport near its top; exposed copper counterweight "
        "arms and drum wheels mounted beside the frame; teal edge-light strips running down the two "
        "meeting edges so the closed seam glows as a thin vertical line; heavy threshold plate with "
        "worn hazard chevrons."
    ),
    "W01_ALT_C002": (
        "CHALLENGER DESIGN (materially different from the incumbent horizontal-split bulkhead): a "
        "vertical folding accordion grille bulkhead: tall narrow vertical slats that fold sideways into "
        "a deep wall pocket on one side; copper guide rails along the top and bottom edges; every third "
        "slat carries a thin teal edge-light so the closed door reads as a striped field; a small lock "
        "stator at pocket height; scuffed lower slats, one slightly dented."
    ),
    "W01_ALT_C003": (
        "CHALLENGER DESIGN (materially different from the incumbent rounded-top pressure door): a "
        "diagonal-split rectangular bulkhead: two unequal panels meeting on a stepped diagonal seam "
        "with interlocking teeth; heavy riveted rectangular frame; a single small reinforced porthole "
        "in the upper panel; teal lock indicators glowing at both ends of the seam; copper patch seams "
        "and old weld scars across the lower panel."
    ),
    "B02_ALT_C001": (
        "CHALLENGER DESIGN (materially different from the incumbent symmetric hall with a huge "
        "central teal reactor ring): an asymmetric deep-perspective bay: the composition pushes left "
        "with a towering vertical gantry crane armature holding a dormant station module, its copper "
        "cables sagging across the upper third; distant machinery language of stacked vertical gantry "
        "towers and docking clamps instead of colossal symmetric silhouettes; lighting arranged as "
        "several small scattered worklight pools along a maintenance catwalk plus one faint amber "
        "warning beacon far in the back instead of one central reactor glow; a long diagonal conveyor "
        "line with idle carriers leads the eye into depth on the right, where a single teal-cyan "
        "coolant column rises; exposed aged plating and conduit bundles on the near-left wall, deep "
        "quiet negative space across the middle band."
    ),
    "B02_ALT_C002": (
        "CHALLENGER DESIGN (materially different from the incumbent asymmetric collapsed machinery "
        "slope with hanging cables and cyan vapor columns): a sunken service-pit bay: the far deck "
        "opens into a wide maintenance pit exposing glowing sub-deck machinery below floor level, "
        "ringed by a cool spill-light rim; two slender vertical lift towers rise on the right with "
        "a parked service tram on a long horizontal rail line; a single taut cable-stayed mast "
        "replaces the hanging cables; lighting is a horizontal rhythm: pit-rim spill lights plus one "
        "warm amber crane beacon; the impossible filament vine climbs the far-left wall; deep quiet "
        "negative space across the middle band."
    ),
    "B02_ALT_C003": (
        "CHALLENGER DESIGN (materially different from the incumbent deep vertical shaft with stacked "
        "galleries and thin copper light lines): a great flywheel hall: a colossal slow flywheel "
        "governor half-visible in the far depth, its spokes catching teal rim light; strong "
        "horizontal banding with three stacked pipe galleries running the full width at different "
        "depths; two calm steam plumes rising from vents on the right; warm porthole lights spaced "
        "along the upper band instead of copper light lines; aged plating and conduit bundles low in "
        "the frame; wide quiet negative space across the middle band."
    ),
    "E02_ALT_C001": (
        "CHALLENGER DESIGN (materially different from the incumbent heavy plated look with thick "
        "bevels and generous copper ribs): an open lattice-truss vocabulary: thin-strut trusswork "
        "tiles, mesh-grating walkway plates you can see through, angle-brace corner pieces, sparse "
        "rivet dots; load-bearing struts marked with thin hydroponic-teal edge lines; copper used "
        "only as small joint collars; wear shown as hairline scratches and one dented-strut variant "
        "instead of heavy bevels and ribs; airy, engineered, precise."
    ),
    "E02_ALT_C002": (
        "CHALLENGER DESIGN (materially different from the incumbent conduit-and-cabling density with "
        "teal status LEDs on many panels): a plumbing-and-gauge vocabulary: rounded pressure-pipe "
        "runs with ring collars, small valve wheels, round dial gauges, vertical tank segments and "
        "drip trays as tile families; plain dusk-blue panels with copper brackets; glow used "
        "sparingly - only two gauge faces glow teal and a few LEDs are bone-white; rhythm of circles "
        "and cylinders instead of cable bundles."
    ),
    "E02_ALT_C003": (
        "CHALLENGER DESIGN (materially different from the incumbent aged repair patches, mismatched "
        "panel generations and moss-green residue): a clean ritual-upkeep vocabulary: deliberately "
        "tidy refurbished tiles - brushed metal with dark composite inlays in alternating diagonal "
        "hatching, a family of muted gold-and-navy safety chevron strip tiles, small engraved notch "
        "counters (tally marks only, no text), and one tile family with a subtle mythic gold "
        "filament inlay; wear is minimal soft edge scuffs; feels lovingly maintained, not decayed."
    ),
    "C02_ALT_C001": (
        "CHALLENGER DESIGN (materially different from the incumbent hook-shaped curls with gold "
        "bell-like pods and a leaning ready state): a whiplash fiddlehead vine: smooth confident "
        "S-curve strokes; stage 3 tip coiled like a fern fiddlehead; the READY state is one great "
        "coiled-spiral gold bud wound like a spring above loosely draping tendrils, with tiny violet "
        "spark dots; the whole growth gesture cascades diagonally toward one side rather than "
        "leaning."
    ),
    "C02_ALT_C002": (
        "CHALLENGER DESIGN (materially different from the incumbent zigzag kinked stems with teal "
        "sap dots and one oversized gold bud): a braided twin-tendril vine: two slender tendrils "
        "twist around each other up a thin copper stake, small crescent-shaped gold buds strung "
        "along the braid; the READY top bud is forked like a jester cap with a violet-green sheen; "
        "the escape gesture: one tendril deliberately slipping off the stake and hooking outward "
        "past the planter rim."
    ),
    "C02_ALT_C003": (
        "CHALLENGER DESIGN (materially different from the incumbent spiraling tendrils that exit and "
        "re-enter the soil with a gold mote halo): a question-mark flourish vine: elegant "
        "interrogation-hook strokes; stage 3 forms a looping arc hovering over the planter rim; the "
        "READY state is one bold hooked gold bud cluster shaped like a curled question mark with "
        "tiny leaf-keys, and a sparse trail of violet motes hanging after it like punctuation."
    ),
    "D01_ALT_C002": (
        "CHALLENGER DESIGN (materially different from the incumbent sitting-regally pose beside a "
        "cargo crate corner): Dexter in a calm sphinx lie: chest down, forepaws extended straight "
        "forward, head held high and perfectly level, tail wrapped over the front paws; no crate - "
        "instead a tiny folded woven trade blanket pinned beneath one forepaw; the coat interpreted "
        "smoother with a crisp white blaze down the chest; same floppy drop ears, same slightly "
        "grayed muzzle, same half-lidded unimpressed ancient authority; strict side view, compact "
        "reclining silhouette."
    ),
    "D01_ALT_C003": (
        "CHALLENGER DESIGN (materially different from the incumbent standing pose with a slight "
        "head-tilt of judgment and a thin teal collar tag): Dexter glancing back over his shoulder: "
        "body standing square but the head turned toward the viewer checking who approaches, ears "
        "swinging with the turn; no collar tag - instead a tiny brass botanist's loupe on a short "
        "cord at the chest; the coat interpreted with slightly wavy feathering and one crisp white "
        "forepaw sock; same floppy drop ears, same grayed muzzle, same half-lidded unimpressed "
        "ancient authority; strict side view body with the head-turn readable."
    ),
    "D02_ALT_C001": (
        "CHALLENGER DESIGN (materially different from the incumbent L-shaped counter with hanging "
        "seed pouches on the left): a barrel-stall kiosk: a big repurposed station cask laid on its "
        "side as the trade counter, its curved lid propped open on a copper stay showing seed "
        "drawers inside; a patchwork cloth canopy tensioned between two angled copper poles, tied "
        "down with visible cords; goods as stacked tin drawers and small glowing canisters on the "
        "cask end; clear open vendor space on the right."
    ),
    "D02_ALT_C002": (
        "CHALLENGER DESIGN (materially different from the incumbent repurposed cargo pod with "
        "flip-open lid): a slender carousel-rack kiosk: a tall narrow open frame rack with three "
        "visible shelf levels holding seed trays and glowing goods canisters, the shelves implied "
        "to rotate around a central copper post; a small fold-down counter leaf at waist height; a "
        "ribbed metal awning cap on top like a mushroom; clear open floor space in front of the "
        "leaf."
    ),
    "D02_ALT_C003": (
        "CHALLENGER DESIGN (materially different from the incumbent scaffold table with glowing "
        "canister rack and awning): a tandem-cart kiosk: two small linked utility carts at slightly "
        "different heights - the higher one carrying a latched glowing canister crate, the lower "
        "one holding shallow seed trays - joined by a short tow bar; a striped tarp awning "
        "stretched on two poles over the rear cart only; a few salvaged components strapped "
        "underneath; clear open vendor space on the left."
    ),
    "P01_ALT_C001": (
        "CHALLENGER DESIGN (materially different from the incumbent bulkier harness with rolled "
        "sleeves and gold-emblem cap): a lean layering silhouette: a long knee-length utility vest "
        "in deep navy over the dusk-blue jumpsuit, side-sling tool belt at the hip, bone-white "
        "sleeve rolled at one forearm only; headwear a narrow folded bandana in moss green with "
        "the hair tied back in a short practical tail; the walk read slightly brisker. Same "
        "technician-cultivator identity, same palette anchors, same 32x48 frame proportions and "
        "baseline."
    ),
    "P01_ALT_C002": (
        "CHALLENGER DESIGN (materially different from the incumbent slimmer open-collar look with "
        "teal knit cap): a compact workwear silhouette: a cropped canvas jacket in moss green over "
        "the jumpsuit with sleeves to the elbow, trouser cuffs rolled once showing bone-white "
        "socks above dark boots, small knee pads; headwear a bone-white painter's cap with a "
        "copper clip; short wavy hair visible at the edges. Same technician-cultivator identity, "
        "same palette anchors, same 32x48 frame proportions and baseline."
    ),
    "C01_ALT_C001": (
        "CHALLENGER DESIGN (materially different from the incumbent golden bulbous pod with folded "
        "lobes and teal stem collar): a lantern-fruit: the READY fruit is a translucent golden "
        "drupe shaped like a tiny paper lantern with a visible inner cluster of glowing seeds "
        "casting restrained teal light through the skin; sage-green leaves instead of collar "
        "foliage; the stem carries small ring nodes like a measuring rod; growth gesture a calm "
        "single curve."
    ),
    "C01_ALT_C002": (
        "CHALLENGER DESIGN (materially different from the incumbent elongated fruit with "
        "laurel-like gold leaves and teal veins): a totem fruit: the READY state stacks two "
        "smaller golden lobes one above the other like a tiny pagoda, the top lobe ringed by a "
        "faint floating teal wisdom-ring; stem gently spiraling; sparse narrow leaves low on the "
        "stem; glow restrained and inner."
    ),
    "T01_ALT_C001": (
        "CHALLENGER DESIGN (materially different from the incumbent rounded-top pedestal family "
        "with a single central lamp and side gauges): a tank-and-slab pair: LEFT repair terminal "
        "built as a vertical cylindrical tank pedestal with heavy copper banding, a fold-out tool "
        "tray at waist height, and an amber lamp recessed in the top rim; RIGHT replenish "
        "terminal as its slab-sided sibling with a front spigot arm ending in a dripping nozzle, "
        "a bubble-level window on its face, and a teal lamp on the spigot joint; same family, "
        "clearly different body geometry."
    ),
    "T01_ALT_C002": (
        "CHALLENGER DESIGN (materially different from the incumbent boxy industrial pedestals with "
        "angled console faces): a pylon pair: both terminals are tall tapering pylons on wide "
        "splayed feet; the LEFT repair pylon carries an open-framed coil cage glowing warm amber "
        "with a copper breaker lever on its side; the RIGHT replenish pylon holds a transparent "
        "helical water column lit soft teal with a small nozzle at its base; slim, vertical, "
        "elegant, same worn station family."
    ),
    "U01_ALT_C001": (
        "CHALLENGER DESIGN (materially different from the incumbent flat two-tone icons with one "
        "highlight cluster each): chunky enamel-badge icons: each glyph drawn as a rounded chunky "
        "enamel pin with a thick bone-white rim and a deep-navy fill; WATER droplet with an "
        "inner crescent; NUTRIENTS as a granule pouch with a rolled fold; POWER bolt with a "
        "double-struck zigzag; WISDOM FRUIT with two visible seed dots; the E key cap drawn as a "
        "round badge with a copper rim. Strong single-weight outlines, no gradient."
    ),
    "U01_ALT_C002": (
        "CHALLENGER DESIGN (materially different from the incumbent dark key-cap backing tiles "
        "behind each glyph): floating-glyph icons with no backings: each symbol hangs free with a "
        "thin dark outline and an inner bone-white core line; WATER as a tilted double-droplet "
        "pair; NUTRIENTS as a triangular flask with visible granules; POWER as a plug seen "
        "side-on with two prongs and a short cable curl; WISDOM FRUIT as a folded fan shape with "
        "a teal glint line; the E key cap as a slim hexagonal cap. Airy, high negative space, "
        "one accent pixel cluster per icon."
    ),
    "E01_ALT_C001": (
        "CHALLENGER DESIGN (materially different from the incumbent bright clean hydroponic "
        "machinery and glass framing with strong teal glow): a copper-and-ceramic botanical "
        "vitrine vocabulary: grow-medium floor panels with visible seeded furrow rows, "
        "bone-white ceramic grow-trough rims instead of metal planter rims, copper-framed glass "
        "cloche tiles with faint green tint, slim watering rails with copper joints, small "
        "trellis-arch tiles; teal appears only as the tiny living sprout glows and one seedling "
        "lamp tile; overall warmer and more botanical, less machinery glow."
    ),
    "E01_ALT_C002": (
        "CHALLENGER DESIGN (materially different from the incumbent aged patched plating with "
        "moss overgrowth creeping on tiles): an orchestrated air-and-water vocabulary: perforated "
        "mist-grate floor tiles with visible hole patterns, slim water-channel tiles with copper "
        "rims and calm reflective fills, arched hoop-support tiles for climbing plants, "
        "condensation-drop decorative tiles, louvered vent tiles in neat banks, small fogger "
        "nozzle props; green appears as deliberate crops (sprout rows on channel edges) rather "
        "than moss residue; feels like a working greenhouse machine for plants."
    ),
    "B01_ALT_C001": (
        "CHALLENGER DESIGN (materially different from the incumbent huge glazed dome curve with "
        "a distant gold tree silhouette): a terraced grow-bay canyon: the greenhouse interior "
        "steps down in wide terraces from the upper left, thin nutrient waterfalls dropping "
        "between terrace edges; a calm giant seed-shaped bioreactor glows soft teal in the mid "
        "depth; the impossible gold plant canopy hangs DOWN from overhead trellis arms instead of "
        "standing; tall glazing panels on the far right with stars beyond; patched panels and "
        "copper weld seams along the terrace lips; wide quiet negative space across the middle "
        "band."
    ),
    "B01_ALT_C002": (
        "CHALLENGER DESIGN (materially different from the incumbent long horizontal window band "
        "with nebula and stacked rack silhouettes): an under-canopy vista: seen from a lower "
        "deck, a vast ceiling of impossible gold-tinged foliage spans the upper third filtering "
        "bone-white light into soft shafts; slender support columns with ring platforms recede "
        "into depth; a tall vertical glazing wall on the far left opens onto deep space with "
        "stars and a thin teal nebula wash; low mist band across the middle distance; hydroponic "
        "rails and pipe runs low in the frame; wide quiet negative space across the middle band."
    ),
    "V01_ALT_C001": (
        "CHALLENGER DESIGN (materially different from the incumbent dense particle clusters with "
        "strong contrast): ring-geometry effects: HARVEST BURST as an expanding double ring of "
        "gold shard triangles with a small inner four-point star; REPAIR SPARK as two orbiting "
        "clamp-shaped sparks trailing short copper bolt strokes; GROWTH GLOW as a rising helix "
        "of teal-green motes on a faint vertical axis; INTERACTION PING as a double-line hollow "
        "diamond pulse with four outward tick marks. Clean orbital geometry, medium density."
    ),
    "V01_ALT_C002": (
        "CHALLENGER DESIGN (materially different from the incumbent lighter sparser effects with "
        "thin strokes): stamp-glyph effects: HARVEST BURST as a radial stamp of eight chunky "
        "triangular gold shards from a tiny core dot; REPAIR SPARK as one bold crossed-bolt "
        "stroke with two copper nodes; GROWTH GLOW as three short columns of ascending spore "
        "dots at different heights; INTERACTION PING as a single thick hollow ring with four "
        "tick marks and one small center dot. Bold and legible, generous negative space inside "
        "each cell."
    ),
    "C03_ALT_C001": (
        "CHALLENGER DESIGN (materially different from the incumbent rounded storm-bulb fruits "
        "with forked micro-arcs between them): a coil-ladder storm vine: the stems grow as a "
        "narrow zigzag ladder coil like a Jacob's ladder with small ceramic insulator discs at "
        "each rung; sparks hop rung to rung in pale electric blue-white; the READY state crowns "
        "a single Anthurium-like spathe fruit - a bright coil nest cradled in an open spathe "
        "leaf - with a tight arc halo around the nest."
    ),
    "C03_ALT_C002": (
        "CHALLENGER DESIGN (materially different from the incumbent tall thin stems ending in "
        "sparking bud spires): a bonsai storm tree: a miniature gnarled trunk with two flat "
        "layered canopy discs like a tiny bonsai; arcs hop along the canopy edges; small "
        "insulator beads stud the trunk; the READY state gathers one bright gold-cored coil "
        "nest at the trunk fork, with contained lightning visibly feeding it from the canopy "
        "above."
    ),
    "D01_ALT_C001": (
        "CHALLENGER DESIGN (materially different from the incumbent standing-proud pose with leather "
        "satchel): Dexter mid-strut: an unhurried three-legged walk with the tail carried high and "
        "curved, one forepaw lifted mid-step; no satchel - instead a tiny rolled seed-cloth bundle held "
        "gently and precisely in his mouth; the coat interpreted slightly fluffier and wind-brushed "
        "with stronger warm-tan patches over the eyes and cheeks; same floppy drop ears, same grayed "
        "muzzle, same half-lidded unimpressed authority."
    ),
}

AXES = {
    "A01_ALT_C001": ["chassis geometry: tall lantern-spine vs boxy rounded slab",
                     "tending mechanism: three fanned care arms vs one folded arm",
                     "locomotion: annular ring thruster vs single underside nozzle",
                     "silhouette: tall narrow with high negative space vs compact low"],
    "A01_ALT_C002": ["chassis geometry: low wedge skimmer vs round pod",
                     "tending mechanism: seed hopper + needle spout vs pot cradle + misting nozzle",
                     "locomotion: caged rear tilt-fans vs twin mini thrusters",
                     "surface: bone pin-striping vs plain hull"],
    "A01_ALT_C003": ["chassis geometry: sphere-in-cage vs low wide hexagon",
                     "tending mechanism: equatorial pincer tenders vs side clipper arm",
                     "locomotion: gimbal core hover vs visible thrusters",
                     "internal rhythm: radial symmetric vs asymmetric layout"],
    "T02_ALT_C001": ["console architecture: cantilevered off-balance head vs full monolith",
                     "display: rising helix data thread vs one large tilted plane",
                     "support: single heavy pillar vs monolith body",
                     "information-light: cyan helix over specimen dish vs violet rim light"],
    "T02_ALT_C002": ["console architecture: sweeping arc console vs twin columns",
                     "display: downward data cone onto floating prism vs orbiting holo rings",
                     "support: continuous arc base vs two separate columns",
                     "specimen treatment: floating prism in open cradle vs central core column"],
    "T02_ALT_C003": ["console architecture: three offset elevator shelves vs squat console body",
                     "scan-hood: flush-integrated in top shelf vs tall thin sensor mast",
                     "display: glyphs spiraling around column vs holo-lattice above",
                     "module rhythm: discrete stacked shelves with dials vs single console mass"],
    "W01_ALT_C001": ["opening mechanism: hinged swing-gate vs vertical lift",
                     "external hardware: exposed counterweights + drum wheels vs piston columns",
                     "status lighting: teal edge strips on meeting edges vs top band",
                     "panel treatment: reinforced viewports in solid halves vs plated lift panels"],
    "W01_ALT_C002": ["opening mechanism: accordion fold into wall pocket vs horizontal split",
                     "panel segmentation: many vertical slats vs two solid panels",
                     "status lighting: repeated slat edge-lights vs single central seal",
                     "visual rhythm: striped vertical field vs two heavy masses"],
    "W01_ALT_C003": ["opening mechanism: diagonal split with interlocking teeth vs rounded pressure hull",
                     "seam language: stepped diagonal vs circular lock indicator",
                     "panel treatment: riveted rectangular panels + porthole vs segmented dome frame",
                     "wear story: copper patch seams and weld scars vs thick segmented frame"],
    "B02_ALT_C001": ["architectural depth composition: asymmetric gantry-crane left-weighted depth vs symmetric hall",
                     "distant machinery language: stacked gantry towers + docking clamps vs colossal symmetric silhouettes",
                     "light-source arrangement: scattered worklight pools + one far amber beacon vs single central reactor ring",
                     "structural rhythm: diagonal conveyor line leading into depth vs central radial symmetry"],
    "B02_ALT_C002": ["spatial concept: sunken service pit below deck level vs collapsed machinery slope",
                     "cable language: single taut cable-stayed mast vs hanging cable bundles",
                     "atmosphere: calm pit-rim spill lights + rail rhythm vs cyan vapor columns",
                     "depth markers: lift towers + parked tram on horizontal rail vs slope silhouette"],
    "B02_ALT_C003": ["spatial concept: colossal half-hidden flywheel in deep depth vs vertical shaft galleries",
                     "structural rhythm: horizontal stacked pipe galleries vs vertical stacking",
                     "light language: warm porthole lights along top band vs thin copper light lines",
                     "atmosphere: calm steam plumes vs shaft void"],
    "E02_ALT_C001": ["modular vocabulary: thin-strut lattice trusses + mesh gratings vs heavy plated slabs",
                     "material breakup: airy see-through grating tiles vs thick bevels",
                     "copper usage: small joint collars only vs generous copper ribs",
                     "wear pattern: hairline scratches + one dented strut vs heavy bevel wear"],
    "E02_ALT_C002": ["modular vocabulary: pipes, valves, gauges, tank segments vs conduits and cables",
                     "shape rhythm: circles and cylinders vs linear cable bundles",
                     "light language: two glowing gauge faces + bone-white LEDs vs many teal LEDs",
                     "decorative family: drip trays and ring collars vs status-LED panels"],
    "E02_ALT_C003": ["wear story: clean ritual upkeep with soft scuffs vs aged patches and moss",
                     "panel language: brushed metal + composite diagonal-hatch inlays vs mismatched generations",
                     "accent family: muted gold/navy chevron strips + notch counters vs moss residue tiles",
                     "mythic note: one gold filament inlay family vs organic moss growth"],
    "C02_ALT_C001": ["botanical morphology: fiddlehead spiral strokes vs hook-shaped curls",
                     "bud structure: one coiled-spring spiral bud vs bell-like pods",
                     "growth gesture: diagonal cascade vs visible lean",
                     "accent: violet spark dots vs gold pod glow only"],
    "C02_ALT_C002": ["botanical morphology: two tendrils braided up a copper stake vs zigzag kinked stems",
                     "bud structure: crescent buds strung along the braid + forked jester-cap top vs one oversized bud",
                     "support element: thin copper stake (new prop) vs free-standing stems",
                     "accent language: violet-green sheen on top bud vs teal sap dots"],
    "C02_ALT_C003": ["botanical morphology: interrogation-hook question-mark strokes vs exit-and-reenter spirals",
                     "ready state: bold hooked bud cluster with leaf-keys vs mote halo",
                     "stage-3 gesture: looping arc hovering over the rim vs tendrils re-entering soil",
                     "accent language: sparse violet punctuation motes vs gold mote halo"],
    "D01_ALT_C002": ["pose: calm sphinx lie with tail over paws vs sitting regally upright",
                     "prop: tiny folded woven trade blanket under one paw vs cargo crate corner",
                     "coat interpretation: smoother coat with crisp white chest blaze vs silky natural fall",
                     "silhouette: long low reclining mound vs upright seated posture"],
    "D01_ALT_C003": ["pose: glancing back over the shoulder vs standing with slight head-tilt",
                     "accessory: tiny brass botanist's loupe on a cord vs thin teal collar tag",
                     "coat interpretation: wavy feathering + one white forepaw sock vs smooth silky fall",
                     "gaze: head turned toward viewer, ears swinging vs level forward gaze"],
    "D02_ALT_C001": ["counter architecture: cask laid on its side with propped lid vs L-shaped counter",
                     "canopy: patchwork cloth tensioned on angled copper poles vs fixed strut canopy",
                     "storage: stacked tin drawers + drawers inside the cask vs hanging seed pouches",
                     "silhouette: curved barrel mass vs angular L"],
    "D02_ALT_C002": ["kiosk structure: tall slender carousel rack vs repurposed cargo pod box",
                     "display: rotating shelf levels around a copper post vs flip-open lid display",
                     "counter: small fold-down leaf vs pod lid",
                     "silhouette: vertical slender frame with mushroom cap vs boxy pod"],
    "D02_ALT_C003": ["base: two linked utility carts at stepped heights vs single scaffold table",
                     "awning: striped tarp on two poles over rear cart only vs fixed awning",
                     "goods arrangement: latched canister crate + shallow seed trays vs glowing rack",
                     "silhouette: tandem stepped carts vs one table mass"],
    "P01_ALT_C001": ["outfit layering: long knee-length navy utility vest vs jumpsuit with rolled sleeves",
                     "headwear: narrow moss-green folded bandana, hair in short tail vs gold-emblem cap",
                     "harness: side-sling tool belt at the hip vs bulkier back harness",
                     "walk read: brisker stride phrasing vs standard walk cycle"],
    "P01_ALT_C002": ["outfit layering: cropped moss-green canvas jacket vs slim open-collar jumpsuit",
                     "headwear: bone-white painter's cap with copper clip vs teal knit cap",
                     "legwear detail: rolled cuffs + knee pads + white socks vs plain trousers",
                     "silhouette rhythm: compact cropped torso vs long lean lines"],
    "C01_ALT_C001": ["fruit structure: translucent lantern-drupe with inner glowing seed cluster vs bulbous folded pod",
                     "foliage: sage-green leaves vs teal-glow stem collar",
                     "stem detail: ring nodes like a measuring rod vs plain collar",
                     "glow treatment: inner translucency vs luminescence between folds"],
    "C01_ALT_C002": ["fruit architecture: two stacked golden lobes like a tiny pagoda vs single elongated fruit",
                     "ornament: faint floating teal wisdom-ring around the top lobe vs laurel-like gold leaves",
                     "stem gesture: gently spiraling vs straight slender",
                     "glow treatment: restrained inner glow vs teal veins"],
    "T01_ALT_C001": ["body geometry: cylindrical tank (L) + slab (R) vs rounded-top pedestals",
                     "service element: fold-out tool tray vs side gauges",
                     "lamp placement: recessed in top rim (L) / on spigot joint (R) vs single central lamp",
                     "display: bubble-level window + spigot arm vs console face gauges"],
    "T01_ALT_C002": ["body geometry: tall tapering pylons on splayed feet vs boxy industrial pedestals",
                     "display element: open-framed amber coil cage (L) / transparent helical column (R) vs angled consoles",
                     "accents: copper breaker lever (L) / nozzle at base (R) vs base cable stubs",
                     "silhouette: slim vertical elegant vs wide boxy stance"],
    "U01_ALT_C001": ["icon construction: chunky enamel-badge glyphs with thick bone rims vs flat two-tone fills",
                     "WATER treatment: inner crescent droplet vs plain droplet",
                     "NUTRIENTS shape: rolled-fold granule pouch vs flask",
                     "E cap: round badge with copper rim vs plain dark key cap"],
    "U01_ALT_C002": ["icon construction: free-floating outlined glyphs, no backings vs key-cap backing tiles",
                     "WATER treatment: tilted double-droplet pair vs single droplet",
                     "POWER shape: side-on plug with cable curl vs lightning bolt",
                     "E cap: slim hexagonal cap vs rounded square cap"],
    "E01_ALT_C001": ["material vocabulary: copper-framed glass cloches + ceramic troughs vs metal machinery blocks",
                     "floor language: seeded furrow grow-medium panels vs plain worn plates",
                     "accent strategy: teal only as living sprout glows vs strong teal machinery glow",
                     "prop family: trellis arches + watering rails vs vents and machine blocks"],
    "E01_ALT_C002": ["material vocabulary: mist grates + water channels + hoop supports vs patched plating",
                     "green presence: deliberate crop rows on channel edges vs creeping moss",
                     "decorative family: condensation drops + fogger nozzles vs worn patch scars",
                     "air treatment: louvered vent banks + perforation patterns vs solid aged panels"],
    "B01_ALT_C001": ["spatial concept: stepped terrace canyon descending left vs one huge dome curve",
                     "water language: thin nutrient waterfalls between terraces vs none",
                     "mythic anchor: calm giant seed-shaped bioreactor mid-depth vs distant gold tree silhouette",
                     "canopy treatment: gold foliage hanging down from overhead trellis vs standing tree"],
    "B01_ALT_C002": ["spatial concept: under-canopy vista from a lower deck vs long horizontal window band",
                     "light language: soft bone-white shafts filtered by foliage vs nebula wash through windows",
                     "depth markers: slender columns with ring platforms vs stacked rack silhouettes",
                     "glazing placement: tall vertical wall far left vs horizontal band"],
    "V01_ALT_C001": ["effect geometry: expanding rings + orbital clamps vs dense particle bursts",
                     "burst structure: double ring of shard triangles + inner star vs radiating cluster",
                     "glow gesture: rising helix of motes on an axis vs free-floating spores",
                     "ping treatment: double-line hollow diamond vs single ring pulse"],
    "V01_ALT_C002": ["effect geometry: bold radial stamps and single strokes vs lighter scattered effects",
                     "burst structure: eight chunky shard triangles from a core dot vs sparse shards",
                     "spark treatment: one crossed-bolt stroke with copper nodes vs diffuse spark cluster",
                     "density rhythm: high negative space with chunky marks vs thin-stroke sparseness"],
    "C03_ALT_C001": ["plant architecture: Jacob's-ladder coil stems with insulator discs vs rounded storm bulbs",
                     "spark path: arcs hopping rung to rung vs forked micro-arcs between fruits",
                     "READY structure: coil nest cradled in an open spathe vs clustered bulb fruits",
                     "growth gesture: narrow vertical ladder vs bushy vine"],
    "C03_ALT_C002": ["plant architecture: gnarled bonsai trunk with flat canopy discs vs tall thin spires",
                     "spark path: arcs hopping along canopy edges vs tip sparks",
                     "READY structure: gold-cored coil nest at the trunk fork vs sparking bud spires",
                     "silhouette: miniature layered tree vs upright stems"],
    "D01_ALT_C001": ["pose: unhurried mid-strut walk vs standing proud",
                     "trade detail: rolled seed-cloth bundle held in mouth vs leather satchel strap",
                     "coat interpretation: fluffier wind-brushed with stronger tan patches vs silky smooth",
                     "silhouette: extended stride with high tail vs compact upright stance"],
}


def alt_prompt(alt_cid):
    slot = alt_cid.split("_ALT_")[0]
    slot_id = next(k for k in SLOTS if k.split("_")[0] == slot)
    return SHARED + "  " + SLOT_CONTRACT[slot_id] + "  " + CHALLENGER[alt_cid]


ALT_SPECS = {
    cid: dict(axes=AXES[cid], prompt=alt_prompt(cid)) for cid in CHALLENGER
}
