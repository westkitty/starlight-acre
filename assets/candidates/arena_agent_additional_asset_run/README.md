# Starlight Acre — ADDITIONAL asset run (discovered slots)

Third candidate library: **new asset slots discovered from the actual repository** —
placeholders in code, documented-but-missing assets, documented near-term modules/agents/
hazards, and modular environment polish. No overlap with the 18 established families of
the two prior runs.

## Discovery (frozen)

`DISCOVERED_ASSETS.json` records every discovered slot with evidence, evidence paths,
gameplay role, priority, integration target, dimensions (marking NEWLY PROPOSED ones),
topology, and placeholder/overlap status. Sources inspected: OPERATIONAL_STATE.md,
README.md, Starlight_Acre_bible.md, docs/GAME_DESIGN.md, assets/docs/*, all scenes,
all scripts, and both prior candidate-library manifests.

Discovered slots (11): A02 Reactor Core (A), U02 HUD Extension Icons (A),
T03 Terminal Active Glow (A), A03 Engineer Drone (B), A04 Harvester Drone (B),
A05 Maintenance Drone (B), B03 Docking Collar (B), B04 Hydroponics Rig (B),
B05 Archive Stack (B), V02 Hazard VFX (B), E03 Cargo Props (C).

## Candidate policy

Priority A → 3 candidates, B → 2, C → 1. Total target: **24 candidates**.

## Structure

- `DISCOVERED_ASSETS.json` — frozen discovery record with evidence
- `ADDITIONAL_ASSET_REQUIREMENTS.json` — technical contracts per discovered slot
- `ADDITIONAL_GENERATION_MANIFEST.json` — all candidates, statuses, hashes, flags
- `ADDITIONAL_PROMPTS.md` — verbatim prompts
- `additional_spec.py` — slot specs (contracts + variant designs)
- `tools_additional_build.py` — deterministic pipeline; reuses the original run's
  normalization/validation (in-memory slot registration; original files untouched)
- `review.html` — slot navigation, category/priority/status/decision filters, source vs
  game_ready toggle, NN zoom + 1:1, checkerboard, evidence + integration target,
  KEEP/MAYBE/REJECT/UNSORTED (K/M/R/U) in localStorage, EXPORT SELECTIONS →
  `additional_selections.json`. Never selects winners automatically.

## Rules

- this is still a candidate run: nothing is integrated, no live asset replaced,
  no scene modified, no gameplay changed
- both prior candidate libraries are read-only
- sources preserved unchanged; `game_ready.png` is a deterministic derivative
- honest flags only; technical status is never an aesthetic judgment
