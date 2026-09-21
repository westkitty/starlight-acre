# Starlight Acre Operational State

Project ID: starlight-acre
Revision: 12
Updated: 2026-09-21

## Purpose
A small, finishable 2D orbital mythic farming-station game in which the player restores a failing station by cultivating mythic crops, managing station systems, automating repetitive work, and expanding into additional sectors.

## Current baseline
- Repository: westkitty/starlight-acre
- Source baseline before this upgrade: main at 97eb3f8
- Active implementation worktree: /Users/andrew/starlight-acre-visual-qa (arena/01a0bd0b-starlight-acre)
- Engine verified on development Mac: Godot 4.7.1 stable
- Project feature target: Godot 4.7
- Phase 2 asset-integration work from defaecd had been reverted by 97eb3f8 and has now been selectively restored into the working tree.
- Repository PNG paths now contain actual PNG-encoded bytes.

## Protected capabilities
- Player movement with coyote time and jump buffering.
- Plant -> grow -> tend -> harvest loop.
- Power loss pauses crop growth.
- Events autoload remains a signal/event surface rather than gameplay state.
- Interactable contract remains get_prompt() + interact().
- Gardener automation acts through public crop behavior and must travel to a crop before acting.
- Pixel-art nearest-neighbor filtering remains enabled.
- Natural-language agent creation remains out of scope.
- Greenhouse floor/wall collision is authoritative on the canonical TileMapLayers; obsolete StaticBody2D room stubs must not return.
- The live pixel-art viewport is 640×360 with nearest-neighbor filtering; the player Camera2D follows horizontally within sector limits and keeps the full 32px Greenhouse floor slab visible.

## Verified working
- Godot 4.7.1 can initialize the modified project headlessly without script/resource parse errors.
- `tests/smoke_test.gd` passes and loads GreenhouseSector, EngineeringBay, CropPlot, ResearchTerminal, and Wisdom Fruit Resource.
- The real main scene runs headlessly for 120 frames without script/runtime errors.
- Previously invalid JPEG-encoded .png files were normalized and import successfully.
- Recovered July terminal/HUD/VFX files parse under the current runtime.
- GameState autoload is accepted by the project.
- Multi-sector scenes and resource definitions load successfully.
- Automated Greenhouse -> Engineering -> Greenhouse round-trip passes with correct horizontal spawn routing and normal gravity settling.
- JSON persistence survives a real two-process quit/relaunch test for resources, upgrades, plot state/timer/crop ID, emergency resupplies, power, and current sector.
- Startup routing resumes the saved Engineering sector on relaunch and safely falls back to Greenhouse for an invalid saved sector.
- Research progression is regression-verified at exactly 4 Wisdom Fruit for Efficient Grid and 6 for Closed-Loop Hydroponics, including their 0.6 power-drain multiplier and 15-unit resource caps.
- Gardener Drone functional travel + ordinary READY-crop harvest is regression-verified through public crop behavior; Trickster Vine explicitly refuses drone auto-harvest.
- Trickster Vine is implemented as the second mythic crop: 24s growth, 15% tend bonus, one deterministic 72px flee on first harvest attempt, separate catchable fruit entity, 1 Chaos on catch, and persisted flee/catch state across sector reloads and quit/relaunch.
- First Mythic Ecology proof is implemented: once per Trickster growth cycle, a nearby GROWING Trickster Vine can steal one tending pulse from neighboring GROWING Wisdom Fruit within 224px. The Wisdom crop loses that one tend and the Trickster receives the same absolute growth reduction. The spent-steal state persists across sector reloads.
- Chaos now has a progression sink: Paradox Trellis costs 3 Chaos at the Research Terminal. Once unlocked, a stolen Wisdom tending pulse is mirrored so both Wisdom and Trickster receive the reduction while Trickster remains limited to one theft per growth cycle.
- `tests/run_core_systems.sh` verifies persistence, sector routing, all three research purchases, Trickster flee/catch behavior, Wisdom↔Trickster ecology before/after Paradox Trellis, Gardener behavior, Greenhouse TileMap collision/cell counts, the 640×360 camera contract, and the configured main scene for 120 frames; it rejects Godot SCRIPT ERROR/ERROR output even when a test token is printed.
- Greenhouse TileMap migration is regression-verified: 150 floor cells and 136 wall cells use the canonical E01 atlas, TileSet physics blocks the player at the floor and both side walls, and the old Floor/WallLeft/WallRight StaticBody2D stubs have been removed.
- Camera/viewport behavior is regression-verified: 640×360 internal viewport, 1280×720 default desktop window, horizontal camera centers clamp at -280/0/280 across the room, vertical center is fixed at 116 so the entire 32px floor slab remains visible, and the sector background tracks the active camera center.
- First recurring station hazard is implemented and regression-verified: Solar Flare cycles 30s initial calm → 5s warning → 8s active → 45s recovery. Active flare multiplies normal power drain by 5×; Efficient Grid's existing 0.6 multiplier still mitigates it.
- Solar Flare state is intentionally transient across quit/relaunch but survives live Greenhouse ↔ Engineering transitions. The exact-zero phase-boundary transition case is regression-verified to advance rather than reset.
- Solar Flare HUD feedback uses canonical V02 cell 1. A real 640×360 active-flare render passed; all 297 nontransparent source pixels produced exactly 297 changed pixels inside the intended 32×32 HUD rectangle with no spill.

