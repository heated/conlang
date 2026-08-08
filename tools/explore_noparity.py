#!/usr/bin/env python3
"""Exploration experiment (conlang-zec): does the check-bit register earn
its keep, or can the core lexicon run on natural-grade emergent
redundancy (phonotactics + SSM templates + sparse assignment + repair)?

Compares two architectures over matched lexicons:

  A  (current spec): register = confusion-weighted check bit. Lexicon
     assignment may use "covered" minimal pairs (register differs, so a
     register-sensitive listener detects the substitution).
  B  (no-parity): no register channel at all. Assignment policy treats
     high-confusion pairs (covered + forbidden) as conflicts for
     monosyllable assignment — the "humility" policy — and relies on
     lexical-gap detection, templates, context, and repair.

Error model: single-channel substitutions with class-dependent relative
probabilities (high-confusion pairs likelier than distinct ones), applied
to Zipf-weighted word tokens. Listener models:
  sensitive — perceives vowel length (register); in A, a substitution
              that flips the check bit is detected even if the segmental
              result is another word's body.
  deaf      — cannot perceive length; register information contributes
              nothing in either architecture.

Metric: silent-substitution rate = P(corrupted percept is another legal
word, undetected) over the error distribution, per listener, per
architecture, split by mono/disyllables. Detection channels tallied:
  parity   (A + sensitive only), lexgap (percept is not a word),
  none     (silent substitution).

Run: python3 tools/explore_noparity.py [--json PATH]
"""

from __future__ import annotations

import json
import random
import sys
from itertools import combinations
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lexgen import max_independent_set  # noqa: E402
from phonology import ConflictRules, Inventory, Syllable  # noqa: E402

# relative substitution likelihood by pair class (not absolute rates;
# only ratios matter for comparing architectures)
import os
W_HIGH = float(os.environ.get("W_HIGH", 10.0))  # covered + forbidden pairs
W_LOW = 1.0     # weighted + unlisted same-channel pairs

ZIPF_S = 1.0    # Zipf exponent for word-frequency weighting
N_DISYLL = 1000
SEED = 7


def pair_class_tables(inv: Inventory):
    spec = inv.spec
    cov = {ch: {frozenset(p) for p in prs}
           for ch, prs in spec["covered_confusion_pairs"].items()
           if ch != "comment"}
    forb = {ch: {frozenset(p) for p in prs}
            for ch, prs in spec["confusion_policy"]["forbidden"].items()
            if ch != "comment"}

    def weight(channel: str, a: str, b: str) -> float:
        pair = frozenset((a, b))
        if pair in cov.get(channel, set()) or pair in forb.get(channel, set()):
            return W_HIGH
        return W_LOW

    return weight, cov, forb


def check_bits(inv: Inventory):
    ob = {o["roman"]: o["check"]
          for o in inv.spec["onsets"]["content"] + inv.spec["onsets"]["particle"]}
    vb = {v["roman"]: v["check"] for v in inv.spec["vowels"]}
    cb = {c["roman"]: c["check"] for c in inv.spec["codas"]}
    return ob, vb, cb


def build_body_graph(inv, rules, conflict_level: str):
    """Monosyllable body conflict graph.
    conflict_level 'spec'    — forbidden pairs only (architecture A's rule)
    conflict_level 'humility'— forbidden + covered pairs (architecture B)"""
    weight, cov, forb = pair_class_tables(inv)
    bodies = [(o, v) for o in inv.content_onsets for v in inv.vowels
              if (o, v) not in inv.glide_cells]
    edges = {b: set() for b in bodies}
    for a, b in combinations(bodies, 2):
        if (a[0] == b[0]) == (a[1] == b[1]):
            continue  # need exactly one differing channel
        channel = "onset" if a[0] != b[0] else "vowel"
        pair = frozenset((a[0], b[0])) if channel == "onset" \
            else frozenset((a[1], b[1]))
        conflicted = pair in forb.get(channel, set())
        if conflict_level == "humility":
            conflicted = conflicted or pair in cov.get(channel, set())
        # coronal-i applies in both
        if channel == "onset" and a[1] == "i" \
                and pair in ({frozenset(("t", "c")), frozenset(("s", "c"))}):
            conflicted = True
        if conflicted:
            edges[a].add(b)
            edges[b].add(a)
    return bodies, edges


