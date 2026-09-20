# Starlight Acre — One-Click Visual QA

A double-clickable macOS harness that proves what the game actually looks
like after the canonical asset promotion: it runs the project's technical
checks, captures real screenshots of the live Greenhouse and Engineering
scenes, extracts close-up QA views of every consumed atlas region, and opens
an offline HTML review page.

## How to run (normal workflow)

1. In Finder, open the repository's `tools/` folder.
2. Double-click **`Starlight_Acre_Visual_QA.command`**.
3. That's it. A Terminal window shows progress, a game window opens for a few
   seconds while screenshots are taken, and the report then opens in your
   browser automatically.

Nothing needs to be typed, edited, or configured.

## What happens, in order

1. The launcher finds Godot (no downloads, nothing installed, no global
   system changes). It checks the `godot` / `godot4` commands,
   `/usr/local/bin`, `/opt/homebrew/bin`, `/Applications/Godot*.app`, and
   `~/Applications/Godot*.app`, and requires version 4.x (4.7.1 verified).
2. It runs the repository's two existing checks headlessly:
   `tests/asset_promotion_test.gd` and `tests/smoke_test.gd`.
3. It runs `tools/visual_qa/run_visual_qa.gd` in a real game window, which
   instantiates the actual `GreenhouseSector` and `EngineeringBay` scenes
   (player, HUD, drone, terminals, doors — the true live composition) and
   saves screenshots plus the exact atlas crops the scenes consume
   (player animation frames, Wisdom Fruit states, terminals, HUD icons,
   true-scale reference set).
4. `tools/visual_qa/build_report.py` (Python standard library only — no
   third-party packages) builds `visual_qa_output/index.html`, a single
   self-contained offline page with all images embedded.
5. The report opens in your browser via `open`.

## Reviewing

For each section of the report click **LOOKS GOOD** or **NEEDS ATTENTION**
(add a note where attention is needed), fill in the TileMap decision gate,
then press **SHOW REVIEW SUMMARY** and copy the text (Command+A, Command+C)
back into the chat. The summary text is always visible in the page — no
download or clipboard permission is needed.

Choices persist in the browser's localStorage. If your browser refuses to
store localStorage for local files (Safari sometimes does), simply copy the
summary before closing the page.

## Requirements

- macOS
- Godot 4.x (4.7.1 is the verified version)
- `python3` (standard on Macs with Apple's Command Line Tools)

## Safety

- No gameplay scripts, scenes, or artwork are modified — this is a read-only
  QA pass over what is already there.
- No cheats or debug behavior are added to production scripts.
- Every Godot run uses an isolated `HOME` (`visual_qa_output/.qa_home`,
  deleted afterwards), so the QA run cannot read or write your real Godot
  application data or saves.
- All output lives in `visual_qa_output/` at the repository root, which is
  git-ignored; each run replaces the previous results.
- Every Godot invocation is watchdogged (90 s) so nothing can hang forever.

## Troubleshooting

- **"Godot could not be found"** — install the Godot 4 app (drag `Godot.app`
  into `/Applications`) and double-click the launcher again.
- **"Godot was found, but it is not version 4.x"** — an old Godot 3 was found
  first; install Godot 4 and retry.
- **macOS refuses to run the file** — files created by `git clone` normally
  run without any prompt. If macOS nevertheless blocks it, right-click the
  file and choose *Open* once (or System Settings → Privacy & Security →
  *Open Anyway*). If it says the file is not executable, run once in
  Terminal: `chmod +x <path>/tools/Starlight_Acre_Visual_QA.command`.
- **The game window flashes and closes** — that is the screenshot capture;
  it is supposed to take only a few seconds.
- A stuck or failing step is reported in the Terminal window, and failing
  checks (with their logs) are shown in the report itself.

## Files

| File | Purpose |
|---|---|
| `tools/Starlight_Acre_Visual_QA.command` | Double-clickable launcher |
| `tools/visual_qa/run_visual_qa.gd` | Godot capture harness (screenshots + atlas crops + report.json) |
| `tools/visual_qa/build_report.py` | Offline HTML report builder (stdlib only) |
| `tools/visual_qa/README.md` | This file |
| `visual_qa_output/` | Generated at runtime (git-ignored) |
