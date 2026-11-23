"""Compare every PROVES footprint with the footprint it replaces on the six live, as-ordered boards.

Usage: python3 lib/tools/compare_asordered.py [--json OUT.json] [--md OUT.md]

For each board footprint, the PROVES pads are rotated in 90-degree steps and translated onto the
board's pads (matched by pad number where both sides number them, otherwise by nearest position).
A pad whose position, size, shape or drill moved is a delta; each footprint's reason comes from REASONS.
"""

import argparse
import glob
import json
import math
import sys
from pathlib import Path

LIB_DIR = Path(__file__).resolve().parent.parent
REPO = LIB_DIR.parent
sys.path.insert(0, str(LIB_DIR))
sys.path.insert(0, str(LIB_DIR / "tools"))

from sexpr import child, children, parse, prop, value  # noqa: E402

import parts  # noqa: E402

LIVE_BOARDS = ("XY_Face_V4", "XY_Face_V4nb", "XY_Faces_V3lp", "XY_Faces_V3r", "Z_Face_V3", "2U_Varients/2U_XY_V1a")
TOL = 0.005

REASONS = {
    "C_0402_1005Metric": "Same IPC-7351B nominal equations as KiCad's stock part, fed the ordered Samsung CL05 "
    "tolerances instead of IPC-SM-782 generic ones.",
    "C_0603_1608Metric": "IPC-7351B nominal from the YAGEO and FH 0603 envelope; their wider terminal range "
    "narrows the gap.",
    "C_0805_2012Metric": "IPC-7351B nominal from the Samsung CL21 body.",
    "R_0402_1005Metric": "IPC-7351B nominal from the UNI-ROYAL 0402 body.",
    "R_0603_1608Metric": "IPC-7351B nominal from the UNI-ROYAL 0603 body.",
    "LED_0603_1608Metric": "IPC-7351B nominal from the KENTO KT-0603 body.",
    "D_SMA_DO-214AC": "Comchip CDBA240LL-HF suggested pads (2.60 x 1.70 at 4.10) replace the 2.5 x 1.7 at 4.0 "
    "house pads.",
    "Hirose_DF11-4DP-2DSA_2x02_P2.00mm_Vertical": "Hirose hole 0.8 +0.1/-0 drilled at 0.85 with a 1.45 round pad "
    "(SPEC THT rule) replaces KiCad's 1.2 x 1.65 oval.",
    "Hirose_DF11-6DP-2DSA_2x03_P2.00mm_Vertical": "As DF11-4DP.",
    "Molex_PicoLock_504050-0691_1x06_P1.50mm_Horizontal": "Molex recommended pattern: signal pads 0.6 x 1.0 "
    "(easyeda copy used 1.5 long), nails numbered MP.",
    "MountingHole_3.2mm_M3_ISO7380_Pad": "Pad is the ISO 7380-1 M3 head diameter, unchanged.",
    "MountingHole_3.2mm_M3_DIN965_Pad": "Pad is the ISO 7046-1 (DIN 965) M3 actual head diameter 5.5, not KiCad's 5.6.",
    "TI_DGS0010A_VSSOP-10_3x3mm_P0.5mm": "TI DGS land; KiCad stock already matched TI within rounding.",
    "TI_DGK0008A_VSSOP-8_3x3mm_P0.65mm": "TI DGK land (1.4 x 0.45 at 4.4 span) replaces KiCad's 1.625 x 0.5 "
    "and easyeda's 1.69 x 0.36 oval.",
    "TI_DRL0006A_SOT-563": "TI DRL land (0.67 x 0.3 at 1.48 span) replaces KiCad's 0.675 x 0.35 at 1.425.",
    "TI_DNK0008A_VSON-CLIP-8_5x6mm_P1.27mm": "The board used Infineon's TDSON-8-1 land with unnumbered paste "
    "pads; PROVES uses TI's CSD17576Q5B pattern and stencil.",
    "Vishay_VEML6031X00_2.67x2.45mm": "Vishay recommended footprint; easyeda copy rounded 1.145/1.035 to 1.15/1.04.",
    "Vishay_VEML7700-TT_TopView": "Vishay top-view pad layout.",
    "Anysolar_SM101K07TF": "The board footprint is the KXOB101K08F cell (two 13 x 3 SMD tabs, 40 mm apart). "
    "SM101K07TF, the cell the board orders, has two 3.0 mm back contacts 9 mm apart.",
    "Anysolar_SM261K10TF": "Contact positions match the ANYSOLAR drawing.",
    "Anysolar_SM531K10TF": "The board's contacts sit 48.5 x 25 mm apart; the SM531K10TF drawing puts them "
    "44.4 x 59 mm apart.",
    "TestPad_2.5x2.5mm": "House part kept as flown.",
    "BurnWire_2xTHT_P5.08mm": "House part kept as flown (was a borrowed axial-resistor footprint).",
}


