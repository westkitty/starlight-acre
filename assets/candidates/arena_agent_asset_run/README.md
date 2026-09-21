# Starlight Acre — Arena Agent Asset Candidate Run

**Run ID:** `arena_agent_asset_run` · **Date:** 2026-09-20 · **Baseline commit:** `97544d7`

## What this batch is

A **candidate visual-asset library** for Starlight Acre produced by an autonomous agent run.
Multiple candidates per asset slot are **intentional** — near-duplicates and alternative
interpretations are wanted, so a human can choose later. The purpose of this batch is:

    GENERATE -> NORMALIZE -> VALIDATE -> ORGANIZE -> REVIEW LATER

It is explicitly **not** a decision pass: nothing here was aesthetically ranked by the agent.

## NOT canonical — nothing is live

**No generated candidate in this directory is canonical production art.** No live game file
was touched. The protected live assets

- `assets/sprites/player/player_sheet.png`
- `assets/sprites/crops/wisdom_fruit_states.png`
- `assets/sprites/terminals/terminals.png`
- `assets/tilesets/greenhouse_tiles.png`
- `assets/ui/icons/hud_icons.png`
- `assets/backgrounds/greenhouse_sector_bg.png`

and all gameplay scenes, ColorRect/Polygon2D placeholders, scripts, and balance are
**unchanged**. See `git diff main` to verify: this run only adds files under
`assets/candidates/arena_agent_asset_run/`.

## Slots and candidate counts

| Priority | Slots | Target candidates each |
|---|---|---|
| A | A01_GARDENER_DRONE, T02_RESEARCH_TERMINAL, W01_SECTOR_DOOR, B02_ENGINEERING_BACKGROUND, E02_ENGINEERING_TILESET, C02_TRICKSTER_VINE, D01_DEXTER_VENDOR, D02_DEXTER_VENDOR_KIOSK | 3 |
| B | P01_PLAYER_SHEET, C01_WISDOM_FRUIT, T01_REPAIR_REPLENISH_TERMINALS, U01_HUD_ICONS, E01_GREENHOUSE_TILESET, B01_GREENHOUSE_BACKGROUND, V01_CORE_VFX | 2 |
| C | C03_LIGHTNING_VINE, C04_SHADOW_ROOT, C05_GOLDEN_BLOSSOM | 2 |

Target total: **44 candidates**. Current actual counts (including not-yet-generated slots)
are recorded honestly in `GENERATION_MANIFEST.json` — that file is the single source of
truth for what exists. If `generated_count` is below 44, the remainder are recorded with
`generation_status: "not_generated"` and were not fabricated.

## `source.png` vs `game_ready.png`

- **`source.png`** — the untouched generator output, preserved exactly as produced
  (hash-recorded). Generated sources are typically far larger than game dimensions.
- **`game_ready.png`** — a **deterministic, scripted** normalization
  (`tools_build.py`, re-runnable): flat-background flood key where safe, aspect-preserving
  **nearest-neighbor** resize, bottom-center anchoring for sprites, exact target canvas
  size. No AI steps, no smoothing, no invented or rearranged frames.

Generated sheets that may not truly contain the required frame topology are flagged
`FRAME_LAYOUT_UNCERTAIN` / `FRAME_LAYOUT_INVALID` rather than silently declared usable.
`TECHNICAL_FAIL_FRAME_LAYOUT` in candidate notes means the same: do not trust slicing
without review.

## Technical status meanings

- **PASS** — game_ready exists at the exact expected dimensions with no functional flags.
- **PASS_WITH_FLAGS** — usable candidate, but review the `technical_flags` in its
  `candidate.json` (e.g. `CONVERSION_REQUIRED`, `FRAME_LAYOUT_UNCERTAIN`,
  `OPAQUE_BACKGROUND`, `CROPPED_CONTENT`, `UNREADABLE_AT_TARGET_SCALE`).
- **FAIL** — generation or normalization failed; kept for the record only.

The agent does **not** rank candidates artistically; status is purely technical.

## How to review (`review.html`)

Open `review.html` in any modern browser. Fully offline, single file, no server.
Candidates are loaded from relative paths; state persists in `localStorage`.

- Slot navigation bar (top) + status filters: `ALL / UNSORTED / KEEP / MAYBE / REJECT / PASS / PASS_WITH_FLAGS / FAIL`
- Large nearest-neighbor preview with **checkerboard toggle** for alpha inspection
- **Raw source vs game_ready toggle**, **zoom −/+**, and **1:1 true-pixel toggle**
- **A/B compare**: press `A` then `B` on any two candidates of the same slot (or use the
  `set A` / `set B` buttons / dropdowns) and toggle `A/B` — side-by-side, images stay
  separate files; no combined comparison PNG is ever created
- Per-candidate: expected vs actual dimensions, technical status, flags, collapsible full prompt

### Keyboard shortcuts

| Key | Action |
|---|---|
| `←` / `→` | previous / next candidate |
| `K` | KEEP |
| `M` | MAYBE |
| `R` | REJECT |
| `U` | UNSORTED (clear verdict) |
| `A` / `B` | mark current candidate as comparison A / B |
| `P` | toggle prompt panel |

## `selections.json`

`EXPORT SELECTIONS` (top right) downloads `selections.json` containing your verdict for
every candidate (`keep / maybe / reject / unsorted`). It is a review artifact only —
the game never reads it.

## How a future developer promotes a candidate safely

1. Review in `review.html`, export `selections.json`.
2. Pick the winning `candidate_id` per slot from `candidate.json` files (all metadata,
   hashes, and flags live there and in `GENERATION_MANIFEST.json`).
3. **Do not** copy `game_ready.png` blindly. For multi-frame slots (player, crops, VFX,
   HUD, terminals) verify the frame topology against the integration contract in
   `ASSET_REQUIREMENTS.json` (recorded from the current `.tscn` scenes, which override
   older prose docs — legacy live PNGs are 640×640 sources, while scenes slice game-sized
   regions: player 32×48 rows, crops hframes=4, HUD 16×16, terminals 32×64, tiles 16×16).
4. Re-slice from `source.png` if `game_ready` is flagged, then copy into the live asset
   path in a **separate, reviewable commit** (e.g. `assets: promote A01_C002 gardener drone`),
   and only after visual QA in Godot with Nearest filtering.

## Reprocessing / regenerating

- `python3 run_spec.py` — re-emit `ASSET_REQUIREMENTS.json` and slot directories.
- `python3 tools_build.py` — re-normalize, re-validate, rebuild `candidate.json` files,
  `GENERATION_MANIFEST.json`, and `review.html`. Sources are never modified.
- `PROMPTS.md` — complete verbatim prompts for every slot and candidate, for regeneration.

## Files

```
ASSET_REQUIREMENTS.json   technical contract per slot (from current implementation)
GENERATION_MANIFEST.json  every expected candidate incl. failures, hashes, flags
PROMPTS.md                complete generation prompts
review.html               offline review tool
run_spec.py / tools_build.py  deterministic pipeline (kept for reproducibility)
slots/<SLOT>/<CANDIDATE>/ source.png, game_ready.png (when valid), candidate.json
```
