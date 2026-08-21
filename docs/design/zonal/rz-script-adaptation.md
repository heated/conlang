# RZ channels & the featural script adapted (workshop note)

Bead conlang-0y7 / feeds ow7 and 6sa. Question (Edward, 2026-08-14):
what are RZ's channels, and what does the greenfield script look like
adapted to RZ? Standing decision unchanged: Latin-primary
(zonal-script-pricing.md); everything here is the *secondary* layer —
input method + optional dense display.

## 1. RZ's channels

**Syllable level (phonological, codespace only):**

- onset = (s-)? × consonant × (liquid)? — three sub-channels
  (covers spr-, tr-, bl-, …; ~35 surface onsets from ~14 primitives)
- nucleus = vowel {a e i o u} × (glide)? for diphthongs
- coda = {∅, l, n, r, s}

No designed semantics, no check bit — these axes just carry the
lexicon.

**Word level (morphological — the real channels, deterministic
because the morphology was regularized to exception-freeness):**

- tense channel: -a/-e/-i present · -va past · -ria conditional ·
  va+inf future (auxiliary, pre-verbal)
- number channel: -s/-es
- POS/derivation channel: -cion (noun, always) · -mente (adverb,
  always) · -al/-oso/-abile (adjective) · -or/-ista (agent) · bare
  -ar/-er/-ir (infinitive)

Natural Romance has these statistically; RZ has them absolutely.
Summary: **the greenfield's channels live in the syllable; RZ's live
in the suffix.**

## 2. The adapted featural script (wide-model instantiation)

1. **Consonants: ~12 base letters + a voicing modifier** covering the
   systematic pairs p/b t/d k/g f/v s/z. This deliberately relaxes
   the v0.2 distance-2 doctrine (voicing pairs are ear-confusable yet
   would differ by one mark): acceptable because this layer is
   secondary — Latin carries the text; learnability outranks
   robustness here. The voicing mark must still be a robust-ink class
   (full crossing stroke, not a dot).
2. **Vowel carrier unchanged** (same five vowels — the best-reviewed
   part of the greenfield script transfers verbatim); diphthongs get
   a second, smaller glide tick.
3. **Onset zone composes clusters**: s-prefix mark + base letter +
   liquid mark — one glyph zone, mirroring the chord banks
   one-to-one (block = chord diagram survives; rz-chording.md).
4. **Coda strip adds r** to the n/s/l bar family.
5. **The transplant — suffix logograms in the strip.** Greenfield
   principle: the grammar channel gets the loudest ink. RZ's grammar
   channels are suffixes, so -va, -s, -cion, -mente, -al, -or get
   dedicated strip-native marks instead of spelled-out letters:
   tense, number, and POS become skim-readable, recovering the
   silhouette grammar inside the display layer — the one concrete
   thing this script buys that Latin RZ text cannot do.
6. No check channel (stands as priced: that machinery dies outside
   the greenfield).

## 3. Status: VECTOR PROTOTYPE (downgraded from 'taped out', 2026-08-15
review — voicing pairs measure 0 raster distance at worst phase at
14px; -cion/-itate collapse at 7px; no regression suite; h-deletion
contradicts the no-silent-letters contract; see project-review-sol.md
findings 4, 5, 9, 12)

### 3b. Hardening pass, 2026-08-22 (conlang-dka)

All four review findings closed, plus the v1 backlog:

- **Raster regression suite** (test_rz_script.py): phase-minimized
  occupancy distances, greenfield methodology. Floors: all onset
  pairs ≥0.15 @14px; voicing pairs ≥0.30 (measured min f/v 0.371 —
  the review's "0.000" came from a crop window that excluded the
  ground bar; with an honest window the pairs were never at zero,
  but three geometry fixes still lifted the worst cases: thicker/
  wider ground bar, m-slash protruding past the ring (ts/m
  0.138→0.219), full-width vertical cross (b/dZ 0.146→0.182));
  logograms ≥0.40 @7px; function marks ≥0.15 @10px.
- **-cion/-itate collapse fixed**: -itate redesigned as a
  double-crossed descender (‡ family, no ring) — 7px phase-min went
  0.000 → 0.538+.
- **Tense logograms live**: -va = left arrow (past), -ria = fork
  (conditional), gated by a verb-stem set harvested from the lexicon
  docs (infinitives in -ar/-er/-ir, glosses stripped) — `parlava`
  segments, `materia` doesn't. Suppletives (era, seria…) tag POS
  and render plain. No hand-tagging needed for regular forms.
- **h letterform enters RZ** (tick doubled, greenfield transfer):
  the number mode makes [h] a real phoneme in mode frames
  (rz-number-mode.md) — `hu` renders with ink, `hotel` stays
  silent-h. This RESOLVES the h-deletion contradiction: the script
  writes phonemes, and [h] now exists exactly where it is pronounced.
  The ly-vs-h lookalike was pre-empted: ly's cap is now wider and
  higher than its main bar (h/ly phase-min ≥0.40 enforced).
- **R-scheme POS prototype** (the GZ script-only dial, gz-sketch.md):
  optional underlines — verb = full underbar, adjective = leading
  half-bar, noun bare. Auto-fired by verbal morphology; `word:adj`
  tags cover the rest. This is the concrete artifact the E/R/M
  decision can look at.
- **Hangul mutual sizing**: main letter shrinks (0.82) under
  satellites; s- top-left, liquid moved to top-right (clears the
  voicing bar zone). Enforced invariant: satellite ink lands on main
  ink ≤3% of satellite cells, tested over every legal cluster.

