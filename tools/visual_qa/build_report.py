#!/usr/bin/env python3
"""Build the offline Starlight Acre visual QA report (index.html).

Reads the QA output folder produced by tools/Starlight_Acre_Visual_QA.command
(technical-check logs, report.json from the Godot capture run, screenshots,
extracted crop PNGs) and writes a single self-contained index.html designed
for human visual review.

Completely offline: all images are embedded as base64 data URIs and no
external resources are referenced. Python standard library only — no
third-party packages are required.

Usage:
    python3 build_report.py [--repo REPO_ROOT] [--output OUTPUT_DIR]
"""

import argparse
import base64
import datetime
import html
import json
import os
import struct
import subprocess
import sys

# Pass tokens printed by the repository's existing Godot tests.
CHECK_TOKENS = {
    "asset_test": "STARLIGHT_ASSET_PROMOTION_PASS",
    "smoke_test": "STARLIGHT_SMOKE_PASS",
}
CHECK_LABELS = {
    "asset_test": "Asset promotion test",
    "smoke_test": "Smoke test",
    "screenshot_capture": "Screenshot capture",
}
CHECK_FILES = {
    "asset_test": "tests/asset_promotion_test.gd",
    "smoke_test": "tests/smoke_test.gd",
    "screenshot_capture": "tools/visual_qa/run_visual_qa.gd",
}

# Reviewable report sections.
SECTIONS = [
    ("greenhouse", "Greenhouse"),
    ("engineering", "Engineering"),
    ("player_sheet", "Player Animation Sheet"),
    ("wisdom_fruit", "Wisdom Fruit States"),
    ("terminals", "Terminals"),
    ("hud_icons", "HUD Icons"),
    ("scale_check", "Scale Check"),
]

# TileMap decision gate — environment composition decisions for a LATER phase.
TILEMAP_ITEMS = [
    ("floor_tiling", "Floor tiling"),
    ("wall_tiling", "Wall tiling"),
    ("foreground_trim", "Foreground trim"),
    ("prop_density", "Prop density"),
    ("depth_improvement", "Depth improvement"),
]

