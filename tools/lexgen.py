#!/usr/bin/env python3
"""Lexicon-space tooling: enumeration, validation, conflict analysis, and
the honest capacity report the freeze packet requires.

Usage:
  python3 tools/lexgen.py enumerate [--payload|--particles]
  python3 tools/lexgen.py validate WORD [WORD...]   (romanized content words)
  python3 tools/lexgen.py report [--json PATH]
"""

from __future__ import annotations

import argparse
import json
import sys
from itertools import combinations
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from phonology import ConflictRules, Inventory, Syllable  # noqa: E402


def body_conflict_graph(inv: Inventory, rules: ConflictRules,
                        policy: str) -> tuple[list[tuple[str, str]], dict]:
    """Monosyllabic root-body candidates (onset, vowel) and conflict edges.

    policy 'strict'  — forbidden AND weighted pairs conflict
    policy 'adopted' — only forbidden pairs (incl. coronal-i) conflict
    """
    bodies = [(o, v) for o in inv.content_onsets for v in inv.vowels
              if (o, v) not in inv.glide_cells]
    edges: dict[tuple, set[tuple]] = {b: set() for b in bodies}

    def conflicted(a, b) -> bool:
        # bodies as bare-vowel noun forms; coda channel identical, so only
        # onset/vowel substitutions matter here
        cls = rules.classify_pair([Syllable(a[0], a[1], "")],
                                  [Syllable(b[0], b[1], "")])
        if cls == "forbidden":
            return True
        return policy == "strict" and cls == "weighted"

    for a, b in combinations(bodies, 2):
        if (a[0] == b[0]) != (a[1] == b[1]):  # exactly one channel differs
            if conflicted(a, b):
                edges[a].add(b)
                edges[b].add(a)
    return bodies, edges


def max_independent_set(nodes: list, edges: dict) -> list:
    """Exact MIS by branch and bound; the graphs here are small/sparse."""
    best: list = []
    order = sorted(nodes, key=lambda n: len(edges[n]), reverse=True)

    def bb(candidates: list, chosen: list):
        nonlocal best
        if len(chosen) + len(candidates) <= len(best):
            return
        if not candidates:
            if len(chosen) > len(best):
                best = chosen[:]
            return
        n = candidates[0]
        rest = candidates[1:]
        # branch 1: take n
        bb([c for c in rest if c not in edges[n]], chosen + [n])
        # branch 2: skip n
        bb(rest, chosen)

    bb(order, [])
    return best


def capacity_report(inv: Inventory, rules: ConflictRules) -> dict:
    out: dict = {}
    for policy in ("strict", "adopted"):
        bodies, edges = body_conflict_graph(inv, rules, policy)
        mis = max_independent_set(bodies, edges)
        out[f"monosyllable_root_bodies_{policy}"] = len(mis)
        out[f"monosyllable_example_{policy}"] = sorted(
            f"{o}{v}" for o, v in mis)
    reserve = inv.spec["reserve_fraction"]  # required key — no silent default
    adopted = out["monosyllable_root_bodies_adopted"]
    out["reserve_fraction"] = reserve
    out["monosyllable_assignable_after_reserve"] = int(adopted * (1 - reserve))

    # disyllabic root bodies: first syllable any lexical content triple
    # (minus glide cells), final syllable a bare-vowel body (noun form),
    # minus fake geminates.
    firsts = [s for s in inv.lexical_content_syllables()
              if (s.onset, s.vowel) not in inv.glide_cells]
    finals = [Syllable(o, v, "") for o in inv.content_onsets for v in inv.vowels
              if (o, v) not in inv.glide_cells]
    count = 0
    for s1 in firsts:
        for s2 in finals:
            if s1.coda and s1.coda == s2.onset:  # fake geminate
                continue
            count += 1
    out["disyllable_root_bodies_upper_bound"] = count
    out["note"] = ("disyllable figure excludes glide cells and fake "
                   "geminates only; echo-vowel, tosmabru, and pairwise "
                   "spacing are assignment-time checks (kps)")
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    en = sub.add_parser("enumerate")
    en.add_argument("--payload", action="store_true")
    en.add_argument("--particles", action="store_true")
    va = sub.add_parser("validate")
    va.add_argument("words", nargs="+")
    rp = sub.add_parser("report")
    rp.add_argument("--json", dest="json_path")
    args = ap.parse_args()

    inv = Inventory()
    rules = ConflictRules(inv)

    if args.cmd == "enumerate":
        if args.particles:
            sylls = inv.particle_syllables()
        else:
            sylls = inv.lexical_content_syllables()
        for s in sylls:
            print(inv.romanize_syllable(s, payload=args.payload))
        return 0

    if args.cmd == "validate":
        bad = 0
        for w in args.words:
            try:
                sylls = inv.parse_word(w)
            except ValueError as e:
                print(f"{w}: PARSE ERROR: {e}")
                bad += 1
                continue
            issues = inv.validate_content_word(sylls)
            if issues:
                bad += 1
                print(f"{w}: " + "; ".join(issues))
            else:
                pos = inv.pos_by_coda[sylls[-1].coda]
                print(f"{w}: ok ({pos}, {len(sylls)} syllable(s), "
                      f"canonical {inv.romanize_word(sylls)})")
        return 1 if bad else 0

    if args.cmd == "report":
        rep = capacity_report(inv, rules)
        for k, v in rep.items():
            if not k.startswith("monosyllable_example"):
                print(f"{k:42s} {v}")
        if args.json_path:
            Path(args.json_path).write_text(json.dumps(rep, indent=2))
            print(f"written: {args.json_path}")
        return 0

    return 2


if __name__ == "__main__":
    sys.exit(main())
