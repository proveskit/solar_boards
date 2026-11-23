"""Write library parts as KiCad 10 footprint and symbol files with stable UUIDs."""

from __future__ import annotations

import math
import uuid

from model import (
    CRTYD_WIDTH,
    FAB_WIDTH,
    FONT,
    PIN_LENGTH,
    SILK_WIDTH,
    SYMBOL_GRID,
    Footprint,
    Pin,
    Symbol,
    pin1_chamfer,
    pin1_marker,
    silk_outline,
    snap,
)

FP_VERSION = "20260206"
SYM_VERSION = "20251024"
GENERATOR = "proves-lib"
NAMESPACE = uuid.UUID("5f1c3c2e-7c1a-4a8e-9b1e-0b5e2a9d6f10")


def num(v):
    v = round(float(v), 6)
    if v == 0:
        return "0"
    s = f"{v:.6f}".rstrip("0").rstrip(".")
    return s


def q(s):
    return '"' + str(s).replace("\\", "\\\\").replace('"', '\\"') + '"'


class _Uuids:
    def __init__(self, scope):
        self.scope, self.n = scope, 0

    def __call__(self):
        self.n += 1
        return str(uuid.uuid5(NAMESPACE, f"{self.scope}/{self.n}"))


def _font(size, thickness=None, justify=None, hide=False):
    lines = ["\t\t(effects", "\t\t\t(font", f"\t\t\t\t(size {num(size)} {num(size)})"]
    if thickness is not None:
        lines.append(f"\t\t\t\t(thickness {num(thickness)})")
    lines.append("\t\t\t)")
    if justify:
        lines.append(f"\t\t\t(justify {justify})")
    lines.append("\t\t)")
    return lines


def _fp_property(uid, name, value, at, layer, size, hide=False, thickness=None):
    out = [f"\t(property {q(name)} {q(value)}", f"\t\t(at {num(at[0])} {num(at[1])} 0)"]
    if name in ("Reference", "Value"):
        out.append("\t\t(unlocked yes)")
    out.append(f"\t\t(layer {q(layer)})")
    if hide:
        out.append("\t\t(hide yes)")
    out.append(f"\t\t(uuid {q(uid())})")
    out.extend(_font(size, thickness))
    out.append("\t)")
    return out


def _stroke(width):
    return ["\t\t(stroke", f"\t\t\t(width {num(width)})", "\t\t\t(type solid)", "\t\t)"]


def _line(uid, a, b, layer, width):
    return (
        ["\t(fp_line", f"\t\t(start {num(a[0])} {num(a[1])})", f"\t\t(end {num(b[0])} {num(b[1])})"]
        + _stroke(width)
        + [f"\t\t(layer {q(layer)})", f"\t\t(uuid {q(uid())})", "\t)"]
    )


def _rect(uid, x0, y0, x1, y1, layer, width):
    return (
        ["\t(fp_rect", f"\t\t(start {num(x0)} {num(y0)})", f"\t\t(end {num(x1)} {num(y1)})"]
        + _stroke(width)
        + ["\t\t(fill no)", f"\t\t(layer {q(layer)})", f"\t\t(uuid {q(uid())})", "\t)"]
    )


def _poly(uid, pts, layer, width, fill=False):
    out = ["\t(fp_poly", "\t\t(pts"]
    out += [f"\t\t\t(xy {num(x)} {num(y)})" for x, y in pts]
    out += (
        ["\t\t)"]
        + _stroke(width)
        + [f"\t\t(fill {'yes' if fill else 'no'})", f"\t\t(layer {q(layer)})", f"\t\t(uuid {q(uid())})", "\t)"]
    )
    return out


def _circle(uid, x, y, r, layer, width, fill):
    return (
        ["\t(fp_circle", f"\t\t(center {num(x)} {num(y)})", f"\t\t(end {num(x + r)} {num(y)})"]
        + _stroke(width)
        + [f"\t\t(fill {'yes' if fill else 'no'})", f"\t\t(layer {q(layer)})", f"\t\t(uuid {q(uid())})", "\t)"]
    )


