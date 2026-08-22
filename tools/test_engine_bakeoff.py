"""Regression rails for the bake-off renderers (2026-08-22 review):
anchors must sit on ink (the connected-figure invariant the first
stroke draft silently broke for t/s/h), and every renderer's ink must
stay inside the bounds it reports."""

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from engine_bakeoff import ENGINES, LEX, parts_bbox, word_parts  # noqa: E402
from strokes import LETTERS, W  # noqa: E402


def _dist_to_segment(p, a, b):
    (px, py), (ax, ay), (bx, by) = p, a, b
    vx, vy = bx - ax, by - ay
    L2 = vx * vx + vy * vy
    t = 0.0 if L2 == 0 else max(0.0, min(1.0, ((px - ax) * vx +
                                               (py - ay) * vy) / L2))
    return math.hypot(px - (ax + t * vx), py - (ay + t * vy))


def test_anchors_on_ink():
    """Entry and exit anchors lie within a stroke half-width of some
    stroke of their letter — connectors attached there are connected."""
    for roman, spec in LETTERS().items():
        for kind in ("entry", "exit"):
            p = spec[kind]
            d = min(_dist_to_segment(p, path[i], path[i + 1])
                    for path in spec["paths"]
                    for i in range(len(path) - 1))
            assert d <= W / 2 + 0.01, (roman, kind, round(d, 2))


def test_ink_within_reported_bounds():
    """Each engine's word ink stays inside (or within a stated margin
    of) the width/height it reports — layout consumers rely on it."""
    # E1 is exempt on x/y: its tails/hooks deliberately overhang and
    # callers pad for it (para layout uses an explicit margin).
    for cls in ENGINES:
        eng = cls()
        if eng.tag == "E1":
            continue
        for name in LEX:
            wp, ww, wh = word_parts(eng, name)
            x0, y0, x1, y1 = parts_bbox(wp)
            assert x0 >= -3 and y0 >= -3, (eng.tag, name, x0, y0)
            assert x1 <= ww + 3, (eng.tag, name, x1, ww)
            assert y1 <= wh + 3, (eng.tag, name, y1, wh)