# Exact atlas regions extracted by tools/visual_qa/run_visual_qa.gd.
# crop_id -> (display label, note, expected_w, expected_h) — must match the
# CROPS table in run_visual_qa.gd.
CROP_GROUPS = {
    "player_frames": {
        "factor": 4,
        "rows": [
            ("Idle (4 frames)", ["player_idle_0", "player_idle_1", "player_idle_2", "player_idle_3"]),
            ("Walk (6 frames)", ["player_walk_0", "player_walk_1", "player_walk_2", "player_walk_3", "player_walk_4", "player_walk_5"]),
            ("Jump / Fall / Land", ["player_jump", "player_fall", "player_land"]),
            ("Interact (2 frames)", ["player_interact_0", "player_interact_1"]),
        ],
        "items": {
            "player_idle_0": ("idle 0", "rect (0,0)", 32, 48),
            "player_idle_1": ("idle 1", "rect (32,0)", 32, 48),
            "player_idle_2": ("idle 2", "rect (64,0)", 32, 48),
            "player_idle_3": ("idle 3", "rect (96,0)", 32, 48),
            "player_walk_0": ("walk 0", "rect (0,48)", 32, 48),
            "player_walk_1": ("walk 1", "rect (32,48)", 32, 48),
            "player_walk_2": ("walk 2", "rect (64,48)", 32, 48),
            "player_walk_3": ("walk 3", "rect (96,48)", 32, 48),
            "player_walk_4": ("walk 4", "rect (128,48)", 32, 48),
            "player_walk_5": ("walk 5", "rect (160,48)", 32, 48),
            "player_jump": ("jump", "rect (0,96)", 32, 48),
            "player_fall": ("fall", "rect (32,96)", 32, 48),
            "player_land": ("land", "rect (64,96)", 32, 48),
            "player_interact_0": ("interact 0", "rect (0,144)", 32, 48),
            "player_interact_1": ("interact 1", "rect (32,144)", 32, 48),
        },
    },
    "fruit_states": {
        "factor": 4,
        "rows": [("Four states (CropPlot hframes=4, 32x32 cells)",
                  ["fruit_empty", "fruit_planted", "fruit_growing", "fruit_ready"])],
        "items": {
            "fruit_empty": ("empty", "cell 0", 32, 32),
            "fruit_planted": ("planted (seedling)", "cell 1", 32, 32),
            "fruit_growing": ("growing", "cell 2", 32, 32),
            "fruit_ready": ("ready", "cell 3", 32, 32),
        },
    },
    "terminals": {
        "factor": 3,
        "rows": [("Live terminal sprites",
                  ["terminal_repair", "terminal_replenish", "terminal_research"])],
        "items": {
            "terminal_repair": ("Repair", "left half of terminals.png", 32, 64),
            "terminal_replenish": ("Replenish", "right half of terminals.png", 32, 64),
            "terminal_research": ("Research", "research_terminal.png", 64, 80),
        },
    },
    "hud_icons": {
        "factor": 4,
        "rows": [("Five live HUD cells (16x16)",
                  ["hud_water", "hud_nutrient", "hud_power", "hud_fruit", "hud_prompt"])],
        "items": {
            "hud_water": ("water", "cell 0", 16, 16),
            "hud_nutrient": ("nutrient", "cell 1", 16, 16),
            "hud_power": ("power", "cell 2", 16, 16),
            "hud_fruit": ("fruit", "cell 3", 16, 16),
            "hud_prompt": ("prompt", "cell 4", 16, 16),
        },
    },
    "scale_row": {
        "factor": 1,
        "rows": [("All sprites at true relative pixel scale — nothing is resized", [
            "scale_player", "scale_gardener_drone", "scale_wisdom_fruit",
            "scale_repair_terminal", "scale_research_terminal", "scale_sector_door",
            "scale_reactor_core"])],
        "items": {
            "scale_player": ("Player (idle 0)", "32x48", 32, 48),
            "scale_gardener_drone": ("Gardener Drone", "32x32", 32, 32),
            "scale_wisdom_fruit": ("Wisdom Fruit (ready)", "32x32", 32, 32),
            "scale_repair_terminal": ("Repair terminal", "32x64", 32, 64),
            "scale_research_terminal": ("Research terminal", "64x80", 64, 80),
            "scale_sector_door": ("Sector Door", "64x112", 64, 112),
            "scale_reactor_core": ("Reactor Core", "96x96", 96, 96),
        },
    },
}

# Which crop group feeds which reviewable section.
SECTION_CROP_GROUP = {
    "player_sheet": "player_frames",
    "wisdom_fruit": "fruit_states",
    "terminals": "terminals",
    "hud_icons": "hud_icons",
    "scale_check": "scale_row",
}


def read_png_size(path):
    """Return (width, height) from a PNG header, or None."""
    try:
        with open(path, "rb") as f:
            head = f.read(24)
        if len(head) >= 24 and head[:8] == b"\x89PNG\r\n\x1a\n" and head[12:16] == b"IHDR":
            w, h = struct.unpack(">II", head[16:24])
            return int(w), int(h)
    except OSError:
        pass
    return None


def data_uri(path):
    """Return a data:image/png;base64 URI, or None if unreadable."""
    try:
        with open(path, "rb") as f:
            return "data:image/png;base64," + base64.b64encode(f.read()).decode("ascii")
    except OSError:
        return None


def log_tail(text, max_chars=4000, max_lines=40):
    lines = text.rstrip().splitlines()
    return "\n".join(lines[-max_lines:])[:max_chars]


def read_check(out_dir, name):
    """Read one technical check. PASS requires exit code 0 AND the pass token."""
    rc_path = os.path.join(out_dir, "check_%s.rc" % name)
    log_path = os.path.join(out_dir, "check_%s.log" % name)
    if not os.path.isfile(rc_path):
        return {"status": "NOT_RUN", "exit_code": None, "log": ""}
    try:
        rc = open(rc_path).read().strip()
    except OSError:
        return {"status": "NOT_RUN", "exit_code": None, "log": ""}
    log = ""
    if os.path.isfile(log_path):
        try:
            log = open(log_path, errors="replace").read()
        except OSError:
            log = ""
    token = CHECK_TOKENS.get(name, "")
    ok = rc == "0" and (not token or token in log)
    return {"status": "PASS" if ok else "FAIL", "exit_code": rc, "log": log}


