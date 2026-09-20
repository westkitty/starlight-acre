#!/usr/bin/env python3
"""Starlight Acre — ADDITIONAL-ALT (challenger) run specs.

One materially different challenger for every candidate of the completed
additional-asset run (../arena_agent_additional_asset_run). Each challenger
prompt = the SHARED identity block (style lock, imported from the original run)
+ the SOURCE slot contract VERBATIM (all technical/semantic requirements,
dimensions, topology, state meanings preserved) + a CHALLENGER DESIGN paragraph
that solves the same production problem materially differently.

Anti-cheat: challengers change silhouette / mechanical construction / geometry /
arrangement / metaphor — never just palette or seed. Identity locks and cell
order are preserved. Anti-defect hardening lines counter the source run's known
failure evidence (e.g. T03 warm/cool seam mixing, V02 cell occupancy).
"""
import os, sys

_SRC_ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "arena_agent_additional_asset_run"))
_ORIG_ROOT = os.path.abspath(os.path.join(_SRC_ROOT, "..", "arena_agent_asset_run"))
for _p in (_SRC_ROOT, _ORIG_ROOT):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from run_spec import SHARED  # style lock: identical identity block
from additional_spec import SLOTS as SRC_SLOTS, SLOT_ORDER, candidate_ids  # frozen source contracts


def alt_id(cid):
    short, num = cid.split("_")
    return f"{short}_ALT_{num}"


ALT_ADDITIONAL_SPECS = {}


def _reg(sid, ci, design, axes, hardening=""):
    cid = candidate_ids(sid)[ci]
    aid = alt_id(cid)
    base = SRC_SLOTS[sid]["base"]
    prompt = SHARED + "  " + base + "  " + design + (("  " + hardening) if hardening else "")
    ALT_ADDITIONAL_SPECS[aid] = {
        "slot_id": sid, "source_candidate_id": cid,
        "prompt": prompt, "axes": axes,
    }


# ---------------------------------------------------------------- A02 reactor core (vs torus / column / sphere)
_reg("A02_REACTOR_CORE", 0,
     "Challenger design: a horizontal drum-bottle reactor - a wide cylindrical containment vessel "
     "lying on its side, its teal plasma heart visible through a long window slit, riding in two "
     "heavy station-gray cradle saddles, banded with maintenance copper cooling rings, a small "
     "valve stack rising from the top.",
     ["horizontal drum vessel vs upright torus", "cradle-saddle mount vs gimbal pedestal",
      "window-slit plasma reveal vs open ring", "cooling-ring bands vs pedestal feed conduits"])
_reg("A02_REACTOR_CORE", 1,
     "Challenger design: a stacked hex-cell core - a compact honeycomb block of six-sided plasma "
     "cells arranged like a small pyramid, each cell holding a teal glow, clamped in a dusk-blue "
     "corner-bolted frame, feed pipes entering from below through a thick base manifold.",
     ["modular honeycomb block vs monolithic crystal column", "corner-bolted clamp frame vs four-strut cage",
      "pyramidal massing vs vertical column", "under-base manifold vs wide base plate"])
_reg("A02_REACTOR_CORE", 2,
     "Challenger design: a gyroscope core - one small bright teal orb held at the center of two "
     "nested copper gimbal rings that suggest slow rotation, standing on a single thick "
     "station-gray pylon wound with copper coil at its base, two tiny guide lights at the foot.",
     ["nested rotating rings vs static electromagnet arms", "centered orb held by ring depth vs suspended sphere with arc filaments",
      "single coil-wound pylon vs braced arm array"])

# ---------------------------------------------------------------- U02 HUD icons (vs two-tone / badge / line-glyph)
_reg("U02_HUD_EXTENSION_ICONS", 0,
     "Challenger design: beveled relief emblems - each glyph drawn as a chunky beveled tile emblem "
     "with a thin copper keyline and one darker inset shadow step, like embossed station signage; "
     "the six glyphs keep their exact meanings and cell order.",
     ["beveled relief treatment vs flat two-tone", "copper keyline vs single highlight cluster",
      "embossed signage material vs plain solid fill"])
_reg("U02_HUD_EXTENSION_ICONS", 1,
     "Challenger design: framed pictogram tiles - each glyph sits inside a thin station-gray square "
     "frame with notched corners, the glyph itself rendered in two bright colors with a single dark "
     "drop-step beneath it; the six glyphs keep their exact meanings and cell order.",
     ["notched square frames vs rounded badge chips", "two-color glyphs with drop-step vs rimmed chip badges",
      "tile pictogram language vs badge language"])
_reg("U02_HUD_EXTENSION_ICONS", 2,
     "Challenger design: stencil-cut plates - each glyph looks cut from a small dark plate: a "
     "deep-navy plate silhouette with a glowing cut-out interior, one teal or warm gold glow color "
     "per icon; the six glyphs keep their exact meanings and cell order.",
     ["stencil cut-out negative space vs open outline glyphs", "glowing cut-out interior vs one warm accent cluster",
      "plate silhouette mass vs line weight"])

