# Starlight Acre Operational State

Project ID: starlight-acre
Revision: 4
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
- Generated art source files are 640x640 despite historical documentation claiming sprite-sheet dimensions such as 32x48, 32x32, and 16x16.
- Technical loading therefore does not prove that recovered atlas regions look correct.
- No bespoke art exists yet for Trickster Vine or other additional mythic crops.
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
- `assets/candidates/visual_canon/FINAL_VISUAL_CANON_MANIFEST.json` is authoritative for subsequent asset promotion (canonical file per slot, hashes, repair provenance).
- Live-game promotion remains pending; visual playthrough remains pending. Nothing has been promoted into assets/sprites, assets/backgrounds, assets/tilesets or assets/ui.

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
| Godot headless editor load | verified |
| Repository smoke test | verified |
| 120-frame main-scene run | verified |
| git diff --check | verified |
| Manual editor playthrough | pending |
| Visual sprite-slice QA | pending |
| TileMap visual/collision QA | pending |
| Save/relaunch persistence journey | pending |

## Pending priority
1. Manual Godot editor visual/playthrough proof.
2. Correct/reslice generated sprite sheets based on actual source imagery.
3. Paint greenhouse TileMapLayer and validate collision before deleting stubs.
4. Add second mythic crop only after crop-resource architecture and visuals are proven.
5. Implement the first cross-crop Mythic Ecology interaction.
6. Dexter vendor, anomaly framework, audio, and release polish.

## Revision history
- Revision 1: initial current-state control surface created during upgrade pass.
- Revision 2: promoted headless import/smoke/runtime checks to verified after successful execution; reconciled implemented progression and persistence state.
- Revision 3: recorded explicit human approval of all 29 recommended visual-canon primaries; ratification decision file is now authoritative while repair compilation and live promotion remain pending.
- Revision 4: compiled the human-ratified canon (29/29), pruned the 25-entry draft repair queue to 3 canonical repairs, completed all 3 repairs non-destructively, and published FINAL_VISUAL_CANON_MANIFEST.json as the authoritative promotion input; live promotion and visual playthrough remain pending.

## Delivery
- Implementation commit: 07e6196bc1278e55dd6653798c5865e55f7d21fb
