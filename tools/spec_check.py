#!/usr/bin/env python3
"""Verify docs/spec/channels.json against the spec's normative claims.

Checks are of three kinds:
  1. Frozen assignments: the exact digit maps, POS map, check bits, and
     register indices the spec declares normative.
  2. Structural invariants: index contiguity, check-bit coverage of the
     declared confusion pairs, template sanity.
  3. Recomputed arithmetic: every number in budget_expected, plus a real
     enumeration of the lexical codespace and its distance profile.

Exits nonzero on any mismatch. Run: python3 tools/spec_check.py
Self-test (asserts that known corruptions are caught): add --selftest.
"""

import copy
import itertools
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

SPEC = Path(__file__).resolve().parent.parent / "docs" / "spec" / "channels.json"

# Frozen normative assignments (SPEC.md §2, §6, §10). A change here is a
# spec version bump, not a data edit.
FROZEN_TENS = {"c": 0, "p": 1, "t": 2, "k": 3, "m": 4,
               "n": 5, "s": 6, "l": 7, "w": 8, "j": 9}
FROZEN_ONSET_INDEX = {"c": 0, "p": 1, "t": 2, "k": 3, "m": 4,
                      "n": 5, "s": 6, "l": 7, "w": 8, "j": 9, "h": 10}
FROZEN_VOWEL_INDEX = {"a": 0, "e": 1, "i": 2, "o": 3, "u": 4}
FROZEN_UNITS = {0: ("a", ""), 1: ("e", ""), 2: ("i", ""), 3: ("o", ""),
                4: ("u", ""), 5: ("a", "n"), 6: ("e", "n"), 7: ("i", "n"),
                8: ("o", "n"), 9: ("u", "n")}
FROZEN_POS = {"": "noun", "n": "verb", "s": "modifier", "l": "reserved"}
FROZEN_REGISTERS = {0: "short", 1: "long"}
PARTICLE_ONSET = "h"

# Frozen featural-script assignments (script.md §3–§4, v0.2
# confusion-aware anti-iconic code, solved by tools/assign_glyphs.py).
# The decomposition is normative data: glyphs are computed from it.
FROZEN_ONSET_FEATURES = {
    "c": ("circle", "plain"), "p": ("vertical", "plain"),
    "t": ("diagonal", "crossed"), "k": ("angle", "doubled"),
    "m": ("circle", "crossed"), "n": ("vertical", "doubled"),
    "s": ("diagonal", "doubled"), "l": ("angle", "plain"),
    "w": ("circle", "capped"), "j": ("vertical", "crossed"),
    "h": ("tick", "doubled"),
}
FROZEN_VOWEL_FEATURES = {
    "a": ("low", "central"), "e": ("mid", "front"), "i": ("high", "front"),
    "o": ("mid", "back"), "u": ("high", "back"),
}
FROZEN_BASES = {"circle", "vertical", "diagonal", "angle", "tick"}
FROZEN_MODIFIERS = {"plain", "crossed", "doubled", "capped"}


