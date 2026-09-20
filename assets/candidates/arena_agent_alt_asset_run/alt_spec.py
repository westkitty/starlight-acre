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