**Post-review fixes (Codex xhigh on the hardening commit, 2026-08-22
— 2 IMPORTANT + 2 MINOR, all confirmed and closed):**

1. The doc-only verb harvest missed most corpus past forms (only
   9/21 -va tokens got the logogram) and `stava` was mislabeled
   suppletive (rz-grammar §4 calls it the regular past of `sta`).
   Now: two evidence streams — lexicon-doc infinitives (filename
   spans excluded; `gramma` no longer scraped from `rz-grammar.md`)
   plus corpus attestation (every -ava/-eva/-iva token testifies to
   its own stem; a small NON_VERB_FORMS lexicon set blocks
   `tentativa`-class false positives). A corpus-wide test asserts
   EVERY attested past form segments stem+va with the logogram.
2. Cluster satellites (top ink at dy−10) were clipped by the CLI
   word/sentence viewBox at dy=0. All CLI canvases now inset by
   TOP_INSET; an end-to-end test parses emitted SVG and asserts all
   ink lies inside the viewBox.
3. The phase-shifted crop windows themselves are now guarded: a
   window must contain all measured ink at EVERY sampled phase
   (the v1 onset window cropped voiced ground bars at x-phase 3.14
   — the windows are now phase-padded and the guard is a test).
   Recalibrated minima: onset worst b/dZ 0.171; voicing worst f/v
   0.369; logogram worst 0.500; func worst con/en 0.313.
4. The POS-tag test now asserts mark geometry (verb full-width bar
   at POS_Y, adjective 40% bar, noun bare — both dense modes), not
   just that tagged input renders.

### 3d. Aesthetic pass v1 (2026-08-22, conlang-18s — Edward's visual
### feedback, partially applied; further script work DEPRIORITIZED)

Edward's feedback on the specimen pages, acted on:
1. **Two-weight discipline**: every stroke is STROKE (5, structural)
   or W_MARK (3.5, marks) — the per-scale width variation
   ("a little cursed") is gone. Cost paid consciously: the voicing
   ground bar thinned 8→5, f/v raster min 0.371→0.271, floor moved
   0.30→0.25 with the trade documented in the test.
2. **Headstroke killed** ("invariably ugly and doesn't add much") —
   mode removed from renderer, CLI, and pages.
3. **No more floating marks**: cluster satellites replaced by
   full-height, x-narrowed letters in phonetic order (Hangul-ㅄ
   slots) — same block height as plain onsets, uniform weight.
4. **Visual-margin criterion** replaces bare non-overlap: minimum
   ink-to-ink distance between cluster letters enforced by test
   (3px pairs, 2px triples).
Remaining from the feedback: coda minis and some logogram elements
still read small ("marks in weird places" residue); the
experimental-direction pull (fusion/beauty studies) untouched.
**Both parked — Edward directive 2026-08-22: deprioritize script
work pending the multi-approach workshop pipeline
(docs/process/design-workshop.md).**

### 3c. Beauty pass — variant sheet (2026-08-22; decision = taste,
### parked at the human gate — SUPERSEDED in part by §3d: Edward's
### 18s feedback already killed headstroke, mooting V4/V5)

With optimal settled and floored, the beauty lever is a
display-parameter choice, not a geometry change (all regression
floors are measured at baseline weight and stay authoritative).
Comparison sheet: `.ship-notes/rz-beauty-variants.svg` — the fable
clause in five settings: V1 baseline (STROKE 5, gap 24), V2 light
+ airy (0.68x, gap 30), V3 heavy + tight (1.32x, gap 17,
display/poster), V4 headstroke, V5 light headstroke.

Observations (mine; the pick is Edward's):
- **V2 reads most like a text face** — counters open up, voicing
  ground bars stay unambiguous; recommended default for running
  text.
- **V3 works as display/poster only** — satellites and doubled
  bars begin to fill; never use heavy at small sizes (the floors
  are calibrated at baseline).
- **V5 (light headstroke) is the aesthetic surprise** — a
  Devanagari-adjacent rhythm with word cohesion for free.
- **Found issue: function-word dashes nearly vanish under the
  headstroke rule** (a dash under a rule reads as rule texture).
  Before any headstroke adoption, func marks need to hang lower or
  the rule should skip function words. Filed as the one geometry
  item the beauty pass surfaced.

Implemented in `tools/rz_script.py` (stdlib SVG; specimen in
`.ship-notes/rz-specimen.svg`). What shipped: 18 pairwise-distinct
consonant letterforms (greenfield-shared phonemes keep their
greenfield glyphs; voicing = full-width ground bar; new cells for
f r dZ ny ly), twin-carrier diphthongs, coda strip incl. the r
up-tick (mirror-of-l flagged), marginal-coda fallback (x-words),
cluster satellites (s- top-left, liquid bottom-right, 0.38 scale),
and suffix logograms for -mente/-cion/-itate/-abile (-itate
redesigned mid-tape-out to avoid rendering as the ♀ symbol). A
spelling→phoneme→syllable pipeline covers the whole reader pack:
all 234 distinct RZ sample words render. Density observed: nacion
and veritate are two glyph-units each; the fable clause "le vento
del norte e le sol disputava" is ~13 units.

Known v1 items: satellite/main-letter Hangul-style mutual sizing,
ly-vs-greenfield-h lookalike (cross-system only), -va/-ria
logograms need morphologically tagged input, raster-floor
methodology not yet applied (relaxed doctrine to be made explicit
when it is). Still display-layer only; Latin remains primary; cloze
pilot remains the gate for investing further.
