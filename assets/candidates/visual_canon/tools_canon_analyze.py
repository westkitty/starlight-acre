#!/usr/bin/env python3
"""Starlight Acre — VISUAL CANON analysis pass (art-direction consolidation).

Deterministically measures every candidate's game_ready.png (the actual in-game
representation) and builds:

  MASTER_ASSET_INDEX.json      — all 136 candidates with pixel metrics + observations
  VISUAL_CANON_SELECTIONS.json — PRIMARY / SECONDARY / REJECT_AS_STYLE_REFERENCE per slot
  canon_metrics_summary.json   — family-level statistics used by the canon/report
  continuity_outliers.json     — cross-family drift audit input

HONESTY NOTE (recorded in every output): this environment has NO image-viewing
capability. All "observations" are quantitative pixel measurements (palette usage,
outline ring darkness/thickness, edge density, cluster run length, lighting bias,
glow ratio, silhouette coverage) computed from the real artwork, combined with the
recorded generation prompts and technical flags. No human-style aesthetic viewing
was performed. Selections are art-direction DRAFTS grounded in these measurements.

Read-only with respect to all four candidate libraries. Never modifies sources.
"""
import json, os, math
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
CAND = os.path.abspath(os.path.join(HERE, ".."))
REPO = os.path.abspath(os.path.join(CAND, "..", ".."))

RUNS = [
    ("original",       "arena_agent_asset_run",          "GENERATION_MANIFEST.json",            "candidates", "candidate_id"),
    ("alt",            "arena_agent_alt_asset_run",       "ALT_GENERATION_MANIFEST.json",        "candidates", "alternate_candidate_id"),
    ("additional",     "arena_agent_additional_asset_run","ADDITIONAL_GENERATION_MANIFEST.json", "candidates", "candidate_id"),
    ("additional_alt", "arena_agent_additional_alt_asset_run","ALT_ADDITIONAL_GENERATION_MANIFEST.json","candidates","alternate_candidate_id"),
]

FAMILY = {
    "P01_PLAYER_SHEET": "PLAYER / HUMANOID",
    "A01_GARDENER_DRONE": "DRONES / AGENTS", "A03_ENGINEER_DRONE": "DRONES / AGENTS",
    "A04_HARVESTER_DRONE": "DRONES / AGENTS", "A05_MAINTENANCE_DRONE": "DRONES / AGENTS",
    "T01_REPAIR_REPLENISH_TERMINALS": "TERMINALS", "T02_RESEARCH_TERMINAL": "TERMINALS",
    "W01_SECTOR_DOOR": "STATION DOORS / FIXTURES",
    "B01_GREENHOUSE_BACKGROUND": "ENVIRONMENT BACKGROUNDS", "B02_ENGINEERING_BACKGROUND": "ENVIRONMENT BACKGROUNDS",
    "E01_GREENHOUSE_TILESET": "ENVIRONMENT TILESETS", "E02_ENGINEERING_TILESET": "ENVIRONMENT TILESETS",
    "E03_CARGO_PROPS": "ENVIRONMENT PROPS",
    "C01_WISDOM_FRUIT": "CROPS / MYTHIC BIOLOGY", "C02_TRICKSTER_VINE": "CROPS / MYTHIC BIOLOGY",
    "C03_LIGHTNING_VINE": "CROPS / MYTHIC BIOLOGY", "C04_SHADOW_ROOT": "CROPS / MYTHIC BIOLOGY",
    "C05_GOLDEN_BLOSSOM": "CROPS / MYTHIC BIOLOGY",
    "D01_DEXTER_VENDOR": "DEXTER / VENDOR", "D02_DEXTER_VENDOR_KIOSK": "DEXTER / VENDOR",
    "U01_HUD_ICONS": "HUD / ICONOGRAPHY", "U02_HUD_EXTENSION_ICONS": "HUD / ICONOGRAPHY",
    "V01_CORE_VFX": "VFX / GLOWS", "T03_TERMINAL_ACTIVE_GLOW": "VFX / GLOWS", "V02_HAZARD_VFX": "VFX / GLOWS",
    "A02_REACTOR_CORE": "LARGE MACHINERY",
    "B04_HYDROPONICS_RIG": "GREENHOUSE MACHINERY",
    "B05_ARCHIVE_STACK": "ARCHIVE / RESEARCH TECHNOLOGY",
    "B03_DOCKING_COLLAR": "DOCKING TECHNOLOGY",
}

