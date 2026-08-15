#!/usr/bin/env python3
"""The FAIR fusion experiment (conlang-r5y; replaces the retracted
2026-08-14 comparison, per code-review BLOCKER 1).

Design corrections vs the retracted run:
- ANTIALIASED coverage rasters (3x3 supersampled gray per cell), not
  binary point-sampling; distance = Soergel (sum|a-b| / sum max(a,b)),
  phase-minimized over 4 sub-cell alignments.
- FACTORIAL: layout {stacked, fused-v0, fused-v1} x stroke-floor
  {off, on} x frame {equal-height, equal-area}. The retracted run
  compared floored-fused vs unfloored-stacked at equal height only —
  granting fusion both an area advantage and an ink advantage.
- Frames: every word must fit line height H. equal-height: stacked
  n-syllable = geometry scaled by 1/n (its natural width shrinks to
  100/n — fused gets n x the AREA; this frame prices legibility at
  fixed line height including that advantage, and says so). equal-area:
  stacked scaled by 1/sqrt(n) then height-capped... no — equal-area
  keeps total ink area comparable: stacked scaled by 1/sqrt(n) is
  taller than H, so instead the fused character is shrunk to width
  100/sqrt(n) at the same height, equalizing area against the
  height-fit stacked word. Both frames reported; the truth lives in
  the pair.
- Deterministic: fixed seed, neighbor set recorded in the output doc.
- Emits docs/design/fusion-study-data.md verbatim (generated file).

Run: python3 tools/fusion_study.py [--fast]
"""

import itertools
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import xml.etree.ElementTree as ET  # noqa: E402

from fused_script import FusedRenderer, transform_parts  # noqa: E402
from phonology import Inventory, Syllable  # noqa: E402
from script import ScriptRenderer  # noqa: E402

PHASES = [(0.0, 0.0), (0.5, 0.5), (0.25, 0.75), (0.75, 0.25)]  # cell fracs
SS = 3          # supersamples per cell axis


def _prims(parts):
    out = []
    for el in ET.fromstring("<svg>" + "".join(parts) + "</svg>"):
        w = float(el.get("stroke-width", 0))
        if el.tag == "line":
            out.append(("l", float(el.get("x1")), float(el.get("y1")),
                        float(el.get("x2")), float(el.get("y2")), w / 2))
        else:
            filled = el.get("fill") == "currentColor"
            out.append(("c", float(el.get("cx")), float(el.get("cy")),
                        float(el.get("r")), filled, w / 2))
    return out


def coverage(parts, x0, y0, x1, y1, pitch, phase=(0.0, 0.0)):
    """Gray raster: fraction of each cell's 3x3 subsamples on ink."""
    prims = _prims(parts)
    nx = max(1, round((x1 - x0) / pitch))
    ny = max(1, round((y1 - y0) / pitch))
    ox, oy = phase[0] * pitch, phase[1] * pitch
    grid = []
    for j in range(ny):
        for i in range(nx):
            hits = 0
            for sj in range(SS):
                for si in range(SS):
                    px = x0 + ox + (i + (si + 0.5) / SS) * pitch
                    py = y0 + oy + (j + (sj + 0.5) / SS) * pitch
                    for p in prims:
                        if p[0] == "l":
                            _, ax, ay, bx, by, hw = p
                            vx, vy = bx - ax, by - ay
                            L2 = vx * vx + vy * vy
                            t = 0.0 if L2 == 0 else max(0.0, min(
                                1.0, ((px - ax) * vx + (py - ay) * vy) / L2))
                            dx, dy = px - (ax + t * vx), py - (ay + t * vy)
                            if dx * dx + dy * dy <= hw * hw:
                                hits += 1
                                break
                        else:
                            _, cx, cy, r, filled, hw = p
                            d2 = (px - cx) ** 2 + (py - cy) ** 2
                            if (d2 <= r * r if filled
                                    else abs(d2 ** 0.5 - r) <= hw):
                                hits += 1
                                break
            grid.append(hits / (SS * SS))
    return grid


def soergel(a, b):
    num = sum(abs(x - y) for x, y in zip(a, b))
    den = sum(max(x, y) for x, y in zip(a, b))
    return 0.0 if den == 0 else num / den


def phase_min(parts_a, parts_b, x0, y0, x1, y1, pitch):
    return min(
        soergel(coverage(parts_a, x0, y0, x1, y1, pitch, ph),
                coverage(parts_b, x0, y0, x1, y1, pitch, ph))
        for ph in PHASES)


