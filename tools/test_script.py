#!/usr/bin/env python3
"""Tests for the featural block script renderer (tools/script.py, v0.2)."""

import contextlib
import io
import itertools
import json
import sys
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from phonology import Syllable  # noqa: E402
from script import (BLOCK, DOT_R, DOT_X, DOT_Y, RULE_X,  # noqa: E402
                    STRIP_Y0, STRIP_Y1, ScriptRenderer, main,
                    raster_distance, rasterize, specimen)


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
        w = float(el.get("stroke-width", 0))
        if el.tag == "line":
            y0, y1 = float(el.get("y1")), float(el.get("y2"))
            ymin = min(ymin, min(y0, y1) - w)   # half-width + cap <= w
            ymax = max(ymax, max(y0, y1) + w)
        elif el.tag == "circle":
            cy, r = float(el.get("cy")), float(el.get("r"))
            ymin = min(ymin, cy - r - w / 2)
            ymax = max(ymax, cy + r + w / 2)
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

    def test_onset_ink_clear_of_strip_and_carrier(self):
        for o in self.inv.content_onsets + ["h"]:
            parts = self.r._onset(o)
            _, ymax = ink_bounds(parts)
            self.assertLess(ymax, STRIP_Y0, o)
            for el in parse_parts(parts):
                xs = []
                if el.tag == "line":
                    xs = [float(el.get("x1")), float(el.get("x2"))]
                elif el.tag == "circle":
                    xs = [float(el.get("cx")) + float(el.get("r"))]
                w = float(el.get("stroke-width", 0))
                self.assertLess(max(xs) + w, 74 - 2.5, o)

    def test_check_dot_clear_of_high_back_tick(self):
        # the u-tick and the check dot must not touch
        tick = [el for el in parse_parts(self.r._vowel("u"))
                if el.tag == "line" and el.get("y1") == el.get("y2")][0]
        tick_top = float(tick.get("y1")) - float(tick.get("stroke-width"))
        dot_bottom = DOT_Y + DOT_R
        self.assertGreater(tick_top - dot_bottom, 1.0)

    def test_unsupported_recipe_rejected(self):
        # feature-grid cells without a verified recipe must raise,
        # not silently render a bare base
        self.r.onset_features["_x"] = {"base": "angle",
                                      "modifier": "crossed"}
        try:
            with self.assertRaises(ValueError):
                self.r._onset("_x")
        finally:
            del self.r.onset_features["_x"]


class TestRasterFloor(unittest.TestCase):
    """Small-size legibility regression floor: occupancy-grid distances
    at a 14x14 raster of the onset zone (~14 px rendering). Thresholds
    sit below currently measured minima; a geometry change that erodes
    a distinction trips them (the v0.1 collapses scored near zero)."""

    @classmethod
    def setUpClass(cls):
        cls.r = ScriptRenderer()
        cls.inv = cls.r.inv
        cls.onsets = cls.inv.content_onsets + ["h"]
        cls.grids = {o: rasterize(cls.r._onset(o), 4, 4, 70, 62, 14)
                     for o in cls.onsets}
        spec = json.loads(
            (Path(__file__).resolve().parent.parent / "docs" / "spec" /
             "channels.json").read_text())
        cls.phonetic = set()
        for grp in (spec["covered_confusion_pairs"]["onset"],
                    spec["confusion_policy"]["forbidden"].get("onset", []),
                    spec["confusion_policy"]["weighted"].get("onset", [])):
            for a, b in grp:
                cls.phonetic.add(frozenset((a, b)))

    def test_all_onset_pairs_above_floor(self):
        for a, b in itertools.combinations(self.onsets, 2):
            d = raster_distance(self.grids[a], self.grids[b])
            self.assertGreaterEqual(d, 0.20, f"{a}/{b} at {d:.3f}")

    def test_phonetic_pairs_far_apart(self):
        # the anti-iconic code's payoff: ear-confusable pairs are
        # visually FAR (v0.1 equivalents scored near-collapse)
        for p in self.phonetic:
            a, b = tuple(p)
            d = raster_distance(self.grids[a], self.grids[b])
            self.assertGreaterEqual(d, 0.60, f"{a}/{b} at {d:.3f}")

    def test_coda_marks_far_apart(self):
        grids = {c: rasterize(self.r._coda(c), 8, 70, 92, 96, 12)
                 for c in ("n", "s", "l")}
        for a, b in itertools.combinations(("n", "s", "l"), 2):
            d = raster_distance(grids[a], grids[b])
            self.assertGreaterEqual(d, 0.55, f"{a}/{b} at {d:.3f}")

    def test_vowel_ticks_distinct_at_small_size(self):
        grids = {v: rasterize(self.r._vowel(v), 58, 8, 92, 66, 12)
                 for v in self.inv.vowels}
        for a, b in itertools.combinations(self.inv.vowels, 2):
            d = raster_distance(grids[a], grids[b])
            self.assertGreater(d, 0.10, f"{a}/{b} at {d:.3f}")


