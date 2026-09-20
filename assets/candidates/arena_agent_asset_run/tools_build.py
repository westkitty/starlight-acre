#!/usr/bin/env python3
"""Starlight Acre — Arena agent asset run: deterministic normalize + validate + metadata pipeline.

Idempotent: scans slots/*/*/source.png, produces game_ready.png where deterministically safe,
writes candidate.json per candidate, then rebuilds review.html + GENERATION_MANIFEST.json.

Rules (from run contract):
  * sources are never modified
  * nearest-neighbor only, no smoothing, preserve aspect ratio, crop only when safe
  * flat-background removal only when the border is dominantly one flat color
  * never invent or rearrange frames; uncertain topology is flagged, not faked
"""
import hashlib, json, os, sys
from collections import Counter, deque
from PIL import Image

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
from run_spec import SLOTS, candidate_ids, full_prompt, PROJECT, RUN_ID

TOL_KEY = 30        # per-channel tolerance for background key
BORDER_DOM = 0.85   # fraction of border pixels that must share one quantized color

SLOT_ORDER = list(SLOTS.keys())


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def border_seed_colors(im, min_share=0.08):
    """Quantized border colors covering >= min_share of the border. Returns list of (r,g,b)."""
    w, h = im.size
    px = im.convert("RGB").load()
    border = []
    for x in range(w):
        border.append(px[x, 0]); border.append(px[x, h - 1])
    for y in range(h):
        border.append(px[0, y]); border.append(px[w - 1, y])
    q = Counter((r // 16, g // 16, b // 16) for r, g, b in border)
    seeds = []
    for (qr, qg, qb), n in q.most_common(6):
        if n / len(border) < min_share:
            continue
        sel = [c for c in border if (c[0] // 16, c[1] // 16, c[2] // 16) == (qr, qg, qb)]
        seeds.append((sum(c[0] for c in sel) // len(sel),
                      sum(c[1] for c in sel) // len(sel),
                      sum(c[2] for c in sel) // len(sel)))
    return seeds


def flood_key(im, seeds, tol=26, halo_tol=60):
    """Remove border-connected background regions (BFS from edges), then clean a 1px halo.
    Enclosed same-color regions are preserved. Returns (rgba, removed_frac)."""
    rgba = im.convert("RGBA")
    w, h = rgba.size
    px = rgba.load()

    def near(c, s, t):
        return abs(c[0] - s[0]) <= t and abs(c[1] - s[1]) <= t and abs(c[2] - s[2]) <= t

    def near_any(c, t):
        return any(near(c, s, t) for s in seeds)

    seen = bytearray(w * h)
    queue = deque()
    for x in range(w):
        for y in (0, h - 1):
            if not seen[y * w + x] and near_any(px[x, y], tol):
                seen[y * w + x] = 1; queue.append((x, y))
    for y in range(h):
        for x in (0, w - 1):
            if not seen[y * w + x] and near_any(px[x, y], tol):
                seen[y * w + x] = 1; queue.append((x, y))
    while queue:
        x, y = queue.popleft()
        for nx, ny in ((x+1,y),(x-1,y),(x,y+1),(x,y-1)):
            if 0 <= nx < w and 0 <= ny < h and not seen[ny * w + nx] and near_any(px[nx, ny], tol):
                seen[ny * w + nx] = 1; queue.append((nx, ny))
    removed = 0
    for i in range(w * h):
        if seen[i]:
            x, y = i % w, i // w
            r, g, b, a = px[x, y]
            px[x, y] = (r, g, b, 0); removed += 1
    # 1px halo cleanup: opaque pixels adjacent to keyed area and near a seed (loose tol)
    halo = []
    for y in range(h):
        for x in range(w):
            if seen[y * w + x]:
                continue
            r, g, b, a = px[x, y]
            if a == 0:
                continue
            for nx, ny in ((x+1,y),(x-1,y),(x,y+1),(x,y-1)):
                if 0 <= nx < w and 0 <= ny < h and seen[ny * w + nx]:
                    if near_any((r, g, b), halo_tol):
                        halo.append((x, y))
                    break
    for x, y in halo:
        r, g, b, a = px[x, y]
        px[x, y] = (r, g, b, 0); removed += 1
    return rgba, removed / (w * h)


def alpha_bbox(im):
    return im.getbbox()  # uses alpha channel for RGBA


SINGLE_SPRITE_SLOTS = {"A01_GARDENER_DRONE", "T02_RESEARCH_TERMINAL", "W01_SECTOR_DOOR",
                       "D01_DEXTER_VENDOR", "D02_DEXTER_VENDOR_KIOSK"}

# logical grid contracts for multi-cell sheets, measured on the final game_ready raster
SHEET_TOPOLOGY = {
    # crop growth strips: four consecutive 32x32 cells, planter at cell bottom in every cell
    "C01_WISDOM_FRUIT":   dict(rows=1, cols=4, cw=32, ch=32, exp=[[1, 1, 1, 1]], planter=True),
    "C02_TRICKSTER_VINE": dict(rows=1, cols=4, cw=32, ch=32, exp=[[1, 1, 1, 1]], planter=True),
    "C03_LIGHTNING_VINE": dict(rows=1, cols=4, cw=32, ch=32, exp=[[1, 1, 1, 1]], planter=True),
    "C04_SHADOW_ROOT":    dict(rows=1, cols=4, cw=32, ch=32, exp=[[1, 1, 1, 1]], planter=True),
    "C05_GOLDEN_BLOSSOM": dict(rows=1, cols=4, cw=32, ch=32, exp=[[1, 1, 1, 1]], planter=True),
    # four isolated VFX cells
    "V01_CORE_VFX":       dict(rows=1, cols=4, cw=32, ch=32, exp=[[1, 1, 1, 1]]),
    # five 16x16 HUD icon cells
    "U01_HUD_ICONS":      dict(rows=1, cols=5, cw=16, ch=16, exp=[[1, 1, 1, 1, 1]]),
    # player sheet: 6 cols x 4 rows of 32x48; per Player.tscn rows idle x4 / walk x6 / jump-fall-land / interact x2
    "P01_PLAYER_SHEET":   dict(rows=4, cols=6, cw=32, ch=48, baseline=True,
                               exp=[[1, 1, 1, 1, 0, 0], [1, 1, 1, 1, 1, 1],
                                    [1, 1, 1, 0, 0, 0], [1, 1, 0, 0, 0, 0]]),
    # two-terminal pair: LEFT repair (copper/warm), RIGHT replenish (teal/cool), each 32x64
    "T01_REPAIR_REPLENISH_TERMINALS": dict(rows=1, cols=2, cw=32, ch=64, exp=[[1, 1]], halves=True),
}


def analyze_sheet_topology(slot_id, gr_path, src_path):
    """Deterministic per-cell topology check of the final game_ready raster against the
    slot's logical grid contract. Flags only; never modifies the image."""
    t = SHEET_TOPOLOGY[slot_id]
    flags, notes = set(), []
    gr = Image.open(gr_path).convert("RGBA")
    if gr.size != (t["cols"] * t["cw"], t["rows"] * t["ch"]):
        notes.append(f"sheet topology not checked: game_ready {gr.size[0]}x{gr.size[1]} != "
                     f"logical grid canvas {t['cols']*t['cw']}x{t['rows']*t['ch']}")
        return flags, notes
    px = gr.load()
    occ = [[0.0] * t["cols"] for _ in range(t["rows"])]
    bottoms = []
    for r in range(t["rows"]):
        for c in range(t["cols"]):
            n = op = 0
            for y in range(r * t["ch"], (r + 1) * t["ch"]):
                for x in range(c * t["cw"], (c + 1) * t["cw"]):
                    n += 1
                    if px[x, y][3] > 0:
                        op += 1
            occ[r][c] = op / n
    shares = " / ".join(" ".join(f"{v:.0%}" for v in row) for row in occ)
    notes.append(f"sheet cell opaque shares (row-major): {shares}")

    empty_bad, occ_bad = [], []
    for r in range(t["rows"]):
        for c in range(t["cols"]):
            if t["exp"][r][c] == 0 and occ[r][c] > 0.25:
                empty_bad.append(f"r{r+1}c{c+1}={occ[r][c]:.0%}")
            if t["exp"][r][c] == 1 and occ[r][c] < 0.04:
                occ_bad.append(f"r{r+1}c{c+1}={occ[r][c]:.0%}")
    if empty_bad:
        flags.add("EMPTY_CELLS_OPAQUE")
        notes.append("cells that must stay transparent are opaque in game_ready: " + ", ".join(empty_bad))
        # root cause: is the SOURCE's flat background a different color from its border frame,
        # so border-seeded flood keying could not reach the interior?
        try:
            src = Image.open(src_path).convert("RGB")
            sw, sh = src.size
            sp = src.load()
            flat_ok = True
            for r in range(t["rows"]):
                for c in range(t["cols"]):
                    if t["exp"][r][c] != 0:
                        continue
                    from collections import Counter
                    cnt = Counter()
                    for y in range(int(r * sh / t["rows"]), max(int(r * sh / t["rows"]) + 1, int((r + 1) * sh / t["rows"]))):
                        for x in range(int(c * sw / t["cols"]), max(int(c * sw / t["cols"]) + 1, int((c + 1) * sw / t["cols"]))):
                            cnt[(sp[x, y][0] // 16, sp[x, y][1] // 16, sp[x, y][2] // 16)] += 1
                    if not cnt or cnt.most_common(1)[0][1] / sum(cnt.values()) < 0.80:
                        flat_ok = False
            if flat_ok:
                flags.add("KEYING_INCOMPLETE_FRAMED_SOURCE")
                notes.append("source empty cells are >=80% a single flat color (the sheet background), but the "
                             "source border is a different color (dark frame), so border-seeded flood keying "
                             "removed only the frame and left the interior background opaque; re-key from the "
                             "interior background color before slicing")
            else:
                flags.add("SOURCE_TOPOLOGY_MISMATCH")
                notes.append("source empty cells are not a single flat background color; generated sheet does "
                             "not follow the required empty-cell topology")
        except Exception as e:
            notes.append(f"source empty-cell flatness check failed: {e}")
    if occ_bad:
        flags.add("EXPECTED_CELL_EMPTY")
        notes.append("cells that must contain a frame/prop are (near-)empty in game_ready: " + ", ".join(occ_bad))

    if t.get("planter"):
        # lifecycle strips: planter band = bottom 10px of each 32px cell, must stay put across cells
        band = 10
        b0 = [[px[x, y][3] > 0 for x in range(0, t["cw"])]
              for y in range(t["ch"] - band, t["ch"])]
        ious = []
        for c in range(1, t["cols"]):
            inter = union = 0
            for yi in range(band):
                for xi in range(t["cw"]):
                    v = px[xi + c * t["cw"], yi + t["ch"] - band][3] > 0
                    inter += 1 if (b0[yi][xi] and v) else 0
                    union += 1 if (b0[yi][xi] or v) else 0
            ious.append(inter / union if union else 0.0)
        notes.append("planter-band IoU vs cell1: " + " ".join(f"c{c+2}={v:.2f}" for c, v in enumerate(ious)))
        if ious and min(ious) < 0.50:
            flags.add("PLANTER_BAND_INCONSISTENT")
        drops = [occ[0][c] - occ[0][c + 1] for c in range(t["cols"] - 1)]
        if any(d > 0.10 for d in drops):
            flags.add("LIFECYCLE_OCCUPANCY_NON_MONOTONIC")
            notes.append("crop strip cell occupancy decreases by >10% between consecutive stages")

    if t.get("baseline"):
        for r in range(t["rows"]):
            for c in range(t["cols"]):
                if not t["exp"][r][c]:
                    continue
                for y in range(t["ch"] - 1, -1, -1):
                    if any(px[x, y + r * t["ch"]][3] > 0 for x in range(c * t["cw"], (c + 1) * t["cw"])):
                        bottoms.append(y)
                        break
        if bottoms:
            spread = max(bottoms) - min(bottoms)
            notes.append(f"occupied-cell content bottom rows: min={min(bottoms)} max={max(bottoms)} "
                         f"(cell height {t['ch']}, spread {spread})")
            if spread > 6:
                flags.add("PLAYER_BASELINE_MISALIGNED")

    if t.get("halves"):
        mid = t["cw"]
        lw = sum(1 for y in range(t["ch"]) for x in range(0, mid) if px[x, y][3] > 0)
        rw = sum(1 for y in range(t["ch"]) for x in range(mid, 2 * mid) if px[x, y][3] > 0)
        if lw < 0.04 * mid * t["ch"] or rw < 0.04 * mid * t["ch"]:
            flags.add("TERMINAL_HALF_MISSING")
        # bridging: one connected component with substantial pixels in both halves
        seen = {}
        comps = []
        for y0 in range(t["ch"]):
            for x0 in range(2 * mid):
                if px[x0, y0][3] > 0 and (x0, y0) not in seen:
                    comp = [(x0, y0)]
                    seen[(x0, y0)] = len(comps)
                    stack = [(x0, y0)]
                    while stack:
                        x, y = stack.pop()
                        for nx, ny in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
                            if 0 <= nx < 2 * mid and 0 <= ny < t["ch"] and px[nx, ny][3] > 0 and (nx, ny) not in seen:
                                seen[(nx, ny)] = len(comps)
                                comp.append((nx, ny))
                                stack.append((nx, ny))
                    comps.append(comp)
        for i, comp in enumerate(comps):
            l = sum(1 for x, y in comp if x < mid)
            rr = sum(1 for x, y in comp if x >= mid)
            if comp and min(l, rr) > 0.05 * len(comp) and l > 0.10 * lw and rr > 0.10 * rw:
                flags.add("TERMINAL_HALVES_BRIDGED")
                notes.append(f"component {i+1} spans both halves ({l}px left / {rr}px right)")
                break
        # theme colors: LEFT repair = copper/warm, RIGHT replenish = teal/cool
        warm_l = cool_l = warm_r = cool_r = nl = nr = 0
        for y in range(t["ch"]):
            for x in range(2 * mid):
                r_, g_, b_ = px[x, y][:3]
                if px[x, y][3] > 0:
                    if x < mid:
                        nl += 1
                        warm_l += 1 if (r_ > g_ + 20 and r_ > b_ + 20) else 0
                        cool_l += 1 if (b_ > r_ + 20 or g_ > r_ + 20) else 0
                    else:
                        nr += 1
                        warm_r += 1 if (r_ > g_ + 20 and r_ > b_ + 20) else 0
                        cool_r += 1 if (b_ > r_ + 20 or g_ > r_ + 20) else 0
        if nl and nr:
            notes.append(f"half theme colors: left warm={warm_l/nl:.0%} cool={cool_l/nl:.0%}; "
                         f"right warm={warm_r/nr:.0%} cool={cool_r/nr:.0%} (left should be warm/copper, right cool/teal)")
    return flags, notes


def count_major_islands(rgba, min_share=0.10, sample_max=512):
    """Number of disconnected opaque islands each covering >= min_share of opaque pixels.
    Deterministic; downsampled for speed. Used to flag multi-subject single-sprite sources."""
    im = rgba.convert("RGBA")
    w, h = im.size
    if max(w, h) > sample_max:
        sc = sample_max / max(w, h)
        im = im.resize((max(1, int(w * sc)), max(1, int(h * sc))), Image.NEAREST)
        w, h = im.size
    a = im.getchannel("A")
    px = a.load()
    total_opaque = sum(1 for y in range(h) for x in range(w) if px[x, y] > 16)
    if total_opaque == 0:
        return 0
    thresh = total_opaque * min_share
    seen = bytearray(w * h)
    major = 0
    for y0 in range(h):
        for x0 in range(w):
            i0 = y0 * w + x0
            if seen[i0] or px[x0, y0] <= 16:
                continue
            size = 0
            stack = [(x0, y0)]
            seen[i0] = 1
            while stack:
                x, y = stack.pop()
                size += 1
                for nx, ny in ((x+1,y),(x-1,y),(x,y+1),(x,y-1)):
                    if 0 <= nx < w and 0 <= ny < h:
                        j = ny * w + nx
                        if not seen[j] and px[nx, ny] > 16:
                            seen[j] = 1
                            stack.append((nx, ny))
            if size >= thresh:
                major += 1
    return major


def make_game_ready(slot_id, src):
    """Deterministic normalization. Returns (img_or_None, flags, notes)."""
    s = SLOTS[slot_id]
    tw, th = s["w"], s["h"]
    flags, notes = set(), []
    im = Image.open(src)
    im.load()
    opaque_src = im.mode in ("RGB", "L", "P")
    alpha_expected = s["alpha"]

    # --- background removal for sprites/props/sheets that want alpha ---
    if alpha_expected:
        seeds = border_seed_colors(im)
        if seeds:
            rgba, removed = flood_key(im, seeds)
            notes.append(f"flood-keyed border background (seeds={len(seeds)}, removed {removed:.1%})")
            flags.add("BACKGROUND_REMOVED")
            base = rgba
        else:
            base = im.convert("RGBA")
            flags.add("OPAQUE_BACKGROUND")
            flags.add("CONVERSION_REQUIRED")
            notes.append("no flat border color found; kept opaque")
        bbox = base.getbbox()
        if bbox:
            bw, bh = bbox[2] - bbox[0], bbox[3] - bbox[1]
            if (bw / im.width < 0.12) or (bh / im.height < 0.12):
                notes.append(f"subject occupies only {bw}x{bh} of {im.width}x{im.height} source frame; "
                             f"consider regeneration for detail retention")
        if slot_id in SINGLE_SPRITE_SLOTS:
            islands = count_major_islands(base)
            if islands >= 2:
                flags.add("MULTIPLE_SUBJECTS_POSSIBLE")
                notes.append(f"deterministic island analysis found {islands} major opaque islands in a "
                             f"single-sprite slot; source may contain repeated subjects")
    else:
        base = im.convert("RGB")

    bbox = base.getbbox() if alpha_expected else None

    def contain_fit(img, cw, ch):
        """Aspect-preserving NEAREST fit centered in cw x ch canvas."""
        w, h = img.size
        sc = min(cw / w, ch / h)
        nw, nh = max(1, round(w * sc)), max(1, round(h * sc))
        out = img.resize((nw, nh), Image.NEAREST)
        canvas = Image.new("RGBA" if img.mode == "RGBA" else "RGB", (cw, ch),
                           (0, 0, 0, 0) if img.mode == "RGBA" else (10, 14, 26, 255))
        canvas.paste(out, ((cw - nw) // 2, (ch - nh) // 2))
        return canvas, sc

    def anchored_fit(img, cw, ch):
        """Aspect-preserving NEAREST fit, bottom-center anchored, transparent padding."""
        w, h = img.size
        sc = min(cw / w, ch / h)
        nw, nh = max(1, round(w * sc)), max(1, round(h * sc))
        out = img.resize((nw, nh), Image.NEAREST)
        canvas = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
        canvas.paste(out, ((cw - nw) // 2, ch - nh))
        return canvas, sc

    if slot_id in ("B01_GREENHOUSE_BACKGROUND", "B02_ENGINEERING_BACKGROUND"):
        # center-crop to 16:9 then nearest to 640x360
        w, h = base.size
        target_ar = tw / th
        if abs(w / h - target_ar) > 0.01:
            if w / h > target_ar:
                nw = int(h * target_ar); x0 = (w - nw) // 2
                base = base.crop((x0, 0, x0 + nw, h))
            else:
                nh = int(w / target_ar); y0 = (h - nh) // 2
                base = base.crop((0, y0, w, y0 + nh))
            flags.add("CROPPED_CONTENT")
            notes.append("center-cropped to 16:9")
        out = base.resize((tw, th), Image.NEAREST)
        flags.add("CONVERSION_REQUIRED")
        return out, flags, notes

    if slot_id in ("E01_GREENHOUSE_TILESET", "E02_ENGINEERING_TILESET"):
        # grid contract needs exact square source aspect; aspect-preserving fit otherwise
        w, h = base.size
        ar = w / h
        if abs(ar - 1.0) <= 0.02:
            out = base.resize((tw, th), Image.NEAREST)
            flags.add("CONVERSION_REQUIRED")
            notes.append(f"square source downscaled {w}x{h} -> {tw}x{th}; 16x16 grid preserved proportionally")
            return out, flags, notes
        out, sc = contain_fit(base, tw, th)
        flags.add("FRAME_LAYOUT_INVALID")
        flags.add("CONVERSION_REQUIRED")
        notes.append(f"source aspect {ar:.3f} != 1.0; grid contract 16x16 tiles cannot be honored; "
                     f"game_ready is aspect-preserving fit only (scale {sc:.4f}); use source for manual reslicing")
        return out, flags, notes

    if alpha_expected:
        # sprite / prop / strip: work on keyed+cropped content, bottom-center anchor into target canvas
        content = base.crop(bbox) if bbox else base
        cw, ch = content.size
        out, sc = anchored_fit(content, tw, th)
        flags.add("CONVERSION_REQUIRED")
        if sc > 1:
            notes.append(f"content upscaled x{sc:.3f} (NEAREST) into {tw}x{th} canvas, bottom-center anchor")
        else:
            notes.append(f"content downscaled x{sc:.4f} (NEAREST) into {tw}x{th} canvas, bottom-center anchor")
        if slot_id in ("C01_WISDOM_FRUIT", "C02_TRICKSTER_VINE", "C03_LIGHTNING_VINE",
                       "C04_SHADOW_ROOT", "C05_GOLDEN_BLOSSOM", "V01_CORE_VFX",
                       "U01_HUD_ICONS", "P01_PLAYER_SHEET", "T01_REPAIR_REPLENISH_TERMINALS"):
            flags.add("FRAME_LAYOUT_UNCERTAIN")
            notes.append("multi-cell/strip sheet: generated source is a single raster; per-cell topology "
                         "not deterministically guaranteed; review before slicing")
        if sc < 0.2:
            flags.add("UNREADABLE_AT_TARGET_SCALE")
        return out, flags, notes

    # opaque non-background fallback (should not happen)
    out, sc = contain_fit(base, tw, th)
    return out, flags, notes


def process_candidate(slot_id, cid):
    d = os.path.join(ROOT, "slots", slot_id, cid)
    src = os.path.join(d, "source.png")
    s = SLOTS[slot_id]
    rec = {
        "project": PROJECT, "slot_id": slot_id, "candidate_id": cid, "priority": s["priority"],
        "source_file": None, "game_ready_file": None, "generation_status": "pending",
        "technical_status": "FAIL", "actual_source_width": None, "actual_source_height": None,
        "actual_game_width": None, "actual_game_height": None,
        "expected_width": s["w"], "expected_height": s["h"],
        "expected_frame_layout": s["layout"], "alpha_present": None,
        "sha256_source": None, "sha256_game_ready": None,
        "generation_prompt": full_prompt(slot_id, candidate_ids(slot_id).index(cid)),
        "technical_flags": [], "notes": [], "selected": False, "rejected": False,
        "live_asset_replaced": False,
    }
    if not os.path.exists(src) or os.path.getsize(src) == 0:
        rec["generation_status"] = "not_generated" if not os.path.exists(src) else "failed"
        rec["technical_flags"] = ["GENERATION_FAILED"] if os.path.exists(src) else ["NOT_GENERATED"]
        rec["notes"] = ["source.png missing or empty"]
        write_json(os.path.join(d, "candidate.json"), rec)
        return rec
    rec["source_file"] = os.path.relpath(src, ROOT)
    rec["generation_status"] = "generated"
    rec["sha256_source"] = sha256(src)
    try:
        im = Image.open(src); im.load()
    except Exception as e:
        rec["generation_status"] = "failed"
        rec["technical_flags"] = ["SOURCE_NOT_PNG", "UNDECODABLE"]
        rec["notes"] = [f"decode error: {e}"]
        write_json(os.path.join(d, "candidate.json"), rec)
        return rec
    rec["actual_source_width"], rec["actual_source_height"] = im.size
    rec["alpha_present"] = (im.mode == "RGBA" and im.getextrema()[3][0] < 255)
    flags, notes = set(), []
    if im.format != "PNG":
        flags.add("SOURCE_NOT_PNG")
    if SLOTS[slot_id]["alpha"] and not rec["alpha_present"]:
        flags.add("NO_ALPHA")
    try:
        gr, gflags, gnotes = make_game_ready(slot_id, src)
        gp = os.path.join(d, "game_ready.png")
        gr.save(gp, "PNG", optimize=True)
        rec["game_ready_file"] = os.path.relpath(gp, ROOT)
        rec["sha256_game_ready"] = sha256(gp)
        gim = Image.open(gp); gim.load()
        rec["actual_game_width"], rec["actual_game_height"] = gim.size
        rec["alpha_present"] = rec["alpha_present"] or (gim.mode == "RGBA" and gim.getextrema()[3][0] < 255)
        flags |= gflags
        notes += gnotes
        if (rec["actual_game_width"], rec["actual_game_height"]) != (s["w"], s["h"]):
            flags.add("WRONG_DIMENSIONS")
        if slot_id in SHEET_TOPOLOGY:
            try:
                tflags, tnotes = analyze_sheet_topology(slot_id, gp, src)
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
    write_json(os.path.join(d, "candidate.json"), rec)
    return rec


def write_json(path, obj):
    with open(path, "w") as f:
        json.dump(obj, f, indent=2)


def main():
    all_recs = []
    for sid in SLOT_ORDER:
        for cid in candidate_ids(sid):
            all_recs.append(process_candidate(sid, cid))
    gen = [r for r in all_recs if r["generation_status"] == "generated"]
    val = [r for r in gen if r["actual_game_width"]]
    by_status = Counter(r["technical_status"] for r in gen)
    manifest = {
        "project": PROJECT, "run_id": RUN_ID, "timestamp": "2026-09-20",
        "repository_commit_baseline": "97544d74d534b75472bfa99ee79439ba5752c9cf",
        "target_candidate_count": len(all_recs),
        "generated_count": len(gen),
        "validated_count": len(val),
        "failed_count": len(all_recs) - len(gen),
        "technical_status_counts": dict(by_status),
        "slots": SLOT_ORDER,
        "candidates": [{k: r[k] for k in (
            "slot_id", "candidate_id", "priority", "generation_status", "technical_status",
            "source_file", "game_ready_file", "actual_source_width", "actual_source_height",
            "actual_game_width", "actual_game_height", "expected_width", "expected_height",
            "alpha_present", "sha256_source", "sha256_game_ready", "technical_flags")} for r in all_recs],
    }
    write_json(os.path.join(ROOT, "GENERATION_MANIFEST.json"), manifest)
    print(f"candidates={len(all_recs)} generated={len(gen)} validated={len(val)} "
          f"failed={manifest['failed_count']} status={dict(by_status)}")
    build_review(all_recs)


def build_review(recs):
    """Rebuild review.html with embedded candidate index (images via relative paths)."""
    items = []
    for r in recs:
        if r["generation_status"] != "generated":
            continue
        sid = r["slot_id"]
        s = SLOTS[sid]
        rel = os.path.dirname(os.path.relpath(os.path.join(ROOT, r["source_file"]), ROOT))
        items.append({
            "cid": r["candidate_id"], "slot": sid, "priority": r["priority"],
            "src": f"{rel}/source.png", "ready": (f"{rel}/game_ready.png" if r["game_ready_file"] else None),
            "sw": r["actual_source_width"], "sh": r["actual_source_height"],
            "gw": r["actual_game_width"], "gh": r["actual_game_height"],
            "ew": r["expected_width"], "eh": r["expected_height"],
            "status": r["technical_status"], "flags": r["technical_flags"],
            "notes": r["notes"], "prompt": r["generation_prompt"],
            "layout": r["expected_frame_layout"],
        })
    html = REVIEW_TEMPLATE.replace("__DATA__", json.dumps(items))
    with open(os.path.join(ROOT, "review.html"), "w") as f:
        f.write(html)
    print(f"review.html rebuilt with {len(items)} candidates")


REVIEW_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Starlight Acre — Candidate Review</title>
<style>
  :root{
    --navy:#0A0E1A; --dusk:#1E2D4A; --teal:#2E8B8B; --moss:#4F7942; --gold:#D4AF37;
    --copper:#B87333; --gray:#708090; --bone:#F5F5DC;
  }
  *{box-sizing:border-box}
  body{margin:0;background:var(--navy);color:var(--bone);
       font-family:"Courier New",ui-monospace,monospace;font-size:13px}
  header{padding:10px 16px;border-bottom:1px solid #1E2D4A;display:flex;gap:18px;align-items:center;flex-wrap:wrap}
  header h1{font-size:15px;margin:0;color:var(--gold);letter-spacing:2px}
  header .sub{color:var(--gray)}
  #filters{display:flex;gap:6px;flex-wrap:wrap}
  button{background:var(--dusk);color:var(--bone);border:1px solid #2E8B8B55;padding:4px 10px;
         cursor:pointer;font-family:inherit;font-size:12px;border-radius:2px}
  button:hover{border-color:var(--teal)}
  button.on{background:var(--teal);color:#06110f;border-color:var(--teal);font-weight:bold}
  #slotNav{display:flex;gap:4px;flex-wrap:wrap;padding:8px 16px;border-bottom:1px solid #1E2D4A}
  #slotNav button{font-size:11px;padding:3px 8px}
  #slotNav button .n{color:var(--gold)}
  main{display:flex;min-height:calc(100vh - 96px)}
  #stage{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;
         padding:18px;position:relative}
  #canvasWrap{position:relative;background:transparent;
              image-rendering:pixelated;image-rendering:crisp-edges}
  #canvasWrap.checker{background:
     repeating-conic-gradient(#141a2b 0% 25%, #1b2337 0% 50%) 0 0/16px 16px}
  #stage img{image-rendering:pixelated;image-rendering:crisp-edges;display:block}
  #meta{position:absolute;left:16px;top:12px;line-height:1.6}
  #meta .cid{color:var(--gold);font-size:15px;letter-spacing:1px}
  #meta .dim{color:var(--teal)}
  #meta .flags{color:var(--copper);max-width:420px}
  #zoom{position:absolute;right:16px;top:12px;display:flex;gap:6px;align-items:center}
  #verdict{position:absolute;right:16px;bottom:14px;display:flex;gap:8px}
  #verdict button{min-width:74px}
  #verdict .keep.on{background:var(--moss);border-color:var(--moss);color:#eafbe7}
  #verdict .maybe.on{background:var(--gold);border-color:var(--gold);color:#241d05}
  #verdict .reject.on{background:#7a2e2e;border-color:#7a2e2e}
  #promptBox{max-height:120px;overflow:auto;background:#0d1322;border:1px solid #1E2D4A;
             padding:8px;margin-top:10px;color:#9fb0c8;font-size:11px;display:none}
  #promptBox.open{display:block}
  #cmp{display:none;gap:24px;align-items:flex-end;justify-content:center;width:100%}
  #cmp .cell{text-align:center}
  #cmp .cell .lbl{color:var(--gold);margin-bottom:6px}
  #abBar{position:absolute;left:16px;bottom:14px;display:flex;gap:8px;align-items:center}
  #abBar select{background:var(--dusk);color:var(--bone);border:1px solid #2E8B8B55;font-family:inherit;padding:3px}
  .tag{display:inline-block;padding:1px 6px;border:1px solid;margin-left:6px;font-size:10px}
  .tag.PASS{color:var(--moss);border-color:var(--moss)}
  .tag.PASS_WITH_FLAGS{color:var(--gold);border-color:var(--gold)}
  .tag.FAIL{color:#e07070;border-color:#e07070}
</style>
</head>
<body>
<header>
  <h1>ST★RLIGHT ACRE</h1><span class="sub">candidate foundry review — nothing here is live</span>
  <div id="filters"></div>
  <span class="sub" id="count"></span>
  <button id="promptToggle">prompt</button>
  <button id="checkerToggle">checker</button>
  <button id="srcToggle">view: game_ready</button>
  <button id="sizeToggle">zoom 1:1</button>
  <button id="cmpToggle">A/B</button>
  <button id="exportBtn">EXPORT SELECTIONS</button>
</header>
<div id="slotNav"></div>
<main>
  <div id="stage">
    <div id="meta"></div>
    <div id="zoom">
      <button id="zOut">−</button><span id="zLbl">4x</span><button id="zIn">+</button>
      <button id="abA">set A</button><button id="abB">set B</button>
    </div>
    <div id="cmp"></div>
    <div id="canvasWrap" class="checker"><img id="img" alt=""></div>
    <div id="promptBox"></div>
    <div id="abBar"></div>
    <div id="verdict">
      <button class="keep" data-v="keep">KEEP (K)</button>
      <button class="maybe" data-v="maybe">MAYBE (M)</button>
      <button class="reject" data-v="reject">REJECT (R)</button>
      <button data-v="unsorted">UNSORTED (U)</button>
    </div>
  </div>
</main>
<script>
const DATA = __DATA__;
const SLOT_ORDER = [...new Set(DATA.map(d=>d.slot))];
const store = {
  get v(){ try{return JSON.parse(localStorage.getItem('sa_review_v1'))||{}}catch(e){return{}} },
  set(k,val){ const s=this.v; s[k]=val; localStorage.setItem('sa_review_v1',JSON.stringify(s)); render(); },
  verdict(cid){ return this.v['v:'+cid]||'unsorted'; }
};
let slotFilter='ALL', statusFilter='ALL', idx=0, zoom=null, showSrc=false, checker=true,
    promptOpen=false, cmpMode=false, abA=null, abB=null;

function list(){
  return DATA.filter(d=>(slotFilter==='ALL'||d.slot===slotFilter))
             .filter(d=>{
               const v=store.verdict(d.cid);
               if(statusFilter==='ALL')return true;
               if(['keep','maybe','reject','unsorted'].includes(statusFilter)) return v===statusFilter;
               return d.status===statusFilter;
             });
}
function zoomFor(d){ if(zoom)return zoom;
  const vw=Math.min(window.innerWidth-420, 1100), vh=window.innerHeight-260;
  const s=Math.max(1,Math.min(Math.floor(vw/d.ew)||1, Math.floor(vh/d.eh)||1));
  const s2=Math.min(vw/d.ew, vh/d.eh); return s2>1? Math.max(1,s) : Math.max(0.2,s2);
}
function render(){
  const L=list(); if(idx>=L.length)idx=L.length-1; if(idx<0)idx=0;
  document.getElementById('count').textContent = L.length+' / '+DATA.length+' candidates';
  // slot nav
  const nav=document.getElementById('slotNav'); nav.innerHTML='';
  const mk=(id,label,n)=>{const b=document.createElement('button');b.textContent=(label||id)+ (n!==undefined?' ('+n+')':'');
    b.onclick=()=>{slotFilter=id;idx=0;render();}; if(slotFilter===id)b.classList.add('on'); nav.appendChild(b);};
  mk('ALL','ALL',DATA.length);
  for(const s of SLOT_ORDER){ const n=DATA.filter(d=>d.slot===s).length; mk(s,null,n); }
  // filters
  const fl=document.getElementById('filters'); fl.innerHTML='';
  for(const f of ['ALL','UNSORTED','KEEP','MAYBE','REJECT','PASS','PASS_WITH_FLAGS','FAIL']){
    const b=document.createElement('button'); b.textContent=f;
    b.onclick=()=>{statusFilter=f;render();}; if(statusFilter===f)b.classList.add('on'); fl.appendChild(b);
  }
  const d=L[idx]; const wrap=document.getElementById('canvasWrap'); const img=document.getElementById('img');
  const cmp=document.getElementById('cmp');
  document.getElementById('abBar').style.display=cmpMode?'flex':'none';
  cmp.style.display=cmpMode?'flex':'none';
  wrap.style.display=cmpMode?'none':'block';
  if(!d){img.removeAttribute('src');document.getElementById('meta').innerHTML='no candidates match';return;}
  const z=zoomFor(d), w=Math.round((showSrc?d.sw:d.gw||d.ew)*z), h=Math.round((showSrc?d.sh:d.gh||d.eh)*z);
  if(!cmpMode){
    img.src = (showSrc||!d.ready)? d.src : d.ready;
    img.style.width=w+'px'; img.style.height=h+'px';
    wrap.style.width=w+'px'; wrap.style.height=h+'px';
    document.getElementById('zLbl').textContent=(Math.round(z*100)/100)+'x';
  } else {
    cmp.innerHTML='';
    for(const [lbl,c] of [['A',abA],['B',abB]]){
      const cd=DATA.find(x=>x.cid===c);
      const cell=document.createElement('div');cell.className='cell';
      cell.innerHTML='<div class="lbl">'+(cd?cd.cid:'— set with “set A/B” —')+'</div>';
      if(cd){const im2=document.createElement('img');
        const z2=zoomFor(d); im2.src=(showSrc||!cd.ready)?cd.src:cd.ready;
        im2.style.width=Math.round((showSrc?cd.sw:cd.gw||cd.ew)*z2)+'px';
        im2.style.height=Math.round((showSrc?cd.sh:cd.gh||cd.eh)*z2)+'px';
        cell.appendChild(im2);}
      cmp.appendChild(cell);
    }
  }
  const v=store.verdict(d.cid);
  document.getElementById('meta').innerHTML =
    '<span class="cid">'+d.cid+'</span><span class="tag '+d.status+'">'+d.status+'</span><br>'+
    '<span class="dim">expected '+d.ew+'x'+d.eh+'</span> · source '+d.sw+'x'+d.sh+
    ' · game_ready '+(d.gw?d.gw+'x'+d.gh:'none')+'<br>'+
    '<span class="flags">'+(d.flags.length?d.flags.join(' · '):'no flags')+'</span><br>'+
    '<span style="color:#7f8ea6">'+d.layout+'</span>';
  const pb=document.getElementById('promptBox'); pb.classList.toggle('open',promptOpen);
  pb.textContent=d.prompt;
  document.querySelectorAll('#verdict button').forEach(b=>{
    b.classList.toggle('on', b.dataset.v===v || (b.dataset.v==='unsorted'&&v==='unsorted'));
  });
  // A/B selects
  const ab=document.getElementById('abBar');
  ab.innerHTML='A/B compare (same slot): '+selHtml('abSelA',abA,d)+' '+selHtml('abSelB',abB,d)+
    '<button onclick="abA=null;abB=null;render()">clear</button>';
}
function setAB(which,val){ if(which==='A')abA=val||null; else abB=val||null; }
function selHtml(id,val,d){
  const which = id==='abSelA' ? 'A' : 'B';
  const opts=['<option value="">—</option>'].concat(
    DATA.filter(x=>x.slot===d.slot).map(x=>'<option value="'+x.cid+'"'+(x.cid===val?' selected':'')+'>'+x.cid+'</option>')
  ).join('');
  return '<select id="'+id+'" onchange="setAB(\''+which+'\',this.value);render()">'+opts+'</select>';
}
document.getElementById('verdict').addEventListener('click',e=>{
  const b=e.target.closest('button'); if(!b)return; const d=list()[idx]; if(!d)return;
  store.set('v:'+d.cid, b.dataset.v);
});
document.getElementById('promptToggle').onclick=()=>{promptOpen=!promptOpen;render();};
document.getElementById('checkerToggle').onclick=()=>{checker=!checker;
  document.getElementById('canvasWrap').classList.toggle('checker',checker);};
document.getElementById('srcToggle').onclick=()=>{showSrc=!showSrc;
  document.getElementById('srcToggle').textContent='view: '+(showSrc?'raw source':'game_ready');render();};
document.getElementById('sizeToggle').onclick=()=>{ zoom = zoom===null ? 1 : null; render();
  document.getElementById('sizeToggle').textContent = zoom ? 'zoom fit' : 'zoom 1:1';};
document.getElementById('zIn').onclick=()=>{zoom=zoomFor(list()[idx])*1.5; if(zoom>40)zoom=40;render();};
document.getElementById('zOut').onclick=()=>{zoom=zoomFor(list()[idx])/1.5; if(zoom<0.1)zoom=0.1;render();};
document.getElementById('abA').onclick=()=>{const d=list()[idx]; if(d){abA=d.cid; render();}};
document.getElementById('abB').onclick=()=>{const d=list()[idx]; if(d){abB=d.cid; cmpMode=true; document.getElementById('cmpToggle').classList.add('on'); render();}};
document.getElementById('cmpToggle').onclick=()=>{cmpMode=!cmpMode;
  document.getElementById('cmpToggle').classList.toggle('on',cmpMode);
  if(cmpMode){const L=list();abA=abA||L[Math.max(0,idx-1)]?.cid;abB=abB||L[idx]?.cid;}render();};
document.getElementById('exportBtn').onclick=()=>{
  const out={exported:new Date().toISOString(), tool:'starlight-acre candidate review',
             note:'review decisions only; nothing here is canonical production art', decisions:{}};
  for(const d of DATA){ out.decisions[d.cid]={slot:d.slot, verdict:store.verdict(d.cid)}; }
  const blob=new Blob([JSON.stringify(out,null,2)],{type:'application/json'});
  const a=document.createElement('a'); a.href=URL.createObjectURL(blob);
  a.download='selections.json'; a.click(); URL.revokeObjectURL(a.href);
};
window.addEventListener('keydown',e=>{
  if(e.target.tagName==='SELECT')return;
  const d=list()[idx];
  switch(e.key){
    case 'ArrowLeft': idx--; render(); e.preventDefault(); break;
    case 'ArrowRight': idx++; render(); e.preventDefault(); break;
    case 'k': case 'K': if(d)store.set('v:'+d.cid,'keep'); break;
    case 'm': case 'M': if(d)store.set('v:'+d.cid,'maybe'); break;
    case 'r': case 'R': if(d)store.set('v:'+d.cid,'reject'); break;
    case 'u': case 'U': if(d)store.set('v:'+d.cid,'unsorted'); break;
    case 'a': case 'A': abA=d.cid; render(); break;
    case 'b': case 'B': abB=d.cid; render(); break;
    case 'p': case 'P': promptOpen=!promptOpen; render(); break;
  }
});
render();
</script>
</body>
</html>
"""

if __name__ == "__main__":
    main()
