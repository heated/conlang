#!/usr/bin/env python3
"""Exploration experiment v2 (conlang-zec): what does the register buy,
under which lexicon-assignment policy, for whom?

v1 was reviewed adversarially (Codex + Fable) and found confounded: it
varied the register and the assignment policy together, omitted the
compromise architecture, and simulated a lexicon with no morphology —
excluding the same-root POS minimal pairs (∅/n/s final codas) that no
assignment policy can avoid and that the register's covered pairs
partially protect. v2 fixes all of that.

Architectures (assignment policy × register):
  A       spec assignment (covered minimal pairs licensed) + register
  Aprime  humility assignment (covered pairs refused)      + register
  B       humility assignment                              + no register

Lexicon: root bodies (monosyllabic per architecture policy + one SHARED
disyllabic pool, distance >= 2 at body level), each expanded to three
POS wordforms (final coda ∅ noun / n verb / s modifier) with
class-conditional token frequencies (0.5 / 0.3 / 0.2 of the root's
Zipf mass). Cross-length substitution collisions are impossible
(substitutions preserve length), so sharing the disyllable pool is
sound and removes v1's pool-divergence confound.

Error model: single-channel substitutions, class-weighted (confusable
pairs W_HIGH, others W_LOW). Listeners: length-sensitive (perceives the
register; in A/Aprime a check-bit flip is audibly malformed) and
length-deaf.

Outcome classes per corrupted percept:
  parity — register architectures + sensitive listener + bit flip
  syntax — percept is a different POS form of the SAME root; caught by
           syntactic expectation or recovered semantically with some
           unmodeled probability — its own class, folded into neither
           silent nor detected
  silent — percept is a form of a DIFFERENT root: wrong meaning
  lexgap — percept is not a word: caught by lexical lookup

Metrics, both reported (review requirement):
  conditional — P(outcome | exactly one substitution in this word)
  exposure    — global event-weighted rate (longer words carry more
                corruption surface)

Run: python3 tools/explore_noparity.py [--json PATH]
"""

from __future__ import annotations

import json
import os
import random
import sys
from itertools import combinations
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lexgen import max_independent_set  # noqa: E402
from phonology import Inventory, Syllable  # noqa: E402

W_HIGH = float(os.environ.get("W_HIGH", 10.0))
W_LOW = 1.0
ZIPF_S = 1.0
N_DISYLL_ROOTS = 800
POS_CODAS = ("", "n", "s")          # noun / verb / modifier wordforms
POS_FREQ = (0.5, 0.3, 0.2)
SEED = int(os.environ.get("NOPARITY_SEED", 7))

ARCHS = {  # name -> (assignment_level, has_register)
    "A": ("spec", True),
    "Aprime": ("humility", True),
    "B": ("humility", False),
}


def pair_tables(inv: Inventory):
    spec = inv.spec
    cov = {ch: {frozenset(p) for p in prs}
           for ch, prs in spec["covered_confusion_pairs"].items()
           if ch != "comment"}
    forb = {ch: {frozenset(p) for p in prs}
            for ch, prs in spec["confusion_policy"]["forbidden"].items()
            if ch != "comment"}
    coronal = {frozenset(p) for p in
               spec["lexical_cell_rules"]["coronal_i_pairs"]}
    return cov, forb, coronal


def check_bits(inv: Inventory):
    return ({o["roman"]: o["check"] for o in inv.spec["onsets"]["content"]},
            {v["roman"]: v["check"] for v in inv.spec["vowels"]},
            {c["roman"]: c["check"] for c in inv.spec["codas"]})


def body_graph(inv, level: str):
    cov, forb, coronal = pair_tables(inv)
    bodies = [(o, v) for o in inv.content_onsets for v in inv.vowels
              if (o, v) not in inv.glide_cells]
    edges = {b: set() for b in bodies}
    for a, b in combinations(bodies, 2):
        if (a[0] == b[0]) == (a[1] == b[1]):
            continue
        channel = "onset" if a[0] != b[0] else "vowel"
        pair = frozenset((a[0], b[0])) if channel == "onset" \
            else frozenset((a[1], b[1]))
        conflicted = pair in forb.get(channel, set())
        if level == "humility":
            conflicted = conflicted or pair in cov.get(channel, set())
        if channel == "onset" and a[1] == "i" and pair in coronal:
            conflicted = True
        if conflicted:
            edges[a].add(b)
            edges[b].add(a)
    return bodies, edges