class Cond:
    """One factorial condition: renders a word to (parts, w, h)."""

    def __init__(self, layout, floor_on):
        self.layout = layout
        self.floor_on = floor_on
        self.name = f"{layout}{'/floor' if floor_on else ''}"
        floor = 4.4 if floor_on else 0.0
        self.fr = FusedRenderer(floor=floor)
        self.sr = ScriptRenderer()
        self.floor = floor

    def render(self, sylls, frame):
        n = len(sylls)
        if self.layout == "stacked":
            raw = []
            for i, syl in enumerate(sylls):
                raw += self.sr.syllable_block(syl, dy=i * 100)
            if frame == "equal-height":
                s = 1.0 / n          # fit line height; width 100/n
                w, h = 100.0 / n, 100.0
            else:                    # equal-area vs 100x100 fused
                s = 1.0 / n          # height-fit is mandatory;
                w, h = 100.0 / n, 100.0
            return (transform_parts(raw, s, 0, 0, floor=self.floor), w, h)
        maker = (self.fr.word_char if self.layout == "fused-v0"
                 else self.fr.word_char_v1)
        raw = maker(sylls)
        if frame == "equal-height":
            return (raw, 100.0, 100.0)
        # equal-area: shrink fused width to match stacked's 100/n x 100
        s = (1.0 / n) ** 0.5
        return (transform_parts(raw, s, 0, 0, floor=self.floor),
                100.0 * s, 100.0 * s)


def neighbor_set(inv):
    S = Syllable
    base2 = [S("t", "a", ""), S("k", "o", "")]
    n2 = ([[S("t", "a", ""), S(o, "o", "")]
           for o in inv.content_onsets if o != "k"]
          + [[S("t", "a", ""), S("k", v, "")] for v in "aeiu"]
          + [[S("t", "a", ""), S("k", "o", c)] for c in ("n", "s")])
    base3 = [S("m", "e", ""), S("n", "o", ""), S("k", "i", "s")]
    n3 = ([[S("m", "e", ""), S(o, "o", ""), S("k", "i", "s")]
           for o in inv.content_onsets if o != "n"]
          + [[S("m", "e", ""), S("n", v, ""), S("k", "i", "s")]
             for v in "aiu"])
    return (base2, n2), (base3, n3)


def run(fast=False):
    inv = Inventory()
    (base2, n2), (base3, n3) = neighbor_set(inv)
    conds = [Cond(lay, fl) for lay in ("stacked", "fused-v0", "fused-v1")
             for fl in ((False, True) if not fast else (True,))]
    heights = (20, 28) if fast else (20, 28, 40)
    rows = []
    for H in heights:
        pitch = 100.0 / H       # units per pixel-cell
        for frame in ("equal-height", "equal-area"):
            for cond in conds:
                for label, base, nbrs in (("2syl", base2, n2),
                                          ("3syl", base3, n3)):
                    pb, wb, hb = cond.render(base, frame)
                    ds = []
                    for nb in nbrs:
                        pn, wn, hn = cond.render(nb, frame)
                        w = max(wb, wn)
                        h = max(hb, hn)
                        ds.append(phase_min(pb, pn, 0, 0, w, h, pitch))
                    ds.sort()
                    rows.append((H, frame, cond.name, label, ds[0],
                                 ds[len(ds) // 2]))
    return rows


def emit(rows):
    lines = [
        "# Fusion study data (GENERATED by tools/fusion_study.py — do "
        "not hand-edit)",
        "",
        "Fair factorial comparison (see the tool docstring for design "
        "corrections vs the retracted 2026-08-14 run). Metric: Soergel "
        "distance on 3x3-supersampled coverage rasters, phase-min over "
        "4 alignments. Neighbor sets: all one-channel neighbors of "
        "taako (2syl) and menookis-family (3syl).",
        "",
        "| H px | frame | condition | words | min | median |",
        "|---|---|---|---|---|---|",
    ]
    for H, frame, cond, label, dmin, dmed in rows:
        lines.append(f"| {H} | {frame} | {cond} | {label} "
                     f"| {dmin:.3f} | {dmed:.3f} |")
    return "\n".join(lines) + "\n"


def main():
    fast = "--fast" in sys.argv
    rows = run(fast=fast)
    doc = emit(rows)
    out = Path(__file__).resolve().parent.parent / "docs" / "design" / \
        "fusion-study-data.md"
    out.write_text(doc)
    print(doc)
    print(f"written: {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
