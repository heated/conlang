#!/usr/bin/env python3
"""Featural block script renderer, v0.2 (SVG, stdlib only).

The featural mapping is normative data (channels.json script_features):
onset -> (base, modifier) cell of the confusion-aware anti-iconic code
(solved by tools/assign_glyphs.py — every phonetic confusion pair
differs in BOTH base and modifier); vowel height/backness ->
carrier-tick position; coda -> strip-native full-width mark (POS gets
the loudest ink); written check -> top-right dot (lexical only).
Payload spans are marked by a continuous run-rule beside the glyph
stack, not per-block marks.

Blocks are 100x100 units. Content words stack their syllable blocks
vertically into one tall glyph; particles render as a single block at
70% scale (silhouette skimming by height, SPEC §5 / script.md). A
horizontal shared-headstroke layout is implemented as the documented
alternative for the freeze-gate comparison.

Usage:
  python3 tools/script.py word WORD [WORD...]      (romanized content words)
  python3 tools/script.py particle WORD            (h-onset particle)
  python3 tools/script.py payload WORD             (mode payload syllables)
  python3 tools/script.py specimen [--out PATH]
"""

from __future__ import annotations

import sys
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from phonology import Inventory, Syllable  # noqa: E402

BLOCK = 100
STROKE = 5

# onset-zone geometry
CX, CY, CR = 33, 34, 20                  # circle base
VX = 33                                  # vertical base x
ZY0, ZY1 = 12, 58                        # base vertical extent
# vowel carrier
CARRIER_X, CARRIER_Y0, CARRIER_Y1 = 74, 12, 62
TICK_LEN = 13
HEIGHT_Y = {"high": 20, "mid": 37, "low": 56}
# coda strip: full-width strip-native marks
STRIP_Y0, STRIP_Y1 = 72, 94
STRIP_X0, STRIP_X1 = 12, 88
# check slot (kept clear of the high-back vowel tick; see test bounds)
DOT_X, DOT_Y, DOT_R = 91, 7, 4.5
# payload run-rule
RULE_X, RULE_W = 4, 3

