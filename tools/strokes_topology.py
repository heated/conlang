#!/usr/bin/env python3
"""Vowels as JOIN TOPOLOGY — testing the stroke-system's parked lead.

stroke-system.md §4.2 flagged fusion's weak cell: vowel pairs at band
1/2 measured 0.057 (sala/sela) against 0.534 for a consonant change,
because a vowel is a 12u branch tick — small ink. The proposed fix,
never built: **let the vowel modulate the join between letters**, so a
vowel change reshapes the whole word figure instead of moving a tick.
Topology survives sizes that ticks do not.

Three schemes, measured against the tick control:

  T0  ticks (control)        vowel = branch tick on the spine
  T1  join height           vowel HEIGHT sets the y-offset at which the
                            next letter attaches (high/mid/low);
                            BACKNESS sets horizontal tuck (front =
                            overlap deeper, back = extend) — the tick
                            is dropped entirely except word-finally
  T2  join height + tick    T1, plus a reduced tick kept everywhere
                            (belt and braces: topology carries the
                            contrast at small sizes, the tick
                            disambiguates at large ones)

Word-final vowels have no following letter, so every scheme keeps a
terminal tick there — a real asymmetry the report names rather than
hides.

Measurement: antialiased-free occupancy rasters via tools/script.py
(same family as every other floor in the repo), phase-minimized over
9 sub-cell alignments, on minimal-pair words that differ in ONE vowel
vs ONE onset. Reports the vowel/onset distance ratio — the number the
lead is about.

Usage:
  python3 tools/strokes_topology.py measure
  python3 tools/strokes_topology.py sheet [--out PATH]
"""

from __future__ import annotations

import itertools
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from script import rasterize, raster_distance  # noqa: E402
from strokes import LETTERS, VOWEL_BRANCH, W, _seg, poly, svg  # noqa: E402

# vowel -> (spine fraction = height, side = backness) is reused from
# strokes.py; topology maps the same two features onto the join:
#   height  -> y offset of the next letter's attachment
#   backness-> horizontal tuck (front pulls in, back pushes out)
JOIN_DY = {0.2: -14.0, 0.5: 0.0, 0.8: +14.0}      # by height fraction
JOIN_DX = {-1: -8.0, 0: 0.0, +1: +8.0}            # by backness side


def _vowel_tick(spec, vowel, dx, dy, length=12.0, w=W):
    f, side = VOWEL_BRANCH[vowel]
    (x0, y0), (x1, y1) = spec["spine"]
    bx, by = x0 + (x1 - x0) * f + dx, y0 + (y1 - y0) * f + dy
    ang = math.atan2(y1 - y0, x1 - x0) + math.pi / 2
    ex, ey = math.cos(ang) * length, math.sin(ang) * length
    out = []
    if side in (-1, 0):
        out.append(_seg(bx, by, bx - ex, by - ey, w=w))
    if side in (+1, 0):
        out.append(_seg(bx, by, bx + ex, by + ey, w=w))
    return out


def word(sylls, scheme="T0", dx=0.0, dy=0.0):
    """Render a word's onset+vowel skeleton under a vowel scheme.
    Letters always touch (band 1); the scheme decides how the vowel is
    carried. Returns (parts, width)."""
    Ls = LETTERS()
    parts = []
    ox, oy = dx, dy
    prev = None                      # (exit_x, exit_y, vowel) of last
    for i, syl in enumerate(sylls):
        spec = Ls[syl.onset]
        if prev is not None:
            px, py, pv = prev
            ox = px - spec["entry"][0]
            oy = dy
            if scheme in ("T1", "T2"):
                f, side = VOWEL_BRANCH[pv]
                oy = dy + JOIN_DY[f]
                ox += JOIN_DX[side]
        for path in spec["paths"]:
            parts += poly([(x + ox, y + oy) for x, y in path])
        last = i == len(sylls) - 1
        if syl.vowel:
            if scheme == "T0" or last:
                parts += _vowel_tick(spec, syl.vowel, ox, oy)
            elif scheme == "T2":
                parts += _vowel_tick(spec, syl.vowel, ox, oy, length=7.0)
            # T1 non-final: the vowel is entirely in the join
        ex, ey = spec["exit"]
        prev = (ox + ex, oy + ey, syl.vowel)
    return parts, ox + 62 - dx


# --- measurement ---------------------------------------------------------

class Syl:
    """Minimal syllable stand-in (avoids the Inventory dependency)."""
    def __init__(self, onset, vowel, coda=""):
        self.onset, self.vowel, self.coda = onset, vowel, coda


PHASES = [(px, py) for px in (0, 1.6, 3.2) for py in (0, 1.6, 3.2)]
WIN = (-30, -34, 160, 100)


def pmin(a, b, n):
    return min(raster_distance(
        rasterize(a, WIN[0] + px, WIN[1] + py, WIN[2] + px, WIN[3] + py, n),
        rasterize(b, WIN[0] + px, WIN[1] + py, WIN[2] + px, WIN[3] + py, n))
        for px, py in PHASES)


