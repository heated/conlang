"""Regression tests for the spatial sentence layer (conlang-4j7)."""

import re
import sys
import unittest

sys.path.insert(0, __file__.rsplit("/", 1)[0])

import spatial_layer as S  # noqa: E402


class TestParse(unittest.TestCase):
    def test_roles_are_deterministic(self):
        cl = S.parse()
        c0 = cl[0]                       # engineer build-n bridge stone-s hol valley
        self.assertEqual(c0.pred, "build")
        self.assertEqual(c0.arg("AG").ent, "engineer")
        self.assertEqual(c0.arg("PAT").ent, "bridge")
        self.assertEqual(c0.arg("PAT").mods, ["stone"])
        self.assertEqual(c0.arg("LOC").ent, "valley")

    def test_time_word_reroles_from_locative(self):
        cl = S.parse()
        flood = [c for c in cl if c.pred == "flood"][0]
        self.assertEqual(flood.arg("TIME").ent, "spring")
        self.assertIsNone(flood.arg("LOC"))
        self.assertIn("PAST", flood.marks)

    def test_negation_attaches_to_its_own_clause(self):
        cl = S.parse()
        dmg = [c for c in cl if c.pred == "damage"][0]
        self.assertIn("NEG", dmg.marks)
        self.assertTrue(all("NEG" not in c.marks for c in cl
                            if c.pred != "damage"))

    def test_complement_becomes_a_child_clause(self):
        cl = S.parse()
        say = [c for c in cl if c.pred == "say"][0]
        hold = [c for c in cl if c.pred == "hold"][0]
        self.assertEqual(hold.parent, say.idx)
        self.assertEqual(hold.arg("AG").ent, "stone")
        # the complement's subject must NOT leak into the matrix clause
        self.assertIsNone(say.arg("PAT"))


class TestLayouts(unittest.TestCase):
    def setUp(self):
        self.clauses = S.parse()
        self.ents = S.entity_order(self.clauses)

    def test_every_mention_is_rendered(self):
        """No layout may silently drop a participant."""
        want = set()
        for c in self.clauses:
            want.update(c.ents())
        for key, fn in S.LAYOUTS:
            lay = fn(self.clauses, self.ents)
            got = {m[0] for m in lay.mentions}
            self.assertEqual(want - got, set(),
                             f"{key} dropped entities")

    def test_every_predicate_is_rendered(self):
        for key, fn in S.LAYOUTS:
            lay = fn(self.clauses, self.ents)
            blob = "".join(lay.parts)
            for c in self.clauses:
                self.assertIn(f">{c.pred}<", blob,
                              f"{key} dropped predicate {c.pred}")

    def test_canvas_contains_all_ink(self):
        """qlmanage-style clipping hides real content; the canvas must be
        fitted to the ink, not to the layout's own guess."""
        for key, _ in S.LAYOUTS:
            doc = S.page(key)
            w = float(re.search(r'width="([\d.]+)"', doc).group(1))
            h = float(re.search(r'height="([\d.]+)"', doc).group(1))
            body = re.sub(r"<svg[^>]*>", "", doc)
            _, _, mx, my = S.content_bbox([body])
            self.assertLessEqual(mx, w + 1, f"{key} ink overflows width")
            self.assertLessEqual(my, h + 1, f"{key} ink overflows height")

    def test_mentions_carry_extents_not_points(self):
        for key, fn in S.LAYOUTS:
            lay = fn(self.clauses, self.ents)
            for m in lay.mentions:
                self.assertEqual(len(m), 5, f"{key}: mention lacks extent")
                self.assertGreater(m[3], 0)
                self.assertGreater(m[4], 0)


class TestMetrics(unittest.TestCase):
    def setUp(self):
        self.clauses = S.parse()
        self.ents = S.entity_order(self.clauses)

    def test_metrics_are_bounded_and_finite(self):
        for key, fn in S.LAYOUTS:
            m = S.metrics(fn(self.clauses, self.ents), self.clauses,
                          self.ents)
            self.assertGreater(m["ink_area_per_prop"], 0)
            self.assertGreater(m["marks_per_prop"], 0)
            self.assertTrue(0.0 < m["search"] <= 1.0, f"{key} search")
            self.assertTrue(0.0 <= m["scatter"] <= 1.5, f"{key} scatter")

    def test_lanes_pin_reference_better_than_the_string(self):
        """The one structural claim round 1 actually supports."""
        s0 = S.metrics(S.layout_S0(self.clauses, self.ents), self.clauses,
                       self.ents)
        s1 = S.metrics(S.layout_S1(self.clauses, self.ents), self.clauses,
                       self.ents)
        self.assertLess(s1["search"], s0["search"] / 10)

    def test_margin_padding_cannot_improve_the_score(self):
        """Normalization is against the ink box, so blank margin is inert."""
        lay = S.layout_S4(self.clauses, self.ents)
        base = S.metrics(lay, self.clauses, self.ents)
        padded = S.Layout(lay.key, lay.name, list(lay.parts), lay.w + 800,
                          lay.h + 800, lay.mentions, lay.labels)
        after = S.metrics(padded, self.clauses, self.ents)
        self.assertAlmostEqual(base["search"], after["search"], places=9)
        self.assertAlmostEqual(base["scatter"], after["scatter"], places=9)

    def test_crossing_counter(self):
        x = [S.line(0, 0, 10, 10), S.line(0, 10, 10, 0)]
        self.assertEqual(S.count_crossings(x), 1)
        par = [S.line(0, 0, 10, 0), S.line(0, 5, 10, 5)]
        self.assertEqual(S.count_crossings(par), 0)

    def test_guide_lines_are_not_counted_as_content(self):
        guide = [S.line(0, 0, 10, 10, stroke=S.GUIDE_COLOURS[0]),
                 S.line(0, 10, 10, 0, stroke=S.GUIDE_COLOURS[0])]
        self.assertEqual(S.count_crossings(guide), 0)
        self.assertEqual(S.count_marks(guide), 0)


class TestOracle(unittest.TestCase):
    def test_coverage_matrix_is_well_formed(self):
        for key, _ in S.LAYOUTS:
            self.assertIn(key, S.COVERAGE)
            self.assertEqual(len(S.COVERAGE[key]), len(S.ORACLE_FIELDS),
                             f"{key} coverage row is the wrong length")
            self.assertIn(key, S.COVERAGE_NOTES)

    def test_a_layout_that_loses_a_field_is_declared_lossy(self):
        """S3 has no reading order and nowhere to hang a complement edge;
        that must stay declared, not quietly become 'yes'."""
        i = S.ORACLE_FIELDS.index("clause order")
        j = S.ORACLE_FIELDS.index("complement edge")
        self.assertEqual(S.COVERAGE["S3"][i], "NO")
        self.assertEqual(S.COVERAGE["S3"][j], "NO")


if __name__ == "__main__":
    unittest.main()
