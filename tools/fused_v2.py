#!/usr/bin/env python3
"""Fused word-characters v2: disyllable-unity mechanisms (r5y).

The v1 verdict (script-fusion-study.md): trisyllables compose, but a
disyllable "still reads as a letter pair". This renders the study's
named candidate mechanisms side by side as a WORKSHOP ROUND
(docs/process/design-workshop.md):

  U0  v1 baseline        symmetric 50/50 left|right halves (control)
  U1  asymmetric 40/60   narrow first component, dominant second —
                         the hanzi radical/phonetic proportion
  U2  interlock          components overlap; the second letter nests
                         into the first's right whitespace
  U3  shared spine       the first syllable's vowel stub grows into a
                         full-height midline stroke BOTH components
                         attach to; syllable-1 vowel ticks ride the
                         spine (feature logic unchanged: height =
                         vowel height, side = backness)
  U4  vertical stack     top/bottom halves (hanzi type-2 composition)

Output: one comparison sheet, full-size row per mechanism + a
reading-size paragraph strip per mechanism (both scales, per the
workshop spec). Exploration render — no floors asserted here; the
fair-metric pass follows whichever mechanism survives the round.

Usage: python3 tools/fused_v2.py sheet [--out PATH]
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from fused_script import (FusedRenderer, VOWEL_TICKS,  # noqa: E402
                          transform_parts)
from phonology import Syllable  # noqa: E402
from script import _el, _line  # noqa: E402


class FusedV2(FusedRenderer):

    def _component_v2(self, syl, x0, y0, x1, y1, stub=True,
                      check_syl=None):
        """As v1's _component, with the vowel stub optional (U3 moves
        syllable-1's vowel onto the shared spine)."""
        cw, ch = x1 - x0, y1 - y0
        span = 86 if stub else 62          # no stub apparatus to fit
        s = min((cw - 10) / span, (ch - 6) / 56)
        lx = x0 + 3 - 8 * s
        ly = y0 + (ch - 52 * s) / 2 - 8 * s
        parts = transform_parts(self.r._onset(syl.onset), s, lx, ly,
                                floor=self.floor)
        if stub:
            frac, inward, outward = VOWEL_TICKS[syl.vowel]
            edge_x = lx + 74 * s
            ty = ly + (8 + 52 * frac) * s
            st = max(11.0 * s, 7.0)
            tk = max(9.0 * s, 6.5)
            w = max(5 * s, self.floor)
            parts.append(_line(edge_x, ty - st, edge_x, ty + st, w=w))
            if inward:
                parts.append(_line(edge_x - tk, ty, edge_x, ty, w=w))
            if outward:
                parts.append(_line(edge_x, ty, edge_x + tk, ty, w=w))
        if syl.coda:
            cyy = y1 - 3
            parts.append(_line(x1 - 16, cyy, x1 - 4, cyy, w=4))
            if syl.coda == "s":
                parts.append(_line(x1 - 16, cyy - 6, x1 - 4, cyy - 6, w=4))
            elif syl.coda == "l":
                parts.append(_line(x1 - 4, cyy, x1 - 4, cyy - 8, w=4))
        if self.inv.register(check_syl or syl) == 1:
            parts.append(_el("circle", cx=x1 - 6, cy=y0 + 6, r=4.2,
                             fill="currentColor"))
        return parts

    def _pos_radical(self, final, dx, dy):
        if not final:
            return []
        yy = dy + 86
        if final == "n":
            return [_line(dx + 30, yy, dx + 70, yy)]
        if final == "s":
            return [_line(dx + 30, yy - 4, dx + 70, yy - 4),
                    _line(dx + 30, yy + 5, dx + 70, yy + 5)]
        if final == "l":
            return [_line(dx + 30, yy, dx + 64, yy),
                    _line(dx + 64, yy, dx + 64, yy - 8)]
        return []

    def disyllable(self, sylls, mech, dx=0.0, dy=0.0):
        """One disyllabic character under unity mechanism U0-U4."""
        assert len(sylls) == 2
        final = sylls[-1].coda
        body_y1 = dy + (74 if final else 96)
        s2 = Syllable(sylls[1].onset, sylls[1].vowel, "")
        parts = []
        if mech == "U0":                     # v1 control
            return self.word_char_v1(sylls, dx=dx, dy=dy)
        if mech == "U1":                     # asymmetric 40/60
            mid = dx + 41
            parts += self._component_v2(sylls[0], dx + 3, dy + 4,
                                        mid - 2, body_y1)
            parts += self._component_v2(s2, mid + 2, dy + 4, dx + 97,
                                        body_y1, check_syl=sylls[1])
        elif mech == "U2":                   # interlock: 14u overlap
            parts += self._component_v2(sylls[0], dx + 3, dy + 4,
                                        dx + 57, body_y1)
            parts += self._component_v2(s2, dx + 43, dy + 4, dx + 97,
                                        body_y1, check_syl=sylls[1])
        elif mech == "U3":                   # shared spine
            mid = dx + 50
            parts += self._component_v2(sylls[0], dx + 4, dy + 4,
                                        mid - 4, body_y1, stub=False)
            parts += self._component_v2(s2, mid + 4, dy + 4, dx + 97,
                                        body_y1, stub=True,
                                        check_syl=sylls[1])
            # the spine: one full-height stroke both halves touch;
            # syllable-1's vowel ticks ride it (height = vowel height,
            # side = backness — feature logic unchanged)
            parts.append(_line(mid, dy + 6, mid, body_y1 - 2, w=5))
            frac, inward, outward = VOWEL_TICKS[sylls[0].vowel]
            ty = dy + 10 + (body_y1 - dy - 20) * frac
            if inward:
                parts.append(_line(mid - 10, ty, mid, ty, w=5))
            if outward:
                parts.append(_line(mid, ty, mid + 10, ty, w=5))
        elif mech == "U4":                   # vertical stack
            mid_y = dy + 4 + (body_y1 - dy - 4) / 2
            parts += self._component_v2(sylls[0], dx + 8, dy + 4,
                                        dx + 92, mid_y - 2)
            parts += self._component_v2(s2, dx + 8, mid_y + 2,
                                        dx + 92, body_y1,
                                        check_syl=sylls[1])
        else:
            raise ValueError(mech)
        parts += self._pos_radical(final, dx, dy)
        return parts


