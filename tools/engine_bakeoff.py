#!/usr/bin/env python3
"""GZ script-engine bake-off on GZ-shaped text (conlang-e35).

Four genuinely different engines render the SAME specimen (words +
a running paragraph with particles and codas), so the fork the
program charter left open — which rendering engine carries the GZ
script — can be judged side by side:

  E0  boxed featural blocks (v0.2 script.py): syllable blocks
      stacked vertically; vowel = carrier tick; coda = strip mark.
      The incumbent. Measured in TWO modes: full renderer (with the
      register check dot) and vowel-channel-isolated (dot stripped),
      because the dot is a function of the whole syllable and can
      mask or fake vowel-channel distance.
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

Comparability discipline (2026-08-22 review): raster windows are
SQUARE with square cells; grid resolution is derived from each
engine's MEASURED median onset-ink span (cell = span/6) rather than
hand-picked; phase offsets are thirds of the actual cell pitch; and
paragraph scales are computed from the same measured spans so every
engine renders onsets at the same pixel size, with a fixed pixel
inter-word gap.

Usage:
  python3 tools/engine_bakeoff.py sheet [--out PATH]
  python3 tools/engine_bakeoff.py para  [--outdir DIR]
  python3 tools/engine_bakeoff.py measure
"""

from __future__ import annotations

import itertools
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from fused_v3 import CW, NarrowRenderer, refit  # noqa: E402
from phonology import Syllable  # noqa: E402
from script import (  # noqa: E402
    BLOCK, ScriptRenderer, _line, raster_distance, rasterize)
from strokes import LETTERS, VOWEL_BRANCH, poly  # noqa: E402
from strokes_continuous import word as c_word  # noqa: E402
from strokes_topology import median  # noqa: E402

S = Syllable


# --- E0: boxed featural blocks (control) --------------------------------

class E0:
    tag, name = "E0", "boxed featural blocks (v0.2), vertical stack"

    def __init__(self):
        self.r = ScriptRenderer()

    def word(self, sylls, dx=0.0, dy=0.0, checks=True):
        """checks=False strips the register dot (vowel-channel
        isolation mode: the dot is a function of the whole syllable —
        it adds distance to some vowel pairs that the vowel INK does
        not provide, and none to others)."""
        parts = []
        for i, syl in enumerate(sylls):
            parts += self.r.syllable_block(
                syl, payload=not checks, dx=dx, dy=dy + i * BLOCK)
        return parts, BLOCK, BLOCK * len(sylls)

    def particle(self, syl, dx=0.0, dy=0.0):
        inner = self.r.syllable_block(syl)
        return (refit(inner, 0.7, dx, dy + 0.15 * BLOCK),
                BLOCK * 0.7, BLOCK * 0.7 + 0.15 * BLOCK)

    def onset_ink(self, roman):
        return self.r._onset(roman)


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

    def onset_ink(self, roman):
        parts = []
        for path in LETTERS()[roman]["paths"]:
            parts += poly(path)
        return parts


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

    def onset_ink(self, roman):
        # a row in the standard 2-row cell geometry, vowel ink off
        return self.nr._row(S(roman, "a", ""), 12, 4, 12 + CW - 14, 50,
                            vowel_ink=False)


# --- E3: syllable block, vowel as structure (the Hangul move) -----------

BW = 64          # block width; open block is 64 tall, coda adds a band
BAR_W = 4.6


class E3:
    tag, name = "E3", "syllable block: vowel = structural bar (Hangul move)"

    def _frame(self, syl, dx, dy):
        """The vowel's structural bar(s) + the onset region they leave."""
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
        return parts, region

    def _onset_into(self, roman, region):
        rx0, ry0, rx1, ry1 = region
        s = min((rx1 - rx0) / 64, (ry1 - ry0) / 64)
        cx = rx0 + ((rx1 - rx0) - 60 * s) / 2
        cy = ry0 + ((ry1 - ry0) - 60 * s) / 2
        parts = []
        for path in LETTERS()[roman]["paths"]:
            parts += poly([(cx + x * s, cy + y * s) for x, y in path],
                          w=BAR_W)
        return parts

    def block(self, syl, dx=0.0, dy=0.0):
        parts, region = self._frame(syl, dx, dy)
        parts += self._onset_into(syl.onset, region)
        h = 64.0
        if syl.coda:
            # coda band fully inside the returned height (review
            # finding: the first draft's s-bars overran it)
            y0 = dy + 66
            x0, x1 = dx + 10, dx + 54
            if syl.coda == "n":
                parts.append(_line(x0, y0 + 7, x1, y0 + 7, w=BAR_W))
            elif syl.coda == "s":
                parts.append(_line(x0, y0 + 3, x1, y0 + 3, w=BAR_W))
                parts.append(_line(x0, y0 + 11, x1, y0 + 11, w=BAR_W))
            elif syl.coda == "l":
                parts.append(_line(x0, y0 + 7, x1 - 8, y0 + 7, w=BAR_W))
                parts.append(_line(x1 - 8, y0 + 7, x1 - 8, y0 - 1, w=BAR_W))
            h = 82.0
        return parts, h

    def word(self, sylls, dx=0.0, dy=0.0, checks=True):
        parts, y = [], dy
        for syl in sylls:
            bp, bh = self.block(syl, dx=dx, dy=y)
            parts += bp
            y += bh + 2
        return parts, BW, y - 2 - dy
    particle = word

    def onset_ink(self, roman):
        # one variant per vowel frame (the region the onset gets
        # depends on the vowel) — spans are measured per variant, not
        # on the inflating union of all five
        return [self._onset_into(roman, self._frame(
                    S(roman, v, ""), 0, 0)[1]) for v in "aeiou"]


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

