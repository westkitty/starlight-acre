# Starlight Acre Operational State

Project ID: starlight-acre
Revision: 2
Updated: 2026-09-17

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

## Delivery
- Implementation commit: 07e6196bc1278e55dd6653798c5865e55f7d21fb
