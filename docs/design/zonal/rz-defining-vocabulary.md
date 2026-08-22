# A self-hosting lexicon: the defining-vocabulary discipline
(exploration, 2026-08-22, conlang-i78; steal-pass item — precedents:
Longman/LDOCE, Oxford 3000, Basic English; relates to conlang-em5)

## The steal

Learner dictionaries solved a problem RZ is about to have. The
Longman Dictionary of Contemporary English writes **every definition
in a controlled ~2,000-word defining vocabulary**, so a learner who
owns that core can read the whole dictionary — the lexicon becomes
**self-hosting**: past the core, the language explains itself and
the bilingual dictionary retires. Oxford does the same with the
Oxford 3000; Basic English pushed the same idea to 850 words at the
cost of contortion.

RZ can adopt this discipline *at design time* — before a single
definition exists — and its architecture makes the discipline
stronger than the precedents:

1. **The defining set is not a new list.** Longman had to curate its
   2,000 separately from any curriculum. RZ's curriculum is already
   a coverage-greedy frequency sort (rz-curriculum.md), so the
   defining set can simply BE a curriculum prefix — "definitions use
   only lesson vocabulary" and "definitions use only the defining
   set" become the same statement. A learner at hour N can read
   every definition whose headword they can reach.
2. **The closed class is guaranteed closed.** Half of definition
   text is function words (49.2% of running tokens in the corpus);
   rz-grammar §12 already freezes that inventory at 96 forms. The
   precedents had no such guarantee.
3. **Derivation is exceptionless**, so the defining set counts
   *lemmas*, and every definition gets the §9 families for free
   (defining-set `nacion` licenses `nacional`, `nacionalitate`).

## The proposal (POLICY now, artifact later)

Adopted as lexicon policy, mirror of the coinage-screen adoption
(policy-now/instrument-pending, gz-rz-mining-audit.md):

- **P1 — defining set = a frozen curriculum prefix.** Sized
  honestly: Basic English's 850 forced contortion, Longman's ~2,000
  is the empirical floor for defining a full dictionary without
  contortion. Target: **the first ~1,000 curriculum lemmas** (with
  the 96 closed forms, numerals, and §9 derivation free). The
  current corpus curriculum only reaches ~220 open lemmas, so the
  set freezes when the lexicon's frequency ordering matures past
  rank 1,000; until then the policy binds authorship, not a list.
- **P2 — every RZ-RZ definition uses only: the defining set, the
  headword's own derivational family, and words whose own
  definitions the entry explicitly links** (no hidden chains).
- **P3 — the instrument is a lint**, trivially buildable on
  tools/coverage.py's lemmatizer: parse each definition, flag any
  lemma outside the licensed set. It ships with the first dictionary
  artifact, not before.

## Pricing (learning-budget terms)

- **First-contact tax: zero.** Dictionary-internal; no surface form
  changes.
- **Learner cost: zero — the sign is negative.** The discipline
  *saves* hours at the intermediate stage: the moment a learner
  clears the curriculum head, monolingual lookup replaces bilingual
  lookup, which is itself comprehension practice ([H]: the size of
  that saving is unmeasured; the *mechanism* — graded monolingual
  definitions extend receptive exposure — is the entire learner-
  dictionary industry's operating premise).
- **Author cost: real and known.** Controlled-vocabulary definition
  writing is hard (Longman staffs it). This prices against project
  time, not learner time — the ledger's currency is unaffected.
- **Gate class: pure-upside on the learner side, reversible,
  touches no inherited surface → agent-callable** under the
  2026-08-22 calibration. Adopted; recorded in rz-lexicon.md.

## Toolkit entry (portable)

Portable to any auxlang with a frequency-ordered curriculum:
*align the defining vocabulary with a curriculum prefix so
"can read the dictionary" falls out of "took the lessons"*. The
alignment trick — not the controlled vocabulary itself, which is
prior art — is the contribution. Strength scales with how greedy
the curriculum can be, which is itself a function of closed-class
discipline and exceptionless derivation (both toolkit entries
already).

## S1 tie-in

The graded-reader funnel's tap-glosses (rz-bootstrap-scenarios.md)
get a growth dial: beginner taps show the L1 gloss, intermediate
taps show the defining-vocabulary RZ definition — the reader
deepens into monolingual immersion without leaving the page.
