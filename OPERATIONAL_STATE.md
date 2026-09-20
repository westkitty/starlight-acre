# Starlight Acre Operational State

Project ID: starlight-acre
Revision: 5
Updated: 2026-09-20

## Purpose
A small, finishable 2D orbital mythic farming-station game in which the player restores a failing station by cultivating mythic crops, managing station systems, automating repetitive work, and expanding into additional sectors.

## Current baseline
- Repository: westkitty/starlight-acre
- Source baseline before this upgrade: main at 97eb3f8
- Active implementation worktree: /Users/andrew/starlight-acre-upgrade
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
- StaticBody2D greenhouse collision remains until TileMap collision is explicitly proven.

## Verified working
- Godot 4.7.1 can initialize the modified project headlessly without script/resource parse errors.
- `tests/smoke_test.gd` passes and loads GreenhouseSector, EngineeringBay, CropPlot, ResearchTerminal, and Wisdom Fruit Resource.
- The real main scene runs headlessly for 120 frames without script/runtime errors.
- Previously invalid JPEG-encoded .png files were normalized and import successfully.
- Recovered July terminal/HUD/VFX files parse under the current runtime.
- GameState autoload is accepted by the project.
- Multi-sector scenes and resource definitions load successfully.

## Implemented but not fully verified
- Manual player journey across Greenhouse -> Engineering -> Greenhouse.
- JSON persistence across a full quit/relaunch user journey.
- Research purchase UX and exact balance.
- Spatial Gardener Drone feel/pathing during interactive play.
- Visual sprite slicing and composition.

## Known limitations
- TileMapLayer floor/wall painting remains unfinished; StaticBody2D collision is authoritative.
- ~~Generated art source files are 640x640 despite historical documentation claiming sprite-sheet dimensions~~ Resolved by canon promotion: live files are now exactly the documented sheet dimensions (192x192 player, 128x32 crop states, 64x64 terminals, 80x16 HUD, 256x256 tileset, 128x32 VFX, 640x360 backgrounds).
- Visual QA of the promoted art is PENDING HUMAN REVIEW: dimensions, hashes, region bounds, and scene loads are deterministically verified, but on-screen appearance has not been judged.
- Additional mythic crops (C02-C05), engineering fixtures, drones, Dexter (D01_ALT_C001 exact, locked), HUD extensions, and hazard VFX are promoted as PROMOTED_FUTURE_USE art only — no gameplay instantiated.
- Audio remains absent.
- Implementation commit recorded: 07e6196bc1278e55dd6653798c5865e55f7d21fb. Push status is recorded below after delivery.

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
- 17 slots are PROMOTED_FUTURE_USE (drones A03-A05, fixtures B03-B05, crops C02-C05, Dexter D01/D02, E02/E03, T03 active glow, U02, V02): present in the live library, deliberately not instantiated, zero gameplay/schema changes. T03 has no existing visual state in research_terminal.gd, so it stays uninstantiated per contract.
- Visual playthrough remains pending (see Pending priority).

## Current gameplay economy
- Initial water: 5.
- Initial nutrients: 5.
- Initial power: 100%.
- Initial emergency resupplies: 2.
- After emergency resupplies are exhausted, a full resupply costs 1 Wisdom Fruit.
- Repairing power below 50% costs 1 Wisdom Fruit.
- Efficient Grid costs 4 Wisdom Fruit and reduces passive power drain by 40%.
- Closed-Loop Hydroponics costs 6 Wisdom Fruit, raises water/nutrient caps to 15, and makes resupply free.

## Validation matrix
| Check | State |
|---|---|
| Godot headless editor load | verified (pre-promotion baseline; re-run recommended after promotion) |
| Repository smoke test | verified (pre-promotion baseline; re-run recommended after promotion) |
| 120-frame main-scene run | verified (pre-promotion baseline; re-run recommended after promotion) |
| git diff --check | verified (post-promotion) |
| Promotion: 29/29 exist, PNG-decode, exact dimensions | verified (deterministic, sandbox) |
| Promotion: live SHA-256 == canonical SHA-256, 29/29 | verified (deterministic, sandbox) |
| Atlas-region contracts in bounds (player/crop/terminal/HUD) | verified (deterministic, sandbox) |
| Scene diffs minimal: all original nodes/connections/scripts preserved | verified (deterministic, sandbox) |
| Godot `tests/asset_promotion_test.gd` | pending user environment (no Godot binary in promotion sandbox; test delivered, one command: `godot --headless --script tests/asset_promotion_test.gd`, expect `STARLIGHT_ASSET_PROMOTION_PASS`) |
| Godot post-promotion smoke + 120-frame re-run | pending user environment |
| Manual editor playthrough | pending |
| Visual QA of promoted art | PENDING HUMAN REVIEW |
| TileMap visual/collision QA | pending |
| Save/relaunch persistence journey | pending |

## Pending priority
1. Manual Godot editor visual/playthrough proof of the promoted canon (run `godot --headless --script tests/asset_promotion_test.gd` and the smoke test first in the verified 4.7.1 environment).
2. Human visual QA pass over the 29 promoted assets in-game.
3. Paint greenhouse TileMapLayer and validate collision before deleting stubs (E01/E02 tilesets already promoted).
4. Add second mythic crop only after crop-resource architecture and visuals are proven (C02-C05 art ready as PROMOTED_FUTURE_USE).
5. Implement the first cross-crop Mythic Ecology interaction.
6. Dexter vendor, anomaly framework, audio, and release polish (D01_ALT_C001 art ready, locked, no vendor gameplay).

## Revision history
- Revision 1: initial current-state control surface created during upgrade pass.
- Revision 2: promoted headless import/smoke/runtime checks to verified after successful execution; reconciled implemented progression and persistence state.
- Revision 3: recorded explicit human approval of all 29 recommended visual-canon primaries; ratification decision file is now authoritative while repair compilation and live promotion remain pending.
- Revision 4: compiled the human-ratified canon (29/29), pruned the 25-entry draft repair queue to 3 canonical repairs, completed all 3 repairs non-destructively, and published FINAL_VISUAL_CANON_MANIFEST.json as the authoritative promotion input; live promotion and visual playthrough remain pending.
- Revision 5: promoted all 29 ratified canonical assets byte-preserving into live paths (7 replaced with rollback hashes recorded, 22 created; LIVE_ASSET_PROMOTION_MANIFEST.json published), integrated canonical art into the existing implemented surfaces via minimal visual-only scene edits, delivered tests/asset_promotion_test.gd, and verified promotion deterministically in-sandbox (hashes, dimensions, region bounds, scene preservation, git diff --check). Godot-run checks and visual QA pending the user's environment and review.

## Delivery
- Implementation commit: 07e6196bc1278e55dd6653798c5865e55f7d21fb