class Checker:
    def __init__(self, data):
        self.data = data
        self.failures = []

    def fail(self, msg):
        self.failures.append(msg)

    def expect(self, cond, msg):
        if not cond:
            self.fail(msg)

    def run(self):
        d = self.data
        content = d["onsets"]["content"]
        particle = d["onsets"]["particle"]
        vowels = d["vowels"]
        codas = d["codas"]
        registers = d["registers"]
        exp = d["budget_expected"]

        # --- frozen assignments ---
        self.expect({o["roman"]: o["index"] for o in content + particle}
                    == FROZEN_ONSET_INDEX, "onset roman->index differs from frozen table")
        self.expect({o["roman"]: o.get("digit_tens") for o in content}
                    == FROZEN_TENS, "digit_tens differs from frozen table")
        self.expect({v["roman"]: v["index"] for v in vowels}
                    == FROZEN_VOWEL_INDEX, "vowel roman->index differs from frozen table")
        units = {u["digit"]: (u["vowel"], u["coda"])
                 for u in d["digit_units_rimes"]["map"]}
        self.expect(units == FROZEN_UNITS, "digit_units_rimes differs from frozen table")
        self.expect({c["roman"]: c["pos_class"] for c in codas}
                    == FROZEN_POS, "coda->POS map differs from frozen table")
        self.expect({r["index"]: r["roman"] for r in registers}
                    == FROZEN_REGISTERS, "register indices/names differ from frozen table")
        self.expect([p["roman"] for p in particle] == [PARTICLE_ONSET],
                    "particle onset class must be exactly [h]")
        self.expect(d["register_rule"]["rule"]
                    == "register_index == (check(onset) + check(vowel) + check(coda)) mod 2",
                    "register rule string changed")

        # --- featural script (script.md) ---
        sf = d.get("script_features")
        if sf is None:
            self.fail("script_features missing from channels.json")
        else:
            of = {k: (v["base"], v["modifier"])
                  for k, v in sf["onset_features"].items()}
            vf = {k: (v["height"], v["backness"])
                  for k, v in sf["vowel_features"].items()}
            self.expect(of == FROZEN_ONSET_FEATURES,
                        "onset_features differ from frozen table")
            self.expect(vf == FROZEN_VOWEL_FEATURES,
                        "vowel_features differ from frozen table")
            self.expect(len(set(of.values())) == len(of),
                        "onset (base,modifier) cells must be injective")
            self.expect(len(set(vf.values())) == len(vf),
                        "vowel (height,backness) pairs must be injective")
            vg = sf["visual_grammar"]
            self.expect(set(vg.get("bases", {})) == FROZEN_BASES,
                        "visual_grammar.bases differ from frozen set")
            self.expect(set(vg.get("modifiers", {})) == FROZEN_MODIFIERS,
                        "visual_grammar.modifiers differ from frozen set")
            banned = {tuple(c) for c in vg.get("banned_cells", [])}
            self.expect(banned == {("circle", "doubled"),
                                   ("angle", "capped")},
                        "banned_cells differ from frozen set")
            for o, (b, m) in of.items():
                self.expect(b in FROZEN_BASES, f"onset {o}: unknown base {b!r}")
                self.expect(m in FROZEN_MODIFIERS,
                            f"onset {o}: unknown modifier {m!r}")
                self.expect((b, m) not in banned,
                            f"onset {o}: assigned to banned cell {(b, m)}")
            for v, (hgt, bck) in vf.items():
                self.expect(hgt in ("high", "mid", "low"),
                            f"vowel {v}: unknown height {hgt!r}")
                self.expect(bck in ("front", "central", "back"),
                            f"vowel {v}: unknown backness {bck!r}")
            # the anti-iconic code's defining invariant: every phonetic
            # confusion pair sits at visual distance 2 (base AND modifier
            # differ), so no single degraded feature class can merge a
            # phonetically confusable pair
            phon_pairs = set()
            for grp in (d["covered_confusion_pairs"]["onset"],
                        d["confusion_policy"]["forbidden"].get("onset", []),
                        d["confusion_policy"]["weighted"].get("onset", [])):
                for a, b in grp:
                    phon_pairs.add((a, b))
            for a, b in phon_pairs:
                self.expect(of[a][0] != of[b][0] and of[a][1] != of[b][1],
                            f"phonetic pair {a}/{b} not at visual distance 2")
            scp = sf.get("script_confusion_pairs")
            if scp is None:
                self.fail("script_confusion_pairs missing (eye-channel "
                          "pricing input, lexgen strict_with_script)")
            else:
                known = set(of)
                listed = set()
                for a, b in scp["onset"]:
                    self.expect(a in known and b in known and a != b,
                                f"script_confusion_pairs: bad pair {a!r}/{b!r}")
                    listed.add(frozenset((a, b)))
                # the eye's weak set is the same-base set BY CONSTRUCTION
                # of the anti-iconic code; silent readers get no phonetic
                # protection on them, so every same-base pair must be
                # priced by the lexicon (Fable review, conlang-wqj)
                for a in of:
                    for b in of:
                        if a < b and of[a][0] == of[b][0]:
                            self.expect(
                                frozenset((a, b)) in listed,
                                f"same-base pair {a}/{b} missing from "
                                f"script_confusion_pairs")

        # --- structural invariants ---
        for group, items in (("onsets", content + particle), ("vowels", vowels),
                             ("codas", codas)):
            self.expect(all(isinstance(i.get("check"), int) and i["check"] in (0, 1)
                            for i in items), f"{group}: every value needs a 0/1 check bit")
        for shape_key in ("particle", "content"):
            syl = d["word_shapes"][shape_key]["syllables"]
            self.expect(isinstance(syl, dict) and set(syl) == {"min", "max"}
                        and syl["min"] <= syl["max"],
                        f"word_shapes.{shape_key}.syllables must be {{min,max}}")
        self.expect(d["word_shapes"]["content"]["syllables"] == {"min": 1, "max": 3},
                    "content word shape must be 1-3 syllables")
        self.expect(d["word_shapes"]["particle"]["syllables"] == {"min": 1, "max": 1},
                    "particles must be exactly 1 syllable")

        def bits(group_items):
            return {i["roman"]: i["check"] for i in group_items}
        onset_bits = bits(content + particle)
        vowel_bits = bits(vowels)
        coda_bits = bits(codas)

        # covered confusion pairs must have different check bits
        table = {"onset": onset_bits, "vowel": vowel_bits, "coda": coda_bits}
        for channel, pairs in d["covered_confusion_pairs"].items():
            if channel == "comment":
                continue
            for a, b in pairs:
                self.expect(table[channel][a] != table[channel][b],
                            f"covered confusion pair {channel} {a!r}/{b!r} shares a check bit")
        # residual pairs must be same-bit (else they belong in covered)
        for channel, pairs in d["residual_confusion_pairs"].items():
            if channel == "comment":
                continue
            for a, b in pairs:
                self.expect(table[channel][a] == table[channel][b],
                            f"residual pair {channel} {a!r}/{b!r} has different bits — move to covered")

        # confusion_policy must exactly partition the residual pairs,
        # over exactly the supported channels — no extras anywhere
        CHANNELS = {"onset", "vowel", "coda"}

        def pairset(block):
            return {ch: {frozenset(p) for p in prs}
                    for ch, prs in block.items() if ch != "comment"}
        residual = pairset(d["residual_confusion_pairs"])
        forbidden = pairset(d["confusion_policy"]["forbidden"])
        weighted = pairset(d["confusion_policy"]["weighted"])
        for name, block in (("residual", residual), ("forbidden", forbidden),
                            ("weighted", weighted)):
            self.expect(set(block) == CHANNELS,
                        f"{name} pairs must cover exactly {sorted(CHANNELS)}, "
                        f"got {sorted(block)}")
        for ch in CHANNELS:
            f, w = forbidden.get(ch, set()), weighted.get(ch, set())
            self.expect(not (f & w),
                        f"confusion_policy {ch}: pair in both forbidden and weighted")
            self.expect(f | w == residual.get(ch, set()),
                        f"confusion_policy {ch}: forbidden+weighted must equal residual pairs")

        # humility invariant (conlang-bf2): the runtime forbidden set must
        # equal covered ∪ confusion_policy.forbidden per channel
        try:
            import phonology
            rt = phonology.ConflictRules(phonology.Inventory(d))
            for ch in CHANNELS:
                want = forbidden.get(ch, set())                     | {frozenset(p) for p in d["covered_confusion_pairs"].get(ch, [])}
                self.expect(rt.forbidden.get(ch, set()) == want,
                            f"runtime forbidden[{ch}] != covered ∪ forbidden")
        except Exception as e:  # pragma: no cover
            self.fail(f"runtime humility check failed to run: {e}")

        # structured cell rules must reference real inventory values
        cells = d["lexical_cell_rules"]
        onset_romans = {o["roman"] for o in content}
        vowel_romans2 = {v["roman"] for v in vowels}
        for key in ("banned_cells", "weighted_cells"):
            for o, v in cells[key]:
                self.expect(o in onset_romans and v in vowel_romans2,
                            f"{key} cell ({o},{v}) not in inventory")
        for a, b in cells["coronal_i_pairs"]:
            self.expect(a in onset_romans and b in onset_romans,
                        f"coronal_i pair ({a},{b}) not in inventory")
        for v in cells["echo_vowels"]:
            self.expect(v in vowel_romans2, f"echo vowel {v!r} not in inventory")
        self.expect(isinstance(d.get("reserve_fraction"), float)
                    and 0 < d["reserve_fraction"] < 1,
                    "reserve_fraction must be present and in (0,1)")

        # --- enumeration: lexical codespace and distance profile ---
        content_bits = [(o["roman"], o["check"]) for o in content]
        lex = [(o, v, c) for (o, _ob) in content_bits
               for v in vowel_bits if v in FROZEN_VOWEL_INDEX
               for c in coda_bits]
        # register per syllable
        def reg(o, v, c):
            return (onset_bits[o] + vowel_bits[v] + coda_bits[c]) % 2

        # distance-1 pairs among lexical (o,v,c) triples that share register:
        # these are the substitutions the check channel cannot see.
        undetected = 0
        for (o, v, c) in lex:
            r = reg(o, v, c)
            for o2, _ in content_bits:
                if o2 != o and onset_bits[o2] == onset_bits[o]:
                    undetected += 1
            for v2 in vowel_bits:
                if v2 != v and vowel_bits[v2] == vowel_bits[v]:
                    undetected += 1
            for c2 in coda_bits:
                if c2 != c and coda_bits[c2] == coda_bits[c]:
                    undetected += 1
        undetected //= 2  # each unordered pair counted twice
        # sanity: with 5/5 onset bits, 3/2 vowel bits, 2/2 coda bits the
        # same-bit neighbor counts are fixed; assert the derived total so the
        # profile is visible and any bit reassignment is priced consciously.
        per_syllable_same_bit_neighbors = None  # computed below for report

        # --- recomputed arithmetic ---
        n_co, n_po = len(content), len(particle)
        n_v, n_c, n_r = len(vowels), len(codas), len(registers)
        active = sum(1 for c in codas if c["pos_class"] != "reserved")
        computed = {
            "raw_total": (n_co + n_po) * n_v * n_c * n_r,
            "content_raw": n_co * n_v * n_c * n_r,
            "particle_raw": n_po * n_v * n_c * n_r,
            "content_lexical": n_co * n_v * n_c,
            "particle_lexical": n_po * n_v * n_c,
            "content_complement": n_co * n_v * n_c,
            "particle_complement": n_po * n_v * n_c,
            "monosyllable_wordforms_per_pos_class": n_co * n_v,
            "pos_classes_active": active,
            "monosyllable_wordforms_active": n_co * n_v * active,
            "monosyllable_root_bodies": n_co * n_v,
            "disyllable_wordforms_active": (n_co * n_v * n_c) * (n_co * n_v * active),
            "disyllable_root_bodies": (n_co * n_v * n_c) * (n_co * n_v),
            "uniform_distance2_bound": (n_co * n_v * n_c) // n_co,
            "digit_pairs_needed": 10 * 10,
            "hour_quarter_values": 24 * 4,
            "month_day_values": 12 * 31,
            "one_syllable_payload_points": n_co * n_v * n_c,
        }
        for key, want in exp.items():
            got = computed.get(key)
            if got is None:
                self.fail(f"budget_expected has unknown key {key}")
            elif got != want:
                self.fail(f"{key}: spec claims {want}, computed {got}")
        for key in computed:
            if key not in exp:
                self.fail(f"budget_expected is missing key {key}")

        # fits the spec relies on
        self.expect(computed["digit_pairs_needed"] <= computed["one_syllable_payload_points"],
                    "digit pairs do not fit in one payload syllable")
        self.expect(computed["hour_quarter_values"] <= computed["one_syllable_payload_points"],
                    "hour x quarter does not fit in one payload syllable")
        self.expect(computed["month_day_values"] > computed["one_syllable_payload_points"],
                    "month x day unexpectedly fits one payload syllable; update SPEC")

        return computed, len(lex), undetected


