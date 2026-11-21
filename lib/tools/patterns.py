"""Land-pattern builders. Each takes the numbers a datasheet prints and returns pads in footprint coordinates."""

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