def shared_disyllable_roots(inv, rng):
    """One disyllabic root pool reused by every architecture; distance
    >= 2 enforced at body level within the pool."""
    firsts = [s for s in inv.lexical_content_syllables()
              if (s.onset, s.vowel) not in inv.glide_cells]
    final_bodies = [(o, v) for o in inv.content_onsets for v in inv.vowels
                    if (o, v) not in inv.glide_cells]
    pool, taken = [], set()

    def neighbors(body):
        s1, fb = body
        out = []
        for o in inv.content_onsets:
            if o != s1.onset:
                out.append((Syllable(o, s1.vowel, s1.coda), fb))
        for v in inv.vowels:
            if v != s1.vowel:
                out.append((Syllable(s1.onset, v, s1.coda), fb))
        for c in inv.codas:
            if c != s1.coda:
                out.append((Syllable(s1.onset, s1.vowel, c), fb))
        for o in inv.content_onsets:
            if o != fb[0]:
                out.append((s1, (o, fb[1])))
        for v in inv.vowels:
            if v != fb[1]:
                out.append((s1, (fb[0], v)))
        return out

    attempts = 0
    while len(pool) < N_DISYLL_ROOTS and attempts < 300000:
        attempts += 1
        s1 = rng.choice(firsts)
        fb = rng.choice(final_bodies)
        if s1.coda and s1.coda == fb[0]:   # fake geminate
            continue
        body = (s1, fb)
        if body in taken or any(n in taken for n in neighbors(body)):
            continue
        taken.add(body)
        pool.append(body)
    return pool


def build_lexicon(inv, level, disyll_pool):
    """Roots (most frequent first) expanded to POS wordforms.
    Returns (forms, monosyllable_root_count) with forms =
    [(word_tuple, root_id, freq), ...]."""
    bodies, edges = body_graph(inv, level)
    monos = sorted(max_independent_set(bodies, edges))
    roots = [("m", b) for b in monos] + [("d", b) for b in disyll_pool]
    forms = []
    for rank, (kind, body) in enumerate(roots):
        zipf = 1.0 / (rank + 1) ** ZIPF_S
        for coda, share in zip(POS_CODAS, POS_FREQ):
            if kind == "m":
                o, v = body
                word = (Syllable(o, v, coda),)
            else:
                s1, (fo, fv) = body
                word = (s1, Syllable(fo, fv, coda))
            forms.append((word, rank, zipf * share))
    return forms, len(monos)


def simulate(inv, forms, has_register, listener):
    cov, forb, _ = pair_tables(inv)
    ob, vb, cb = check_bits(inv)
    bit = {"onset": ob, "vowel": vb, "coda": cb}
    values = {"onset": inv.content_onsets, "vowel": inv.vowels,
              "coda": list(inv.codas)}
    form_root = {word: root for word, root, _ in forms}

    def weight(channel, a, b):
        pair = frozenset((a, b))
        if pair in cov.get(channel, set()) or pair in forb.get(channel, set()):
            return W_HIGH
        return W_LOW

    cond = {"parity": 0.0, "syntax": 0.0, "silent": 0.0, "lexgap": 0.0}
    events = []
    ftot = sum(f for _, _, f in forms)
    for word, root_id, f in forms:
        subs = []
        for i, syl in enumerate(word):
            for channel in ("onset", "vowel", "coda"):
                cur = getattr(syl, channel)
                for new in values[channel]:
                    if new == cur:
                        continue
                    kw = {"onset": syl.onset, "vowel": syl.vowel,
                          "coda": syl.coda}
                    kw[channel] = new
                    corrupted = word[:i] + (Syllable(**kw),) + word[i + 1:]
                    subs.append((corrupted, weight(channel, cur, new),
                                 bit[channel][cur] != bit[channel][new]))
        wtot = sum(w for _, w, _ in subs)
        for corrupted, w, flips in subs:
            if has_register and listener == "sensitive" and flips:
                outcome = "parity"
            elif corrupted in form_root:
                outcome = ("syntax" if form_root[corrupted] == root_id
                           else "silent")
            else:
                outcome = "lexgap"
            cond[outcome] += (f / ftot) * (w / wtot)
            events.append((outcome, f * w))
    expo = {k: 0.0 for k in cond}
    etot = sum(w for _, w in events)
    for outcome, w in events:
        expo[outcome] += w / etot
    rnd = lambda d: {k: round(v, 5) for k, v in d.items()}
    return rnd(cond), rnd(expo)


def main() -> int:
    rng = random.Random(SEED)
    inv = Inventory()
    disyll_pool = shared_disyllable_roots(inv, rng)
    built = {name: build_lexicon(inv, level, disyll_pool)
             for name, (level, _) in ARCHS.items()}
    # concept-match: same root count in every architecture, identical
    # Zipf mass per root rank
    total_roots = min(len(f) // len(POS_CODAS) for f, _ in built.values())
    report = {"disyllable_roots_shared": len(disyll_pool),
              "concept_roots_compared": total_roots,
              "w_high": W_HIGH}
    for name, (level, has_register) in ARCHS.items():
        forms, monos = built[name]
        forms = forms[:total_roots * len(POS_CODAS)]
        report[f"{name}_monosyllable_roots"] = monos
        for listener in ("sensitive", "deaf"):
            cond, expo = simulate(inv, forms, has_register, listener)
            report[f"{name}_{listener}_conditional"] = cond
            report[f"{name}_{listener}_exposure"] = expo
    print(json.dumps(report, indent=2))
    if "--json" in sys.argv:
        Path(sys.argv[sys.argv.index("--json") + 1]).write_text(
            json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
