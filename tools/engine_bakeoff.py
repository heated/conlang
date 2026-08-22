#!/usr/bin/env python3
"""GZ script-engine bake-off on GZ-shaped text (conlang-e35).

Four genuinely different engines render the SAME specimen (words +
a running paragraph with particles and codas), so the fork the
program charter left open — which rendering engine carries the GZ
script — can be judged side by side:

  E0  boxed featural blocks (v0.2 script.py): syllable blocks
      stacked vertically; vowel = carrier tick; coda = strip mark.
      The incumbent.
  E1  continuous stroke chain (strokes_continuous.py, conlang-h05):
      letters are stroke programs joined by drawn connectors whose
      slope/reach IS the vowel; horizontal; coda = POS underline
      under the final letter (provisional).
  E2  fused narrow character (fused_v3 N1 spine stack, generalized
      to 1-3 syllables): one narrow 64u-wide character per word,
      rows attached to a vertical spine; vowel = right-edge bar;
      coda = bottom radical.
  E3  syllable block with VOWEL AS STRUCTURE (the Hangul move, new):
      the vowel is the block's full-size structural bar — front
      vowels frame the right edge (vertical bar), back vowels the
      bottom (horizontal bar), central-low a is the corner L;
      mid-height doubles the bar. The onset letterform fills the
      remaining region; coda = bottom band radical; words stack.
      A vowel change re-frames the whole block: vowel ink cannot
      phase-vanish by construction.

Usage:
  python3 tools/engine_bakeoff.py sheet [--out PATH]
  python3 tools/engine_bakeoff.py para  [--outdir DIR]
  python3 tools/engine_bakeoff.py measure
"""

from __future__ import annotations

import itertools
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from fused_v3 import CW, NarrowRenderer, refit  # noqa: E402
from phonology import Syllable  # noqa: E402
from script import (  # noqa: E402
    BLOCK, ScriptRenderer, _line, raster_distance, rasterize)
from strokes import LETTERS, VOWEL_BRANCH, poly  # noqa: E402
from strokes_continuous import word as c_word, word_bounds  # noqa: E402

S = Syllable


# --- E0: boxed featural blocks (control) --------------------------------

class E0:
    tag, name = "E0", "boxed featural blocks (v0.2), vertical stack"

    def __init__(self):
        self.r = ScriptRenderer()

    def word(self, sylls, dx=0.0, dy=0.0, checks=True):
        """checks=False strips the register dot (measurement mode: the
        dot is a function of the syllable and would confound vowel-pair
        distances with free check-channel ink)."""
        parts = []
        for i, syl in enumerate(sylls):
            parts += self.r.syllable_block(
                syl, payload=not checks, dx=dx, dy=dy + i * BLOCK)
        return parts, BLOCK, BLOCK * len(sylls)

    def particle(self, syl, dx=0.0, dy=0.0):
        inner = self.r.syllable_block(syl)
        return (refit(inner, 0.7, dx, dy + 0.15 * BLOCK),
                BLOCK * 0.7, BLOCK * 0.7 + 0.15 * BLOCK)


# --- E1: continuous stroke chain ----------------------------------------

class E1:
    tag, name = "E1", "continuous stroke chain (h05): vowel = join"

    def word(self, sylls, dx=0.0, dy=0.0, checks=True):
        parts, w = c_word(sylls, dx=dx, dy=dy + 14)
        coda = sylls[-1].coda
        if coda:
            # POS underline under the final letter (provisional device;
            # precedented by the R-scheme underlines in rz_script)
            x1, x0 = dx + w - 18, dx + w - 52
            y = dy + 82
            parts.append(_line(x0, y, x1, y, w=4.2))
            if coda == "s":
                parts.append(_line(x0, y + 7, x1, y + 7, w=4.2))
            elif coda == "l":
                parts.append(_line(x1, y, x1, y - 8, w=4.2))
        return parts, w, 96
    particle = word


# --- E2: fused narrow character (N1 spine stack, 1-3 syllables) ---------