# ---------------------------------------------------------------- T03 terminal glow (vs halo / motes / rings)
_T03_HARD = ("Hardening: keep every warm pixel strictly inside the LEFT half and every teal pixel "
             "strictly inside the RIGHT half; the two glows must never mix or cross the middle seam.")
_reg("T03_TERMINAL_ACTIVE_GLOW", 0,
     "Challenger design: corner-lit wash - each half lit diagonally from its upper corner with "
     "stepped luminous bands fading toward the opposite corner, denser clusters tracing the "
     "pedestal silhouette edge.",
     ["diagonal corner wash vs concentric halo shells", "directional lighting placement vs symmetric shells",
      "silhouette-edge cluster tracing vs top-edge brightness"], _T03_HARD)
_reg("T03_TERMINAL_ACTIVE_GLOW", 1,
     "Challenger design: curtain-fall glow - each half lit from a bright top bar, a soft luminous "
     "curtain of stepped clusters descending the pedestal shape with a few drifting flecks and a "
     "faint pool at the base.",
     ["top-down falling curtain vs bottom-up rising mote columns", "bright top bar anchor vs base pool anchor",
      "descending flecks vs climbing motes"], _T03_HARD)
_reg("T03_TERMINAL_ACTIVE_GLOW", 2,
     "Challenger design: edge-vein glow - thin bright veins tracing the outline of the pedestal "
     "shape with a faint fill halo inside, like backlit panel seams, small corner ticks where the "
     "veins meet.",
     ["outline vein tracing vs nested pulse rings", "backlit seam metaphor vs ring-pulse metaphor",
      "internal fill halo vs spark ticks at corners"], _T03_HARD)

# ---------------------------------------------------------------- A03 engineer drone (vs cable-layer / twin-boom)
_reg("A03_ENGINEER_DRONE", 0,
     "Challenger design: a keel-busbar drone - a flat trapezoid hull with a bright copper busbar "
     "rail slung beneath it, two insulated gripper calipers on side arms, a small amber status "
     "beacon on top, hovering on two wide side thruster pods.",
     ["underslung copper busbar rail vs side cable spool", "side caliper arms vs forward probe arm",
      "twin side thruster pods vs single fan", "flat trapezoid hull vs drum body"])
_reg("A03_ENGINEER_DRONE", 1,
     "Challenger design: a backpack-transformer drone - a compact cube hull carrying a coil-wound "
     "mini transformer on its back, a hinged test-probe snout at the front, two tiny fold-out "
     "landing feet, riding one annular thruster ring.",
     ["cube hull with transformer backpack vs twin-boom frame", "hinged probe snout vs extendable visor arm",
      "single annular ring thruster vs three caged thrusters"])

# ---------------------------------------------------------------- A04 harvester drone (vs basket / scoop-tram)
_reg("A04_HARVESTER_DRONE", 0,
     "Challenger design: a net-bag reaper - a slim vertical mast body under a top lift-rotor "
     "shroud, a gentle three-finger gripper on one side, and a deep mesh produce net hanging "
     "below the hull with two tiny gold fruits visible inside.",
     ["hanging mesh produce net vs slung woven basket", "mast body with top rotor vs rounded hull with ducted fan",
      "three-finger side gripper vs folded pincer claw"])
_reg("A04_HARVESTER_DRONE", 1,
     "Challenger design: a drum-reel picker - a rounded wagon-like body with a rotating picker "
     "reel at the front, a cushioned conveyor channel along its top carrying one gold fruit, and "
     "a wide rear stabilizer fin.",
     ["front picker reel vs front scoop tray", "top conveyor channel vs tray-held fruit",
      "wide rear fin vs twin rear thrusters"])

# ---------------------------------------------------------------- A05 maintenance drone (vs brush puck / sealant boom)
_reg("A05_MAINTENANCE_DRONE", 0,
     "Challenger design: a mag-rail crawler - a low wedge body with dark magnetic runner skids, a "
     "wide soft buffing belt on its belly, and a small tilting inspector head with a bone-white "
     "lamp.",
     ["magnetic runner skids with belly buffing belt vs rotating brush pads underneath",
      "tilting inspector head vs polish-wheel arm", "low wedge silhouette vs rounded puck"])
_reg("A05_MAINTENANCE_DRONE", 1,
     "Challenger design: a patch-welder drone - a turtle-shell hull carrying a small stack of "
     "repair patches on top, one stub welder arm with a warm tip glow, and a copper scraper blade "
     "at the rear.",
     ["patch stack with welder arm vs hopper with spray boom", "warm welder tip as the glow focus vs inspection lamp focus",
      "turtle-shell silhouette vs compact box"])

