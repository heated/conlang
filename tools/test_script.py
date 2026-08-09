#!/usr/bin/env python3
"""Tests for the featural block script renderer (tools/script.py)."""

import sys
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from phonology import Syllable  # noqa: E402
from script import (BLOCK, DOT_R, DOT_X, DOT_Y, STRIP_Y0, STRIP_Y1,  # noqa: E402
                    ScriptRenderer, main, specimen)


def block_key(renderer, syl, payload=False):
    return "".join(renderer.syllable_block(syl, payload=payload))


def parse_parts(parts):
    """Parse a list of SVG fragments into elements."""
    return list(ET.fromstring("<svg>" + "".join(parts) + "</svg>"))


def ink_bounds(parts):
    """(ymin, ymax) of all ink in the fragments, including stroke
    half-widths and round caps."""
    ymin, ymax = float("inf"), float("-inf")
    for el in parse_parts(parts):
        tag = el.tag
        w = float(el.get("stroke-width", 0))
        if tag == "line":
            y0, y1 = float(el.get("y1")), float(el.get("y2"))
            lo, hi = min(y0, y1), max(y0, y1)
            ymin = min(ymin, lo - w)      # half-width + round cap <= w
            ymax = max(ymax, hi + w)
        elif tag == "circle":
            cy, r = float(el.get("cy")), float(el.get("r"))
            ymin = min(ymin, cy - r - w / 2)
            ymax = max(ymax, cy + r + w / 2)
        elif tag == "path":
            ys = []
            tokens = el.get("d").replace(",", " ").split()
            # M x y A rx ry rot large sweep x y — take explicit y coords
            ys = [float(tokens[2]), float(tokens[-1])]
            r = float(tokens[4])
            for y in ys:
                ymin = min(ymin, y - r - w)
                ymax = max(ymax, y + r + w)
    return ymin, ymax


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


class TestZoneGeometry(unittest.TestCase):
    """Distinctness must hold per zone, independent of the derived
    check mark (which is recoverable and may be omitted by a font)."""

    @classmethod
    def setUpClass(cls):
        cls.r = ScriptRenderer()
        cls.inv = cls.r.inv

    def test_onset_letters_pairwise_distinct(self):
        forms = {o: "".join(self.r._onset(o))
                 for o in self.inv.content_onsets + ["h"]}
        self.assertEqual(len(set(forms.values())), 11, forms)

    def test_vowel_carriers_pairwise_distinct(self):
        forms = {v: "".join(self.r._vowel(v)) for v in self.inv.vowels}
        self.assertEqual(len(set(forms.values())), 5, forms)

    def test_coda_marks_pairwise_distinct(self):
        forms = {c: "".join(self.r._coda(c)) for c in self.inv.codas}
        self.assertEqual(len(set(forms.values())), 4, forms)

    def test_coda_ink_stays_in_strip(self):
        for c in self.inv.codas:
            if not c:
                continue
            ymin, ymax = ink_bounds(self.r._coda(c))
            self.assertGreaterEqual(ymin, STRIP_Y0 - 0.5, c)
            self.assertLessEqual(ymax, STRIP_Y1 + 0.5, c)

    def test_mini_s_strokes_do_not_overlap(self):
        # the doubled vertical must survive miniaturization: gap between
        # stroke edges must be positive (Fable finding 2a)
        lines = [el for el in parse_parts(self.r._coda("s"))
                 if el.tag == "line"]
        self.assertEqual(len(lines), 2)
        xs = sorted(float(el.get("x1")) for el in lines)
        w = float(lines[0].get("stroke-width"))
        self.assertGreater(xs[1] - xs[0] - w, 0.5)

    def test_check_dot_clear_of_high_back_tick(self):
        # Fable finding 1: the u-tick and the check mark must not touch
        tick = [el for el in parse_parts(self.r._vowel("u"))
                if el.tag == "line" and el.get("y1") == el.get("y2")][0]
        tick_top = float(tick.get("y1")) - float(tick.get("stroke-width"))
        ring_bottom = DOT_Y + DOT_R + 2.5 / 2  # ring outer edge
        self.assertGreater(tick_top - ring_bottom, 1.0)

    def test_unsupported_recipe_rejected(self):
        # wide-model grid cells without a verified recipe must raise,
        # not silently render a bare base (Codex finding 2)
        self.r.onset_features["_x"] = {"place": "velar",
                                      "manner": "approximant"}
        try:
            with self.assertRaises(ValueError):
                self.r._onset("_x")
        finally:
            del self.r.onset_features["_x"]


class TestCheckMarking(unittest.TestCase):
    """Glyph check slot must agree with the written-layer check
    (dot <=> romanization doubling) and with payload polarity."""

    @classmethod
    def setUpClass(cls):
        cls.r = ScriptRenderer()
        cls.inv = cls.r.inv

    def slot_mark(self, syl, payload):
        """Return 'dot', 'ring', or None from parsed check-slot ink."""
        marks = [el for el in parse_parts(
                     self.r._check(syl, payload))
                 if el.tag == "circle"
                 and float(el.get("cx")) == DOT_X
                 and float(el.get("cy")) == DOT_Y]
        if not marks:
            return None
        el = marks[0]
        if el.get("fill") == "currentColor":
            return "dot"
        self.assertEqual(el.get("fill"), "none")
        self.assertEqual(el.get("stroke"), "currentColor")
        return "ring"

    def test_dot_iff_lexical_check(self):
        for syl in self.inv.iter_triples(self.inv.content_onsets):
            mark = self.slot_mark(syl, payload=False)
            roman = self.inv.romanize_syllable(syl)
            doubled = syl.vowel * 2 in roman
            want = "dot" if self.inv.register(syl) == 1 else None
            self.assertEqual(mark, want, syl)
            self.assertEqual(mark == "dot", doubled, syl)

    def test_ring_iff_payload_polarity(self):
        for syl in self.inv.iter_triples(self.inv.content_onsets):
            mark = self.slot_mark(syl, payload=True)
            want = ("ring" if self.inv.register(syl, payload=True) == 1
                    else None)
            self.assertEqual(mark, want, syl)

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
        r = ScriptRenderer()
        ET.fromstring(specimen(r))
        sylls = r.inv.parse_word("salaan", mode="lexical")
        parts, w, h = r.word_glyph(sylls)
        ET.fromstring(r.svg(parts, w, h))


class TestCLI(unittest.TestCase):
    def test_valid_paths_exit_zero(self):
        import contextlib
        import io
        for argv in (["word", "sala"], ["payload", "ma"],
                     ["particle", "hu"], ["specimen"]):
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                self.assertEqual(main(argv), 0, argv)
            ET.fromstring(buf.getvalue().strip().splitlines()[-1])

    def test_bad_arity_and_operands_exit_two(self):
        import contextlib
        import io
        for argv in ([], ["word"], ["payload"], ["particle"],
                     ["particle", "hu", "ha"], ["particle", "sala"],
                     ["particle", "sa"], ["specimen", "--out"],
                     ["specimen", "stray"], ["frobnicate"]):
            with contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(main(argv), 2, argv)


if __name__ == "__main__":
    unittest.main()