## Implemented but not fully verified
- Manual player journey across Greenhouse -> Engineering -> Greenhouse (automated round-trip verified; interactive feel still pending).
- Research purchase UX feel (costs and effects are verified).
- Spatial Gardener Drone feel/pathing at normal gameplay speed (functional travel + harvest are verified).
- Trickster Fruit flee animation/composition has a successful real render capture, but human aesthetic judgment of the jump/landing/readability is still pending.
- Full human aesthetic review of promoted sprite animation/composition; Greenhouse floor/wall composition has an assistant visual sanity pass from a real 640×360 Godot capture.

## Known limitations
- Greenhouse TileMap painting/collision migration is complete. Engineering Bay still uses its earlier StaticBody2D floor/wall collision and Polygon2D floor visual.
- ~~Generated art source files are 640x640 despite historical documentation claiming sprite-sheet dimensions~~ Resolved by canon promotion: live files are now exactly the documented sheet dimensions (192x192 player, 128x32 crop states, 64x64 terminals, 80x16 HUD, 256x256 tileset, 128x32 VFX, 640x360 backgrounds).
- Visual QA of the promoted art remains PENDING USER REVIEW overall: dimensions, hashes, region bounds, scene loads, Greenhouse camera framing, and Greenhouse floor/wall render sanity are verified; the user has not yet signed off on the complete sprite/scene aesthetic pass.
- Remaining mythic crops (C03-C05), engineering fixtures, future drones, Dexter (D01_ALT_C001 exact, locked), and HUD extensions remain PROMOTED_FUTURE_USE art only. C02 Trickster Vine and V02 Solar Flare VFX have graduated into live gameplay; V02 cells 2-4 remain unused.
- Audio remains absent.
- Delivery identity is the active branch `arena/01a0bd0b-starlight-acre` and PR #2; use Git history for exact per-revision commit hashes rather than embedding a self-referential current SHA here.

## Visual asset canon
- All four candidate foundry runs are complete: original 44/44, original ALT 44/44, additional 24/24, additional ALT 24/24.
- Visual-canon consolidation covers 136 candidates across 29 slots.
- On 2026-09-20, the user explicitly approved all 29 draft PRIMARY recommendations as the human-ratified canon.
- Authoritative decision file: `assets/candidates/visual_canon/RATIFICATION_DECISIONS.json`.
- Ratified canon compiled 2026-09-20: 29/29 slots ratified, zero DEFER, zero NEEDS_NEW_REFERENCE (`RATIFIED_VISUAL_CANON.json`).
- Draft repair queue pruned from 25 entries to 3 canonical repairs (`RATIFIED_REPAIR_QUEUE.json`); the other 22 are preserved as rejected candidates with files untouched.
- Canonical repairs completed 3/3 (`RATIFIED_REPAIR_RESULTS.json`): E01_C002 tileset re-derived from the intact opaque source with zero keying (REPAIRED_WITH_FLAGS, 100% identity with all previously retained pixels, dark-tile pixels restored); B01_C001 and B02_C002 backgrounds recomposed to full-frame 16:9 and re-derived at exactly 640x360 (REPAIRED). Repaired derivatives live only under `assets/candidates/visual_canon/ratified_repairs/`; original candidate libraries are byte-untouched.
- `assets/candidates/visual_canon/FINAL_VISUAL_CANON_MANIFEST.json` was authoritative for asset promotion (canonical file per slot, hashes, repair provenance).
- LIVE PROMOTION COMPLETE 2026-09-20: all 29 canonical assets promoted byte-preserving (copy only, SHA-256 verified live == canonical for every file); 7 replaced existing live paths (previous live SHA-256 recorded), 22 created at deterministic snake_case paths. Full map with provenance and rollback hashes: `assets/candidates/visual_canon/LIVE_ASSET_PROMOTION_MANIFEST.json`. Git history is the rollback mechanism.
- Integrated into existing implemented surfaces (visual-only changes): player sheet regions, Wisdom Fruit hframes=4, Repair/Replenish terminal atlas halves, HUD five 16x16 icons, ReadyGlow VFX texture, greenhouse background (z -10), greenhouse tileset (promoted only — no TileMap painting), ResearchTerminal/GardenerDrone/SectorDoor placeholder polygons/ColorRect replaced by canonical Sprite2Ds at floor-consistent positions (names, scripts, Area2D shapes, connections unchanged), EngineeringBay gained a Background Sprite2D (Backdrop retained beneath at z -11) and the CoreGlow polygon was replaced by the 96x96 reactor core Sprite2D at the established position (visual only).
- 15 slots remain PROMOTED_FUTURE_USE (drones A03-A05, fixtures B03-B05, crops C03-C05, Dexter D01/D02, E02/E03, T03 active glow, U02): present in the live library and deliberately not instantiated. C02 Trickster Vine and V02 Solar Flare VFX have graduated into live gameplay; V02 cells 2-4 remain reserved for future hazards. T03 has no existing visual state in research_terminal.gd, so it stays uninstantiated per contract.
- Visual playthrough remains pending (see Pending priority).

