#!/usr/bin/env python3
"""Compositional stroke system + fusion grammar prototype
(docs/design/stroke-system.md; conlang-r5y).

Letters are stroke PROGRAMS (connected polyline/arc paths with round
joins) instead of placed marks. Words fuse by frequency band:
band 0 = side-by-side, band 1 = touch-joined, band 2 = shared-stroke
merge + redundancy drops. All ink is emitted as <line> segments (arcs
chorded) so the existing raster machinery measures it unchanged.

Usage:
  python3 tools/strokes.py specimen [--out PATH]
  python3 tools/strokes.py word ROMAN [BAND]
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from phonology import Inventory, Syllable  # noqa: E402

W = 5.4      # stroke width (>= 2x half cell pitch at 12px so single strokes never phase-vanish)


def _seg(x1, y1, x2, y2, w=W):
    return (f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" '
            f'y2="{y2:.2f}" stroke="currentColor" stroke-width="{w}" '
            f'stroke-linecap="round"/>')


def arc_pts(cx, cy, r, a0, a1, n=10):
    return [(cx + r * math.cos(math.radians(a0 + (a1 - a0) * i / n)),
             cy + r * math.sin(math.radians(a0 + (a1 - a0) * i / n)))
            for i in range(n + 1)]


def poly(pts, w=W):
    return [_seg(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], w)
            for i in range(len(pts) - 1)]


# Letter programs on a 60x60 design box (0..60). Each: list of point-
# paths (each path = connected polyline; arcs pre-chorded), plus
# anchors: entry (left), exit (right), spine (for vowel branches:
# p0->p1 line along which height fractions land).
# Identities = the v0.2 anti-iconic code, re-founded as strokes.
def LETTERS():
    L = {}
    # p: vertical
    L["p"] = dict(paths=[[(30, 6), (30, 54)]],
                  spine=((30, 6), (30, 54)), exit=(30, 30), entry=(30, 30))
    # j: vertical crossed (+)
    L["j"] = dict(paths=[[(30, 6), (30, 54)], [(8, 30), (52, 30)]],
                  spine=((30, 6), (30, 54)), exit=(52, 30), entry=(8, 30))
    # n: wide double vertical
    L["n"] = dict(paths=[[(18, 6), (18, 54)], [(42, 6), (42, 54)]],
                  spine=((42, 6), (42, 54)), exit=(42, 30), entry=(18, 30))
    # t: crossed diagonals (X)
    L["t"] = dict(paths=[[(8, 54), (52, 6)], [(8, 6), (52, 54)]],
                  spine=((8, 54), (52, 6)), exit=(52, 30), entry=(8, 30))
    # s: doubled rising diagonal
    L["s"] = dict(paths=[[(4, 54), (40, 6)], [(20, 54), (56, 6)]],
                  spine=((20, 54), (56, 6)), exit=(56, 30), entry=(4, 30))
    # l: corner
    L["l"] = dict(paths=[[(12, 6), (48, 6)], [(12, 6), (12, 54)]],
                  spine=((12, 6), (12, 54)), exit=(48, 6), entry=(12, 30))
    # k: nested corners
    L["k"] = dict(paths=[[(10, 6), (50, 6)], [(10, 6), (10, 54)],
                         [(26, 24), (50, 24)], [(26, 24), (26, 54)]],
                  spine=((10, 6), (10, 54)), exit=(50, 24), entry=(10, 30))
    # c (ts): ring
    L["c"] = dict(paths=[arc_pts(30, 30, 22, -90, 270)],
                  spine=((30, 8), (30, 52)), exit=(52, 30), entry=(8, 30))
    # m: ring crossed by rising diagonal
    L["m"] = dict(paths=[arc_pts(30, 30, 22, -90, 270),
                         [(12, 48), (48, 12)]],
                  spine=((12, 48), (48, 12)), exit=(48, 12), entry=(12, 48))
    # w: ring with attached top bar
    L["w"] = dict(paths=[arc_pts(30, 32, 20, -90, 270),
                         [(6, 12), (54, 12)]],
                  spine=((30, 12), (30, 52)), exit=(54, 12), entry=(6, 12))
    # h: doubled short horizontal (=)
    L["h"] = dict(paths=[[(12, 24), (48, 24)], [(12, 38), (48, 38)]],
                  spine=((12, 24), (48, 24)), exit=(48, 31), entry=(12, 31))
    return L


VOWEL_BRANCH = {"i": (0.2, -1), "u": (0.2, +1), "e": (0.5, -1),
                "o": (0.5, +1), "a": (0.8, 0)}   # (spine frac, side)


def letter_parts(roman, vowel=None, dx=0.0, dy=0.0):
    spec = LETTERS()[roman]
    parts = []
    for path in spec["paths"]:
        parts += poly([(x + dx, y + dy) for x, y in path])
    if vowel:
        f, side = VOWEL_BRANCH[vowel]
        (x0, y0), (x1, y1) = spec["spine"]
        bx, by = x0 + (x1 - x0) * f + dx, y0 + (y1 - y0) * f + dy
        # branch perpendicular-ish to the spine, length 12
        ang = math.atan2(y1 - y0, x1 - x0) + math.pi / 2
        ex, ey = math.cos(ang) * 12, math.sin(ang) * 12
        if side in (-1, 0):
            parts.append(_seg(bx, by, bx - ex, by - ey))
        if side in (+1, 0):
            parts.append(_seg(bx, by, bx + ex, by + ey))
    return parts


def word_parts(sylls, band=1, dy=0.0):
    """Render a word's onset+vowel skeleton at a fusion band.
    band 0: 14u gaps. band 1: letters touch (exit meets entry).
    band 2: touch + shared-stroke merge for compatible verticals +
    drop the second letter's entry stroke when merged."""
    parts = []
    x = 0.0
    prev_exit = None
    Ls = LETTERS()
    for i, syl in enumerate(sylls):
        spec = Ls[syl.onset]
        if band == 0 or prev_exit is None:
            ox = x
        else:
            # translate so entry anchor touches previous exit
            ox = prev_exit[0] - spec["entry"][0] + (0 if band >= 1 else 14)
        paths = spec["paths"]
        merged = False
        if band == 2 and prev_exit is not None and i > 0:
            # shared-stroke: if first path is a vertical and previous
            # letter ended with a vertical at the junction, drop it
            p0 = paths[0]
            if len(p0) == 2 and abs(p0[0][0] - p0[1][0]) < 0.1:
                paths = paths[1:] or paths
                merged = True
        for path in paths:
            parts += poly([(px + ox, py + dy) for px, py in path])
        if syl.vowel:
            parts += letter_parts_vowel_only(syl.onset, syl.vowel, ox, dy)
        ex, ey = spec["exit"]
        prev_exit = (ox + ex + (0 if band >= 1 else 14), ey)
        x = ox + 62
    return parts, x