class TestCheckMarking(unittest.TestCase):
    """Check slot: lexical dot iff written check 1 (= romanization
    doubling); payload blocks carry no slot mark — payload words carry
    the run-rule instead."""

    @classmethod
    def setUpClass(cls):
        cls.r = ScriptRenderer()
        cls.inv = cls.r.inv

    def slot_dot(self, syl, payload):
        marks = [el for el in parse_parts(self.r._check(syl, payload))
                 if el.tag == "circle"
                 and float(el.get("cx")) == DOT_X
                 and float(el.get("cy")) == DOT_Y
                 and el.get("fill") == "currentColor"]
        return bool(marks)

    def test_dot_iff_lexical_check(self):
        for syl in self.inv.iter_triples(self.inv.content_onsets):
            has_dot = self.slot_dot(syl, payload=False)
            roman = self.inv.romanize_syllable(syl)
            self.assertEqual(has_dot, self.inv.register(syl) == 1, syl)
            self.assertEqual(has_dot, syl.vowel * 2 in roman, syl)

    def test_payload_blocks_carry_no_slot_mark(self):
        for syl in self.inv.iter_triples(self.inv.content_onsets):
            self.assertFalse(self.slot_dot(syl, payload=True), syl)

    def test_payload_word_carries_run_rule(self):
        sylls = [Syllable("m", "a", ""), Syllable("m", "i", "")]
        lex, _, _ = self.r.word_glyph(sylls)
        pay, _, h = self.r.word_glyph(sylls, payload=True)
        rules = [el for el in parse_parts(pay)
                 if el.tag == "line" and float(el.get("x1")) == RULE_X]
        self.assertEqual(len(rules), 1)
        self.assertEqual(float(rules[0].get("y2")), h - 4)
        self.assertFalse([el for el in parse_parts(lex)
                          if el.tag == "line"
                          and float(el.get("x1")) == RULE_X])


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

    def test_horizontal_layout_runs_left_to_right(self):
        sylls = [Syllable("s", "a", ""), Syllable("l", "a", "n")]
        parts, w, h = self.r.word_glyph_horizontal(sylls)
        self.assertEqual((w, h), (2 * BLOCK, BLOCK))
        heads = [el for el in parse_parts(parts)
                 if el.tag == "line" and float(el.get("y1")) == 4
                 and float(el.get("y2")) == 4]
        self.assertEqual(len(heads), 1)
        self.assertEqual(float(heads[0].get("x2")), 2 * BLOCK - 4)

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

    def test_invalid_coda_rejected(self):
        with self.assertRaises(ValueError):
            self.r.syllable_block(Syllable("t", "a", "x"))

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
        for argv in (["word", "sala"], ["payload", "ma"],
                     ["particle", "hu"], ["specimen"]):
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                self.assertEqual(main(argv), 0, argv)
            ET.fromstring(buf.getvalue().strip().splitlines()[-1])

    def test_bad_arity_and_operands_exit_two(self):
        for argv in ([], ["word"], ["payload"], ["particle"],
                     ["particle", "hu", "ha"], ["particle", "sala"],
                     ["particle", "sa"], ["specimen", "--out"],
                     ["specimen", "stray"], ["frobnicate"]):
            with contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(main(argv), 2, argv)


if __name__ == "__main__":
    unittest.main()
