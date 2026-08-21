#!/usr/bin/env python3
"""GZ x directional-cluster co-design: space arithmetic + motor audit.

Two computations feeding docs/design/gz-chord-fit.md:

1. **Exact-fit arithmetic** — GZ is greenfield, so its phonotactics
   can be DEFINED as the chord dimensions (onset<=36, nucleus 8,
   glide 3, coda 6). Raw syllable cells vs the GZ sketch's 2-3k
   target gives the humility-screen survival rate the chord space
   implies; compare against the measured ~40% survival from the
   width-ladder work.

2. **Digit motor audit** — the chord-layer analog of digitgen's
   acoustic confusion audit. Each digit's tens-onset occupies one
   index x middle cell (6 states/finger: null, N, E, S, W, press).
   A motor slip = one finger one ring-step off / press / null. The
   audit requires numerically close digits to be motor-DISTANT
   (same principle as the acoustic codebook: confusable -> far
   apart in value). Hill-climb assignment, naive vs optimized.

Usage: python3 tools/gz_chord_fit.py
"""

import itertools
import random

# --- 1. space arithmetic -------------------------------------------------

ONSETS = 36          # index x middle, incl. null-null = vowel-initial
NUCLEI = 8           # thumb: a e i o u ai au oi (9th state = command)
GLIDES = 3           # ring: none, i-glide, u-glide (x2 boundary flag)
CODAS = 6            # pinky: none n s r l m
GZ_TARGET = (2000, 3000)          # gz-sketch.md syllable-space target
MEASURED_SURVIVAL = 0.40          # width-ladder humility pass rate [M]


def arithmetic():
    raw = ONSETS * NUCLEI * GLIDES * CODAS
    lo, hi = GZ_TARGET
    return {
        "raw_cells": raw,
        "gz_target": GZ_TARGET,
        "implied_survival": (round(lo / raw, 2), round(hi / raw, 2)),
        "measured_survival_width_ladder": MEASURED_SURVIVAL,
        "survivors_at_measured_rate": int(raw * MEASURED_SURVIVAL),
    }


# --- 2. digit motor audit ------------------------------------------------

# per-finger states: 0=null 1=N 2=E 3=S 4=W 5=press
RING = {(1, 2), (2, 3), (3, 4), (4, 1)}


def fdist(a, b):
    """Per-finger motor confusability distance (0 = same state)."""
    if a == b:
        return 0
    lo, hi = min(a, b), max(a, b)
    if (lo, hi) in RING or (hi, lo) in RING:
        return 1                     # ring-adjacent direction slip
    if lo == 0 and hi == 5:
        return 2                     # null vs press: hard to confuse
    if lo == 0 or hi == 5:
        return 1                     # missed press / over-push
    return 2                         # opposite directions


def chord_dist(c1, c2):
    return fdist(c1[0], c2[0]) + fdist(c1[1], c2[1])


CELLS = [(i, m) for i in range(6) for m in range(6) if (i, m) != (0, 0)]
# (0,0) = null-null = vowel-initial syllables, not a digit onset


def audit(assign):
    """min chord distance over numerically-close digit pairs, plus the
    violation list (|a-b| in {1,2} but motor distance <= 1)."""
    worst, viols = 99, []
    for a, b in itertools.combinations(range(10), 2):
        nd = min(abs(a - b), 10 - abs(a - b))     # circular: 9~0 close
        if nd > 2:
            continue
        d = chord_dist(assign[a], assign[b])
        worst = min(worst, d)
        if d <= 1:
            viols.append((a, b, d))
    return worst, viols


def mean_close_dist(assign):
    ds = [chord_dist(assign[a], assign[b])
          for a, b in itertools.combinations(range(10), 2)
          if min(abs(a - b), 10 - abs(a - b)) <= 2]
    return sum(ds) / len(ds)


def optimize(restarts=300, seed=1729):
    rng = random.Random(seed)
    best = None
    for _ in range(restarts):
        cells = rng.sample(CELLS, 10)
        improved = True
        while improved:
            improved = False
            score = (audit(cells)[0], mean_close_dist(cells))
            for i in range(10):
                for cell in CELLS:
                    if cell in cells:
                        continue
                    trial = cells[:i] + [cell] + cells[i + 1:]
                    ts = (audit(trial)[0], mean_close_dist(trial))
                    if ts > score:
                        cells, score, improved = trial, ts, True
        if best is None or (audit(cells)[0], mean_close_dist(cells)) > \
                (audit(best)[0], mean_close_dist(best)):
            best = cells
    return best


def main():
    a = arithmetic()
    print("== exact-fit arithmetic ==")
    print(f"raw cells (36 x 8 x 3 x 6): {a['raw_cells']}")
    print(f"GZ sketch target: {a['gz_target']} -> implied humility "
          f"survival {a['implied_survival']}")
    print(f"measured width-ladder survival ~{a['measured_survival_width_ladder']:.0%} "
          f"-> {a['survivors_at_measured_rate']} survivors")

    print("\n== digit motor audit (tens onsets on index x middle) ==")
    naive = CELLS[:10]               # row-major fill, the lazy layout
    w, v = audit(naive)
    print(f"naive row-major: min close-pair motor distance {w}, "
          f"{len(v)} violations {v[:6]}")
    opt = optimize()
    w, v = audit(opt)
    print(f"optimized:       min close-pair motor distance {w}, "
          f"{len(v)} violations")
    print(f"  mean close-pair distance {mean_close_dist(opt):.2f}")
    names = {0: "null", 1: "N", 2: "E", 3: "S", 4: "W", 5: "press"}
    for d in range(10):
        i, m = opt[d]
        print(f"  digit {d}: index={names[i]:<5} middle={names[m]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
