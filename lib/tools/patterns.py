"""Land-pattern builders. Each takes the numbers a datasheet prints and returns pads in footprint coordinates."""

import math

from model import Pad


def two_terminal(pad_w, pad_h, centre):
    """Chip or SMA part: pad 1 on the left (cathode for polarized parts), pad 2 on the right."""
    return (Pad("1", -centre, 0, pad_w, pad_h), Pad("2", centre, 0, pad_w, pad_h))


def dual_row(n, pitch, span, pad_w, pad_h, radius=None):
    """Gull-wing or SON pins: 1..n/2 down the left column, n/2+1..n up the right, pin 1 top-left."""
    half = n // 2
    top = -(half - 1) * pitch / 2
    pads = [Pad(str(i + 1), -span / 2, round(top + i * pitch, 6), pad_w, pad_h, radius=radius) for i in range(half)]
    pads += [
        Pad(str(half + i + 1), span / 2, round(-top - i * pitch, 6), pad_w, pad_h, radius=radius) for i in range(half)
    ]
    return tuple(pads)


def header_2row(n, pitch, row_pitch, drill, pad):
    """Two-row through-hole header, pin 1 at the origin, odd pins along +x, even pins one row below."""
    pads = []
    for i in range(n // 2):
        pads.append(
            Pad(
                str(2 * i + 1),
                i * pitch,
                0,
                pad,
                pad,
                kind="thru",
                drill=drill,
                shape="roundrect" if i == 0 else "circle",
            )
        )
        pads.append(Pad(str(2 * i + 2), i * pitch, row_pitch, pad, pad, kind="thru", drill=drill, shape="circle"))
    return tuple(sorted(pads, key=lambda p: int(p.number)))


# IPC-7351B chip-component fillet goals (Table 3-5 for 1608 and larger, Table 3-6 below 1608), density level B
# (nominal), with KiCad's library tolerances F = 0.1 fabrication and P = 0.05 placement and its rounding steps.
IPC_CHIP_NOMINAL = {
    "small": dict(toe=0.20, heel=0.0, side=0.0, step=0.02),
    "large": dict(toe=0.35, heel=0.0, side=0.0, step=0.05),
}
IPC_FAB_TOL = 0.1
IPC_PLACE_TOL = 0.05


def ipc_chip(length, width, terminal, small):
    """Two-terminal chip land from body (min, max) tolerances by the IPC-7351B Z/G/X equations.

    Returns (pads, note) where the note records the inputs and the Z, G, X result.
    """
    goal = IPC_CHIP_NOMINAL["small" if small else "large"]
    (lmin, lmax), (wmin, wmax), (tmin, tmax) = length, width, terminal
    ltol, wtol, ttol = lmax - lmin, wmax - wmin, tmax - tmin
    smin, smax = lmin - 2 * tmax, lmax - 2 * tmin
    s_rms = math.sqrt(ltol**2 + 2 * ttol**2)
    smax_rms = smax - ((smax - smin) - s_rms) / 2
    fp_tol = IPC_FAB_TOL**2 + IPC_PLACE_TOL**2
    z = lmin + 2 * goal["toe"] + math.sqrt(ltol**2 + fp_tol)
    g = smax_rms - 2 * goal["heel"] - math.sqrt(s_rms**2 + fp_tol)
    x = wmin + 2 * goal["side"] + math.sqrt(wtol**2 + fp_tol)
    z, g, x = (round(round(v / goal["step"]) * goal["step"], 4) for v in (z, g, x))
    pad_len = round((z - g) / 2, 4)
    note = (
        f"IPC-7351B nominal from body L {lmin}-{lmax}, W {wmin}-{wmax}, terminal {tmin}-{tmax}: Z={z:g} G={g:g} X={x:g}"
    )
    return two_terminal(pad_len, x, round((z + g) / 4, 4)), note