def _pad(uid, p):
    shape = p.resolved_shape()
    kind = {"smd": "smd", "thru": "thru_hole", "npth": "np_thru_hole"}[p.kind]
    out = [f"\t(pad {q(p.number)} {kind} {shape}", f"\t\t(at {num(p.x)} {num(p.y)})"]
    if shape == "custom":
        out.append(f"\t\t(size {num(p.w)} {num(p.h)})")
    else:
        out.append(f"\t\t(size {num(p.w)} {num(p.h)})")
    if p.drill is not None:
        out.append(f"\t\t(drill {num(p.drill)})")
    if p.kind == "smd":
        layers = '"F.Cu" "F.Mask" "F.Paste"' if p.paste else '"F.Cu" "F.Mask"'
    elif p.kind == "thru":
        layers = '"*.Cu" "*.Mask"'
    else:
        layers = '"*.Cu" "*.Mask"'
    out.append(f"\t\t(layers {layers})")
    if shape == "roundrect":
        out.append(f"\t\t(roundrect_rratio {num(p.rratio())})")
    if shape == "custom":
        out += [
            "\t\t(options",
            "\t\t\t(clearance outline)",
            "\t\t\t(anchor rect)",
            "\t\t)",
            "\t\t(primitives",
            "\t\t\t(gr_poly",
            "\t\t\t\t(pts",
        ]
        out += [f"\t\t\t\t\t(xy {num(x)} {num(y)})" for x, y in p.polygon]
        out += ["\t\t\t\t)", "\t\t\t\t(width 0)", "\t\t\t\t(fill yes)", "\t\t\t)", "\t\t)"]
    out += [f"\t\t(uuid {q(uid())})", "\t)"]
    return out


def footprint_text(fp: Footprint) -> str:
    uid = _Uuids("fp/" + fp.name)
    descr = f"{fp.description}. Source: {fp.source.cite()}"
    if fp.notes:
        descr += ". " + ". ".join(fp.notes)
    cy0, cy1 = fp.courtyard()[1], fp.courtyard()[3]
    out = [
        f"(footprint {q(fp.name)}",
        f"\t(version {FP_VERSION})",
        f"\t(generator {q(GENERATOR)})",
        '\t(generator_version "10.0")',
        '\t(layer "F.Cu")',
        f"\t(descr {q(descr)})",
        f"\t(tags {q(fp.tags)})",
    ]
    out += _fp_property(uid, "Reference", "REF**", (0, snap(cy0 - 0.8)), "F.SilkS", 1, hide=True, thickness=0.15)
    out += _fp_property(uid, "Value", fp.name, (0, snap(cy1 + 0.8)), "F.Fab", 1, thickness=0.15)
    out += _fp_property(uid, "Datasheet", fp.source.url, (0, 0), "F.Fab", 1.27, hide=True)
    out += _fp_property(uid, "Description", fp.description, (0, 0), "F.Fab", 1.27, hide=True)
    attr = "through_hole" if fp.tht else "smd"
    out += [f"\t(attr {attr})", "\t(duplicate_pad_numbers_are_jumpers no)"]

    if fp.round_body:
        out += _circle(
            uid,
            (fp.body[0] + fp.body[2]) / 2,
            (fp.body[1] + fp.body[3]) / 2,
            (fp.body[2] - fp.body[0]) / 2,
            "F.Fab",
            FAB_WIDTH,
            False,
        )
        keep = []
    else:
        out += _poly(uid, pin1_chamfer(fp), "F.Fab", FAB_WIDTH)
        segs, keep = silk_outline(fp)
        for a, b in segs:
            out += _line(uid, a, b, "F.SilkS", SILK_WIDTH)
    if fp.polarized:
        x, y, r = pin1_marker(fp, keep)
        out += _circle(uid, x, y, r / 2, "F.SilkS", r, True)
    x0, y0, x1, y1 = fp.courtyard()
    out += _rect(uid, x0, y0, x1, y1, "F.CrtYd", CRTYD_WIDTH)
    for a in fp.paste_apertures:
        out += _poly(
            uid,
            [
                (a.x - a.w / 2, a.y - a.h / 2),
                (a.x + a.w / 2, a.y - a.h / 2),
                (a.x + a.w / 2, a.y + a.h / 2),
                (a.x - a.w / 2, a.y + a.h / 2),
            ],
            "F.Paste",
            0,
            True,
        )

    bw, bh = fp.body[2] - fp.body[0], fp.body[3] - fp.body[1]
    size = snap(max(0.25, min(1.0, 0.3 * min(bw, bh))), 0.01)
    out += [
        '\t(fp_text user "${REFERENCE}"',
        f"\t\t(at {num((fp.body[0] + fp.body[2]) / 2)} {num((fp.body[1] + fp.body[3]) / 2)} 0)",
        "\t\t(unlocked yes)",
        '\t\t(layer "F.Fab")',
        f"\t\t(uuid {q(uid())})",
    ]
    out += _font(size, snap(size * 0.15, 0.001))
    out.append("\t)")
    for p in fp.pads:
        out += _pad(uid, p)
    out += ["\t(embedded_fonts no)", ")", ""]
    return "\n".join(out)