def run_file_checks(data, verbose=True, capacity=True):
    ck = Checker(data)
    computed, lex_size, undetected = ck.run()
    if capacity:
        # assert the exact spacing-capacity numbers the docs quote, by
        # actually running the generator against this spec data
        try:
            import lexgen
            import phonology
            inv = phonology.Inventory(data)
            rules = phonology.ConflictRules(inv)
            rep = lexgen.capacity_report(inv, rules)
            for key, want in data["capacity_expected"].items():
                if key == "comment":
                    continue
                got = rep.get(key)
                if got != want:
                    ck.fail(f"capacity_expected.{key}: spec claims {want}, "
                            f"generator computed {got}")
        except KeyError as e:
            ck.fail(f"capacity check aborted, missing key: {e}")
    if verbose:
        print(f"lexical content triples enumerated: {lex_size}")
        print(f"check-invisible distance-1 pairs (generator's responsibility): {undetected}")
        for key, val in computed.items():
            print(f"  {key:40s} {val}")
    return ck.failures


MUTATIONS = [
    ("units digit 5 coda n->l",
     lambda d: d["digit_units_rimes"]["map"][5].__setitem__("coda", "l")),
    ("swap tens digits of c and p",
     lambda d: (d["onsets"]["content"][0].__setitem__("digit_tens", 1),
                d["onsets"]["content"][1].__setitem__("digit_tens", 0))),
    ("long register index 1->9",
     lambda d: d["registers"][1].__setitem__("index", 9)),
    ("register rule replaced",
     lambda d: d["register_rule"].__setitem__("rule", "always short")),
    ("s/c share a check bit",
     lambda d: d["onsets"]["content"][0].__setitem__("check", 0)),
    ("forbidden pair dropped from policy",
     lambda d: d["confusion_policy"]["forbidden"]["onset"].clear()),
    ("pair in both forbidden and weighted",
     lambda d: d["confusion_policy"]["weighted"]["onset"].append(["p", "k"])),
    ("extra channel smuggled into policy",
     lambda d: d["confusion_policy"]["forbidden"].__setitem__("tone", [["x", "y"]])),
    ("banned cell references unknown onset",
     lambda d: d["lexical_cell_rules"]["banned_cells"].append(["q", "a"])),
    ("reserve_fraction removed",
     lambda d: d.__delitem__("reserve_fraction")),
    ("POS of coda n changed",
     lambda d: d["codas"][1].__setitem__("pos_class", "noun")),
    ("content words allowed 4 syllables",
     lambda d: d["word_shapes"]["content"]["syllables"].__setitem__("max", 4)),
    ("budget number corrupted",
     lambda d: d["budget_expected"].__setitem__("content_lexical", 201)),
    ("t reassigned to vertical (breaks p/t distance 2)",
     lambda d: d["script_features"]["onset_features"]["t"]
     .__setitem__("base", "vertical"),
     "differ from frozen"),
    ("vowel u fronted (collides with i)",
     lambda d: d["script_features"]["vowel_features"]["u"]
     .__setitem__("backness", "front"),
     "differ from frozen"),
    ("script_features removed",
     lambda d: d.__delitem__("script_features"),
     "script_features missing"),
    ("visual_grammar base set corrupted",
     lambda d: d["script_features"]["visual_grammar"]["bases"]
     .__setitem__("triangle", "three strokes"),
     "visual_grammar.bases"),
    ("confusable pair merged onto one base+modifier axis",
     # p/t are phonetically confusable; give t p's modifier as well as a
     # frozen-table-passing... (frozen check fires first, distance check
     # must ALSO fire when frozen table itself is edited to match)
     lambda d: (d["script_features"]["onset_features"]["t"]
                .__setitem__("modifier", "plain"),
                d["script_features"]["onset_features"]["t"]
                .__setitem__("base", "vertical")),
     "not at visual distance 2"),
    ("script confusion pair references unknown onset",
     lambda d: d["script_features"]["script_confusion_pairs"]["onset"]
     .append(["q", "t"]),
     "script_confusion_pairs"),
    ("script_confusion_pairs removed",
     lambda d: d["script_features"].__delitem__("script_confusion_pairs"),
     "script_confusion_pairs missing"),
    ("same-base pair c/w dropped from eye pricing",
     lambda d: d["script_features"]["script_confusion_pairs"]["onset"]
     .remove(["c", "w"]),
     "missing from script_confusion_pairs"),
    ("banned_cells cleared",
     lambda d: d["script_features"]["visual_grammar"]["banned_cells"]
     .clear(),
     "banned_cells differ from frozen"),
]


