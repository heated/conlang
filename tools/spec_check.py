#!/usr/bin/env python3
"""Recompute every number the spec claims from channels.json.

Exits nonzero if any computed value disagrees with budget_expected or any
structural invariant fails. Run from the repo root: python3 tools/spec_check.py
"""

import json
import sys
from pathlib import Path

SPEC = Path(__file__).resolve().parent.parent / "docs" / "spec" / "channels.json"


def fail(msg: str) -> None:
    print(f"FAIL: {msg}")
    fail.count += 1


fail.count = 0


def main() -> int:
    data = json.loads(SPEC.read_text())

    content_onsets = data["onsets"]["content"]
    particle_onsets = data["onsets"]["particle"]
    vowels = data["vowels"]
    codas = data["codas"]
    registers = data["registers"]
    exp = data["budget_expected"]

    n_co, n_po = len(content_onsets), len(particle_onsets)
    n_v, n_c, n_r = len(vowels), len(codas), len(registers)

    # --- structural invariants ---
    for group, items in (("content onsets", content_onsets),
                         ("particle onsets", particle_onsets),
                         ("vowels", vowels), ("codas", codas),
                         ("registers", registers)):
        romans = [i["roman"] for i in items]
        if len(set(romans)) != len(romans):
            fail(f"duplicate romanizations in {group}: {romans}")
    all_onset_idx = [o["index"] for o in content_onsets + particle_onsets]
    if sorted(all_onset_idx) != list(range(n_co + n_po)):
        fail(f"onset indices not contiguous 0..{n_co + n_po - 1}: {sorted(all_onset_idx)}")
    if [v["index"] for v in vowels] != list(range(n_v)):
        fail("vowel indices not contiguous")
    if [c["index"] for c in codas] != list(range(n_c)):
        fail("coda indices not contiguous")
    if n_r != 2:
        fail(f"parity rule assumes 2 registers, found {n_r}")

    # digit tens: exactly digits 0-9, one per content onset
    tens = sorted(o.get("digit_tens") for o in content_onsets)
    if tens != list(range(10)):
        fail(f"digit_tens must cover 0-9 exactly, got {tens}")

    # digit units: exactly digits 0-9 with valid rimes
    units = data["digit_units_rimes"]["map"]
    if sorted(u["digit"] for u in units) != list(range(10)):
        fail("digit_units_rimes must cover 0-9 exactly")
    vowel_romans = {v["roman"] for v in vowels}
    coda_romans = {c["roman"] for c in codas}
    seen_rimes = set()
    for u in units:
        if u["vowel"] not in vowel_romans:
            fail(f"units digit {u['digit']}: unknown vowel {u['vowel']!r}")
        if u["coda"] not in coda_romans:
            fail(f"units digit {u['digit']}: unknown coda {u['coda']!r}")
        rime = (u["vowel"], u["coda"])
        if rime in seen_rimes:
            fail(f"duplicate units rime {rime}")
        seen_rimes.add(rime)

    # POS classes: noun/verb/modifier active + one reserved
    pos = [c["pos_class"] for c in codas]
    if sorted(pos) != sorted(["noun", "verb", "modifier", "reserved"]):
        fail(f"expected POS classes noun/verb/modifier/reserved, got {pos}")

    # --- budget arithmetic ---
    computed = {
        "raw_total": (n_co + n_po) * n_v * n_c * n_r,
        "content_raw": n_co * n_v * n_c * n_r,
        "particle_raw": n_po * n_v * n_c * n_r,
        # parity fixes register for every (onset, vowel, coda)
        "content_lexical": n_co * n_v * n_c,
        "particle_lexical": n_po * n_v * n_c,
        "content_complement": n_co * n_v * n_c,
        "particle_complement": n_po * n_v * n_c,
        "content_monosyllables_per_pos_class": n_co * n_v,
        "pos_classes_active": sum(1 for p in pos if p != "reserved"),
        "content_monosyllables_usable_v01":
            n_co * n_v * sum(1 for p in pos if p != "reserved"),
        "digit_pairs_needed": 10 * 10,
        "hour_quarter_values": 24 * 4,
        "month_day_values": 12 * 31,
        "one_syllable_payload_points": n_co * n_v * n_c,
    }

    for key, want in exp.items():
        got = computed.get(key)
        if got is None:
            fail(f"budget_expected has unknown key {key}")
        elif got != want:
            fail(f"{key}: spec claims {want}, computed {got}")

    # --- fit checks the spec relies on ---
    if computed["digit_pairs_needed"] > computed["one_syllable_payload_points"]:
        fail("digit pairs do not fit in one payload syllable")
    if computed["hour_quarter_values"] > computed["one_syllable_payload_points"]:
        fail("hour x quarter does not fit in one payload syllable")
    if computed["month_day_values"] <= computed["one_syllable_payload_points"]:
        fail("month x day unexpectedly fits in one complement syllable; "
             "spec says it needs two — update SPEC §modes preview")

    # parity rule sanity: register determined and in range for every syllable
    for o in range(n_co + n_po):
        for v in range(n_v):
            for c in range(n_c):
                if (o + v + c) % 2 not in (0, 1):
                    fail("parity rule out of range (unreachable)")

    print(f"channel space: {n_co}+{n_po} onsets x {n_v} vowels x {n_c} codas "
          f"x {n_r} registers")
    for key in exp:
        print(f"  {key:40s} {computed[key]}")
    if fail.count:
        print(f"\n{fail.count} check(s) FAILED")
        return 1
    print("\nall checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
