#!/usr/bin/env python3
"""Tests for phonology.py and lexgen.py. Run: python3 tools/test_phonology.py"""

import sys
import unittest
from itertools import combinations
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lexgen import body_conflict_graph, capacity_report, max_independent_set
from phonology import ConflictRules, Inventory, Syllable


INV = Inventory()
RULES = ConflictRules(INV)


class TestRegister(unittest.TestCase):
    def test_hand_computed_registers(self):
        # sala: sa (s0+a0+∅0=0 short), la (l0+a0+∅0=0 short)
        self.assertEqual(INV.register(Syllable("s", "a", "")), 0)
        self.assertEqual(INV.register(Syllable("l", "a", "")), 0)
        # lan: l0+a0+n1=1 long ; las: l0+a0+s1=1 long
        self.assertEqual(INV.register(Syllable("l", "a", "n")), 1)
        self.assertEqual(INV.register(Syllable("l", "a", "s")), 1)
        # payload mi: m0+i1+∅0=1 lexical-long -> payload short
        self.assertEqual(INV.register(Syllable("m", "i", ""), payload=True), 0)
        # payload cin: c1+i1+n1=3 odd -> payload short
        self.assertEqual(INV.register(Syllable("c", "i", "n"), payload=True), 0)

    def test_derivation_example_romanization(self):
        sa, la = Syllable("s", "a", ""), Syllable("l", "a", "")
        lan, las = Syllable("l", "a", "n"), Syllable("l", "a", "s")
        self.assertEqual(INV.romanize_word([sa, la]), "sala")
        self.assertEqual(INV.romanize_word([sa, lan]), "salaan")
        self.assertEqual(INV.romanize_word([sa, las]), "salaas")


class TestParseRoundTrip(unittest.TestCase):
    def test_all_syllables_round_trip(self):
        for syl in INV.lexical_content_syllables() + INV.particle_syllables():
            for double in (True, False):
                text = INV.romanize_syllable(syl, double_long=double)
                parsed = INV.parse_word(text)
                self.assertEqual(parsed, [syl], f"round trip failed: {text}")

    def test_multisyllable_parse(self):
        self.assertEqual(INV.parse_word("salaan"),
                         [Syllable("s", "a", ""), Syllable("l", "a", "n")])
        # coda vs onset disambiguation: 'sana' = sa.na, not san.a
        self.assertEqual(INV.parse_word("sana"),
                         [Syllable("s", "a", ""), Syllable("n", "a", "")])

    def test_parse_rejects_garbage(self):
        for bad in ("asa", "s", "sq", "hhh", ""):
            if bad == "":
                self.assertEqual(INV.parse_word(bad), [])
                continue
            with self.assertRaises(ValueError, msg=bad):
                INV.parse_word(bad)

    def test_parse_register_checking(self):
        # 'can' is lexical-short: doubling asserts a false long register
        with self.assertRaises(ValueError):
            INV.parse_word("caan", mode="lexical")
        self.assertEqual(len(INV.parse_word("caan", mode="structural")), 1)
        # 'mii' is lexical-long: doubling fine lexically, wrong for payload
        self.assertEqual(len(INV.parse_word("mii", mode="lexical")), 1)
        with self.assertRaises(ValueError):
            INV.parse_word("mii", mode="payload")
        # undoubled spelling of a long syllable is always acceptable
        self.assertEqual(INV.parse_word("mi", mode="lexical"),
                         INV.parse_word("mii", mode="lexical"))
        # multisyllable: false doubling on first syllable of salaan
        with self.assertRaises(ValueError):
            INV.parse_word("saalaan", mode="lexical")


class TestValidation(unittest.TestCase):
    def test_glide_cells_rejected(self):
        self.assertTrue(INV.validate_content_word([Syllable("j", "i", "")]))
        self.assertTrue(INV.validate_content_word([Syllable("w", "u", "n")]))
        self.assertFalse(INV.validate_content_word([Syllable("j", "a", "")]))

    def test_shapes(self):
        s = Syllable("t", "a", "")
        self.assertTrue(INV.validate_content_word([s, s, s, s]))  # 4 syllables
        self.assertFalse(INV.validate_content_word([s, s, s]))
        self.assertTrue(INV.validate_particle([s]))          # wrong onset
        self.assertFalse(INV.validate_particle([Syllable("h", "a", "")]))
        self.assertTrue(INV.validate_content_word([Syllable("h", "a", "")]))

    def test_reserved_pos_rejected(self):
        self.assertTrue(INV.validate_content_word([Syllable("t", "a", "l")]))


