#!/usr/bin/env python3
"""The compression dial on the E3 block substrate (GZ efficiency lane).

Edward's standing verdict on every transparent rendering: "still not
very efficient per se". Efficiency lives in the Zipf-tiered fusion
grammar (stroke-system.md §2), which no engine round ever exercised.
This tool builds the dial on the adopted E3 substrate — four
cumulative positions, each rule-derived (same word -> same form,
sound-out ladder intact):

  D0  transparent baseline (adopted E3 blocks, no compression)
  D1  + FRAME-ONLY PARTICLES: h is the only particle onset, so its
      letterform carries zero information within the class — drop
      it. A particle renders as its vowel frame + coda band alone,
      at 0.72 scale. (~37% of running tokens are particles.)
  D2  + VERTICAL SQUASH: multi-syllable content words squash each
      block to 0.75 height (anisotropic; hanzi-style). Buys line
      pitch; costs distinctness — the floors are re-measured and
      reported, not assumed.
  D3  + BRIEFS: high-frequency multi-syllable content words (corpus
      frequency >= BRIEF_FREQ) render as FIRST block + final coda
      band + a brief mark (double diagonal tick). POS survives via
      the coda; the rest is recovered lexically (steno-brief logic:
      fluency, not spelling). Collision policy across the full
      lexicon is future work and named in the round packet.

Usage:
  python3 tools/block_compress.py sheet [--out PATH]
  python3 tools/block_compress.py pages [--outdir DIR]
  python3 tools/block_compress.py stats
  python3 tools/block_compress.py floors     (D2 squash vs baseline)
"""

from __future__ import annotations

import math
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import xml.etree.ElementTree as ET  # noqa: E402

from engine_bakeoff import (  # noqa: E402
    E3, LEX, PARA, _geometry, _pmin, _svg, _text, onset_span, parts_bbox)
from fused_v3 import refit  # noqa: E402
from phonology import Syllable  # noqa: E402
from strokes_topology import median  # noqa: E402

S = Syllable
E = E3()

SQUASH = 0.75
PARTICLE_SCALE = 0.72
BRIEF_FREQ = 6
PAGE_W = 1180
WORD_GAP_PX = 10.0
PAGE_SCALE = 0.3376        # E3's density-normalized scale (onset ~12px)

FREQ = Counter(PARA)
# page metrics run on a longer text so line-count quantization does
# not swallow real layout gains (105 tokens -> only 3 lines)
PAGE_TEXT = PARA * 3
DIALS = ("D0", "D1", "D2", "D3")
ALL_MODES = DIALS + ("F",)


def squash_y(parts, k, y_top):
    """Anisotropic vertical squash about y_top (line elements only —
    the E3 substrate emits nothing else)."""
    out = []
    for el in ET.fromstring("<svg>" + "".join(parts) + "</svg>"):
        assert el.tag == "line", el.tag
        y1 = y_top + (float(el.get("y1")) - y_top) * k
        y2 = y_top + (float(el.get("y2")) - y_top) * k
        out.append(f'<line x1="{el.get("x1")}" y1="{y1:.2f}" '
                   f'x2="{el.get("x2")}" y2="{y2:.2f}" '
                   f'stroke="currentColor" '
                   f'stroke-width="{el.get("stroke-width")}" '
                   f'stroke-linecap="round"/>')
    return out


def _brief_mark(dx, dy):
    """Double diagonal tick: 'more follows, recover lexically'.
    Diagonal so it cannot be misread as a (horizontal) coda bar."""
    return [f'<line x1="{dx + 40}" y1="{dy + 12}" x2="{dx + 50}" '
            f'y2="{dy + 2}" stroke="currentColor" stroke-width="4.6" '
            f'stroke-linecap="round"/>',
            f'<line x1="{dx + 52}" y1="{dy + 12}" x2="{dx + 62}" '
            f'y2="{dy + 2}" stroke="currentColor" stroke-width="4.6" '
            f'stroke-linecap="round"/>']


def is_particle(name):
    return name[0] == "h"


def is_brief(name):
    return (not is_particle(name) and FREQ[name] >= BRIEF_FREQ
            and len(LEX[name]) >= 2)


PARTICLE_CELL = 46.0