ANCHORS = {
    "deep_space_navy": (0x0A, 0x0E, 0x1A), "dusk_blue": (0x1E, 0x2D, 0x4A),
    "hydroponic_teal": (0x2E, 0x8B, 0x8B), "moss_green": (0x4F, 0x79, 0x42),
    "mythic_warm_gold": (0xD4, 0xAF, 0x37), "maintenance_copper": (0xB8, 0x73, 0x33),
    "station_gray": (0x70, 0x80, 0x90), "bone_highlight": (0xF5, 0xF5, 0xDC),
}

# flags that indicate real defects (weight), vs pipeline-standard flags (ignored)
DEFECT_FLAGS = {
    "CROPPED_CONTENT": 3.0, "MULTIPLE_SUBJECTS_POSSIBLE": 2.0, "TILESET_OVERKEYED": 2.0,
    "EXPECTED_CELL_EMPTY": 2.0, "CELL_BACKGROUND_NOT_REMOVED": 1.5,
    "TERMINAL_HALF_MISSING": 3.0, "TERMINAL_HALVES_BRIDGED": 2.0,
    "KEYING_INCOMPLETE_FRAMED_SOURCE": 2.0, "EMPTY_CELLS_OPAQUE": 2.0,
    "SOURCE_TOPOLOGY_MISMATCH": 1.5, "WRONG_DIMENSIONS": 3.0,
    "NORMALIZATION_FAILED": 3.0, "SOURCE_NOT_PNG": 3.0, "UNDECODABLE": 3.0,
    "OPAQUE_BACKGROUND": 1.0, "NO_ALPHA": 0.25, "FRAME_LAYOUT_INVALID": 2.0,
    "TILE_GRID_INVALID": 2.0, "PLAYER_BASELINE_MISALIGNED": 1.5,
    "PLANTER_BAND_INCONSISTENT": 1.5, "LIFECYCLE_OCCUPANCY_NON_MONOTONIC": 1.5,
}


def rgb_to_hsv(r, g, b):
    r, g, b = r/255, g/255, b/255
    mx, mn = max(r, g, b), min(r, g, b)
    d = mx - mn
    v = mx
    s = 0 if mx == 0 else d/mx
    if d == 0: h = 0
    elif mx == r: h = ((g-b)/d) % 6
    elif mx == g: h = (b-r)/d + 2
    else: h = (r-g)/d + 4
    return h*60, s, v