class TestConflictRules(unittest.TestCase):
    def test_forbidden_and_weighted(self):
        pa, ka = [Syllable("p", "a", "")], [Syllable("k", "a", "")]
        self.assertEqual(RULES.classify_pair(pa, ka), "forbidden")
        # humility assignment (conlang-bf2): covered pairs are banned for
        # unrelated minimal pairs too
        pa2, ta = [Syllable("p", "a", "")], [Syllable("t", "a", "")]
        self.assertEqual(RULES.classify_pair(pa2, ta), "forbidden")
        se, si = [Syllable("s", "e", "")], [Syllable("s", "i", "")]
        self.assertEqual(RULES.classify_pair(se, si), "forbidden")  # e/i covered
        pa2, ma = [Syllable("p", "a", "")], [Syllable("m", "a", "")]
        self.assertEqual(RULES.classify_pair(pa2, ma), "weighted")
        ta, sa = [Syllable("t", "a", "")], [Syllable("s", "a", "")]
        self.assertEqual(RULES.classify_pair(ta, sa), "ok")  # unlisted pair

    def test_coronal_i(self):
        ti, ci = [Syllable("t", "i", "")], [Syllable("c", "i", "")]
        self.assertEqual(RULES.classify_pair(ti, ci), "forbidden")
        ta, ca = [Syllable("t", "a", "")], [Syllable("c", "a", "")]
        self.assertEqual(RULES.classify_pair(ta, ca), "ok")

    def test_same_root_exemption(self):
        tan, tas = [Syllable("t", "a", "n")], [Syllable("t", "a", "s")]
        self.assertEqual(RULES.classify_pair(tan, tas), "weighted")
        self.assertEqual(RULES.classify_pair(tan, tas, same_root=True), "ok")

    def test_fake_geminate(self):
        self.assertTrue(RULES.fake_geminate(
            [Syllable("n", "a", "s"), Syllable("s", "a", "")]))
        self.assertFalse(RULES.fake_geminate(
            [Syllable("n", "a", "s"), Syllable("t", "a", "")]))

    def test_echo_vowel_final(self):
        nas = [Syllable("n", "a", "s")]
        nasu = [Syllable("n", "a", ""), Syllable("s", "u", "")]
        self.assertTrue(RULES.echo_vowel_conflict(nas, nasu))
        self.assertTrue(RULES.echo_vowel_conflict(nasu, nas))  # symmetric
        natu = [Syllable("n", "a", ""), Syllable("t", "u", "")]
        self.assertFalse(RULES.echo_vowel_conflict(nas, natu))
        # non-echo vowel: 'a' is not epenthetic
        nasa = [Syllable("n", "a", ""), Syllable("s", "a", "")]
        self.assertFalse(RULES.echo_vowel_conflict(nas, nasa))

    def test_echo_vowel_medial(self):
        # /nas.ta/ vs /na.su.ta/ — the medial case the review caught
        nasta = [Syllable("n", "a", "s"), Syllable("t", "a", "")]
        nasuta = [Syllable("n", "a", ""), Syllable("s", "u", ""),
                  Syllable("t", "a", "")]
        self.assertTrue(RULES.echo_vowel_conflict(nasta, nasuta))
        # differing suffix breaks the match
        nasuti = [Syllable("n", "a", ""), Syllable("s", "u", ""),
                  Syllable("t", "i", "")]
        self.assertFalse(RULES.echo_vowel_conflict(nasta, nasuti))

    def test_tosmabru_normalized(self):
        tas = [Syllable("t", "a", "s")]
        particles = [Syllable("h", "a", "")]
        # lexicon is normalized syllable tuples — spelling-independent
        tasa_word = (Syllable("t", "a", ""), Syllable("s", "a", ""))
        hazards = RULES.tosmabru_conflict(tas, particles, {tasa_word})
        self.assertEqual(len(hazards), 1)
        # canonical romanization of the hazard: 'ta' is check-long (t=1)
        self.assertEqual(hazards[0], "taasa")
        other = (Syllable("t", "a", ""), Syllable("s", "i", ""))
        self.assertEqual(RULES.tosmabru_conflict(tas, particles, {other}), [])

    def test_tosmabru_word_sequence(self):
        # merged stream parses as TWO monosyllabic words — still a hazard
        tas = [Syllable("t", "a", "s")]
        particles = [Syllable("h", "a", "")]
        ta = (Syllable("t", "a", ""),)
        sa = (Syllable("s", "a", ""),)
        self.assertEqual(len(RULES.tosmabru_conflict(tas, particles, {ta, sa})), 1)
        # coda-less word: no hazard possible
        na = [Syllable("n", "a", "")]
        self.assertEqual(RULES.tosmabru_conflict(na, particles, {ta, sa}), [])


class TestCapacity(unittest.TestCase):
    def test_mis_exact_on_small_graph(self):
        # triangle plus isolated node -> MIS size 2
        nodes = ["a", "b", "c", "d"]
        edges = {"a": {"b", "c"}, "b": {"a", "c"}, "c": {"a", "b"}, "d": set()}
        self.assertEqual(len(max_independent_set(nodes, edges)), 2)

    def test_mis_against_brute_force_oracle(self):
        import random
        rng = random.Random(42)
        for trial in range(60):
            n = rng.randint(1, 12)
            nodes = list(range(n))
            edges = {v: set() for v in nodes}
            for a, b in combinations(nodes, 2):
                if rng.random() < 0.35:
                    edges[a].add(b)
                    edges[b].add(a)
            best = 0
            for mask in range(1 << n):
                subset = [v for v in nodes if mask >> v & 1]
                if all(b not in edges[a] for a, b in combinations(subset, 2)):
                    best = max(best, len(subset))
            got = len(max_independent_set(nodes, edges))
            self.assertEqual(got, best, f"trial {trial}: MIS {got} != oracle {best}")

    def test_real_graph_independence_and_pinned_cardinality(self):
        exp = INV.spec["capacity_expected"]
        for policy, key in (("adopted", "monosyllable_root_bodies_adopted"),
                            ("strict", "monosyllable_root_bodies_strict")):
            bodies, edges = body_conflict_graph(INV, RULES, policy)
            mis = max_independent_set(bodies, edges)
            for a, b in combinations(mis, 2):
                self.assertNotIn(b, edges[a])
            self.assertEqual(len(mis), exp[key], policy)

    def test_report_matches_capacity_expected(self):
        rep = capacity_report(INV, RULES)
        for key, want in INV.spec["capacity_expected"].items():
            if key == "comment":
                continue
            self.assertEqual(rep[key], want, key)
        self.assertLess(rep["monosyllable_assignable_after_reserve"],
                        rep["monosyllable_root_bodies_adopted"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
