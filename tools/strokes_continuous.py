#!/usr/bin/env python3
"""Continuous-join vowel topology for the stroke engine (conlang-h05).

The conflict on record (workshop-shadow-log, vowel-topology-r1):
Edward prefers T0 ticks ("one continuous character") but T0's vowel
pairs measure 0.000 — identical — at reading raster. T1/T2 fix the
metric by STEPPING the next letter (teleport by the vowel's offset),
which he read as "all over the place". His reconciling hypothesis:
the step is the problem, not the topology.

Scheme C makes the join continuous: the vowel IS the connector
stroke between letters —

  height   -> the slope of the connector (next letter rides high /
              level / low relative to baseline; the connector is a
              real drawn stroke from exit anchor to entry anchor,
              so the ink never breaks)
  backness -> the connector's length (front tucks the next letter
              in close, back extends the reach)

Word-final vowels use THE SAME rule: the connector simply has no
next letter to arrive at, so it becomes a terminal tail with the
same slope/length code. One rule, both positions — the T-scheme's
hybrid tick asymmetry disappears.

Usage:
  python3 tools/strokes_continuous.py measure     (C vs T0/T1/T2)
  python3 tools/strokes_continuous.py sheet [--out PATH]
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from strokes import LETTERS, VOWEL_BRANCH, W, poly, svg  # noqa: E402
from strokes_topology import (  # noqa: E402
    SAMPLE, Syl, measure as measure_T, pmin, word as word_T)

# height fraction (VOWEL_BRANCH) -> ride of the NEXT letter, u.
# Softer than T1's +-14: Edward read the 14u step as misalignment.
RIDE = {0.2: -11.0, 0.5: 0.0, 0.8: +11.0}
# backness side -> connector length, u (front tucks, back reaches)
REACH = {-1: 5.0, 0: 11.0, +1: 17.0}
# terminal tail: same code, no next letter to arrive at
TAIL_ANG = {0.2: -45.0, 0.5: 0.0, 0.8: +45.0}     # degrees, by height


def word(sylls, dx=0.0, dy=0.0):
    """Render a word under scheme C. Letters sit at baseline+ride,
    every junction is a drawn connector stroke: ink is continuous
    from first letter to terminal tail. Returns (parts, width)."""
    Ls = LETTERS()
    parts = []
    ox = dx
    prev = None                      # (exit_pt, vowel) of previous letter
    for syl in sylls:
        spec = Ls[syl.onset]
        f, side = VOWEL_BRANCH[syl.vowel]
        if prev is None:
            oy = dy
        else:
            (px, py), pv = prev
            pf, pside = VOWEL_BRANCH[pv]
            oy = dy + RIDE[pf]
            ox = px + REACH[pside] - spec["entry"][0]
            ax, ay = ox + spec["entry"][0], oy + spec["entry"][1]
            parts += poly([(px, py), (ax, ay)])          # the connector
        for path in spec["paths"]:
            parts += poly([(x + ox, y + oy) for x, y in path])
        ex, ey = spec["exit"]
        prev = ((ox + ex, oy + ey), syl.vowel)
        ox += 62
    # terminal tail: the last vowel's connector, arriving nowhere.
    # Slope = height (as medially); backness = reach, shown as length
    # PLUS an end-hook (front curls up, back curls down) — pure length
    # is subset-ink and can raster-vanish, a hook cannot.
    (px, py), pv = prev
    pf, pside = VOWEL_BRANCH[pv]
    ang = math.radians(TAIL_ANG[pf])
    L = REACH[pside] + 6
    tx, ty = px + L * math.cos(ang), py + L * math.sin(ang)
    tail = [(px, py), (tx, ty)]
    if pside:
        # hook set 70deg off the tail direction (front curls against
        # travel, back curls with it) and sized to exceed the
        # reading-raster cell pitch, so it cannot phase-vanish the way
        # a tick can — and cannot go near-collinear with its own tail
        h = ang + math.radians(70.0) * pside
        tail.append((tx + 11.0 * math.cos(h), ty + 11.0 * math.sin(h)))
    parts += poly(tail)
    return parts, (px + L + 4) - dx


def word_bounds(sylls):
    """(width, min_y_offset, max_y_offset) of a C-scheme word relative
    to its baseline — rides and tails move ink outside the 0..60 box."""
    parts, w = word(sylls)
    ys = []
    for p in parts:
        import re
        ys += [float(v) for v in re.findall(r'y[12]="([-\d.]+)"', p)]
    return w, min(ys) - W / 2, max(ys) + W / 2


def measure():
    """C on the same pair families/windows as strokes_topology, so the
    row is directly comparable with the T0/T1/T2 table."""
    import itertools
    VOWELS = "aeiou"
    ONSETS = ["s", "l", "t", "m", "p", "k", "n", "w", "c", "j"]
    vow, ons = [], []
    for v1, v2 in itertools.combinations(VOWELS, 2):
        for pos in (0, 1):
            base = [Syl("s", "a"), Syl("l", "a")]
            other = [Syl("s", "a"), Syl("l", "a")]
            base[pos] = Syl(base[pos].onset, v1)
            other[pos] = Syl(other[pos].onset, v2)
            vow.append(pmin(word(base)[0], word(other)[0], 22))
    for o1, o2 in itertools.combinations(ONSETS, 2):
        for pos in (0, 1):
            base = [Syl("s", "a"), Syl("l", "a")]
            other = [Syl("s", "a"), Syl("l", "a")]
            base[pos] = Syl(o1, base[pos].vowel)
            other[pos] = Syl(o2, other[pos].vowel)
            ons.append(pmin(word(base)[0], word(other)[0], 22))
    from strokes_topology import median
    vow.sort()
    ons.sort()
    return {"vowel_min": round(vow[0], 4),
            "vowel_median": round(median(vow), 4),
            "onset_min": round(ons[0], 4),
            "onset_median": round(median(ons), 4),
            "ratio_median": round(median(vow) / median(ons), 3)}


def sheet():
    parts, y = [], 46
    rows = [("T0", "ticks (Edward's r1 pick; vowel floor 0.000)",
             lambda s, x, yy: word_T(s, "T0", dx=x, dy=yy)),
            ("C", "continuous join: vowel = connector slope + reach",
             lambda s, x, yy: word(s, dx=x, dy=yy))]
    for tag, desc, fn in rows:
        x = 20
        for name, sylls in SAMPLE:
            pw, wid = fn(sylls, x, y)
            parts += pw
            parts.append(f'<text x="{x}" y="{y + 92}" font-size="11" '
                         f'fill="#999" font-family="monospace">{name}</text>')
            x += wid + 34
        parts.append(f'<text x="20" y="{y - 22}" font-size="13" '
                     f'fill="#555" font-family="monospace">{tag}: {desc}'
                     f'</text>')
        small, sx = [], 0.0
        for _, sylls in SAMPLE * 2:
            pw, wid = fn(sylls, sx, 0.0)
            small += pw
            sx += wid + 34
        parts.append(f'<g transform="translate(20 {y + 106}) scale(0.42)">'
                     + "".join(small) + "</g>")
        y += 230
    return svg([f'<rect width="1980" height="{y}" fill="white"/>'] + parts,
               1980, y)


def main(argv=None):
    args = sys.argv[1:] if argv is None else argv
    if args and args[0] == "measure":
        res = measure_T()
        res["C"] = measure()
        print(f"{'scheme':<8}{'vowel min':>11}{'vowel med':>11}"
              f"{'onset min':>11}{'onset med':>11}{'ratio':>8}")
        for s, r in res.items():
            print(f"{s:<8}{r['vowel_min']:>11.4f}{r['vowel_median']:>11.4f}"
                  f"{r['onset_min']:>11.4f}{r['onset_median']:>11.4f}"
                  f"{r['ratio_median']:>8.3f}")
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