def board_footprints(board):
    pcb = next(p for p in glob.glob(str(REPO / board / "*.kicad_pcb")))
    tree = parse(Path(pcb).read_text())
    for fp in children(tree, "footprint"):
        at = child(fp, "at")
        rot = float(at[3]) if len(at) > 3 else 0.0
        # KiCad stores a back-side footprint's pads already flipped about x; undo it to compare in the part's own frame.
        flip = -1.0 if value(fp, "layer") == "B.Cu" else 1.0
        pads = []
        for p in children(fp, "pad"):
            pat, size, drill = child(p, "at"), child(p, "size"), child(p, "drill")
            prot = ((float(pat[3]) if len(pat) > 3 else 0.0) - rot) % 180
            w, h = float(size[1]), float(size[2])
            if abs(prot - 90) < 1:
                w, h = h, w
            pads.append(
                dict(
                    number=p[1],
                    x=float(pat[1]),
                    y=flip * float(pat[2]),
                    w=w,
                    h=h,
                    shape=str(p[3]),
                    drill=float(drill[1]) if drill and len(drill) > 1 else None,
                )
            )
        yield fp[1], prop(fp, "Reference"), pads


def lib_pads(footprint, quarter_turns):
    out = []
    for p in footprint.pads:
        x, y, w, h = p.x, p.y, p.w, p.h
        if p.polygon:
            b = p.bbox
            x, y, w, h = (b[0] + b[2]) / 2, (b[1] + b[3]) / 2, b[2] - b[0], b[3] - b[1]
        for _ in range(quarter_turns):
            x, y, w, h = -y, x, h, w
        out.append(dict(number=p.number, x=x, y=y, w=w, h=h, shape=p.resolved_shape(), drill=p.drill))
    return out


def match(old, new, by_number):
    pairs, free = [], list(new)
    for o in old:
        numbered = [n for n in free if n["number"] == o["number"]]
        pool = (
            numbered
            if by_number and numbered
            else [n for n in free if not by_number or n["number"] not in {x["number"] for x in old}] or free
        )
        if not pool:
            pairs.append((o, None))
            continue
        ox, oy = o["x"], o["y"]
        best = min(pool, key=lambda n: (n["x"] - ox) ** 2 + (n["y"] - oy) ** 2)
        free.remove(best)
        pairs.append((o, best))
    return pairs, free


def fit(old, footprint):
    """Best 90-degree rotation and translation of the PROVES pads onto the board pads."""
    new_numbers = {p.number for p in footprint.pads}
    by_number = any(o["number"] in new_numbers for o in old)
    best = None
    for turns in range(4):
        new = lib_pads(footprint, turns)
        ocx = sum(o["x"] for o in old) / len(old)
        ocy = sum(o["y"] for o in old) / len(old)
        ncx = sum(n["x"] for n in new) / len(new)
        ncy = sum(n["y"] for n in new) / len(new)
        shifted = [dict(n, x=n["x"] + ocx - ncx, y=n["y"] + ocy - ncy) for n in new]
        pairs, extra = match(old, shifted, by_number)
        matched = [(o, n) for o, n in pairs if n]
        dx = sum(o["x"] - n["x"] for o, n in matched) / len(matched)
        dy = sum(o["y"] - n["y"] for o, n in matched) / len(matched)
        for _, n in matched:
            n["x"] += dx
            n["y"] += dy
        rms = math.sqrt(sum((o["x"] - n["x"]) ** 2 + (o["y"] - n["y"]) ** 2 for o, n in matched) / len(matched))
        if best is None or rms < best["rms"] - 1e-9:
            best = dict(turns=turns, rms=rms, pairs=pairs, extra=extra, by_number=by_number)
    return best