# ---------------------------------------------------------------- B03 docking collar (vs circular / freight airlock)
_reg("B03_DOCKING_COLLAR", 0,
     "Challenger design: an octagonal berth ring - an eight-sided collar with heavy copper tension "
     "arms folded at the corners, a soft worn inner seal lip, and small teal guide lights set in "
     "pairs along the top edges, mounted on a riveted station-gray frame.",
     ["octagonal geometry vs circular collar", "corner tension arms vs clamp petals",
      "paired lights along top edges vs full guide-light ring"])
_reg("B03_DOCKING_COLLAR", 1,
     "Challenger design: a vertical slot berth - a tall narrow docking slot with twin vertical "
     "clamp rails, a top-mounted capture hook, roller curtains at the mouth, and one calm teal "
     "light strip down each side.",
     ["vertical slot mouth vs rectangular cargo mouth", "capture hook with rail clamps vs side ram clamps",
      "vertical side light strips vs chevron lights above"])

# ---------------------------------------------------------------- B04 hydroponics rig (vs twin tanks / tube rack)
_reg("B04_HYDROPONICS_RIG", 0,
     "Challenger design: a drum-filter station - one wide rotating filter drum sitting in a teal "
     "water bath, a copper hand-crank and backwash pipe on the side, a slim sight tube with one "
     "moss-green root strand, and a small drip spout at the front.",
     ["single end-on filter drum vs twin round tanks", "hand-crank with backwash pipe vs copper manifold with drip arm",
      "root-strand sight tube vs sight-gauge windows"])
_reg("B04_HYDROPONICS_RIG", 1,
     "Challenger design: a zigzag still - copper pipes descending in a zigzag ladder from a header "
     "tank into a lower calm chamber with a soft teal glow, one tiny plant rail with a moss-green "
     "sprout at the midpoint.",
     ["zigzag pipe ladder vs vertical tube rack", "header tank feeding a lower chamber vs topfill reservoir over pump heart",
      "midpoint sprout rail vs row of gauge dials"])

# ---------------------------------------------------------------- B05 archive stack (vs shelf rows / data-drum)
_reg("B05_ARCHIVE_STACK", 0,
     "Challenger design: a drawer-totem stack - four offset copper-handled drawers set in a tall "
     "dusk-blue monolith, one drawer pulled open showing a glowing crystal cluster inside, a thin "
     "reader wand docked on the side.",
     ["offset drawers vs uniform shelf rows", "pulled-drawer reveal vs glass front",
      "docked reader wand vs reader probe arm"])
_reg("B05_ARCHIVE_STACK", 1,
     "Challenger design: a hanging vial rack - a tall slender frame with three horizontal rails of "
     "suspended glowing vials, each cradled in a small copper claw, the topmost vial brightest, a "
     "ladder-step retrieval probe at the base.",
     ["hanging vial rails vs spiral drum slots", "copper claw cradles vs rounded drum cabinet",
      "ladder-step probe at base vs retrieval claw at top"])

# ---------------------------------------------------------------- V02 hazard VFX (vs dense / sparse)
_V02_HARD = ("Hardening: every one of the four cells must end with clearly visible effect pixels "
             "after the flat background is removed; keep all effect colors far from pure magenta "
             "and make each cell's content unmistakably non-empty.")
_reg("V02_HAZARD_VFX", 0,
     "Challenger design: radial-burst interpretation - each effect rebuilt as one compact centered "
     "radial burst: the flare as a radiating golden sun-shard star, the anomaly as a violet "
     "eye-ring with orbiting motes, the malfunction as a four-way spark cross from a central "
     "failing node, the power failure as a dimming ring of dying dots around a fading light bar.",
     ["centered radial bursts vs corner washes and falling showers", "sun-shard / eye-ring / spark-cross metaphors",
      "compact symmetric composition per cell"], _V02_HARD)
_reg("V02_HAZARD_VFX", 1,
     "Challenger design: sweeping-arc interpretation - each effect rebuilt as sweeping curved "
     "strokes: the flare as a curved golden fan, the anomaly as a spiral shimmer curl, the "
     "malfunction as falling arcing bolt trails, the power failure as a waning crescent strip "
     "with guttering dots.",
     ["sweeping curved strokes vs straight diagonal shards", "fan / spiral / crescent metaphors",
      "curved motion language across all four cells"], _V02_HARD)

# ---------------------------------------------------------------- E03 cargo props (vs dusk-blue family)
_reg("E03_CARGO_PROPS", 0,
     "Challenger design: riveted gray family - all four props rebuilt as one station-gray riveted "
     "family with copper straps and small teal working lights: the crate as a ribbed shipping box "
     "with strap buckles, the canister as a twin-cap capsule tank, the tool case as a chest with a "
     "fold-out tray lip, the seed rack as a tiered shelf with two moss-green sprouts.",
     ["station-gray riveted shells vs dusk-blue matched shells", "ribbed crate / capsule tank / fold-out chest / tiered rack redesigns",
      "teal working-light accents vs copper-trim-only accents"])

assert len(ALT_ADDITIONAL_SPECS) == sum(SRC_SLOTS[s]["count"] for s in SLOT_ORDER), "challenger universe must be one-to-one"