def particle_mark(name, dx=0.0, dy=0.0):
    """Frame-only particle, r2 fixes (Edward, 2026-08-25): FULL stroke
    weight (the 0.72-scaled marks read 'not as bold' next to blocks),
    and centered on its own INK — the frame's position inside the old
    64u ghost box made marks sit 'on the right side of a blank
    square'."""
    syl = LEX[name][0]
    raw = E._frame(syl, 0, 0)[0]
    if syl.coda:
        raw += E.coda_band(syl.coda, 0, 64)
    x0, y0, x1, y1 = parts_bbox(raw)
    s = PARTICLE_SCALE
    ox = dx + (PARTICLE_CELL - (x1 - x0) * s) / 2 - x0 * s
    oy = dy + 12 + (52 - (y1 - y0) * s) / 2 - y0 * s
    return refit(raw, s, ox, oy, floor=4.6), PARTICLE_CELL, 64.0


def brief_glyph(name, dx=0.0, dy=0.0):
    """Brief, r2 fix: the tick sits fully BELOW the word's ink with
    clearance (it 'intersects a little weirdly' when a bottom-bar
    vowel put ink where the tick landed)."""
    sylls = LEX[name]
    parts, _ = E.block(S(sylls[0].onset, sylls[0].vowel, ""), dx, dy)
    coda = sylls[-1].coda
    if coda:
        parts += E.coda_band(coda, dx, dy + 66)
    bottom = parts_bbox(parts)[3]
    parts += _brief_mark(dx, bottom + 4)
    return parts, 64, bottom + 18 - dy


def word(name, dial, dx=0.0, dy=0.0):
    """Render one word at a dial position. Returns (parts, w, h)."""
    sylls = LEX[name]
    if dial == "F":
        return word_F(name, dx, dy)
    lvl = DIALS.index(dial)
    if lvl >= 1 and is_particle(name):
        return particle_mark(name, dx, dy)
    if lvl >= 3 and is_brief(name):
        return brief_glyph(name, dx, dy)
    parts, w, h = E.word(sylls, dx, dy)
    if lvl >= 2 and len(sylls) >= 2:
        parts = squash_y(parts, SQUASH, dy)
        h *= SQUASH
    return parts, w, h


# --- F-mode: fixed-size character cell ----------------------------------

CELL_H = 78.0        # 64u body + 14u coda/brief band — EVERY content
#                      word occupies exactly one 64x78 cell (the CJK
#                      ideal Edward keeps pointing at): 1-syll words
#                      fill it, n-syll words squash n blocks into the
#                      same 64u body, briefs are 1 block + band mark.
#                      Uniform cell -> uniform line pitch, which also
#                      answers the D0 complaint (inter-line gap vs
#                      intra-word gap ambiguity) and kills the 3-tall
#                      outliers that capped D3's space use.


def word_F(name, dx=0.0, dy=0.0):
    if is_particle(name):
        return particle_mark(name, dx, dy)
    sylls = LEX[name]
    if is_brief(name):
        parts, w, _ = brief_glyph(name, dx, dy)
        return parts, w, CELL_H
    coda = sylls[-1].coda
    bare = [S(s_.onset, s_.vowel, "") for s_ in sylls]
    parts, w, h = E.word(bare, dx, dy)
    if len(sylls) > 1 or h > 64:
        parts = squash_y(parts, 64.0 / h, dy)
    if coda:
        parts += E.coda_band(coda, dx, dy + 66)
    return parts, 64, CELL_H


def ink_length(parts):
    total = 0.0
    for el in ET.fromstring("<svg>" + "".join(parts) + "</svg>"):
        total += math.hypot(float(el.get("x2")) - float(el.get("x1")),
                            float(el.get("y2")) - float(el.get("y1")))
    return total


DIAL_DESC = {
    "D0": "transparent baseline (adopted E3 blocks)",
    "D1": "+ frame-only particles (h carries no info in its class)",
    "D2": "+ 0.75 vertical squash on multisyllable content words",
    "D3": "+ briefs: freq>=6 words as block1 + coda + tick",
    "F": "FIXED CELL 64x78: every content word is one character"}