def assign_lexicon(inv, rules, arch: str, rng: random.Random):
    """Return a list of words (tuples of Syllable), most-frequent first.
    Monosyllables: MIS of the architecture's body graph (nouns, coda ∅).
    Disyllables: sampled, avoiding glide cells, fake geminates, and any
    single-substitution neighbor already in the lexicon (both
    architectures can afford this — the space is huge)."""
    level = "spec" if arch == "A" else "humility"
    bodies, edges = build_body_graph(inv, rules, level)
    mis = max_independent_set(bodies, edges)
    words = [(Syllable(o, v, ""),) for (o, v) in sorted(mis)]

    firsts = [s for s in inv.lexical_content_syllables()
              if (s.onset, s.vowel) not in inv.glide_cells]
    finals = [Syllable(o, v, "") for o in inv.content_onsets
              for v in inv.vowels if (o, v) not in inv.glide_cells]
    taken = set(words)

    def neighbors(word):
        out = []
        for i, syl in enumerate(word):
            for o in inv.content_onsets:
                if o != syl.onset:
                    out.append(word[:i] + (Syllable(o, syl.vowel, syl.coda),)
                               + word[i + 1:])
            for v in inv.vowels:
                if v != syl.vowel:
                    out.append(word[:i] + (Syllable(syl.onset, v, syl.coda),)
                               + word[i + 1:])
            for c in inv.codas:
                if c != syl.coda:
                    out.append(word[:i] + (Syllable(syl.onset, syl.vowel, c),)
                               + word[i + 1:])
        return out

    attempts = 0
    while sum(1 for w in taken if len(w) == 2) < N_DISYLL and attempts < 200000:
        attempts += 1
        s1, s2 = rng.choice(firsts), rng.choice(finals)
        if s1.coda and s1.coda == s2.onset:      # fake geminate
            continue
        w = (s1, s2)
        if w in taken:
            continue
        if any(n in taken for n in neighbors(w)):
            continue  # keep distance 2 among disyllables — space is cheap
        taken.add(w)
        words.append(w)
    return words


def simulate(inv, rules, words, arch: str, listener: str):
    """Expected detection outcomes over Zipf-weighted words and
    class-weighted single-channel substitutions."""
    weight, _, _ = pair_class_tables(inv)
    ob, vb, cb = check_bits(inv)
    lexicon = set(words)
    freq = [1.0 / (rank + 1) ** ZIPF_S for rank in range(len(words))]
    ftot = sum(freq)

    tallies = {"parity": 0.0, "lexgap": 0.0, "silent": 0.0}
    for word, f in zip(words, freq):
        subs = []
        for i, syl in enumerate(word):
            for channel, values, bits in (("onset", inv.content_onsets, ob),
                                          ("vowel", inv.vowels, vb),
                                          ("coda", inv.codas, cb)):
                cur = getattr(syl, channel)
                for new in values:
                    if new == cur:
                        continue
                    kw = {"onset": syl.onset, "vowel": syl.vowel,
                          "coda": syl.coda}
                    kw[channel] = new
                    corrupted = word[:i] + (Syllable(**kw),) + word[i + 1:]
                    w = weight(channel, cur, new)
                    flips = bits[cur] != bits[new]
                    subs.append((corrupted, w, flips))
        wtot = sum(w for _, w, _ in subs)
        for corrupted, w, flips in subs:
            p = (f / ftot) * (w / wtot)
            if arch == "A" and listener == "sensitive" and flips:
                # percept keeps the original duration; check fails audibly
                tallies["parity"] += p
            elif corrupted in lexicon:
                tallies["silent"] += p
            else:
                tallies["lexgap"] += p
    return tallies


def main() -> int:
    rng = random.Random(SEED)
    inv = Inventory()
    rules = ConflictRules(inv)
    report = {}
    lexicons = {arch: assign_lexicon(inv, rules, arch, rng)
                for arch in ("A", "B")}
    # concept-matched comparison: truncate both to the same concept count
    # so every frequency rank carries identical Zipf mass in both
    # architectures; B's higher ranks are simply longer words.
    total = min(len(w) for w in lexicons.values())
    for arch in ("A", "B"):
        words = lexicons[arch][:total]
        monos = sum(1 for w in words if len(w) == 1)
        report[f"{arch}_monosyllables"] = monos
        report[f"{arch}_disyllables"] = len(words) - monos
        for listener in ("sensitive", "deaf"):
            t = simulate(inv, rules, words, arch, listener)
            key = f"{arch}_{listener}"
            report[key] = {k: round(v, 5) for k, v in t.items()}
    report["concepts"] = total
    print(json.dumps(report, indent=2))
    if "--json" in sys.argv:
        out = sys.argv[sys.argv.index("--json") + 1]
        Path(out).write_text(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
