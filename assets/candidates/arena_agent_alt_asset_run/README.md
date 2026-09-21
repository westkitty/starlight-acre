# Starlight Acre — ALTERNATE (challenger) asset run

Second, parallel candidate library: **exactly one materially different alternate for each
of the 44 candidates** in the original run (`../arena_agent_asset_run/`).

Mapping is one-to-one and deterministic: `<SLOT>_C00N` → `<SLOT>_ALT_C00N`
(e.g. `A01_C001` → `A01_ALT_C001`). Every alternate record carries
`source_candidate_id` + `alternate_candidate_id` so the pairing can never be lost.

## Champion-vs-challenger principle

Each original candidate is the incumbent champion. The alternate solves the **same**
gameplay/art problem under the **same** technical contract (dimensions, perspective,
frame count/order, topology, anchors, palette relationships, Starlight Acre identity)
while exploring a materially different design (silhouette, structure, geometry,
mechanism, morphology, composition). Not a recolor, not a reseed.

Challenger design axes are recorded in each `candidate.json` under `challenger_axes`
and composed in `alt_spec.py` (prompts preserved verbatim in `ALT_PROMPTS.md`).

## Structure

- `ALT_ASSET_REQUIREMENTS.json` — integration contracts (identical to the original run)
- `ALT_GENERATION_MANIFEST.json` — all 44 one-to-one mappings, statuses, hashes, flags
- `ALT_PROMPTS.md` — challenger prompts + axes per alternate
- `alt_spec.py` — challenger specs (slot contracts + challenger designs)
- `tools_alt_build.py` — deterministic pipeline; reuses the original run's
  normalization/validation functions so both libraries are processed identically
- `review.html` — champion-vs-challenger review tool (see below)
- `slots/<SLOT>/<ALT_ID>/{source.png, game_ready.png, candidate.json}`

## Review tool

Open `review.html` locally. Left panel = ORIGINAL/CHAMPION, right panel =
ALTERNATE/CHALLENGER. Source/game_ready toggle, nearest-neighbor zoom + 1:1,
checkerboard, metadata, flags, prompts, challenger axes.

Decide per pair: ORIGINAL (O) / ALT (A) / BOTH (B) / NEITHER (N) / UNDECIDED (U);
navigate with ←/→. Decisions persist in localStorage and are **never automatic** —
this tool never declares winners. EXPORT DECISIONS writes `alt_selections.json`.

## Rules

- the original library and all live game assets are never modified
- sources are preserved unchanged; `game_ready.png` is a deterministic derivative
- flags are honest (technical status is never an aesthetic judgment)
- promotion of any winner remains a human decision
