#!/usr/bin/env python3
"""Starlight Acre — ADDITIONAL asset run: deterministic pipeline.

Processes the discovered new slots (see DISCOVERED_ASSETS.json / additional_spec.py).
Normalization/validation reuses the ORIGINAL run's battle-tested functions
(tools_build.make_game_ready, analyze_sheet_topology, island analysis) by registering
the new slot contracts into the imported dicts IN MEMORY ONLY — the original run's
files are never modified.

Idempotent: scans slots/*/*/source.png, produces game_ready.png where deterministically
valid, writes candidate.json per candidate, rebuilds ADDITIONAL_GENERATION_MANIFEST.json,
ADDITIONAL_ASSET_REQUIREMENTS.json, ADDITIONAL_PROMPTS.md and review.html.
"""
import hashlib, json, os, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
ORIG_ROOT = os.path.abspath(os.path.join(ROOT, "..", "arena_agent_asset_run"))
if ORIG_ROOT not in sys.path:
    sys.path.insert(0, ORIG_ROOT)

import run_spec  # noqa: E402
import tools_build as orig  # noqa: E402
from additional_spec import SLOTS, SLOT_ORDER, candidate_ids, full_prompt  # noqa: E402

RUN_ID = "arena_agent_additional_asset_run"
BASELINE = "97544d74d534b75472bfa99ee79439ba5752c9cf"
PROJECT = "starlight-acre"
DISCOVERY = json.load(open(os.path.join(ROOT, "DISCOVERED_ASSETS.json")))

# --- register new slot contracts into the original pipeline dicts (in memory only) ---
_NEW_SINGLE = {"A02_REACTOR_CORE", "A03_ENGINEER_DRONE", "A04_HARVESTER_DRONE",
               "A05_MAINTENANCE_DRONE", "B03_DOCKING_COLLAR", "B04_HYDROPONICS_RIG",
               "B05_ARCHIVE_STACK"}
_NEW_TOPOLOGY = {
    "U02_HUD_EXTENSION_ICONS": dict(rows=1, cols=6, cw=16, ch=16,
                                    exp=[[1, 1, 1, 1, 1, 1]]),
    "T03_TERMINAL_ACTIVE_GLOW": dict(rows=1, cols=2, cw=32, ch=64, exp=[[1, 1]], halves=True),
    "V02_HAZARD_VFX": dict(rows=1, cols=4, cw=32, ch=32, exp=[[1, 1, 1, 1]], transparent_cells=True),
    "E03_CARGO_PROPS": dict(rows=2, cols=2, cw=32, ch=32, exp=[[1, 1], [1, 1]]),
}
_MULTI_CELL = set(_NEW_TOPOLOGY)

for sid, s in SLOTS.items():
    # make_game_ready reads w/h/alpha from SLOTS; layout kept for metadata
    run_spec.SLOTS[sid] = dict(priority=s["priority"], w=s["w"], h=s["h"], alpha=s["alpha"],
                               layout=s["layout"])
orig.SINGLE_SPRITE_SLOTS |= _NEW_SINGLE
orig.SHEET_TOPOLOGY.update(_NEW_TOPOLOGY)

CAND_META = {a["asset_id"]: a for a in DISCOVERY["assets"]}


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def wjson(path, obj):
    with open(path, "w") as f:
        json.dump(obj, f, indent=2)


