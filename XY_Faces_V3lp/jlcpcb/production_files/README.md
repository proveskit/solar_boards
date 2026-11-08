# XY_Faces_V3lp JLCPCB order files

These files match JLCPCB order W2026110214273992 (25 boards, placed 2026-11-02).

- `BOM-XY_Faces_V3lp.csv` and `CPL-XY_Faces_V3lp.csv` list the parts JLCPCB assembled.
- U4 is a TCA4307DGKR (C880333). It is a pin-for-pin replacement for the TCA4311A and adds stuck-bus recovery.
- CN1 (DF11-6DP-2DSA(08), C506668) is not assembled by JLCPCB. It is excluded in `jlcpcb/project.db` and is fitted by hand.
- The solar cells (SC1 to SC6) are not assembled by JLCPCB.

The CPL rotations are KiCad's own, except for four parts that JLCPCB places at a different angle:

| Ref | KiCad | JLCPCB |
| --- | ----- | ------ |
| U2  | 0     | 180    |
| U3  | 0     | 270    |
| U5  | 0     | 180    |
| U6  | 180   | 0      |

If you export a new CPL with a plugin, apply these angles again before you upload it.
