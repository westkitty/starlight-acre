#!/usr/bin/env python3
"""Static validation for Godot text scenes and resource references.

This is not a substitute for opening the project in Godot, but it catches common
branch-breaking mistakes before the editor/runtime pass: missing res:// targets,
missing instance paths, and missing key validation surfaces.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RES_PATTERN = re.compile(r'res://([^"\)]+)')
REQUIRED_PATHS = [
    "project.godot",
    "autoload/Events.gd",
    "autoload/GameState.gd",
    "actors/crops/CropPlot.tscn",
    "actors/crops/crop_plot.gd",
    "actors/transitions/DoorTransition.tscn",
    "actors/terminals/SaveTerminal.tscn",
    "actors/vendors/DexterTerminal.tscn",
    "data/crops/trickster_vine.gd",
    "scenes/world/GreenhouseSector.tscn",
    "scenes/world/ArchiveLibrary.tscn",
    "ui/hud/HUD.tscn",
]
REQUIRED_TEXT = {
    "project.godot": ["GameState=\"*res://autoload/GameState.gd\""],
    "autoload/Events.gd": ["signal status_message_changed"],
    "scenes/world/GreenhouseSector.tscn": ["TileVisualPass", "ArchiveDoor", "TricksterPlot", "SaveTerminal", "LoadTerminal"],
    "scenes/world/ArchiveLibrary.tscn": ["DexterTerminal", "GreenhouseDoor", "TricksterPlot"],
    "ui/hud/HUD.tscn": ["StatusLabel", "TricksterVine"],
}


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return ""


def main() -> int:
    failures: list[str] = []

    for rel in REQUIRED_PATHS:
        if not (ROOT / rel).exists():
            failures.append(f"missing required path: {rel}")

    for rel, needles in REQUIRED_TEXT.items():
        text = read_text(ROOT / rel)
        for needle in needles:
            if needle not in text:
                failures.append(f"{rel} missing expected text: {needle}")

    for path in ROOT.rglob("*.tscn"):
        text = read_text(path)
        for match in RES_PATTERN.finditer(text):
            rel = match.group(1)
            if not (ROOT / rel).exists():
                failures.append(f"{path.relative_to(ROOT)} references missing res://{rel}")

    if failures:
        print("Static scene audit failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("Static scene audit passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
