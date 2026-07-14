# Starlight Acre Validation Runbook

This branch is still a prototype branch. Completion claims require evidence from the checks below.

## Static Audit

Run from the repository root:

```bash
python3 tools/validation/static_scene_audit.py
```

Pass condition:
- required prototype files exist;
- key scene nodes are present;
- `.tscn` `res://` references point to existing files.

This check does not prove Godot can import or run the project.

## Godot Headless Smoke Test

Run from the repository root on a machine with Godot 4.3:

```bash
godot4 --headless --path . --script tools/validation/godot_smoke_test.gd
```

If the binary is named `godot`, use:

```bash
godot --headless --path . --script tools/validation/godot_smoke_test.gd
```

Pass condition:
- required scenes and resources load;
- Greenhouse, Archive Library, and HUD instantiate;
- critical nodes exist in each scene.

## Manual Prototype Smoke Path

Run `scenes/world/GreenhouseSector.tscn` in Godot 4.3 and verify:

1. Player moves left/right and jumps.
2. Wisdom Fruit can be planted, tended, and harvested.
3. Trickster Vine can be planted, tended, and harvested.
4. Repair and Replenish terminals update HUD resources.
5. Save terminal shows a success status message.
6. Load terminal with no save shows a visible failure message.
7. Archive door transitions to Archive Library.
8. Returning from Archive Library preserves Greenhouse resource and crop state.
9. Archive Library crop state persists after leaving and returning.
10. Dexter trade fails visibly without 2 Wisdom Fruit.
11. Dexter trade succeeds visibly with 2 Wisdom Fruit.
12. HUD prompt and status messages do not overlap core resource UI.
13. No critical console errors appear during a 10-minute session.

## Visual Tile Pass

This branch includes a text-authored `TileVisualPass` fallback in `GreenhouseSector.tscn` so the greenhouse is not visually empty if TileMapLayer painting has not happened yet.

Still recommended in the Godot editor:
- paint the actual `TileMapLayer_Background`, `TileMapLayer_Floor`, and `TileMapLayer_Walls` layers;
- configure tile collision before removing the StaticBody2D floor/walls;
- keep `TileVisualPass` only if it still improves readability after the editor-authored TileMap pass.

## Evidence To Record

After validation, append a dated note to `Starlight_Acre_bible.md` with:

- Godot version;
- operating system;
- commands run;
- smoke-test result;
- manual findings;
- screenshots or capture location if available;
- remaining defects.
