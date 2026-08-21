#!/usr/bin/env python3
"""Joint optimization of the 100-point digit codebook (conlang-1f2).

digitgen.py optimizes the two channels separately and only audits
jointly. This does the real thing:

- **Syllable-level confusion**: conf((o1,r1),(o2,r2)) = onset-conf x
  rime-conf when both channels differ (the spec's multiplicative
  rule), single-channel conf otherwise. The cross terms (e.g. onset
  0.7 x rime 0.7 = 0.49) are exactly what per-channel optimization
  never sees.
- **Joint objective over VALUES**: syllable (o,r) encodes
  10*tens[o] + units[r]; maximize (min |v1-v2| over high-conf
  syllable pairs, sum conf*|v1-v2|), hill-climbing units and tens
  TOGETHER across the best rime subsets.
- **Non-product relaxation, priced**: free bijection of the same 100
  syllables to 0..99 (breaking value = 10*t+u decomposability).
  Reports the safety gain; the learnability price of a non-product
  codebook (100 rote pairs vs 10+10 digits) is the trade.
- **Acceptance proxy vs spoken English digits** [D, TODO-verify]:
  English's known worst pairs set the bar — five/nine (acoustic
  twins, numeric distance 4) and six/seven (shared onset, adjacent
  values). Bar transposed: the codebook must have NO pair with
  conf >= 0.7 at distance < 4, and no conf >= 0.3 pair at
  distance <= 1. Model-level stand-in; the human read-aloud test
  stays parked.

Deterministic (seeded). Runtime-capped to stay under ~4 minutes.
"""

import itertools
import json
import random
import sys
import time
from pathlib import Path

from digitgen import pair_weights, rime_conf, choose_rimes, HIGH

SPEC = Path(__file__).resolve().parent.parent / "docs" / "spec" / "channels.json"
T0 = time.monotonic()
BUDGET_S = 230


def syll_conf(s1, s2, oconf, rconf):
    (o1, r1), (o2, r2) = s1, s2
    if s1 == s2:
        return 0.0
    oc = oconf.get(frozenset((o1, o2)), 0.05) if o1 != o2 else None
    rc = rconf.get((r1, r2), rconf.get((r2, r1), 0.05)) \
        if r1 != r2 else None
    if oc is None:
        return rc
    if rc is None:
        return oc
    return oc * rc


def joint_pairs(onsets, rimes, oconf, rconf, floor=0.1):
    """Relevant syllable pairs (conf >= floor) over the product
    codebook, as (o1, r1, o2, r2, conf)."""
    sylls = [(o, r) for o in onsets for r in rimes]
    out = []
    for s1, s2 in itertools.combinations(sylls, 2):
        c = syll_conf(s1, s2, oconf, rconf)
        if c >= floor:
            out.append((s1, s2, c))
    return out


def joint_score(pairs, tens, units):
    mind, tot = 100, 0.0
    for (o1, r1), (o2, r2), c in pairs:
        d = abs((10 * tens[o1] + units[r1]) - (10 * tens[o2] + units[r2]))
        tot += c * d
        if c >= HIGH and d < mind:
            mind = d
    return (mind, round(tot, 4))


def joint_optimize(onsets, rimes, oconf, rconf, warm, seed=4711,
                   restarts=8):
    """Hill-climb units and tens together (swap moves in either map)."""
    pairs = joint_pairs(onsets, rimes, oconf, rconf)
    rng = random.Random(seed)
    best = None
    starts = [warm] + [None] * (restarts - 1)
    for st in starts:
        if time.monotonic() - T0 > BUDGET_S:
            break
        if st is None:
            du, dt = list(range(10)), list(range(10))
            rng.shuffle(du)
            rng.shuffle(dt)
            units = dict(zip(rimes, du))
            tens = dict(zip(onsets, dt))
        else:
            tens, units = dict(st[0]), dict(st[1])
        improved = True
        while improved:
            improved = False
            cur = joint_score(pairs, tens, units)
            move = None
            for m, keys in ((units, rimes), (tens, onsets)):
                for a, b in itertools.combinations(keys, 2):
                    m[a], m[b] = m[b], m[a]
                    sc = joint_score(pairs, tens, units)
                    if sc > cur:
                        cur, move = sc, (m, a, b)
                    m[a], m[b] = m[b], m[a]
            if move:
                m, a, b = move
                m[a], m[b] = m[b], m[a]
                improved = True
        sc = joint_score(pairs, tens, units)
        if best is None or sc > best[0]:
            best = (sc, dict(tens), dict(units))
    return best, pairs


