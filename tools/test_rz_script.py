#!/usr/bin/env python3
"""Tests for the RZ featural display renderer (workshop hardening).

Raster floors follow the greenfield methodology (test_script.py):
occupancy-grid distances minimized over sub-cell sampling phases, so
a floor can't be passed by a lucky grid alignment. Thresholds sit
below currently measured phase-minima; a geometry change that erodes
a distinction trips them. Measured 2026-08-22 (14px onsets / 7px
logograms): onset worst pair b/dZ 0.182; voicing worst f/v 0.371;
logogram worst mente/abile & mente/va 0.500; func-mark worst a/al
0.222. (The v0 -cion/-itate collapse scored 0.000 at 7px.)
"""

import itertools
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from rz_script import (CODAS, FUNC_MARKS, LEGAL_ONSETS,  # noqa: E402
                       RZ_ONSETS, SUFFIX_LOGOGRAMS, TENSE_LOGOGRAMS,
                       analyze, coda_glyph, logogram, onset_glyph,
                       onset_parts, to_phonemes, word_glyph)
from script import rasterize, raster_distance  # noqa: E402

# sub-cell sampling phases (greenfield methodology, Codex finding)
PHASES = [(px, py) for px in (0, 1.57, 3.14) for py in (0, 1.38, 2.76)]
ONSET_WIN = (2, 2, 66, 64)          # includes the voicing ground bar
LOGO_WIN = (2, 2, 50, 64)
FUNC_WIN = (4, 14, 40, 60)


def pmin(a, b, win, n):
    return min(
        raster_distance(
            rasterize(a, win[0] + px, win[1] + py, win[2] + px,
                      win[3] + py, n),
            rasterize(b, win[0] + px, win[1] + py, win[2] + px,
                      win[3] + py, n))
        for px, py in PHASES)


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

    def test_mode_particle_h_pronounced(self):
        # rz-number-mode.md: [h] is silent in RZ words, pronounced in
        # mode-frame particles — hu gets ink, hotel does not
        self.assertEqual(to_phonemes("hu"), ["h", "u"])
        self.assertEqual(to_phonemes("hotel"), ["o", "t", "e", "l"])
        parts, _ = word_glyph("hu")
        self.assertTrue(parts)


class TestMorphology(unittest.TestCase):
    """The verb-stem gate for tense logograms: suffix fires only when
    stripping it leaves a known verb stem."""

    TABLE = [
        ("parlava", ("parla", "va", "v")),
        ("parlaria", ("parla", "ria", "v")),
        ("materia", ("materia", None, None)),   # mate is not a verb
        ("historia", ("historia", None, None)),
        ("seria", ("seria", None, "v")),        # suppletive: plain + POS
        ("era", ("era", None, "v")),
        ("vento", ("vento", None, None)),
        ("parlar", ("parlar", None, "v")),      # known infinitive
    ]

    def test_analyze(self):
        for word, want in self.TABLE:
            self.assertEqual(analyze(word), want, word)

    def test_tagged_pos_input_renders(self):
        for w in ("manto:adj", "calde:a", "vento:n", "parlava:v"):
            parts, _ = word_glyph(w, pos=True)
            self.assertTrue(parts)

    def test_pos_underline_only_when_enabled(self):
        plain, _ = word_glyph("parlava", pos=False)
        marked, _ = word_glyph("parlava", pos=True)
        self.assertGreater(len(marked), len(plain))


