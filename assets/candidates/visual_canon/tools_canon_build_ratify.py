#!/usr/bin/env python3
"""Starlight Acre — builds ratify.html, the HUMAN RATIFICATION CONSOLE.

Reads VISUAL_CANON_SELECTIONS.json + MASTER_ASSET_INDEX.json +
COHESION_REPAIR_QUEUE.json and emits a self-contained offline decision
interface. Metric-derived draft roles are displayed as DRAFTS only — this tool
never ratifies anything; humans do. Decisions persist in localStorage
(starlight-acre-visual-ratification-v1) and export as RATIFICATION_DECISIONS.json
for apply_ratification.py.

The console JS is structured so all decision logic (export payload building,
import validation, candidate resolution) lives in pure headless-testable
functions; DOM wiring is guarded behind `if (typeof document !== "undefined")`.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))

HIGH_RISK_ORDER = [
    "B01_GREENHOUSE_BACKGROUND", "B02_ENGINEERING_BACKGROUND", "E01_GREENHOUSE_TILESET",
    "P01_PLAYER_SHEET", "D01_DEXTER_VENDOR", "A04_HARVESTER_DRONE", "C01_WISDOM_FRUIT",
    "T03_TERMINAL_ACTIVE_GLOW", "V01_CORE_VFX", "V02_HAZARD_VFX",
]

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
]


def rel(p):
    return os.path.relpath(os.path.join(REPO, p), HERE).replace(os.sep, "/")


def main():
    idx = json.load(open(os.path.join(HERE, "MASTER_ASSET_INDEX.json")))
    sel = json.load(open(os.path.join(HERE, "VISUAL_CANON_SELECTIONS.json")))
    queue = json.load(open(os.path.join(HERE, "COHESION_REPAIR_QUEUE.json")))

    queue_by_id = {}
    for e in queue["entries"]:
        queue_by_id.setdefault(e["candidate_id"], e)  # ids are unique across all runs

    by_slot = {}
    for c in idx["candidates"]:
        by_slot.setdefault(c["slot_id"], []).append(c)

    slots = []
    sel_order = [s["slot_id"] for s in sel["selections"]]
    ordered = HIGH_RISK_ORDER + [s for s in sel_order if s not in HIGH_RISK_ORDER]
    assert len(ordered) == 29 and len(set(ordered)) == 29

    for sid in ordered:
        s = next(x for x in sel["selections"] if x["slot_id"] == sid)
        role = {s["primary_reference"]["candidate_id"]: "PRIMARY"}
        if s.get("secondary_reference"):
            role[s["secondary_reference"]["candidate_id"]] = "SECONDARY"
        for r in s["reject_as_style_reference"]:
            role.setdefault(r["candidate_id"], "REJECT")
        cands = []
        for c in by_slot[sid]:
            for key in ("source_file", "game_ready_file"):
                assert os.path.isfile(os.path.join(REPO, c[key])), c[key]
            q = queue_by_id.get(c["candidate_id"])
            cands.append({
                "cid": c["candidate_id"], "run": c["run"],
                "role": role.get(c["candidate_id"], "OTHER"),
                "status": c["technical_status"], "flags": c["technical_flags"],
                "source": rel(c["source_file"]), "game_ready": rel(c["game_ready_file"]),
                "sw": c["source_dimensions"][0], "sh": c["source_dimensions"][1],
                "gw": c["actual_game_dimensions"][0], "gh": c["actual_game_dimensions"][1],
                "traits": c["art_direction_observations"],
                "queue": ({"action": q["recommended_action"], "problem": q["problem"],
                           "severity": q["severity"]} if q else None),
            })
        cands.sort(key=lambda c: ({"PRIMARY": 0, "SECONDARY": 1, "OTHER": 2, "REJECT": 3}[c["role"]], c["run"], c["cid"]))
        slots.append({
            "slot_id": sid, "asset_name": s["asset_name"], "family": s["asset_family"],
            "high_risk": sid in HIGH_RISK_ORDER,
            "draft_primary": s["primary_reference"]["candidate_id"],
            "draft_secondary": (s["secondary_reference"]["candidate_id"] if s.get("secondary_reference") else None),
            "candidates": cands,
        })

    data = {"slots": slots, "total_queue_entries": len(queue["entries"])}
    scale = [{"slot_id": t[0], "label": t[1]} for t in SCALE_BOARD]

    html = TEMPLATE.replace("__DATA_JSON__", json.dumps(data)).replace("__SCALE_JSON__", json.dumps(scale))
    open(os.path.join(HERE, "ratify.html"), "w").write(html)
    print("ratify.html written: %d slots (high-risk first: %s), %d candidate cards, %d scale entries" % (
        len(slots), ", ".join(s["slot_id"].split("_")[0] for s in slots[:10]),
        sum(len(s["candidates"]) for s in slots), len(scale)))


TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Starlight Acre — Visual Canon Ratification Console</title>
<style>
:root{--bg:#0d1220;--panel:#151d33;--ink:#e8e4d8;--dim:#9aa3b8;--teal:#2e8b8b;--gold:#d4af37;--copper:#b87333;--bad:#c0504d;--ok:#6fbf73}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:14px/1.45 system-ui,sans-serif}
header{padding:10px 14px;border-bottom:1px solid #26304d;position:sticky;top:0;background:var(--bg);z-index:6}
h1{font-size:15px;margin:0 0 6px;color:var(--gold);font-weight:600}
.progress{display:flex;gap:14px;flex-wrap:wrap;font-size:12px;color:var(--dim);align-items:center}
.progress b{color:var(--ink)}
.progress .warn{color:var(--bad);font-weight:700}
.bar{display:flex;gap:6px;flex-wrap:wrap;align-items:center;margin-top:8px}
button,select,input[type=text]{background:#1c2742;border:1px solid #33406a;color:var(--ink);border-radius:4px;padding:4px 10px;cursor:pointer;font-size:12px}
button:hover,select:hover{border-color:var(--teal)}
button.on{background:var(--teal);border-color:var(--teal);color:#06121a;font-weight:600}
button.dec{font-weight:600}
button.dec.on{background:var(--gold);border-color:var(--gold);color:#231d07}
#banner{display:none;background:#3a1f22;border:1px solid var(--bad);color:#f0c9c7;padding:6px 12px;margin-top:8px;border-radius:4px;font-size:12px}
main{padding:12px;display:flex;gap:12px;align-items:flex-start;flex-wrap:wrap}
#slotpanel{flex:2 1 640px;min-width:520px}
#sidepanel{flex:1 1 320px;min-width:300px}
.panel{background:var(--panel);border:1px solid #26304d;border-radius:6px;padding:10px;margin-bottom:12px}
h2{margin:0;font-size:15px;color:var(--gold)}
h2 .hr{color:var(--bad);font-size:11px;letter-spacing:.08em}
h3{margin:0 0 6px;font-size:13px;color:var(--teal)}
.slotnav{display:flex;gap:4px;flex-wrap:wrap;margin:8px 0 0}
.slotnav button{padding:2px 7px;font-size:11px}
.slotnav button.cur{border-color:var(--gold);color:var(--gold)}
.slotnav button.done{border-color:var(--ok);color:var(--ok)}
.slotnav button.done.cur{background:var(--ok);color:#06121a}
.card{background:var(--panel);border:1px solid #26304d;border-radius:6px;padding:10px;margin-bottom:10px}
.card.chosen{border-color:var(--gold);box-shadow:0 0 0 1px var(--gold)}
.card .cid{font-weight:700}
.card .sub{color:var(--dim);font-size:11px;margin-top:2px}
.badge{display:inline-block;font-size:10px;font-weight:700;letter-spacing:.06em;border-radius:3px;padding:1px 6px;margin-left:6px;vertical-align:middle}
.badge.PRIMARY{background:var(--gold);color:#231d07}
.badge.SECONDARY{background:#33406a;color:var(--ink)}
.badge.REJECT{background:#5a2d2f;color:#f0c9c7}
.badge.OTHER{background:#26304d;color:var(--dim)}
.badge.q{background:var(--copper);color:#1c1206;margin-left:3px}
.badge.ok{background:#234d2b;color:#bfe8c4}
.imgs{display:flex;gap:10px;margin-top:8px;flex-wrap:wrap}
.imgbox{border:1px solid #26304d;border-radius:4px;overflow:auto;max-height:42vh;display:flex;align-items:flex-start;justify-content:center}
.checker{background:repeating-conic-gradient(#232a3d 0% 25%,#2c3550 0% 50%) 50%/16px 16px}
.imgbox img{image-rendering:pixelated;image-rendering:crisp-edges;display:block}
.truebox{max-width:260px}
.cap{font-size:10px;color:var(--dim);margin-top:2px;text-align:center}
.flags span{display:inline-block;background:#1c2742;border:1px solid #33406a;border-radius:3px;padding:0 5px;margin:2px 3px 0 0;font-size:10px;color:var(--dim)}
.traits{margin:6px 0 0;padding-left:16px;font-size:11px;color:var(--dim)}
.traits li{margin:1px 0}
.decisionrow{display:flex;gap:6px;flex-wrap:wrap;margin:8px 0}
.note{width:100%;margin-top:6px}
#dexter .lock{background:#231d2e;border:1px solid #4a3a6b;border-radius:4px;padding:8px;margin-top:6px;font-size:12px}
#dexter ul{margin:6px 0 6px 18px;padding:0}
#dexter .rej{color:var(--bad);font-size:12px;margin-top:6px}
#scaleboard .baseline{display:flex;gap:14px;align-items:flex-end;flex-wrap:wrap;border-bottom:2px solid #3b4a6b;overflow-x:auto;padding-top:8px}
.item{display:flex;flex-direction:column;align-items:center;justify-content:flex-end}
.item .lbl{font-size:10px;color:var(--dim);margin-bottom:4px;text-align:center;max-width:150px}
.item img{image-rendering:pixelated;image-rendering:crisp-edges;display:block}
.item.unratified img{opacity:.65;filter:saturate(.8)}
.item .st{font-size:9px;margin-top:3px;color:var(--dim)}
.item .st.rat{color:var(--ok);font-weight:700}
footer{padding:8px 14px;color:var(--dim);font-size:11px;border-top:1px solid #26304d}
#importMsg{font-size:12px;margin-top:6px;display:none;padding:5px 8px;border-radius:4px}
#importMsg.err{display:block;background:#3a1f22;border:1px solid var(--bad);color:#f0c9c7}
#importMsg.ok{display:block;background:#1d3324;border:1px solid var(--ok);color:#bfe8c4}
.miss{color:var(--dim);font-style:italic}
kbd{background:#1c2742;border:1px solid #33406a;border-radius:3px;padding:0 4px;font-size:10px}
</style>
</head>
<body>
<header>
  <h1>VISUAL CANON RATIFICATION CONSOLE — metric drafts await HUMAN decisions</h1>
  <div class="progress" id="progress"></div>
  <div id="banner">A canon is NOT ratified while DEFER entries remain. NEEDS_NEW_REFERENCE slots are recorded as gaps, not as ratified canon.</div>
  <div class="bar">
    <button id="prev">&larr; PREVIOUS</button>
    <button id="nextUnrev" style="border-color:var(--gold);color:var(--gold)">NEXT UNREVIEWED</button>
    <select id="slotjump"></select>
    <button id="imgMode">IMG: game_ready</button>
    <button id="z1">1:1</button><button id="z2">2x</button><button id="z4" class="on">4x</button><button id="z8">8x</button>
    <button id="checker" class="on">checker</button>
    <button id="flagsBtn" class="on">flags</button>
    <button id="metricsBtn">metrics</button>
  </div>
  <div class="bar">
    <button id="export" style="border-color:var(--gold);color:var(--gold);font-weight:700">EXPORT RATIFICATION</button>
    <button id="copy">COPY JSON</button>
    <button id="importBtn">IMPORT RATIFICATION</button>
    <input type="file" id="importFile" accept=".json,application/json" style="display:none">
    <span id="exportNote" style="font-size:11px;color:var(--dim)"></span>
  </div>
  <div id="importMsg"></div>
</header>
<main>
<section id="slotpanel"></section>
<aside id="sidepanel">
  <div class="panel" id="dexter" style="display:none">
    <h3>DEXTER IDENTITY LOCK — non-negotiable</h3>
    <div class="lock">DEXTER MUST BE:
      <ul>
        <li>very small</li><li>elderly</li><li>tricolor Phal&egrave;ne</li><li>long coat</li>
        <li>floppy ears DOWN</li><li>not upright Papillon ears</li><li>not puppy-proportioned</li>
        <li>unimpressed rather than mascot-cute</li><li>exactly one Dexter</li>
      </ul>
      Authority reference: <b>D01_ALT_C001</b> (draft primary). Secondary: <b>D01_C003</b>.
      <div class="rej">D01_C002 — Recorded duplicate-subject defect: two dogs.</div>
    </div>
  </div>
  <div class="panel">
    <h3>GAME SCALE — live with decisions</h3>
    <div style="font-size:11px;color:var(--dim);margin:4px 0">Currently selected/ratified candidate per slot updates live. True relative pixel scale; uniform zoom only; no per-asset rescaling.</div>
    <div class="baseline" id="baseline"></div>
  </div>
  <div class="panel">
    <h3>Keyboard</h3>
    <div style="font-size:12px;color:var(--dim)">
      <kbd>P</kbd> approve draft primary &middot; <kbd>S</kbd> use draft secondary &middot;
      <kbd>O</kbd> choose other &middot; <kbd>N</kbd> needs new reference &middot; <kbd>D</kbd> defer<br>
      <kbd>&larr;</kbd> previous slot &middot; <kbd>&rarr;</kbd> next slot &middot; <kbd>G</kbd> toggle image &middot; <kbd>C</kbd> checker
    </div>
  </div>
</aside>
</main>
<footer>Starlight Acre ratification gate — metric-derived selection &ne; human-ratified canon. This console records human decisions only; it never declares aesthetic winners.
Decisions persist in localStorage key <code>starlight-acre-visual-ratification-v1</code>. Export writes <code>RATIFICATION_DECISIONS.json</code> (schema v1) for <code>apply_ratification.py</code>. Offline; no external dependencies.</footer>
<script>
const DATA = __DATA_JSON__;
const SCALE = __SCALE_JSON__;
const LS_KEY = "starlight-acre-visual-ratification-v1";
const DECISIONS = ["APPROVE_PRIMARY","USE_SECONDARY","CHOOSE_OTHER","NEEDS_NEW_REFERENCE","DEFER"];

// ---------------- pure logic (headless-testable; no DOM above this line) ----------------
function slotById(id){ return DATA.slots.find(s => s.slot_id === id) || null; }
function decisionOf(state, slot){ return (state[slot.slot_id] && state[slot.slot_id].decision) || null; }
function selectedCandidate(state, slot){
  const st = state[slot.slot_id]; if (!st) return null;
  if (st.decision === "APPROVE_PRIMARY") return slot.candidates.find(c => c.cid === slot.draft_primary) || null;
  if (st.decision === "USE_SECONDARY" && slot.draft_secondary) return slot.candidates.find(c => c.cid === slot.draft_secondary) || null;
  if (st.decision === "CHOOSE_OTHER" && st.selected_candidate_id) return slot.candidates.find(c => c.cid === st.selected_candidate_id) || null;
  return null;
}
function counts(state){
  const c = {}; DECISIONS.forEach(d => c[d] = 0);
  DATA.slots.forEach(s => { const d = decisionOf(state, s); if (d) c[d]++; });
  c.reviewed = DECISIONS.reduce((a, d) => a + c[d], 0);
  return c;
}
function buildExportPayload(state){
  const slots = [];
  DATA.slots.forEach(s => {
    const st = state[s.slot_id]; if (!st) return;
    const sel = selectedCandidate(state, s);
    slots.push({ slot_id: s.slot_id, decision: st.decision,
      selected_candidate_id: sel ? sel.cid : null,
      draft_primary: s.draft_primary, draft_secondary: s.draft_secondary || null,
      human_note: st.human_note || "" });
  });
  return { project: "starlight-acre", schema_version: 1,
    visual_canon_source: "VISUAL_CANON_SELECTIONS.json",
    reviewed_count: slots.length, total_slots: DATA.slots.length, slots: slots };
}
function validateImportPayload(payload){
  const errors = [];
  if (!payload || typeof payload !== "object" || Array.isArray(payload)) return ["payload is not an object"];
  if (payload.project !== "starlight-acre") errors.push("project mismatch: expected \"starlight-acre\"");
  if (payload.schema_version !== 1) errors.push("schema_version must be 1");
  if (!Array.isArray(payload.slots)) { errors.push("slots must be an array"); return errors; }
  const seen = {};
  payload.slots.forEach((e, i) => {
    if (!e || typeof e !== "object") { errors.push("slots["+i+"]: not an object"); return; }
    const s = slotById(e.slot_id);
    if (!s) { errors.push("slots["+i+"]: unknown slot_id \""+e.slot_id+"\""); return; }
    if (seen[e.slot_id]) errors.push("slots["+i+"]: duplicate slot_id \""+e.slot_id+"\"");
    seen[e.slot_id] = 1;
    if (!DECISIONS.includes(e.decision)) errors.push("slots["+i+"] "+e.slot_id+": invalid decision \""+e.decision+"\"");
    if (e.decision === "CHOOSE_OTHER"){
      if (!e.selected_candidate_id) errors.push("slots["+i+"] "+e.slot_id+": CHOOSE_OTHER requires selected_candidate_id");
      else if (!s.candidates.some(c => c.cid === e.selected_candidate_id))
        errors.push("slots["+i+"] "+e.slot_id+": candidate \""+e.selected_candidate_id+"\" does not belong to this slot (cross-slot selection rejected)");
    }
    if (e.decision === "USE_SECONDARY" && !s.draft_secondary)
      errors.push("slots["+i+"] "+e.slot_id+": USE_SECONDARY invalid — this slot has no draft secondary");
  });
  return errors;
}
function importIntoState(state, payload){
  const next = JSON.parse(JSON.stringify(state));
  payload.slots.forEach(e => {
    next[e.slot_id] = { decision: e.decision,
      selected_candidate_id: e.selected_candidate_id || null,
      human_note: e.human_note || "" };
  });
  return next;
}

// ---------------- DOM wiring ----------------
if (typeof document !== "undefined") { (function(){
  let state = {};
  try { state = JSON.parse(localStorage.getItem(LS_KEY) || "{}") || {}; } catch(e) { state = {}; }
  let si = 0, imgMode = "game_ready", zoom = 4, checker = true, showFlags = true, showMetrics = false, szoom = 2;

  const $ = id => document.getElementById(id);
  function save(){ localStorage.setItem(LS_KEY, JSON.stringify(state)); }

  function setDecision(d, cid){
    const s = DATA.slots[si];
    const prev = state[s.slot_id] || {};
    state[s.slot_id] = { decision: d,
      selected_candidate_id: (d === "CHOOSE_OTHER" ? (cid || prev.selected_candidate_id || null) : null),
      human_note: prev.human_note || "" };
    save(); render();
  }

  function imgHtml(c){
    const mainSrc = imgMode === "source" ? c.source : c.game_ready;
    const mainW = (imgMode === "source" ? c.sw : c.gw) * zoom;
    return '<div class="imgs">'
      + '<div class="imgbox' + (checker ? ' checker' : '') + '"><img src="' + mainSrc + '" style="width:' + mainW + 'px" alt=""></div>'
      + '<div class="imgbox truebox' + (checker ? ' checker' : '') + '"><img src="' + c.game_ready + '" style="width:' + c.gw + 'px" alt=""></div>'
      + '</div><div class="cap">left: ' + imgMode + ' @ ' + zoom + 'x nearest-neighbor &middot; right: TRUE SIZE game_ready ' + c.gw + 'x' + c.gh + '</div>';
  }

  function cardHtml(c, s){
    const chosen = selectedCandidate(state, s);
    const isSel = chosen && chosen.cid === c.cid;
    const roleBadge = '<span class="badge ' + c.role + '">' + (c.role === "OTHER" ? "OTHER" : c.role) + '</span>';
    const qBadge = c.queue ? '<span class="badge q">REPAIR QUEUE: ' + c.queue.action + '</span>' : '<span class="badge ok">not in repair queue</span>';
    let h = '<div class="card' + (isSel ? ' chosen' : '') + '">'
      + '<div class="cid">' + c.cid + roleBadge + qBadge + (isSel ? '<span class="badge PRIMARY">CURRENT SELECTION</span>' : '') + '</div>'
      + '<div class="sub">run: ' + c.run + ' &middot; technical: <span class="' + (c.status === 'FAIL' ? 'miss' : '') + '">' + c.status + '</span>'
      + ' &middot; source ' + c.sw + 'x' + c.sh + ' &rarr; game_ready ' + c.gw + 'x' + c.gh + '</div>';
    if (showFlags) h += '<div class="flags">' + (c.flags.length ? c.flags.map(f => '<span>' + f + '</span>').join("") : '<span>none</span>') + '</div>';
    h += imgHtml(c);
    if (c.queue && showMetrics) h += '<div class="traits"><b>queue problem:</b> ' + c.queue.problem + ' (severity ' + c.queue.severity + ')</div>';
    if (showMetrics) h += '<ul class="traits">' + c.traits.map(t => '<li>' + t + '</li>').join("") + '</ul>';
    return h + '</div>';
  }

  function render(){
    const s = DATA.slots[si];
    const c = counts(state);
    $("progress").innerHTML =
      'REVIEWED: <b>' + c.reviewed + ' / ' + DATA.slots.length + '</b>'
      + ' &middot; APPROVE PRIMARY: <b>' + c.APPROVE_PRIMARY + '</b>'
      + ' &middot; USE SECONDARY: <b>' + c.USE_SECONDARY + '</b>'
      + ' &middot; CHOOSE OTHER: <b>' + c.CHOOSE_OTHER + '</b>'
      + ' &middot; NEEDS NEW: <b>' + c.NEEDS_NEW_REFERENCE + '</b>'
      + ' &middot; DEFER: <b class="' + (c.DEFER ? 'warn' : '') + '">' + c.DEFER + '</b>';
    $("banner").style.display = c.DEFER ? "block" : "none";

    const st = state[s.slot_id] || {};
    const dec = st.decision || null;
    let h = '<div class="panel"><h2>' + s.slot_id + ' — ' + s.asset_name
      + (s.high_risk ? ' <span class="hr">HIGH-RISK SLOT</span>' : '') + '</h2>'
      + '<div class="sub" style="color:var(--dim);font-size:12px">family: ' + s.family
      + ' &middot; draft primary: <b>' + s.draft_primary + '</b>'
      + ' &middot; draft secondary: <b>' + (s.draft_secondary || 'none') + '</b>'
      + ' &middot; ' + s.candidates.length + ' candidates</div>'
      + '<div class="decisionrow">'
      + '<button class="dec" data-d="APPROVE_PRIMARY">APPROVE PRIMARY (P)</button>'
      + '<button class="dec" data-d="USE_SECONDARY"' + (s.draft_secondary ? '' : ' disabled title="no draft secondary for this slot"') + '>USE SECONDARY (S)</button>'
      + '<button class="dec" data-d="CHOOSE_OTHER">CHOOSE OTHER (O)</button>'
      + '<button class="dec" data-d="NEEDS_NEW_REFERENCE">NEEDS NEW REFERENCE (N)</button>'
      + '<button class="dec" data-d="DEFER">DEFER (D)</button>'
      + '</div>'
      + '<div><select id="chooseOther"><option value="">— CHOOSE OTHER: pick a candidate from THIS slot —</option>'
      + s.candidates.map(cc => '<option value="' + cc.cid + '"' + (st.selected_candidate_id === cc.cid ? ' selected' : '') + '>'
         + cc.cid + ' [' + cc.role + ']</option>').join("")
      + '</select></div>'
      + '<input type="text" class="note" id="note" placeholder="optional human note for this slot (exported in human_note)" value="'
      + (st.human_note || "").replace(/"/g, '&quot;') + '">'
      + '<div class="slotnav">' + DATA.slots.map((ss, i) => {
          const d = decisionOf(state, ss);
          return '<button data-i="' + i + '" class="' + (i === si ? 'cur' : '') + (d ? ' done' : '') + '">'
            + (d ? '\u2713 ' : '') + ss.slot_id.split('_')[0] + '</button>';
        }).join("") + '</div></div>';
    h += s.candidates.map(cc => cardHtml(cc, s)).join("");
    $("slotpanel").innerHTML = h;

    document.querySelectorAll(".dec").forEach(b => {
      b.classList.toggle("on", b.dataset.d === dec);
      b.onclick = () => { if (b.dataset.d === "CHOOSE_OTHER") { $("chooseOther").focus(); }
                          else setDecision(b.dataset.d); };
    });
    $("chooseOther").onchange = e => { if (e.target.value) setDecision("CHOOSE_OTHER", e.target.value); };
    $("note").onchange = e => { const p = state[s.slot_id] = state[s.slot_id] || {decision: null, selected_candidate_id: null}; p.human_note = e.target.value; save(); };
    document.querySelectorAll(".slotnav button").forEach(b => b.onclick = () => { si = +b.dataset.i; render(); });

    $("dexter").style.display = s.slot_id === "D01_DEXTER_VENDOR" ? "block" : "none";
    renderScale();
    const sj = $("slotjump");
    if (!sj.options.length) DATA.slots.forEach((ss, i) => { const o = document.createElement("option"); o.value = i; o.textContent = (ss.high_risk ? "\u26a0 " : "") + ss.slot_id; sj.appendChild(o); });
    sj.value = si;
    [["z1",1],["z2",2],["z4",4],["z8",8]].forEach(([id, z]) => $(id).classList.toggle("on", zoom === z));
    $("imgMode").textContent = "IMG: " + imgMode;
  }

  function renderScale(){
    const b = $("baseline");
    b.innerHTML = SCALE.map(sc => {
      const s = slotById(sc.slot_id); if (!s) return "";
      const sel = selectedCandidate(state, s);
      const c = sel || s.candidates.find(x => x.cid === s.draft_primary);
      if (!c) return "";
      const rat = !!sel;
      return '<div class="item' + (rat ? '' : ' unratified') + '"><div class="lbl">' + sc.label + '<br>' + c.gw + '&times;' + c.gh + '</div>'
        + '<img src="' + c.game_ready + '" style="width:' + (c.gw * szoom) + 'px;height:' + (c.gh * szoom) + 'px" alt="">'
        + '<div class="st' + (rat ? ' rat' : '') + '">' + (rat ? 'ratified: ' : 'draft: ') + c.cid + '</div></div>';
    }).join("");
  }

  function step(n){ si = Math.max(0, Math.min(DATA.slots.length - 1, si + n)); render(); }
  function nextUnreviewed(){
    for (let i = 0; i < DATA.slots.length; i++) if (!decisionOf(state, DATA.slots[i])) { si = i; render(); return; }
    si = 0; render();
  }

  $("prev").onclick = () => step(-1);
  $("nextUnrev").onclick = nextUnreviewed;
  $("slotjump").onchange = e => { si = +e.target.value; render(); };
  $("imgMode").onclick = () => { imgMode = imgMode === "source" ? "game_ready" : "source"; render(); };
  [["z1",1],["z2",2],["z4",4],["z8",8]].forEach(([id, z]) => $(id).onclick = () => { zoom = z; render(); });
  $("checker").onclick = e => { checker = !checker; e.target.classList.toggle("on", checker); render(); };
  $("flagsBtn").onclick = e => { showFlags = !showFlags; e.target.classList.toggle("on", showFlags); render(); };
  $("metricsBtn").onclick = e => { showMetrics = !showMetrics; e.target.classList.toggle("on", showMetrics); render(); };

  $("export").onclick = () => {
    const payload = buildExportPayload(state);
    $("exportNote").textContent = payload.reviewed_count < payload.total_slots
      ? ("partial export: " + payload.reviewed_count + "/" + payload.total_slots + " slots decided — canon cannot be ratified until all 29 are decided")
      : "complete: all " + payload.total_slots + " slots decided";
    const a = document.createElement("a");
    a.href = URL.createObjectURL(new Blob([JSON.stringify(payload, null, 2)], {type: "application/json"}));
    a.download = "RATIFICATION_DECISIONS.json"; a.click();
  };
  $("copy").onclick = () => {
    const txt = JSON.stringify(buildExportPayload(state), null, 2);
    const ta = document.createElement("textarea"); ta.value = txt; document.body.appendChild(ta); ta.select();
    try { document.execCommand("copy"); $("exportNote").textContent = "JSON copied to clipboard"; }
    catch(e) { $("exportNote").textContent = "copy failed — use EXPORT instead"; }
    document.body.removeChild(ta);
  };
  $("importBtn").onclick = () => $("importFile").click();
  $("importFile").onchange = e => {
    const f = e.target.files[0]; if (!f) return;
    const msg = $("importMsg");
    const rd = new FileReader();
    rd.onload = () => {
      let payload = null;
      try { payload = JSON.parse(rd.result); }
      catch(err) { msg.className = "err"; msg.textContent = "IMPORT REJECTED: file is not valid JSON (" + err.message + ")"; return; }
      const errors = validateImportPayload(payload);
      if (errors.length) { msg.className = "err"; msg.textContent = "IMPORT REJECTED: " + errors.join(" | "); return; }
      state = importIntoState(state, payload); save(); render();
      msg.className = "ok"; msg.textContent = "IMPORTED: " + payload.slots.length + " slot decision(s) restored.";
    };
    rd.readAsText(f);
    e.target.value = "";
  };

  document.addEventListener("keydown", e => {
    if (e.target.tagName === "INPUT" || e.target.tagName === "TEXTAREA" || e.target.tagName === "SELECT") return;
    const k = e.key.toLowerCase();
    if (k === "p") setDecision("APPROVE_PRIMARY");
    else if (k === "s") { if (DATA.slots[si].draft_secondary) setDecision("USE_SECONDARY"); }
    else if (k === "o") $("chooseOther").focus();
    else if (k === "n") setDecision("NEEDS_NEW_REFERENCE");
    else if (k === "d") setDecision("DEFER");
    else if (e.key === "ArrowLeft") step(-1);
    else if (e.key === "ArrowRight") step(1);
    else if (k === "g") { imgMode = imgMode === "source" ? "game_ready" : "source"; render(); }
    else if (k === "c") { checker = !checker; $("checker").classList.toggle("on", checker); render(); }
  });

  render();
})(); }
</script>
</body>
</html>
"""


if __name__ == "__main__":
    main()