class E2:
    tag, name = "E2", "fused narrow character (N1 spine), one per word"

    def __init__(self):
        self.nr = NarrowRenderer()

    def word(self, sylls, dx=0.0, dy=0.0, checks=True):
        rows = len(sylls)
        coda = sylls[-1].coda
        top = dy + 3
        bot = top + rows * 47
        h = (bot - dy) + (14 if coda else 3)
        sx = dx + 8
        parts = [_line(sx, top + 1, sx, bot - 1, w=4.6)]
        for i, syl in enumerate(sylls):
            bare = S(syl.onset, syl.vowel, "")
            parts += self.nr._row(bare, sx + 4, top + i * 47 + 1,
                                  dx + CW - 2, top + (i + 1) * 47 - 1)
        if coda:
            # _pos draws at (its) dy + 100 - 7: shift so the radical
            # lands in this character's bottom band
            parts += self.nr._pos(coda, dx, dy + h - 100)
        return parts, CW, h
    particle = word


# --- E3: syllable block, vowel as structure (the Hangul move) -----------

BW = 64          # block width; open block is 64 tall, coda adds 14
BAR_W = 4.6


class E3:
    tag, name = "E3", "syllable block: vowel = structural bar (Hangul move)"

    def block(self, syl, dx=0.0, dy=0.0):
        f, side = VOWEL_BRANCH[syl.vowel]
        parts = []
        if side == -1:                     # front: vertical bar(s), right
            parts.append(_line(dx + 55, dy + 6, dx + 55, dy + 58, w=BAR_W))
            if f == 0.5:                   # mid height doubles the bar
                parts.append(_line(dx + 46, dy + 6, dx + 46, dy + 58,
                                   w=BAR_W))
            region = (dx + 3, dy + 4, dx + (39 if f == 0.5 else 48), dy + 60)
        elif side == +1:                   # back: horizontal bar(s), bottom
            parts.append(_line(dx + 6, dy + 55, dx + 58, dy + 55, w=BAR_W))
            if f == 0.5:
                parts.append(_line(dx + 6, dy + 46, dx + 58, dy + 46,
                                   w=BAR_W))
            region = (dx + 3, dy + 3, dx + 61, dy + (39 if f == 0.5 else 48))
        else:                              # a (central-low): corner L
            parts.append(_line(dx + 55, dy + 10, dx + 55, dy + 55, w=BAR_W))
            parts.append(_line(dx + 10, dy + 55, dx + 55, dy + 55, w=BAR_W))
            region = (dx + 3, dy + 3, dx + 46, dy + 46)
        rx0, ry0, rx1, ry1 = region
        s = min((rx1 - rx0) / 64, (ry1 - ry0) / 64)
        cx = rx0 + ((rx1 - rx0) - 60 * s) / 2
        cy = ry0 + ((ry1 - ry0) - 60 * s) / 2
        for path in LETTERS()[syl.onset]["paths"]:
            parts += poly([(cx + x * s, cy + y * s) for x, y in path],
                          w=BAR_W)
        h = 64.0
        if syl.coda:
            y0 = dy + 68
            x0, x1 = dx + 10, dx + 54
            if syl.coda == "n":
                parts.append(_line(x0, y0 + 6, x1, y0 + 6, w=BAR_W))
            elif syl.coda == "s":
                parts.append(_line(x0, y0 + 2, x1, y0 + 2, w=BAR_W))
                parts.append(_line(x0, y0 + 10, x1, y0 + 10, w=BAR_W))
            elif syl.coda == "l":
                parts.append(_line(x0, y0 + 6, x1 - 8, y0 + 6, w=BAR_W))
                parts.append(_line(x1 - 8, y0 + 6, x1 - 8, y0 - 2, w=BAR_W))
            h = 78.0
        return parts, h

    def word(self, sylls, dx=0.0, dy=0.0, checks=True):
        parts, y = [], dy
        for syl in sylls:
            bp, bh = self.block(syl, dx=dx, dy=y)
            parts += bp
            y += bh + 2
        return parts, BW, y - 2 - dy
    particle = word


ENGINES = [E0, E1, E2, E3]

# --- specimen ------------------------------------------------------------

