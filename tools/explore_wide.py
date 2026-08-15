#!/usr/bin/env python3
"""GF-W: the wide greenfield variant, computed (bead: wide-variant).

Builds a wide-inventory spec (16 content onsets + h, 5 vowels, same
POS codas) with humility-covered confusion pairs for every added
contrast (voicing pairs; r/l; z/s), then computes real capacities
with the existing lexgen machinery. Prints the numbers used in
docs/design/gfw-sketch.md.

Inventory (L1 pricing in the sketch doc):
  narrow 10: c p t k m n s l w j   (+h particles)
  wide  +6:  b d g f z r
Covered-pair additions: p/b t/d k/g (voicing; Mandarin/Korean remap),
f/p (Korean/Filipino), z/s (Spanish merger), r/l (Japanese/Korean),
plus the narrow set carried over.
"""

import copy
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lexgen  # noqa: E402
import phonology  # noqa: E402

SPEC = Path(__file__).resolve().parent.parent / "docs" / "spec" / "channels.json"


def wide_spec():
    d = json.loads(SPEC.read_text())
    w = copy.deepcopy(d)
    add = [("b", 1), ("d", 0), ("g", 1), ("f", 1), ("z", 1), ("r", 1)]
    idx = len(d["onsets"]["content"])
    for i, (roman, chk) in enumerate(add):
        w["onsets"]["content"].append(
            {"roman": roman, "index": idx + i, "check": chk,
             "digit_tens": None})
    cov = w["covered_confusion_pairs"]["onset"]
    cov += [["p", "b"], ["t", "d"], ["k", "g"], ["f", "p"],
            ["z", "s"], ["r", "l"], ["b", "w"], ["d", "n"],
            ["g", "k"]]
    # dedupe
    w["covered_confusion_pairs"]["onset"] = sorted(
        {tuple(sorted(p)) for p in cov})
    w["covered_confusion_pairs"]["onset"] = [
        list(p) for p in w["covered_confusion_pairs"]["onset"]]
    return w


def main():
    d = json.loads(SPEC.read_text())
    w = wide_spec()
    for name, spec in (("narrow", d), ("wide", w)):
        try:
            inv = phonology.Inventory(spec)
            rules = phonology.ConflictRules(inv)
            bodies, edges = lexgen.body_conflict_graph(inv, rules, "adopted")
            mis = lexgen.max_independent_set(bodies, edges)
            n_on = len(spec["onsets"]["content"])
            syl = n_on * 5 * 4
            print(f"{name}: {n_on} content onsets; {syl} content "
                  f"syllables; {len(bodies)} bodies; "
                  f"adopted-MIS {len(mis)} monosyllabic roots")
            if name == "wide":
                print("  wide MIS:", " ".join(sorted(
                    f"{o}{v}" for o, v in mis)))
        except Exception as e:
            print(f"{name}: FAILED — {e}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
