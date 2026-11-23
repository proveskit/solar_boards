"""Part model for the PROVES library and the rules in lib/SPEC.md that derive geometry from it.

A part entry states only datasheet facts: pad copper, body size, pin functions and the
source they came from. Everything else (fab, silk, courtyard, pin-1 marks, symbol box)
is derived here, so every part follows the spec by construction.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

GRID = 0.01
COURTYARD_MARGIN = 0.25
SILK_WIDTH = 0.12
SILK_PAD_CLEARANCE = 0.2
FAB_WIDTH = 0.1
CRTYD_WIDTH = 0.05
MAX_CORNER_RADIUS = 0.25
CORNER_FRACTION = 0.25
SYMBOL_GRID = 2.54
PIN_LENGTH = 2.54
FONT = 1.27


def snap(v, grid=GRID):
    return round(round(v / grid) * grid, 6)


@dataclass(frozen=True)
class Source:
    """Where a dimension came from: document, revision, page and figure."""

    document: str
    url: str
    page: str
    figure: str

    def cite(self):
        return f"{self.document}, p.{self.page}, {self.figure}"


@dataclass(frozen=True)
class Pad:
    number: str
    x: float
    y: float
    w: float
    h: float
    kind: str = "smd"  # smd | thru | npth
    drill: float | None = None
    radius: float | None = None  # copper corner radius stated by the datasheet
    shape: str | None = None  # None derives from kind; "circle" or "custom"
    polygon: tuple[tuple[float, float], ...] | None = None  # custom outline, pad-relative
    paste: bool = True

    @property
    def bbox(self):
        if self.polygon:
            xs = [self.x + p[0] for p in self.polygon]
            ys = [self.y + p[1] for p in self.polygon]
            return min(xs), min(ys), max(xs), max(ys)
        return self.x - self.w / 2, self.y - self.h / 2, self.x + self.w / 2, self.y + self.h / 2

    def resolved_shape(self):
        if self.shape:
            return self.shape
        return "roundrect" if self.kind == "smd" else "circle"

    def rratio(self):
        short = min(self.w, self.h)
        radius = self.radius if self.radius is not None else min(MAX_CORNER_RADIUS, CORNER_FRACTION * short)
        return round(radius / short, 6)


@dataclass(frozen=True)
class PasteAperture:
    x: float
    y: float
    w: float
    h: float


@dataclass(frozen=True)
class Footprint:
    name: str
    description: str
    source: Source
    pads: tuple[Pad, ...]
    body: tuple[float, float, float, float]  # x0, y0, x1, y1 of the package body, footprint coords
    tags: str
    polarized: bool = True
    paste_apertures: tuple[PasteAperture, ...] = ()
    notes: tuple[str, ...] = ()
    round_body: bool = False  # fasteners: the body is a screw head of diameter body[2]-body[0]

    @property
    def tht(self):
        return any(p.kind == "thru" for p in self.pads)

    def copper_bbox(self):
        boxes = [p.bbox for p in self.pads]
        return (min(b[0] for b in boxes), min(b[1] for b in boxes), max(b[2] for b in boxes), max(b[3] for b in boxes))

    def courtyard(self):
        c = self.copper_bbox()
        b = self.body
        x0, y0 = min(c[0], b[0]) - COURTYARD_MARGIN, min(c[1], b[1]) - COURTYARD_MARGIN
        x1, y1 = max(c[2], b[2]) + COURTYARD_MARGIN, max(c[3], b[3]) + COURTYARD_MARGIN
        return (
            math.floor(x0 / GRID) * GRID,
            math.floor(y0 / GRID) * GRID,
            math.ceil(x1 / GRID) * GRID,
            math.ceil(y1 / GRID) * GRID,
        )

    def pin1(self):
        return next(p for p in self.pads if p.number == "1")


@dataclass(frozen=True)
class Pin:
    number: str
    name: str
    etype: str  # KiCad electrical type: input output bidirectional passive power_in power_out open_collector no_connect
    hidden: bool = False


@dataclass(frozen=True)
class Symbol:
    name: str
    reference: str
    value: str
    description: str
    keywords: str
    footprint: str  # "PROVES:<name>" for atomic parts, "" for generic ones
    footprint_filters: tuple[str, ...]
    datasheet: str
    left: tuple[Pin, ...] = ()
    right: tuple[Pin, ...] = ()
    top: tuple[Pin, ...] = ()
    bottom: tuple[Pin, ...] = ()
    fields: tuple[tuple[str, str], ...] = ()  # MPN, Manufacturer, LCSC Part
    graphic: str = "box"  # box | resistor | capacitor | led | schottky | solar | testpoint | mountinghole | burnwire
    show_pin_numbers: bool = True
    show_pin_names: bool = True

    def pins(self):
        return self.left + self.right + self.top + self.bottom


def clip_segment(seg, keepouts):
    """Split an axis-aligned segment so no piece enters any keep-out rectangle."""
    (x0, y0), (x1, y1) = seg
    horizontal = abs(y0 - y1) < 1e-9
    a, b = (min(x0, x1), max(x0, x1)) if horizontal else (min(y0, y1), max(y0, y1))
    fixed = y0 if horizontal else x0
    pieces = [(a, b)]
    for k in keepouts:
        lo, hi, flo, fhi = (k[0], k[2], k[1], k[3]) if horizontal else (k[1], k[3], k[0], k[2])
        if not (flo < fixed < fhi):
            continue
        nxt = []
        for s, e in pieces:
            if e <= lo or s >= hi:
                nxt.append((s, e))
                continue
            if s < lo:
                nxt.append((s, lo))
            if e > hi:
                nxt.append((hi, e))
        pieces = nxt
    out = []
    for s, e in pieces:
        if e - s < 0.2:
            continue
        out.append(((s, fixed), (e, fixed)) if horizontal else ((fixed, s), (fixed, e)))
    return out


def silk_outline(fp: Footprint):
    """Body outline pushed out by half the silk width, clipped clear of every pad."""
    off = SILK_WIDTH / 2
    x0, y0, x1, y1 = fp.body
    x0, y0, x1, y1 = x0 - off, y0 - off, x1 + off, y1 + off
    keep = [
        (
            b[0] - SILK_PAD_CLEARANCE - off,
            b[1] - SILK_PAD_CLEARANCE - off,
            b[2] + SILK_PAD_CLEARANCE + off,
            b[3] + SILK_PAD_CLEARANCE + off,
        )
        for b in (p.bbox for p in fp.pads)
    ]
    edges = [((x0, y0), (x1, y0)), ((x1, y0), (x1, y1)), ((x1, y1), (x0, y1)), ((x0, y1), (x0, y0))]
    segs = []
    for e in edges:
        segs.extend(clip_segment(e, keep))
    return [((snap(a[0]), snap(a[1])), (snap(b[0]), snap(b[1]))) for a, b in segs], keep


def pin1_marker(fp: Footprint, keep):
    """A silk dot beside pad 1 on the side facing away from the body centre, clear of all copper."""
    p = fp.pin1()
    bx0, by0, bx1, by1 = p.bbox
    cx = (fp.body[0] + fp.body[2]) / 2
    cy = (fp.body[1] + fp.body[3]) / 2
    r = 0.15
    gap = SILK_PAD_CLEARANCE + r + SILK_WIDTH / 2
    candidates = []
    if abs(p.x - cx) >= abs(p.y - cy):
        sx = -1 if p.x < cx else 1
        candidates.append((bx0 - gap if sx < 0 else bx1 + gap, p.y))
        candidates.append((p.x, by0 - gap))
    else:
        sy = -1 if p.y < cy else 1
        candidates.append((p.x, by0 - gap if sy < 0 else by1 + gap))
        candidates.append((bx0 - gap, p.y))
    for x, y in candidates:
        if all(not (k[0] - r < x < k[2] + r and k[1] - r < y < k[3] + r) for k in keep):
            return snap(x), snap(y), r
    x, y = candidates[0]
    return snap(x), snap(y), r


def pin1_chamfer(fp: Footprint):
    """Fab outline with the corner nearest pad 1 cut at 45 degrees."""
    x0, y0, x1, y1 = fp.body
    p = fp.pin1()
    c = min(1.0, 0.25 * min(x1 - x0, y1 - y0))
    corners = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
    near = min(range(4), key=lambda i: (corners[i][0] - p.x) ** 2 + (corners[i][1] - p.y) ** 2)
    pts = []
    for i, (cx, cy) in enumerate(corners):
        if i != near or not fp.polarized:
            pts.append((cx, cy))
            continue
        px, py = corners[i - 1]
        nx, ny = corners[(i + 1) % 4]
        pts.append(
            (cx + math.copysign(c, px - cx) if px != cx else cx, cy + math.copysign(c, py - cy) if py != cy else cy)
        )
        pts.append(
            (cx + math.copysign(c, nx - cx) if nx != cx else cx, cy + math.copysign(c, ny - cy) if ny != cy else cy)
        )
    return [(snap(x), snap(y)) for x, y in pts]
