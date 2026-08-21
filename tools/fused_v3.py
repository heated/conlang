#!/usr/bin/env python3
"""Fused word-characters v3: NARROW vertical composition (r5y round 2).

Built from Edward's round-1 verdict, not the agent's shadow pick:

  liked   U3 shared spine ("makes each character more recognizable")
          U4 vertical stack ("less like sprawling English")
  rejected width/sprawl ("wide algebra-looking clusters", "Hanzi
          unoptimized for squishing together in nice ways")
  defects alternating check dots; POS underlines colliding upward;
          huge-vs-tiny subletter contrast; decagon arcs; and
          "diagonal slashes merge at small sizes because the stroke
          weight doesn't decrease as it gets smaller"

Fixed here, all four:
  * cell is 64x100 (NARROW), not 100x100 — vertical composition means
    a word takes less line width, which is also the density lever;
  * stroke weight is PROPORTIONAL (floor 0.8u, not 4.4u) so small
    sizes thin out instead of blobbing;
  * arcs at 32 chords (no decagon);
  * check dots dropped from the character (they are a droppable
    computed layer; they were the "alternating dots" noise);
  * POS is a compact bottom radical INSIDE the cell, never a rule
    that can collide with a neighbour.

Variants (all narrow + vertical):
  N0  plain stack        two half-height rows, tight
  N1  spine stack        a vertical spine down the cell that both
                         rows attach to (U3 x U4)
  N2  seam share         rows share one horizontal stroke at the seam
                         — the "squish together" move
  N3  nested             row 2 tucks into row 1's whitespace
                         (hanzi-style tight packing, uneven split)

Usage: python3 tools/fused_v3.py sheet [--out PATH]
"""

from __future__ import annotations

import math
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from phonology import Syllable  # noqa: E402
from script import ScriptRenderer, _circle, _line  # noqa: E402

CW, CH = 64.0, 100.0          # narrow cell
INK_FLOOR = 0.8               # proportional ink; no blobbing at size


def refit(parts, s, dx, dy, floor=INK_FLOOR, arcs=True):
    """Scale/translate fragments with PROPORTIONAL stroke weight, and
    re-render circles as 32-gons so arcs stop reading as decagons."""
    out = []
    for el in ET.fromstring("<svg>" + "".join(parts) + "</svg>"):
        w = max(float(el.get("stroke-width", 0)) * s, floor)
        if el.tag == "line":
            out.append(_line(dx + float(el.get("x1")) * s,
                             dy + float(el.get("y1")) * s,
                             dx + float(el.get("x2")) * s,
                             dy + float(el.get("y2")) * s, w=w))
        elif el.tag == "circle":
            cx = dx + float(el.get("cx")) * s
            cy = dy + float(el.get("cy")) * s
            r = float(el.get("r")) * s
            if el.get("fill") == "currentColor":
                continue          # check dots dropped (Edward: noise)
            if arcs:
                n = 32
                pts = [(cx + r * math.cos(2 * math.pi * i / n),
                        cy + r * math.sin(2 * math.pi * i / n))
                       for i in range(n + 1)]
                out += [_line(pts[i][0], pts[i][1],
                              pts[i + 1][0], pts[i + 1][1], w=w)
                        for i in range(n)]
            else:
                out.append(_circle(cx, cy, r, w=w))
    return out


VOWEL = {"i": (0.20, -1), "u": (0.20, +1), "e": (0.52, -1),
         "o": (0.52, +1), "a": (0.84, 0)}