def page(dial):
    parts = [_text(20, 26, f"{dial}: {DIAL_DESC[dial]}", 14)]
    x, y = 24, 60
    line_h, n_lines = 0.0, 1
    ink = 0.0
    for name in PAGE_TEXT:
        wp, ww, wh = word(name, dial)
        ink += ink_length(wp)
        adv = ww * PAGE_SCALE + WORD_GAP_PX
        if x + adv > PAGE_W - 44:
            x, y = 24, y + line_h + 12
            line_h, n_lines = 0.0, n_lines + 1
        parts += refit(wp, PAGE_SCALE, x, y)
        x += adv
        line_h = max(line_h, wh * PAGE_SCALE)
    total_h = y + line_h + 30
    stats = {"lines": n_lines, "height_px": round(total_h),
             "area_per_word": round(PAGE_W * (total_h - 40) / len(PAGE_TEXT)),
             "ink_u_per_word": round(ink / len(PAGE_TEXT), 1)}
    return _svg(parts, PAGE_W, total_h), stats


def stats():
    rows = {}
    base = None
    for dial in ALL_MODES:
        _, st = page(dial)
        if base is None:
            base = st
        st["area_vs_D0"] = f"{st['area_per_word'] / base['area_per_word']:.0%}"
        st["ink_vs_D0"] = f"{st['ink_u_per_word'] / base['ink_u_per_word']:.0%}"
        rows[dial] = st
    return rows


SAMPLE = ["ha", "ho", "han", "sala", "piton", "namu", "salaan", "menokis"]


def sheet():
    parts, y = [], 46
    for dial in ALL_MODES:
        parts.append(_text(20, y - 24, f"{dial}: {DIAL_DESC[dial]}"))
        x, tall = 24, 0.0
        for name in SAMPLE:
            wp, ww, wh = word(name, dial, dx=0, dy=0)
            parts += refit(wp, 0.85, x, y)
            parts.append(_text(x, y + wh * 0.85 + 14, name, 11, "#999"))
            x += max(ww * 0.85, 40) + 26
            tall = max(tall, wh * 0.85)
        # reading-size strip
        sx, small, strip_h = 24, [], 0.0
        for name in PARA[:20]:
            wp, ww, wh = word(name, dial)
            small += refit(wp, PAGE_SCALE, sx, y + tall + 28)
            sx += ww * PAGE_SCALE + WORD_GAP_PX
            strip_h = max(strip_h, wh * PAGE_SCALE)
        parts += small
        y += tall + 28 + strip_h + 54
    return _svg(parts, 1450, y)


def floors():
    """Does the D2 squash keep the reading-raster floors? Same pair
    families as the bake-off, squashed vs baseline disyllables."""
    import itertools
    span = onset_span(E) * SQUASH        # squashed letterforms are smaller
    win, n, phases = _geometry(E, span, 12)
    out = {}
    for tag, k in (("E3 baseline", 1.0), ("D2 squash", SQUASH),
                   ("F disyllable", 64.0 / 130.0)):
        def render(sylls, k=k):
            p = E.word(sylls)[0]
            return squash_y(p, k, 0.0) if k != 1.0 else p
        vow, ons = [], []
        for v1, v2 in itertools.combinations("aeiou", 2):
            for pos in (0, 1):
                a = [S("s", "a", ""), S("l", "a", "")]
                b = [S("s", "a", ""), S("l", "a", "")]
                a[pos] = S(a[pos].onset, v1, "")
                b[pos] = S(b[pos].onset, v2, "")
                vow.append(_pmin(win, n, phases, render(a), render(b)))
        for o1, o2 in itertools.combinations(
                ["s", "l", "t", "m", "p", "k", "n", "w", "c", "j"], 2):
            for pos in (0, 1):
                a = [S("s", "a", ""), S("l", "a", "")]
                b = [S("s", "a", ""), S("l", "a", "")]
                a[pos] = S(o1, a[pos].vowel, "")
                b[pos] = S(o2, b[pos].vowel, "")
                ons.append(_pmin(win, n, phases, render(a), render(b)))
        vow.sort()
        ons.sort()
        out[tag] = {"vowel_min": round(vow[0], 4),
                    "vowel_median": round(median(vow), 4),
                    "onset_min": round(ons[0], 4),
                    "onset_median": round(median(ons), 4)}
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
    if args and args[0] == "pages":
        outdir = Path(args[args.index("--outdir") + 1]
                      if "--outdir" in args else ".")
        for dial in ALL_MODES:
            svg_text, st = page(dial)
            p = outdir / f"page_{dial}.svg"
            p.write_text(svg_text)
            print(f"{dial}: {st}  -> {p}")
        return 0
    if args and args[0] == "stats":
        for dial, st in stats().items():
            print(dial, st)
        return 0
    if args and args[0] == "floors":
        for tag, r in floors().items():
            print(f"{tag}: {r}")
        return 0
    print(__doc__, file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
