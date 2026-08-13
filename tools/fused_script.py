#!/usr/bin/env python3
"""Fused word-characters for the greenfield script — r5y study v0.

One glyph per word (the stated ideal): a content word of 1-3
syllables renders as ONE square character.

The unlock is the abugida move: the vowel carrier bar (~30% of block
width) is deleted; vowels become short ticks ATTACHED to the onset
letterform's right edge, keeping the same feature logic —
height = vowel height, direction = backness:

    i = high, inward    u = high, outward
    e = mid,  inward    o = mid,  outward
    a = low,  crossing (both)

Character anatomy (square, 100x100):
  - 1-3 syllable-letters left-to-right in the body (temporal order),
    scaled by count (1: 90%, 2: 55%, 3: 38%)
  - POS strip spans the full character bottom (the final coda IS the
    word's POS, so the strip is word-level ink — unchanged principle)
  - medial codas: small bar under their own syllable-letter
  - per-syllable written-check dots above each letter slot (computed,
    droppable)

Codespace: 220^2 ~ 48k disyllabic characters (the "~50k codepoints
per char" target), composed from 11 letterforms + 5 tick positions +
strip marks — nothing enumerated, everything computed.

Usage:
  python3 tools/fused_script.py word WORD [WORD...]   (romanized)
  python3 tools/fused_script.py specimen [--out PATH]
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import xml.etree.ElementTree as ET  # noqa: E402

from phonology import Inventory, Syllable  # noqa: E402
from script import ScriptRenderer, _circle, _el, _line  # noqa: E402


STROKE_FLOOR = 4.4     # fused-mode ink never thins below this (units)


def transform_parts(parts, s, dx, dy):
    """Numerically scale+translate SVG line/circle fragments (keeps
    everything top-level so the raster machinery sees the ink). Stroke
    widths are floored: sub-pixel ink is the death mode of fusion."""
    out = []
    for el in ET.fromstring("<svg>" + "".join(parts) + "</svg>"):
        w = max(float(el.get("stroke-width", 0)) * s, STROKE_FLOOR)
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
                out.append(_el("circle", cx=cx, cy=cy, r=r,
                               fill="currentColor"))
            else:
                out.append(_circle(cx, cy, r, w=w))
    return out

CHAR = 100
STRIP_Y0, STRIP_Y1 = 74, 96
STRIP_X0, STRIP_X1 = 8, 92

# per-syllable-count layout: (scale, [slot x-centers], letter y)
LAYOUTS = {
    1: (0.90, [50], 8),
    2: (0.55, [26, 74], 16),
    3: (0.38, [17, 50, 83], 22),
}
# vowel tick: (height fraction of letter box, inward, outward)
VOWEL_TICKS = {
    "i": (0.18, True, False), "u": (0.18, False, True),
    "e": (0.52, True, False), "o": (0.52, False, True),
    "a": (0.86, True, True),
}


class FusedRenderer:
    def __init__(self, inv: Inventory | None = None):
        self.r = ScriptRenderer(inv)
        self.inv = self.r.inv

    def syllable_letter(self, syl: Syllable, scale, cx, top):
        """Onset letterform + attached vowel tick, centered at cx."""
        # the greenfield onset zone spans roughly x 8..66, y 8..60;
        # its center is ~(37, 34)
        s = scale
        dx = cx - 37 * s
        dy = top
        parts = transform_parts(self.r._onset(syl.onset), s, dx, dy)
        # vowel = miniature carrier stub at the letter's right edge:
        # a short vertical stub at tick height + the v0.2 tick logic
        # (front = left, back = right, central = both). The stub keeps
        # the measured robustness of the full carrier at ~1/3 size.
        frac, inward, outward = VOWEL_TICKS[syl.vowel]
        edge_x = dx + 74 * s
        ty = dy + (8 + 52 * frac) * s
        stub = max(11.0 * s, 8.0)
        tick = max(10.0 * s, 7.5)
        w = max(5 * s, STROKE_FLOOR)
        parts.append(_line(edge_x, ty - stub, edge_x, ty + stub, w=w))
        if inward:
            parts.append(_line(edge_x - tick, ty, edge_x, ty, w=w))
        if outward:
            parts.append(_line(edge_x, ty, edge_x + tick, ty, w=w))
        return parts

    def word_char(self, sylls, dx=0.0, dy=0.0, checks=True):
        """One square character for a 1-3 syllable content word."""
        n = len(sylls)
        if n not in LAYOUTS:
            raise ValueError("content words are 1-3 syllables")
        scale, slots, top = LAYOUTS[n]
        parts = []
        for syl, cx in zip(sylls, slots):
            parts += [p if isinstance(p, str) else p for p in
                      self.syllable_letter(syl, scale, dx + cx, dy + top)]
            # medial coda (non-final): small bar under its own letter
            if syl is not sylls[-1] and syl.coda:
                bw = 26 * (scale / 0.55)
                parts.append(_line(dx + cx - bw / 2, dy + 68,
                                   dx + cx + bw / 2, dy + 68, w=3.5))
                if syl.coda == "s":
                    parts.append(_line(dx + cx - bw / 2, dy + 63,
                                       dx + cx + bw / 2, dy + 63, w=3.5))
            if checks and self.inv.register(syl) == 1:
                parts.append(_el("circle", cx=dx + cx, cy=dy + 7, r=4.5,
                                 fill="currentColor"))
        # word-level POS strip = final coda
        final = sylls[-1].coda
        def L(x1, y1, x2, y2):
            return _line(dx + x1, dy + y1, dx + x2, dy + y2)
        if final == "n":
            parts.append(L(STRIP_X0, 85, STRIP_X1, 85))
        elif final == "s":
            parts += [L(STRIP_X0, 80, STRIP_X1, 80),
                      L(STRIP_X0, 90, STRIP_X1, 90)]
        elif final == "l":
            parts += [L(STRIP_X0, 82, 82, 82), L(82, 82, 82, 92)]
        return parts

    # --- v1: radical composition (response to review: v0 read as
    # "underlined English" — letter-row + full-width rule. v1 composes
    # hanzi-style: components FILL regions, POS is a bottom radical
    # region with short centered marks, ink density evens out.) ---

    def _component(self, syl: Syllable, x0, y0, x1, y1, check=True):
        """One syllable as a component filling cell (x0,y0)-(x1,y1):
        onset letterform fitted to the cell, vowel stub inside the
        cell's right edge, medial coda as a corner tick."""
        cw, ch = x1 - x0, y1 - y0
        # letter ink spans ~(8..66, 8..60) = 58x52; leave room for the
        # vowel stub (12u) at the right of the letter
        s = min((cw - 14) / 58, ch / 52)
        lx = x0 + (cw - 14 - 58 * s) / 2 - 8 * s
        ly = y0 + (ch - 52 * s) / 2 - 8 * s
        parts = transform_parts(self.r._onset(syl.onset), s, lx, ly)
        frac, inward, outward = VOWEL_TICKS[syl.vowel]
        edge_x = lx + 74 * s
        ty = ly + (8 + 52 * frac) * s
        stub = max(11.0 * s, 7.0)
        tick = max(9.0 * s, 6.5)
        w = max(5 * s, STROKE_FLOOR)
        parts.append(_line(edge_x, ty - stub, edge_x, ty + stub, w=w))
        if inward:
            parts.append(_line(edge_x - tick, ty, edge_x, ty, w=w))
        if outward:
            parts.append(_line(edge_x, ty, edge_x + tick, ty, w=w))
        if syl.coda:                      # medial coda: corner tick(s)
            cyy = y1 - 3
            parts.append(_line(x1 - 16, cyy, x1 - 4, cyy, w=4))
            if syl.coda == "s":
                parts.append(_line(x1 - 16, cyy - 6, x1 - 4, cyy - 6, w=4))
        if check and self.inv.register(syl) == 1:
            parts.append(_el("circle", cx=x1 - 6, cy=y0 + 6, r=4.2,
                             fill="currentColor"))
        return parts

    def word_char_v1(self, sylls, dx=0.0, dy=0.0):
        """v1 character: radical composition. 1-syl fills the square;
        2-syl = left|right halves; 3-syl = left + stacked right.
        POS = bottom radical region (short centered marks)."""
        n = len(sylls)
        final = sylls[-1].coda
        body_y1 = dy + (74 if final else 96)
        parts = []
        if n == 1:
            parts += self._component(sylls[0], dx + 6, dy + 4,
                                     dx + 94, body_y1)
        elif n == 2:
            mid = dx + 50
            parts += self._component(sylls[0], dx + 3, dy + 4, mid - 2,
                                     body_y1)
            s2 = Syllable(sylls[1].onset, sylls[1].vowel, "")
            parts += self._component(s2, mid + 2, dy + 4, dx + 97,
                                     body_y1)
        elif n == 3:
            mid = dx + 48
            h2 = (body_y1 - dy - 4) / 2
            parts += self._component(sylls[0], dx + 3, dy + 4, mid - 2,
                                     body_y1)
            parts += self._component(sylls[1], mid + 2, dy + 4,
                                     dx + 97, dy + 4 + h2 - 2)
            s3 = Syllable(sylls[2].onset, sylls[2].vowel, "")
            parts += self._component(s3, mid + 2, dy + 4 + h2 + 2,
                                     dx + 97, body_y1)
        else:
            raise ValueError("content words are 1-3 syllables")
        # POS bottom radical region: SHORT centered marks (not a rule)
        if final:
            yy = dy + 86
            if final == "n":
                parts.append(_line(dx + 30, yy, dx + 70, yy))
            elif final == "s":
                parts += [_line(dx + 30, yy - 4, dx + 70, yy - 4),
                          _line(dx + 30, yy + 5, dx + 70, yy + 5)]
            elif final == "l":
                parts += [_line(dx + 30, yy, dx + 64, yy),
                          _line(dx + 64, yy, dx + 64, yy - 8)]
        return parts

    def particle_char(self, syl: Syllable, dx=0.0, dy=0.0, v1=False):
        """Particles stay small: 60% character, vertically centered."""
        maker = self.word_char_v1 if v1 else self.word_char
        if v1:
            inner = self.word_char_v1([syl])
        else:
            inner = self.word_char([syl], checks=False)
        return transform_parts(inner, 0.6, dx, dy + 14)

    def svg(self, parts, w, h):
        return (f'<svg xmlns="http://www.w3.org/2000/svg" '
                f'viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
                f'style="color:#1a1a1a">' + "".join(parts) + "</svg>")