def pad_delta(o, n):
    if n is None:
        return dict(pad=o["number"], change="pad removed in PROVES")
    d = dict(pad=n["number"], old_pad=o["number"])
    moved = math.hypot(o["x"] - n["x"], o["y"] - n["y"])
    if moved > TOL:
        d["moved_mm"] = round(moved, 3)
    if abs(o["w"] - n["w"]) > TOL or abs(o["h"] - n["h"]) > TOL:
        d["size"] = f"{o['w']:g} x {o['h']:g} -> {n['w']:g} x {n['h']:g}"
    if o["shape"] != n["shape"]:
        d["shape"] = f"{o['shape']} -> {n['shape']}"
    if (o["drill"] or 0) != (n["drill"] or 0) and abs((o["drill"] or 0) - (n["drill"] or 0)) > TOL:
        d["drill"] = f"{o['drill']} -> {n['drill']}"
    if o["number"] != n["number"]:
        d["renumbered"] = f"{o['number'] or '(none)'} -> {n['number']}"
    return d if len(d) > 2 or "renumbered" in d else None


def compare():
    rows, seen = [], set()
    for board in LIVE_BOARDS:
        for lib_id, ref, pads in board_footprints(board):
            if lib_id in parts.NOT_PARTS or lib_id in seen:
                continue
            seen.add(lib_id)
            target = parts.REPLACES[lib_id]
            best = fit(pads, target)
            deltas = [d for d in (pad_delta(o, n) for o, n in best["pairs"]) if d]
            deltas += [dict(pad=n["number"], change="pad added in PROVES") for n in best["extra"]]
            mirrored = False
            if best["rms"] > 0.05:
                mirrored_fp = mirror(target)
                if fit(pads, mirrored_fp)["rms"] < best["rms"] / 10:
                    mirrored = True
            rows.append(
                dict(
                    board=board,
                    ref=ref,
                    old=lib_id,
                    new=f"{parts.LIB}:{target.name}",
                    rotation_deg=best["turns"] * 90,
                    rms_mm=round(best["rms"], 3),
                    matched_by="number" if best["by_number"] else "position",
                    board_is_mirror_image=mirrored,
                    pads_changed=len(deltas),
                    deltas=deltas,
                    reason=REASONS[target.name],
                )
            )
    return rows


def mirror(footprint):
    from dataclasses import replace

    return replace(footprint, pads=tuple(replace(p, x=-p.x) for p in footprint.pads))


def markdown(rows):
    out = [
        "# PROVES library vs as-ordered boards",
        "",
        "Generated by `lib/tools/compare_asordered.py`. One row per board footprint, first board that places it.",
        "",
        "| Board footprint | PROVES footprint | Pads changed | Largest move (mm) | Mirror | Reason |",
        "|---|---|---|---|---|---|",
    ]
    for r in rows:
        largest = max([d.get("moved_mm", 0) for d in r["deltas"]] or [0])
        out.append(
            f"| `{r['old']}` ({r['board']} {r['ref']}) | `{r['new']}` | {r['pads_changed']} | {largest:g} | "
            f"{'yes' if r['board_is_mirror_image'] else ''} | {r['reason']} |"
        )
    out += ["", "## Pad detail", ""]
    for r in rows:
        if not r["deltas"]:
            continue
        out.append(f"### `{r['old']}` -> `{r['new']}`")
        out.append("")
        out.append(f"Fit: rotate PROVES {r['rotation_deg']} deg, matched by {r['matched_by']}, rms {r['rms_mm']} mm.")
        out.append("")
        for d in r["deltas"]:
            out.append("- " + ", ".join(f"{k} {v}" for k, v in d.items()))
        out.append("")
    return "\n".join(out)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", type=Path)
    ap.add_argument("--md", type=Path)
    args = ap.parse_args()
    rows = compare()
    if args.json:
        args.json.write_text(json.dumps(rows, indent=1) + "\n")
    if args.md:
        args.md.write_text(markdown(rows) + "\n")
    for r in rows:
        largest = max([d.get("moved_mm", 0) for d in r["deltas"]] or [0])
        flag = " MIRROR" if r["board_is_mirror_image"] else ""
        print(f"{r['pads_changed']:3d} pads changed, max move {largest:6.3f}  {r['old']} -> {r['new']}{flag}")