VOWELS = "aeiou"
ONSETS = ["s", "l", "t", "m", "p", "k", "n", "w", "c", "j"]


def median(sorted_vals):
    """Conventional median (mean of the middle two for even n) — the
    first published tables used the upper-middle value, which inflated
    even-n medians (2026-08-22 review finding)."""
    n = len(sorted_vals)
    return (sorted_vals[(n - 1) // 2] + sorted_vals[n // 2]) / 2


def measure(n=22):
    """For each scheme: worst/median distance over one-vowel-different
    pairs, and over one-onset-different pairs, plus the ratio."""
    out = {}
    for scheme in ("T0", "T1", "T2"):
        vow, ons = [], []
        # disyllables s?-l? : vary vowel 1, vowel 2, onset 1, onset 2
        for v1, v2 in itertools.combinations(VOWELS, 2):
            for pos in (0, 1):
                base = [Syl("s", "a"), Syl("l", "a")]
                other = [Syl("s", "a"), Syl("l", "a")]
                base[pos] = Syl(base[pos].onset, v1)
                other[pos] = Syl(other[pos].onset, v2)
                vow.append(pmin(word(base, scheme)[0],
                                word(other, scheme)[0], n))
        for o1, o2 in itertools.combinations(ONSETS, 2):
            for pos in (0, 1):
                base = [Syl("s", "a"), Syl("l", "a")]
                other = [Syl("s", "a"), Syl("l", "a")]
                base[pos] = Syl(o1, base[pos].vowel)
                other[pos] = Syl(o2, other[pos].vowel)
                ons.append(pmin(word(base, scheme)[0],
                                word(other, scheme)[0], n))
        vow.sort()
        ons.sort()
        out[scheme] = {
            "vowel_min": round(vow[0], 4),
            "vowel_median": round(median(vow), 4),
            "onset_min": round(ons[0], 4),
            "onset_median": round(median(ons), 4),
            "ratio_median": round(median(vow) / median(ons), 3),
            "n_vowel_pairs": len(vow), "n_onset_pairs": len(ons),
        }
    return out


SAMPLE = [("sala", [Syl("s", "a"), Syl("l", "a")]),
          ("sela", [Syl("s", "e"), Syl("l", "a")]),
          ("sila", [Syl("s", "i"), Syl("l", "a")]),
          ("sola", [Syl("s", "o"), Syl("l", "a")]),
          ("sula", [Syl("s", "u"), Syl("l", "a")]),
          ("sata", [Syl("s", "a"), Syl("t", "a")]),
          ("weto", [Syl("w", "e"), Syl("t", "o")]),
          ("menokis", [Syl("m", "e"), Syl("n", "o"), Syl("k", "i")])]


def sheet():
    parts, y = [], 40
    for scheme in ("T0", "T1", "T2"):
        x = 20
        for name, sylls in SAMPLE:
            pw, wid = word(sylls, scheme, dx=x, dy=y)
            parts += pw
            parts.append(f'<text x="{x}" y="{y + 92}" font-size="11" '
                         f'fill="#888" font-family="monospace">{name}</text>')
            x += wid + 34
        parts.append(f'<text x="20" y="{y - 18}" font-size="13" '
                     f'fill="#555" font-family="monospace">{scheme}'
                     f'</text>')
        # reading-size row
        small, sx = [], 0
        for name, sylls in SAMPLE * 2:
            pw, wid = word(sylls, scheme, dx=sx, dy=0)
            small += pw
            sx += wid + 34
        parts.append(f'<g transform="translate(20 {y + 108}) scale(0.42)">'
                     + "".join(small) + "</g>")
        y += 230
    return svg(parts, 1500, y)


def main(argv=None):
    args = sys.argv[1:] if argv is None else argv
    if args and args[0] == "measure":
        res = measure()
        print(f"{'scheme':<8}{'vowel min':>11}{'vowel med':>11}"
              f"{'onset min':>11}{'onset med':>11}{'ratio':>8}")
        for s, r in res.items():
            print(f"{s:<8}{r['vowel_min']:>11.4f}{r['vowel_median']:>11.4f}"
                  f"{r['onset_min']:>11.4f}{r['onset_median']:>11.4f}"
                  f"{r['ratio_median']:>8.3f}")
        print(f"\npairs per cell: {res['T0']['n_vowel_pairs']} vowel, "
              f"{res['T0']['n_onset_pairs']} onset; "
              f"phase-min over {len(PHASES)} alignments at n=22")
        return 0
    if args and args[0] == "sheet":
        out = args[args.index("--out") + 1] if "--out" in args else None
        s = sheet()
        if out:
            Path(out).write_text(s)
            print(f"written: {out}")
        else:
            print(s)
        return 0
    print(__doc__, file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
