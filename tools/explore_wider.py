#!/usr/bin/env python3
"""Width ladder: greenfield variants wider than GF-W (conlang-4h1).

Computes real capacities (lexgen on programmatically widened specs,
humility machinery applied to every added contrast) for the rungs:

  GF-N   narrow baseline          10 onsets x 5 nuclei
  GF-ND  narrow + diphthongs      10 x 8   (ai au oi)
  GF-W   wide onsets              16 x 5   (+ b d g f z r)
  GF-X   wider onsets             19 x 5   (+ v sh dj)
  GF-WD  wide + diphthongs        16 x 8
  GF-XD  wider + diphthongs       19 x 8
  GF-C   + stop-liquid clusters   31 onset units x 8

Multi-char roman tokens (sh, dj, ai, pl...) are safe here: the
conflict-graph path treats channel values as opaque strings and never
calls parse_word. Check bits for added phonemes are PROVISIONAL.

Honesty notes printed with results:
- exact MIS for small graphs; greedy+swap lower bound above the size
  threshold (labeled ">=").
- GF-C monosyllable MIS ignores cluster epenthesis (pla ~ pVla): with
  licensed epenthesis the conflict lands on DISYLLABLE space
  (shadowing), not the monosyllable count, but cross-length modeling
  is future work; treat GF-C rows as upper bounds in that respect.
"""

import copy
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lexgen  # noqa: E402
import phonology  # noqa: E402

SPEC = Path(__file__).resolve().parent.parent / "docs" / "spec" / "channels.json"

WIDE6 = [("b", 1), ("d", 0), ("g", 1), ("f", 1), ("z", 1), ("r", 1)]
WIDE6_COV = [["p", "b"], ["t", "d"], ["k", "g"], ["f", "p"],
             ["z", "s"], ["r", "l"], ["b", "w"], ["d", "n"], ["g", "k"]]

# GF-X additions. sh requires tightening c's licensed realizations to
# [tʃ]~[ts] strictly (the spec note already treats [ʃ] as unlicensed
# drift); dj sits between c, j and z; v between w, b, f.
X3 = [("v", 0), ("sh", 0), ("dj", 1)]
X3_COV = [["v", "w"], ["v", "b"], ["v", "f"],
          ["sh", "s"], ["sh", "c"],
          ["dj", "c"], ["dj", "j"], ["dj", "z"], ["dj", "d"]]

# Diphthong nuclei: near-universal (most L1s have ai/au-like sequences
# or transparent a+i composition). Covered against their common
# monophthongizations and each other.
DIPH = [("ai", 1), ("au", 0), ("oi", 1)]
DIPH_COV = [["ai", "a"], ["ai", "e"], ["au", "o"], ["au", "a"],
            ["oi", "o"], ["oi", "e"], ["ai", "oi"]]

# Stop/f + liquid clusters (tl, dl excluded: cross-linguistically
# awkward). Covered: cluster-reduction to the base (many L1s drop the
# liquid), liquid-swap (r/l cohort), voicing partner.
CLUSTERS = [("pl", 0), ("pr", 1), ("tr", 0), ("kl", 1), ("kr", 0),
            ("bl", 1), ("br", 0), ("dr", 1), ("gl", 0), ("gr", 1),
            ("fl", 0), ("fr", 1)]
CLUSTER_COV = (
    [[c, c[0]] for c, _ in CLUSTERS]                     # reduction
    + [["pl", "pr"], ["bl", "br"], ["kl", "kr"],
       ["gl", "gr"], ["fl", "fr"]]                       # liquid swap
    + [["pl", "bl"], ["pr", "br"], ["tr", "dr"],
       ["kl", "gl"], ["kr", "gr"]]                       # voicing
)


def widen(spec, onsets=(), onset_cov=(), nuclei=(), nucleus_cov=()):
    w = copy.deepcopy(spec)
    idx = len(w["onsets"]["content"])
    for i, (roman, chk) in enumerate(onsets):
        w["onsets"]["content"].append(
            {"roman": roman, "index": idx + i, "check": chk,
             "digit_tens": None, "provisional": True})
    vidx = len(w["vowels"])
    for i, (roman, chk) in enumerate(nuclei):
        w["vowels"].append(
            {"roman": roman, "index": vidx + i, "check": chk,
             "digit_units_short": None, "provisional": True})
    for channel, pairs in (("onset", onset_cov), ("vowel", nucleus_cov)):
        cov = w["covered_confusion_pairs"].setdefault(channel, [])
        cov += [list(p) for p in pairs]
        w["covered_confusion_pairs"][channel] = [
            list(p) for p in sorted({tuple(sorted(p)) for p in cov})]
    return w


def greedy_mis(bodies, edges, restarts=5000, seed=4711):
    """Multi-start randomized greedy + saturation fill: lower bound."""
    import random
    rng = random.Random(seed)
    best = []
    for r in range(restarts):
        order = sorted(bodies,
                       key=lambda b: (len(edges[b]), rng.random()))
        chosen, blocked = set(), set()
        for b in order:
            if b not in blocked:
                chosen.add(b)
                blocked.add(b)
                blocked |= edges[b]
        if len(chosen) > len(best):
            best = sorted(chosen)
    return best


def measure(name, spec, exact_limit=50):
    inv = phonology.Inventory(spec)
    rules = phonology.ConflictRules(inv)
    bodies, edges = lexgen.body_conflict_graph(inv, rules, "adopted")
    n_on = len(spec["onsets"]["content"])
    n_nu = len(spec["vowels"])
    syl = n_on * n_nu * 4
    if len(bodies) <= exact_limit:
        mis = lexgen.max_independent_set(bodies, edges)
        tag = ""
    else:
        mis = greedy_mis(bodies, edges)
        tag = ">="
    print(f"{name:6s} {n_on:3d} onsets x {n_nu} nuclei = {syl:5d} "
          f"content syllables; {len(bodies):3d} bodies; "
          f"adopted-MIS {tag}{len(mis)} monosyllabic roots", flush=True)
    return mis


def main():
    base = json.loads(SPEC.read_text())
    ladder = [
        ("GF-N", widen(base)),
        ("GF-ND", widen(base, nuclei=DIPH, nucleus_cov=DIPH_COV)),
        ("GF-W", widen(base, WIDE6, WIDE6_COV)),
        ("GF-X", widen(base, WIDE6 + X3, WIDE6_COV + X3_COV)),
        ("GF-WD", widen(base, WIDE6, WIDE6_COV, DIPH, DIPH_COV)),
        ("GF-XD", widen(base, WIDE6 + X3, WIDE6_COV + X3_COV,
                        DIPH, DIPH_COV)),
        ("GF-C", widen(base, WIDE6 + X3 + CLUSTERS,
                       WIDE6_COV + X3_COV + CLUSTER_COV,
                       DIPH, DIPH_COV)),
    ]
    results = {}
    for name, spec in ladder:
        results[name] = measure(name, spec)
    print("\nGF-XD MIS bodies:",
          " ".join(sorted(f"{o}{v}" for o, v in results["GF-XD"])))
    return 0


if __name__ == "__main__":
    sys.exit(main())
