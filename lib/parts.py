"""Every part in the PROVES library, one entry each, with the datasheet facts it rests on.

Numbers here are copied from the cited figure. Derived geometry (silk, fab, courtyard,
pin-1 marks, symbol bodies) comes from lib/tools/model.py per lib/SPEC.md.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "tools"))

from model import Footprint, Pad, PasteAperture, Pin, Source, Symbol  # noqa: E402
from patterns import dual_row, header_2row, ipc_chip, two_terminal  # noqa: E402

LIB = "PROVES"

# ------------------------------------------------------------------ sources

SAMSUNG_CL = Source(
    "Samsung Electro-Mechanics MLCC catalog (CL05, CL21), Standard & High Capacitors",
    "https://datasheet.lcsc.com/datasheet/pdf/02336ea48ea44ca18c72517dd3cb7b47.pdf?productCode=C15195",
    "6",
    "Structure and Dimensions table (L, W, BW)",
)
YAGEO_CC = Source(
    "YAGEO CC series X7R product specification V.26 (Nov 2024)",
    "https://datasheet.lcsc.com/datasheet/pdf/23ccee80ee542e7cf156a772bb589942.pdf?productCode=C14663",
    "3",
    "Dimension table, code DA (0603); FH 0603B code DA body folded in",
)
UNIROYAL_R = Source(
    "UNI-ROYAL thick film chip resistors data sheet V.3 (Feb 2019)",
    "https://datasheet.lcsc.com/datasheet/pdf/0a975aaa49b7c97f38a963127be4a823.pdf?productCode=C25744",
    "4",
    "Dimension table (L, W, B bottom terminal)",
)
KENTO_LED = Source(
    "KENTO KT-0603B 0603 LED datasheet",
    "https://datasheet.lcsc.com/datasheet/pdf/1096dc34dcf507e4677a7d79542be828.pdf?productCode=C2288",
    "2",
    "Package Profile & Soldering PAD Suggested",
)
COMCHIP_SMA = Source(
    "Comchip CDBA240LL-HF datasheet Rev D (QW-JL008)",
    "https://datasheet.lcsc.com/datasheet/pdf/0ad6c82af01d682deff9bf6691cf993a.pdf?productCode=C2886093",
    "4",
    "Suggested PAD Layout, DO-214AC (SMA)",
)
HIROSE_DF11 = Source(
    "Hirose DF11-**DP-2DSA(08) drawing EDC3-084377-01",
    "https://datasheet.lcsc.com/datasheet/pdf/0fb75dbeb6fa72e0d40172102f5c9d8d.pdf?productCode=C506668",
    "1",
    "Recommended pattern (board thickness t=1.6mm); A/B table",
)
MOLEX_504050 = Source(
    "Molex 504050-0691 sales drawing 5040500000-SD rev B",
    "https://www.molex.com/content/dam/molex/molex-dot-com/products/automated/en-us/salesdrawingpdf/504/504050/5040500691_sd.pdf",
    "2",
    "Recommended pattern layout (REF.); pad coordinates read from 5040500691.dxf",
)
ISO_7380 = Source(
    "ISO 7380-1 button head screw, M3 head diameter dk max 5.7; ISO 273 fine clearance hole 3.2",
    "https://www.iso.org/standard/53582.html",
    "Table 1",
    "dk max, M3",
)
ISO_7046 = Source(
    "ISO 7046-1 (DIN 965) countersunk screw, M3 actual head diameter dk max 5.5; ISO 273 fine clearance hole 3.2",
    "https://www.iso.org/standard/36592.html",
    "Table 1",
    "dk actual max, M3",
)
TI_DRV2605L = Source(
    "TI DRV2605L datasheet SLOS854D",
    "https://www.ti.com/lit/ds/symlink/drv2605l.pdf",
    "71",
    "DGS0010A example board layout 4221984/A",
)
TI_TCA4311A = Source(
    "TI TCA4311A datasheet SCPS226C",
    "https://www.ti.com/lit/ds/symlink/tca4311a.pdf",
    "25",
    "DGK0008A example board layout 4214862/A",
)
TI_TCA4307 = Source(
    "TI TCA4307 datasheet SCPS270B",
    "https://www.ti.com/lit/ds/symlink/tca4307.pdf",
    "3",
    "Pin configuration, 8-pin VSSOP DGK",
)
TI_TMP112 = Source(
    "TI TMP112 datasheet SBOS473L",
    "https://www.ti.com/lit/ds/symlink/tmp112.pdf",
    "40",
    "DRL0006A example board layout 4223266/C",
)
TI_CSD17576 = Source(
    "TI CSD17576Q5B datasheet SLPS497A",
    "https://www.ti.com/lit/ds/symlink/csd17576q5b.pdf",
    "9",
    "7.2 Recommended PCB pattern and 7.3 recommended stencil pattern",
)
VISHAY_VEML6031 = Source(
    "Vishay VEML6031X00 datasheet rev 1.4, doc 80007",
    "https://www.vishay.com/docs/80007/veml6031x00.pdf",
    "12",
    "Package dimensions, recommended footprint",
)
VISHAY_VEML7700 = Source(
    "Vishay VEML7700 datasheet rev 1.8, doc 84286",
    "https://www.vishay.com/docs/84286/veml7700.pdf",
    "10",
    "Proposed pad layout from component side, top view",
)
ANYSOLAR_SM101 = Source(
    "ANYSOLAR SM101K07TF datasheet (May 2021)",
    "http://konkur.de/content/files/pdf/anysolar/SM101K07TF%20DATA%20SHEET%20202105.pdf",
    "3",
    "Package front-side and back-side view",
)
ANYSOLAR_SM261 = Source(
    "ANYSOLAR SM261K10TF datasheet (May 2021)",
    "http://konkur.de/content/files/pdf/anysolar/SM261K10TF%20DATA%20SHEET%20202105.pdf",
    "3",
    "Package front-side and back-side view",
)
ANYSOLAR_SM531 = Source(
    "ANYSOLAR SM531K10TF datasheet (May 2021)",
    "http://konkur.de/content/files/pdf/anysolar/SM531K10TF%20DATA%20SHEET%20202105.pdf",
    "3",
    "Package front-side and back-side view",
)
HOUSE = Source(
    "PROVES house part (no vendor drawing exists)",
    "https://docs.proveskit.com",
    "-",
    "geometry kept from the flown XY V4 and 2U V1a boards",
)

CELL_LAND = (
    "Cell land: plated hole the size of the cell's 3.0 mm contact, soldered from the board's back "
    "through the hole; 5.0 mm pad as flown on the XY and 2U faces"
)


def fp(name, description, source, pads, body, tags, **kw):
    return Footprint(name, description, source, tuple(pads), body, tags, **kw)


def passive(n="1"):
    return Pin(n, "~", "passive")


# ------------------------------------------------------------------ footprints

_C0402, _C0402_NOTE = ipc_chip((0.95, 1.05), (0.45, 0.55), (0.15, 0.35), small=True)
C_0402 = fp(
    "C_0402_1005Metric",
    "Chip capacitor 0402 (1005 metric), IPC-7351B nominal",
    SAMSUNG_CL,
    _C0402,
    (-0.5, -0.25, 0.5, 0.25),
    "capacitor 0402 1005",
    polarized=False,
    notes=(_C0402_NOTE, "Samsung CL05 code 5: L 1.00+-0.05, W 0.50+-0.05, BW 0.25+-0.10"),
)
_C0603, _C0603_NOTE = ipc_chip((1.5, 1.7), (0.7, 0.9), (0.15, 0.6), small=False)
C_0603 = fp(
    "C_0603_1608Metric",
    "Chip capacitor 0603 (1608 metric), IPC-7351B nominal",
    YAGEO_CC,
    _C0603,
    (-0.8, -0.4, 0.8, 0.4),
    "capacitor 0603 1608",
    polarized=False,
    notes=(_C0603_NOTE, "Envelope of YAGEO CC0603 DA (BW 0.2-0.6) and FH 0603B DA (WB 0.35+-0.20)"),
)
_C0805, _C0805_NOTE = ipc_chip((1.9, 2.1), (1.15, 1.35), (0.2, 0.7), small=False)
C_0805 = fp(
    "C_0805_2012Metric",
    "Chip capacitor 0805 (2012 metric), IPC-7351B nominal",
    SAMSUNG_CL,
    _C0805,
    (-1.0, -0.625, 1.0, 0.625),
    "capacitor 0805 2012",
    polarized=False,
    notes=(_C0805_NOTE, "Samsung CL21 code F: L 2.00+-0.10, W 1.25+-0.10, BW 0.5 +0.2/-0.3"),
)
_R0402, _R0402_NOTE = ipc_chip((0.9, 1.1), (0.45, 0.55), (0.15, 0.35), small=True)
R_0402 = fp(
    "R_0402_1005Metric",
    "Chip resistor 0402 (1005 metric), IPC-7351B nominal",
    UNIROYAL_R,
    _R0402,
    (-0.5, -0.25, 0.5, 0.25),
    "resistor 0402 1005",
    polarized=False,
    notes=(_R0402_NOTE, "UNI-ROYAL 0402: L 1.00+-0.10, W 0.50+-0.05, B 0.25+-0.10"),
)
_R0603, _R0603_NOTE = ipc_chip((1.5, 1.7), (0.7, 0.9), (0.1, 0.5), small=False)
R_0603 = fp(
    "R_0603_1608Metric",
    "Chip resistor 0603 (1608 metric), IPC-7351B nominal",
    UNIROYAL_R,
    _R0603,
    (-0.8, -0.4, 0.8, 0.4),
    "resistor 0603 1608",
    polarized=False,
    notes=(_R0603_NOTE, "UNI-ROYAL 0603: L 1.60+-0.10, W 0.80+-0.10, B 0.30+-0.20"),
)
_LED0603, _LED0603_NOTE = ipc_chip((1.5, 1.7), (0.7, 0.9), (0.2, 0.4), small=False)
LED_0603 = fp(
    "LED_0603_1608Metric",
    "Chip LED 0603 (1608 metric), IPC-7351B nominal, pad 1 cathode",
    KENTO_LED,
    _LED0603,
    (-0.8, -0.4, 0.8, 0.4),
    "LED 0603 1608",
    notes=(
        _LED0603_NOTE,
        "KENTO KT-0603: 1.6 x 0.8 body, 0.30 terminal, +-0.10 general tolerance",
        "Datasheet pin 2 (cathode) is pad 1 here",
    ),
)
D_SMA = fp(
    "D_SMA_DO-214AC",
    "DO-214AC (SMA) diode, pad 1 cathode",
    COMCHIP_SMA,
    two_terminal(2.60, 1.70, 2.05),
    (-2.15, -1.3, 2.15, 1.3),
    "diode SMA DO-214AC",
    notes=("A=4.10 B=2.60 C=1.70 D=6.70 E=1.50",),
)

DF11_6 = fp(
    "Hirose_DF11-6DP-2DSA_2x03_P2.00mm_Vertical",
    "Hirose DF11 2x03 2.00 mm vertical header",
    HIROSE_DF11,
    header_2row(6, 2.0, 2.0, 0.85, 1.45),
    (-2.0, -1.5, 6.0, 3.5),
    "connector Hirose DF11 2x03",
    notes=(
        "Hole 0.8 +0.1/-0 drilled at 0.85; pad = drill + 0.6 (SPEC THT rule)",
        "Top view rotated 180 deg: contact 2 behind contact 1, contact 3 beside it",
    ),
)
DF11_4 = fp(
    "Hirose_DF11-4DP-2DSA_2x02_P2.00mm_Vertical",
    "Hirose DF11 2x02 2.00 mm vertical header",
    HIROSE_DF11,
    header_2row(4, 2.0, 2.0, 0.85, 1.45),
    (-2.0, -1.5, 4.0, 3.5),
    "connector Hirose DF11 2x02",
    notes=(
        "Hole 0.8 +0.1/-0 drilled at 0.85; pad = drill + 0.6 (SPEC THT rule)",
        "Top view rotated 180 deg: contact 2 behind contact 1, contact 3 beside it",
    ),
)

_MOLEX_SIG_Y = 2.795
MOLEX_6 = fp(
    "Molex_PicoLock_504050-0691_1x06_P1.50mm_Horizontal",
    "Molex Pico-Lock 504050-0691 1x06 1.50 mm right-angle header",
    MOLEX_504050,
    [Pad(str(i + 1), round(3.75 - 1.5 * i, 6), _MOLEX_SIG_Y, 0.6, 1.0) for i in range(6)]
    + [
        Pad("MP", 6.355, round(_MOLEX_SIG_Y - 5.19, 6), 1.25, 1.8),
        Pad("MP", -6.355, round(_MOLEX_SIG_Y - 5.19, 6), 1.25, 1.8),
    ],
    (-6.375, round(_MOLEX_SIG_Y - 6.09, 6), 6.375, round(_MOLEX_SIG_Y + 0.01, 6)),
    "connector Molex Pico-Lock 504050",
    notes=(
        "Signal 0.6 x 1.0 at 1.5 pitch; nails 1.25 x 1.8, 1.68 beyond the outer signal pad edge, "
        "3.79 behind the signal pad edge",
        "Circuit 1 on the right in top view",
    ),
)

MH_ISO7380 = fp(
    "MountingHole_3.2mm_M3_ISO7380_Pad",
    "M3 mounting hole, plated pad for an ISO 7380 button head",
    ISO_7380,
    [Pad("1", 0, 0, 5.7, 5.7, kind="thru", drill=3.2)],
    (-2.85, -2.85, 2.85, 2.85),
    "mounting hole M3 ISO7380",
    polarized=False,
    round_body=True,
)
MH_DIN965 = fp(
    "MountingHole_3.2mm_M3_DIN965_Pad",
    "M3 mounting hole, plated pad for a DIN 965 countersunk head",
    ISO_7046,
    [Pad("1", 0, 0, 5.5, 5.5, kind="thru", drill=3.2)],
    (-2.75, -2.75, 2.75, 2.75),
    "mounting hole M3 DIN965",
    polarized=False,
    round_body=True,
)

TI_DGS = fp(
    "TI_DGS0010A_VSSOP-10_3x3mm_P0.5mm",
    "TI DGS0010A VSSOP-10 3 x 3 mm, 0.5 mm pitch",
    TI_DRV2605L,
    dual_row(10, 0.5, 4.4, 1.45, 0.3, radius=0.05),
    (-1.5, -1.5, 1.5, 1.5),
    "VSSOP-10 DGS TI",
    notes=("10X (1.45) x 10X (0.3), 8X (0.5) pitch, (4.4) row span, R0.05",),
)
TI_DGK = fp(
    "TI_DGK0008A_VSSOP-8_3x3mm_P0.65mm",
    "TI DGK0008A VSSOP-8 3 x 3 mm, 0.65 mm pitch",
    TI_TCA4311A,
    dual_row(8, 0.65, 4.4, 1.4, 0.45, radius=0.05),
    (-1.5, -1.5, 1.5, 1.5),
    "VSSOP-8 DGK MSOP-8 TI",
    notes=("8X (1.4) x 8X (0.45), 6X (0.65) pitch, (4.4) row span, R0.05",),
)
TI_DRL = fp(
    "TI_DRL0006A_SOT-563",
    "TI DRL0006A SOT-563 1.6 x 1.2 mm, 0.5 mm pitch",
    TI_TMP112,
    dual_row(6, 0.5, 1.48, 0.67, 0.3, radius=0.05),
    (-0.6, -0.8, 0.6, 0.8),
    "SOT-563 DRL TI",
    notes=("6X (0.67) x 6X (0.3), 4X (0.5) pitch, (1.48) row span, R0.05",),
)

# CSD17576Q5B: TI's pattern shows pin 1 bottom-right; rotated 180 deg so pin 1 sits top-left.
# Drain (pins 5-8) is one copper island: a 3.85 x 4.52 body plus four 0.59 x 0.71 fingers.
_Q5B_FINGER_X = (2.866, 3.456)
_Q5B_ROWS = (-1.905, -0.635, 0.635, 1.905)
_q5b_poly = [(-0.984, -2.26), (2.866, -2.26)]
for _y in _Q5B_ROWS:
    _q5b_poly += [
        (_Q5B_FINGER_X[0], _y - 0.355),
        (_Q5B_FINGER_X[1], _y - 0.355),
        (_Q5B_FINGER_X[1], _y + 0.355),
        (_Q5B_FINGER_X[0], _y + 0.355),
    ]
_q5b_poly += [(2.866, 2.26), (-0.984, 2.26)]
_Q5B_ANCHOR = (0.941, 0.0)
TI_Q5B = fp(
    "TI_DNK0008A_VSON-CLIP-8_5x6mm_P1.27mm",
    "TI DNK VSON-CLIP 5 x 6 mm (SON 5x6, Q5B), drain island",
    TI_CSD17576,
    [Pad(str(i + 1), -2.770, _Q5B_ROWS[i], 1.372, 0.71, paste=False) for i in range(4)]
    + [
        Pad(
            "5",
            _Q5B_ANCHOR[0],
            _Q5B_ANCHOR[1],
            0.5,
            0.5,
            shape="custom",
            paste=False,
            polygon=tuple((round(x - _Q5B_ANCHOR[0], 6), round(y - _Q5B_ANCHOR[1], 6)) for x, y in _q5b_poly),
        )
    ]
    + [Pad(str(8 - i), 3.161, _Q5B_ROWS[i], 0.59, 0.71, paste=False) for i in range(3)],
    (-3.0, -2.5, 3.0, 2.5),
    "SON 5x6 Q5B DNK VSON-CLIP TI MOSFET",
    paste_apertures=tuple(
        [PasteAperture(-2.758, y, 1.072, 0.562) for y in _Q5B_ROWS]
        + [PasteAperture(2.910, y, 0.766, 0.508) for y in _Q5B_ROWS]
        + [PasteAperture(x, y, 1.294, 0.746) for x in (1.594, -0.050) for y in (-1.569, -0.523, 0.523, 1.569)]
    ),
    notes=(
        "Pads 1-4 1.372 x 0.710 at 1.270 pitch, 1.100 gap to drain; drain 4.440 x 4.520 with 0.590 fingers",
        "Stencil per 7.3; drain-row gap 0.300 is dimensioned only at the centre row and applied to all rows",
    ),
)

VEML6031 = fp(
    "Vishay_VEML6031X00_2.67x2.45mm",
    "Vishay VEML6031X00 ambient light sensor, 6 pads",
    VISHAY_VEML6031,
    [
        Pad("1", 0, 1.035, 0.85, 0.79),
        Pad("2", 1.145, 0.6, 0.79, 0.85),
        Pad("3", 1.145, -0.6, 0.79, 0.85),
        Pad("4", 0, -1.035, 0.85, 0.79),
        Pad("5", -1.145, -0.6, 0.79, 0.85),
        Pad("6", -1.145, 0.6, 0.79, 0.85),
    ],
    (-1.335, -1.225, 1.335, 1.225),
    "light sensor VEML6031 Vishay",
    notes=("Side pads 0.79 x 0.85 at 1.2 pitch with 1.5 between them; centre pads 0.85 x 0.79, 1.28 apart",),
)
VEML7700 = fp(
    "Vishay_VEML7700-TT_TopView",
    "Vishay VEML7700-TT ambient light sensor, top-view mounting",
    VISHAY_VEML7700,
    [Pad(str(i + 1), round(-1.905 + 1.27 * i, 6), 0, 0.7, 1.6) for i in range(4)],
    (-3.4, -1.5, 3.4, 1.5),
    "light sensor VEML7700 Vishay",
    notes=(
        "4 x (0.7 x 1.6) at 1.27 pitch; body position relative to the pads is not dimensioned, "
        "fab outline centred on the pad row",
    ),
)

SM101 = fp(
    "Anysolar_SM101K07TF",
    "ANYSOLAR SM101K07TF solar cell 22 x 35 mm, two back contacts",
    ANYSOLAR_SM101,
    [Pad("1", -4.5, -13.0, 5.0, 5.0, kind="thru", drill=3.0), Pad("2", 4.5, -13.0, 5.0, 5.0, kind="thru", drill=3.0)],
    (-11.0, -17.5, 11.0, 17.5),
    "solar cell ANYSOLAR SM101K07TF",
    notes=(
        "Contacts 3.0 dia, 4.5 from the top edge, 6.5 from each side; back view mirrored to top view, pad 1 +",
        CELL_LAND,
    ),
)
SM261 = fp(
    "Anysolar_SM261K10TF",
    "ANYSOLAR SM261K10TF solar cell 64 x 45 mm, two back contacts",
    ANYSOLAR_SM261,
    [Pad("1", 22.0, 0, 5.0, 5.0, kind="thru", drill=3.0), Pad("2", -22.0, 0, 5.0, 5.0, kind="thru", drill=3.0)],
    (-32.0, -22.5, 32.0, 22.5),
    "solar cell ANYSOLAR SM261K10TF",
    notes=(
        "Contacts 10.00 from each side on the centreline; contact size not dimensioned, 3.0 by drawing scale "
        "and family; back view mirrored to top view, pad 1 +",
        CELL_LAND,
    ),
)
SM531 = fp(
    "Anysolar_SM531K10TF",
    "ANYSOLAR SM531K10TF solar cell 89 x 65 mm, four back contacts",
    ANYSOLAR_SM531,
    [
        Pad("1", 22.2, 29.5, 5.0, 5.0, kind="thru", drill=3.0),
        Pad("2", 22.2, -29.5, 5.0, 5.0, kind="thru", drill=3.0),
        Pad("3", -22.2, -29.5, 5.0, 5.0, kind="thru", drill=3.0),
        Pad("4", -22.2, 29.5, 5.0, 5.0, kind="thru", drill=3.0),
    ],
    (-44.5, -32.5, 44.5, 32.5),
    "solar cell ANYSOLAR SM531K10TF",
    notes=(
        "Contacts 3.0 dia, 22.3 from each side, 3.0 from top and bottom (bottom row per SM531K10L drawing)",
        "Back view mirrored to top view: pads 1/2 are the +/- of one half, 3/4 of the other",
        CELL_LAND,
    ),
)

TEST_PAD = fp(
    "TestPad_2.5x2.5mm",
    "Square SMD test pad 2.5 mm for probe or wire tack",
    HOUSE,
    [Pad("1", 0, 0, 2.5, 2.5)],
    (-1.25, -1.25, 1.25, 1.25),
    "test point pad",
    polarized=False,
)
BURN_WIRE = fp(
    "BurnWire_2xTHT_P5.08mm",
    "Burn wire tie-down: two plated holes the FireLine loop passes through",
    HOUSE,
    [Pad("1", 0, 0, 1.4, 1.4, kind="thru", drill=0.7), Pad("2", 5.08, 0, 1.4, 1.4, kind="thru", drill=0.7)],
    (-0.7, -0.7, 5.78, 0.7),
    "burn wire nichrome FireLine",
    polarized=False,
)

# ------------------------------------------------------------------ symbols


def generic(name, ref, desc, kw, filters, graphic, pins, **kw2):
    return Symbol(
        name,
        ref,
        name,
        desc,
        kw,
        "",
        filters,
        "~",
        left=pins,
        graphic=graphic,
        show_pin_numbers=False,
        show_pin_names=False,
        **kw2,
    )


def atomic(name, ref, desc, kw, footprint, datasheet, mpn, maker, lcsc, graphic="box", **pins):
    fields = (("MPN", mpn), ("Manufacturer", maker)) + ((("LCSC Part", lcsc),) if lcsc else ())
    return Symbol(
        name, ref, name, desc, kw, f"{LIB}:{footprint.name}", (), datasheet, fields=fields, graphic=graphic, **pins
    )


SYM_R = generic(
    "R", "R", "Resistor, IEEE 315 zig-zag", "R resistor", ("R_*",), "resistor", (passive("1"), passive("2"))
)
SYM_C = generic("C", "C", "Unpolarized capacitor", "C capacitor", ("C_*",), "capacitor", (passive("1"), passive("2")))
SYM_LED = generic(
    "LED",
    "D",
    "Light emitting diode, pin 1 cathode",
    "LED diode",
    ("LED_*",),
    "led",
    (Pin("1", "K", "passive"), Pin("2", "A", "passive")),
)
SYM_TP = generic("TestPoint", "TP", "Test pad", "test point", ("TestPad*",), "testpoint", (passive("1"),))
SYM_MH = generic(
    "MountingHole_Pad",
    "H",
    "Plated mounting hole tied to a net",
    "mounting hole",
    ("MountingHole*",),
    "mountinghole",
    (passive("1"),),
)
SYM_BW = generic(
    "BurnWire",
    "J",
    "Burn wire tie-down points; the FireLine loop runs between them",
    "burn wire",
    ("BurnWire*",),
    "burnwire",
    (passive("1"), passive("2")),
)

SYM_CDBA = atomic(
    "CDBA240LL-HF",
    "D",
    "Schottky rectifier 40 V 2 A, ultra low VF, SMA",
    "diode schottky",
    D_SMA,
    COMCHIP_SMA.url,
    "CDBA240LL-HF",
    "Comchip",
    "C2886093",
    graphic="schottky",
    left=(Pin("1", "K", "passive"), Pin("2", "A", "passive")),
)
SYM_SM101 = atomic(
    "SM101K07TF",
    "SC",
    "Solar cell 4.84 V Voc, 41.9 mA Isc, 22 x 35 mm",
    "solar cell",
    SM101,
    ANYSOLAR_SM101.url,
    "SM101K07TF",
    "ANYSOLAR",
    "",
    graphic="solar",
    left=(Pin("1", "+", "passive"), Pin("2", "-", "passive")),
)
SYM_SM261 = atomic(
    "SM261K10TF",
    "SC",
    "Solar cell 6.91 V Voc, 109 mA Isc, 64 x 45 mm",
    "solar cell",
    SM261,
    ANYSOLAR_SM261.url,
    "SM261K10TF",
    "ANYSOLAR",
    "C22086161",
    graphic="solar",
    left=(Pin("1", "+", "passive"), Pin("2", "-", "passive")),
)
SYM_SM531 = atomic(
    "SM531K10TF",
    "SC",
    "Solar cell module 89 x 65 mm, two halves with their own contacts",
    "solar cell",
    SM531,
    ANYSOLAR_SM531.url,
    "SM531K10TF",
    "ANYSOLAR",
    "",
    left=(Pin("1", "+A", "passive"), Pin("2", "-A", "passive")),
    right=(Pin("3", "+B", "passive"), Pin("4", "-B", "passive")),
)
SYM_DF11_6 = atomic(
    "DF11-6DP-2DSA",
    "J",
    "Hirose DF11 2x03 2.00 mm header",
    "connector DF11",
    DF11_6,
    HIROSE_DF11.url,
    "DF11-6DP-2DSA(08)",
    "Hirose",
    "C506668",
    left=tuple(Pin(str(n), f"Pin_{n}", "passive") for n in (1, 3, 5)),
    right=tuple(Pin(str(n), f"Pin_{n}", "passive") for n in (2, 4, 6)),
)
SYM_DF11_4 = atomic(
    "DF11-4DP-2DSA",
    "J",
    "Hirose DF11 2x02 2.00 mm header",
    "connector DF11",
    DF11_4,
    HIROSE_DF11.url,
    "DF11-4DP-2DSA(08)",
    "Hirose",
    "",
    left=tuple(Pin(str(n), f"Pin_{n}", "passive") for n in (1, 3)),
    right=tuple(Pin(str(n), f"Pin_{n}", "passive") for n in (2, 4)),
)
SYM_MOLEX_6 = atomic(
    "504050-0691",
    "J",
    "Molex Pico-Lock 1x06 1.50 mm right-angle header",
    "connector Pico-Lock",
    MOLEX_6,
    MOLEX_504050.url,
    "5040500691",
    "Molex",
    "C563981",
    left=tuple(Pin(str(n), f"Pin_{n}", "passive") for n in range(1, 7)),
)
SYM_DRV2605L = atomic(
    "DRV2605LDGS",
    "U",
    "Haptic driver for ERM and LRA, I2C, VSSOP-10",
    "haptic driver I2C",
    TI_DGS,
    TI_DRV2605L.url,
    "DRV2605LDGSR",
    "Texas Instruments",
    "C527464",
    left=(
        Pin("2", "SCL", "input"),
        Pin("3", "SDA", "bidirectional"),
        Pin("4", "IN/TRIG", "input"),
        Pin("5", "EN", "input"),
    ),
    right=(Pin("7", "OUT+", "output"), Pin("9", "OUT-", "output"), Pin("1", "REG", "power_out")),
    top=(Pin("10", "VDD", "power_in"), Pin("6", "VDD/NC", "power_in")),
    bottom=(Pin("8", "GND", "power_in"),),
)
SYM_TMP112 = atomic(
    "TMP112AIDRLR",
    "U",
    "Digital temperature sensor, I2C, +-0.5 C, SOT-563",
    "temperature sensor I2C",
    TI_DRL,
    TI_TMP112.url,
    "TMP112AIDRLR",
    "Texas Instruments",
    "C28927",
    left=(Pin("1", "SCL", "input"), Pin("6", "SDA", "bidirectional"), Pin("4", "ADD0", "input")),
    right=(Pin("3", "ALERT", "open_collector"),),
    top=(Pin("5", "V+", "power_in"),),
    bottom=(Pin("2", "GND", "power_in"),),
)
_TCA_PINS = dict(
    left=(Pin("3", "SCLIN", "bidirectional"), Pin("6", "SDAIN", "bidirectional"), Pin("1", "EN", "input")),
    right=(
        Pin("2", "SCLOUT", "bidirectional"),
        Pin("7", "SDAOUT", "bidirectional"),
        Pin("5", "READY", "open_collector"),
    ),
    top=(Pin("8", "VCC", "power_in"),),
    bottom=(Pin("4", "GND", "power_in"),),
)
SYM_TCA4311A = atomic(
    "TCA4311ADGKR",
    "U",
    "Hot-swap I2C buffer, VSSOP-8",
    "I2C buffer hot swap",
    TI_DGK,
    TI_TCA4311A.url,
    "TCA4311ADGKR",
    "Texas Instruments",
    "C130025",
    **_TCA_PINS,
)
SYM_TCA4307 = atomic(
    "TCA4307DGKR",
    "U",
    "Hot-swap I2C buffer with stuck-bus recovery, VSSOP-8",
    "I2C buffer hot swap",
    TI_DGK,
    TI_TCA4307.url,
    "TCA4307DGKR",
    "Texas Instruments",
    "C880333",
    **_TCA_PINS,
)
SYM_CSD17576 = atomic(
    "CSD17576Q5B",
    "Q",
    "N-channel NexFET 30 V 1.7 mOhm, SON 5x6",
    "MOSFET N-channel",
    TI_Q5B,
    TI_CSD17576.url,
    "CSD17576Q5B",
    "Texas Instruments",
    "",
    graphic="nmos",
    left=(Pin("4", "G", "input"),),
    top=(
        Pin("5", "D", "passive"),
        Pin("6", "D", "passive", hidden=True),
        Pin("7", "D", "passive", hidden=True),
        Pin("8", "D", "passive", hidden=True),
    ),
    bottom=(Pin("1", "S", "passive"), Pin("2", "S", "passive", hidden=True), Pin("3", "S", "passive", hidden=True)),
)
SYM_VEML6031 = atomic(
    "VEML6031X00",
    "U",
    "Ambient light sensor, I2C, 2.67 x 2.45 mm",
    "light sensor I2C",
    VEML6031,
    VISHAY_VEML6031.url,
    "VEML6031X00",
    "Vishay",
    "C3678616",
    left=(Pin("5", "SCL", "input"), Pin("2", "SDA", "bidirectional")),
    right=(Pin("3", "INT", "open_collector"),),
    top=(Pin("6", "VDD", "power_in"),),
    bottom=(Pin("1", "GND", "power_in"), Pin("4", "GND", "power_in")),
)
SYM_VEML7700 = atomic(
    "VEML7700-TT",
    "U",
    "Ambient light sensor, I2C, top-view mounting",
    "light sensor I2C",
    VEML7700,
    VISHAY_VEML7700.url,
    "VEML7700-TT",
    "Vishay",
    "C1850416",
    left=(Pin("1", "SCL", "input"), Pin("4", "SDA", "bidirectional")),
    top=(Pin("2", "VDD", "power_in"),),
    bottom=(Pin("3", "GND", "power_in"),),
)

FOOTPRINTS = (
    C_0402,
    C_0603,
    C_0805,
    R_0402,
    R_0603,
    LED_0603,
    D_SMA,
    DF11_4,
    DF11_6,
    MOLEX_6,
    MH_ISO7380,
    MH_DIN965,
    TI_DGS,
    TI_DGK,
    TI_DRL,
    TI_Q5B,
    VEML6031,
    VEML7700,
    SM101,
    SM261,
    SM531,
    TEST_PAD,
    BURN_WIRE,
)
SYMBOLS = (
    SYM_R,
    SYM_C,
    SYM_LED,
    SYM_TP,
    SYM_MH,
    SYM_BW,
    SYM_CDBA,
    SYM_SM101,
    SYM_SM261,
    SYM_SM531,
    SYM_DF11_4,
    SYM_DF11_6,
    SYM_MOLEX_6,
    SYM_DRV2605L,
    SYM_TMP112,
    SYM_TCA4311A,
    SYM_TCA4307,
    SYM_CSD17576,
    SYM_VEML6031,
    SYM_VEML7700,
)

# What each footprint on the six live boards becomes. LOGO and dfsdf are board artwork, not parts.
REPLACES = {
    "Capacitor_SMD:C_0402_1005Metric": C_0402,
    "Capacitor_SMD:C_0603_1608Metric": C_0603,
    "Capacitor_SMD:C_0805_2012Metric": C_0805,
    "Resistor_SMD:R_0402_1005Metric": R_0402,
    "Resistor_SMD:R_0603_1608Metric": R_0603,
    "LED_SMD:LED_0603_1608Metric": LED_0603,
    "SolarPanelBoards:DO-214AC": D_SMA,
    "Connector_Hirose:Hirose_DF11-4DP-2DSA_2x02_P2.00mm_Vertical": DF11_4,
    "Connector_Hirose:Hirose_DF11-6DP-2DSA_2x03_P2.00mm_Vertical": DF11_6,
    "Molex 6 pos:MOLEX_5040500691": MOLEX_6,
    "easyeda2kicad:CONN-SMD_6P-P1.50_A1501WRB-S-6P": MOLEX_6,
    "MountingHole:MountingHole_3.2mm_M3_ISO7380_Pad": MH_ISO7380,
    "MountingHole:MountingHole_3.2mm_M3_DIN965_Pad": MH_DIN965,
    "Package_SO:VSSOP-10_3x3mm_P0.5mm": TI_DGS,
    "Package_SO:VSSOP-8_3x3mm_P0.65mm": TI_DGK,
    "easyeda2kicad:MSOP-8_L3.0-W3.0-P0.65-LS5.0-BL": TI_DGK,
    "Package_TO_SOT_SMD:SOT-563": TI_DRL,
    "Package_TO_SOT_SMD:TDSON-8-1": TI_Q5B,
    "easyeda2kicad:SENSOR-SMD_VEML6031X00": VEML6031,
    "VEML7700-TT:XDCR_VEML7700-TT": VEML7700,
    "SolarPanelBoards:KXOB101K08F-TR": SM101,
    "Solar_Cell_Library:SM261K10TF": SM261,
    "Solar_Cell_Library:SM531K10T": SM531,
    "SolarPanelBoards:Test Pad": TEST_PAD,
    "Resistor_THT:R_Axial_DIN0204_L3.6mm_D1.6mm_P5.08mm_Horizontal": BURN_WIRE,
}
NOT_PARTS = ("LOGO", "dfsdf")