## Current gameplay economy
- Initial water: 5.
- Initial nutrients: 5.
- Initial power: 100%.
- Initial emergency resupplies: 2.
- Chaos: 0 initially; caught Trickster Fruit yields 1 Chaos. The catch reports the stored total through the station-message HUD rather than inventing an unratified icon.
- Paradox Trellis costs 3 Chaos; after unlock, Trickster tend theft becomes a shared pulse that advances both the neighboring Wisdom Fruit and the Trickster Vine.
- After emergency resupplies are exhausted, a full resupply costs 1 Wisdom Fruit.
- Repairing power below 50% costs 1 Wisdom Fruit.
- Efficient Grid costs 4 Wisdom Fruit and reduces passive power drain by 40%.
- Closed-Loop Hydroponics costs 6 Wisdom Fruit, raises water/nutrient caps to 15, and makes resupply free.
- Paradox Trellis costs 3 Chaos and converts the once-per-cycle Trickster tend theft into a mirrored Wisdom+Trickster pulse.

## Validation matrix
| Check | State |
|---|---|
| Godot headless editor load | verified on MacBook Godot 4.7.1 post-promotion |
| Repository smoke test | verified post-promotion and after startup-router change |
| 120-frame configured main-scene run | verified after Startup router; zero runtime/script errors |
| git diff --check | verified (post-promotion) |
| Promotion: 29/29 exist, PNG-decode, exact dimensions | verified (deterministic, sandbox) |
| Promotion: live SHA-256 == canonical SHA-256, 29/29 | verified (deterministic, sandbox) |
| Atlas-region contracts in bounds (player/crop/terminal/HUD) | verified (deterministic, sandbox) |
| Scene diffs minimal: all original nodes/connections/scripts preserved | verified (deterministic, sandbox) |
| Godot `tests/asset_promotion_test.gd` | verified on MacBook Godot 4.7.1 after completed import pass |
| Godot post-promotion smoke test | verified on MacBook Godot 4.7.1 |
| One-click visual QA harness: static build validation | verified (sandbox) |
| One-click visual QA harness: actual Mac run + screenshots | verified at 640×360: Greenhouse + Engineering captured, 34/34 crops extracted, report rebuilt; report builder also accepts a successful `report.json` when the outer launcher rc marker is missing |
| Core systems regression suite | verified: persistence relaunch, sector round-trip/fallback, all research purchases, Trickster flee/catch + persistence, one-shot Wisdom↔Trickster tend theft, Paradox Trellis mirrored pulse, Gardener, Solar Flare lifecycle/drain/mitigation/transition boundary, Greenhouse TileMap/camera, 120-frame main |
| Manual editor playthrough | pending |
| Trickster flee-event render capture | verified technically (`visual_qa_output/trickster_flee.png` produced by real Godot render); aesthetic review pending |
| Visual QA of promoted art | PENDING HUMAN REVIEW |
| Greenhouse TileMap visual/collision QA | verified mechanically + real render sanity pass; user aesthetic sign-off pending |
| Solar Flare hazard QA | verified lifecycle + exact drain rates + Efficient Grid mitigation + cross-sector continuity + exact-zero boundary + canonical V02 HUD render; user feel/aesthetic sign-off pending |
| Save/relaunch persistence journey | verified across separate Godot processes, including saved-sector resume |