def process_candidate(sid, cid):
    d = os.path.join(ROOT, "slots", sid, cid)
    os.makedirs(d, exist_ok=True)
    src = os.path.join(d, "source.png")
    s = SLOTS[sid]
    meta = CAND_META[sid]
    ci = candidate_ids(sid).index(cid)
    rec = {
        "project": PROJECT, "slot_id": sid, "candidate_id": cid,
        "asset_name": meta["name"], "priority": s["priority"],
        "category": s["category"],
        "discovery_evidence": meta["evidence"],
        "evidence_paths": meta["evidence_paths"],
        "integration_target": meta["integration_target"],
        "generation_status": "not_generated", "technical_status": "FAIL",
        "source_file": None, "game_ready_file": None,
        "actual_source_width": None, "actual_source_height": None,
        "actual_game_width": None, "actual_game_height": None,
        "expected_width": s["w"], "expected_height": s["h"],
        "expected_topology": s["layout"],
        "alpha_present": None, "sha256_source": None, "sha256_game_ready": None,
        "generation_prompt": full_prompt(sid, ci),
        "technical_flags": ["NOT_GENERATED"],
        "notes": ["discovered asset awaiting generation"],
        "selected": False, "rejected": False, "live_asset_replaced": False,
    }
    if not os.path.exists(src) or os.path.getsize(src) == 0:
        wjson(os.path.join(d, "candidate.json"), rec)
        return rec
    rec["source_file"] = os.path.relpath(src, ROOT)
    rec["generation_status"] = "generated"
    rec["sha256_source"] = sha256(src)
    try:
        im = orig.Image.open(src); im.load()
    except Exception as e:
        rec["technical_flags"] = ["SOURCE_NOT_PNG", "UNDECODABLE"]
        rec["notes"] = [f"decode error: {e}"]
        wjson(os.path.join(d, "candidate.json"), rec)
        return rec
    rec["actual_source_width"], rec["actual_source_height"] = im.size
    rec["alpha_present"] = (im.mode == "RGBA" and im.getextrema()[3][0] < 255)
    flags, notes = set(), []
    if im.format != "PNG":
        flags.add("SOURCE_NOT_PNG")
    if s["alpha"] and not rec["alpha_present"]:
        flags.add("NO_ALPHA")
    try:
        gr, gflags, gnotes = orig.make_game_ready(sid, src)
        gp = os.path.join(d, "game_ready.png")
        gr.save(gp, "PNG", optimize=True)
        rec["game_ready_file"] = os.path.relpath(gp, ROOT)
        rec["sha256_game_ready"] = sha256(gp)
        gim = orig.Image.open(gp); gim.load()
        rec["actual_game_width"], rec["actual_game_height"] = gim.size
        rec["alpha_present"] = rec["alpha_present"] or (gim.mode == "RGBA" and gim.getextrema()[3][0] < 255)
        flags |= gflags
        notes += gnotes
        if (rec["actual_game_width"], rec["actual_game_height"]) != (s["w"], s["h"]):
            flags.add("WRONG_DIMENSIONS")
        if sid in orig.SHEET_TOPOLOGY:
            try:
                tflags, tnotes = orig.analyze_sheet_topology(sid, gp, src)
                flags |= tflags
                notes += tnotes
            except Exception as e:
                flags.add("TOPOLOGY_ANALYSIS_FAILED")
                notes.append(f"sheet topology analysis error: {e}")
        if sid in _MULTI_CELL:
            flags.add("FRAME_LAYOUT_UNCERTAIN")
            notes.append("multi-cell sheet: generated source is a single raster; per-cell topology "
                         "measured deterministically where possible; review before slicing")
    except Exception as e:
        flags.add("NORMALIZATION_FAILED")
        notes.append(f"normalization error: {e}")
    rec["technical_flags"] = sorted(flags)
    rec["notes"] = notes
    hard = {"NORMALIZATION_FAILED", "GENERATION_FAILED"} & flags
    if hard or rec["game_ready_file"] is None:
        rec["technical_status"] = "FAIL"
    elif flags - {"BACKGROUND_REMOVED", "CONVERSION_REQUIRED"}:
        rec["technical_status"] = "PASS_WITH_FLAGS"
    else:
        rec["technical_status"] = "PASS"
    wjson(os.path.join(d, "candidate.json"), rec)
    return rec


def build_requirements(recs):
    req = {
        "project": PROJECT, "run_id": RUN_ID, "created": "2026-09-20",
        "engine": "Godot 4.7.x", "view": "2D side-view",
        "relationship": ("additional discovered slots only; no overlap with the 18 established "
                         "families of arena_agent_asset_run / arena_agent_alt_asset_run"),
        "style_lock": "assets/docs/style_guide.md palette anchors; same identity block as prior runs",
        "dimension_authority": ("derived from current scenes/resources where possible; NEWLY PROPOSED "
                               "dimensions are explicitly marked in DISCOVERED_ASSETS.json"),
        "asset_slots": {},
    }
    for sid in SLOT_ORDER:
        s = SLOTS[sid]
        m = CAND_META[sid]
        gen = [r for r in recs if r["slot_id"] == sid and r["generation_status"] == "generated"]
        req["asset_slots"][sid] = {
            "asset_name": m["name"], "priority": s["priority"], "category": s["category"],
            "target_width": s["w"], "target_height": s["h"], "alpha_expected": s["alpha"],
            "frame_layout": s["layout"], "candidate_count": s["count"],
            "integration_target": m["integration_target"],
            "dimensions_note": m["expected_dimensions"],
            "generated_count": len(gen),
        }
    wjson(os.path.join(ROOT, "ADDITIONAL_ASSET_REQUIREMENTS.json"), req)


