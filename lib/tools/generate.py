"""Regenerate lib/PROVES.pretty and lib/PROVES.kicad_sym from lib/parts.py.

Usage: python3 lib/tools/generate.py [--out DIR]

The raw files go through `kicad-cli fp upgrade` and `kicad-cli sym upgrade`, so the committed
library is exactly what KiCad 10 itself would save: opening and saving a part in KiCad makes no diff.
UUIDs are derived from part names, so the output is byte-for-byte stable and check.py can prove the
committed library matches the source.
"""

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

LIB_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(LIB_DIR))
sys.path.insert(0, str(LIB_DIR / "tools"))

from kicad import footprint_text, symbol_lib_text  # noqa: E402

import parts  # noqa: E402

KICAD_CLI = shutil.which("kicad-cli") or "kicad-cli"


def _cli(*args):
    subprocess.run([KICAD_CLI, *args], check=True, capture_output=True)


def write(out: Path):
    pretty = out / f"{parts.LIB}.pretty"
    sym = out / f"{parts.LIB}.kicad_sym"
    with tempfile.TemporaryDirectory() as tmp:
        raw = Path(tmp) / "raw.pretty"
        raw.mkdir()
        for f in parts.FOOTPRINTS:
            (raw / f"{f.name}.kicad_mod").write_text(footprint_text(f))
        raw_sym = Path(tmp) / "raw.kicad_sym"
        raw_sym.write_text(symbol_lib_text(parts.SYMBOLS))
        if pretty.exists():
            shutil.rmtree(pretty)
        sym.unlink(missing_ok=True)
        _cli("fp", "upgrade", "--force", "-o", str(pretty), str(raw))
        _cli("sym", "upgrade", "--force", "-o", str(sym), str(raw_sym))
    return len(parts.FOOTPRINTS), len(parts.SYMBOLS)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=LIB_DIR)
    n_fp, n_sym = write(ap.parse_args().out)
    print(f"wrote {n_fp} footprints and {n_sym} symbols")
