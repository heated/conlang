#!/usr/bin/env python3
"""Tests for the featural block script renderer (tools/script.py)."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from phonology import Inventory, Syllable  # noqa: E402
from script import BLOCK, ScriptRenderer, specimen  # noqa: E402


def block_key(renderer, syl, payload=False):
    return "".join(renderer.syllable_block(syl, payload=payload))


class TestDeterminism(unittest.TestCase):
    def test_same_syllable_same_output(self):
        r1, r2 = ScriptRenderer(), ScriptRenderer()
        syl = Syllable("s", "a", "n")
        self.assertEqual(block_key(r1, syl), block_key(r2, syl))
        self.assertEqual(block_key(r1, syl), block_key(r1, syl))

    def test_specimen_deterministic(self):
        r = ScriptRenderer()
        self.assertEqual(specimen(r), specimen(r))


class TestDistinctness(unittest.TestCase):
    """All 220 syllable blocks (200 content + 20 particle) must have
    pairwise-distinct path data, in both lexical and payload modes."""

    @classmethod
    def setUpClass(cls):
        cls.r = ScriptRenderer()
        cls.inv = cls.r.inv
        cls.triples = list(cls.inv.iter_triples(
            cls.inv.content_onsets + ["h"]))

    def test_220_syllables(self):
        content = [s for s in self.triples if s.onset != "h"]
        self.assertEqual(len(content), 200)
        self.assertEqual(len(self.triples), 220)

    def test_lexical_blocks_distinct(self):
        seen = {}
        for syl in self.triples:
            key = block_key(self.r, syl)
            self.assertNotIn(key, seen,
                             f"{syl} collides with {seen.get(key)}")
            seen[key] = syl

    def test_payload_blocks_distinct(self):
        seen = {}
        for syl in self.triples:
            key = block_key(self.r, syl, payload=True)
            self.assertNotIn(key, seen,
                             f"{syl} collides with {seen.get(key)}")
            seen[key] = syl

    def test_banned_glide_cells_still_render(self):
        # ji/wu are phonotactic exclusions, not visual ones
        for o, v in (("j", "i"), ("w", "u")):
            parts = self.r.syllable_block(Syllable(o, v, ""))
            self.assertTrue(parts)


class TestCheckMarking(unittest.TestCase):
    """Glyph check slot must agree with the written-layer check
    (dot <=> romanization doubling) and with payload polarity."""

    @classmethod
    def setUpClass(cls):
        cls.r = ScriptRenderer()
        cls.inv = cls.r.inv

    def test_dot_iff_lexical_check(self):
        for syl in self.inv.iter_triples(self.inv.content_onsets):
            key = block_key(self.r, syl)
            has_dot = 'fill="currentColor"' in key
            roman = self.inv.romanize_syllable(syl)
            doubled = syl.vowel * 2 in roman
            self.assertEqual(has_dot, self.inv.register(syl) == 1, syl)
            self.assertEqual(has_dot, doubled, syl)

    def test_ring_iff_payload_polarity(self):
        for syl in self.inv.iter_triples(self.inv.content_onsets):
            key = block_key(self.r, syl, payload=True)
            has_ring = 'r="4.5" stroke="currentColor"' in key
            self.assertNotIn('fill="currentColor"', key, syl)
            self.assertEqual(
                has_ring, self.inv.register(syl, payload=True) == 1, syl)

    def test_lexical_and_payload_blocks_always_differ(self):
        # payload polarity is the anti-check, so exactly one of the two
        # modes marks the slot for every syllable
        for syl in self.inv.iter_triples(self.inv.content_onsets):
            self.assertNotEqual(block_key(self.r, syl),
                                block_key(self.r, syl, payload=True), syl)


class TestAssembly(unittest.TestCase):
    def setUp(self):
        self.r = ScriptRenderer()

    def test_word_glyph_stacks_vertically(self):
        sylls = [Syllable("s", "a", ""), Syllable("l", "a", "n")]
        parts, w, h = self.r.word_glyph(sylls)
        self.assertEqual((w, h), (BLOCK, 2 * BLOCK))
        three = [Syllable("t", "a", ""), Syllable("k", "o", ""),
                 Syllable("m", "e", "s")]
        _, w3, h3 = self.r.word_glyph(three)
        self.assertEqual((w3, h3), (BLOCK, 3 * BLOCK))

    def test_particle_glyph_is_scaled_block(self):
        parts, w, h = self.r.particle_glyph(Syllable("h", "u", ""))
        self.assertLess(w, BLOCK)
        self.assertIn("scale(0.7)", parts[0])

    def test_invalid_onset_rejected(self):
        with self.assertRaises(KeyError):
            self.r.syllable_block(Syllable("x", "a", ""))

    def test_invalid_vowel_rejected(self):
        with self.assertRaises(KeyError):
            self.r.syllable_block(Syllable("t", "y", ""))

    def test_specimen_covers_all_syllables(self):
        r = ScriptRenderer()
        svg = specimen(r)
        inv = r.inv
        for syl in inv.iter_triples(inv.content_onsets):
            self.assertIn(f">{inv.romanize_syllable(syl)}</text>", svg)
        for syl in inv.iter_triples(["h"]):
            self.assertIn(f">{inv.romanize_syllable(syl)}</text>", svg)

    def test_svg_wellformed(self):
        import xml.etree.ElementTree as ET
        r = ScriptRenderer()
        ET.fromstring(specimen(r))
        sylls = r.inv.parse_word("salaan", mode="lexical")
        parts, w, h = r.word_glyph(sylls)
        ET.fromstring(r.svg(parts, w, h))


if __name__ == "__main__":
    unittest.main()
