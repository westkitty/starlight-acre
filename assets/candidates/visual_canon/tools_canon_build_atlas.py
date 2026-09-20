#!/usr/bin/env python3
"""Starlight Acre — visual canon reference atlas builder.

Reads MASTER_ASSET_INDEX.json + VISUAL_CANON_SELECTIONS.json and emits
reference_atlas.html: a self-contained offline visual-language reference showing
ONLY selected PRIMARY and SECONDARY references, organized by family, plus a
GAME SCALE board that places representative references together at true relative
pixel scale on a shared baseline (uniform zoom only — never per-asset rescaling).
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))

SCALE_BOARD = [
    ("P01_PLAYER_SHEET", "Player (sheet, frames 32x48)"),
    ("A01_GARDENER_DRONE", "Gardener Drone"),
    ("A03_ENGINEER_DRONE", "Engineer Drone"),
    ("A04_HARVESTER_DRONE", "Harvester Drone"),
    ("A05_MAINTENANCE_DRONE", "Maintenance Drone"),
    ("D01_DEXTER_VENDOR", "Dexter (vendor)"),
    ("W01_SECTOR_DOOR", "Sector Door"),
    ("T01_REPAIR_REPLENISH_TERMINALS", "Repair/Replenish Terminals"),
    ("T02_RESEARCH_TERMINAL", "Research Terminal"),
    ("A02_REACTOR_CORE", "Reactor Core"),
    ("B04_HYDROPONICS_RIG", "Hydroponics Rig"),
    ("B05_ARCHIVE_STACK", "Archive Stack"),
    ("E03_CARGO_PROPS", "Cargo Props (2x2 sheet)"),
    ("C01_WISDOM_FRUIT", "Wisdom Fruit (4-state strip)"),
]

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Starlight Acre — Visual Canon Reference Atlas</title>
<style>
:root{--bg:#0d1220;--panel:#151d33;--ink:#e8e4d8;--dim:#9aa3b8;--teal:#2e8b8b;--gold:#d4af37;--copper:#b87333}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:14px/1.45 system-ui,sans-serif}
header{padding:10px 14px;border-bottom:1px solid #26304d;position:sticky;top:0;background:var(--bg);z-index:5;display:flex;flex-wrap:wrap;gap:10px;align-items:center}
h1{font-size:15px;margin:0;color:var(--gold);font-weight:600}
h2{font-size:14px;margin:0 0 10px;color:var(--teal);letter-spacing:.06em}
.bar{display:flex;gap:6px;flex-wrap:wrap;align-items:center}
button,select{background:#1c2742;border:1px solid #33406a;color:var(--ink);border-radius:4px;padding:4px 10px;cursor:pointer;font-size:12px}
button:hover,select:hover{border-color:var(--teal)}
button.on{background:var(--teal);border-color:var(--teal);color:#06121a;font-weight:600}
main{padding:12px}
.family{margin-bottom:18px}
.grid{display:flex;gap:12px;flex-wrap:wrap}
.card{flex:1 1 300px;max-width:640px;background:var(--panel);border:1px solid #26304d;border-radius:6px;padding:10px}
.badge{display:inline-block;font-size:10px;font-weight:700;letter-spacing:.08em;border-radius:3px;padding:1px 6px;margin-left:6px;vertical-align:middle}
.badge.PRIMARY{background:var(--gold);color:#231d07}
.badge.SECONDARY{background:#33406a;color:var(--ink)}
.card h3{margin:0;font-size:13px}
.card .cid{color:var(--dim);font-size:11px}
.imgwrap{overflow:auto;max-height:46vh;border:1px solid #26304d;border-radius:4px;margin-top:8px;display:flex;align-items:flex-start;justify-content:center}
.checker{background:repeating-conic-gradient(#232a3d 0% 25%,#2c3550 0% 50%) 50%/16px 16px}
.imgwrap img{image-rendering:pixelated;image-rendering:crisp-edges;display:block}
.meta{font-size:11px;color:var(--dim);margin-top:6px}
.traits{margin:6px 0 0;padding-left:16px;font-size:11px;color:var(--dim)}
.traits li{margin:2px 0}
#scaleboard{background:var(--panel);border:1px solid #26304d;border-radius:6px;padding:12px;margin-bottom:18px}
.baseline{display:flex;gap:14px;align-items:flex-end;flex-wrap:wrap;border-bottom:2px solid #3b4a6b;padding-bottom:0;overflow-x:auto}
.item{display:flex;flex-direction:column;align-items:center;justify-content:flex-end}
.item .lbl{font-size:10px;color:var(--dim);margin-bottom:4px;text-align:center;max-width:140px}
.item img{image-rendering:pixelated;image-rendering:crisp-edges;display:block}
footer{padding:8px 14px;color:var(--dim);font-size:11px;border-top:1px solid #26304d}
.missing{color:var(--dim);font-style:italic}
</style>
</head>
<body>
<header>
  <h1>VISUAL CANON — REFERENCE ATLAS</h1>
  <div class="bar">
    <button id="modeAll" class="on">ALL</button>
    <button id="modePrimary">PRIMARY ONLY</button>
    <button id="modeSecondary">SECONDARY ONLY</button>
    <select id="famfilter"></select>
    <button id="imgMode">IMG: game_ready</button>
    <button id="zoomOut">zoom &minus;</button><span id="zoomLabel" style="font-size:12px;color:var(--dim)"></span><button id="zoomIn">zoom +</button>
    <button id="oneToOne">1:1</button>
    <button id="checker" class="on">checker</button>
  </div>
</header>
<main>
<section id="scaleboard">
  <h2>GAME SCALE — shared baseline, true relative pixel scale (uniform zoom only, no per-asset rescaling)</h2>
  <div class="baseline" id="baseline"></div>
  <div class="meta" style="margin-top:8px">Representative PRIMARY references bottom-aligned. Player shown as full sheet (frames 32x48). __SCALE_NOTES__</div>
</section>
<div id="families"></div>
</main>
<footer>Starlight Acre visual canon — selected PRIMARY/SECONDARY references only (see VISUAL_CANON_SELECTIONS.json).
This is the project's visual-language reference, not a candidate review interface. Offline; no external dependencies.</footer>
<script>
const DATA = __DATA_JSON__;
const SCALE = __SCALE_JSON__;
let mode = "ALL", fam = "ALL", imgMode = "game_ready", zoom = 3, checker = true, szoom = 2;
function img(w){ return imgMode === "source" ? w.source : w.game_ready; }
function natW(w){ return imgMode === "source" ? w.sw : w.gw; }
function cardHtml(w){
  return '<div class="card" data-fam="'+w.family+'" data-role="'+w.role+'">'
    + '<h3>'+w.asset_name+'<span class="badge '+w.role+'">'+w.role+'</span></h3>'
    + '<div class="cid">'+w.candidate_id+' · '+w.run+' · '+w.family+'</div>'
    + '<div class="imgwrap'+(checker?' checker':'')+'"><img src="'+img(w)+'" style="width:'+(natW(w)*zoom)+'px" alt=""></div>'
    + '<div class="meta">game_ready '+w.gw+'x'+w.gh+' (source '+w.sw+'x'+w.sh+') · '+w.role.toLowerCase()+' style reference</div>'
    + '<ul class="traits">'+w.traits.map(t=>'<li>'+t+'</li>').join('')+'</ul></div>';
}
function render(){
  document.getElementById("modeAll").classList.toggle("on", mode==="ALL");
  document.getElementById("modePrimary").classList.toggle("on", mode==="PRIMARY");
  document.getElementById("modeSecondary").classList.toggle("on", mode==="SECONDARY");
  const host = document.getElementById("families");
  const fams = {};
  DATA.forEach(w => { if (mode!=="ALL" && w.role!==mode) return; if (fam!=="ALL" && w.family!==fam) return;
    (fams[w.family] = fams[w.family] || []).push(w); });
  let html = "";
  Object.keys(fams).sort().forEach(f => {
    html += '<section class="family"><h2>'+f+' — '+fams[f].length+' reference'+(fams[f].length>1?'s':'')+'</h2><div class="grid">'
          + fams[f].map(cardHtml).join("") + '</div></section>';
  });
  host.innerHTML = html || '<div class="missing">no references match this filter</div>';
  document.getElementById("imgMode").textContent = "IMG: " + imgMode;
  document.getElementById("zoomLabel").textContent = zoom + "x";
}
function renderScale(){
  const b = document.getElementById("baseline");
  b.innerHTML = SCALE.map(s => '<div class="item"><div class="lbl">'+s.label+'<br>'+s.gw+'&times;'+s.gh+'</div>'
    + '<img src="'+s.game_ready+'" style="width:'+(s.gw*szoom)+'px;height:'+(s.gh*szoom)+'px" alt=""></div>').join("");
}
document.getElementById("modeAll").onclick = () => { mode="ALL"; render(); };
document.getElementById("modePrimary").onclick = () => { mode="PRIMARY"; render(); };
document.getElementById("modeSecondary").onclick = () => { mode="SECONDARY"; render(); };
const ff = document.getElementById("famfilter");
["ALL"].concat([...new Set(DATA.map(w=>w.family))].sort()).forEach(f => { const o=document.createElement("option"); o.value=o.textContent=f; ff.appendChild(o); });
ff.onchange = () => { fam = ff.value; render(); };
document.getElementById("imgMode").onclick = () => { imgMode = imgMode==="source" ? "game_ready" : "source"; render(); };
document.getElementById("zoomIn").onclick = () => { zoom = Math.min(12, zoom+1); render(); };
document.getElementById("zoomOut").onclick = () => { zoom = Math.max(1, zoom-1); render(); };
document.getElementById("oneToOne").onclick = () => { zoom = 1; render(); };
document.getElementById("checker").onclick = e => { checker=!checker; e.target.classList.toggle("on",checker); render(); };
render(); renderScale();
</script>
</body>
</html>
"""