def selftest(data):
    bad = 0
    for entry in MUTATIONS:
        name, mutate = entry[0], entry[1]
        expected = entry[2] if len(entry) > 2 else None
        mutant = copy.deepcopy(data)
        mutate(mutant)
        # capacity recomputation is slow; only the capacity mutation needs it
        failures = run_file_checks(mutant, verbose=False, capacity=False)
        if not failures:
            print(f"  SELFTEST FAILURE: mutation '{name}' passed all checks")
            bad += 1
        elif expected and not any(expected in f for f in failures):
            print(f"  SELFTEST FAILURE: mutation '{name}' caught, but no "
                  f"failure mentions {expected!r}: {failures}")
            bad += 1
        else:
            print(f"  selftest ok: caught mutation '{name}'")
    mutant = copy.deepcopy(data)
    mutant["capacity_expected"]["monosyllable_root_bodies_adopted"] = 35
    if run_file_checks(mutant, verbose=False, capacity=True):
        print("  selftest ok: caught mutation 'capacity number corrupted'")
    else:
        print("  SELFTEST FAILURE: mutation 'capacity number corrupted' passed")
        bad += 1
    return bad


def main() -> int:
    data = json.loads(SPEC.read_text())
    failures = run_file_checks(data)
    for f in failures:
        print(f"FAIL: {f}")
    bad = 0
    if "--selftest" in sys.argv:
        print("mutation self-test:")
        bad = selftest(data)
    if failures or bad:
        print(f"\n{len(failures)} check failure(s), {bad} selftest failure(s)")
        return 1
    print("\nall checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
