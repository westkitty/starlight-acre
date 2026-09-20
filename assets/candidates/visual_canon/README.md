# Starlight Acre — Visual Canon

Art-direction consolidation pass over the complete 136-candidate foundry library
(original 44 + ALT 44 + additional 24 + additional-ALT 24). This directory is the
project's durable visual truth for future generation.

## Files

- `STARLIGHT_ACRE_VISUAL_CANON.md` — the canon: visual thesis, pixel density,
  outline, lighting, palette, material, machinery/drone/terminal/biology/environment/
  UI/VFX grammar, Dexter lock, forbidden drift
- `MASTER_ASSET_INDEX.json` — all 136 candidates with pixel metrics + observations
- `VISUAL_CANON_SELECTIONS.json` — per-slot PRIMARY / SECONDARY /
  REJECT_AS_STYLE_REFERENCE selections with reasons
- `reference_atlas.html` — offline atlas of selected references + GAME SCALE board
- `VISUAL_CONTINUITY_REPORT.md` — cross-family drift audit
- `COHESION_REPAIR_QUEUE.json` — 25 queued repairs (KEEP/NORMALIZE_ONLY/
  TARGETED_IMAGE_EDIT/REGENERATE)
- `FUTURE_ASSET_GENERATION_CONTRACT.md` — binding pre-generation reads + minimum
  reference sets per family
- `tools_canon_analyze.py` — reproducible analyzer (builds index/selections/summary)
- `tools_canon_build_atlas.py` — builds `reference_atlas.html`
- `canon_metrics_summary.json`, `continuity_outliers.json` — intermediate data

## Method (honesty note)

The analysis environment has no image-viewing capability. All observations are
deterministic pixel measurements (palette-anchor usage, outline-ring darkness,
edge density, cluster run length, lighting bias, glow ratio, coverage) computed
from each candidate's `game_ready.png`, combined with recorded prompts, technical
flags and run-verification history. Selections are measurement-grounded
art-direction drafts for human ratification via the review tools. No candidate
file was modified in this pass.

## Reproduce

```
python3 tools_canon_analyze.py      # rebuild index/selections/summary/outliers
python3 tools_canon_build_atlas.py  # rebuild reference_atlas.html
```
