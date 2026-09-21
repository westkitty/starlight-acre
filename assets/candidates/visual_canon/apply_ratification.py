#!/usr/bin/env python3
"""Starlight Acre — RATIFICATION COMPILER.

Input:  RATIFICATION_DECISIONS.json (schema v1) — must be a REAL file produced by
        a human via ratify.html (EXPORT RATIFICATION). This compiler never
        invents, defaults, or fabricates decisions.

Output: RATIFIED_VISUAL_CANON.json   — the human-ratified reference per slot
        RATIFIED_REPAIR_QUEUE.json   — the SMALLEST JUSTIFIED repair set

Refusals (exit code 2, no output files written):
  * input file missing (no human ratification yet)
  * payload invalid (project / schema / unknown slot / bad decision /
    cross-slot candidate / USE_SECONDARY on a slot without a secondary)
  * any slot missing from the payload (ratification incomplete)
  * any slot decided DEFER (a canon is NOT ratified while DEFER entries remain)

NEEDS_NEW_REFERENCE slots are recorded explicitly as gaps; the canon is emitted
with complete=false and never pretends those slots are ratified.

Repair pruning rules (COHESION_REPAIR_QUEUE.json -> RATIFIED_REPAIR_QUEUE.json):
  A. keep a repair when the defective candidate IS the ratified reference
  B. keep a repair when the candidate is explicitly retained as the ratified
     secondary/reference (covered by A's ratified-id set)
  C. a slot whose every viable candidate is defective is handled by A (the
     ratified-but-defective reference) or by NEEDS_NEW_REFERENCE (new
     generation); rejected defective candidates are NOT repaired
  D. no candidate is repaired merely for being defective
  Everything else is classified PRESERVE_AS_REJECTED_CANDIDATE and its original
  files are left untouched.
"""
import argparse, datetime, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))

RUN_DIRS = {
    "original": "arena_agent_asset_run",
    "alt": "arena_agent_alt_asset_run",
    "additional": "arena_agent_additional_asset_run",
    "additional_alt": "arena_agent_additional_alt_asset_run",
}
DECISIONS = ["APPROVE_PRIMARY", "USE_SECONDARY", "CHOOSE_OTHER",
             "NEEDS_NEW_REFERENCE", "DEFER"]


def fail(msgs):
    for m in msgs:
        print("REFUSED:", m)
    print("No output files written. Ratification is NOT complete.")
    sys.exit(2)


def load_json(path):
    with open(path) as f:
        return json.load(f)


