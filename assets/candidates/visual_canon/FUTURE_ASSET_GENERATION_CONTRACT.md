# FUTURE ASSET GENERATION CONTRACT — Starlight Acre

**Binding for every future asset-generation prompt for this project.**
The repository is the memory: art decisions live in files, not in chat history.

## Mandatory pre-generation reads

Every future generation prompt MUST instruct the generator to:

1. **Read** `assets/candidates/visual_canon/STARLIGHT_ACRE_VISUAL_CANON.md` in full.
2. **Read** `assets/candidates/visual_canon/VISUAL_CANON_SELECTIONS.json` for the
   slot's selected references.
3. **Inspect the relevant PRIMARY_REFERENCE image(s)** (paths are in the selections
   file; previews in `reference_atlas.html`) before writing any prompt.
4. Follow the style law, palette law, outline law, lighting law and family grammar
   sections that apply to the asset's family.

Text descriptions alone are not sufficient authority. The reference image is.

## Minimum reference sets by asset family

| new asset | must inspect (PRIMARY references) |
|---|---|
| **NEW DRONE** (any role) | Gardener `A01_C003` + one sibling drone (`A03_ALT_C001` / `A04_C001` / `A05_C001`) — same body language, new under-slung tool |
| **NEW TERMINAL** | Repair/Replenish `T01_ALT_C001` + Research `T02_ALT_C003` (+ glow overlay `T03_C001` if the terminal has an active state) |
| **NEW CROP / mythic plant** | Wisdom Fruit `C01_ALT_C001` + at least one other crop (`C02_ALT_C002`…`C05_ALT_C001`) — planter grammar and lifecycle-strip rules are mandatory |
| **NEW LARGE MACHINERY** | Reactor `A02_ALT_C002` + Hydroponics rig `B04_C001` + Archive stack `B05_C002` |
| **NEW GREENHOUSE / water equipment** | `B04_C001` + crop family planter band |
| **NEW DOCKING / heavy fixture** | Docking collar `B03_C001` + sector door `W01_C003` |
| **NEW UI / icon** | `U01_ALT_C001` + `U02_C002` (strictest palette adherence, 91%) |
| **NEW VFX / glow** | `V01_ALT_C002` + `V02_ALT_C001` (+ `T03_C001` for terminal glows) |
| **NEW ENVIRONMENT PROP** | Cargo sheet `E03_C001` + the target sector's tileset (`E02_C001`; `E01_C002` until re-derived) |
| **NEW BACKGROUND** | `B01_C001` / `B02_C002` (note: both are repair-queued for cropping — compose full-canvas) + density ladder rule |
| **NEW PLAYER / humanoid** | Player `P01_ALT_C002` (the only frame-clean sheet) |
| **ANY DEXTER IMAGERY** | `D01_ALT_C001` — the Dexter Lock (small elderly tricolor Phalène, ears DOWN, unimpressed) is non-negotiable |
| **NEW VENDOR / kiosk** | `D02_ALT_C002` + `D01_ALT_C001` |

## Prompt construction rules

- Base every prompt on the canon's **identity block** (style lock) plus the
  **family grammar** section — not on ad-hoc prose.
- Preserve the **density ladder**: choose the target family's edge-density band
  before writing, and reject results outside it (see Pixel Density anti-shrink rule).
- One subject per sprite; sheets only when the sheet IS the asset; flat magenta
  `#FF00FF` removable background for isolated assets; strict 2D side view (UI strips
  excepted); no readable text anywhere (sole exception: the "E" prompt icon, `U01` #5).
- **Anti-defect hardening is part of the contract**: warm-left/cool-right terminal
  glows, all-cells-populated VFX strips, planter-band alignment on crop strips,
  full-canvas composition for backgrounds. Known failure patterns and their counters
  are documented in the canon and in the repair queue's problem descriptions.
- Record the complete prompt in the run's PROMPTS file **before** generating;
  save the raw result unchanged as `source.png`; normalize deterministically only.

## Post-generation validation (technical only)

Every new asset must pass the standard foundry checks (existence, decode, format,
dimensions, alpha, SHA-256, grid/frames, subject count, topology) and, in addition,
the canon drift checks:

- edge density and cluster run within the family band (Pixel Density law)
- outline-ring darkness within the family band (Outline law)
- light-from-above bias sign correct for family (Lighting law)
- anchor adherence ≥ family target (Palette law)
- glow ratio within family budget (VFX/machinery glow caps)

Status values remain `PASS` / `PASS_WITH_FLAGS` / `FAIL` — technical states only,
never aesthetic rankings. Preserve ugly-but-valid candidates for human review.

## Protection

Candidate libraries are read-only evidence. New runs go in their own
`assets/candidates/<run>/` directory. Never modify live game assets, scenes, or
gameplay as part of a generation run; integration is a separate, explicit step.