# (base, modifier) cells with implemented, visually verified recipes.
# The rest of the feature grid is headroom (script.md §9); unimplemented
# cells raise rather than silently rendering a bare base.
SUPPORTED_RECIPES = {
    ("circle", "plain"), ("circle", "crossed"), ("circle", "capped"),
    ("vertical", "plain"), ("vertical", "crossed"), ("vertical", "doubled"),
    ("diagonal", "crossed"), ("diagonal", "doubled"),
    ("angle", "plain"), ("angle", "doubled"),
    ("tick", "doubled"),
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


class ScriptRenderer:
    def __init__(self, inv: Inventory | None = None):
        self.inv = inv or Inventory()
        sf = self.inv.spec["script_features"]
        self.onset_features = sf["onset_features"]
        self.vowel_features = sf["vowel_features"]

    # --- onset letters: (base, modifier) cell realizations ---

    def _onset(self, roman, dx=0.0, dy=0.0):
        f = self.onset_features[roman]
        base, mod = f["base"], f["modifier"]
        if (base, mod) not in SUPPORTED_RECIPES:
            raise ValueError(
                f"no implemented recipe for {base} {mod} "
                f"(feature-grid headroom, script.md §9)")

        def L(x1, y1, x2, y2):
            return _line(dx + x1, dy + y1, dx + x2, dy + y2)

        parts = []
        if base == "circle":
            parts.append(_circle(dx + CX, dy + CY, CR))
            if mod == "crossed":       # Ø: full diagonal through center
                parts.append(L(18, 49, 48, 19))
            elif mod == "capped":      # attached top bar
                parts.append(L(14, 11, 52, 11))
        elif base == "vertical":
            if mod == "doubled":       # wide parallel pair
                parts.append(L(24, ZY0, 24, ZY1))
                parts.append(L(44, ZY0, 44, ZY1))
            else:
                parts.append(L(VX, ZY0, VX, ZY1))
                if mod == "crossed":   # +
                    parts.append(L(18, 35, 48, 35))
        elif base == "diagonal":
            if mod == "doubled":       # wide parallel pair, rising
                parts.append(L(8, ZY1, 46, 14))
                parts.append(L(26, ZY1, 64, 14))
            else:
                parts.append(L(14, ZY1, 52, 14))
                if mod == "crossed":   # X
                    parts.append(L(14, 14, 52, ZY1))
        elif base == "angle":
            parts.append(L(14, 14, 52, 14))
            parts.append(L(14, 14, 14, ZY1))
            if mod == "doubled":       # nested inner corner
                parts.append(L(30, 30, 52, 30))
                parts.append(L(30, 30, 30, ZY1))
        elif base == "tick":
            parts.append(L(22, 34, 44, 34))
            if mod == "doubled":       # h: "="
                parts.append(L(22, 44, 44, 44))
        return parts

    # --- vowel carrier ---

    def _vowel(self, roman, dx=0.0, dy=0.0):
        f = self.vowel_features[roman]
        x = dx + CARRIER_X
        parts = [_line(x, dy + CARRIER_Y0, x, dy + CARRIER_Y1)]
        ty = dy + HEIGHT_Y[f["height"]]
        if f["backness"] in ("front", "central"):
            parts.append(_line(x - TICK_LEN, ty, x, ty))
        if f["backness"] in ("back", "central"):
            parts.append(_line(x, ty, x + TICK_LEN, ty))
        return parts

    # --- coda: strip-native full-width marks (POS channel) ---

    def _coda(self, roman, dx=0.0, dy=0.0):
        def L(x1, y1, x2, y2):
            return _line(dx + x1, dy + y1, dx + x2, dy + y2)

        if not roman:
            return []
        if roman == "n":               # single bar = verb
            return [L(STRIP_X0, 83, STRIP_X1, 83)]
        if roman == "s":               # double bar = modifier
            return [L(STRIP_X0, 78, STRIP_X1, 78),
                    L(STRIP_X0, 88, STRIP_X1, 88)]
        if roman == "l":               # hooked bar = reserved
            return [L(STRIP_X0, 80, 80, 80), L(80, 80, 80, 88)]
        raise ValueError(f"unknown coda {roman!r}")

    # --- check slot (lexical written check only) ---

    def _check(self, syl, payload, dx=0.0, dy=0.0):
        if payload:
            return []                  # payload spans use the run-rule
        if self.inv.register(syl) != 1:
            return []
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
        """Content word: syllable blocks stacked vertically. Payload
        words carry a continuous run-rule beside the stack."""
        parts = []
        for i, syl in enumerate(sylls):
            parts += self.syllable_block(syl, payload=payload, dy=i * BLOCK)
        h = BLOCK * len(sylls)
        if payload:
            parts.append(_line(RULE_X, 4, RULE_X, h - 4, w=RULE_W))
        return parts, BLOCK, h

    def word_glyph_horizontal(self, sylls):
        """Documented alternative layout: blocks left-to-right under a
        shared headstroke (freeze-gate comparison; content words only)."""
        parts = []
        for i, syl in enumerate(sylls):
            parts += self.syllable_block(syl, dx=i * BLOCK)
        w = BLOCK * len(sylls)
        parts.append(_line(4, 4, w - 4, 4, w=3.5))
        return parts, w, BLOCK

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


# --- raster regression floor -------------------------------------------

def rasterize(parts, x0, y0, x1, y1, n):
    """Occupancy grid of an SVG fragment list over a window: the set of
    n x n cells whose centers fall on ink. Pure stdlib; supports the
    line/circle primitives the renderer emits."""
    prims = []
    for el in ET.fromstring("<svg>" + "".join(parts) + "</svg>"):
        w = float(el.get("stroke-width", 0))
        if el.tag == "line":
            prims.append(("line", float(el.get("x1")), float(el.get("y1")),
                          float(el.get("x2")), float(el.get("y2")), w))
        elif el.tag == "circle":
            filled = el.get("fill") == "currentColor"
            prims.append(("circle", float(el.get("cx")), float(el.get("cy")),
                          float(el.get("r")), filled, w))
    on = set()
    for i in range(n):
        for j in range(n):
            px = x0 + (x1 - x0) * (i + 0.5) / n
            py = y0 + (y1 - y0) * (j + 0.5) / n
            for p in prims:
                if p[0] == "line":
                    _, ax, ay, bx, by, w = p
                    vx, vy = bx - ax, by - ay
                    L2 = vx * vx + vy * vy
                    t = 0.0 if L2 == 0 else max(
                        0.0, min(1.0, ((px - ax) * vx + (py - ay) * vy) / L2))
                    ddx, ddy = px - (ax + t * vx), py - (ay + t * vy)
                    if (ddx * ddx + ddy * ddy) ** 0.5 <= w / 2:
                        on.add((i, j))
                        break
                else:
                    _, cx, cy, r, filled, w = p
                    dist = ((px - cx) ** 2 + (py - cy) ** 2) ** 0.5
                    hit = dist <= r if filled else abs(dist - r) <= w / 2
                    if hit:
                        on.add((i, j))
                        break
    return frozenset(on)


def raster_distance(a, b):
    """1 - IoU of two occupancy grids (1.0 = disjoint, 0.0 = identical)."""
    if not a and not b:
        return 0.0
    return 1.0 - len(a & b) / len(a | b)


# --- specimen -----------------------------------------------------------

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
    S = Syllable
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
    # payload example: digits 40 42 as one payload word with run-rule
    pay = [S("m", "a", ""), S("m", "i", "")]
    glyph, _, _ = r.word_glyph(pay, payload=True)
    place(glyph, col, row, "payload 4042 (run-rule)", tall=2)
    # running text: same pseudo-lexicon sentence in BOTH layouts
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
    roman_line = [inv.romanize_word(sylls) for _, sylls in sentence]
    row += 3
    x, y = pad, pad + row * rowh
    for kind, sylls in sentence:
        if kind == "p":
            g, gw, _ = r.particle_glyph(sylls[0])
        else:
            g, gw, _ = r.word_glyph(sylls)
        parts.append(f'<g transform="translate({x} {y})">'
                     + "".join(g) + "</g>")
        x += gw + 18
    parts.append(f'<text x="{pad}" y="{y + 3 * BLOCK + 24}" font-size="13" '
                 f'fill="currentColor" font-family="monospace">'
                 f'stacked layout: {" ".join(roman_line)}</text>')
    row += 3
    x, y = pad, pad + row * rowh + 20
    for kind, sylls in sentence:
        if kind == "p":
            g, gw, _ = r.particle_glyph(sylls[0])
        else:
            g, gw, _ = r.word_glyph_horizontal(sylls)
        parts.append(f'<g transform="translate({x} {y})">'
                     + "".join(g) + "</g>")
        x += gw + 18
    parts.append(f'<text x="{pad}" y="{y + BLOCK + 24}" font-size="13" '
                 f'fill="currentColor" font-family="monospace">'
                 f'headstroke layout (alternative): same sentence</text>')
    w = pad * 2 + max(cell * 20, x)
    h = pad * 2 + rowh * (row + 2)
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