def read_capture(out_dir):
    """Assemble the screenshot-capture check from rc + report.json + PNGs."""
    rc_path = os.path.join(out_dir, "check_capture.rc")
    report = {}
    rep_path = os.path.join(out_dir, "report.json")
    if os.path.isfile(rep_path):
        try:
            report = json.load(open(rep_path)) or {}
        except (OSError, ValueError):
            report = {}
    shots = {}
    for name in ("greenhouse", "engineering"):
        png = os.path.join(out_dir, "%s.png" % name)
        present = os.path.isfile(png) and os.path.getsize(png) > 0
        rep_entry = (report.get("captures") or {}).get(name) or {}
        shots[name] = {
            "file": "%s.png" % name,
            "present": present,
            "png_size": read_png_size(png) if present else None,
            "report_status": rep_entry.get("status", ""),
            "report_size": rep_entry.get("size"),
        }
    log = ""
    if os.path.isfile(os.path.join(out_dir, "check_capture.log")):
        try:
            log = open(os.path.join(out_dir, "check_capture.log"), errors="replace").read()
        except OSError:
            log = ""
    both_ok = all(s["present"] and s["report_status"] == "OK" for s in shots.values())
    if not os.path.isfile(rc_path):
        # The outer macOS launcher can be interrupted after the Godot capture
        # script has already completed and written its own authoritative
        # report. In that case, do not downgrade a fully recorded successful
        # capture to NOT_RUN merely because the wrapper's rc marker is absent.
        status = "PASS" if (report.get("status") == "OK" and both_ok) else "NOT_RUN"
        return {"status": status, "exit_code": None, "log": log,
                "report": report, "shots": shots}
    try:
        exit_code = open(rc_path).read().strip()
    except OSError:
        exit_code = None
    status = "PASS" if (exit_code == "0" and both_ok) else "FAIL"
    return {"status": status, "exit_code": exit_code, "log": log,
            "report": report, "shots": shots}


def crop_html(out_dir, crop_id, factor, exp_w, exp_h, true_size=False):
    """One crop image (or PENDING placeholder). Returns bare markup — the
    caller owns the frame wrapper and caption."""
    path = os.path.join(out_dir, "crops", "%s.png" % crop_id)
    uri = data_uri(path)
    if uri is None:
        return ('<div class="pending-box pix" style="width:%dpx;height:%dpx">PENDING</div>'
                % (exp_w * factor, exp_h * factor))
    size = read_png_size(path)
    warn = ""
    if size is not None and size != (exp_w, exp_h):
        warn = ' <span class="dimwarn">(file is %dx%d — expected %dx%d)</span>' \
               % (size[0], size[1], exp_w, exp_h)
    if true_size:
        return ('<img class="pix" src="%s" alt="%s true size">'
                '<div class="cap">true size %dx%d%s</div>'
                % (uri, crop_id, exp_w, exp_h, warn))
    if factor == 1:
        return '<img class="pix" src="%s" alt="%s">%s' % (uri, crop_id, warn)
    return ('<div><img class="pix" style="width:%dpx" src="%s" alt="%s"></div>'
            % (exp_w * factor, uri, crop_id))


def group_html(out_dir, group_key):
    group = CROP_GROUPS[group_key]
    factor = group["factor"]
    show_true = group_key in ("terminals", "hud_icons")
    frames_class = "frames scales" if group_key == "scale_row" else "frames"
    parts = []
    for row_label, ids in group["rows"]:
        parts.append('<div class="row-label">%s</div>' % html.escape(row_label))
        parts.append('<div class="%s">' % frames_class)
        for cid in ids:
            label, note, w, h = group["items"][cid]
            parts.append('<div class="frame">')
            parts.append(crop_html(out_dir, cid, factor, w, h))
            if show_true:
                parts.append('<div style="height:10px"></div>')
                parts.append(crop_html(out_dir, cid, 1, w, h, true_size=True))
            parts.append('<div class="cap"><b>%s</b> · %s</div>'
                         % (html.escape(label), html.escape(note)))
            parts.append("</div>")
        parts.append("</div>")
    return "\n".join(parts)


