# PROVES library format spec

This spec defines every symbol and footprint in the `PROVES` library. `tools/model.py` and `tools/kicad.py` apply the derived rules, so a part entry in `parts.py` holds only datasheet facts. `tools/check.py` enforces the rule IDs below on the committed files. Units are millimetres.

## Sources

| ID | Rule |
|---|---|
| F3 | Every footprint names its source in `descr` as `Source: <document>, p.<page>, <figure>`, and its `Datasheet` property is a URL. |
| — | Copper comes from the land pattern the part's manufacturer publishes. If the ordered manufacturer publishes none, use another manufacturer's published land for the same package and say so in the source. |
| — | Chip resistors, chip capacitors and chip LEDs use the IPC-7351B nominal (level B) Z, G and X equations, fed the body length, width and terminal tolerances from the ordered parts' datasheets. Several makers for one size use the envelope of their tolerances. Fabrication tolerance is 0.1 and placement 0.05. Results round to 0.02 below 1608 and 0.05 from 1608 up. |
| — | A dimension read from drawing scale, symmetry, or a sibling part is stated as such in the footprint notes. |
| — | A house part (no vendor drawing exists) cites `PROVES house part` and keeps the flown geometry. |
| — | Nothing is copied from KiCad stock, easyeda2kicad, SnapEDA, or vendor CAD downloads. They may be read to cross-check a result. |

## Footprints

| ID | Rule |
|---|---|
| F1 | The file name equals the footprint name. Names follow `<Maker>_<PackageCode>_<Package>_<Body>_<Pitch>` for vendor packages and `<Type>_<Size>` for generic chips. |
| F2 | Files are KiCad 10 format (`version 20260206`) exactly as `kicad-cli fp upgrade` writes them. |
| F4 | No 3D model references. Models are a later addition with their own source rule. |
| F5 | `Reference` sits on `F.SilkS` above the courtyard, hidden, so boards carry no refdes on silk. `Value` sits on `F.Fab` below it. A `${REFERENCE}` text sits on `F.Fab` at the body centre. |
| F6 | Every pad has a number. Pad `1` exists. Mechanical pads that carry no signal are numbered `MP`. |
| F7 | An SMD footprint's origin is the centre of its pad extent. A THT footprint's origin is pad 1, the pad-extent centre, or the body centre. |
| F8 | SMD pads use `F.Cu F.Mask F.Paste`. A part with a vendor stencil drawing uses `F.Cu F.Mask` pads and `F.Paste` polygons copied from the stencil. THT pads use `*.Cu *.Mask`. |
| F9 | A THT pad is drill + 0.6 (0.3 annular ring) unless the vendor gives the pad. The drill is the midpoint of the vendor's hole tolerance. The minimum annular ring is 0.15. |
| — | SMD pads are `roundrect`. The corner radius is the vendor's (TI `R0.05`), else 25 % of the short side, capped at 0.25. THT pin 1 is a rounded square. Other THT pads are round. |
| F10 | One `F.CrtYd` rectangle, line 0.05, clears pad copper and the body by 0.25, rounded outward to 0.01. |
| F11 | `F.Fab` carries the body outline from the datasheet's nominal size, line 0.1. Polarized parts cut the corner nearest pad 1 at 45° by 25 % of the short side, at most 1.0. Fasteners draw the head as a circle. |
| F12 | `F.SilkS` traces the body outline, line 0.12, clipped to stay 0.2 from all pad copper. Polarized parts add a 0.3 dot beside pad 1, clear of copper. |
| — | Orientation follows IPC-7351 zero rotation: IC pin 1 top-left, two-terminal pad 1 on the left. Connectors keep the vendor's top view, rotated in 90° steps only. Never mirror a vendor view. |
| — | Diodes and LEDs number the cathode pad `1` whatever the vendor numbers it, and state the mapping in the notes. |

## Symbols

| ID | Rule |
|---|---|
| S1 | One library file, `PROVES.kicad_sym`, KiCad 10 format (`version 20251024`) exactly as `kicad-cli sym upgrade` writes it. |
| S2 | Every symbol has `Reference`, `Value`, `Footprint`, `Datasheet`, `Description`, and `ki_keywords`. `Description` is not empty. |
| S3 | Pin numbers are unique. Pins sit on the 1.27 grid. Box symbols place pins on the 2.54 grid with 2.54 pin length and 1.27 text. |
| S4 | An atomic part (a fixed MPN) fills `Footprint` with `PROVES:<footprint>`, `Datasheet` with the vendor URL, and adds `MPN` and `Manufacturer`. `LCSC Part` is added when the part has one. |
| S5 | An atomic part's pin numbers equal its footprint's pad numbers, excluding `MP`. |
| S6 | A generic part (R, C, LED, test point, mounting hole, burn wire) leaves `Footprint` empty, sets `ki_fp_filters`, and its pin numbers equal the pads of every footprint the filters match. |
| — | Box symbols are functional, per Greenberg: inputs left, outputs right, power on top, ground on the bottom. Connector symbols list pins in physical rows. A MOSFET is drawn as a MOSFET, with duplicate drain and source pins stacked and hidden. |
| — | Passive two-terminal parts use IEEE 315 graphics with pin numbers and names hidden. |
| — | Pin electrical types come from the datasheet pin table. Open-drain outputs are `open_collector`. Supply pins are `power_in`. |

## Library

| ID | Rule |
|---|---|
| L1 | `python3 lib/tools/generate.py` reproduces the committed `PROVES.pretty` and `PROVES.kicad_sym` byte for byte. Hand edits fail the check. |
| L2 | `ipc_chip` reproduces KiCad's stock `C_0402` and `C_0603` pads when given the same IPC-SM-782 bodies. |
