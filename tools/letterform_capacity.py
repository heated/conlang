#!/usr/bin/env python3
"""How many letterforms does the featural grammar actually support?

width-ladder.md: the wide greenfield (GF-W, 16-19 onsets) "forces the
script letter-inventory question, which is exactly what blocks the
parked stroke work". GF-N's 11 letters come from 5 bases x 4
modifiers with most cells unimplemented. Two questions nobody has
answered with numbers:

1. **How far does base x modifier scale before letters collide?**
   Implement every plausible cell, measure all pairs at reading size,
   and find the largest inventory that clears the greenfield's own
   0.15 phase-min floor (the v0.2 letter floor).
2. **Which extension axis is cheapest** — more bases (new shapes) or
   more modifiers (new marks on known shapes)? The learnability
   answer and the legibility answer may differ, and the featural bet
   says modifiers should be cheaper to LEARN while bases should be
   safer to READ. This measures the reading half.

Method: the same occupancy-raster machinery as every other floor
(tools/script.py), phase-minimized over 9 sub-cell alignments, at
14px per letter box — the v0.2 letter-floor condition.

Usage: python3 tools/letterform_capacity.py [--json]
"""

from __future__ import annotations

import itertools
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from script import _circle, _line, rasterize, raster_distance  # noqa: E402

CX, CY, CR = 33, 34, 20
VX, ZY0, ZY1 = 33, 14, 56
FLOOR = 0.15                      # the v0.2 letter floor
WIN = (2, 2, 68, 66)
PHASES = [(px, py) for px in (0, 1.6, 3.2) for py in (0, 1.6, 3.2)]

# Bases: the 5 shipped + 3 candidate extensions for the wide inventory.
BASES = ["circle", "vertical", "diagonal", "angle", "tick",
         "arc", "chevron", "box"]
# Modifiers: the 4 shipped + 2 candidates.
MODS = ["plain", "crossed", "doubled", "capped", "dotted", "hooked"]

# Cells the geometry cannot realize robustly (ink collides with its
# own base, or the mark has nowhere to land).
BANNED = {("circle", "doubled"), ("angle", "capped"),
          ("box", "doubled"), ("box", "capped"), ("box", "crossed"),
          ("tick", "capped"), ("tick", "crossed"),
          ("arc", "doubled"), ("chevron", "capped")}


def base_parts(base):
    L = _line
    if base == "circle":
        return [_circle(CX, CY, CR)]
    if base == "vertical":
        return [L(VX, ZY0, VX, ZY1)]
    if base == "diagonal":
        return [L(14, ZY1, 52, 14)]
    if base == "angle":
        return [L(14, 14, 52, 14), L(14, 14, 14, ZY1)]
    if base == "tick":
        return [L(22, 34, 44, 34)]
    if base == "arc":                 # open right half-ring
        return [_line(20, 16, 46, 30), _line(46, 30, 46, 40),
                _line(46, 40, 20, 54)]
    if base == "chevron":             # v shape
        return [L(14, 16, 33, 52), L(33, 52, 52, 16)]
    if base == "box":                 # closed rectangle
        return [L(14, 16, 52, 16), L(52, 16, 52, 52),
                L(52, 52, 14, 52), L(14, 52, 14, 16)]
    raise ValueError(base)


def cell_parts(base, mod):
    """A (base, modifier) letterform. Modifier realizations are
    deliberately uniform across bases — that IS the featural bet."""
    parts = list(base_parts(base))
    L = _line
    if mod == "plain":
        return parts
    if mod == "crossed":
        if base == "circle":
            parts.append(L(18, 49, 48, 19))
        elif base == "vertical":
            parts.append(L(18, 35, 48, 35))
        elif base == "diagonal":
            parts.append(L(14, 14, 52, ZY1))
        elif base == "angle":
            parts.append(L(14, 34, 40, 34))
        elif base == "chevron":
            parts.append(L(16, 30, 50, 30))
        elif base == "arc":
            parts.append(L(20, 35, 46, 35))
        return parts
    if mod == "doubled":
        if base == "circle":
            parts.append(_circle(CX, CY, CR - 8))
        elif base == "vertical":
            parts = [L(24, ZY0, 24, ZY1), L(44, ZY0, 44, ZY1)]
        elif base == "diagonal":
            parts = [L(8, ZY1, 46, 14), L(26, ZY1, 64, 14)]
        elif base == "angle":
            parts += [L(30, 30, 52, 30), L(30, 30, 30, ZY1)]
        elif base == "tick":
            parts.append(L(22, 44, 44, 44))
        elif base == "chevron":
            parts.append(L(22, 16, 33, 38))
        return parts
    if mod == "capped":
        if base == "circle":
            parts += [L(8, 11, 58, 11), L(8, 11, 8, 20),
                      L(58, 11, 58, 20)]
        elif base == "vertical":
            parts.append(L(16, ZY0, 50, ZY0))
        elif base == "diagonal":
            parts.append(L(14, 10, 52, 10))
        elif base == "arc":
            parts.append(L(16, 12, 50, 12))
        return parts
    if mod == "dotted":               # a filled dot inside/above
        cy = 26 if base in ("circle", "box") else 12
        parts.append(_circle(CX, cy, 4.5, fill="currentColor"))
        return parts
    if mod == "hooked":               # terminal hook on the base's foot
        if base in ("vertical", "diagonal", "tick"):
            parts.append(L(VX, ZY1, VX + 16, ZY1 - 12))
        elif base == "circle":
            parts.append(L(CX + CR - 2, CY + 12, CX + CR + 12, CY + 20))
        elif base == "angle":
            parts.append(L(14, ZY1, 30, ZY1 - 12))
        elif base == "chevron":
            parts.append(L(52, 16, 62, 28))
        elif base == "arc":
            parts.append(L(20, 54, 34, 60))
        elif base == "box":
            parts.append(L(52, 52, 62, 62))
        return parts
    raise ValueError(mod)


