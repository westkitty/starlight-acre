#!/usr/bin/env python3
"""Starlight Acre — ALTERNATE (challenger) asset run: deterministic pipeline.

One-to-one: every original candidate in ../arena_agent_asset_run gets exactly one
alternate challenger (A01_C001 -> A01_ALT_C001 ...). Normalization/validation reuses
the ORIGINAL run's deterministic functions (tools_build.make_game_ready,
analyze_sheet_topology) so both libraries are processed under identical rules.

Idempotent: scans slots/*/*/source.png, produces game_ready.png where deterministically
valid, writes candidate.json per alternate, rebuilds ALT_GENERATION_MANIFEST.json,
ALT_PROMPTS.md, ALT_ASSET_REQUIREMENTS.json and review.html.

Rules:
  * original run and live game assets are NEVER touched (read-only imports)
  * sources are never modified
  * flags are honest; technical status is never an aesthetic judgment
"""
import hashlib, json, os, sys

ALT_ROOT = os.path.dirname(os.path.abspath(__file__))
ORIG_ROOT = os.path.abspath(os.path.join(ALT_ROOT, "..", "arena_agent_asset_run"))
if ORIG_ROOT not in sys.path:
    sys.path.insert(0, ORIG_ROOT)

from run_spec import SLOTS, candidate_ids, PROJECT  # noqa: E402
import tools_build as orig  # noqa: E402
from alt_spec import ALT_SPECS  # noqa: E402

SLOT_ORDER = list(SLOTS.keys())

RUN_ID = "arena_agent_alt_asset_run"
BASELINE = "97544d74d534b75472bfa99ee79439ba5752c9cf"


def alt_id_for(orig_cid):
    short, num = orig_cid.split("_")
    return f"{short}_ALT_{num}"


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def wjson(path, obj):
    with open(path, "w") as f:
        json.dump(obj, f, indent=2)


def process_candidate(sid, orig_cid, acid):
    d = os.path.join(ALT_ROOT, "slots", sid, acid)
    os.makedirs(d, exist_ok=True)
    src = os.path.join(d, "source.png")
    s = SLOTS[sid]
    spec = ALT_SPECS.get(acid, {})
    rec = {
        "project": PROJECT, "slot_id": sid,
        "source_candidate_id": orig_cid, "alternate_candidate_id": acid,
        "priority": s["priority"],
        "generation_status": "not_generated", "technical_status": "FAIL",
        "source_file": None, "game_ready_file": None,
        "actual_source_width": None, "actual_source_height": None,
        "actual_game_width": None, "actual_game_height": None,
        "expected_width": s["w"], "expected_height": s["h"],
        "expected_frame_layout": s["layout"],
        "alpha_present": None,
        "sha256_source": None, "sha256_game_ready": None,
        "generation_prompt": spec.get("prompt"),
        "challenger_axes": spec.get("axes", []),
        "technical_flags": ["NOT_GENERATED"],
        "notes": ["alternate not yet generated" if not spec.get("prompt")
                  else "challenger prompt composed; awaiting generation"],
        "selected": False, "rejected": False, "live_asset_replaced": False,
    }
    if not os.path.exists(src) or os.path.getsize(src) == 0:
        wjson(os.path.join(d, "candidate.json"), rec)
        return rec
    rec["source_file"] = os.path.relpath(src, ALT_ROOT)
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
        rec["game_ready_file"] = os.path.relpath(gp, ALT_ROOT)
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


def build_requirements():
    req = json.load(open(os.path.join(ORIG_ROOT, "ASSET_REQUIREMENTS.json")))
    alt_req = dict(req)
    alt_req["run_id"] = RUN_ID
    alt_req["original_run_path"] = "../arena_agent_asset_run"
    alt_req["relationship"] = ("alternate challenger run: one materially different alternate per "
                               "original candidate; integration contracts identical to the original run")
    alt_req["target_alternate_count"] = 44
    wjson(os.path.join(ALT_ROOT, "ALT_ASSET_REQUIREMENTS.json"), alt_req)