def specimen(fr: FusedRenderer) -> str:
    inv = fr.inv
    S = Syllable
    parts = []
    pad = 10

    def label(x, y, t):
        parts.append(f'<text x="{x}" y="{y}" font-size="12" '
                     f'fill="currentColor" font-family="monospace">{t}</text>')

    # row 1: one word, three POS forms + a trisyllable + payload-free
    y = pad
    samples = [
        ("sala", [S("s", "a", ""), S("l", "a", "")]),
        ("salaan", [S("s", "a", ""), S("l", "a", "n")]),
        ("salaas", [S("s", "a", ""), S("l", "a", "s")]),
        ("taako", [S("t", "a", ""), S("k", "o", "")]),
        ("menokis", [S("m", "e", ""), S("n", "o", ""), S("k", "i", "s")]),
        ("ku", [S("k", "u", "")]),
        ("piton", [S("p", "i", ""), S("t", "o", "n")]),
        ("lewas", [S("l", "e", ""), S("w", "a", "s")]),
        ("namu", [S("n", "a", ""), S("m", "u", "")]),
        ("tasmabru?", [S("t", "a", "s"), S("m", "a", ""), S("l", "u", "")]),
    ]
    x = pad
    for name, sylls in samples:
        parts += fr.word_char(sylls, dx=x, dy=y)
        label(x + 8, y + 116, inv.romanize_word(sylls))
        x += 128
    y += 140
    # row 2: vowel demonstration — one onset, all five vowels
    x = pad
    for v in "iueoa":
        parts += fr.word_char([S("t", v, "")], dx=x, dy=y)
        label(x + 30, y + 116, inv.romanize_syllable(S("t", v, "")))
        x += 128
    # spacing demo: the specimen sentence as fused characters
    y += 150
    sent = [
        ("p", [S("h", "u", "")]),
        ("w", [S("t", "a", ""), S("k", "o", "")]),
        ("w", [S("s", "a", ""), S("l", "a", "n")]),
        ("p", [S("h", "e", "")]),
        ("w", [S("m", "e", ""), S("n", "o", ""), S("k", "i", "s")]),
        ("p", [S("h", "a", "")]),
        ("w", [S("k", "u", "")]),
        ("w", [S("p", "i", ""), S("t", "o", "n")]),
        ("p", [S("h", "o", "s")]),
        ("w", [S("l", "e", ""), S("w", "a", "s")]),
        ("w", [S("n", "a", ""), S("m", "u", "")]),
    ]
    x = pad
    for kind, sylls in sent:
        if kind == "p":
            parts += fr.particle_char(sylls[0], dx=x, dy=y)
            x += 72
        else:
            parts += fr.word_char(sylls, dx=x, dy=y)
            x += 112
    label(pad, y + 126, "sentence: one character per word "
                        "(particles small; word count = char count)")
    return fr.svg(parts, 1400, y + 150)


def main(argv=None) -> int:
    fr = FusedRenderer()
    inv = fr.inv
    args = sys.argv[1:] if argv is None else argv
    if not args:
        print(__doc__, file=sys.stderr)
        return 2
    if args[0] == "word":
        all_parts, x = [], 0
        for wtext in args[1:]:
            sylls = inv.parse_word(wtext, mode="lexical")
            all_parts += fr.word_char(sylls, dx=x)
            x += 112
        print(fr.svg(all_parts, x, 110))
    elif args[0] == "specimen":
        out = args[args.index("--out") + 1] if "--out" in args else None
        s = specimen(fr)
        if out:
            Path(out).write_text(s)
            print(f"written: {out}")
        else:
            print(s)
    else:
        print(__doc__, file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