def analyze_image(path):
    im = Image.open(path).convert("RGBA")
    w, h = im.size
    px = im.load()
    vis = []
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a > 40:
                vis.append((x, y, r, g, b))
    n = len(vis)
    m = {"gw": w, "gh": h, "coverage": round(n / (w*h), 4)}
    if n == 0:
        return m
    # palette / HSV stats
    sat = val = 0.0
    warm = cool = 0
    glow = dark = 0
    anchor_frac = {k: 0 for k in ANCHORS}
    near_any = 0
    colors = {}
    for x, y, r, g, b in vis:
        hh, s, v = rgb_to_hsv(r, g, b)
        sat += s; val += v
        if r > b + 18: warm += 1
        elif b > r + 18: cool += 1
        if (v > 0.82 and s > 0.30) or v > 0.93: glow += 1
        if v < 0.28: dark += 1
        best, bd = None, 1e9
        for k, (ar, ag, ab) in ANCHORS.items():
            d = math.dist((r, g, b), (ar, ag, ab))
            if d < bd: bd, best = d, k
        if bd <= 48:
            anchor_frac[best] += 1
            near_any += 1
        colors[(r >> 4, g >> 4, b >> 4)] = colors.get((r >> 4, g >> 4, b >> 4), 0) + 1
    m["mean_saturation"] = round(sat/n, 3)
    m["mean_value"] = round(val/n, 3)
    m["warm_ratio"] = round(warm/n, 4); m["cool_ratio"] = round(cool/n, 4)
    m["glow_ratio"] = round(glow/n, 4); m["dark_ratio"] = round(dark/n, 4)
    m["anchor_adherence"] = round(near_any/n, 4)
    m["anchor_usage"] = {k: round(v/n, 4) for k, v in anchor_frac.items() if v > 0}
    top = sorted(colors.items(), key=lambda kv: -kv[1])[:6]
    m["dominant_colors"] = [{"rgb4": "%X%X%X" % c, "frac": round(c_/n, 3)} for c, c_ in top]
    m["unique_color_count"] = len(colors)
    # silhouette bbox, lighting bias (bbox halves)
    xs = [v[0] for v in vis]; ys = [v[1] for v in vis]
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    m["bbox"] = [x0, y0, x1-x0+1, y1-y0+1]
    def mean_v_region(yy0, yy1):
        s_ = c_ = 0
        for x, y, r, g, b in vis:
            if yy0 <= y < yy1:
                _, _, vv = rgb_to_hsv(r, g, b)
                s_ += vv; c_ += 1
        return s_/c_ if c_ else 0
    ymid = (y0 + y1 + 1) / 2
    m["light_from_above"] = round(mean_v_region(y0, ymid) - mean_v_region(ymid, y1+1), 3)
    # boundary ring darkness (visible pixels adjacent to transparency)
    visset = set((v[0], v[1]) for v in vis)
    ring = [rgb_to_hsv(r, g, b)[2] for x, y, r, g, b in vis
            if any((x+dx, y+dy) not in visset for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)))]
    m["outline_ring_darkness"] = round(1 - (sum(ring)/len(ring)), 3) if ring else None
    # outline weight proxy: consecutive dark pixels from silhouette edge inward (per row)
    weights = []
    rows = {}
    for x, y, *_ in vis:
        rows.setdefault(y, []).append(x)
    for y, rws in rows.items():
        rws.sort()
        xl, xr = rws[0], rws[-1]
        for x0_, step in ((xl, 1), (xr, -1)):
            run = 0
            for i in range(9):
                x_ = x0_ + step*i
                if (x_, y) not in visset: break
                r, g, b, a = px[x_, y]
                if rgb_to_hsv(r, g, b)[2] < 0.40: run += 1
                else: break
            if run: weights.append(run)
    m["outline_weight_px"] = round(sum(weights)/len(weights), 2) if weights else None
    # edge density + cluster run (horizontal)
    edges = 0
    runs = []
    for y in range(h):
        cur = None; rl = 0
        for x in range(w):
            r, g, b, a = px[x, y]
            key = (r, g, b) if a > 40 else None
            if key is None:
                if rl: runs.append(rl)
                rl = 0; cur = None; continue
            if cur is not None:
                if abs(r-cur[0]) > 26 or abs(g-cur[1]) > 26 or abs(b-cur[2]) > 26:
                    edges += 1
                if (r, g, b) == cur:
                    rl += 1
                else:
                    if rl: runs.append(rl)
                    rl = 1
            else:
                rl = 1
            cur = (r, g, b)
        if rl: runs.append(rl)
    m["edge_density"] = round(edges/n, 3)
    m["cluster_run_length"] = round(sum(runs)/len(runs), 2) if runs else None
    return m


# Curated defect overrides backed by recorded run-history evidence (not taste):
# these defects were verified during the original run's recursive verification and are
# documented in PR #2's honest-flags inventory, but the deterministic pipeline did not
# flag them in candidate.json.
CURATED_DEFECTS = {
    ("original", "D01_C002"): (
        "duplicate subject: two dogs in one sprite, recorded during original-run verification "
        "(PR #2 honest-flags inventory); pipeline island analysis did not flag it", 2.5),
}


def defect_weight(run, cid, flags):
    w = sum(DEFECT_FLAGS.get(f, 0.0) for f in flags)
    w += CURATED_DEFECTS.get((run, cid), ("", 0))[1]
    return w