# ---------------------------------------------------------------- symbols


def _sym_font(hide=False, justify=None):
    out = ["\t\t\t(effects", "\t\t\t\t(font", f"\t\t\t\t\t(size {num(FONT)} {num(FONT)})", "\t\t\t\t)"]
    if justify:
        out.append(f"\t\t\t\t(justify {justify})")
    if hide:
        out.append("\t\t\t\t(hide yes)")
    out.append("\t\t\t)")
    return out


def _sym_property(name, value, at, hide=False, justify=None, angle=0):
    out = [
        f"\t\t(property {q(name)} {q(value)}",
        f"\t\t\t(at {num(at[0])} {num(at[1])} {angle})",
        "\t\t\t(show_name no)",
        "\t\t\t(do_not_autoplace no)",
    ]
    if hide:
        out.append("\t\t\t(hide yes)")
    out += _sym_font(justify=justify)
    out.append("\t\t)")
    return out


def _sym_stroke(width=0.254):
    return ["\t\t\t\t(stroke", f"\t\t\t\t\t(width {num(width)})", "\t\t\t\t\t(type default)", "\t\t\t\t)"]


def _sym_rect(x0, y0, x1, y1):
    return (
        ["\t\t\t(rectangle", f"\t\t\t\t(start {num(x0)} {num(y0)})", f"\t\t\t\t(end {num(x1)} {num(y1)})"]
        + _sym_stroke()
        + ["\t\t\t\t(fill", "\t\t\t\t\t(type background)", "\t\t\t\t)", "\t\t\t)"]
    )


def _sym_poly(pts, fill="none", width=0.254):
    out = ["\t\t\t(polyline", "\t\t\t\t(pts"]
    out += [f"\t\t\t\t\t(xy {num(x)} {num(y)})" for x, y in pts]
    out += ["\t\t\t\t)"] + _sym_stroke(width) + ["\t\t\t\t(fill", f"\t\t\t\t\t(type {fill})", "\t\t\t\t)", "\t\t\t)"]
    return out


def _sym_circle(x, y, r, fill="none", width=0.254):
    return (
        ["\t\t\t(circle", f"\t\t\t\t(center {num(x)} {num(y)})", f"\t\t\t\t(radius {num(r)})"]
        + _sym_stroke(width)
        + ["\t\t\t\t(fill", f"\t\t\t\t\t(type {fill})", "\t\t\t\t)", "\t\t\t)"]
    )


def _sym_pin(pin: Pin, x, y, angle, length=PIN_LENGTH):
    out = [f"\t\t\t(pin {pin.etype} line", f"\t\t\t\t(at {num(x)} {num(y)} {angle})", f"\t\t\t\t(length {num(length)})"]
    if pin.hidden:
        out.append("\t\t\t\t(hide yes)")
    out += [f"\t\t\t\t(name {q(pin.name)}"] + ["\t" + s for s in _sym_font()] + ["\t\t\t\t)"]
    out += [f"\t\t\t\t(number {q(pin.number)}"] + ["\t" + s for s in _sym_font()] + ["\t\t\t\t)", "\t\t\t)"]
    return out


def _ceil_grid(v, g):
    return math.ceil(v / g - 1e-9) * g