def nonproduct_optimize(onsets, rimes, oconf, rconf, tens, units,
                        seed=99, sweeps=40):
    """Relax the product structure: free bijection syllables -> 0..99
    starting from the product solution; value-swap hill-climb."""
    pairs = joint_pairs(onsets, rimes, oconf, rconf)
    sylls = [(o, r) for o in onsets for r in rimes]
    val = {s: 10 * tens[s[0]] + units[s[1]] for s in sylls}

    def score():
        mind, tot = 100, 0.0
        for s1, s2, c in pairs:
            d = abs(val[s1] - val[s2])
            tot += c * d
            if c >= HIGH and d < mind:
                mind = d
        return (mind, round(tot, 4))

    rng = random.Random(seed)
    cur = score()
    for _ in range(sweeps):
        if time.monotonic() - T0 > BUDGET_S:
            break
        improved = False
        idx = list(itertools.combinations(range(100), 2))
        rng.shuffle(idx)
        for i, j in idx:
            a, b = sylls[i], sylls[j]
            val[a], val[b] = val[b], val[a]
            sc = score()
            if sc > cur:
                cur, improved = sc, True
            else:
                val[a], val[b] = val[b], val[a]
        if not improved:
            break
    return cur, val


def acceptance(pairs, tens, units):
    """English-digit bar [D, TODO-verify]: no pair conf>=0.7 at
    d<4 (five/nine bar); no pair conf>=0.3 at d<=1 (six/seven bar)."""
    viol = []
    for (o1, r1), (o2, r2), c in pairs:
        d = abs((10 * tens[o1] + units[r1]) - (10 * tens[o2] + units[r2]))
        if (c >= 0.7 and d < 4) or (c >= HIGH and d <= 1):
            viol.append(((o1, r1), (o2, r2), c, d))
    return viol


def fmt(s):
    (o, (v, c)) = s
    return f"{o}{v}{c}"


def main():
    spec = json.loads(SPEC.read_text())
    vowels = [v["roman"] for v in spec["vowels"]]
    codas = [c["roman"] for c in spec["codas"]]
    onsets = [o["roman"] for o in spec["onsets"]["content"]]
    vw, cw, ow = (pair_weights(spec, ch)
                  for ch in ("vowel", "coda", "onset"))
    oconf = {frozenset((a, b)): ow.get(frozenset((a, b)), 0.05)
             for a, b in itertools.combinations(onsets, 2)}

    # channel-wise v2 solution = warm start + comparison baseline
    rimes, rconf = choose_rimes(vowels, codas, vw, cw)
    from digitgen import assign_digits
    cur_tens = {o["roman"]: o["digit_tens"]
                for o in spec["onsets"]["content"]}
    cur_units = {(v["roman"], ""): v["digit_units_short"]
                 for v in spec["vowels"]}
    units_v2 = assign_digits(rimes, rconf, cur_units)
    oconf_pairs = {(a, b): ow.get(frozenset((a, b)), 0.05)
                   for a, b in itertools.combinations(onsets, 2)}
    tens_v2 = assign_digits(onsets, oconf_pairs, cur_tens)

    pairs = joint_pairs(onsets, rimes, oconf, rconf)
    v2_score = joint_score(pairs, tens_v2, units_v2)
    print(f"relevant syllable pairs (conf>=0.1): {len(pairs)} of 4950")
    print(f"v2 per-channel solution, JOINT score: min-dist {v2_score[0]}, "
          f"sum {v2_score[1]}")

    (jsc, tens_j, units_j), _ = joint_optimize(
        onsets, rimes, oconf, rconf, warm=(tens_v2, units_v2))
    print(f"joint-optimized (same structure):    min-dist {jsc[0]}, "
          f"sum {jsc[1]}")
    print("joint tens: ", "  ".join(
        f"{d}={o}" for o, d in sorted(tens_j.items(), key=lambda kv: kv[1])))
    print("joint units:", "  ".join(
        f"{d}={v}{c}" if c else f"{d}={v}"
        for (v, c), d in sorted(units_j.items(), key=lambda kv: kv[1])))

    viol = acceptance(pairs, tens_j, units_j)
    print(f"\nacceptance proxy (English-digit bar): "
          f"{len(viol)} violations")
    for s1, s2, c, d in viol[:8]:
        print(f"  {fmt(s1)}/{fmt(s2)} conf {c:.2f} at |dv|={d}")

    npsc, _ = nonproduct_optimize(onsets, rimes, oconf, rconf,
                                  tens_j, units_j)
    print(f"\nnon-product relaxation: min-dist {npsc[0]}, sum {npsc[1]}"
          f"  (vs product {jsc[0]}/{jsc[1]})")
    print("elapsed:", round(time.monotonic() - T0, 1), "s")
    return 0


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    sys.exit(main())
