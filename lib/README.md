# PROVES parts library

`lib/` is the PROVES-owned KiCad 10 library for the solar boards: 23 footprints and 20 symbols, each built from its manufacturer's datasheet. It replaces the stock, easyeda2kicad, and copied project libraries the boards use today. It will move to its own repository and come back as a submodule.

| Path | What it is |
|---|---|
| `SPEC.md` | The format rules every part follows. |
| `parts.py` | One entry per part: datasheet numbers and the page and figure they came from. |
| `PROVES.pretty/`, `PROVES.kicad_sym` | The generated library. Do not edit by hand. |
| `tools/generate.py` | Writes the library from `parts.py` through `kicad-cli`. |
| `tools/check.py` | Enforces `SPEC.md` and proves the committed files match a fresh generation. |
| `tools/compare_asordered.py` | Compares each footprint with the one it replaces on the six live boards. |
| `reports/asordered-pad-deltas.md` | That comparison, with a reason for every changed pad. |

## Add or change a part

You need Python 3.10 or later and KiCad 10 (`kicad-cli` on `PATH`).

1. Find the vendor's land pattern, pin table, and package drawing. Note the document revision, page, and figure.
2. Add a `Source`, a footprint, and a symbol to `parts.py`. Use the builders in `tools/patterns.py` where one fits.
3. Run `python3 lib/tools/generate.py`.
4. Run `python3 lib/tools/check.py`. It must report 0 violations.
5. If the part replaces one on a board, add it to `REPLACES` in `parts.py` and its reason to `REASONS` in `tools/compare_asordered.py`. Then run `python3 lib/tools/compare_asordered.py --md lib/reports/asordered-pad-deltas.md --json lib/reports/asordered-pad-deltas.json`.

## Use it in a board

Add the library to the board's tables with a path relative to the project:

```
(lib (name "PROVES")(type "KiCad")(uri "${KIPRJMOD}/../lib/PROVES.pretty")(options "")(descr ""))
```

The boards are not switched yet. That happens board by board in later changes, because the comparison report shows footprints that move copper.
