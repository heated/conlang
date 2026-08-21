#!/usr/bin/env python3
"""Tests for modes.py. Run: python3 tools/test_modes.py"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from modes import (CHECKSUM_MOD, LETTER_ORDER, LETTERS, MAX_FRAME_SYMBOLS,
                   MODE_PARTICLES, FrameError, Modes, confusion_block,
                   examples_block, letters_block, particles_block)
from phonology import Syllable

M = Modes()
DOC = (Path(__file__).resolve().parent.parent / "docs" / "spec" / "modes.md")


class TestDigitPairs(unittest.TestCase):
    def test_round_trip_all_pairs(self):
        for v in range(100):
            self.assertEqual(M.syllable_digit_pair(M.digit_pair_syllable(v)), v)

    def test_pair_syllables_unique(self):
        self.assertEqual(len({M.digit_pair_syllable(v) for v in range(100)}), 100)

    def test_number_pairs(self):
        self.assertEqual(M.number_pairs(0), [0])
        self.assertEqual(M.number_pairs(207), [2, 7])
        self.assertEqual(M.number_pairs(4207), [42, 7])
        for n in (0, 5, 99, 100, 4207, 123456789):
            self.assertEqual(M._fold(M.number_pairs(n)), n)


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
        self.assertEqual(len(M.encode_time(14, 30)), 2)

    def test_invalid_time_syllables_rejected(self):
        with self.assertRaises(ValueError):  # would be hour 24
            M.decode_time_syllable(Syllable(M.tens_onset[4], "a", "s"))
        with self.assertRaises(ValueError):  # vowel u is reserved
            M.decode_time_syllable(Syllable(M.tens_onset[1], "u", ""))
        with self.assertRaises(ValueError):  # coda l is no hour-tens
            M.decode_time_syllable(Syllable(M.tens_onset[1], "a", "l"))


class TestChecksum(unittest.TestCase):
    def test_exhaustive_single_substitution(self):
        # any single value substitution at any position changes the sum
        base_vals = [0, 42, 99, 100, 7]
        base = M.checksum(base_vals)
        for i in range(len(base_vals)):
            for new in range(101):
                if new == base_vals[i]:
                    continue
                mutated = base_vals[:]
                mutated[i] = new
                self.assertNotEqual(M.checksum(mutated), base,
                                    f"silent substitution at {i}: {new}")

    def test_exhaustive_transpositions_all_distances(self):
        vals = [0, 97, 1, 98, 2, 99, 100, 50]
        base = M.checksum(vals)
        n = len(vals)
        for i in range(n):
            for j in range(i + 1, n):
                if vals[i] == vals[j]:
                    continue
                mutated = vals[:]
                mutated[i], mutated[j] = mutated[j], mutated[i]
                self.assertNotEqual(M.checksum(mutated), base,
                                    f"silent transposition {i}<->{j}")

    def test_old_mod97_blind_spots_now_caught(self):
        # the review's counterexamples: 00<->97, 01<->98, 02<->99
        for a, b in ((0, 97), (1, 98), (2, 99)):
            self.assertNotEqual(M.checksum([a]), M.checksum([b]))
            self.assertNotEqual(M.checksum([a, b]), M.checksum([b, a]))

    def test_frame_cap_and_range(self):
        with self.assertRaises(FrameError):
            M.checksum([1] * (MAX_FRAME_SYMBOLS + 1))
        with self.assertRaises(FrameError):
            M.checksum([101])
        self.assertEqual(CHECKSUM_MOD, 101)

    def test_checksum_symbol_round_trip(self):
        for v in range(100):
            syl = M.checksum_syllable(v)
            self.assertEqual(M.read_checksum_syllable(syl), v)

    def test_residue_100_has_no_symbol(self):
        # v2 sparse codebook: no clean 101st syllable exists, so
        # residue 100 is unreachable by the chunking rule instead
        with self.assertRaises(FrameError):
            M.checksum_syllable(100)

    def test_chunking_rule_covers_residue_100(self):
        residue_100 = [n for n in range(2000)
                       if M.checksum(M.number_pairs(n)) == 100]
        self.assertGreater(len(residue_100), 5)
        for n in residue_100:
            chunks = M.chunk_payload(M.number_pairs(n))
            self.assertGreater(len(chunks), 1, n)
            for c in chunks:
                self.assertNotEqual(M.checksum(c), 100, (n, c))
            self.assertEqual([p for c in chunks for p in c],
                             M.number_pairs(n))
            frame = " ".join(M.encode_number(n, checksum=True))
            got = M.decode_frame(frame)
            self.assertEqual(got["value"], n, frame)
            self.assertTrue(got["checksum_ok"], frame)
            self.assertEqual(got["chunks"], len(chunks))

    def test_chunked_frame_detects_corruption(self):
        n = next(x for x in range(2000)
                 if M.checksum(M.number_pairs(x)) == 100)
        toks = M.encode_number(n, checksum=True)
        # corrupt the first chunk's payload syllable
        bad = list(toks)
        bad[1] = M.rom([M.digit_pair_syllable(
            (M.syllable_digit_pair(
                M.inv.parse_word(toks[1], mode="structural")[0]) + 1) % 100)])[0]
        self.assertFalse(M.decode_frame(" ".join(bad))["checksum_ok"])


class TestFrameDecoding(unittest.TestCase):
    def test_number_round_trip(self):
        for n in (0, 7, 42, 4207, 1000000, 987654321):
            for cs in (False, True):
                frame = " ".join(M.encode_number(n, checksum=cs))
                d = M.decode_frame(frame)
                self.assertEqual(d["mode"], "number")
                self.assertEqual(d["value"], n)
                self.assertEqual(d["checksum_ok"], True if cs else None)

    def test_date_round_trip_and_wire_rule(self):
        for year, m_, d_ in (("2026", 8, 8), (None, 8, 8), ("0026", 12, 31),
                             ("120260", 1, 1)):
            frame = " ".join(M.encode_date(year, m_, d_, checksum=True))
            d = M.decode_frame(frame)
            self.assertEqual((d["year"], d["month"], d["day"]), (year, m_, d_))
            self.assertTrue(d["checksum_ok"])
        with self.assertRaises(ValueError):  # 2-digit year illegal on wire
            M.encode_date("26", 8, 8)

    def test_date_bad_lengths_rejected(self):
        # 3 payload pairs is not a legal date frame
        pairs = [M.digit_pair_syllable(p) for p in (20, 8, 8)]
        frame = "ho " + " ".join(M.rom(pairs))
        with self.assertRaises(FrameError):
            M.decode_frame(frame)

    def test_time_round_trip(self):
        for h, mi, s in ((14, 30, None), (14, 37, None), (8, 0, None),
                         (23, 45, None), (0, 0, None), (9, 59, 59)):
            frame = " ".join(M.encode_time(h, mi, s, checksum=True))
            d = M.decode_frame(frame)
            self.assertEqual((d["hour"], d["minute"], d["second"]), (h, mi, s))
            self.assertTrue(d["checksum_ok"])

    def test_spell_round_trip(self):
        for text in ("ntnu", "zoe", "abcdefghijklmnopqrstuvwxyz"):
            frame = " ".join(M.encode_spell(text, checksum=True))
            d = M.decode_frame(frame)
            self.assertEqual(d["text"], text)
            self.assertTrue(d["checksum_ok"])

    def test_corrupt_checksum_detected(self):
        frame = M.encode_number(4207, checksum=True)
        # corrupt one payload digit syllable (42 -> 52)
        frame[1] = M.rom([M.digit_pair_syllable(52)])[0]
        d = M.decode_frame(" ".join(frame))
        self.assertFalse(d["checksum_ok"])

    def test_bad_frames_rejected(self):
        bad = ["", "mi cin",                # no particle
               "haas mi",                   # close cannot open
               "huu",                       # empty payload
               "huu mi hoos",               # checksum symbol missing
               "huu mi haas cin",           # trailing tokens
               "hii kos kos",               # offset pair out of range (23:45 twice)
               "he mi"]                     # 'mi' is not a letter symbol...
        # note: 'mi' IS c-i-l? no: m-i, not a letter shape -> letter error
        for frame in bad:
            with self.assertRaises(FrameError, msg=repr(frame)):
                M.decode_frame(frame)

    def test_wrong_register_particle_rejected(self):
        # number particle is canonically 'huu' (lexical long); 'hu' is the
        # undoubled spelling and legal; but a WRONG doubling like 'hoo'
        # for the date particle (canonically short 'ho') must fail
        with self.assertRaises(FrameError):
            M.decode_frame("hoo ca ca")


class TestSpellTable(unittest.TestCase):
    def test_letter_table_complete_unique_no_h(self):
        self.assertEqual(set(LETTERS), set(LETTER_ORDER))
        self.assertEqual(len(set(LETTERS.values())), 26)
        for o, v, c in LETTERS.values():
            self.assertNotEqual(o, "h", "h-shapes banned from payloads")
            self.assertIn(o, list(M.inv.onset_records))
            self.assertIn(v, M.inv.vowels)
            self.assertIn(c, M.inv.codas)


class TestGeneratedDocBlocks(unittest.TestCase):
    def _assert_block_in_doc(self, block: str, name: str):
        doc = DOC.read_text()
        self.assertIn(block, doc, f"{name} block stale — regenerate "
                                  f"(python3 tools/modes.py {name})")

    def test_examples_block(self):
        self._assert_block_in_doc(examples_block(M), "examples")

    def test_particles_block(self):
        self._assert_block_in_doc(particles_block(M), "particles")

    def test_letters_block(self):
        self._assert_block_in_doc(letters_block(M), "letters")

    def test_confusion_block(self):
        self._assert_block_in_doc(confusion_block(M), "confusion")

    def test_mode_particles_unique(self):
        self.assertEqual(len(set(MODE_PARTICLES.values())),
                         len(MODE_PARTICLES))

    def test_confusion_accounting(self):
        stats = M.digit_confusion_analysis()
        self.assertEqual(stats["total"], 100 * (9 + 4 + 3))
        self.assertEqual(stats["silent"] + stats["mode_gram"], stats["total"])
        # v2 sparse codebook (2026-08-22 spec bump): the codebook uses
        # 100 of the 200 content cells, so single-channel corruptions
        # land outside it more often — frame-grammar catches rose
        # 200 -> 280, silent substitutions fell 1400 -> 1320 (87% ->
        # 82%). The sparse codebook is a free error-detection gain.
        self.assertEqual(stats["mode_gram"], 280)
        self.assertEqual(stats["silent"], 1320)
        self.assertEqual(stats["silent_register_flagged"], 780)


if __name__ == "__main__":
    unittest.main(verbosity=1)
