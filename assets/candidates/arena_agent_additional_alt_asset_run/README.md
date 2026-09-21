# Starlight Acre — ADDITIONAL-ALT (challenger) asset run

`assets/candidates/arena_agent_additional_alt_asset_run/`

One **materially different challenger** for every candidate of the completed
additional discovered-asset run (`../arena_agent_additional_asset_run`, 24/24).
Mapping is one-to-one and permanent: `A02_C001 → A02_ALT_C001`, …, `E03_C001 → E03_ALT_C001`.

## What is preserved (hard invariants)

* gameplay role, asset category, integration target
* pixel/sheet dimensions, frame count, frame order, topology, anchors
* state meanings, cell order and semantic meaning (UI icons, VFX cells, prop sheets)
* Starlight Acre visual language and palette anchors

## What changes (challenger axes)

Silhouette, mechanical construction, geometry, proportions, subcomponent
arrangement, material breakup, negative space, lighting placement, visual
metaphor — recorded per challenger in `candidate.json → challenger_axes` and in
`ALT_ADDITIONAL_PROMPTS.md`. Not mere palette/seed variations.

## Files

* `alt_additional_spec.py` — challenger contracts: source slot contract verbatim
  (imported from `../arena_agent_additional_asset_run/additional_spec.py`) + a
  challenger design paragraph + anti-defect hardening
* `tools_alt_additional_build.py` — deterministic pipeline (idempotent); reuses the
  original run's `make_game_ready` / `analyze_sheet_topology` via in-memory slot
  registration; never modifies any source library
* `ALT_ADDITIONAL_GENERATION_MANIFEST.json` — 24 one-to-one mappings with hashes/flags
* `ALT_ADDITIONAL_ASSET_REQUIREMENTS.json` — immutable technical contracts (copied
  from the source run)
* `ALT_ADDITIONAL_PROMPTS.md` — complete challenger prompt per pair, recorded before
  generation
* `review.html` — offline pair review: LEFT source/champion, RIGHT altered/challenger;
  slot/category/priority filters, source/game_ready toggle, NN zoom, 1:1, checker,
  metadata + flags + both prompts + challenger axes; decisions
  ORIGINAL/ALTERED/BOTH/NEITHER/UNDECIDED (keys O/A/B/N/U) persisted in localStorage
  (`sa_additional_alt_review_v1`); EXPORT writes `additional_alt_selections.json`.
  The tool never decides winners.

## Rules

* sources saved unchanged as `source.png`; `game_ready.png` is deterministic
  normalization only (no generative repair)
* PASS / PASS_WITH_FLAGS / FAIL are technical states only
* all three source libraries and live game files are strictly read-only