class TestGeometry(unittest.TestCase):
    def test_onset_letterforms_injective(self):
        forms = {ph: "".join(onset_glyph([ph])) for ph in RZ_ONSETS}
        self.assertEqual(len(set(forms.values())), len(RZ_ONSETS))

    def test_all_onset_pairs_above_floor(self):
        glyphs = {ph: onset_glyph([ph]) for ph in RZ_ONSETS}
        for a, b in itertools.combinations(RZ_ONSETS, 2):
            d = pmin(glyphs[a], glyphs[b], ONSET_WIN, 14)
            self.assertGreaterEqual(d, 0.15, f"{a}/{b} at {d:.3f}")

    def test_voicing_pairs_survive_small_raster(self):
        # deliberate doctrine relaxation vs greenfield (secondary
        # layer): voicing pairs differ by ONE mark — the ground bar —
        # so the floor is 0.30, not the greenfield's 0.55 phonetic
        # floor. Measured min: f/v 0.371.
        for vl, vd in (("p", "b"), ("t", "d"), ("k", "g"),
                       ("f", "v"), ("s", "z")):
            d = pmin(onset_glyph([vl]), onset_glyph([vd]), ONSET_WIN, 14)
            self.assertGreaterEqual(d, 0.30, f"{vl}/{vd} at {d:.3f}")

    def test_h_distinct_from_tick_family(self):
        # h (tick doubled) vs ly (tick capped) was the known lookalike;
        # the ly cap is now wider+higher than its main bar
        for other in ("ly", "ny"):
            d = pmin(onset_glyph(["h"]), onset_glyph([other]),
                     ONSET_WIN, 14)
            self.assertGreaterEqual(d, 0.40, f"h/{other} at {d:.3f}")

    def test_codas_distinct(self):
        for a, b in itertools.combinations([c for c in CODAS], 2):
            self.assertNotEqual("".join(coda_glyph(a)),
                                "".join(coda_glyph(b)))

    def test_logograms_above_floor_at_7px(self):
        # the v0 -cion/-itate pair scored 0.000 here (review finding)
        logos = {s: logogram(s)
                 for s in SUFFIX_LOGOGRAMS + TENSE_LOGOGRAMS}
        for a, b in itertools.combinations(logos, 2):
            d = pmin(logos[a], logos[b], LOGO_WIN, 7)
            self.assertGreaterEqual(d, 0.40, f"{a}/{b} at {d:.3f}")

    def test_func_marks_above_floor(self):
        marks = {w: word_glyph(w)[0] for w in FUNC_MARKS}
        for a, b in itertools.combinations(marks, 2):
            d = pmin(marks[a], marks[b], FUNC_WIN, 10)
            self.assertGreaterEqual(d, 0.15, f"{a}/{b} at {d:.3f}")


class TestClusterLayout(unittest.TestCase):
    """Hangul-style mutual sizing invariant: satellite ink never lands
    on main-letter ink (fine-grid overlap <= 3% of satellite cells)."""

    def test_no_satellite_main_collision(self):
        for cl in sorted(LEGAL_ONSETS):
            if len(cl) < 2:
                continue
            main, sats = onset_parts(list(cl))
            win = (-10, -14, 70, 66)
            m = rasterize(main, *win, 60)
            s = rasterize(sats, *win, 60)
            frac = len(m & s) / len(s)
            self.assertLessEqual(
                frac, 0.03, f"{'+'.join(cl)}: {frac:.2%} overlap")

    def test_liquid_satellites_distinct(self):
        # pl vs pr differ only by the satellite letterform
        win = (40, -14, 70, 12)
        d = pmin(onset_glyph(["p", "l"]), onset_glyph(["p", "r"]),
                 win, 10)
        self.assertGreaterEqual(d, 0.30, f"pl/pr sat at {d:.3f}")


class TestCorpus(unittest.TestCase):
    def test_full_corpus_renders(self):
        words = set()
        base = Path(__file__).resolve().parent.parent / "docs" / \
            "design" / "zonal"
        for name in ("rz-texts.md",):
            for m in re.finditer(r'^> (.*)$',
                                 (base / name).read_text(), re.M):
                words.update(
                    re.findall(r"[a-zA-Z-]+", m.group(1).lower()))
        for w in words:
            word_glyph(w.strip("-"))

    def test_corpus_renders_with_pos_enabled(self):
        # the R-scheme path must never crash on untagged text
        for w in ("vento", "disputava", "viajator", "manto",
                  "coprite", "quando"):
            word_glyph(w, pos=True)


if __name__ == "__main__":
    unittest.main()
