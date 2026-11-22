"""Enforce lib/SPEC.md on the committed library files, then prove they match a fresh regeneration.

Usage: python3 lib/tools/check.py
Exit status 1 lists every violation as `<file>: <rule>: <detail>`.
"""

import filecmp
import math
import re
import sys
import tempfile
from pathlib import Path

LIB_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(LIB_DIR / "tools"))

from sexpr import child, children, parse, prop, value  # noqa: E402

LIB = "PROVES"
PRETTY = LIB_DIR / f"{LIB}.pretty"
SYMLIB = LIB_DIR / f"{LIB}.kicad_sym"
MECHANICAL_PAD = "MP"
COURTYARD_MARGIN = 0.25
SILK_CLEARANCE = 0.2
EPS = 0.006


def f(v):
    return float(v)


def pad_box(pad):
    at, size = child(pad, "at"), child(pad, "size")
    x, y, w, h = f(at[1]), f(at[2]), f(size[1]), f(size[2])
    prims = child(pad, "primitives")
    if prims:
        pts = [
            (x + f(p[1]), y + f(p[2]))
            for poly in children(prims, "gr_poly")
            for p in children(child(poly, "pts"), "xy")
        ]
        xs, ys = [p[0] for p in pts] + [x - w / 2, x + w / 2], [p[1] for p in pts] + [y - h / 2, y + h / 2]
        return min(xs), min(ys), max(xs), max(ys)
    return x - w / 2, y - h / 2, x + w / 2, y + h / 2


def graphic_points(node):
    for tag in ("start", "end", "center"):
        c = child(node, tag)
        if c:
            yield f(c[1]), f(c[2])
    pts = child(node, "pts")
    if pts:
        for p in children(pts, "xy"):
            yield f(p[1]), f(p[2])


def seg_box_distance(a, b, box):
    """Shortest distance between segment a-b and an axis-aligned box (0 when they touch)."""
    x0, y0, x1, y1 = box

    def point_box(px, py):
        dx = max(x0 - px, 0, px - x1)
        dy = max(y0 - py, 0, py - y1)
        return math.hypot(dx, dy)

    steps = max(2, int(math.hypot(b[0] - a[0], b[1] - a[1]) / 0.02))
    return min(point_box(a[0] + (b[0] - a[0]) * t / steps, a[1] + (b[1] - a[1]) * t / steps) for t in range(steps + 1))