def cells(bases, mods):
    return [(b, m) for b in bases for m in mods
            if (b, m) not in BANNED]


def pmin(a, b, n=14):
    return min(raster_distance(
        rasterize(a, WIN[0] + px, WIN[1] + py, WIN[2] + px, WIN[3] + py, n),
        rasterize(b, WIN[0] + px, WIN[1] + py, WIN[2] + px, WIN[3] + py, n))
        for px, py in PHASES)


def greedy_safe_set(cs, floor=FLOOR):
    """Largest inventory we can certify: greedily add cells that keep
    every pair above the floor (order = most-distinct-first)."""
    glyphs = {c: cell_parts(*c) for c in cs}
    d = {}
    for a, b in itertools.combinations(cs, 2):
        d[(a, b)] = d[(b, a)] = pmin(glyphs[a], glyphs[b])
    # order by each cell's mean distance to the rest (robust first)
    order = sorted(cs, key=lambda c: -sum(d[(c, o)] for o in cs if o != c))
    keep = []
    for c in order:
        if all(d[(c, k)] >= floor for k in keep):
            keep.append(c)
    worst = min((d[(a, b)] for a, b in itertools.combinations(keep, 2)),
                default=1.0)
    return keep, worst, d


def report():
    shipped_b = BASES[:5]
    shipped_m = MODS[:4]
    out = {"floor": FLOOR, "raster_px": 14}

    scenarios = {
        "shipped grid (5 bases x 4 mods)": (shipped_b, shipped_m),
        "+2 modifiers (5 x 6)": (shipped_b, MODS),
        "+3 bases (8 x 4)": (BASES, shipped_m),
        "full candidate grid (8 x 6)": (BASES, MODS),
    }
    for name, (bs, ms) in scenarios.items():
        cs = cells(bs, ms)
        keep, worst, d = greedy_safe_set(cs)
        pairs = list(itertools.combinations(cs, 2))
        below = sum(1 for a, b in pairs if d[(a, b)] < FLOOR)
        out[name] = {
            "implemented_cells": len(cs),
            "certified_letters": len(keep),
            "worst_pair_in_set": round(worst, 4),
            "pairs_below_floor_in_full_grid": below,
            "pct_pairs_below_floor": round(100 * below / len(pairs), 1),
        }
    # which axis is cheaper, measured: mean distance for pairs that
    # differ only in base vs only in modifier
    cs = cells(BASES, MODS)
    glyphs = {c: cell_parts(*c) for c in cs}
    same_mod, same_base = [], []
    for a, b in itertools.combinations(cs, 2):
        dd = pmin(glyphs[a], glyphs[b])
        if a[1] == b[1]:
            same_mod.append(dd)
        elif a[0] == b[0]:
            same_base.append(dd)
    out["axis_comparison"] = {
        "differ_in_base_only_mean": round(sum(same_mod) / len(same_mod), 4),
        "differ_in_base_only_min": round(min(same_mod), 4),
        "differ_in_modifier_only_mean": round(
            sum(same_base) / len(same_base), 4),
        "differ_in_modifier_only_min": round(min(same_base), 4),
        "n_base_pairs": len(same_mod), "n_mod_pairs": len(same_base),
    }
    return out


def main():
    out = report()
    if "--json" in sys.argv:
        print(json.dumps(out, indent=2))
        return 0
    print(f"letterform capacity @ {out['raster_px']}px, "
          f"floor {out['floor']}\n")
    print(f"{'scenario':<32}{'cells':>7}{'certified':>11}"
          f"{'worst':>9}{'%pairs<floor':>14}")
    for k, v in out.items():
        if not isinstance(v, dict) or "certified_letters" not in v:
            continue
        print(f"{k:<32}{v['implemented_cells']:>7}"
              f"{v['certified_letters']:>11}{v['worst_pair_in_set']:>9.3f}"
              f"{v['pct_pairs_below_floor']:>13.1f}%")
    a = out["axis_comparison"]
    print(f"\nextension axis (full grid):")
    print(f"  differ in BASE only     mean {a['differ_in_base_only_mean']:.3f}"
          f"  min {a['differ_in_base_only_min']:.3f}  "
          f"(n={a['n_base_pairs']})")
    print(f"  differ in MODIFIER only mean "
          f"{a['differ_in_modifier_only_mean']:.3f}"
          f"  min {a['differ_in_modifier_only_min']:.3f}  "
          f"(n={a['n_mod_pairs']})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
