#!/usr/bin/env python3
"""Featural block script renderer (SVG, stdlib only).

The featural mapping is normative data (channels.json script_features):
place -> base element, manner -> modifier, vowel height/backness ->
carrier-tick position, coda -> miniature onset form, check -> top-right
slot (filled dot = lexical check 1, ring = payload polarity 1).

Blocks are 100x100 units. Content words stack their syllable blocks
vertically into one tall glyph; particles render as a single block at
70% scale (silhouette skimming by height, SPEC §5 / script.md).

Usage:
  python3 tools/script.py word WORD [WORD...]      (romanized content words)
  python3 tools/script.py particle WORD            (h-onset particle)
  python3 tools/script.py payload WORD             (mode payload syllables)
  python3 tools/script.py specimen [--out PATH]
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from phonology import Inventory, Syllable  # noqa: E402

BLOCK = 100
STROKE = 5

# onset-zone geometry
CX, CY, CR = 33, 34, 20                  # labial circle
VX = 33                                  # coronal vertical x
# vowel carrier
CARRIER_X, CARRIER_Y0, CARRIER_Y1 = 74, 12, 62
TICK_LEN = 13
HEIGHT_Y = {"high": 20, "mid": 37, "low": 56}
# coda strip: miniatures scaled so all ink (incl. stroke caps) stays
# inside STRIP_Y0..STRIP_Y1
STRIP_Y0, STRIP_Y1 = 72, 94
CODA_SCALE, CODA_DX, CODA_DY = 0.35, 24, 72
# check slot (kept clear of the high-back vowel tick; see test bounds)
DOT_X, DOT_Y, DOT_R = 91, 7, 4.5

# (place, manner) pairs with implemented, visually verified recipes.
# The 30-cell feature grid is headroom (script.md §9); unimplemented
# cells raise rather than silently rendering a bare base.
SUPPORTED_RECIPES = {
    ("labial", "stop"), ("labial", "nasal"), ("labial", "approximant"),
    ("coronal", "stop"), ("coronal", "nasal"), ("coronal", "fricative"),
    ("coronal", "lateral"), ("palatal", "affricate"),
    ("palatal", "approximant"), ("velar", "stop"), ("glottal", "fricative"),
}


def _el(name, **attrs):
    a = " ".join(f'{k.replace("_", "-")}="{v}"' for k, v in attrs.items())
    return f"<{name} {a}/>"


def _line(x1, y1, x2, y2, w=STROKE):
    return _el("line", x1=x1, y1=y1, x2=x2, y2=y2,
               stroke="currentColor", stroke_width=w, stroke_linecap="round")


def _circle(cx, cy, r, w=STROKE, fill="none"):
    return _el("circle", cx=cx, cy=cy, r=r, stroke="currentColor",
               stroke_width=w, fill=fill)


def _arc(cx, cy, r, deg0, deg1, w=STROKE):
    import math
    a0, a1 = math.radians(deg0), math.radians(deg1)
    x0, y0 = cx + r * math.cos(a0), cy + r * math.sin(a0)
    x1, y1 = cx + r * math.cos(a1), cy + r * math.sin(a1)
    large = 1 if (deg1 - deg0) % 360 > 180 else 0
    return (f'<path d="M {x0:.2f} {y0:.2f} A {r} {r} 0 {large} 1 '
            f'{x1:.2f} {y1:.2f}" stroke="currentColor" '
            f'stroke-width="{w}" fill="none" stroke-linecap="round"/>')


class ScriptRenderer:
    def __init__(self, inv: Inventory | None = None):
        self.inv = inv or Inventory()
        sf = self.inv.spec["script_features"]
        self.onset_features = sf["onset_features"]
        self.vowel_features = sf["vowel_features"]

    # --- onset elements (place base + manner modifier) ---

    def _base(self, place, manner, scale=1.0, dx=0.0, dy=0.0):
        """Base element for a place, already split for 'broken' manner.

        Stroke widths scale with the geometry so miniatures (codas) stay
        legible instead of merging into blobs."""
        s = scale
        w = STROKE * s

        def T(x, y):
            return (dx + x * s, dy + y * s)

        parts = []
        broken = manner == "approximant"
        if place == "labial":
            cx, cy = T(CX, CY)
            if broken:  # gap at the top
                parts.append(_arc(cx, cy, CR * s, -50, 230, w=w))
            else:
                parts.append(_circle(cx, cy, CR * s, w=w))
        elif place == "coronal":
            x, _ = T(VX, 0)
            _, y0 = T(0, 14)
            _, y1 = T(0, 56)
            if broken:
                _, ym0 = T(0, 30)
                _, ym1 = T(0, 40)
                parts.append(_line(x, y0, x, ym0, w=w))
                parts.append(_line(x, ym1, x, y1, w=w))
            else:
                parts.append(_line(x, y0, x, y1, w=w))
        elif place == "palatal":
            x0, y0 = T(16, 56)
            x1, y1 = T(50, 14)
            if broken:
                xm0, ym0 = T(30, 39)
                xm1, ym1 = T(36, 31)
                parts.append(_line(x0, y0, xm0, ym0, w=w))
                parts.append(_line(xm1, ym1, x1, y1, w=w))
            else:
                parts.append(_line(x0, y0, x1, y1, w=w))
        elif place == "velar":
            x0, y0 = T(16, 14)
            x1, _ = T(50, 14)
            _, y1 = T(0, 56)
            parts.append(_line(x0, y0, x1, y0, w=w))
            parts.append(_line(x0, y0, x0, y1, w=w))
        elif place == "glottal":
            x0, y = T(22, 34)
            x1, _ = T(44, 34)
            parts.append(_line(x0, y, x1, y, w=w))
        return parts

    def _onset(self, roman, scale=1.0, dx=0.0, dy=0.0):
        f = self.onset_features[roman]
        place, manner = f["place"], f["manner"]
        if (place, manner) not in SUPPORTED_RECIPES:
            raise ValueError(
                f"no implemented recipe for {place} {manner} "
                f"(wide-model headroom, script.md §9)")
        s = scale
        w = STROKE * s

        def T(x, y):
            return (dx + x * s, dy + y * s)

        parts = self._base(place, manner, scale, dx, dy)
        if manner == "nasal":
            x0, y = T(20, 5)
            x1, _ = T(46, 5)
            parts.append(_line(x0, y, x1, y, w=w))
        elif manner == "fricative":
            if place == "coronal":
                x, _ = T(VX + 11, 0)
                _, y0 = T(0, 14)
                _, y1 = T(0, 56)
                parts.append(_line(x, y0, x, y1, w=w))
            elif place == "glottal":
                x0, y = T(22, 44)
                x1, _ = T(44, 44)
                parts.append(_line(x0, y, x1, y, w=w))
            elif place == "labial":
                cx, cy = T(CX, CY)
                parts.append(_circle(cx, cy, (CR - 9) * s, w=w))
        elif manner == "affricate":
            x0, y0 = T(22, 40)
            x1, y1 = T(44, 32)
            parts.append(_line(x0, y0, x1, y1, w=w))
        elif manner == "lateral":
            x, _ = T(VX, 0)
            _, y = T(0, 56)
            x1, _ = T(VX + 13, 0)
            parts.append(_line(x, y, x1, y, w=w))
        return parts

    # --- vowel carrier ---

    def _vowel(self, roman, scale=1.0, dx=0.0, dy=0.0):
        f = self.vowel_features[roman]
        s = scale

        def T(x, y):
            return (dx + x * s, dy + y * s)

        x, _ = T(CARRIER_X, 0)
        _, y0 = T(0, CARRIER_Y0)
        _, y1 = T(0, CARRIER_Y1)
        parts = [_line(x, y0, x, y1)]
        _, ty = T(0, HEIGHT_Y[f["height"]])
        tick = TICK_LEN * s
        if f["backness"] in ("front", "central"):
            parts.append(_line(x - tick, ty, x, ty))
        if f["backness"] in ("back", "central"):
            parts.append(_line(x, ty, x + tick, ty))
        return parts

    # --- coda (miniature onset form in the strip) ---

    def _coda(self, roman, dx=0.0, dy=0.0):
        if not roman:
            return []
        return self._onset(roman, scale=CODA_SCALE,
                           dx=dx + CODA_DX, dy=dy + CODA_DY)

    # --- check slot ---

    def _check(self, syl, payload, dx=0.0, dy=0.0):
        value = self.inv.register(syl, payload=payload)
        if value != 1:
            return []
        if payload:
            return [_circle(dx + DOT_X, dy + DOT_Y, DOT_R, w=2.5)]
        return [_el("circle", cx=dx + DOT_X, cy=dy + DOT_Y, r=DOT_R,
                    fill="currentColor")]

    # --- blocks and words ---

    def syllable_block(self, syl: Syllable, payload=False, dx=0.0, dy=0.0):
        parts = []
        parts += self._onset(syl.onset, dx=dx, dy=dy)
        parts += self._vowel(syl.vowel, dx=dx, dy=dy)
        parts += self._coda(syl.coda, dx=dx, dy=dy)
        parts += self._check(syl, payload, dx=dx, dy=dy)
        return parts

    def word_glyph(self, sylls, payload=False):
        """Content word: syllable blocks stacked vertically."""
        parts = []
        for i, syl in enumerate(sylls):
            parts += self.syllable_block(syl, payload=payload, dy=i * BLOCK)
        return parts, BLOCK, BLOCK * len(sylls)

    def particle_glyph(self, syl: Syllable):
        """Particle: single block at 70% scale (short silhouette)."""
        inner = self.syllable_block(syl)
        g = (f'<g transform="scale(0.7) translate(0 {BLOCK * 0.2})">'
             + "".join(inner) + "</g>")
        return [g], BLOCK * 0.7, BLOCK * 0.7 + 10

    def svg(self, parts, w, h):
        return (f'<svg xmlns="http://www.w3.org/2000/svg" '
                f'viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
                f'style="color:#1a1a1a">' + "".join(parts) + "</svg>")


def specimen(r: ScriptRenderer) -> str:
    inv = r.inv
    parts = []
    pad, cell, rowh = 8, 108, 132

    def place(parts_list, col, row, label=None, tall=1):
        x, y = pad + col * cell, pad + row * rowh
        g = f'<g transform="translate({x} {y})">' + "".join(parts_list) + "</g>"
        parts.append(g)
        if label:
            parts.append(f'<text x="{x + 50}" y="{y + tall * BLOCK + 16}" '
                         f'font-size="12" '
                         f'text-anchor="middle" fill="currentColor" '
                         f'font-family="monospace">{label}</text>')

    row = 0
    # all content syllables, one row per onset, columns = vowel x coda
    for o in inv.content_onsets:
        col = 0
        for v in inv.vowels:
            for c in inv.codas:
                syl = Syllable(o, v, c)
                place(r.syllable_block(syl), col, row,
                      inv.romanize_syllable(syl))
                col += 1
        row += 1
    # particle row
    col = 0
    for v in inv.vowels:
        for c in inv.codas:
            syl = Syllable("h", v, c)
            g, _, _ = r.particle_glyph(syl)
            place(g, col, row, inv.romanize_syllable(syl))
            col += 1
    row += 1
    # sample words
    from phonology import Syllable as S
    samples = [
        ("sala", [S("s", "a", ""), S("l", "a", "")]),
        ("salaan", [S("s", "a", ""), S("l", "a", "n")]),
        ("salaas", [S("s", "a", ""), S("l", "a", "s")]),
    ]
    col = 0
    for label, sylls in samples:
        glyph, _, _ = r.word_glyph(sylls)
        place(glyph, col, row, label, tall=len(sylls))
        col += 2
    # digit payload examples: ma=40 shows the ring (anti-check 1);
    # mi=42 shows the honest empty slot (anti-check 0)
    place(r.syllable_block(S("m", "a", ""), payload=True), col, row,
          "payload ma=40 (ring)")
    col += 2
    place(r.syllable_block(S("m", "i", ""), payload=True), col, row,
          "payload mi=42 (no mark)")
    # running text: pseudo-lexicon sentence, vertical-stacking layout
    row += 3
    sentence = [
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
    y = pad + row * rowh
    roman_line = []
    for kind, sylls in sentence:
        if kind == "p":
            g, gw, _ = r.particle_glyph(sylls[0])
            parts.append(f'<g transform="translate({x} {y})">'
                         + "".join(g) + "</g>")
            x += gw + 18
        else:
            glyph, gw, _ = r.word_glyph(sylls)
            parts.append(f'<g transform="translate({x} {y})">'
                         + "".join(glyph) + "</g>")
            x += gw + 18
        roman_line.append(inv.romanize_word(sylls))
    parts.append(f'<text x="{pad}" y="{y + 3 * BLOCK + 24}" font-size="13" '
                 f'fill="currentColor" font-family="monospace">'
                 f'sentence (pseudo-lexicon): {" ".join(roman_line)}</text>')
    w = pad * 2 + cell * 20
    h = pad * 2 + rowh * (row + 4)
    return r.svg(parts, w, h)


def main(argv=None) -> int:
    r = ScriptRenderer()
    inv = r.inv
    args = sys.argv[1:] if argv is None else argv

    def usage(msg):
        print(f"error: {msg}", file=sys.stderr)
        print(__doc__, file=sys.stderr)
        return 2

    if not args:
        return usage("no command")
    cmd = args[0]
    if cmd in ("word", "payload"):
        if len(args) < 2:
            return usage(f"{cmd} needs at least one romanized word")
        payload = cmd == "payload"
        mode = "payload" if payload else "lexical"
        all_parts, x = [], 0
        maxh = 0
        for wtext in args[1:]:
            sylls = inv.parse_word(wtext, mode=mode)
            glyph, gw, gh = r.word_glyph(sylls, payload=payload)
            all_parts.append(f'<g transform="translate({x} 0)">'
                             + "".join(glyph) + "</g>")
            x += gw + 16
            maxh = max(maxh, gh)
        print(r.svg(all_parts, x, maxh))
    elif cmd == "particle":
        if len(args) != 2:
            return usage("particle needs exactly one romanized particle")
        sylls = inv.parse_word(args[1], mode="lexical")
        problems = inv.validate_particle(sylls)
        if problems:
            return usage(f"not a valid particle: {'; '.join(problems)}")
        glyph, gw, gh = r.particle_glyph(sylls[0])
        print(r.svg(glyph, gw, gh))
    elif cmd == "specimen":
        out = None
        rest = args[1:]
        if rest and rest[0] == "--out":
            if len(rest) != 2:
                return usage("--out needs a path")
            out = rest[1]
        elif rest:
            return usage(f"unknown specimen arguments: {rest}")
        svg = specimen(r)
        if out:
            Path(out).write_text(svg)
            print(f"written: {out}")
        else:
            print(svg)
    else:
        return usage(f"unknown command {cmd!r}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