## Pending priority
1. Human visual QA pass over the captured Greenhouse, Engineering, Trickster flee-event, and Solar Flare HUD renders.
2. Manual interactive playthrough for movement/transition feel, Trickster catch/steal feel, Paradox Trellis Research UX, Gardener normal-speed pathing feel, camera feel at both sector edges, and Solar Flare warning/pressure feel.
3. Next bounded gameplay slice: Lightning Vine, using the now-live Solar Flare as its risk/reward hook rather than adding an isolated third crop.
4. Engineering Bay environment pass if needed: replace its remaining placeholder floor/wall presentation without destabilizing the validated sector loop.
5. Dexter vendor, anomaly framework, audio, and release polish (D01_ALT_C001 art ready, locked, no vendor gameplay).

## Revision history
- Revision 1: initial current-state control surface created during upgrade pass.
- Revision 2: promoted headless import/smoke/runtime checks to verified after successful execution; reconciled implemented progression and persistence state.
- Revision 3: recorded explicit human approval of all 29 recommended visual-canon primaries; ratification decision file is now authoritative while repair compilation and live promotion remain pending.
- Revision 4: compiled the human-ratified canon (29/29), pruned the 25-entry draft repair queue to 3 canonical repairs, completed all 3 repairs non-destructively, and published FINAL_VISUAL_CANON_MANIFEST.json as the authoritative promotion input; live promotion and visual playthrough remain pending.
- Revision 5: promoted all 29 ratified canonical assets byte-preserving into live paths (7 replaced with rollback hashes recorded, 22 created; LIVE_ASSET_PROMOTION_MANIFEST.json published), integrated canonical art into the existing implemented surfaces via minimal visual-only scene edits, delivered tests/asset_promotion_test.gd, and verified promotion deterministically in-sandbox (hashes, dimensions, region bounds, scene preservation, git diff --check). Godot-run checks and visual QA pending the user's environment and review.
- Revision 6: added the one-click visual QA harness and offline review report.
- Revision 7: executed the harness on the MacBook with Godot 4.7.1, discovered fresh-checkout imports were required, added an automatic Godot import preflight, then verified asset test PASS, smoke test PASS, Greenhouse capture PASS, Engineering capture PASS, 34/34 crop/frame crops generated, and report generation PASS. Human visual judgment remains pending.
- Revision 8: added a tested Startup router so saved sector state survives an actual relaunch; invalid sector values fall back to Greenhouse. Added durable core-system regression fixtures proving two-process persistence, Greenhouse <-> Engineering routing, Research costs/effects, Gardener travel+harvest, and a 120-frame configured-main run with no runtime/script errors. Manual feel/visual QA remains pending.
- Revision 9: implemented Trickster Vine as the second crop using its canonical C02 art and the original Loki contract: a READY harvest spawns a separate fruit entity that jumps once by 72px, must be caught manually, yields Chaos rather than Wisdom Fruit, persists its escaped state across sector reloads/quit-relaunch, and is intentionally excluded from Gardener auto-harvest. Regression runner now rejects Godot error output even when a PASS token appears; real flee-event render capture succeeds.
- Revision 10: implemented the first Mythic Ecology interaction: a neighboring growing Trickster Vine can steal exactly one Wisdom Fruit tending pulse per growth cycle within 224px, including pulses triggered by automation. Added Paradox Trellis at the Research Terminal for 3 Chaos; after unlock the stolen pulse advances both crops. Steal state, Chaos, and the upgrade persist; regression coverage verifies base theft, one-shot limit, reload persistence, upgraded mirrored behavior, and all prior core systems.
- Revision 11: completed the Greenhouse environment gate. Painted canonical E01 floor/wall TileMapLayers, proved TileSet collision independently, removed the obsolete StaticBody2D room stubs, standardized the live viewport at 640×360 with a bounded player-follow Camera2D and camera-synced sector backgrounds, corrected visual QA capture to the real internal resolution, and hardened report generation so a completed `report.json` remains valid evidence when the outer launcher rc marker is interrupted.
- Revision 12: implemented the first recurring station hazard, Solar Flare. Added a 30/5/8/45 calm-warning-active-recovery cadence, 5× active power drain with Efficient Grid mitigation, transient cross-sector hazard continuity, canonical V02 HUD feedback, an exact-zero transition guard, smoke coverage, a real 640×360 active-flare render proof, and full regression coverage.

## Delivery
- Branch: `arena/01a0bd0b-starlight-acre`
- Pull request: #2 (`westkitty/starlight-acre`)
- Exact implementation commits: use Git history; the operational-state revision is authoritative for semantic status, not a self-embedded SHA.