class NarrowRenderer:
    def __init__(self):
        self.r = ScriptRenderer()
        self.inv = self.r.inv

    def _row(self, syl, x0, y0, x1, y1, vowel_ink=True, tuck=0.0):
        """One syllable filling a row region, ink proportional."""
        rw, rh = x1 - x0, y1 - y0
        s = min((rw - 6) / 62, (rh - 4) / 52)
        lx = x0 + (rw - 62 * s) / 2 - 8 * s + tuck
        ly = y0 + (rh - 52 * s) / 2 - 8 * s
        parts = refit(self.r._onset(syl.onset), s, lx, ly)
        if vowel_ink:
            # vowel as a SHORT bar on the row's right edge: structural
            # (spans a real fraction of the row) rather than a dot
            f, side = VOWEL[syl.vowel]
            ty = y0 + 4 + (rh - 8) * f
            ex = x1 - 3
            w = max(4.4 * s, 1.4)
            if side in (-1, 0):
                parts.append(_line(ex - 11 * s * 1.6, ty, ex, ty, w=w))
            if side in (1, 0):
                parts.append(_line(ex, ty, ex + 5, ty, w=w))
            parts.append(_line(ex, ty - 6 * s, ex, ty + 6 * s, w=w))
        return parts

    def _pos(self, final, dx, dy):
        """POS radical: compact, inside the cell's bottom band."""
        if not final:
            return []
        y = dy + CH - 7
        x0, x1 = dx + 18, dx + CW - 18
        if final == "n":
            return [_line(x0, y, x1, y, w=4.5)]
        if final == "s":
            return [_line(x0, y - 5, x1, y - 5, w=4.5),
                    _line(x0, y, x1, y, w=4.5)]
        if final == "l":
            return [_line(x0, y, x1 - 6, y, w=4.5),
                    _line(x1 - 6, y, x1 - 6, y - 9, w=4.5)]
        return []

    def char(self, sylls, mode, dx=0.0, dy=0.0):
        assert len(sylls) == 2
        final = sylls[-1].coda
        body = dy + (CH - 14 if final else CH - 3)
        s2 = Syllable(sylls[1].onset, sylls[1].vowel, "")
        top, bot = dy + 3, body
        parts = []
        if mode == "N0":                       # plain stack
            mid = (top + bot) / 2
            parts += self._row(sylls[0], dx + 2, top, dx + CW - 2, mid - 1)
            parts += self._row(s2, dx + 2, mid + 1, dx + CW - 2, bot)
        elif mode == "N1":                     # spine stack
            sx = dx + 8
            mid = (top + bot) / 2
            parts += self._row(sylls[0], sx + 4, top, dx + CW - 2, mid - 1)
            parts += self._row(s2, sx + 4, mid + 1, dx + CW - 2, bot)
            parts.append(_line(sx, top + 1, sx, bot - 1, w=4.6))
        elif mode == "N2":                     # seam share
            mid = (top + bot) / 2
            parts += self._row(sylls[0], dx + 2, top, dx + CW - 2, mid + 3)
            parts += self._row(s2, dx + 2, mid - 3, dx + CW - 2, bot)
            parts.append(_line(dx + 6, mid, dx + CW - 6, mid, w=4.6))
        elif mode == "N3":                     # nested, uneven split
            cut = top + (bot - top) * 0.56
            parts += self._row(sylls[0], dx + 2, top, dx + CW - 2, cut)
            parts += self._row(s2, dx + 10, cut - 6, dx + CW - 2, bot,
                               tuck=-3)
        else:
            raise ValueError(mode)
        parts += self._pos(final, dx, dy)
        return parts


MODES = [("N0", "plain stack (narrow)"),
         ("N1", "spine stack (U3 x U4)"),
         ("N2", "seam share — rows squish onto one stroke"),
         ("N3", "nested, uneven split (hanzi tight packing)")]

S = Syllable
WORDS = [("sala", [S("s", "a", ""), S("l", "a", "")]),
         ("salaan", [S("s", "a", ""), S("l", "a", "n")]),
         ("taako", [S("t", "a", ""), S("k", "o", "")]),
         ("piton", [S("p", "i", ""), S("t", "o", "n")]),
         ("lewas", [S("l", "e", ""), S("w", "a", "s")]),
         ("namu", [S("n", "a", ""), S("m", "u", "")]),
         ("weto", [S("w", "e", ""), S("t", "o", "")]),
         ("kimas", [S("k", "i", ""), S("m", "a", "s")])]


def sheet():
    nr = NarrowRenderer()
    parts, y = [], 34

    def label(x, ytxt, t, size=13, fill="#555"):
        parts.append(f'<text x="{x}" y="{ytxt}" font-size="{size}" '
                     f'fill="{fill}" font-family="monospace">{t}</text>')

    for mode, desc in MODES:
        x = 16
        for name, sylls in WORDS:
            parts += nr.char(sylls, mode, dx=x, dy=y)
            label(x, y + CH + 14, name, 11, "#999")
            x += CW + 22
        label(16, y - 10, f"{mode}: {desc}")
        # reading size: one line of running text at 0.42, below the row
        small, sx = [], 0.0
        for _, sylls in (WORDS * 3)[:24]:
            small += nr.char(sylls, mode, dx=sx, dy=0.0)
            sx += CW + 16
        parts += refit(small, 0.42, 16, y + CH + 24)
        y += CH + 24 + CH * 0.42 + 46
    label(16, y, "narrow cell 64x100 | proportional ink | 32-chord "
                 "arcs | no check dots | POS inside the cell", 12, "#777")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1500 '
            f'{y + 20}" width="1500" height="{y + 20}" '
            f'style="color:#1a1a1a"><rect width="1500" height="{y + 20}" '
            f'fill="white"/>' + "".join(parts) + "</svg>")


def main(argv=None):
    args = sys.argv[1:] if argv is None else argv
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