PAGE_W = 1180
TARGET_ONSET_PX = 12.0     # every engine renders onsets at this size
WORD_GAP_PX = 10.0         # fixed pixel inter-word gap on the page


def parts_bbox(parts):
    xs, ys = [], []
    for el in ET.fromstring("<svg>" + "".join(parts) + "</svg>"):
        w = float(el.get("stroke-width", 0)) / 2
        if el.tag == "line":
            for k in ("x1", "x2"):
                xs += [float(el.get(k)) - w, float(el.get(k)) + w]
            for k in ("y1", "y2"):
                ys += [float(el.get(k)) - w, float(el.get(k)) + w]
        elif el.tag == "circle":
            cx, cy, r = (float(el.get(k)) for k in ("cx", "cy", "r"))
            xs += [cx - r - w, cx + r + w]
            ys += [cy - r - w, cy + r + w]
    return min(xs), min(ys), max(xs), max(ys)


ONSETS = ["s", "l", "t", "m", "p", "k", "n", "w", "c", "j"]


def onset_span(eng):
    """Median over content onsets (and per-vowel variants, where the
    onset's rendered size depends on the vowel) of the onset-ink bbox
    max dimension, engine units — the normalizer for scales and
    raster cells."""
    spans = []
    for o in ONSETS:
        ink = eng.onset_ink(o)
        variants = ink if ink and isinstance(ink[0], list) else [ink]
        for v in variants:
            b = parts_bbox(v)
            spans.append(max(b[2] - b[0], b[3] - b[1]))
    return median(sorted(spans))


def para_scales():
    return {cls.tag: TARGET_ONSET_PX / onset_span(cls()) for cls in ENGINES}


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
    ps = para_scales()
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
        # reading-size running line at the normalized paragraph scale
        sc = ps[eng.tag] * 0.85
        sx, small = 24, []
        strip_h = 0.0
        for name in PARA[:18]:
            wp, ww, wh = word_parts(eng, name)
            small += refit(wp, sc, sx, y + tall + 30)
            sx += ww * sc + WORD_GAP_PX
            strip_h = max(strip_h, wh * sc)
        parts += small
        y += tall + 30 + strip_h + 56
    return _svg(parts, 2050, y)


def para_pages():
    ps = para_scales()
    pages = {}
    for cls in ENGINES:
        eng = cls()
        sc = ps[eng.tag]
        parts = [_text(20, 26, f"{eng.tag}: {eng.name}  "
                               f"(onset scale {sc:.3f})", 14)]
        x, y = 24, 60
        line_h = 0.0
        n_lines = 1
        for name in PARA:
            wp, ww, wh = word_parts(eng, name)
            adv = ww * sc + WORD_GAP_PX
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

def _geometry(eng, span, cells_per_span):
    """Square raster window + grid + phase set for one engine. Cell =
    measured onset span / cells_per_span, cells square, phases thirds
    of the actual cell pitch (review finding: the first draft's
    rectangular windows gave per-engine, per-axis cell sizes differing
    up to ~2x). cells_per_span=12 is the READING raster (stroke ~ one
    cell, ~12px onsets); 6 is the EXTREME raster (~6px onsets), where
    sub-cell strokes mostly vanish and only gross structure survives —
    a fragility probe, too degenerate to rank engines by on its own."""
    win = {"E0": (-8, -8, 208, 208),
           "E1": (-25, -45, 195, 175),
           "E2": (-26, -6, 90, 110),
           "E3": (-38, -5, 102, 135)}[eng.tag]
    size = win[2] - win[0]
    assert size == win[3] - win[1], eng.tag
    n = max(10, round(size / (span / cells_per_span)))
    c = size / n
    phases = [(px, py) for px in (0, c / 3, 2 * c / 3)
              for py in (0, c / 3, 2 * c / 3)]
    return win, n, phases