WORDS = [("sala", [S("s", "a", ""), S("l", "a", "")]),
         ("sela", [S("s", "e", ""), S("l", "a", "")]),
         ("sila", [S("s", "i", ""), S("l", "a", "")]),
         ("sola", [S("s", "o", ""), S("l", "a", "")]),
         ("weto", [S("w", "e", ""), S("t", "o", "")]),
         ("piton", [S("p", "i", ""), S("t", "o", "n")]),
         ("lewas", [S("l", "e", ""), S("w", "a", "s")]),
         ("menokis", [S("m", "e", ""), S("n", "o", ""), S("k", "i", "s")])]

LEX = dict(WORDS + [
    ("salaan", [S("s", "a", ""), S("l", "a", "n")]),
    ("taako", [S("t", "a", ""), S("k", "o", "")]),
    ("namu", [S("n", "a", ""), S("m", "u", "")]),
    ("kimas", [S("k", "i", ""), S("m", "a", "s")]),
    ("wajone", [S("w", "a", ""), S("j", "o", ""), S("n", "e", "")]),
    ("ha", [S("h", "a", "")]), ("he", [S("h", "e", "")]),
    ("hi", [S("h", "i", "")]), ("ho", [S("h", "o", "")]),
    ("hu", [S("h", "u", "")]), ("han", [S("h", "a", "n")])])

PARA = ("ha weto salaan ho piton namu he lewas taako kimas ha wajone "
        "sela hu menokis sola he namu piton han sala weto hi taako "
        "lewas ha sela namu ho kimas salaan hu wajone he sala").split() * 3

# paragraph scale per engine: chosen so onset letterforms render at
# roughly equal apparent size (~12px) — the honest density comparison
# is words-per-page at equal letter legibility, not equal glyph height
PARA_SCALE = {"E0": 0.26, "E1": 0.26, "E2": 0.30, "E3": 0.30}
PAGE_W = 1180


def _is_particle(name):
    return name[0] == "h"


def word_parts(eng, name, dx=0.0, dy=0.0, checks=True):
    sylls = LEX[name]
    if _is_particle(name):
        return eng.particle(sylls[0], dx, dy) if eng.tag == "E0" \
            else eng.word(sylls, dx, dy)
    return eng.word(sylls, dx, dy, checks) if eng.tag == "E0" \
        else eng.word(sylls, dx, dy)


def _text(x, y, t, size=13, fill="#555"):
    return (f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" '
            f'font-family="monospace">{t}</text>')


def _svg(parts, w, h):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
            f'width="{w}" height="{h}" style="color:#1a1a1a">'
            f'<rect width="{w}" height="{h}" fill="white"/>'
            + "".join(parts) + "</svg>")


def sheet():
    parts, y = [], 44
    for cls in ENGINES:
        eng = cls()
        parts.append(_text(20, y - 24, f"{eng.tag}: {eng.name}"))
        # full-size specimen row (display scale per engine so rows are
        # comparable; ink weight rescales proportionally via refit)
        disp = {"E0": 0.62, "E1": 0.85, "E2": 0.95, "E3": 0.85}[eng.tag]
        x = 24
        for name, _ in WORDS:
            wp, ww, wh = word_parts(eng, name)
            parts += refit(wp, disp, x, y)
            parts.append(_text(x, y + wh * disp + 16, name, 11, "#999"))
            x += ww * disp + 30
        tall = max(word_parts(eng, n)[2] for n, _ in WORDS) * disp
        # reading-size running line
        sc = PARA_SCALE[eng.tag] * 0.85
        sx, small = 24, []
        strip_h = 0.0
        for name in PARA[:18]:
            wp, ww, wh = word_parts(eng, name)
            small += refit(wp, sc, sx, y + tall + 30)
            sx += (ww + 26) * sc
            strip_h = max(strip_h, wh * sc)
        parts += small
        y += tall + 30 + strip_h + 56
    return _svg(parts, 2050, y)


