#!/usr/bin/env python3
"""Starlight Acre — builds ratified_atlas.html, the FINAL ratified visual reference.

Shows ONLY the 29 human-ratified canonical slots. For repaired slots shows
ORIGINAL vs REPAIRED; for untouched slots the canonical asset only. Includes a
GAME SCALE board built from the ratified/repaired canonical set. No voting
controls — the decisions are final.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))

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
    ("E03_CARGO_PROPS", "Cargo Prop Sheet"),
    ("C01_WISDOM_FRUIT", "Wisdom Fruit"),
    ("E01_GREENHOUSE_TILESET", "Greenhouse Tileset (repaired)"),
    ("B01_GREENHOUSE_BACKGROUND", "Greenhouse Background (repaired)"),
]

TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Starlight Acre — Ratified Visual Canon</title>
<style>
:root{--bg:#0d1220;--panel:#151d33;--ink:#e8e4d8;--dim:#9aa3b8;--teal:#2e8b8b;--gold:#d4af37;--copper:#b87333}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:14px/1.45 system-ui,sans-serif}
header{padding:10px 14px;border-bottom:1px solid #26304d;position:sticky;top:0;background:var(--bg);z-index:5;display:flex;flex-wrap:wrap;gap:10px;align-items:center}
h1{font-size:15px;margin:0;color:var(--gold);font-weight:600}
h2{font-size:14px;margin:0 0 10px;color:var(--teal);letter-spacing:.06em}
h3{margin:0 0 6px;font-size:13px}
.bar{display:flex;gap:6px;flex-wrap:wrap;align-items:center}
button{background:#1c2742;border:1px solid #33406a;color:var(--ink);border-radius:4px;padding:4px 10px;cursor:pointer;font-size:12px}
button:hover{border-color:var(--teal)}
button.on{background:var(--teal);border-color:var(--teal);color:#06121a;font-weight:600}
main{padding:12px}
.panel{background:var(--panel);border:1px solid #26304d;border-radius:6px;padding:10px;margin-bottom:14px}
.grid{display:flex;gap:12px;flex-wrap:wrap}
.card{flex:1 1 300px;max-width:660px;background:var(--panel);border:1px solid #26304d;border-radius:6px;padding:10px}
.card.repaired{border-color:var(--copper)}
.badge{display:inline-block;font-size:10px;font-weight:700;letter-spacing:.06em;border-radius:3px;padding:1px 6px;margin-left:6px}
.badge.canon{background:var(--gold);color:#231d07}
.badge.rep{background:var(--copper);color:#1c1206}
.badge.clean{background:#234d2b;color:#bfe8c4}
.imgwrap{overflow:auto;max-height:44vh;border:1px solid #26304d;border-radius:4px;margin-top:8px;display:flex;align-items:flex-start;justify-content:center}
.checker{background:repeating-conic-gradient(#232a3d 0% 25%,#2c3550 0% 50%) 50%/16px 16px}
.imgwrap img{image-rendering:pixelated;image-rendering:crisp-edges;display:block}
.meta{font-size:11px;color:var(--dim);margin-top:6px;word-break:break-word}
.pair{display:flex;gap:8px;flex-wrap:wrap}
.pair>div{flex:1 1 260px}
.cap{font-size:10px;color:var(--dim);margin-top:2px;text-align:center}
#scaleboard .baseline{display:flex;gap:14px;align-items:flex-end;flex-wrap:wrap;border-bottom:2px solid #3b4a6b;overflow-x:auto;padding-top:8px}
.item{display:flex;flex-direction:column;align-items:center;justify-content:flex-end}
.item .lbl{font-size:10px;color:var(--dim);margin-bottom:4px;text-align:center;max-width:160px}
.item img{image-rendering:pixelated;image-rendering:crisp-edges;display:block}
.item .st{font-size:9px;margin-top:3px;color:var(--gold)}
footer{padding:8px 14px;color:var(--dim);font-size:11px;border-top:1px solid #26304d}
</style>
</head>
<body>
<header>
  <h1>RATIFIED VISUAL CANON — 29/29 human-ratified · decisions final</h1>
  <div class="bar">
    <button id="all" class="on">ALL 29</button>
    <button id="repairedOnly">REPAIRED ONLY</button>
    <button id="imgMode">IMG: canonical</button>
    <button id="zoomOut">zoom &minus;</button><span id="zoomLabel" style="font-size:12px;color:var(--dim)"></span><button id="zoomIn">zoom +</button>
    <button id="oneToOne">1:1</button>
    <button id="checker" class="on">checker</button>
  </div>
</header>
<main>
<section class="panel" id="scaleboard">
  <h2>GAME SCALE — ratified canonical set, true relative pixel scale (uniform zoom only)</h2>
  <div class="baseline" id="baseline"></div>
</section>
<div id="slots"></div>
</main>
<footer>Starlight Acre ratified canon. Repaired slots show ORIGINAL vs REPAIRED (copper badge). Canonical files for repaired slots are the repaired derivatives in visual_canon/ratified_repairs/. Offline; no external dependencies.</footer>
<script>
const DATA = __DATA_JSON__;
const SCALE = __SCALE_JSON__;
let mode = "ALL", imgMode = "canonical", zoom = 3, checker = true, szoom = 2;
function imgKey(c){
  if (imgMode === "source") return c.repaired ? "orig_source" : "source";
  return c.repaired ? "repaired_game_ready" : "game_ready";
}
function natW(c){ const k = imgKey(c); return c[k+"_w"]; }
function srcOf(c){ return c[imgKey(c)]; }
function render(){
  document.getElementById("all").classList.toggle("on", mode==="ALL");
  document.getElementById("repairedOnly").classList.toggle("on", mode==="REPAIRED");
  let html = "";
  DATA.forEach(s => {
    if (mode==="REPAIRED" && !s.repaired) return;
    const c = s;
    let inner;
    if (s.repaired){
      inner = '<div class="pair">'
        + '<div><div class="imgwrap' + (checker?' checker':'') + '"><img src="' + c.game_ready + '" style="width:' + (c.game_ready_w*zoom) + 'px"></div><div class="cap">ORIGINAL (damaged) · game_ready ' + c.game_ready_w + 'x' + c.game_ready_h + '</div></div>'
        + '<div><div class="imgwrap' + (checker?' checker':'') + '"><img src="' + c.repaired_game_ready + '" style="width:' + (c.repaired_game_ready_w*zoom) + 'px"></div><div class="cap">REPAIRED (canonical) · ' + c.repaired_game_ready_w + 'x' + c.repaired_game_ready_h + '</div></div>'
        + '</div>';
    } else {
      inner = '<div class="imgwrap' + (checker?' checker':'') + '"><img src="' + srcOf(c) + '" style="width:' + (natW(c)*zoom) + 'px"></div>';
    }
    html += '<section class="card' + (s.repaired?' repaired':'') + '">'
      + '<h3>' + s.slot_id + ' — ' + s.asset_name
      + '<span class="badge canon">' + c.cid + '</span>'
      + (s.repaired ? '<span class="badge rep">REPAIRED · ' + s.repair_action + '</span>' : '<span class="badge clean">canonical · untouched</span>')
      + '</h3>'
      + '<div class="meta">family: ' + s.family + ' · ' + c.gw + 'x' + c.gh + (s.repaired ? ' · repair: ' + s.repair_reason : ' · ratified primary, no repair needed') + '</div>'
      + inner + '</section>';
  });
  document.getElementById("slots").innerHTML = html;
  document.getElementById("imgMode").textContent = "IMG: " + imgMode;
  document.getElementById("zoomLabel").textContent = zoom + "x";
}
function renderScale(){
  document.getElementById("baseline").innerHTML = SCALE.map(s =>
    '<div class="item"><div class="lbl">' + s.label + '<br>' + s.gw + '&times;' + s.gh + '</div>'
    + '<img src="' + s.file + '" style="width:' + (s.gw*szoom) + 'px;height:' + (s.gh*szoom) + 'px">'
    + '<div class="st">' + (s.repaired ? 'repaired' : 'canonical') + '</div></div>').join("");
}
document.getElementById("all").onclick = () => { mode="ALL"; render(); };
document.getElementById("repairedOnly").onclick = () => { mode="REPAIRED"; render(); };
document.getElementById("imgMode").onclick = () => { imgMode = imgMode==="canonical" ? "source" : "canonical"; render(); };
document.getElementById("zoomIn").onclick = () => { zoom=Math.min(12,zoom+1); render(); };
document.getElementById("zoomOut").onclick = () => { zoom=Math.max(1,zoom-1); render(); };
document.getElementById("oneToOne").onclick = () => { zoom=1; render(); };
document.getElementById("checker").onclick = e => { checker=!checker; e.target.classList.toggle("on",checker); render(); };
render(); renderScale();
</script>
</body>
</html>
"""


