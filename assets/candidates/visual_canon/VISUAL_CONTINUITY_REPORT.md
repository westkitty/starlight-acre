# VISUAL CONTINUITY REPORT — Starlight Acre canon audit

Cross-family audit of the selected PRIMARY/SECONDARY references (and the full
136-candidate pool behind them). Method: deterministic pixel metrics
(`MASTER_ASSET_INDEX.json`) + recorded technical flags + run-verification history.
No image viewing was available; classifications below cite their measured evidence.
**Nothing was repaired in this pass.**

Verdict scale: `PASS` · `MINOR` (keep, documented) · `REPAIR_RECOMMENDED`
(`COHESION_REPAIR_QUEUE.json` entry) · `REGENERATE_RECOMMENDED`.

## Summary

| drift category | verdict | evidence |
|---|---|---|
| PIXEL SCALE | REPAIR_RECOMMENDED (4) | P01 framed trio + V01_C001 retain bright frames/background (sat 0.90–0.92, glow 76–82%, anchors 12–17% vs clean player 0.49/10%/77%) |
| OUTLINE | REPAIR_RECOMMENDED (4, E01 slot) | E01 keying destroyed legitimate dark pixels: ring 0.49–0.56 vs tileset median 0.887; flagged TILESET_OVERKEYED in all four candidates |
| PALETTE | PASS (one MINOR) | copper discipline 3–7% on all hardware; gold confined to crops/VFX; U02_C001 adherence 0.688 vs HUD 0.912 (MINOR, already non-reference) |
| LIGHTING | PASS (MINOR notes) | top-light bias holds (+0.02 global, +0.07…+0.13 foreground families); deliberate uplight accents A01_ALT_C001/A04_C002 (−0.06…−0.09) and W01_C002 (−0.018) documented as permitted rare variation |
| MATERIAL | PASS | no measured copper/gold misuse in reference set |
| PERSPECTIVE | PASS (contract-enforced) | strict side-view in every contract; not machine-measurable — no aspect/topology violations detected; held by prompt law and review |
| PROPORTION | MINOR + REPAIR_RECOMMENDED (10, B01/B02) | Dexter 64×64 canvas vs player 32×48 frame (display-scale at integration); all B01/B02 backgrounds CROPPED_CONTENT |
| GLOW | PASS (MINOR notes) | references within family glow budgets; A01_ALT_C003 20% drone glow, T02_ALT_C002 19%, B05_C001 10.5% documented as non-reference variants |
| DETAIL DENSITY | PASS (MINOR notes) | density ladder intact (bg 0.112 → props 0.614); D02_C002 and T01_ALT_C002 dense variants documented |
| SILHOUETTE FAMILY | REPAIR_RECOMMENDED (5) | D01_C002 duplicate subject (curated evidence); A04_ALT_C001 possible duplicate; C01_ALT_C002 planter band; T03_C003 mixed glow halves; V01/V02 empty-cell defects |

**Totals: 25 repair-level issues queued · 13 minor keep-with-notes observations ·
all other 98 candidates PASS with no action.**

## Repair-level issues (→ COHESION_REPAIR_QUEUE.json)