SCALE_NOTES = ("Cohesion note: Dexter's 64x64 reference canvas vs the player's 32x48 frame — display-scale Dexter "
               "down at integration so the dog reads clearly smaller than the player (logged in the continuity report).")


def main():
    idx = json.load(open(os.path.join(HERE, "MASTER_ASSET_INDEX.json")))
    sel = json.load(open(os.path.join(HERE, "VISUAL_CANON_SELECTIONS.json")))
    by_id = {(c["run"], c["candidate_id"]): c for c in idx["candidates"]}

    def rel(p):
        return os.path.relpath(os.path.join(os.path.dirname(HERE), "..", "..", "..", p), HERE).replace(os.sep, "/") \
            if False else os.path.relpath(os.path.join("/home/user/starlight-acre", p), HERE).replace(os.sep, "/")

    data = []
    for s in sel["selections"]:
        for role, key in (("PRIMARY", "primary_reference"), ("SECONDARY", "secondary_reference")):
            r = s.get(key)
            if not r:
                continue
            c = by_id[(r["run"], r["candidate_id"])]
            data.append({
                "family": s["asset_family"], "slot_id": s["slot_id"],
                "candidate_id": r["candidate_id"], "run": r["run"],
                "asset_name": s["asset_name"], "role": role,
                "source": rel(c["source_file"]), "game_ready": rel(c["game_ready_file"]),
                "sw": c["source_dimensions"][0], "sh": c["source_dimensions"][1],
                "gw": c["actual_game_dimensions"][0], "gh": c["actual_game_dimensions"][1],
                "traits": c["art_direction_observations"][:5],
            })

    primaries = {s["slot_id"]: s["primary_reference"] for s in sel["selections"]}
    scale = []
    for slot, label in SCALE_BOARD:
        r = primaries.get(slot)
        if not r:
            continue
        c = by_id[(r["run"], r["candidate_id"])]
        scale.append({"label": label, "candidate_id": r["candidate_id"],
                      "game_ready": rel(c["game_ready_file"]),
                      "gw": c["actual_game_dimensions"][0], "gh": c["actual_game_dimensions"][1]})

    html = (TEMPLATE.replace("__DATA_JSON__", json.dumps(data))
                    .replace("__SCALE_JSON__", json.dumps(scale))
                    .replace("__SCALE_NOTES__", SCALE_NOTES))
    out = os.path.join(HERE, "reference_atlas.html")
    open(out, "w").write(html)
    print("reference_atlas.html written: %d reference cards (%d primary, %d secondary), %d scale-board entries" % (
        len(data), sum(1 for d in data if d["role"] == "PRIMARY"),
        sum(1 for d in data if d["role"] == "SECONDARY"), len(scale)))


if __name__ == "__main__":
    main()