def rel(p):
    return os.path.relpath(os.path.join(REPO, p), HERE).replace(os.sep, "/")


def main():
    canon = json.load(open(os.path.join(HERE, "RATIFIED_VISUAL_CANON.json")))
    idx = json.load(open(os.path.join(HERE, "MASTER_ASSET_INDEX.json")))
    results = json.load(open(os.path.join(HERE, "RATIFIED_REPAIR_RESULTS.json")))
    from PIL import Image
    cand = {(c["run"], c["candidate_id"]): c for c in idx["candidates"]}
    rep = {r["candidate_id"]: r for r in results["repairs"]}

    data = []
    for s in canon["slots"]:
        c = cand[(s["source_run"], s["ratified_candidate_id"])]
        r = rep.get(s["ratified_candidate_id"])
        entry = {
            "slot_id": s["slot_id"], "asset_name": next(x["asset_name"] for x in idx["candidates"]
                                                        if x["slot_id"] == s["slot_id"]),
            "family": c["asset_family"], "cid": c["candidate_id"],
            "source": rel(c["source_file"]), "game_ready": rel(c["game_ready_file"]),
            "game_ready_w": c["actual_game_dimensions"][0], "game_ready_h": c["actual_game_dimensions"][1],
            "gw": c["actual_game_dimensions"][0], "gh": c["actual_game_dimensions"][1],
            "repaired": bool(r),
            "repair_action": r["repair_action"] if r else None,
            "repair_reason": (r["technical_flags_before"] and "over-keyed dark tiles restored" if c["candidate_id"] == "E01_C002" else "cropped composition recomposed to full frame") if r else None,
        }
        if r:
            entry["orig_source"] = rel(c["source_file"])
            p = os.path.join(REPO, r["repaired_game_ready_path"])
            im = Image.open(p)
            entry["repaired_game_ready"] = rel(r["repaired_game_ready_path"])
            entry["repaired_game_ready_w"], entry["repaired_game_ready_h"] = im.size
        data.append(entry)

    scale = []
    for sid, label in SCALE_BOARD:
        s = next(x for x in canon["slots"] if x["slot_id"] == sid)
        r = rep.get(s["ratified_candidate_id"])
        if r:
            im = Image.open(os.path.join(REPO, r["repaired_game_ready_path"]))
            scale.append({"label": label, "file": rel(r["repaired_game_ready_path"]),
                          "gw": im.size[0], "gh": im.size[1], "repaired": True})
        else:
            c = cand[(s["source_run"], s["ratified_candidate_id"])]
            scale.append({"label": label, "file": rel(c["game_ready_file"]),
                          "gw": c["actual_game_dimensions"][0], "gh": c["actual_game_dimensions"][1],
                          "repaired": False})

    html = (TEMPLATE.replace("__DATA_JSON__", json.dumps(data))
                    .replace("__SCALE_JSON__", json.dumps(scale)))
    open(os.path.join(HERE, "ratified_atlas.html"), "w").write(html)
    print("ratified_atlas.html written: %d canonical slots (%d repaired), %d scale entries" % (
        len(data), sum(1 for d in data if d["repaired"]), len(scale)))


if __name__ == "__main__":
    main()