def load_all():
    entries = []
    slot_names = {}
    for run, rdir, mfile, listkey, idkey in RUNS:
        mp = os.path.join(CAND, rdir, mfile)
        m = json.load(open(mp))
        for c in m[listkey]:
            sid = c["slot_id"]
            cid = c[idkey]
            if c.get("asset_name"): slot_names[sid] = c["asset_name"]
            if c.get("generation_status") != "generated":
                continue
            gr = c.get("game_ready_file") or c.get("game_ready")
            sf = c.get("source_file") or c.get("source")
            entries.append({
                "run": run, "run_dir": rdir, "slot_id": sid, "candidate_id": cid,
                "asset_family": FAMILY[sid],
                "asset_name": c.get("asset_name") or slot_names.get(sid, sid),
                "source_file": os.path.join("assets/candidates", rdir, sf) if sf else None,
                "game_ready_file": os.path.join("assets/candidates", rdir, gr) if gr else None,
                "source_dimensions": [c.get("actual_source_width"), c.get("actual_source_height")],
                "dimensions": [c.get("expected_width"), c.get("expected_height")],
                "actual_game_dimensions": [c.get("actual_game_width"), c.get("actual_game_height")],
                "technical_status": c.get("technical_status"),
                "technical_flags": c.get("technical_flags") or c.get("flags") or [],
            })
    for e in entries:
        e["asset_name"] = slot_names.get(e["slot_id"], e["asset_name"])
    return entries


FEATS = ["edge_density", "cluster_run_length", "outline_ring_darkness", "glow_ratio",
         "dark_ratio", "mean_saturation", "light_from_above", "anchor_adherence"]