MECHS = [
    ("U0", "v1 control: symmetric halves"),
    ("U1", "asymmetric 40/60 (radical/phonetic proportion)"),
    ("U2", "interlock (14u overlap)"),
    ("U3", "shared spine (syl-1 vowel rides the midline stroke)"),
    ("U4", "vertical stack (hanzi type-2)"),
]

S = Syllable
WORDS = [
    ("sala", [S("s", "a", ""), S("l", "a", "")]),
    ("salaan", [S("s", "a", ""), S("l", "a", "n")]),
    ("taako", [S("t", "a", ""), S("k", "o", "")]),
    ("piton", [S("p", "i", ""), S("t", "o", "n")]),
    ("lewas", [S("l", "e", ""), S("w", "a", "s")]),
    ("namu", [S("n", "a", ""), S("m", "u", "")]),
]
SENT = [[S("t", "a", ""), S("k", "o", "")],
        [S("s", "a", ""), S("l", "a", "n")],
        [S("m", "e", ""), S("n", "o", "")],
        [S("k", "u", ""), S("p", "i", "")],
        [S("l", "e", ""), S("w", "a", "s")],
        [S("n", "a", ""), S("m", "u", "")],
        [S("p", "o", ""), S("t", "e", "n")],
        [S("w", "i", ""), S("m", "a", "")]]


def sheet(fr: FusedV2) -> str:
    parts, y = [], 14

    def label(x, ytxt, t):
        parts.append(f'<text x="{x}" y="{ytxt}" font-size="13" '
                     f'fill="#555" font-family="monospace">{t}</text>')

    for mech, desc in MECHS:
        x = 14
        for name, sylls in WORDS:
            parts += fr.disyllable(sylls, mech, dx=x, dy=y)
            x += 124
        label(14, y + 118, f"{mech}: {desc}")
        # reading-size line (0.45 scale ~ 45px chars), own row
        strip = []
        for i, sylls in enumerate(SENT * 2):
            strip += fr.disyllable(sylls, mech, dx=i * 108, dy=0)
        parts += transform_parts(strip, 0.45, 14, y + 130, floor=1.6)
        y += 205
    label(14, y + 6, "words: sala salaan taako piton lewas namu; "
                     "second row of each pair = reading size")
    return fr.svg(parts, 1240, y + 30)


def main(argv=None) -> int:
    args = sys.argv[1:] if argv is None else argv
    fr = FusedV2()
    if args and args[0] == "sheet":
        out = args[args.index("--out") + 1] if "--out" in args else None
        s = sheet(fr)
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