def screenshot_html(out_dir, name, capture):
    shot = capture["shots"][name]
    if not shot["present"]:
        return ('<div class="pending-shot">SCREENSHOT PENDING — this image is '
                'generated when the harness runs on a Mac with Godot.</div>')
    uri = data_uri(os.path.join(out_dir, "%s.png" % name))
    png_size = shot["png_size"]
    rep_size = shot["report_size"]
    meta = "captured %dx%d" % png_size if png_size else ""
    if rep_size and tuple(rep_size) != tuple(png_size or ()):
        meta += " (window %sx%s)" % (rep_size[0], rep_size[1])
    status_note = "" if shot["report_status"] == "OK" else \
        ' <span class="dimwarn">(capture script reported: %s)</span>' \
        % html.escape(shot["report_status"] or "no status")
    return (
        '<img class="shot" src="%s" alt="%s screenshot">'
        '<div class="cap">%s%s</div>'
        '<details><summary>view full resolution (1:1 pixels)</summary>'
        '<div class="fullsize"><img class="pix" src="%s" alt="%s full resolution"></div>'
        "</details>"
        % (uri, name, meta, status_note, uri, name))


def review_block(section_id):
    return (
        '<div class="review" data-section="%s">'
        '<div class="review-label">Your review:</div>'
        '<button type="button" class="choice good" id="btn_%s_LOOKS_GOOD">LOOKS GOOD</button> '
        '<button type="button" class="choice attention" id="btn_%s_NEEDS_ATTENTION">NEEDS ATTENTION</button>'
        '<textarea class="note" id="note_%s" rows="3" '
        'placeholder="What needs attention? (added to the review summary)"></textarea>'
        "</div>" % (section_id, section_id, section_id, section_id))


def chip(status):
    return '<span class="chip %s">%s</span>' % (status.lower(), html.escape(status))


def fill_template(page, values):
    for token, value in values.items():
        page = page.replace("{{%s}}" % token, value)
    return page


def build_html(out_dir, checks, capture, commit, build_time):
    tech = dict(checks)
    tech["screenshot_capture"] = {
        "status": capture["status"], "exit_code": capture["exit_code"],
        "log": capture["log"]}
    all_pass = all(c["status"] == "PASS" for c in tech.values())
    banner = (
        '<div class="banner ok">ALL TECHNICAL CHECKS PASS — review the visuals below</div>'
        if all_pass else
        '<div class="banner bad">TECHNICAL ISSUES DETECTED — see Overall Status '
        "below; failing checks are listed there with their logs</div>")

    report = capture.get("report") or {}
    godot_version = str(report.get("godot_version", "not recorded"))
    window_size = report.get("window_size")

    # ---- Overall status table
    rows = []
    for key in ("asset_test", "smoke_test", "screenshot_capture"):
        c = tech[key]
        log = log_tail(c["log"])
        log_html = ""
        if log:
            log_html = ('<details><summary>view log (last lines)</summary>'
                        "<pre>%s</pre></details>" % html.escape(log))
        exit_note = ""
        if c["exit_code"] not in (None, "0"):
            exit_note = ' <span class="dimwarn">(exit code %s)</span>' \
                        % html.escape(str(c["exit_code"]))
        rows.append(
            "<tr><td>%s</td><td>%s</td><td>%s%s</td><td>%s</td></tr>"
            % (html.escape(CHECK_LABELS[key]), chip(c["status"]),
               html.escape(CHECK_FILES[key]), exit_note, log_html))

    meta_bits = ["generated %s" % build_time,
                 "Godot %s" % html.escape(godot_version),
                 "commit %s" % html.escape(commit)]
    if window_size:
        meta_bits.append("capture window %sx%s" % (window_size[0], window_size[1]))

    # ---- Reviewable sections
    sections_html = []
    for sid, title in SECTIONS:
        if sid == "greenhouse":
            body = screenshot_html(out_dir, "greenhouse", capture)
        elif sid == "engineering":
            body = screenshot_html(out_dir, "engineering", capture)
        elif sid in SECTION_CROP_GROUP:
            body = group_html(out_dir, SECTION_CROP_GROUP[sid])
        else:
            body = ""
        sections_html.append(
            '<section id="%s"><h2>%s</h2>%s%s</section>'
            % (sid, html.escape(title), body, review_block(sid)))

    tile_rows = []
    for tid, tlabel in TILEMAP_ITEMS:
        tile_rows.append(
            '<div class="tile-row"><span>%s</span>'
            '<select id="tile_%s"><option>UNSURE</option><option>YES</option>'
            "<option>NO</option></select></div>" % (html.escape(tlabel), tid))

    report_js = {
        "project": "starlight-acre",
        "qa_phase": "post-promotion-visual",
        "generated_at": build_time,
        "godot_version": godot_version,
        "git_commit": commit,
        "technical_checks": {k: {"status": v["status"]} for k, v in tech.items()},
    }
    report_json = json.dumps(report_js).replace("</", "<\\/")

    return fill_template(HTML_TEMPLATE, {
        "META": " · ".join(meta_bits),
        "BANNER": banner,
        "CHECKS_ROWS": "\n".join(rows),
        "SECTIONS": "\n".join(sections_html),
        "TILE_ROWS": "\n".join(tile_rows),
        "REPORT_JSON": report_json,
    })


