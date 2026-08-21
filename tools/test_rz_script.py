#!/usr/bin/env python3
"""Tests for the RZ featural display renderer (workshop hardening).

Raster floors follow the greenfield methodology (test_script.py):
occupancy-grid distances minimized over sub-cell sampling phases, so
a floor can't be passed by a lucky grid alignment. Thresholds sit
below currently measured phase-minima; a geometry change that erodes
a distinction trips them. Measured 2026-08-22 under the phase-padded
windows (14px onsets / 7px logograms): onset worst pair b/dZ 0.171;
voicing worst f/v 0.369; h vs ny 0.60; logogram worst mente/abile
0.500; func-mark worst con/en 0.313. (The v0 -cion/-itate collapse
scored 0.000 at 7px; the v1 windows cropped voiced ground bars at
x-phase 3.14 — both fixed.)
"""

import contextlib
import io
import itertools
import re
import sys
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from rz_script import (CODAS, FUNC_MARKS, LEGAL_ONSETS,  # noqa: E402
                       NON_VERB_FORMS, POS_Y, RZ_ONSETS,
                       SUFFIX_LOGOGRAMS, TENSE_LOGOGRAMS, analyze,
                       coda_glyph, logogram, main, onset_glyph,
                       onset_parts, to_phonemes, word_glyph)
from script import rasterize, raster_distance  # noqa: E402

# sub-cell sampling phases (greenfield methodology, Codex finding)
PHASES = [(px, py) for px in (0, 1.57, 3.14) for py in (0, 1.38, 2.76)]
MAXP = (3.14, 2.76)
# windows are padded left/top by the max phase so every sampled crop
# still contains all measured ink (Codex 2026-08-22 finding 3: the
# old (2,…) onset window cropped voiced ground bars at x-phase 3.14).
# TestWindowHonesty enforces this against future geometry changes.
ONSET_WIN = (-4, 2, 66, 64)         # includes the voicing ground bar
LOGO_WIN = (2, 2, 50, 64)
FUNC_WIN = (0, 10, 40, 60)


def pmin(a, b, win, n):
    return min(
        raster_distance(
            rasterize(a, win[0] + px, win[1] + py, win[2] + px,
                      win[3] + py, n),
            rasterize(b, win[0] + px, win[1] + py, win[2] + px,
                      win[3] + py, n))
        for px, py in PHASES)


def ink_bounds(parts):
    """(minx, miny, maxx, maxy) of an SVG fragment list, including
    stroke extent (linecap round adds w/2 beyond endpoints)."""
    bs = []
    for el in ET.fromstring("<svg>" + "".join(parts) + "</svg>"):
        w = float(el.get("stroke-width", 0)) / 2
        if el.tag == "line":
            xs = (float(el.get("x1")), float(el.get("x2")))
            ys = (float(el.get("y1")), float(el.get("y2")))
            bs.append((min(xs) - w, min(ys) - w,
                       max(xs) + w, max(ys) + w))
        elif el.tag == "circle":
            cx, cy = float(el.get("cx")), float(el.get("cy"))
            r = float(el.get("r")) + w
            bs.append((cx - r, cy - r, cx + r, cy + r))
        elif el.tag == "text":
            continue
    return (min(b[0] for b in bs), min(b[1] for b in bs),
            max(b[2] for b in bs), max(b[3] for b in bs))


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
        # Codex 2026-08-22 finding 1: corpus verbs the doc-only
        # harvest missed, plus the regular past of sta
        ("stava", ("sta", "va", "v")),          # rz-grammar §4: regular
        ("arivava", ("ariva", "va", "v")),
        ("demandava", ("demanda", "va", "v")),
        ("respondeva", ("responde", "va", "v")),
        ("telefonava", ("telefona", "va", "v")),
        ("sedeva", ("sede", "va", "v")),
        ("tentativa", ("tentativa", None, None)),  # noun, not tentati+va
        ("grammar", ("grammar", None, None)),   # filename scrape guard
    ]

    def test_analyze(self):
        for word, want in self.TABLE:
            self.assertEqual(analyze(word), want, word)

    def test_every_corpus_past_form_segments(self):
        # the advertised rule: regular past = stem+va, no hand-tagging.
        # Every attested -ava/-eva/-iva token must carry the logogram.
        base = Path(__file__).resolve().parent.parent / "docs" / \
            "design" / "zonal"
        toks = set()
        for name in ("rz-texts.md", "romance-zonal-v0.md",
                     "cloze-test-v0.md", "rz-lite.md"):
            p = base / name
            if not p.exists():
                continue
            for m in re.finditer(r"^> (.*)$", p.read_text(), re.M):
                line = re.sub(r"\([^)]*\)", " ", m.group(1))
                toks.update(re.findall(r"[a-z]+", line.lower()))
        pasts = sorted(t for t in toks if len(t) > 4
                       and t.endswith(("ava", "eva", "iva"))
                       and t not in NON_VERB_FORMS)
        self.assertGreater(len(pasts), 15)      # the corpus has ~30
        for t in pasts:
            self.assertEqual(analyze(t), (t[:-2], "va", "v"), t)

    def _pos_lines(self, parts):
        return [tuple(float(el.get(k)) for k in ("x1", "y1", "x2", "y2"))
                for el in ET.fromstring("<svg>" + "".join(parts)
                                        + "</svg>")
                if el.tag == "line" and float(el.get("y1")) == POS_Y
                and float(el.get("y2")) == POS_Y]

    def test_tagged_pos_marks_have_expected_geometry(self):
        # Codex 2026-08-22 finding 4: assert the actual mark, not just
        # that something rendered — verb = full-width bar at POS_Y,
        # adjective = leading ~40% bar, in both dense modes
        for dense in (True, False):
            vparts, vw = word_glyph("parlava:v", pos=True, dense=dense)
            vlines = self._pos_lines(vparts)
            self.assertEqual(len(vlines), 1, f"dense={dense}")
            self.assertEqual(vlines[0][0], 4)
            self.assertEqual(vlines[0][2], vw - 4)
            aparts, aw = word_glyph("manto:adj", pos=True, dense=dense)
            alines = self._pos_lines(aparts)
            self.assertEqual(len(alines), 1, f"dense={dense}")
            self.assertEqual(alines[0][0], 4)
            self.assertAlmostEqual(alines[0][2], 4 + 0.4 * aw)
            nparts, _ = word_glyph("vento:n", pos=True, dense=dense)
            self.assertEqual(self._pos_lines(nparts), [])

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