def check_footprint(path, errors):
    fp = parse(path.read_text())
    name = fp[1]
    err = lambda rule, detail: errors.append(f"{path.name}: {rule}: {detail}")  # noqa: E731
    if name != path.stem:
        err("F1 name", f"footprint {name!r} in file {path.name}")
    if value(fp, "version") != "20260206":
        err("F2 format", f"version {value(fp, 'version')}, expected KiCad 10 (20260206)")
    descr = value(fp, "descr", "")
    if "Source: " not in descr:
        err("F3 source", "descr has no 'Source: <document>, p.<page>, <figure>' citation")
    if not (prop(fp, "Datasheet") or "").startswith("http"):
        err("F3 source", "Datasheet property is not a URL")
    if children(fp, "model"):
        err("F4 no borrowed models", "3D model reference present")
    ref = next(p for p in children(fp, "property") if p[1] == "Reference")
    val = next(p for p in children(fp, "property") if p[1] == "Value")
    if value(ref, "layer") != "F.SilkS" or value(val, "layer") != "F.Fab":
        err("F5 text", "Reference must be on F.SilkS and Value on F.Fab")
    if not any(
        t[1] == "user" and t[2] == "${REFERENCE}" and value(t, "layer") == "F.Fab" for t in children(fp, "fp_text")
    ):
        err("F5 text", "no ${REFERENCE} on F.Fab")

    pads = children(fp, "pad")
    numbers = [p[1] for p in pads]
    if not pads:
        err("F6 pads", "no pads")
        return
    if any(n == "" for n in numbers):
        err("F6 pads", "unnumbered pad")
    if "1" not in numbers:
        err("F6 pads", "no pad 1")
    boxes = [pad_box(p) for p in pads]
    copper = (min(b[0] for b in boxes), min(b[1] for b in boxes), max(b[2] for b in boxes), max(b[3] for b in boxes))
    smd = all(p[2] == "smd" for p in pads)
    if smd:
        cx, cy = (copper[0] + copper[2]) / 2, (copper[1] + copper[3]) / 2
        if abs(cx) > EPS or abs(cy) > EPS:
            err("F7 origin", f"SMD origin must be the pad-extent centre, off by ({cx:.3f}, {cy:.3f})")
    else:
        at = child(next(p for p in pads if p[1] == "1"), "at")
        fab_pts = [
            pt
            for g in children(fp, "fp_poly") + children(fp, "fp_circle")
            if value(g, "layer") == "F.Fab"
            for pt in graphic_points(g)
        ]
        centres = [(f(at[1]), f(at[2])), ((copper[0] + copper[2]) / 2, (copper[1] + copper[3]) / 2)]
        if fab_pts:
            xs, ys = [p[0] for p in fab_pts], [p[1] for p in fab_pts]
            centres.append(((min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2))
        if not any(abs(x) < EPS and abs(y) < EPS for x, y in centres):
            err("F7 origin", "THT origin must be pad 1, the pad-extent centre or the body centre")
    for p in pads:
        layers = child(p, "layers")[1:]
        if p[2] == "smd" and not {"F.Cu", "F.Mask"} <= set(layers):
            err("F8 layers", f"pad {p[1]} SMD pad without F.Cu and F.Mask")
        if p[2] == "thru_hole" and not {"*.Cu", "*.Mask"} <= set(layers):
            err("F8 layers", f"pad {p[1]} THT pad without *.Cu and *.Mask")
        if p[2] == "thru_hole":
            drill, size = f(child(p, "drill")[1]), min(f(child(p, "size")[1]), f(child(p, "size")[2]))
            if (size - drill) / 2 < 0.15 - EPS:
                err("F9 annular", f"pad {p[1]} annular ring {(size - drill) / 2:.3f} < 0.15")

    graphics = [g for tag in ("fp_line", "fp_rect", "fp_poly", "fp_circle") for g in children(fp, tag)]
    crt = [g for g in graphics if value(g, "layer") == "F.CrtYd"]
    fab = [g for g in graphics if value(g, "layer") == "F.Fab"]
    silk = [g for g in graphics if value(g, "layer") == "F.SilkS"]
    if len(crt) != 1 or crt[0][0] != "fp_rect":
        err("F10 courtyard", "exactly one F.CrtYd rectangle required")
    else:
        width = f(value(child(crt[0], "stroke"), "width"))
        if abs(width - 0.05) > 1e-6:
            err("F10 courtyard", f"line width {width}, expected 0.05")
        (x0, y0), (x1, y1) = list(graphic_points(crt[0]))
        body = [pt for g in fab for pt in graphic_points(g)]
        if body and fab[0][0] == "fp_circle":
            ccx, ccy = f(child(fab[0], "center")[1]), f(child(fab[0], "center")[2])
            ex, ey = f(child(fab[0], "end")[1]), f(child(fab[0], "end")[2])
            r = math.hypot(ex - ccx, ey - ccy)
            body = [(ccx - r, ccy - r), (ccx + r, ccy + r)]
        need = (
            min([copper[0]] + [p[0] for p in body]) - COURTYARD_MARGIN,
            min([copper[1]] + [p[1] for p in body]) - COURTYARD_MARGIN,
            max([copper[2]] + [p[0] for p in body]) + COURTYARD_MARGIN,
            max([copper[3]] + [p[1] for p in body]) + COURTYARD_MARGIN,
        )
        if x0 > need[0] + EPS or y0 > need[1] + EPS or x1 < need[2] - EPS or y1 < need[3] - EPS:
            err("F10 courtyard", f"courtyard {x0, y0, x1, y1} does not clear pads and body by 0.25")
    if not fab:
        err("F11 fab", "no F.Fab body outline")
    for g in silk:
        if g[0] != "fp_line":
            continue
        a, b = list(graphic_points(g))
        half = f(value(child(g, "stroke"), "width")) / 2
        for p, box in zip(pads, boxes, strict=True):
            d = seg_box_distance(a, b, box) - half
            if d < SILK_CLEARANCE - EPS:
                err("F12 silk", f"silk line {a}-{b} is {d:.3f} from pad {p[1]} (< {SILK_CLEARANCE})")
    return name, set(numbers) - {MECHANICAL_PAD}


def check_symbols(footprints, errors):
    lib = parse(SYMLIB.read_text())
    if value(lib, "version") != "20251024":
        errors.append(f"{SYMLIB.name}: S1 format: version {value(lib, 'version')}, expected KiCad 10 (20251024)")
    names = set()
    for s in children(lib, "symbol"):
        name = s[1]
        names.add(name)
        err = lambda rule, detail, name=name: errors.append(f"{SYMLIB.name}:{name}: {rule}: {detail}")  # noqa: E731
        for field in ("Reference", "Value", "Footprint", "Datasheet", "Description", "ki_keywords"):
            if prop(s, field) is None:
                err("S2 fields", f"missing {field}")
        if not prop(s, "Description"):
            err("S2 fields", "empty Description")
        pins = [p for unit in children(s, "symbol") for p in children(unit, "pin")]
        numbers = [value(p, "number") for p in pins]
        if len(numbers) != len(set(numbers)):
            err("S3 pins", "duplicate pin number")
        for p in pins:
            at = child(p, "at")
            for v in (f(at[1]), f(at[2])):
                if abs(v / 1.27 - round(v / 1.27)) > 1e-6:
                    err("S3 pins", f"pin {value(p, 'number')} off the 1.27 mm grid at {at[1]}, {at[2]}")
        fpref = prop(s, "Footprint")
        if fpref:
            for field in ("MPN", "Manufacturer"):
                if not prop(s, field):
                    err("S4 atomic", f"atomic part without {field}")
            if not prop(
                s,
                "Datasheet",
            ).startswith("http"):
                err("S4 atomic", "atomic part Datasheet is not a URL")
            libname, _, fpname = fpref.partition(":")
            if libname != LIB or fpname not in footprints:
                err("S5 footprint", f"{fpref} is not in {LIB}.pretty")
            elif set(numbers) != footprints[fpname]:
                err("S5 footprint", f"pins {sorted(set(numbers))} != pads {sorted(footprints[fpname])} of {fpname}")
        else:
            filters = (prop(s, "ki_fp_filters") or "").split()
            if not filters:
                err("S6 generic", "generic part without ki_fp_filters")
            matched = [n for n in footprints for pat in filters if re.fullmatch(pat.replace("*", ".*"), n)]
            if not matched:
                err("S6 generic", f"filters {filters} match no {LIB} footprint")
            for n in matched:
                if set(numbers) != footprints[n]:
                    err("S6 generic", f"pins {sorted(set(numbers))} != pads of {n}")
    return names


def check_regenerates(errors):
    import generate

    with tempfile.TemporaryDirectory() as tmp:
        generate.write(Path(tmp))
        fresh = Path(tmp)
        committed = {p.name for p in PRETTY.glob("*.kicad_mod")}
        regenerated = {p.name for p in (fresh / f"{LIB}.pretty").glob("*.kicad_mod")}
        for extra in sorted(committed - regenerated):
            errors.append(f"{extra}: L1 regenerate: committed but not produced by parts.py")
        for missing in sorted(regenerated - committed):
            errors.append(f"{missing}: L1 regenerate: produced by parts.py but not committed")
        for name in sorted(committed & regenerated):
            if not filecmp.cmp(PRETTY / name, fresh / f"{LIB}.pretty" / name, shallow=False):
                errors.append(f"{name}: L1 regenerate: differs from parts.py output (hand edit?)")
        if not filecmp.cmp(SYMLIB, fresh / SYMLIB.name, shallow=False):
            errors.append(f"{SYMLIB.name}: L1 regenerate: differs from parts.py output (hand edit?)")


def check_ipc_equations(errors):
    """The IPC chip calculator must reproduce KiCad's stock C_0402 and C_0603 pads from the same IPC-SM-782 bodies."""
    from patterns import ipc_chip

    for args, want in (
        (((0.9, 1.1), (0.4, 0.6), (0.1, 0.3), True), (0.56, 0.62, 0.48)),
        (((1.45, 1.75), (0.65, 0.95), (0.2, 0.5), False), (0.9, 0.95, 0.775)),
    ):
        pad = ipc_chip(*args)[0][1]
        got = (round(pad.w, 4), round(pad.h, 4), round(pad.x, 4))
        if got != want:
            errors.append(f"tools/patterns.py: L2 IPC equations: {args} gave {got}, expected {want}")


def main():
    errors = []
    footprints = {}
    for path in sorted(PRETTY.glob("*.kicad_mod")):
        result = check_footprint(path, errors)
        if result:
            footprints[result[0]] = result[1]
    symbols = check_symbols(footprints, errors)
    check_regenerates(errors)
    check_ipc_equations(errors)
    for e in errors:
        print(e)
    print(f"{len(footprints)} footprints, {len(symbols)} symbols, {len(errors)} violations")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
