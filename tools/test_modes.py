#!/usr/bin/env python3
"""Tests for modes.py. Run: python3 tools/test_modes.py"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from modes import LETTERS, MODE_PARTICLES, Modes, worked_examples
from phonology import Syllable

M = Modes()


class TestDigitPairs(unittest.TestCase):
    def test_round_trip_all_pairs(self):
        for v in range(100):
            syl = M.digit_pair_syllable(v)
            self.assertEqual(M.syllable_digit_pair(syl), v)

    def test_pair_syllables_unique(self):
        seen = {M.digit_pair_syllable(v) for v in range(100)}
        self.assertEqual(len(seen), 100)

    def test_number_pairs(self):
        self.assertEqual(M.number_pairs(0), [0])
        self.assertEqual(M.number_pairs(7), [7])
        self.assertEqual(M.number_pairs(207), [2, 7])
        self.assertEqual(M.number_pairs(4207), [42, 7])
        self.assertEqual(M.number_pairs(1000000), [1, 0, 0, 0])
        for n in (0, 5, 99, 100, 4207, 123456789):
            self.assertEqual(M.decode_number_pairs(M.number_pairs(n)), n)


class TestTime(unittest.TestCase):
    def test_all_96_cells_round_trip(self):
        seen = set()
        for hour in range(24):
            for quarter in (0, 15, 30, 45):
                syl = M.time_syllable(hour, quarter)
                seen.add(syl)
                self.assertEqual(M.decode_time_syllable(syl), (hour, quarter))
        self.assertEqual(len(seen), 96)

    def test_time_is_one_payload_syllable(self):
        out = M.encode_time(14, 30)
        self.assertEqual(len(out), 2)  # particle + one syllable

    def test_invalid_time_syllable_rejected(self):
        # hour tens coda s with last digit 4+ would exceed 23... e.g. 24+
        bad = Syllable(M.tens_onset[4], "a", "s")  # would be hour 24
        with self.assertRaises(ValueError):
            M.decode_time_syllable(bad)


class TestChecksum(unittest.TestCase):
    def test_catches_single_pair_substitution(self):
        pairs = [42, 7, 93]
        base = M.checksum(pairs)
        for i in range(len(pairs)):
            for delta in (1, 9, 50):
                mutated = pairs[:]
                mutated[i] = (mutated[i] + delta) % 100
                if mutated != pairs:
                    self.assertNotEqual(M.checksum(mutated), base,
                                        f"missed substitution at {i} +{delta}")

    def test_catches_adjacent_transposition(self):
        pairs = [42, 7, 93, 15]
        base = M.checksum(pairs)
        for i in range(len(pairs) - 1):
            if pairs[i] == pairs[i + 1]:
                continue
            mutated = pairs[:]
            mutated[i], mutated[i + 1] = mutated[i + 1], mutated[i]
            self.assertNotEqual(M.checksum(mutated), base, f"transposition {i}")


class TestSpell(unittest.TestCase):
    def test_letter_table_complete_and_unique(self):
        self.assertEqual(set(LETTERS), set("abcdefghijklmnopqrstuvwxyz"))
        self.assertEqual(len(set(LETTERS.values())), 26)

    def test_letter_syllables_are_legal_payload_shapes(self):
        for o, v, c in LETTERS.values():
            self.assertIn(o, list(M.inv.onset_records))
            self.assertIn(v, M.inv.vowels)
            self.assertIn(c, M.inv.codas)


class TestParticlesAndExamples(unittest.TestCase):
    def test_mode_particles_unique_h_syllables(self):
        seen = set()
        for mode, (v, c) in MODE_PARTICLES.items():
            self.assertIn(v, M.inv.vowels, mode)
            self.assertIn(c, M.inv.codas, mode)
            seen.add((v, c))
        self.assertEqual(len(seen), len(MODE_PARTICLES))

    def test_examples_match_doc(self):
        doc = (Path(__file__).resolve().parent.parent
               / "docs" / "spec" / "modes.md").read_text()
        for label, rendering in worked_examples(M):
            self.assertIn(f"`{rendering}`", doc,
                          f"doc example missing/stale for {label}: {rendering}")

    def test_confusion_analysis_accounting(self):
        stats = M.digit_confusion_analysis()
        self.assertEqual(stats["total"], 100 * (9 + 4 + 3))
        self.assertEqual(stats["silent"] + stats["mode_gram"], stats["total"])
        self.assertLessEqual(stats["silent_register_flagged"], stats["silent"])
        # coda s/l corruptions are exactly the mode-grammar-detected class
        self.assertEqual(stats["mode_gram"], 200)


if __name__ == "__main__":
    unittest.main(verbosity=1)