HTML_TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Starlight Acre — Visual QA</title>
<style>
  body { font: 15px/1.5 -apple-system, BlinkMacSystemFont, "Helvetica Neue", Arial, sans-serif;
         margin: 0 auto; max-width: 1120px; padding: 26px 20px 90px; color: #1c1c1e;
         background: #f5f5f7; }
  h1 { font-size: 27px; margin: 0 0 4px; }
  h2 { font-size: 20px; margin: 0 0 12px; }
  .meta { color: #6b6b70; font-size: 13px; }
  section { margin: 30px 0; padding: 18px 20px; background: #fff; border: 1px solid #d8d8dd;
            border-radius: 12px; }
  .banner { padding: 11px 15px; border-radius: 9px; font-weight: 600; margin: 14px 0 4px; }
  .banner.ok { background: #d9f2e1; color: #14532d; }
  .banner.bad { background: #fde0dc; color: #7f1d1d; }
  table { border-collapse: collapse; width: 100%; }
  td, th { text-align: left; padding: 7px 10px; border-bottom: 1px solid #e6e6ea; vertical-align: top; }
  .chip { display: inline-block; padding: 2px 10px; border-radius: 20px; font-weight: 700;
          font-size: 12px; letter-spacing: .04em; }
  .chip.pass { background: #177a3d; color: #fff; }
  .chip.fail { background: #b3362c; color: #fff; }
  .chip.not_run { background: #77777d; color: #fff; }
  .shot { width: 100%; height: auto; border-radius: 8px; display: block;
          border: 1px solid #cfcfd4; }
  .pix { image-rendering: pixelated; image-rendering: crisp-edges; }
  .cap { font-size: 12px; color: #6b6b70; margin-top: 4px; text-align: center; }
  .row-label { font-size: 13px; font-weight: 600; color: #3c3c40; margin: 14px 0 6px; }
  .frames { display: flex; flex-wrap: wrap; gap: 14px; align-items: flex-start; }
  .frames.scales { align-items: flex-end; }
  .frame { text-align: center; }
  .frame img, .pending-box { display: block; margin: 0 auto; border: 1px solid #cfcfd4;
        background: repeating-conic-gradient(#e9e9ee 0% 25%, #ffffff 0% 50%) 0 0 / 16px 16px; }
  .pending-box { display: flex; align-items: center; justify-content: center;
                 color: #9a9aa0; font-size: 11px; border-style: dashed; }
  .pending-shot { padding: 60px 20px; text-align: center; color: #6b6b70;
                  background: repeating-conic-gradient(#e9e9ee 0% 25%, #f5f5f7 0% 50%) 0 0 / 24px 24px;
                  border: 1px dashed #b9b9c0; border-radius: 8px; }
  .fullsize { overflow: auto; max-height: 560px; border: 1px solid #d8d8dd; margin-top: 8px; }
  details { margin-top: 8px; }
  summary { cursor: pointer; color: #42427a; font-size: 13px; }
  pre { background: #17171b; color: #d6d6de; padding: 10px 12px; border-radius: 8px;
        overflow: auto; font-size: 11.5px; max-height: 300px; }
  .dimwarn { color: #b3362c; font-weight: 600; }
  .review { margin-top: 16px; padding: 12px 14px; background: #f2f2f6; border-radius: 9px; }
  .review-label { font-size: 13px; font-weight: 600; margin-bottom: 7px; }
  .choice { border: 2px solid #b9b9c0; background: #fff; border-radius: 20px;
            padding: 6px 16px; font-weight: 700; font-size: 13px; cursor: pointer; }
  .choice.good.active { background: #177a3d; border-color: #177a3d; color: #fff; }
  .choice.attention.active { background: #b3362c; border-color: #b3362c; color: #fff; }
  .note { display: none; width: 100%; margin-top: 9px; box-sizing: border-box;
          border: 1px solid #b9b9c0; border-radius: 8px; padding: 8px 10px; font: inherit; }
  .note.show { display: block; }
  .tile-row { display: flex; justify-content: space-between; align-items: center;
              padding: 8px 4px; border-bottom: 1px solid #ececf1; max-width: 480px; }
  .tile-row select { font: inherit; padding: 4px 8px; }
  .howto { background: #eef0fb; border: 1px solid #c9cdf3; padding: 12px 15px;
           border-radius: 9px; font-size: 13.5px; }
  textarea#summary_text { width: 100%; box-sizing: border-box;
           font: 12.5px/1.45 "SF Mono", Menlo, Consolas, monospace; border: 1px solid #b9b9c0;
           border-radius: 8px; padding: 10px; background: #fbfbfd; }
  button.big { border: 0; background: #42427a; color: #fff; font-weight: 700;
               padding: 10px 18px; border-radius: 9px; font-size: 14px; cursor: pointer; }
  button.ghost { border: 1px solid #b9b9c0; background: #fff; font-weight: 600;
                 padding: 8px 14px; border-radius: 9px; font-size: 13px; cursor: pointer; }
  footer { color: #86868c; font-size: 12px; margin-top: 40px; }
</style>
</head>
<body>
<h1>Starlight Acre — Visual QA</h1>
<div class="meta">{{META}}</div>
{{BANNER}}

<div class="howto"><b>How to review:</b> look at each section below and click
<b>LOOKS GOOD</b> or <b>NEEDS ATTENTION</b> (add a short note when attention is
needed). At the end, press <b>SHOW REVIEW SUMMARY</b> and copy the text
(Command+A, Command+C) back into the chat. Your choices are kept in this
browser (localStorage); if your browser does not save them for local files,
just copy the summary before closing the page.</div>

<section id="overall">
<h2>Overall Status</h2>
<table>
<tr><th>Check</th><th>Result</th><th>Source</th><th>Log</th></tr>
{{CHECKS_ROWS}}
</table>
</section>

{{SECTIONS}}

<section id="tilemap_gate">
<h2>TileMap Decision Gate (for the NEXT phase — not implemented here)</h2>
<p style="font-size:13.5px;color:#55555a">Looking at the screenshots above:
does the current environment visibly need each of these? This only records
your decision — no TileMap painting happens in this phase.</p>
{{TILE_ROWS}}
</section>

<section id="review_summary">
<h2>Review Summary</h2>
<p>
<button type="button" class="big" id="show_summary">SHOW REVIEW SUMMARY</button>
<button type="button" class="ghost" id="copy_summary">COPY (optional)</button>
<button type="button" class="ghost" id="reset_review">RESET REVIEW</button>
</p>
<p style="font-size:13px;color:#55555a">The summary text below is always kept
up to date — click into it and press Command+A then Command+C to copy. No
download and no clipboard permission is needed.</p>
<textarea id="summary_text" rows="26" readonly spellcheck="false"></textarea>
</section>

<footer>Generated by tools/visual_qa/build_report.py from the live canonical
assets and real scene captures · this page is fully offline and self-contained ·
Starlight Acre post-promotion visual QA.</footer>

<script>
"use strict";
var REPORT_KEY = "starlight-acre_visual-qa_post-promotion-visual_v1";
var SECTION_IDS = ["greenhouse","engineering","player_sheet","wisdom_fruit","terminals","hud_icons","scale_check"];
var TILE_ITEMS = ["floor_tiling","wall_tiling","foreground_trim","prop_density","depth_improvement"];
var REPORT = {{REPORT_JSON}};

function emptyState() { return { sections: {}, tilemap: {} }; }

function loadState() {
  if (typeof localStorage === "undefined") { return emptyState(); }
  try {
    var raw = localStorage.getItem(REPORT_KEY);
    if (!raw) { return emptyState(); }
    var s = JSON.parse(raw);
    if (!s || typeof s !== "object") { return emptyState(); }
    if (!s.sections) { s.sections = {}; }
    if (!s.tilemap) { s.tilemap = {}; }
    return s;
  } catch (e) { return emptyState(); }
}

function saveState(state) {
  if (typeof localStorage === "undefined") { return; }
  try { localStorage.setItem(REPORT_KEY, JSON.stringify(state)); } catch (e) {}
}

/*CORE-START*/
function buildSummary(report, state) {
  var sections = {};
  SECTION_IDS.forEach(function (id) {
    var s = (state && state.sections && state.sections[id]) || {};
    sections[id] = { status: s.status || "NOT_REVIEWED", note: s.note || "" };
  });
  var tilemap = {};
  TILE_ITEMS.forEach(function (t) {
    tilemap[t] = (state && state.tilemap && state.tilemap[t]) || "UNSURE";
  });
  var checks = {};
  if (report && report.technical_checks) {
    Object.keys(report.technical_checks).forEach(function (k) {
      var v = report.technical_checks[k];
      checks[k] = (v && v.status) ? v.status : "NOT_RUN";
    });
  }
  return {
    project: (report && report.project) || "starlight-acre",
    qa_phase: (report && report.qa_phase) || "post-promotion-visual",
    generated_at: (report && report.generated_at) || "",
    godot_version: (report && report.godot_version) || "",
    git_commit: (report && report.git_commit) || "",
    technical_checks: checks,
    sections: sections,
    tilemap_gate: tilemap
  };
}
/*CORE-END*/

function setChoice(id, status) {
  var st = loadState();
  if (!st.sections[id]) { st.sections[id] = {}; }
  st.sections[id].status = status;
  saveState(st);
  renderAll();
}

function noteChanged(id, value) {
  var st = loadState();
  if (!st.sections[id]) { st.sections[id] = {}; }
  st.sections[id].note = value;
  saveState(st);
  refreshSummary();
}

function tileChanged(item, value) {
  var st = loadState();
  st.tilemap[item] = value;
  saveState(st);
  refreshSummary();
}

function renderAll() {
  var st = loadState();
  SECTION_IDS.forEach(function (id) {
    var s = st.sections[id] || {};
    var good = document.getElementById("btn_" + id + "_LOOKS_GOOD");
    var att = document.getElementById("btn_" + id + "_NEEDS_ATTENTION");
    var note = document.getElementById("note_" + id);
    if (good) { good.className = "choice good" + (s.status === "LOOKS_GOOD" ? " active" : ""); }
    if (att) { att.className = "choice attention" + (s.status === "NEEDS_ATTENTION" ? " active" : ""); }
    if (note) {
      note.value = s.note || "";
      note.className = "note" + (s.status === "NEEDS_ATTENTION" ? " show" : "");
    }
  });
  TILE_ITEMS.forEach(function (t) {
    var sel = document.getElementById("tile_" + t);
    if (sel) { sel.value = (st.tilemap && st.tilemap[t]) || "UNSURE"; }
  });
  refreshSummary();
}

function refreshSummary() {
  var ta = document.getElementById("summary_text");
  if (!ta) { return; }
  ta.value = JSON.stringify(buildSummary(REPORT, loadState()), null, 2);
}

function init() {
  SECTION_IDS.forEach(function (id) {
    var good = document.getElementById("btn_" + id + "_LOOKS_GOOD");
    var att = document.getElementById("btn_" + id + "_NEEDS_ATTENTION");
    var note = document.getElementById("note_" + id);
    if (good) { good.addEventListener("click", function () { setChoice(id, "LOOKS_GOOD"); }); }
    if (att) { att.addEventListener("click", function () { setChoice(id, "NEEDS_ATTENTION"); }); }
    if (note) { note.addEventListener("input", function () { noteChanged(id, note.value); }); }
  });
  TILE_ITEMS.forEach(function (t) {
    var sel = document.getElementById("tile_" + t);
    if (sel) { sel.addEventListener("change", function () { tileChanged(t, sel.value); }); }
  });
  var show = document.getElementById("show_summary");
  if (show) {
    show.addEventListener("click", function () {
      refreshSummary();
      var ta = document.getElementById("summary_text");
      if (ta) {
        ta.focus();
        ta.select();
        ta.scrollIntoView({ behavior: "smooth", block: "center" });
      }
    });
  }
  var copy = document.getElementById("copy_summary");
  if (copy) {
    copy.addEventListener("click", function () {
      var ta = document.getElementById("summary_text");
      if (!ta) { return; }
      ta.focus();
      ta.select();
      var done = false;
      try { done = document.execCommand("copy"); } catch (e) { done = false; }
      copy.textContent = done ? "COPIED" : "COPY (use Command+C instead)";
      setTimeout(function () { copy.textContent = "COPY (optional)"; }, 2500);
    });
  }
  var reset = document.getElementById("reset_review");
  if (reset) {
    reset.addEventListener("click", function () {
      saveState(emptyState());
      renderAll();
    });
  }
  renderAll();
}

if (typeof document !== "undefined") { init(); }
</script>
</body>
</html>
"""


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    default_repo = os.path.dirname(os.path.dirname(here))
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--repo", default=default_repo,
                        help="repository root (default: auto-detect)")
    parser.add_argument("--output", default=None,
                        help="QA output folder (default: REPO/visual_qa_output)")
    args = parser.parse_args()
    repo = os.path.abspath(args.repo)
    out_dir = os.path.abspath(args.output or os.path.join(repo, "visual_qa_output"))
    if not os.path.isdir(out_dir):
        print("note: output folder %s does not exist yet — building a report "
              "with PENDING placeholders" % out_dir)

    checks = {name: read_check(out_dir, name) for name in CHECK_TOKENS}
    capture = read_capture(out_dir)

    commit = "unknown"
    commit_file = os.path.join(out_dir, "git_commit.txt")
    if os.path.isfile(commit_file):
        try:
            commit = open(commit_file).read().strip() or "unknown"
        except OSError:
            pass
    else:
        try:
            commit = subprocess.run(
                ["git", "-C", repo, "rev-parse", "--short", "HEAD"],
                capture_output=True, text=True, timeout=10).stdout.strip() or "unknown"
        except (OSError, subprocess.SubprocessError):
            pass

    build_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    page = build_html(out_dir, checks, capture, commit, build_time)

    target = os.path.join(out_dir, "index.html")
    try:
        os.makedirs(out_dir, exist_ok=True)
        with open(target, "w", encoding="utf-8") as f:
            f.write(page)
    except OSError as exc:
        print("ERROR: cannot write %s: %s" % (target, exc))
        return 1

    tech = dict(checks)
    tech["screenshot_capture"] = capture
    summary = ", ".join("%s %s" % (k, v["status"]) for k, v in tech.items())
    shots = sum(1 for s in capture["shots"].values() if s["present"])
    total_crops = sum(len(g["items"]) for g in CROP_GROUPS.values())
    crops = 0
    for g in CROP_GROUPS.values():
        for cid in g["items"]:
            if os.path.isfile(os.path.join(out_dir, "crops", "%s.png" % cid)):
                crops += 1
    print("report written: %s" % target)
    print("checks: %s | screenshots: %d/2 | crops: %d/%d"
          % (summary, shots, crops, total_crops))
    return 0


if __name__ == "__main__":
    sys.exit(main())