def build_prompts_md(recs):
    lines = [
        "# Starlight Acre — ALTERNATE (challenger) run prompts",
        "",
        "One alternate per original candidate. Each prompt = the run's shared identity block",
        "+ the slot contract (all technical/semantic requirements preserved) + a CHALLENGER",
        "DESIGN paragraph exploring materially different design axes. Anti-failure directives",
        "from the original run's known defects are baked into every slot contract.",
        "",
    ]
    for r in recs:
        lines.append(f"## {r['slot_id']} — challenges {r['source_candidate_id']}")
        lines.append("")
        lines.append(f"### {r['alternate_candidate_id']} [{r['generation_status']}]")
        lines.append("")
        if r.get("challenger_axes"):
            lines.append("Challenger axes:")
            for a in r["challenger_axes"]:
                lines.append(f"- {a}")
            lines.append("")
        if r.get("generation_prompt"):
            lines.append("```")
            lines.append(r["generation_prompt"])
            lines.append("```")
        else:
            lines.append("Challenger prompt not yet composed (pending generation turn).")
        lines.append("")
    open(os.path.join(ALT_ROOT, "ALT_PROMPTS.md"), "w").write("\n".join(lines))


REVIEW_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Starlight Acre — ALT Run Review: Champion vs Challenger</title>
<style>
:root{--bg:#0d1220;--panel:#151d33;--ink:#e8e4d8;--dim:#9aa3b8;--teal:#2e8b8b;--gold:#d4af37;--bad:#c0504d}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:14px/1.45 system-ui,sans-serif}
header{padding:10px 14px;border-bottom:1px solid #26304d;display:flex;flex-wrap:wrap;gap:10px;align-items:center}
h1{font-size:15px;margin:0;color:var(--gold);font-weight:600}
.bar{display:flex;gap:6px;flex-wrap:wrap;align-items:center}
button,select{background:#1c2742;border:1px solid #33406a;color:var(--ink);border-radius:4px;padding:4px 10px;cursor:pointer;font-size:12px}
button:hover{border-color:var(--teal)}
button.on{background:var(--teal);border-color:var(--teal);color:#06121a;font-weight:600}
button.dec-ORIGINAL.on{background:#b87333;border-color:#b87333}
button.dec-ALT.on{background:var(--gold);border-color:var(--gold)}
button.dec-BOTH.on{background:#4f7942;border-color:#4f7942}
button.dec-NEITHER.on{background:var(--bad);border-color:var(--bad)}
.pairnav{display:flex;gap:6px;align-items:center;color:var(--dim);font-size:12px}
main{display:flex;gap:12px;padding:12px;align-items:stretch;flex-wrap:wrap}
.panel{flex:1 1 380px;background:var(--panel);border:1px solid #26304d;border-radius:6px;padding:10px;min-width:320px}
.panel h2{margin:0 0 6px;font-size:13px;letter-spacing:.06em}
.panel.orig h2{color:#b87333}.panel.alt h2{color:var(--gold)}
.imgwrap{overflow:auto;max-height:52vh;border:1px solid #26304d;border-radius:4px;display:flex;align-items:flex-start;justify-content:center}
.checker{background:repeating-conic-gradient(#232a3d 0% 25%,#2c3550 0% 50%) 50%/16px 16px}
.imgwrap img{image-rendering:pixelated;image-rendering:crisp-edges;display:block}
.meta{font-size:12px;color:var(--dim);margin-top:8px;word-break:break-word}
.meta b{color:var(--ink)}
.flags span{display:inline-block;background:#1c2742;border:1px solid #33406a;border-radius:3px;padding:0 5px;margin:2px 3px 0 0;font-size:11px}
.status-PASS{color:#6fbf73}.status-PASS_WITH_FLAGS{color:var(--gold)}.status-FAIL{color:var(--bad)}.status-not_generated{color:var(--dim)}
details{margin-top:8px}summary{cursor:pointer;color:var(--teal);font-size:12px}
pre{white-space:pre-wrap;font-size:11px;color:var(--dim);max-height:180px;overflow:auto}
ul.axes{margin:6px 0 0;padding-left:18px;font-size:12px;color:var(--dim)}
footer{padding:8px 14px;color:var(--dim);font-size:11px;border-top:1px solid #26304d}
.missing{color:var(--dim);font-style:italic;padding:24px;text-align:center}
</style>
</head>
<body>
<header>
  <h1>ALT RUN — CHAMPION vs CHALLENGER</h1>
  <div class="pairnav">
    <button id="prev">&larr;</button><span id="pos"></span><button id="next">&rarr;</button>
  </div>
  <div class="bar">
    <select id="filter"></select>
    <button id="imgMode">IMG: source</button>
    <button id="zoomOut">zoom &minus;</button><span id="zoomLabel" style="font-size:12px;color:var(--dim)"></span><button id="zoomIn">zoom +</button>
    <button id="oneToOne">1:1</button>
    <button id="checker" class="on">checker</button>
  </div>
  <div class="bar" id="decisions">
    <button class="dec-ORIGINAL" data-d="ORIGINAL" title="O">ORIGINAL</button>
    <button class="dec-ALT" data-d="ALT" title="A">ALT</button>
    <button class="dec-BOTH" data-d="BOTH" title="B">BOTH</button>
    <button class="dec-NEITHER" data-d="NEITHER" title="N">NEITHER</button>
    <button class="dec-UNDECIDED" data-d="UNDECIDED" title="U">UNDECIDED</button>
    <button id="export">EXPORT DECISIONS</button>
  </div>
</header>
<main id="main"></main>
<footer>Decisions are stored locally in your browser (localStorage key <code>sa_alt_review_v1</code>) and are
never automatic — this tool never declares winners. Export writes <code>alt_selections.json</code>.
Keys: O/A/B/N/U decide, &larr;/&rarr; navigate, G toggle source/game_ready, C checker, 1 one-to-one.</footer>
<script>
const PAIRS = __PAIRS_JSON__;
const LS_KEY = "sa_alt_review_v1";
const DECISIONS = ["ORIGINAL","ALT","BOTH","NEITHER","UNDECIDED"];
const FILTERS = ["ALL","UNDECIDED","ORIGINAL","ALT","BOTH","NEITHER","PASS","PASS_WITH_FLAGS","FAIL"];
let state = JSON.parse(localStorage.getItem(LS_KEY) || "{}");
let idx = 0, filter = "ALL", imgMode = "source", zoom = 3, checker = true;

function save(){ localStorage.setItem(LS_KEY, JSON.stringify(state)); }
function dec(p){ return state[p.alt.cid] || "UNDECIDED"; }
function passFilter(p){
  if (filter === "ALL") return true;
  if (filter === "UNDECIDED") return dec(p) === "UNDECIDED";
  if (DECISIONS.includes(filter)) return dec(p) === filter;
  return p.alt.status === filter;
}
function visible(){ return PAIRS.filter(passFilter); }

function imgTag(side, p){
  const f = side === "orig" ? p.orig : p.alt;
  if (!f.generated) return '<div class="missing">not generated yet</div>';
  const src = imgMode === "source" ? f.source : f.game_ready;
  const w = (imgMode === "source" ? f.sw : f.gw) * zoom;
  return '<img src="' + src + '" style="width:' + w + 'px" alt="">';
}
function flagsHtml(fl){ return '<span>' + (fl && fl.length ? fl.join('</span><span>') : 'none') + '</span>'; }
function metaHtml(f, isAlt){
  let h = '<div class="meta"><b>' + f.cid + '</b> &middot; <span class="status-' + f.status + '">' + f.status + '</span><br>'
    + 'source ' + f.sw + '&times;' + f.sh + ' &rarr; game_ready ' + f.gw + '&times;' + f.gh
    + ' (target ' + f.tw + '&times;' + f.th + ') &middot; alpha: ' + (f.alpha ? 'yes' : 'no') + '</div>'
    + '<div class="meta flags"><b>flags:</b><br>' + flagsHtml(f.flags) + '</div>';
  if (isAlt && f.axes && f.axes.length)
    h += '<ul class="axes">' + f.axes.map(a => '<li>' + a + '</li>').join('') + '</ul>';
  if (f.prompt) h += '<details><summary>generation prompt</summary><pre>' + f.prompt.replace(/</g,'&lt;') + '</pre></details>';
  return h;
}
function render(){
  const vis = visible();
  if (!vis.length){ document.getElementById("main").innerHTML = '<div class="missing" style="flex:1">no pairs match this filter</div>'; }
  else {
    if (idx >= vis.length) idx = vis.length - 1;
    const p = vis[idx];
    const d = dec(p);
    document.getElementById("main").innerHTML =
      '<section class="panel orig"><h2>ORIGINAL / CHAMPION &middot; ' + p.slot_id + '</h2>'
      + '<div class="imgwrap' + (checker ? ' checker' : '') + '">' + imgTag("orig", p) + '</div>'
      + metaHtml(p.orig, false) + '</section>'
      + '<section class="panel alt"><h2>ALTERNATE / CHALLENGER &middot; ' + p.alt.cid + ' &middot; vs ' + p.orig.cid + '</h2>'
      + '<div class="imgwrap' + (checker ? ' checker' : '') + '">' + imgTag("alt", p) + '</div>'
      + metaHtml(p.alt, true) + '</section>';
    document.getElementById("pos").textContent = (idx + 1) + " / " + vis.length + "  (" + p.orig.cid + " vs " + p.alt.cid + ")";
    document.querySelectorAll("#decisions .dec-ORIGINAL,.dec-ALT,.dec-BOTH,.dec-NEITHER,.dec-UNDECIDED")
      .forEach(b => b.classList.toggle("on", b.dataset.d === d));
  }
  document.getElementById("imgMode").textContent = "IMG: " + imgMode;
  document.getElementById("zoomLabel").textContent = zoom + "x";
}
function decide(d){ const vis = visible(); if (!vis.length) return; state[vis[idx].alt.cid] = d; save(); render(); }
function step(n){ const vis = visible(); if (!vis.length) return; idx = Math.max(0, Math.min(vis.length - 1, idx + n)); render(); }

const fs = document.getElementById("filter");
FILTERS.forEach(f => { const o = document.createElement("option"); o.value = o.textContent = f; fs.appendChild(o); });
fs.onchange = () => { filter = fs.value; idx = 0; render(); };
document.getElementById("prev").onclick = () => step(-1);
document.getElementById("next").onclick = () => step(1);
document.getElementById("imgMode").onclick = () => { imgMode = imgMode === "source" ? "game_ready" : "source"; render(); };
document.getElementById("zoomIn").onclick = () => { zoom = Math.min(12, zoom + 1); render(); };
document.getElementById("zoomOut").onclick = () => { zoom = Math.max(1, zoom - 1); render(); };
document.getElementById("oneToOne").onclick = () => { zoom = 1; render(); };
document.getElementById("checker").onclick = (e) => { checker = !checker; e.target.classList.toggle("on", checker); render(); };
document.querySelectorAll("#decisions [data-d]").forEach(b => b.onclick = () => decide(b.dataset.d));
document.getElementById("export").onclick = () => {
  const out = { project: "starlight-acre", run_id: "arena_agent_alt_asset_run",
    exported: new Date().toISOString().slice(0, 10), decisions: PAIRS.map(p => ({
      slot_id: p.slot_id, source_candidate_id: p.orig.cid, alternate_candidate_id: p.alt.cid,
      decision: state[p.alt.cid] || "UNDECIDED",
      original_technical_status: p.orig.status, alternate_technical_status: p.alt.status })) };
  const a = document.createElement("a");
  a.href = URL.createObjectURL(new Blob([JSON.stringify(out, null, 2)], {type: "application/json"}));
  a.download = "alt_selections.json"; a.click();
};
document.addEventListener("keydown", e => {
  if (e.target.tagName === "INPUT" || e.target.tagName === "TEXTAREA") return;
  const k = e.key.toLowerCase();
  if (k === "o") decide("ORIGINAL"); else if (k === "a") decide("ALT");
  else if (k === "b") decide("BOTH"); else if (k === "n") decide("NEITHER");
  else if (k === "u") decide("UNDECIDED");
  else if (e.key === "ArrowLeft") step(-1); else if (e.key === "ArrowRight") step(1);
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
    pairs = []
    for r in recs:
        oc = json.load(open(os.path.join(ORIG_ROOT, "slots", r["slot_id"], r["source_candidate_id"], "candidate.json")))
        pairs.append({
            "slot_id": r["slot_id"],
            "orig": {
                "cid": r["source_candidate_id"], "status": oc["technical_status"],
                "flags": oc.get("technical_flags", []),
                "source": "../arena_agent_asset_run/" + oc["source_file"],
                "game_ready": "../arena_agent_asset_run/" + oc["game_ready_file"],
                "sw": oc["actual_source_width"], "sh": oc["actual_source_height"],
                "gw": oc["actual_game_width"], "gh": oc["actual_game_height"],
                "tw": oc["expected_width"], "th": oc["expected_height"],
                "alpha": oc.get("alpha_present"), "prompt": oc.get("generation_prompt"),
                "generated": True,
            },
            "alt": {
                "cid": r["alternate_candidate_id"], "status": r["technical_status"],
                "flags": r["technical_flags"],
                "source": r["source_file"], "game_ready": r["game_ready_file"],
                "sw": r["actual_source_width"], "sh": r["actual_source_height"],
                "gw": r["actual_game_width"], "gh": r["actual_game_height"],
                "tw": r["expected_width"], "th": r["expected_height"],
                "alpha": r.get("alpha_present"), "prompt": r.get("generation_prompt"),
                "axes": r.get("challenger_axes", []),
                "generated": r["generation_status"] == "generated",
            },
        })
    html = REVIEW_TEMPLATE.replace("__PAIRS_JSON__", json.dumps(pairs))
    open(os.path.join(ALT_ROOT, "review.html"), "w").write(html)
    return len(pairs)


def main():
    recs = []
    for sid in SLOT_ORDER:
        for orig_cid in candidate_ids(sid):
            recs.append(process_candidate(sid, orig_cid, alt_id_for(orig_cid)))
    gen = [r for r in recs if r["generation_status"] == "generated"]
    val = [r for r in gen if r["actual_game_width"]]
    by_status = {}
    for r in gen:
        by_status[r["technical_status"]] = by_status.get(r["technical_status"], 0) + 1
    manifest = {
        "project": PROJECT, "run_id": RUN_ID,
        "original_run_path": "../arena_agent_asset_run",
        "repository_commit_baseline": BASELINE,
        "target_alternate_count": 44,
        "generated_count": len(gen), "validated_count": len(val),
        "failed_count": len([r for r in gen if r["technical_status"] == "FAIL"]),
        "technical_status_counts": by_status,
        "slots": list(SLOT_ORDER),
        "mapping": "one-to-one: <SLOT>_C00N -> <SLOT>_ALT_C00N",
        "candidates": [{
            "slot_id": r["slot_id"],
            "source_candidate_id": r["source_candidate_id"],
            "alternate_candidate_id": r["alternate_candidate_id"],
            "priority": r["priority"],
            "generation_status": r["generation_status"],
            "technical_status": r["technical_status"],
            "original_candidate_path": f"../arena_agent_asset_run/slots/{r['slot_id']}/{r['source_candidate_id']}/candidate.json",
            "alternate_candidate_path": f"slots/{r['slot_id']}/{r['alternate_candidate_id']}/candidate.json",
            "source_file": r["source_file"], "game_ready_file": r["game_ready_file"],
            "actual_source_width": r["actual_source_width"], "actual_source_height": r["actual_source_height"],
            "actual_game_width": r["actual_game_width"], "actual_game_height": r["actual_game_height"],
            "expected_width": r["expected_width"], "expected_height": r["expected_height"],
            "alpha_present": r["alpha_present"],
            "sha256_source": r["sha256_source"], "sha256_game_ready": r["sha256_game_ready"],
            "technical_flags": r["technical_flags"], "challenger_axes": r["challenger_axes"],
        } for r in recs],
    }
    wjson(os.path.join(ALT_ROOT, "ALT_GENERATION_MANIFEST.json"), manifest)
    build_requirements()
    build_prompts_md(recs)
    n = build_review(recs)
    print(f"alt candidates=44 generated={len(gen)} validated={len(val)} "
          f"failed={manifest['failed_count']} status={by_status}")
    print(f"review.html rebuilt with {n} champion/challenger pairs")


if __name__ == "__main__":
    main()
