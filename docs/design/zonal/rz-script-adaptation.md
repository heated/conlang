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