def para_pages():
    pages = {}
    for cls in ENGINES:
        eng = cls()
        sc = PARA_SCALE[eng.tag]
        parts = [_text(20, 26, f"{eng.tag}: {eng.name}", 14)]
        x, y = 24, 60
        line_h = 0.0
        n_lines = 1
        for name in PARA:
            wp, ww, wh = word_parts(eng, name)
            adv = (ww + 30) * sc
            # -44: word ink (tails, hooks) can overhang the nominal
            # advance; keep it clear of the page edge
            if x + adv > PAGE_W - 44:
                x = 24
                y += line_h + 14
                line_h = 0.0
                n_lines += 1
            parts += refit(wp, sc, x, y)
            x += adv
            line_h = max(line_h, wh * sc)
        total_h = y + line_h + 30
        area = PAGE_W * (total_h - 40)
        pages[eng.tag] = (_svg(parts, PAGE_W, total_h),
                          {"lines": n_lines, "height_px": round(total_h),
                           "area_per_word": round(area / len(PARA))})
    return pages


# --- measurement: same pair families for every engine -------------------

PHASES = [(px, py) for px in (0, 1.6, 3.2) for py in (0, 1.6, 3.2)]


def _window(eng):
    """Raster window + grid per engine, cell size ~= onset_size/6 so
    floors are comparable across engines with different glyph metrics."""
    return {
        "E0": ((-6, -6, 106, 206), 26),    # onset zone ~46u -> cell ~7.9
        "E1": ((-24, -30, 176, 126), 24),  # letters 48u -> cell ~7.5
        "E2": ((-4, -4, 68, 104), 14),     # row letters ~34u -> cell ~6.4
        "E3": ((-4, -4, 68, 136), 18),     # onset region ~36u -> cell ~6.2
    }[eng.tag]


def _pmin(eng, a, b):
    (x0, y0, x1, y1), n = _window(eng)
    return min(raster_distance(
        rasterize(a, x0 + px, y0 + py, x1 + px, y1 + py, n),
        rasterize(b, x0 + px, y0 + py, x1 + px, y1 + py, n))
        for px, py in PHASES)


ONSETS = ["s", "l", "t", "m", "p", "k", "n", "w", "c", "j"]


def measure():
    out = {}
    for cls in ENGINES:
        eng = cls()

        def render(sylls):
            return (eng.word(sylls, checks=False)[0] if eng.tag == "E0"
                    else eng.word(sylls)[0])

        vow, ons = [], []
        for v1, v2 in itertools.combinations("aeiou", 2):
            for pos in (0, 1):
                base = [S("s", "a", ""), S("l", "a", "")]
                other = [S("s", "a", ""), S("l", "a", "")]
                base[pos] = S(base[pos].onset, v1, "")
                other[pos] = S(other[pos].onset, v2, "")
                vow.append(_pmin(eng, render(base), render(other)))
        for o1, o2 in itertools.combinations(ONSETS, 2):
            for pos in (0, 1):
                base = [S("s", "a", ""), S("l", "a", "")]
                other = [S("s", "a", ""), S("l", "a", "")]
                base[pos] = S(o1, base[pos].vowel, "")
                other[pos] = S(o2, other[pos].vowel, "")
                ons.append(_pmin(eng, render(base), render(other)))
        vow.sort()
        ons.sort()
        out[eng.tag] = {
            "vowel_min": round(vow[0], 4),
            "vowel_median": round(vow[len(vow) // 2], 4),
            "onset_min": round(ons[0], 4),
            "onset_median": round(ons[len(ons) // 2], 4),
            "ratio": round(vow[len(vow) // 2] / ons[len(ons) // 2], 3)}
    return out


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
    if args and args[0] == "para":
        outdir = Path(args[args.index("--outdir") + 1]
                      if "--outdir" in args else ".")
        for tag, (svg_text, stats) in para_pages().items():
            p = outdir / f"para_{tag}.svg"
            p.write_text(svg_text)
            print(f"{tag}: {stats}  -> {p}")
        return 0
    if args and args[0] == "measure":
        res = measure()
        print(f"{'engine':<8}{'vowel min':>11}{'vowel med':>11}"
              f"{'onset min':>11}{'onset med':>11}{'ratio':>8}")
        for tag, r in res.items():
            print(f"{tag:<8}{r['vowel_min']:>11.4f}{r['vowel_median']:>11.4f}"
                  f"{r['onset_min']:>11.4f}{r['onset_median']:>11.4f}"
                  f"{r['ratio']:>8.3f}")
        return 0
    print(__doc__, file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
