#!/usr/bin/env python3
"""Solve the v0.2 anti-iconic phoneme -> (base, modifier) assignment.

Confusion-aware anti-iconic policy (conlang-wqj): the visual grammar
stays compositional (base x modifier), but the assignment is solved as
an error-correcting code against the PHONETIC confusion pairs in
channels.json rather than mirroring articulation:

  HARD  every phonetic confusion pair (covered ∪ forbidden ∪ weighted)
        differs in base AND modifier — visual distance 2, with base
        (the robust feature) always among the differences.
  HARD  letters occupy distinct (base, modifier) cells; cells with no
        robust realization are unusable; base loads within 2..3.
  HARD  h is not assigned here: it keeps the tick base alone
        (lightest glyph = particle scaffold).

Deterministic: ordered depth-first search (letters in spec order,
cells ordered by current-lowest base load, then base, then modifier);
the first perfect solution is the canonical one. If no perfect
solution existed the script would report it loudly rather than
silently relaxing.

Run: python3 tools/assign_glyphs.py   (prints the chosen assignment
and the stats quoted in docs/design/script-v02-assignment.md)
"""

import json
import sys
from pathlib import Path

SPEC = Path(__file__).resolve().parent.parent / "docs" / "spec" / "channels.json"

BASES = ["circle", "vertical", "diagonal", "angle"]
MODIFIERS = ["plain", "crossed", "doubled", "capped"]

# realization vetoes: combinations with no robust full-scale
# realization (see plan D1); everything else is drawable at 16 px
BANNED_CELLS = {("circle", "doubled"), ("angle", "capped")}


def phonetic_pairs(data):
    pairs = set()
    for group in (data["covered_confusion_pairs"]["onset"],
                  data["confusion_policy"]["forbidden"].get("onset", []),
                  data["confusion_policy"]["weighted"].get("onset", [])):
        for a, b in group:
            pairs.add(frozenset((a, b)))
    return pairs


def solve(onsets, pairs):
    """First perfect assignment found by ordered DFS, or None."""
    neighbors = {o: set() for o in onsets}
    for p in pairs:
        a, b = tuple(p)
        neighbors[a].add(b)
        neighbors[b].add(a)
    assign: dict = {}

    def cells():
        load = {b: sum(1 for c in assign.values() if c[0] == b)
                for b in BASES}
        order = sorted(
            ((b, m) for b in BASES for m in MODIFIERS
             if (b, m) not in BANNED_CELLS and load[b] < 3),
            key=lambda c: (load[c[0]], BASES.index(c[0]),
                           MODIFIERS.index(c[1])))
        return order

    def dfs(i):
        if i == len(onsets):
            load = {b: sum(1 for c in assign.values() if c[0] == b)
                    for b in BASES}
            return min(load.values()) >= 2
        o = onsets[i]
        for cell in cells():
            if cell in assign.values():
                continue
            ok = True
            for nb in neighbors[o]:
                if nb in assign:
                    nbase, nmod = assign[nb]
                    if nbase == cell[0] or nmod == cell[1]:
                        ok = False
                        break
            if ok:
                assign[o] = cell
                if dfs(i + 1):
                    return True
                del assign[o]
        return False

    return dict(assign) if dfs(0) else None


def main() -> int:
    data = json.loads(SPEC.read_text())
    onsets = [o["roman"] for o in data["onsets"]["content"]]
    pairs = phonetic_pairs(data)
    result = solve(onsets, pairs)
    if result is None:
        print("NO PERFECT SOLUTION — relax constraints deliberately",
              file=sys.stderr)
        return 1
    print(f"phonetic pairs: {len(pairs)} — all at visual distance 2 "
          f"(base and modifier both differ)")
    for o in onsets:
        b, m = result[o]
        print(f"  {o}: {b:9s} {m}")
    print(json.dumps({o: {"base": result[o][0], "modifier": result[o][1]}
                      for o in onsets}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