def _pmin(win, n, phases, a, b):
    x0, y0, x1, y1 = win
    return min(raster_distance(
        rasterize(a, x0 + px, y0 + py, x1 + px, y1 + py, n),
        rasterize(b, x0 + px, y0 + py, x1 + px, y1 + py, n))
        for px, py in phases)


def measure(cells_per_span=12):
    """Floors per engine; E0 in both modes (full renderer / vowel
    channel isolated). Also returns the actual near-zero pair lists —
    doc claims are written from these, not from aggregates."""
    out = {}
    for cls in ENGINES:
        eng = cls()
        span = onset_span(eng)
        win, n, phases = _geometry(eng, span, cells_per_span)
        modes = ([("E0", False), ("E0+dot", True)] if eng.tag == "E0"
                 else [(eng.tag, None)])
        for label, checks in modes:

            def render(sylls):
                if eng.tag == "E0":
                    return eng.word(sylls, checks=checks)[0]
                return eng.word(sylls)[0]

            vow, ons = [], []
            zeros = {"vowel": [], "onset": []}
            for v1, v2 in itertools.combinations("aeiou", 2):
                for pos in (0, 1):
                    base = [S("s", "a", ""), S("l", "a", "")]
                    other = [S("s", "a", ""), S("l", "a", "")]
                    base[pos] = S(base[pos].onset, v1, "")
                    other[pos] = S(other[pos].onset, v2, "")
                    d = _pmin(win, n, phases, render(base), render(other))
                    vow.append(d)
                    if d < 0.02:
                        zeros["vowel"].append(f"{v1}/{v2}@{pos}")
            for o1, o2 in itertools.combinations(ONSETS, 2):
                for pos in (0, 1):
                    base = [S("s", "a", ""), S("l", "a", "")]
                    other = [S("s", "a", ""), S("l", "a", "")]
                    base[pos] = S(o1, base[pos].vowel, "")
                    other[pos] = S(o2, other[pos].vowel, "")
                    d = _pmin(win, n, phases, render(base), render(other))
                    ons.append(d)
                    if d < 0.02:
                        zeros["onset"].append(f"{o1}/{o2}@{pos}")
            vow.sort()
            ons.sort()
            out[label] = {
                "vowel_min": round(vow[0], 4),
                "vowel_median": round(median(vow), 4),
                "vowel_zero_pairs": len([d for d in vow if d < 1e-9]),
                "onset_min": round(ons[0], 4),
                "onset_median": round(median(ons), 4),
                "ratio": round(median(vow) / median(ons), 3),
                "near_zeros": zeros,
                "grid": f"n={n} cell={size_str(win, n)}u span={span:.1f}u"}
    return out


def size_str(win, n):
    return f"{(win[2] - win[0]) / n:.1f}"


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
        for tag, sc in sorted(para_scales().items()):
            print(f"{tag} scale {sc:.4f} (onset -> {TARGET_ONSET_PX}px)")
        for tag, (svg_text, stats) in para_pages().items():
            p = outdir / f"para_{tag}.svg"
            p.write_text(svg_text)
            print(f"{tag}: {stats}  -> {p}")
        return 0
    if args and args[0] == "measure":
        for cps, label in ((12, "READING raster (stroke ~ 1 cell, "
                                "~12px onsets) — the primary table"),
                           (6, "EXTREME raster (~6px onsets) — "
                               "fragility probe, secondary")):
            res = measure(cps)
            print(f"\n== {label} ==")
            print(f"{'engine':<12}{'vowel min':>10}{'vowel med':>10}"
                  f"{'v-zeros':>8}{'onset min':>10}{'onset med':>10}"
                  f"{'ratio':>7}   grid")
            for tag, r in res.items():
                print(f"{tag:<12}{r['vowel_min']:>10.4f}"
                      f"{r['vowel_median']:>10.4f}"
                      f"{r['vowel_zero_pairs']:>8}"
                      f"{r['onset_min']:>10.4f}{r['onset_median']:>10.4f}"
                      f"{r['ratio']:>7.3f}   {r['grid']}")
            print("near-zero pairs (<0.02):")
            for tag, r in res.items():
                z = r["near_zeros"]
                print(f"  {tag}  vowel: {', '.join(z['vowel']) or '—'}")
                print(f"       onset: {', '.join(z['onset']) or '—'}")
        return 0
    print(__doc__, file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
