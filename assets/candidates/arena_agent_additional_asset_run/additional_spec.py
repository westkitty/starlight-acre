#!/usr/bin/env python3
"""Starlight Acre ADDITIONAL asset run — discovered slot specs, contracts, prompts.

Discovery is FROZEN here (see DISCOVERED_ASSETS.json for evidence). Slot IDs are new;
none reuse the 18 established families from the two prior foundry runs.
Prompt = SHARED identity block (style lock, imported from the original run) + a hardened
slot contract (anti-failure directives learned from both prior runs) + a variant design.
"""
import os, sys

ORIG_ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "arena_agent_asset_run"))
if ORIG_ROOT not in sys.path:
    sys.path.insert(0, ORIG_ROOT)

from run_spec import SHARED  # style lock: identical Starlight Acre identity block

# New slots. priority: A (current playable-build gap) / B (documented near-term) /
# C (modular environment polish). Candidates: A=3, B=2, C=1.
SLOTS = {
    "A02_REACTOR_CORE": dict(priority="A", w=96, h=96, alpha=True, count=3,
        category="machinery prop",
        layout="single prop, 96x96 canvas (6x6 tiles of 16px, NEWLY PROPOSED dimensions), hover/center anchor",
        base=(
            "The station's Energy Reactor core for a 2D side-view pixel game: exactly ONE reactor core "
            "prop centered on a solid flat pure magenta #FF00FF background (one flat single color edge "
            "to edge, no checkerboard, no gradient, no border, no frame, no caption panel). Slightly "
            "square 1:1 composition. Strict side view. A contained luminous teal-cyan plasma heart "
            "held inside worn station hardware: dusk-blue and station-gray housing, maintenance copper "
            "feed lines and bolts, subtle repair seams; the glow reads as restrained and calm, not "
            "explosive; dark subtle outline; clean hard pixel-cluster edges against the background. "
            "It must read as the power heart of the engineering bay at gameplay scale. No readable "
            "text, no second core, no duplicate views, no floor, no stage, no drop shadow on the "
            "background, no presentation board."
        ),
        variants=[
            "Variant 1: a glowing teal plasma TORUS held upright in a copper-ringed gimbal frame on a "
            "single station-gray pedestal drum, three copper feed conduits curving into the base.",
            "Variant 2: a vertical crystalline core column in a cage of four copper struts, its teal "
            "heart segmented like stacked glass cells, standing on a wide dusk-blue base plate.",
            "Variant 3: a suspended teal sphere core floating between two angled electromagnet arms "
            "mounted on one pylon, tiny contained arc filaments hopping between the arms and the sphere.",
        ]),

    "U02_HUD_EXTENSION_ICONS": dict(priority="A", w=96, h=16, alpha=True, count=3,
        category="UI icons",
        layout="icon strip 96x16, six 16x16 icons in a row: resupply canister / biomass / research data / anomaly residue / upgrade component / seed",
        base=(
            "HUD extension icon strip for a 2D pixel game: ONE row of six 16x16 pixel icons on a very "
            "wide thin strip (96x16 proportion, 6:1), on a solid flat pure magenta #FF00FF background "
            "that is ONE single flat color edge to edge - between icons, around glyphs, across the "
            "whole strip - with no border, no frame, no caption panel, no drawn dividing lines. Icon 1 "
            "EMERGENCY RESUPPLY: a small supply canister with a strap clip. Icon 2 BIOMASS: a compact "
            "leafy moss-green clump. Icon 3 RESEARCH DATA: a small data crystal or lattice shard in "
            "cyan-teal. Icon 4 ANOMALY RESIDUE: a tiny violet flask with a droplet. Icon 5 UPGRADE "
            "COMPONENT: a small gear-and-chip fitting in station gray with a copper rim. Icon 6 SEED: "
            "a single large seed with a tiny sprout line. Each icon is complete and centered inside "
            "its own 16x16 cell; strong tiny-scale readability, bold single-pixel outlines, high "
            "contrast, GBA/SNES pixel art; absolutely no letters, no words, no numbers anywhere."
        ),
        variants=[
            "Variant 1: solid two-tone icons with one highlight pixel cluster each.",
            "Variant 2: badge icons: each glyph on a small dark rounded chip with a thin bone-white rim.",
            "Variant 3: open line-glyph icons with a dark outline and one warm accent pixel cluster each.",
        ]),

    "T03_TERMINAL_ACTIVE_GLOW": dict(priority="A", w=64, h=64, alpha=True, count=3,
        category="VFX overlay",
        layout="glow overlay sheet 64x64, two 32x64 regions matching terminals.png: LEFT repair (warm amber) / RIGHT replenish (teal)",
        base=(
            "Terminal active-glow overlay sheet for a 2D side-view pixel game: a square 64x64-"
            "proportioned canvas on a solid flat pure magenta #FF00FF background (one flat color edge "
            "to edge, no border, no frame) containing exactly TWO soft glow overlays side by side, "
            "each filling its own 32-wide by 64-tall half. LEFT half: a warm amber-copper luminous "
            "aura shaped like an upright terminal pedestal (repair terminal active glow). RIGHT half: "
            "a hydroponic-teal luminous aura shaped like an upright terminal pedestal (replenish "
            "terminal active glow). Deliberate GBA/SNES pixel-cluster glow: clustered dither steps, "
            "hard pixel edges, NO smooth gradients, no blur, no anti-aliasing; darker core silhouette "
            "implied by denser clusters, brighter at the edges that would touch machinery. No text, "
            "no letters, no machinery drawn - glow shapes only, no third glow, nothing crossing the "
            "middle seam."
        ),
        variants=[
            "Variant 1: rounded halo auras - layered rounded-rectangle glow shells, brightest along "
            "the top edge of each pedestal shape.",
            "Variant 2: rising mote columns - columns of small glow motes climbing each half with a "
            "soft base pool at the bottom.",
            "Variant 3: ring-pulse auras - two nested outline rings per half with tiny spark ticks at "
            "the corners.",
        ]),

    "A03_ENGINEER_DRONE": dict(priority="B", w=32, h=32, alpha=True, count=2,
        category="agent sprite",
        layout="single sprite, 32x32, hover center anchor (matches GardenerDrone A01 family)",
        base=(
            "A small automated orbital ENGINEER drone for a 2D side-view pixel game: exactly ONE "
            "drone, single sprite centered on a solid flat pure magenta #FF00FF background (one flat "
            "single color edge to edge, no checkerboard, no gradient, no border, no frame, no caption "
            "panel). Square 1:1 composition. Strict side view. This drone's job is STATION SYSTEMS "
            "work, visibly different from a gardening drone: cable runs, diagnostics and power "
            "hardware; worn station-metal hull in station gray and dusk blue with copper accents and "
            "a small amber readout; hover center anchor; clearly a non-human helper. Dark subtle "
            "outline, clean hard edges against the background. No weapons, no combat language, no "
            "giant antennae, no cartoon mascot face, no huge expressive eyes, no humanoid body, no "
            "second drone or duplicate, no floor, no stage, no drop shadow on the background."
        ),
        variants=[
            "Variant 1: a drum-bodied cable-layer drone with a visible copper cable spool on its side, "
            "a thin probe arm extended forward, and a small amber diagnostic readout strip.",
            "Variant 2: a twin-boom systems drone carrying a tiny diagnostic visor on an extendable "
            "arm and two folded conductor wands, hovering on three small caged thrusters.",
        ]),

    "A04_HARVESTER_DRONE": dict(priority="B", w=32, h=32, alpha=True, count=2,
        category="agent sprite",
        layout="single sprite, 32x32, hover center anchor (matches GardenerDrone A01 family)",
        base=(
            "A small automated orbital HARVESTER drone for a 2D side-view pixel game: exactly ONE "
            "drone, single sprite centered on a solid flat pure magenta #FF00FF background (one flat "
            "single color edge to edge, no checkerboard, no gradient, no border, no frame, no caption "
            "panel). Square 1:1 composition. Strict side view. This drone's job is GENTLE HARVESTING "
            "and produce carrying, visibly different from a gardening drone: a soft-grip claw or "
            "cutter and a visible produce basket, crate or scoop; worn station-metal hull in station "
            "gray and dusk blue with moss green and warm gold accents; hover center anchor; clearly a "
            "non-human helper. Dark subtle outline, clean hard edges against the background. No "
            "weapons, no combat language, no giant antennae, no cartoon mascot face, no huge "
            "expressive eyes, no humanoid body, no second drone or duplicate, no floor, no stage, no "
            "drop shadow on the background."
        ),
        variants=[
            "Variant 1: a basket-drone: rounded hull with a woven station-gray produce basket slung "
            "underneath, one soft pincer claw folded above it, single ducted hover fan.",
            "Variant 2: a low scoop-tram: flat skimmer body with a front scoop tray holding two tiny "
            "gold fruits, a gentle cutter wheel at the lip, twin rear thrusters.",
        ]),

    "A05_MAINTENANCE_DRONE": dict(priority="B", w=32, h=32, alpha=True, count=2,
        category="agent sprite",
        layout="single sprite, 32x32, hover center anchor (matches GardenerDrone A01 family)",
        base=(
            "A small automated orbital MAINTENANCE drone for a 2D side-view pixel game: exactly ONE "
            "drone, single sprite centered on a solid flat pure magenta #FF00FF background (one flat "
            "single color edge to edge, no checkerboard, no gradient, no border, no frame, no caption "
            "panel). Square 1:1 composition. Strict side view. This drone's job is SURFACE REPAIR AND "
            "UPKEEP, visibly different from gardening and engineering drones: scrubbing, polishing, "
            "sealant and inspection hardware; worn station-metal hull in station gray and dusk blue "
            "with maintenance copper accents and a small bone-white inspection lamp; hover center "
            "anchor; clearly a non-human helper. Dark subtle outline, clean hard edges against the "
            "background. No weapons, no combat language, no giant antennae, no cartoon mascot face, "
            "no huge expressive eyes, no humanoid body, no second drone or duplicate, no floor, no "
            "stage, no drop shadow on the background."
        ),
        variants=[
            "Variant 1: a rounded wall-crawler puck with two rotating brush pads underneath and a "
            "small polish-wheel on an arm, hovering close to its work height.",
            "Variant 2: a compact sealant drone with a copper spray nozzle on a short boom, a tiny "
            "patch-material hopper on its back, and a bone-white inspection lamp at the front.",
        ]),

    "B03_DOCKING_COLLAR": dict(priority="B", w=64, h=96, alpha=True, count=2,
        category="module fixture",
        layout="single prop, 64x96 canvas (4x6 tiles of 16px, NEWLY PROPOSED dimensions), bottom-center anchor",
        base=(
            "A universal docking collar fixture for the station's Docking Bay in a 2D side-view pixel "
            "game: exactly ONE fixture prop centered on a solid flat pure magenta #FF00FF background "
            "(one flat single color edge to edge, no checkerboard, no border, no frame). Tall portrait "
            "composition about 2:3. Strict side view, frontal face of the fixture. Worn docking "
            "hardware: a heavy dusk-blue and station-gray collar ring with maintenance copper clamp "
            "petals or arms, teal guide lights in a calm ring, worn seal material, subtle scuffs and "
            "old repair seams; clearly the berth where a visiting ship or Dexter's trader vessel "
            "docks. Dark subtle outline. No readable text, no ship, no second fixture, no floor, no "
            "stage, no drop shadow on the background."
        ),
        variants=[
            "Variant 1: a circular universal collar: round hatch opening with four copper clamp "
            "petals and a ring of small teal guide lights, bolted rectangular backing plate.",
            "Variant 2: a rectangular freight airlock: tall cargo mouth with pressurized roller seal "
            "strips, side ram clamps, and chevron guide lights above the opening.",
        ]),

    "B04_HYDROPONICS_RIG": dict(priority="B", w=64, h=64, alpha=True, count=2,
        category="machinery prop",
        layout="single prop, 64x64 canvas (4x4 tiles of 16px, NEWLY PROPOSED dimensions), bottom-center anchor",
        base=(
            "A hydroponics water-recycling rig for the station's Hydroponics Wing in a 2D side-view "
            "pixel game: exactly ONE machine prop centered on a solid flat pure magenta #FF00FF "
            "background (one flat single color edge to edge, no checkerboard, no border, no frame). "
            "Slightly square 1:1 composition. Strict side view. Worn station hardware in dusk blue "
            "and station gray with maintenance copper pipes and fittings; visible water in calm "
            "hydroponic teal: tanks, gauges, filter cartridges and drip lines; a small moss-green "
            "trace of life where water feeds a plant rail; clearly a water recycling machine, calm "
            "and functional. Dark subtle outline. No readable text, no second machine, no floor, no "
            "stage, no drop shadow on the background."
        ),
        variants=[
            "Variant 1: twin round tanks joined by a copper manifold, a drip rail arm extending to "
            "one side, two small sight-gauge windows glowing teal.",
            "Variant 2: a vertical rack of slim nutrient tubes around a small pump heart, with a "
            "topfill reservoir and a row of tiny gauge dials.",
        ]),

    "B05_ARCHIVE_STACK": dict(priority="B", w=64, h=80, alpha=True, count=2,
        category="module fixture",
        layout="single prop, 64x80 canvas (matches research terminal scale), bottom-center anchor",
        base=(
            "An archive data-stack for the station's Archive Library in a 2D side-view pixel game: "
            "exactly ONE tall shelf prop centered on a solid flat pure magenta #FF00FF background "
            "(one flat single color edge to edge, no checkerboard, no border, no frame). Slightly "
            "tall portrait composition (about 4:5). Strict side view. A worn dusk-blue and "
            "station-gray cabinet stack with maintenance copper trim; the archived knowledge shown "
            "as small glowing data crystals or sealed vials in tidy rows, cyan-teal with restrained "
            "violet accents; one small retrieval arm or reader probe; calm, precious, slightly "
            "uncanny. Dark subtle outline. No readable text, no letters, no second cabinet, no "
            "floor, no stage, no drop shadow on the background."
        ),
        variants=[
            "Variant 1: three stacked shelf rows of glowing data crystals behind a copper-framed "
            "glass front, small reader probe arm at the middle shelf.",
            "Variant 2: a rounded data-drum cabinet with a spiral of sealed vial slots and a tiny "
            "retrieval claw at the top, one slot glowing brighter.",
        ]),

    "V02_HAZARD_VFX": dict(priority="B", w=128, h=32, alpha=True, count=2,
        category="VFX",
        layout="vfx strip 128x32, four consecutive 32x32 cells: solar flare / anomaly shimmer / malfunction sparks / power failure",
        base=(
            "Hazard VFX sprite strip for a 2D pixel game: ONE row of four consecutive 32x32 cells on "
            "a wide 4:1 strip (128x32 proportion), each effect isolated and centered in its own "
            "cell, on a solid flat pure magenta #FF00FF background that is ONE single flat color "
            "edge to edge - between cells, around effects, across the whole strip - with no border, "
            "no frame, no caption panel, no drawn dividing lines. EVERY one of the four cells must "
            "actually contain its effect, fully inside the cell, nothing crossing cell boundaries. "
            "Cell 1 SOLAR FLARE: a wash of warm gold-red diagonal ray shards from one corner. Cell "
            "2 MYTHIC ANOMALY: a violet shimmer of floating mote clusters and one small distortion "
            "ring. Cell 3 SYSTEM MALFUNCTION: a spark shower of copper-orange bolt strokes falling "
            "from a small failing node. Cell 4 POWER FAILURE: a dimming bone-white light strip with "
            "dark flicker strokes and two dying glow dots. GBA/SNES pixel art, hard pixel clusters, "
            "no smooth gradients, no text, no letters anywhere."
        ),
        variants=[
            "Variant 1: denser particle clusters, stronger contrast.",
            "Variant 2: sparser effects, thinner strokes, more negative space inside each cell.",
        ]),

    "E03_CARGO_PROPS": dict(priority="C", w=64, h=64, alpha=True, count=1,
        category="environment props",
        layout="prop sheet 64x64, 2x2 grid of 32x32 props: cargo crate / sealed canister / tool case / seed rack",
        base=(
            "Cargo and storage prop sheet for a 2D side-view pixel game: a strict 2x2 grid of four "
            "consecutive 32x32 cells on a square 64x64-proportioned canvas - top-left, top-right, "
            "bottom-left, bottom-right - on a solid flat pure magenta #FF00FF background that is ONE "
            "single flat color edge to edge, between cells and around props, with absolutely no grid "
            "lines, no separating borders, no frame, no caption panel. Top-left: a worn station "
            "cargo crate in dusk blue with copper corner brackets. Top-right: a sealed cylindrical "
            "supply canister in station gray with a teal seal ring. Bottom-left: a compact tool case "
            "with a copper latch and a small bone-white handle. Bottom-right: a small seed rack "
            "holding a few tiny seed trays with one moss-green sprout. Worn, repaired, lived-in "
            "orbital hardware; GBA/SNES pixel art, dark subtle outlines; no readable text, no "
            "letters, no characters, no floor, no shadows on the background."
        ),
        variants=[
            "Variant 1: matched utilitarian set - all four props share the same dusk-blue shell "
            "color and copper trim so they read as one station family.",
        ]),
}

SLOT_ORDER = list(SLOTS.keys())


def candidate_ids(slot_id):
    return [f"{slot_id.split('_')[0]}_C{c:03d}" for c in range(1, SLOTS[slot_id]["count"] + 1)]


def full_prompt(slot_id, ci):
    s = SLOTS[slot_id]
    return SHARED + "  " + s["base"] + "  " + s["variants"][ci]