def letter_parts_vowel_only(roman, vowel, dx, dy):
    spec = LETTERS()[roman]
    f, side = VOWEL_BRANCH[vowel]
    (x0, y0), (x1, y1) = spec["spine"]
    bx, by = x0 + (x1 - x0) * f + dx, y0 + (y1 - y0) * f + dy
    ang = math.atan2(y1 - y0, x1 - x0) + math.pi / 2
    ex, ey = math.cos(ang) * 12, math.sin(ang) * 12
    out = []
    if side in (-1, 0):
        out.append(_seg(bx, by, bx - ex, by - ey))
    if side in (+1, 0):
        out.append(_seg(bx, by, bx + ex, by + ey))
    return out


def svg(parts, w, h):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
            f'width="{w}" height="{h}" style="color:#1a1a1a">'
            + "".join(parts) + "</svg>")


def specimen():
    inv = Inventory()
    parts = []
    y = 12
    # letter table
    x = 10
    for o in list("cptkmnslwj") + ["h"]:
        parts += letter_parts(o, dx=x, dy=y)
        parts.append(f'<text x="{x+22}" y="{y+78}" font-size="11" '
                     f'fill="currentColor" font-family="monospace">{o}</text>')
        x += 78
    y += 100
    # one letter, five vowels as branches
    x = 10
    for v in "iueoa":
        parts += letter_parts("t", vowel=v, dx=x, dy=y)
        parts.append(f'<text x="{x+22}" y="{y+78}" font-size="11" '
                     f'fill="currentColor" font-family="monospace">t+{v}</text>')
        x += 78
    y += 100
    # seed words at three bands
    S = Syllable
    words = [("sala", [S("s", "a", ""), S("l", "a", "")]),
             ("weto", [S("w", "e", ""), S("t", "o", "")]),
             ("lutan", [S("l", "u", ""), S("t", "a", "n")]),
             ("wajone", [S("w", "a", ""), S("j", "o", ""), S("n", "e", "")])]
    for band in (0, 1, 2):
        x = 10
        for name, sylls in words:
            wp, ww = word_parts(sylls, band=band, dy=y)
            parts += [p for p in wp]
            parts = _shift_last(parts, len(wp), x)
            parts.append(f'<text x="{x}" y="{y+80}" font-size="11" '
                         f'fill="currentColor" font-family="monospace">'
                         f'{name}</text>')
            x += ww + 40
        parts.append(f'<text x="{x}" y="{y+40}" font-size="12" '
                     f'fill="currentColor" font-family="monospace">'
                     f'band {band}</text>')
        y += 105
    return svg(parts, 1250, y + 20)


def _shift_last(parts, n, dx):
    """Shift the last n <line> parts right by dx."""
    import re
    out = parts[:-n]
    for p in parts[-n:]:
        def rep(m):
            k, v = m.group(1), float(m.group(2))
            return f'{k}="{v + dx:.2f}"' if k in ("x1", "x2") else m.group(0)
        out.append(re.sub(r'(x1|x2)="([-\d.]+)"', rep, p))
    return out


def main(argv=None):
    args = sys.argv[1:] if argv is None else argv
    if not args:
        print(__doc__, file=sys.stderr)
        return 2
    if args[0] == "specimen":
        out = args[args.index("--out") + 1] if "--out" in args else None
        s = specimen()
        if out:
            Path(out).write_text(s)
            print(f"written: {out}")
        else:
            print(s)
    elif args[0] == "word":
        inv = Inventory()
        band = int(args[2]) if len(args) > 2 else 1
        sylls = inv.parse_word(args[1], mode="lexical")
        wp, ww = word_parts(sylls, band=band)
        print(svg(wp, ww + 10, 70))
    else:
        print(__doc__, file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