def build_prompts_md(recs):
    lines = [
        "# Starlight Acre — ADDITIONAL asset run prompts",
        "",
        "Discovered new slots only (see DISCOVERED_ASSETS.json for evidence). Each prompt =",
        "the shared Starlight Acre identity block + a hardened slot contract + a variant design.",
        "",
    ]
    for sid in SLOT_ORDER:
        s = SLOTS[sid]
        m = CAND_META[sid]
        lines.append(f"## {sid} — {m['name']} — Priority {s['priority']} — target {s['w']}x{s['h']}")
        lines.append("")
        lines.append(f"Evidence: {m['evidence']}")
        lines.append("")
        for r in recs:
            if r["slot_id"] != sid:
                continue
            lines.append(f"### {r['candidate_id']} [{r['generation_status']}]")
            lines.append("")
            lines.append("```")
            lines.append(r["generation_prompt"])
            lines.append("```")
            lines.append("")
    open(os.path.join(ROOT, "ADDITIONAL_PROMPTS.md"), "w").write("\n".join(lines))


REVIEW_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Starlight Acre — Additional Asset Run Review</title>
<style>
:root{--bg:#0d1220;--panel:#151d33;--ink:#e8e4d8;--dim:#9aa3b8;--teal:#2e8b8b;--gold:#d4af37;--bad:#c0504d;--keep:#6fbf73}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:14px/1.45 system-ui,sans-serif}
header{padding:10px 14px;border-bottom:1px solid #26304d;display:flex;flex-wrap:wrap;gap:10px;align-items:center}
h1{font-size:15px;margin:0;color:var(--gold);font-weight:600}
.bar{display:flex;gap:6px;flex-wrap:wrap;align-items:center}
button,select{background:#1c2742;border:1px solid #33406a;color:var(--ink);border-radius:4px;padding:4px 10px;cursor:pointer;font-size:12px}
button:hover{border-color:var(--teal)}
button.on{background:var(--teal);border-color:var(--teal);color:#06121a;font-weight:600}
button.k-KEEP.on{background:var(--keep);border-color:var(--keep)}
button.k-MAYBE.on{background:var(--gold);border-color:var(--gold)}
button.k-REJECT.on{background:var(--bad);border-color:var(--bad)}
.nav{display:flex;gap:6px;align-items:center;color:var(--dim);font-size:12px}
main{display:flex;gap:12px;padding:12px;flex-wrap:wrap;align-items:flex-start}
.panel{background:var(--panel);border:1px solid #26304d;border-radius:6px;padding:10px}
.viewpanel{flex:1 1 460px}
.imgwrap{overflow:auto;max-height:56vh;border:1px solid #26304d;border-radius:4px;display:flex;align-items:flex-start;justify-content:center;background:#0a0e1a}
.checker{background:repeating-conic-gradient(#232a3d 0% 25%,#2c3550 0% 50%) 50%/16px 16px}
.imgwrap img{image-rendering:pixelated;image-rendering:crisp-edges;display:block}
.meta{font-size:12px;color:var(--dim);margin-top:8px;word-break:break-word}
.meta b{color:var(--ink)}
.ev{border-left:3px solid var(--teal);padding:4px 8px;margin-top:8px;background:#111a30;border-radius:3px;font-size:12px;color:var(--dim)}
.flags span{display:inline-block;background:#1c2742;border:1px solid #33406a;border-radius:3px;padding:0 5px;margin:2px 3px 0 0;font-size:11px}
.status-PASS{color:#6fbf73}.status-PASS_WITH_FLAGS{color:var(--gold)}.status-FAIL{color:var(--bad)}.status-not_generated{color:var(--dim)}
details{margin-top:8px}summary{cursor:pointer;color:var(--teal);font-size:12px}
pre{white-space:pre-wrap;font-size:11px;color:var(--dim);max-height:200px;overflow:auto}
.slotlist{width:250px;max-height:70vh;overflow:auto}
.slotlist button{display:block;width:100%;text-align:left;margin-bottom:4px}
.slotlist button.cur{border-color:var(--gold);color:var(--gold)}
footer{padding:8px 14px;color:var(--dim);font-size:11px;border-top:1px solid #26304d}
.missing{color:var(--dim);font-style:italic;padding:24px;text-align:center}
</style>
</head>
<body>
<header>
  <h1>ADDITIONAL ASSET RUN — discovered slots</h1>
  <div class="nav"><button id="prev">&larr;</button><span id="pos"></span><button id="next">&rarr;</button></div>
  <div class="bar">
    <select id="filter"></select>
    <button id="imgMode">IMG: source</button>
    <button id="zoomOut">zoom &minus;</button><span id="zoomLabel"></span><button id="zoomIn">zoom +</button>
    <button id="oneToOne">1:1</button>
    <button id="checker" class="on">checker</button>
  </div>
  <div class="bar" id="decisions">
    <button class="k-KEEP" data-k="KEEP" title="K">KEEP</button>
    <button class="k-MAYBE" data-k="MAYBE" title="M">MAYBE</button>
    <button class="k-REJECT" data-k="REJECT" title="R">REJECT</button>
    <button class="k-UNSORTED" data-k="UNSORTED" title="U">UNSORTED</button>
    <button id="export">EXPORT SELECTIONS</button>
  </div>
</header>
<main>
  <aside class="panel slotlist" id="slotlist"></aside>
  <section class="panel viewpanel" id="view"></section>
</main>
<footer>Decisions persist in localStorage (<code>sa_additional_review_v1</code>) and are never automatic.
Export writes <code>additional_selections.json</code>. Keys: K/M/R/U, &larr;/&rarr; navigate slots, G toggle image, C checker, 1 one-to-one.</footer>
<script>
const DATA = __DATA_JSON__;
const LS_KEY = "sa_additional_review_v1";
let state = JSON.parse(localStorage.getItem(LS_KEY) || "{}");
let si = 0, filter = "ALL", imgMode = "source", zoom = 3, checker = true;
const FILTERS = ["ALL","UNSORTED","KEEP","MAYBE","REJECT","PASS","PASS_WITH_FLAGS","FAIL","PRIORITY A","PRIORITY B","PRIORITY C"];
function save(){ localStorage.setItem(LS_KEY, JSON.stringify(state)); }
function dec(c){ return state[c.candidate_id] || "UNSORTED"; }
function passFilter(c){
  if (filter === "ALL") return true;
  if (filter.startsWith("PRIORITY ")) return c.priority === filter.split(" ")[1];
  if (["UNSORTED","KEEP","MAYBE","REJECT"].includes(filter)) return dec(c) === filter;
  return c.status === filter;
}
function render(){
  const fs = document.getElementById("filter");
  [...fs.options].forEach(o => o.selected = o.value === filter);
  const list = document.getElementById("slotlist");
  list.innerHTML = "";
  DATA.forEach((s, i) => {
    const vis = s.candidates.filter(passFilter);
    const b = document.createElement("button");
    b.textContent = s.slot_id + " (" + vis.length + "/" + s.candidates.length + ")";
    b.className = i === si ? "cur" : "";
    b.onclick = () => { si = i; render(); };
    list.appendChild(b);
  });
  const s = DATA[si];
  const vis = s.candidates.filter(passFilter);
  document.getElementById("pos").textContent = (si+1) + "/" + DATA.length;
  let html = '<h2 style="margin:0 0 4px;font-size:14px;color:var(--gold)">' + s.slot_id + " — " + s.name +
    ' <span style="color:var(--dim);font-weight:400">priority ' + s.priority + " · " + s.category + " · target " + s.w + "x" + s.h + '</span></h2>' +
    '<div class="ev"><b>Evidence:</b> ' + s.evidence + '<br><b>Integration target:</b> ' + s.integration_target + '</div>' +
    '<div style="display:flex;gap:12px;flex-wrap:wrap;margin-top:10px">';
  const show = vis.length ? vis : s.candidates;
  show.forEach(c => {
    const d = dec(c);
    const img = !c.generated ? '<div class="missing">not generated yet</div>' :
      '<img src="' + (imgMode === "source" ? c.source : c.game_ready) + '" style="width:' +
      ((imgMode === "source" ? c.sw : c.gw) * zoom) + 'px" alt="">';
    html += '<div style="flex:1 1 300px">' +
      '<div style="font-size:12px;color:var(--dim)"><b style="color:var(--ink)">' + c.candidate_id +
      '</b> · <span class="status-' + c.status + '">' + c.status + '</span></div>' +
      '<div class="imgwrap' + (checker ? ' checker' : '') + '">' + img + '</div>' +
      '<div class="meta">source ' + c.sw + 'x' + c.sh + ' → game_ready ' + c.gw + 'x' + c.gh +
      ' (target ' + c.w + 'x' + c.h + ') · alpha: ' + (c.alpha ? 'yes' : 'no') + '</div>' +
      '<div class="meta flags"><b>flags:</b><br><span>' + (c.flags.length ? c.flags.join('</span><span>') : 'none') + '</span></div>' +
      '<div class="meta" data-cid="' + c.candidate_id + '"><b>decision:</b> ' + d + '</div>' +
      '<details><summary>prompt</summary><pre>' + (c.prompt || '').replace(/</g,'&lt;') + '</pre></details></div>';
  });
  html += '</div>';
  document.getElementById("view").innerHTML = html;
  document.querySelectorAll("#decisions [data-k]").forEach(b => b.classList.toggle("on", false));
  document.getElementById("imgMode").textContent = "IMG: " + imgMode;
  document.getElementById("zoomLabel").textContent = zoom + "x";
}
function decide(k){
  const s = DATA[si]; const vis = s.candidates.filter(passFilter);
  const targets = vis.length === 1 ? vis : s.candidates.filter(c => dec(c) !== "UNSORTED");
  (targets.length ? targets : s.candidates).forEach(c => { state[c.candidate_id] = k; });
  save(); render();
}
function cycle(cid){
  const order = ["UNSORTED","KEEP","MAYBE","REJECT"];
  state[cid] = order[(order.indexOf(dec({candidate_id:cid})) + 1) % order.length];
  save(); render();
}
document.addEventListener("click", e => {
  const m = e.target.closest(".meta[data-cid]");
  if (m) cycle(m.dataset.cid);
});
const fs = document.getElementById("filter");
FILTERS.forEach(f => { const o = document.createElement("option"); o.value = o.textContent = f; fs.appendChild(o); });
fs.onchange = () => { filter = fs.value; render(); };
document.getElementById("prev").onclick = () => { si = (si - 1 + DATA.length) % DATA.length; render(); };
document.getElementById("next").onclick = () => { si = (si + 1) % DATA.length; render(); };
document.getElementById("imgMode").onclick = () => { imgMode = imgMode === "source" ? "game_ready" : "source"; render(); };
document.getElementById("zoomIn").onclick = () => { zoom = Math.min(12, zoom + 1); render(); };
document.getElementById("zoomOut").onclick = () => { zoom = Math.max(1, zoom - 1); render(); };
document.getElementById("oneToOne").onclick = () => { zoom = 1; render(); };
document.getElementById("checker").onclick = e => { checker = !checker; e.target.classList.toggle("on", checker); render(); };
document.querySelectorAll("#decisions [data-k]").forEach(b => b.onclick = () => decide(b.dataset.k));
document.getElementById("export").onclick = () => {
  const out = { project: "starlight-acre", run_id: "arena_agent_additional_asset_run",
    exported: new Date().toISOString().slice(0,10), selections: DATA.flatMap(s => s.candidates.map(c => ({
      slot_id: s.slot_id, candidate_id: c.candidate_id, asset_name: s.name,
      decision: state[c.candidate_id] || "UNSORTED", technical_status: c.status }))) };
  const a = document.createElement("a");
  a.href = URL.createObjectURL(new Blob([JSON.stringify(out, null, 2)], {type:"application/json"}));
  a.download = "additional_selections.json"; a.click();
};
document.addEventListener("keydown", e => {
  if (e.target.tagName === "INPUT" || e.target.tagName === "TEXTAREA") return;
  const k = e.key.toLowerCase();
  if (k === "k") decide("KEEP"); else if (k === "m") decide("MAYBE");
  else if (k === "r") decide("REJECT"); else if (k === "u") decide("UNSORTED");
  else if (e.key === "ArrowLeft") { si = (si - 1 + DATA.length) % DATA.length; render(); }
  else if (e.key === "ArrowRight") { si = (si + 1) % DATA.length; render(); }
  else if (k === "g") { imgMode = imgMode === "source" ? "game_ready" : "source"; render(); }
  else if (k === "c") { checker = !checker; document.getElementById("checker").classList.toggle("on", checker); render(); }
  else if (k === "1") { zoom = 1; render(); }
});
render();
</script>
</body>
</html>
"""


def build_review(recs):
    data = []
    for sid in SLOT_ORDER:
        s = SLOTS[sid]
        m = CAND_META[sid]
        cands = []
        for r in recs:
            if r["slot_id"] != sid:
                continue
            cands.append({
                "candidate_id": r["candidate_id"], "status": r["technical_status"],
                "flags": r["technical_flags"], "source": r["source_file"],
                "game_ready": r["game_ready_file"],
                "sw": r["actual_source_width"], "sh": r["actual_source_height"],
                "gw": r["actual_game_width"], "gh": r["actual_game_height"],
                "w": r["expected_width"], "h": r["expected_height"],
                "alpha": r.get("alpha_present"), "prompt": r.get("generation_prompt"),
                "generated": r["generation_status"] == "generated",
            })
        data.append({
            "slot_id": sid, "name": m["name"], "priority": s["priority"],
            "category": s["category"], "w": s["w"], "h": s["h"],
            "evidence": m["evidence"], "integration_target": m["integration_target"],
            "candidates": cands,
        })
    html = REVIEW_TEMPLATE.replace("__DATA_JSON__", json.dumps(data))
    open(os.path.join(ROOT, "review.html"), "w").write(html)
    return len(data)


def main():
    recs = []
    for sid in SLOT_ORDER:
        for cid in candidate_ids(sid):
            recs.append(process_candidate(sid, cid))
    gen = [r for r in recs if r["generation_status"] == "generated"]
    val = [r for r in gen if r["actual_game_width"]]
    by_status = {}
    for r in gen:
        by_status[r["technical_status"]] = by_status.get(r["technical_status"], 0) + 1
    manifest = {
        "project": PROJECT, "run_id": RUN_ID,
        "repository_commit_baseline": BASELINE,
        "discovery_file": "DISCOVERED_ASSETS.json",
        "target_candidate_count": len(recs),
        "generated_count": len(gen), "validated_count": len(val),
        "failed_count": len([r for r in gen if r["technical_status"] == "FAIL"]),
        "technical_status_counts": by_status,
        "slots": SLOT_ORDER,
        "candidates": [{
            "slot_id": r["slot_id"], "candidate_id": r["candidate_id"],
            "asset_name": r["asset_name"], "priority": r["priority"],
            "category": r["category"],
            "generation_status": r["generation_status"], "technical_status": r["technical_status"],
            "source_file": r["source_file"], "game_ready_file": r["game_ready_file"],
            "actual_source_width": r["actual_source_width"], "actual_source_height": r["actual_source_height"],
            "actual_game_width": r["actual_game_width"], "actual_game_height": r["actual_game_height"],
            "expected_width": r["expected_width"], "expected_height": r["expected_height"],
            "alpha_present": r["alpha_present"],
            "sha256_source": r["sha256_source"], "sha256_game_ready": r["sha256_game_ready"],
            "technical_flags": r["technical_flags"],
            "discovery_evidence": r["discovery_evidence"],
            "integration_target": r["integration_target"],
        } for r in recs],
    }
    wjson(os.path.join(ROOT, "ADDITIONAL_GENERATION_MANIFEST.json"), manifest)
    build_requirements(recs)
    build_prompts_md(recs)
    n = build_review(recs)
    print(f"additional candidates={len(recs)} generated={len(gen)} validated={len(val)} "
          f"failed={manifest['failed_count']} status={by_status}")
    print(f"review.html rebuilt with {n} discovered slots")


if __name__ == "__main__":
    main()
