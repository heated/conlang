#!/usr/bin/env python3
"""Digit codebook v2 generator (conlang-bd3, Edward's revised scheme).

Tens digit -> onset (audited: confusable pairs get numerically distant
values). Units digit -> 10 of the 20 rimes (vowel x coda), chosen for
maximal perceptual spacing. Codebook = 100 syllables sparse in the
200-content space (h-row excluded: it delimits). Replaces the
anti-parity-complement register trick.

Confusion model [D]: pair weights from the spec's own confusion data —
forbidden 1.0, covered 0.7, weighted 0.35, same-channel-unlisted 0.05;
rimes differing in both channels multiply. This is a design model, not
measured perception; the human acceptance test (confusion rate <=
spoken English digits) is parked with all human testing.

Deterministic: exhaustive rime-subset search (C(20,10)=184,756);
seeded multi-restart hill-climb for digit-value assignment.
"""

import itertools
import json
import random
import sys
from pathlib import Path

SPEC = Path(__file__).resolve().parent.parent / "docs" / "spec" / "channels.json"
HIGH = 0.3  # threshold: pairs that must get numeric distance


def pair_weights(spec, channel):
    w = {}
    for p in spec["confusion_policy"]["forbidden"].get(channel, []):
        w[frozenset(p)] = 1.0
    for p in spec["covered_confusion_pairs"].get(channel, []):
        w.setdefault(frozenset(p), 0.7)
    for p in spec["confusion_policy"]["weighted"].get(channel, []):
        w.setdefault(frozenset(p), 0.35)
    return w


def rime_conf(r1, r2, vw, cw):
    (v1, c1), (v2, c2) = r1, r2
    if (v1, c1) == (v2, c2):
        return 0.0
    dv = vw.get(frozenset((v1, v2)), 0.05) if v1 != v2 else None
    dc = cw.get(frozenset((c1, c2)), 0.05) if c1 != c2 else None
    if dv is None:
        return dc
    if dc is None:
        return dv
    return dv * dc


def choose_rimes(vowels, codas, vw, cw):
    """Exhaustive: the 10-subset minimizing (high-pair count, total conf),
    tie-breaking toward bare vowels (continuity with hu-mi examples)."""
    rimes = [(v, c) for v in vowels for c in codas]
    conf = {(a, b): rime_conf(a, b, vw, cw)
            for a, b in itertools.combinations(rimes, 2)}
    best = None
    for sub in itertools.combinations(rimes, 10):
        high = tot = 0
        for a, b in itertools.combinations(sub, 2):
            c = conf[(a, b)]
            tot += c
            if c >= HIGH:
                high += 1
        bare = sum(1 for (v, c) in sub if c == "")
        key = (high, round(tot, 6), -bare)
        if best is None or key < best[0]:
            best = (key, sub)
    return list(best[1]), conf


def assign_digits(items, conf, prior, seed=4711, restarts=500):
    """Map 10 items -> digits 0-9. Maximize (min numeric distance over
    high-conf pairs, sum conf*dist), tie-break toward `prior` map."""
    rng = random.Random(seed)
    pairs = [(a, b, c) for (a, b), c in conf.items() if c >= 0.1
             and a in items and b in items]
    high_pairs = [(a, b) for a, b, c in pairs if c >= HIGH]

    def score(m):
        mind = min((abs(m[a] - m[b]) for a, b in high_pairs), default=9)
        s = sum(c * abs(m[a] - m[b]) for a, b, c in pairs)
        keep = sum(1 for it in items if prior.get(it) == m[it])
        return (mind, round(s, 6), keep)

    best = None
    for r in range(restarts):
        digits = list(range(10))
        rng.shuffle(digits)
        m = dict(zip(items, digits))
        improved = True
        while improved:
            improved = False
            # steepest-ascent over pairwise digit swaps
            cur = score(m)
            move = None
            for i, j in itertools.combinations(items, 2):
                m[i], m[j] = m[j], m[i]
                sc = score(m)
                if sc > cur:
                    cur, move = sc, (i, j)
                m[i], m[j] = m[j], m[i]
            if move:
                i, j = move
                m[i], m[j] = m[j], m[i]
                improved = True
        if best is None or score(m) > score(best):
            best = dict(m)
    return best


def main():
    spec = json.loads(SPEC.read_text())
    vowels = [v["roman"] for v in spec["vowels"]]
    codas = [c["roman"] for c in spec["codas"]]
    onsets = [o["roman"] for o in spec["onsets"]["content"]]
    cur_tens = {o["roman"]: o["digit_tens"] for o in spec["onsets"]["content"]}
    cur_units = {(v["roman"], ""): v["digit_units_short"]
                 for v in spec["vowels"]}

    vw = pair_weights(spec, "vowel")
    cw = pair_weights(spec, "coda")
    ow = pair_weights(spec, "onset")

    rimes, rconf = choose_rimes(vowels, codas, vw, cw)
    print("chosen rimes:",
          " ".join(f"{v}{c}" if c else v for v, c in rimes))
    units = assign_digits(rimes, rconf, cur_units)
    oconf = {(a, b): ow.get(frozenset((a, b)), 0.05)
             for a, b in itertools.combinations(onsets, 2)}
    tens = assign_digits(onsets, oconf, cur_tens)

    print("\nunits:", "  ".join(
        f"{d}={v}{c}" if c else f"{d}={v}"
        for (v, c), d in sorted(units.items(), key=lambda kv: kv[1])))
    print("tens: ", "  ".join(
        f"{d}={o}" for o, d in sorted(tens.items(), key=lambda kv: kv[1])))

    print("\naudit — high-confusion pairs and their numeric distances:")
    for (a, b), c in sorted(rconf.items(), key=lambda kv: -kv[1]):
        if c >= HIGH and a in units and b in units:
            fa = f"{a[0]}{a[1]}" if a[1] else a[0]
            fb = f"{b[0]}{b[1]}" if b[1] else b[0]
            print(f"  rime {fa}/{fb} conf {c:.2f} -> "
                  f"|{units[a]}-{units[b]}| = {abs(units[a]-units[b])}")
    for (a, b), c in sorted(oconf.items(), key=lambda kv: -kv[1]):
        if c >= HIGH:
            print(f"  onset {a}/{b} conf {c:.2f} -> "
                  f"|{tens[a]}-{tens[b]}| = {abs(tens[a]-tens[b])}")
    changed_t = [o for o in onsets if tens[o] != cur_tens.get(o)]
    print(f"\ntens changed vs current spec: {len(changed_t)}/10 "
          f"({' '.join(changed_t)})")

    # reserved residue-100 syllable: unused rime minimizing worst-case
    # confusion with the codebook rimes, on the least-confusable onset
    unused = [r for r in [(v, c) for v in vowels for c in codas]
              if r not in units]
    def worst(r):
        return max(rconf.get((r, q), rconf.get((q, r), 0)) for q in units)
    r100_rime = min(unused, key=lambda r: (worst(r),
                    sum(rconf.get((r, q), rconf.get((q, r), 0))
                        for q in units)))
    onset_load = {o: sum(c for (a, b), c in oconf.items()
                         if c >= HIGH and o in (a, b)) for o in onsets}
    r100_onset = min(onsets, key=lambda o: onset_load[o])
    v, c = r100_rime
    print(f"reserved residue-100 syllable: {r100_onset}{v}{c} "
          f"(worst rime-conf to codebook {worst(r100_rime):.2f})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
