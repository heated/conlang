# RZ chording sketch — what survives of the input-speed story

Workshop draft (conlang-0y7 / feeds conlang-ow7 pricing and
conlang-6sa input methods). Question: Edward's traits are of the
"grab low-hanging fruit & max useful traits" kind — how much does the
Romance lexicon actually wreck chorded input?

## 1. RZ's measurable shape (from the v0 sample texts)

- ~1.83 syllables/word overall (function words are monosyllables;
  content words ≈ 2.7).
- Under onset-maximal syllabification, codas — word-final AND
  word-medial — collapse to a tiny set: **l n r s** (plus rare
  geminate-ish medials the orthography splits). The complexity lives
  in onsets: ~20 simple consonants + obstruent–liquid clusters
  (pr br tr dr cr gr fr, pl bl cl gl fl) + s-clusters (sp st sc…).
- Distinct syllables: 70 in one paragraph alone; a full lexicon
  extrapolates to the low thousands (vs the greenfield's closed 220).

## 2. Chord theory (steno-adapted, but cleaner)

One stroke = one syllable, emitted as orthographic text:

- **Left bank (onset), ~9 keys**: base consonant keys with
  compositional cluster formation — a liquid key (R/L) and an S- key
  chord onto any obstruent (P+R → pr, S+T → st). Every RZ onset is
  one chord; nothing is arbitrary.
- **Thumb bank (nucleus), 5 keys**: a e i o u; two-key chords give
  diphthongs, with element order from thumb position (left = first).
- **Right bank (coda), 4 keys**: l n r s — the entire coda system.
  This is the gift of Romance phonotactics: the right hand is almost
  free, exactly like steno English is not.
- **Emission**: chords → syllable text; a dictionary-assisted joiner
  places word boundaries (explicit boundary thumb-chord as fallback).

Because RZ spelling is regular, the chord→text mapping has **zero
exceptions** — the single biggest pain of English steno (mapping
sound to irregular spelling) does not exist here. That was also the
greenfield's advantage; RZ keeps it.

## 3. Rates, honestly estimated

At steno-typical 3–4 strokes/sec: 180–240 syllables/min ÷ 1.83
syl/word ≈ **100–130 wpm with no memorized briefs at all** (function
words are monosyllables — already one stroke). Steno parity (180–225
wpm) requires a brief layer (one-stroke word abbreviations), which
reintroduces steno's memorization cost — but as an *optional power
tier*, not a floor.

Greenfield comparison (the wreckage quantified): mirrored-hands,
one-syllable-per-hand chording gives the greenfield **one stroke per
word** for its 1–2-syllable-dominant lexicon ≈ 1.0 strokes/word vs
RZ's ≈ 1.8. At equal stroke rate the greenfield words-per-minute
ceiling is ~1.8× RZ's brief-free ceiling, and its ceiling needs no
brief dictionary ever. So: **chorded input survives Romance at
roughly half efficiency, with the no-memorization property intact at
the base tier and lost at the power tier.** That is the best
trait-survival in the whole ow7 table — everything else fares worse.

## 4b. Dial-in (Edward Qs 2026-08-21): mirrored hands? multi-syllable strokes?

**Mirrored one-chord-per-hand (a syllable per hand): right for the
greenfield, wrong for RZ — the key budget says so.** Per-hand key
need, chord-combinatorics style (n keys → 2^n−1 combos):

| | onset bank | nucleus | coda | keys/hand |
|---|---|---|---|---|
| greenfield (10 on, 5 v, 4 codas) | 4 | 3 | 2 | **9** ✓ within hand span |
| RZ (~35 onsets w/ clusters, 13 nuclei, 5 codas) | 8 (6 base + liquid + s) | 4 | 3 | **15** ✗ beyond ~11-12 span |

Same lesson as script density: **the width you buy in speech, you
pay back at the keyboard.** Mirroring itself is fine (bimanual
mirror symmetry is the easy coordination mode; learn one layout,
use both hands) — it's RZ's inventory that doesn't fit in one hand.
This is where the greenfield's 1.0 strokes/word figure comes from,
and RZ can't have it by that route.

**Multi-syllable strokes via channel rearrangement: not dumb — it's
the Velotype direction, and it works.** Instead of hand-per-
syllable, lay the banks left-to-right in time order as a disyllable
template: `[onset₁][nucleus₁][coda₁][onset₂][nucleus₂][coda₂]`
(~28 keys, a Velotype-class board — that machine family does 200
wpm with orthographic syllable strokes, so the form factor is
proven). Every RZ syllable fits the template by construction
(clusters stay key-compositional), so the theory stays
**zero-exception**. Measured on the six-register corpus (335
tokens; syllable distribution 1:152 / 2:113 / 3:51 / 4:16 / 5:3):

| scheme | strokes/word |
|---|---|
| one syllable per stroke (v1 baseline) | 1.82 |
| disyllable template | **1.22** (79% of words = one stroke) |
| + systematic suffix keys (-mente, -cion(e), -itate, -abile, -ava/-eva/-iva) | **1.13** |

The suffix keys are the logogram set as chord banks — deterministic
orthographic emission, not memorized briefs, so the zero-exception
property survives. Net: the template board closes most of the gap
to the greenfield (1.13 vs 1.0) without briefs; the remaining gap
is RZ's trisyllable tail. Cross-word packing of function-word
monosyllables (38% of tokens) into their neighbor's stroke is the
remaining lever — power tier, flagged, not base theory.

**Recommendation [D]: adopt the disyllable-template board as RZ
chording v2**; drop the mirrored variant for RZ (keep it for GF,
where it's cheap).

## 4. What to build when tooling starts (not now)

Keyboard layout diagram + a joiner prototype + a 200-word brief
starter set for the power tier; measure real wpm on the sample texts.
Belongs to conlang-6sa once the RZ lexicon exists.
