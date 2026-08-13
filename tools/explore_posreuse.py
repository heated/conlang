#!/usr/bin/env python3
"""Price the cross-POS reuse rung of the capacity ledger (conlang-sss).

The claim under test (Edward, 2026-08-09): "syntax exemption plus
disciplined context partitioning gets you into the 80-120 range
without touching the phonology."

Structure of the claim: the POS coda is an outer code — a coda
mishearing yields a wrong-POS wordform, which the syntactic slot
rejects with probability q (the context catch rate). If that catch is
reliable, the same (onset,vowel) body can carry UNRELATED meanings in
different POS lanes: 22 humility-safe bodies x 3 active POS = 66
roots, and partial semantic-domain partitioning stacks further.

This simulation prices the NEW silent-error class that reuse creates:
a coda mishearing + an unchecked slot silently substitutes a word
from another lane. Monte Carlo over uttered wordforms with
per-channel confusion rates; outputs silent-substitution rates per
10k words for baseline vs POS-reuse across q values, next to the
pre-existing onset/vowel residual (the ground-truth metric the
project already uses).

Run: python3 tools/explore_posreuse.py
"""

import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from phonology import ConflictRules, Inventory, Syllable  # noqa: E402

# per-channel mishearing rates toward a confusable neighbor (same
# ballpark as the no-parity study's sensitive-listener condition)
E_ONSET, E_VOWEL, E_CODA = 0.010, 0.006, 0.015
# coda confusions: the high-confusion set (∅/n weighted heavily,
# n/s covered, ∅/s moderate)
CODA_CONFUSIONS = {
    "": [("n", 0.6), ("s", 0.4)],
    "n": [("", 0.5), ("s", 0.5)],
    "s": [("", 0.4), ("n", 0.6)],
}
ONSET_NEIGHBORS = {
    "c": "s", "s": "c", "m": "n", "n": "m", "p": "t", "t": "p",
    "k": "t", "l": "n", "w": "l", "j": "l",
}
VOWEL_NEIGHBORS = {"a": "e", "e": "a", "i": "e", "o": "u", "u": "o"}
POS_CODAS = ("", "n", "s")     # noun, verb, modifier


def build_vocab(inv, rules, reuse):
    """Meaning tables. reuse=False: one meaning per body (all three
    POS forms belong to it). reuse=True: three independent meanings
    per body, one per POS lane."""
    import lexgen
    bodies, edges = lexgen.body_conflict_graph(inv, rules, "adopted")
    mis = lexgen.max_independent_set(bodies, edges)
    vocab = {}                  # (onset, vowel, coda) -> meaning id
    for i, (o, v) in enumerate(mis):
        for j, c in enumerate(POS_CODAS):
            mid = (i, 0) if not reuse else (i, j)
            vocab[(o, v, c)] = mid
    return mis, vocab


def perturb(word, rng):
    o, v, c = word
    if rng.random() < E_ONSET:
        o = ONSET_NEIGHBORS.get(o, o)
    if rng.random() < E_VOWEL:
        v = VOWEL_NEIGHBORS[v]
    if rng.random() < E_CODA:
        opts = CODA_CONFUSIONS[c]
        r = rng.random()
        acc = 0.0
        for cand, p in opts:
            acc += p
            if r <= acc:
                c = cand
                break
    return (o, v, c)


def run(trials=400_000, seed=11):
    inv = Inventory()
    rules = ConflictRules(inv)
    rng = random.Random(seed)
    results = {}
    for reuse in (False, True):
        mis, vocab = build_vocab(inv, rules, reuse)
        words = list(vocab)
        for q in (0.80, 0.90, 0.95, 0.99):
            silent = caught = harmless = 0
            for _ in range(trials):
                w = rng.choice(words)
                heard = perturb(w, rng)
                if heard == w:
                    continue
                if heard not in vocab:
                    caught += 1          # non-word: repair
                    continue
                if vocab[heard] == vocab[w]:
                    harmless += 1        # same meaning (same-root form)
                    continue
                # different meaning. POS flip? syntax checks with prob q
                if heard[2] != w[2] and rng.random() < q:
                    caught += 1
                else:
                    silent += 1
            results[(reuse, q)] = (silent / trials * 1e4,
                                   caught / trials * 1e4,
                                   harmless / trials * 1e4,
                                   len(set(vocab.values())))
    return results


def main():
    res = run()
    print("rates per 10k uttered words "
          "(silent substitutions / caught / harmless):")
    print(f"{'mode':16s} {'q':>5s} {'roots':>6s} {'silent':>8s} "
          f"{'caught':>8s} {'harmless':>9s}")
    for (reuse, q), (s, c, h, n) in sorted(res.items()):
        mode = "POS-reuse x3" if reuse else "baseline"
        print(f"{mode:16s} {q:5.2f} {n:6d} {s:8.2f} {c:8.2f} {h:9.2f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