def box_layout(s: Symbol):
    """Body half-sizes and pin anchor points for a functional box symbol (lib/SPEC.md, symbols)."""
    g = SYMBOL_GRID
    char = 1.0
    rows = max(len(s.left), len(s.right), 1)
    cols = max(len(s.top), len(s.bottom), 1)
    name_l = max([len(p.name) for p in s.left] or [0])
    name_r = max([len(p.name) for p in s.right] or [0])
    name_t = max([len(p.name) for p in s.top] or [0])
    name_b = max([len(p.name) for p in s.bottom] or [0])
    side = max(name_l, name_r) * char + 0.762
    centre = cols * g / 2 if (s.top or s.bottom) else 0
    half_w = _ceil_grid(max(side + centre + g / 2, (cols + 1) * g / 2), g)
    half_h = _ceil_grid(max((rows + 1) * g / 2, ((name_t + name_b) * char + 2 * 0.762 + g) / 2), g)
    pins = []
    for i, p in enumerate(s.left):
        pins.append((p, -half_w - PIN_LENGTH, half_h - g * (i + 1), 0))
    for i, p in enumerate(s.right):
        pins.append((p, half_w + PIN_LENGTH, half_h - g * (i + 1), 180))
    start = -((len(s.top) - 1) // 2) * g
    for i, p in enumerate(s.top):
        pins.append((p, start + i * g, half_h + PIN_LENGTH, 270))
    start = -((len(s.bottom) - 1) // 2) * g
    for i, p in enumerate(s.bottom):
        pins.append((p, start + i * g, -half_h - PIN_LENGTH, 90))
    return half_w, half_h, pins


def _graphic(s: Symbol):
    """Return (graphics lines, pin placements, ref anchor, value anchor) for the symbol's drawing style."""
    pins = s.pins()
    if s.graphic == "box":
        hw, hh, placed = box_layout(s)
        top_extra = PIN_LENGTH if s.top else 0
        bot_extra = PIN_LENGTH if s.bottom else 0
        return (
            _sym_rect(-hw, hh, hw, -hh),
            placed,
            (-hw, hh + top_extra + 1.27, "left"),
            (-hw, -hh - bot_extra - 1.27, "left"),
        )
    if s.graphic == "resistor":
        zig = [(0, 2.286)]
        for i in range(6):
            zig.append((1.016 if i % 2 == 0 else -1.016, 2.286 - 0.762 * (i + 0.5)))
        zig.append((0, -2.286))
        art = _sym_poly([(0, 2.54), (0, 2.286)]) + _sym_poly(zig) + _sym_poly([(0, -2.286), (0, -2.54)])
        return art, [(pins[0], 0, 3.81, 270), (pins[1], 0, -3.81, 90)], (2.54, 1.27, "left"), (2.54, -1.27, "left")
    if s.graphic == "capacitor":
        art = _sym_poly([(-2.032, 0.762), (2.032, 0.762)], width=0.508) + _sym_poly(
            [(-2.032, -0.762), (2.032, -0.762)], width=0.508
        )
        return (art, [(pins[0], 0, 3.81, 270), (pins[1], 0, -3.81, 90)], (2.54, 1.27, "left"), (2.54, -1.27, "left"))
    if s.graphic in ("led", "schottky"):
        art = _sym_poly([(1.27, 1.27), (1.27, -1.27), (-1.27, 0), (1.27, 1.27)])
        if s.graphic == "led":
            art += _sym_poly([(-1.27, 1.27), (-1.27, -1.27)])
            art += _sym_poly([(-0.508, 1.524), (0.762, 2.794), (0.254, 2.794), (0.762, 2.794), (0.762, 2.286)])
            art += _sym_poly([(0.508, 1.524), (1.778, 2.794), (1.27, 2.794), (1.778, 2.794), (1.778, 2.286)])
        else:
            art += _sym_poly(
                [(-0.762, 0.762), (-0.762, 1.27), (-1.27, 1.27), (-1.27, -1.27), (-1.778, -1.27), (-1.778, -0.762)]
            )
        art += _sym_poly([(-2.54, 0), (2.54, 0)], width=0)
        return (art, [(pins[0], -3.81, 0, 0), (pins[1], 3.81, 0, 180)], (0, 4.064, None), (0, -2.54, None))
    if s.graphic == "solar":
        art = _sym_poly([(-2.032, 1.016), (2.032, 1.016)], width=0.254)
        art += _sym_poly([(-1.016, 0.254), (1.016, 0.254)], width=0.508)
        art += _sym_poly([(-2.032, -0.508), (2.032, -0.508)], width=0.254)
        art += _sym_poly([(-1.016, -1.27), (1.016, -1.27)], width=0.508)
        art += _sym_poly([(0, 2.54), (0, 1.016)], width=0) + _sym_poly([(0, -1.27), (0, -2.54)], width=0)
        art += _sym_poly([(-4.064, 3.302), (-2.794, 2.032), (-3.302, 2.032), (-2.794, 2.032), (-2.794, 2.54)])
        art += _sym_poly([(-3.048, 4.318), (-1.778, 3.048), (-2.286, 3.048), (-1.778, 3.048), (-1.778, 3.556)])
        art += _sym_poly([(1.524, 2.032), (1.524, 1.524)], width=0.1524) + _sym_poly(
            [(1.27, 1.778), (1.778, 1.778)], width=0.1524
        )
        return (art, [(pins[0], 0, 5.08, 270), (pins[1], 0, -5.08, 90)], (2.54, 1.27, "left"), (2.54, -1.27, "left"))
    if s.graphic == "nmos":
        art = _sym_poly([(-2.54, 0), (-0.762, 0), (-0.762, 1.905), (-0.762, -1.905)])
        for y in (1.27, 0, -1.27):
            art += _sym_poly([(0, y + 0.508), (0, y - 0.508)], width=0.254)
        art += _sym_poly([(0, 1.27), (2.54, 1.27), (2.54, 2.54)])
        art += _sym_poly([(0, -1.27), (2.54, -1.27), (2.54, -2.54)])
        art += _sym_poly([(0, 0), (2.54, 0), (2.54, -1.27)])
        art += _sym_poly([(0.254, 0), (1.016, 0.381), (1.016, -0.381), (0.254, 0)], fill="outline")
        art += _sym_circle(1.27, 0, 2.794)
        d = [p for p in pins if p.name == "D"]
        src = [p for p in pins if p.name == "S"]
        gate = [p for p in pins if p.name == "G"]
        placed = [(gate[0], -5.08, 0, 0)]
        placed += [(p, 2.54, 5.08, 270) for p in d]
        placed += [(p, 2.54, -5.08, 90) for p in src]
        return art, placed, (5.08, 1.27, "left"), (5.08, -1.27, "left")
    if s.graphic == "testpoint":
        art = _sym_circle(0, 3.302, 0.762)
        return art, [(pins[0], 0, 0, 90)], (0, 5.588, None), (0, -1.27, None)
    if s.graphic == "mountinghole":
        art = _sym_circle(0, 1.27, 1.27, width=0.508)
        return art, [(pins[0], 0, -2.54, 90)], (0, 3.81, None), (0, -3.81, None)
    if s.graphic == "burnwire":
        loop = [(-2.54, 0)]
        for i in range(8):
            loop.append((-2.54 + 0.635 * (i + 0.5), 1.016 if i % 2 == 0 else -1.016))
        loop.append((2.54, 0))
        art = _sym_poly(loop)
        return art, [(pins[0], -5.08, 0, 0), (pins[1], 5.08, 0, 180)], (0, 2.794, None), (0, -2.794, None)
    raise ValueError(s.graphic)


def symbol_text(s: Symbol) -> str:
    art, placed, ref_at, val_at = _graphic(s)
    out = [f"\t(symbol {q(s.name)}"]
    if not s.show_pin_numbers:
        out += ["\t\t(pin_numbers", "\t\t\t(hide yes)", "\t\t)"]
    if s.graphic == "box":
        out += ["\t\t(pin_names", "\t\t\t(offset 0.762)", "\t\t)"]
    elif not s.show_pin_names:
        out += ["\t\t(pin_names", "\t\t\t(offset 0)", "\t\t\t(hide yes)", "\t\t)"]
    out += [
        "\t\t(exclude_from_sim no)",
        "\t\t(in_bom yes)",
        "\t\t(on_board yes)",
        "\t\t(in_pos_files yes)",
        "\t\t(duplicate_pin_numbers_are_jumpers no)",
    ]
    out += _sym_property("Reference", s.reference, ref_at[:2], justify=ref_at[2])
    out += _sym_property("Value", s.value, val_at[:2], justify=val_at[2])
    out += _sym_property("Footprint", s.footprint, (0, 0), hide=True)
    out += _sym_property("Datasheet", s.datasheet, (0, 0), hide=True)
    out += _sym_property("Description", s.description, (0, 0), hide=True)
    for k, v in s.fields:
        out += _sym_property(k, v, (0, 0), hide=True)
    out += _sym_property("ki_keywords", s.keywords, (0, 0), hide=True)
    if s.footprint_filters:
        out += _sym_property("ki_fp_filters", " ".join(s.footprint_filters), (0, 0), hide=True)
    out += [f"\t\t(symbol {q(s.name + '_0_1')}"] + art + ["\t\t)"]
    out += [f"\t\t(symbol {q(s.name + '_1_1')}"]
    for pin, x, y, angle in placed:
        length = PIN_LENGTH
        if s.graphic == "capacitor":
            length = 3.048
        elif s.graphic == "resistor":
            length = 1.27
        elif s.graphic == "testpoint":
            length = 2.54
        elif s.graphic == "solar":
            length = 2.54
        elif s.graphic == "mountinghole":
            length = 0

        out += _sym_pin(pin, x, y, angle, length)
    out += ["\t\t)", "\t\t(embedded_fonts no)", "\t)"]
    return "\n".join(out)


def symbol_lib_text(symbols) -> str:
    out = [
        "(kicad_symbol_lib",
        f"\t(version {SYM_VERSION})",
        f"\t(generator {q(GENERATOR)})",
        '\t(generator_version "10.0")',
    ]
    for s in symbols:
        out.append(symbol_text(s))
    out += [")", ""]
    return "\n".join(out)