| # | candidate | problem (measured/recorded) | governing reference | action |
|---|---|---|---|---|
| 1 | P01_C001 | retained bright frame: sat 0.900, glow 76.4%, anchors 17% | P01_ALT_C002 | NORMALIZE_ONLY (re-key from source, expanded seeds) |
| 2 | P01_C002 | retained bright frame: sat 0.917, glow 82.2%, anchors 12% | P01_ALT_C002 | NORMALIZE_ONLY |
| 3 | P01_ALT_C001 | retained bright frame: sat 0.907, glow 77.2%, anchors 17% | P01_ALT_C002 | NORMALIZE_ONLY |
| 4 | V01_C001 | cell background not removed (3.6% keyed; sat 0.171 vs family 0.663) | V01_ALT_C002 | NORMALIZE_ONLY |
| 5 | V02_C001 | CELL_BACKGROUND_NOT_REMOVED residue | V02_ALT_C001 | NORMALIZE_ONLY |
| 6–9 | E01_C001, E01_C002, E01_ALT_C001, E01_ALT_C002 | TILESET_OVERKEYED: dark tile pixels destroyed (ring 0.49–0.56 vs 0.887) | E02_C001 (engineering tileset) | NORMALIZE_ONLY (re-derive game_ready from preserved sources by direct slicing, no keying) |
| 10 | B01_C001 | CROPPED_CONTENT (least-bad primary, still cropped) | E02/E01 grammar | TARGETED_IMAGE_EDIT (recompose to full 640×360) |
| 11 | B02_C002 | CROPPED_CONTENT (least-bad primary, still cropped) | B01_C001 | TARGETED_IMAGE_EDIT |
| 12–14 | B01_C002, B01_ALT_C001, B01_ALT_C002 | CROPPED_CONTENT + family outliers | B01_C001 | REGENERATE |
| 15–19 | B02_C001, B02_C003, B02_ALT_C001, B02_ALT_C002, B02_ALT_C003 | CROPPED_CONTENT (worst z-profiles) | B02_C002 | REGENERATE |
| 20 | D01_C002 | duplicate subject: two dogs (recorded original-run evidence) | D01_ALT_C001 | TARGETED_IMAGE_EDIT (remove second dog) |
| 21 | A04_ALT_C001 | MULTIPLE_SUBJECTS_POSSIBLE + uplight −0.111 | A04_C001 | TARGETED_IMAGE_EDIT (verify/remove duplicate) |
| 22 | C01_ALT_C002 | PLANTER_BAND_INCONSISTENT | C01_ALT_C001 | TARGETED_IMAGE_EDIT (align planter band) |
| 23 | T03_C003 | left glow half mixes warm/cool (51/39 measured in-run) | T03_C001 | TARGETED_IMAGE_EDIT (recolor left half warm) |
| 24 | V01_C002 | EXPECTED_CELL_EMPTY (content missing) | V01_ALT_C002 | REGENERATE |
| 25 | V02_C002 | EXPECTED_CELL_EMPTY (content missing) | V02_ALT_C001 | REGENERATE |

## Minor observations (KEEP, documented — no queue entry)

- A02_ALT_C001 / A02_ALT_C003 — soft-outline reactor variants (ring 0.548/0.412 vs 0.784); glow-led design, acceptable as challengers, not references.
- T02_C001 — lighter keyline (0.592 vs 0.744).
- A05_C002 / A04_C002 — heavier keylines (0.870/0.838); A04_C002 also bottom-lit (−0.087) as a deliberate accent.
- A01_ALT_C001 — bottom-lit accent (−0.062).
- A01_ALT_C003 — glow-heavy drone (20% vs 2.3% family) — rejected as style reference.
- T02_ALT_C002 — bright top-heavy terminal (glow 18.8%, above +0.255) — rejected as reference.
- B05_C001 — glow 10.5% vs archive 1.7% — secondary exists (B05_ALT_C002), keep as variation.
- A05_ALT_C002 — glow 10.6% — minor.
- W01_C002 — light bias −0.018 (z 6.66) — flat-lit door variant.
- D02_C002 — cluster run 1.07 (z 5.0) — dense kiosk variant.
- T01_ALT_C002 — edge density 0.563 vs 0.333 — dense terminal variant.
- U02_C001 — anchor adherence 0.688 vs HUD 0.912 — off-anchor icon strip.
- Dexter scale (proportion MINOR): D01 references occupy 64×64 canvases vs player frame 32×48 — at integration, display-scale Dexter so the dog reads clearly smaller than the player. Asset itself: KEEP.

## Cohesion strengths worth protecting

- Density ladder is clean and monotonic by depth (backgrounds 0.112 → props 0.614).
- Copper/gold discipline holds across every hardware family (measured 3–7% / ~0–1%).
- Drone family conformity is tight (18 candidates, glow 2.3%, one body language).
- Terminal glow halves: references verified 100% warm-left / cool-right separation.
- V02_ALT references: all four hazard cells populated (12–78%) — the empty-cell defect was eliminated by the challenger run.