class TestWindowHonesty(unittest.TestCase):
    """A raster floor only guards what its window contains, at EVERY
    sampled phase (Codex 2026-08-22 finding 3). The crop at phase
    (px,py) is (x0+px, y0+py, x1+px, y1+py), so the binding edges are
    left/top at max phase and right/bottom at zero phase."""

    def assert_covered(self, parts, win, label):
        minx, miny, maxx, maxy = ink_bounds(parts)
        self.assertGreaterEqual(minx, win[0] + MAXP[0], label)
        self.assertGreaterEqual(miny, win[1] + MAXP[1], label)
        self.assertLessEqual(maxx, win[2], label)
        self.assertLessEqual(maxy, win[3], label)

    def test_onset_window_covers_all_ink(self):
        for ph in RZ_ONSETS:
            self.assert_covered(onset_glyph([ph]), ONSET_WIN, ph)

    def test_logo_window_covers_all_ink(self):
        for s in SUFFIX_LOGOGRAMS + TENSE_LOGOGRAMS:
            self.assert_covered(logogram(s), LOGO_WIN, s)

    def test_func_window_covers_all_ink(self):
        for w in FUNC_MARKS:
            self.assert_covered(word_glyph(w)[0], FUNC_WIN, w)


class TestViewport(unittest.TestCase):
    """End-to-end: CLI word/sentence output must contain all ink in
    its viewBox (Codex 2026-08-22 finding 2: cluster satellites rise
    above the block top and were clipped at dy=0)."""

    def _cli_svg(self, argv):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            self.assertEqual(main(argv), 0)
        return buf.getvalue()

    def _assert_ink_in_viewbox(self, svg_text):
        m = re.search(r'viewBox="([-\d.]+) ([-\d.]+) ([\d.]+) ([\d.]+)"',
                      svg_text)
        self.assertIsNotNone(m)
        vx, vy, vw, vh = (float(g) for g in m.groups())
        frags = re.findall(r"<(?:line|circle)[^/]*/>", svg_text)
        self.assertTrue(frags)
        minx, miny, maxx, maxy = ink_bounds(frags)
        self.assertGreaterEqual(minx, vx)
        self.assertGreaterEqual(miny, vy)
        self.assertLessEqual(maxx, vx + vw)
        self.assertLessEqual(maxy, vy + vh)

    def test_word_cli_contains_cluster_satellites(self):
        # pr and st satellites reach y = dy-10 minus stroke extent
        self._assert_ink_in_viewbox(
            self._cli_svg(["word", "prendeva", "stacion"]))

    def test_sentence_cli_contains_all_ink(self):
        self._assert_ink_in_viewbox(
            self._cli_svg(["sentence",
                           "le vento del norte stava presto"]))


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