def main():
    ap = argparse.ArgumentParser(description="Compile human ratification decisions.")
    ap.add_argument("--input", default=os.path.join(HERE, "RATIFICATION_DECISIONS.json"))
    ap.add_argument("--outdir", default=HERE)
    args = ap.parse_args()

    if not os.path.isfile(args.input):
        fail(["no RATIFICATION_DECISIONS.json at %s — human ratification has not happened yet" % args.input])

    try:
        payload = load_json(args.input)
    except Exception as e:
        fail(["input is not valid JSON: %s" % e])

    selections = load_json(os.path.join(HERE, "VISUAL_CANON_SELECTIONS.json"))
    index = load_json(os.path.join(HERE, "MASTER_ASSET_INDEX.json"))
    queue = load_json(os.path.join(HERE, "COHESION_REPAIR_QUEUE.json"))

    sel_by_slot = {s["slot_id"]: s for s in selections["selections"]}
    cand_by_key = {(c["run"], c["candidate_id"]): c for c in index["candidates"]}
    cands_by_slot = {}
    for c in index["candidates"]:
        cands_by_slot.setdefault(c["slot_id"], {})[c["candidate_id"]] = c

    # ---- validate payload ----
    errors = []
    if not isinstance(payload, dict):
        fail(["payload is not an object"])
    if payload.get("project") != "starlight-acre":
        errors.append('project must be "starlight-acre"')
    if payload.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    slots_in = payload.get("slots")
    if not isinstance(slots_in, list):
        errors.append("slots must be an array")
        slots_in = []
    seen = set()
    for e in slots_in:
        if not isinstance(e, dict) or "slot_id" not in e:
            errors.append("slot entry without slot_id"); continue
        sid = e["slot_id"]
        if sid not in sel_by_slot:
            errors.append("unknown slot_id %s" % sid); continue
        if sid in seen:
            errors.append("duplicate slot_id %s" % sid)
        seen.add(sid)
        d = e.get("decision")
        if d not in DECISIONS:
            errors.append("%s: invalid decision %r" % (sid, d)); continue
        if d == "CHOOSE_OTHER":
            cid = e.get("selected_candidate_id")
            if not cid:
                errors.append("%s: CHOOSE_OTHER requires selected_candidate_id" % sid)
            elif cid not in cands_by_slot[sid]:
                errors.append("%s: candidate %s does not belong to this slot (cross-slot selection rejected)" % (sid, cid))
        if d == "USE_SECONDARY" and not sel_by_slot[sid].get("secondary_reference"):
            errors.append("%s: USE_SECONDARY invalid — slot has no draft secondary" % sid)
    if errors:
        fail(errors)

    # ---- completeness ----
    all_slots = list(sel_by_slot.keys())
    missing = [s for s in all_slots if s not in seen]
    if missing:
        fail(["ratification incomplete — %d slot(s) have no decision: %s" % (len(missing), ", ".join(missing))])
    deferred = [e["slot_id"] for e in slots_in if e["decision"] == "DEFER"]
    if deferred:
        fail(["canon NOT ratified while DEFER entries remain: %s" % ", ".join(deferred)])

    # ---- resolve ratified candidates ----
    ratified_slots, needs_new, resolution_errors = [], [], []
    for e in slots_in:
        sid = e["slot_id"]
        s = sel_by_slot[sid]
        d = e["decision"]
        if d == "NEEDS_NEW_REFERENCE":
            needs_new.append(sid)
            ratified_slots.append({
                "slot_id": sid, "decision": d, "ratified_candidate_id": None,
                "source_run": None, "candidate_path": None, "game_ready_path": None,
                "original_draft_primary": s["primary_reference"]["candidate_id"],
                "decision_source": "human_ratification",
                "ratified": False, "needs_new_reference": True,
                "human_note": e.get("human_note", ""),
            })
            continue
        if d == "APPROVE_PRIMARY":
            cid = s["primary_reference"]["candidate_id"]
        elif d == "USE_SECONDARY":
            cid = s["secondary_reference"]["candidate_id"]
        else:  # CHOOSE_OTHER (validated above)
            cid = e["selected_candidate_id"]
        c = cands_by_slot[sid][cid]
        run_dir = RUN_DIRS[c["run"]]
        ratified_slots.append({
            "slot_id": sid, "decision": d, "ratified_candidate_id": cid,
            "source_run": c["run"],
            "candidate_path": "assets/candidates/%s/slots/%s/%s/candidate.json" % (run_dir, sid, cid),
            "game_ready_path": c["game_ready_file"],
            "original_draft_primary": s["primary_reference"]["candidate_id"],
            "decision_source": "human_ratification",
            "ratified": True, "needs_new_reference": False,
            "human_note": e.get("human_note", ""),
        })
    if resolution_errors:
        fail(resolution_errors)

    ratified_ids = {r["ratified_candidate_id"] for r in ratified_slots if r["ratified"]}

    canon = {
        "project": "starlight-acre", "schema_version": 1,
        "decision_source": "human_ratification",
        "generated": datetime.date.today().isoformat(),
        "input": os.path.basename(args.input),
        "complete": len(needs_new) == 0,
        "needs_new_reference_slots": needs_new,
        "note": ("metric-derived selection != human-ratified canon; this file records the human "
                 "ratification only. NEEDS_NEW_REFERENCE slots are gaps, not ratified canon."),
        "slots": ratified_slots,
    }

    # ---- prune repair queue ----
    kept, preserved = [], []
    for entry in queue["entries"]:
        cid = entry["candidate_id"]
        sid = entry["slot_id"]
        if cid in ratified_ids:
            kept.append(dict(entry, retained_rule="A/B: defective candidate is the ratified reference for its slot"))
        elif sid in needs_new:
            preserved.append(dict(entry, classification="PRESERVE_AS_REJECTED_CANDIDATE",
                                  reason="slot ratified as NEEDS_NEW_REFERENCE — a new reference will be generated; "
                                         "rejected defective candidates are not repaired"))
        else:
            preserved.append(dict(entry, classification="PRESERVE_AS_REJECTED_CANDIDATE",
                                  reason="clean ratified alternative exists for this slot; a rejected candidate is not "
                                         "repaired merely because it is defective"))
    repair_queue = {
        "project": "starlight-acre", "schema_version": 1,
        "decision_source": "human_ratification",
        "source_queue": "COHESION_REPAIR_QUEUE.json",
        "original_queue_count": len(queue["entries"]),
        "kept_count": len(kept), "pruned_count": len(preserved),
        "repairs": kept,
        "preserved_as_rejected_candidate": preserved,
        "note": ("smallest justified repair set: only defects on the ratified canon itself. "
                 "PRESERVE_AS_REJECTED_CANDIDATE entries keep their original files untouched."),
    }

    os.makedirs(args.outdir, exist_ok=True)
    json.dump(canon, open(os.path.join(args.outdir, "RATIFIED_VISUAL_CANON.json"), "w"), indent=1)
    json.dump(repair_queue, open(os.path.join(args.outdir, "RATIFIED_REPAIR_QUEUE.json"), "w"), indent=1)

    print("RATIFIED_VISUAL_CANON.json written: %d slots ratified, %d NEEDS_NEW_REFERENCE, complete=%s"
          % (len([r for r in ratified_slots if r["ratified"]]), len(needs_new), canon["complete"]))
    print("RATIFIED_REPAIR_QUEUE.json written: kept %d of %d queue entries; %d preserved as rejected candidates"
          % (len(kept), len(queue["entries"]), len(preserved)))
    for k in kept:
        print("  KEEP %-12s %-18s %s" % (k["candidate_id"], k["recommended_action"], k["problem"][:70]))


if __name__ == "__main__":
    main()