def robust_stats(vals):
    vals = [v for v in vals if v is not None]
    if not vals: return None
    vals.sort()
    med = vals[len(vals)//2]
    mad = sorted(abs(v - med) for v in vals)[len(vals)//2] or 1e-6
    return med, mad


def main():
    entries = load_all()
    print("candidates loaded:", len(entries))
    for e in entries:
        gp = os.path.join(REPO, e["game_ready_file"])
        e["metrics"] = analyze_image(gp)

    # family stats
    fams = {}
    for e in entries:
        fams.setdefault(e["asset_family"], []).append(e)
    fam_stats = {}
    for fam, es in fams.items():
        st = {}
        for f in FEATS:
            r = robust_stats([e["metrics"].get(f) for e in es])
            if r: st[f] = {"median": round(r[0], 3), "mad": round(r[1], 4), "n": len(es)}
        fam_stats[fam] = {"count": len(es), "features": st}
    glob_stats = {}
    for f in FEATS:
        r = robust_stats([e["metrics"].get(f) for e in entries])
        if r: glob_stats[f] = {"median": round(r[0], 3), "mad": round(r[1], 4)}

    def rz(e, f):
        v = e["metrics"].get(f)
        if v is None: return 0.0
        st = fam_stats[e["asset_family"]]["features"].get(f) or glob_stats.get(f)
        if not st: return 0.0
        return abs(v - st["median"]) / (st["mad"] + 1e-6)

    for e in entries:
        e["family_robust_z"] = round(sum(rz(e, f) for f in FEATS) / len(FEATS), 3)
        e["defect_weight"] = round(defect_weight(e["run"], e["candidate_id"], e["technical_flags"]), 2)

    # ---- master index ----
    def obs(e):
        m = e["metrics"]
        o = []
        dens = "dense" if m["edge_density"] > 0.34 else ("moderate" if m["edge_density"] > 0.22 else "clean")
        o.append(f"pixel_density: {dens} (edge {m['edge_density']}, cluster run {m['cluster_run_length']})")
        if m.get("outline_ring_darkness") is not None:
            o.append(f"outline_behavior: boundary ring darkness {m['outline_ring_darkness']}"
                     f" (weight ~{m.get('outline_weight_px')}px)")
        else:
            o.append("outline_behavior: n/a (opaque sheet)")
        au = m.get("anchor_usage", {})
        top3 = sorted(au.items(), key=lambda kv: -kv[1])[:3]
        o.append("palette_usage: " + (", ".join(f"{k} {v:.0%}" for k, v in top3) if top3 else "off-anchor dominant")
                 + f"; adherence {m['anchor_adherence']:.0%}")
        o.append(f"lighting_direction: {'from above' if m['light_from_above'] > 0.02 else ('from below / base-lit' if m['light_from_above'] < -0.02 else 'flat')} (bias {m['light_from_above']})")
        o.append(f"glow_usage: {m['glow_ratio']:.1%} bright-saturated; dark_ratio {m['dark_ratio']:.0%}")
        w = "warm-led" if m["warm_ratio"] > m["cool_ratio"] + 0.05 else ("cool-led" if m["cool_ratio"] > m["warm_ratio"] + 0.05 else "balanced")
        o.append(f"material_language: {w} (warm {m['warm_ratio']:.0%} / cool {m['cool_ratio']:.0%}); "
                 f"{m['unique_color_count']} quantized colors")
        o.append(f"shape_language: silhouette coverage {m['coverage']:.0%}, bbox {m['bbox'][2]}x{m['bbox'][3]}")
        vc = "high" if m["unique_color_count"] > 60 else ("medium" if m["unique_color_count"] > 25 else "low")
        o.append(f"visual_complexity: {vc}")
        o.append(f"family_compatibility: robust-z vs {e['asset_family']} = {e['family_robust_z']}")
        return o

    index = {
        "project": "starlight-acre", "pass": "visual canon consolidation",
        "method_note": ("No image-viewing capability exists in this environment. All observations are "
                        "deterministic pixel measurements computed from each candidate's game_ready.png "
                        "(the actual in-game representation), combined with recorded generation prompts "
                        "and technical flags. No human aesthetic viewing was performed."),
        "families": {f: {"count": v["count"]} for f, v in fam_stats.items()},
        "candidates": [],
    }
    for e in sorted(entries, key=lambda e: (e["asset_family"], e["slot_id"], e["run"], e["candidate_id"])):
        index["candidates"].append({
            "run": e["run"], "slot_id": e["slot_id"], "candidate_id": e["candidate_id"],
            "asset_family": e["asset_family"], "asset_name": e["asset_name"],
            "source_file": e["source_file"], "game_ready_file": e["game_ready_file"],
            "source_dimensions": e["source_dimensions"], "dimensions": e["dimensions"],
            "actual_game_dimensions": e["actual_game_dimensions"],
            "technical_status": e["technical_status"], "technical_flags": e["technical_flags"],
            "art_direction_observations": obs(e),
            "metrics": e["metrics"],
        })
    json.dump(index, open(os.path.join(HERE, "MASTER_ASSET_INDEX.json"), "w"), indent=1)

    # ---- selections ----
    by_slot = {}
    for e in entries:
        by_slot.setdefault(e["slot_id"], []).append(e)

    def score(e):
        return e["defect_weight"] * 10 + e["family_robust_z"]

    def why(e, fam_med):
        m = e["metrics"]
        fl = [f for f in e["technical_flags"] if f not in
              ("BACKGROUND_REMOVED", "CONVERSION_REQUIRED", "NO_ALPHA", "UNREADABLE_AT_TARGET_SCALE",
               "FRAME_LAYOUT_UNCERTAIN")]
        parts = [f"cleanest technical record in slot (non-standard flags: {fl or 'none'})" if e["defect_weight"] <= 0.25
                 else f"least-defective available (flags: {', '.join(fl)})",
                 f"pixel density on family median (edge {m['edge_density']} vs family {fam_med.get('edge_density', {}).get('median', 'n/a')}; "
                 f"cluster run {m['cluster_run_length']})",
                 f"outline ring darkness {m.get('outline_ring_darkness')}, glow {m['glow_ratio']:.1%}, "
                 f"light-from-above bias {m['light_from_above']}",
                 f"family robust-z {e['family_robust_z']} (lower = more typical of the family's visual language)"]
        return " | ".join(parts)

    selections = {"project": "starlight-acre",
                  "method_note": index["method_note"],
                  "note": ("PRIMARY/SECONDARY are art-direction style references, not gameplay promotions. "
                           "REJECT_AS_STYLE_REFERENCE candidates remain usable assets but must not teach "
                           "future generators the project's visual language."),
                  "selections": []}
    for sid in sorted(by_slot):
        es = sorted(by_slot[sid], key=score)
        fam = es[0]["asset_family"]
        fam_med = fam_stats[fam]["features"]
        prim = es[0]
        # secondary: best-scoring candidate from a different run than primary when reasonable
        # secondary: prefer a different run, but never a flagged/defective candidate
        # while a clean one exists; fall back to next-best clean, then next-best.
        clean = [e for e in es[1:] if e["defect_weight"] <= 0.5]
        sec = None
        for e in clean:
            if e["run"] != prim["run"]:
                sec = e; break
        if sec is None and clean:
            sec = clean[0]
        if sec is None and len(es) > 1 and es[1]["defect_weight"] <= 2.0:
            sec = es[1]  # minor-flag fallback only; seriously defective candidates
                         # must not become style references (null secondary is honest)
        rejects = []
        for e in es:
            if e in (prim, sec): continue
            fl = [f for f in e["technical_flags"] if f in DEFECT_FLAGS and DEFECT_FLAGS[f] >= 1.5]
            cur = CURATED_DEFECTS.get((e["run"], e["candidate_id"]))
            reasons = []
            if fl: reasons.append("defect flags: " + ", ".join(fl))
            if cur: reasons.append("curated run-history evidence: " + cur[0])
            if e["family_robust_z"] > 2.5: reasons.append(f"visual outlier vs family (robust-z {e['family_robust_z']})")
            if reasons:
                rejects.append({"candidate_id": e["candidate_id"], "run": e["run"], "reason": "; ".join(reasons)})
        selections["selections"].append({
            "slot_id": sid, "asset_name": prim["asset_name"], "asset_family": fam,
            "primary_reference": {"run": prim["run"], "candidate_id": prim["candidate_id"],
                                  "game_ready_file": prim["game_ready_file"],
                                  "source_file": prim["source_file"],
                                  "why_it_fits_the_family": why(prim, fam_med)},
            "secondary_reference": ({"run": sec["run"], "candidate_id": sec["candidate_id"],
                                     "game_ready_file": sec["game_ready_file"],
                                     "source_file": sec["source_file"],
                                     "why": why(sec, fam_med)} if sec else None),
            "reject_as_style_reference": rejects,
        })
    json.dump(selections, open(os.path.join(HERE, "VISUAL_CANON_SELECTIONS.json"), "w"), indent=1)

    # ---- summaries for the canon writer ----
    summary = {"family_stats": fam_stats, "global_stats": glob_stats,
               "slot_selections": [{ "slot_id": s["slot_id"],
                                     "primary": s["primary_reference"]["candidate_id"],
                                     "primary_run": s["primary_reference"]["run"],
                                     "secondary": s["secondary_reference"]["candidate_id"] if s["secondary_reference"] else None,
                                     "rejects": [r["candidate_id"] for r in s["reject_as_style_reference"]]}
                                    for s in selections["selections"]]}
    json.dump(summary, open(os.path.join(HERE, "canon_metrics_summary.json"), "w"), indent=1)

    # ---- continuity outliers ----
    outliers = []
    for e in entries:
        for f in FEATS:
            z = rz(e, f)
            if z > 4.0:
                outliers.append({"slot_id": e["slot_id"], "candidate_id": e["candidate_id"], "run": e["run"],
                                 "feature": f, "value": e["metrics"].get(f),
                                 "family_median": (fam_stats[e["asset_family"]]["features"].get(f) or {}).get("median"),
                                 "robust_z": round(z, 2)})
    json.dump(outliers, open(os.path.join(HERE, "continuity_outliers.json"), "w"), indent=1)

    print("families:", {f: len(v) for f, v in fams.items()})
    print("\nSLOT SELECTIONS (primary <- run):")
    for s in summary["slot_selections"]:
        print("  %-34s PRIMARY %-16s (%s)  SECONDARY %-16s  rejects: %s" % (
            s["slot_id"], s["primary"], s["primary_run"], s["secondary"] or "-",
            ",".join(s["rejects"]) or "-"))
    print("\nCONTINUITY OUTLIERS (robust-z>4):", len(outliers))
    for o in outliers:
        print("  %s/%s %s=%s (median %s, z=%s)" % (o["slot_id"], o["candidate_id"], o["feature"], o["value"], o["family_median"], o["robust_z"]))
    print("\nGLOBAL MEDIANS:", {f: glob_stats[f]["median"] for f in glob_stats})


if __name__ == "__main__":
    main()
