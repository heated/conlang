# RZ lexical coverage curves (measured 2026-08-22, conlang-i78)

What is one root WORTH, in percent of running text? The learning
budget prices lexicon acquisition in hours but had never measured the
value side. `tools/coverage.py` measures it on the full RZ corpus
(937 tokens across rz-texts / romance-zonal-v0 / cloze-test-v0 /
rz-lite blockquotes).

## Headline findings

1. **Half the language is 62 words.** The closed class (particles,
   determiners, prepositions, pronouns, copulas) covers **49.4% of
   running tokens** with 62 attested words. This is the first-lesson
   block: a learner who memorizes one page of function words can
   already parse every other token of any RZ text. (Natural-language
   comparison: English function words cover ~40-50% — RZ is at the
   top of the natural band because it has no inflectional variants
   inflating the content side.)
2. **~122 content lemmas → 70% of content tokens; ~241 → 95%**
   (in-corpus). With the closed class known, the open-class curve is:
   50% at 74 lemmas, 70% at 122, 80% at 170, 90% at 217, 95% at 241.
3. **In-corpus curves flatter — the planning number is the Zipf
   band.** A 937-token corpus is self-similar (most content words
   appear once), so "241 lemmas = 95%" overstates real-world
   coverage. A Zipf fit anchored on the mid ranks (the head decays
   steeper and is excluded; v1 of the fit got this wrong and
   underestimated below measured values) extrapolates **~470-510
   open lemmas for 95-98%** of an unbounded text population [D,
   rough]. Consistent with natural-language lore (~1k lemmas → ~85%,
   ~3k → 95%): RZ needs somewhat less because derivation is regular
   and the closed class is bigger per token.
4. **The corpus cannot show the inflectional dividend — the grammar
   can.** Measured forms/lemma is 1.037, an artifact of corpus size,
   not evidence of weak morphology. From the grammar: an RZ lemma
   costs ~3.67 recognizable forms on average (verb 7, noun 2, adj 2,
   all exceptionless) vs Spanish ~19.67 synthetic forms (verb 53,
   noun 2, adj 4). **Recognition-load ratio ≈ 5.4x** — per lemma
   learned, a from-scratch learner faces one-fifth the form
   inventory, with zero irregulars. (For the Romance cohort this is
   mostly moot receptively — they already own the donor paradigms —
   which is again the GZ thesis: regularity pays in the cohorts the
   zone doesn't serve.)

## Ledger implication

The "lexicon, productive at C1 breadth" line in learning-budget.md
now has a size estimate behind it: **~500 open-class lemmas ≈ the
95%-coverage lexicon**. At humane acquisition rates (10-20 lemmas/h
recognition for the Romance cohort given cognate transfer; 4-8/h
productive for distant cohorts) that is ~25-50h receptive /
~60-125h productive for the coverage core — inside the ledger's
existing C1 lexicon bands, which is a consistency check, not news.
The news is the SHAPE: 62 closed words = 49%, then a long shallow
tail. Curriculum order should be closed-class block → 122-lemma
core → topic packs.

## Caveats

- n = 937 tokens of largely translated/parallel material; register
  breadth is narrow, so the tail is underestimated even by Zipf.
- The lemma stripper is heuristic (longest-suffix-first, 3-char stem
  floor); spot-checked, not gold-standard.
- Derivation stripping (root curve) currently merges nothing at the
  head — derived pairs (nacion/nacional...) are too rare in-corpus
  to register. The derivation multiplier remains a grammar-side
  argument, not yet a corpus measurement.
