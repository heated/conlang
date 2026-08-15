#!/usr/bin/env python3
"""Tests for the RZ featural display renderer (workshop hardening)."""

import itertools
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from rz_script import (CODAS, RZ_ONSETS, SUFFIX_LOGOGRAMS,  # noqa: E402
                       coda_glyph, logogram, onset_glyph, to_phonemes,
                       word_glyph)
from script import rasterize, raster_distance  # noqa: E402

PH = [(0, 0), (2.4, 2.4), (4.8, 1.2), (1.2, 4.8)]


def pmin(a, b, size=70, n=14):
    return min(raster_distance(rasterize(a, px, py, size + px, size + py, n),
                               rasterize(b, px, py, size + px, size + py, n))
               for px, py in PH)


class TestParser(unittest.TestCase):
    TABLE = [
        ("poc", ["p", "o", "k"]),            # word-final c stays hard
        ("centro", ["ts", "e", "n", "t", "r", "o"]),
        ("gato", ["g", "a", "t", "o"]),
        ("gente", ["dZ", "e", "n", "t", "e"]),
        ("espania", ["e", "s", "p", "a", "ny", "a"]),
        ("linia", ["l", "i", "ny", "a"]),     # ni here IS intervocalic
        ("lion", ["l", "i", "o", "n"]),       # word-initial li: plain
        ("hodie", ["o", "d", "i", "e"]),       # h silent (declared)
        ("forza", ["f", "o", "r", "ts", "a"]),
        ("que", ["k", "e"]),
    ]

    def test_grapheme_rules(self):
        for word, want in self.TABLE:
            self.assertEqual(to_phonemes(word), want, word)

    def test_hyphenated_numbers_render(self):
        for w in ("dece-ses", "vinte-un", "dos-mil-vinte-ses"):
            word_glyph(w)


class TestGeometry(unittest.TestCase):
    def test_onset_letterforms_injective(self):
        forms = {ph: "".join(onset_glyph([ph])) for ph in RZ_ONSETS}
        self.assertEqual(len(set(forms.values())), len(RZ_ONSETS))

    def test_voicing_pairs_survive_small_raster(self):
        for vl, vd in (("p", "b"), ("t", "d"), ("k", "g"),
                       ("f", "v"), ("s", "z")):
            d = pmin(onset_glyph([vl]), onset_glyph([vd]))
            self.assertGreaterEqual(d, 0.15, f"{vl}/{vd} at {d:.3f}")

    def test_codas_and_logograms_distinct(self):
        for a, b in itertools.combinations([c for c in CODAS], 2):
            self.assertNotEqual("".join(coda_glyph(a)),
                                "".join(coda_glyph(b)))
        for a, b in itertools.combinations(SUFFIX_LOGOGRAMS, 2):
            d = pmin(logogram(a), logogram(b), size=60, n=12)
            self.assertGreaterEqual(d, 0.12, f"{a}/{b} at {d:.3f}")


class TestCorpus(unittest.TestCase):
    def test_full_corpus_renders(self):
        words = set()
        base = Path(__file__).resolve().parent.parent / "docs" / "design" / "zonal"
        for name in ("rz-texts.md",):
            for m in re.finditer(r'^> (.*)$', (base / name).read_text(), re.M):
                words.update(re.findall(r"[a-zA-Z-]+", m.group(1).lower()))
        for w in words:
            word_glyph(w.strip("-"))


if __name__ == "__main__":
    unittest.main()
