# GZ script efficiency: the compression dial (2026-08-25)

Edward's standing verdict on every transparent script page — "still
not very efficient per se" — is the axis this lane optimizes. The
substrate is settled (E3 syllable blocks, vowel-as-structure;
adoption recorded in gz-engine-bakeoff.md); efficiency comes from a
Zipf-tiered compression dial in the spirit of the stroke-system
fusion grammar: dense forms are DERIVED BY RULE, decodable slowly at
first, read holistically with practice. Tool:
`tools/block_compress.py`; round images in
`.ship-notes/workshop/gz-efficiency-r1/`.

## The dial (cumulative)

- **D1 frame-only particles.** h is the only particle onset, so its
  letterform carries zero information within the particle class —
  drop it. A particle renders as its vowel frame + coda band at
  0.72 scale. ~37% of running tokens compress to punctuation-scale
  marks, and the page acquires a content/function rhythm that
  visually segments words for free.
- **D2 vertical squash.** Multisyllable content words squash each
  block to 0.75 height (hanzi-style anisotropic compression).
- **D3 briefs.** High-frequency multisyllable words render as
  first block + final coda band + a double-tick brief mark. The
  POS channel survives (coda kept); the remainder is recovered
  lexically — steno-brief logic, explicitly a fluency tier.

## Measured [M] (315-token GZ text, fixed letterform scale)

| dial | area/word | vs D0 | ink/word | vs D0 |
|---|---|---|---|---|
| D0 transparent | 2983 px² | 100% | 300 u | 100% |
| D1 | 2960 | 99% | 275 | 92% |
| D2 | 2357 | 79% | 244 | 82% |
| D3 | 2282 | **77%** | 176 | **59%** |

Distinctness price (reading-raster pair floors, shared grid):
squash moves vowel median 0.450→0.404 and onset 0.260→0.239 with
minima unchanged — nearly free. D1/D3 change lexical recovery, not
pair geometry.

## Round 2: the fixed cell (Edward's r1 review, 2026-08-25)

Edward's r1 verdicts: D0 readable but inter-line gaps blur against
intra-word gaps when 3-tall words stack; D1 particle marks read as
floating inside an invisible box and too light; D2 readable, "a
little uglier"; D3 fine except residual 3-tall words cap the space
gain and the brief tick sometimes clipped block ink. And the
standing ideal, named explicitly: **fixed-size characters** ("seems
nicer, more beautiful, more perfect").

**F-mode** builds that ideal: every content word occupies exactly
one 64×78 cell — 1-syllable words fill it, n-syllable words squash
n blocks into the same 64u body, briefs are one block + band mark,
particles are ink-centered full-weight small marks (fixing both r1
particle complaints), the brief tick is placed below the word's
measured ink (fixing the clipping). Uniform cell → uniform line
pitch, which dissolves the D0 line-gap ambiguity and removes the
3-tall outliers by construction.

| mode | area/word | vs D0 | ink/word | vs D0 |
|---|---|---|---|---|
| D3 (variable) | 2296 px² | 77% | 176 u | 59% |
| **F fixed cell** | **1435** | **48%** | 171 | 57% |

Floors (reading raster, shared grid): the F disyllable squash
(0.49) holds — vowel median 0.377 vs 0.450 baseline, onset 0.232
vs 0.260, no collapses. The measured pair families are disyllabic;
the trisyllable-at-0.31 cell is NOT floor-covered yet and visibly
darkens (the m ring squashes toward a blob) — briefs keep that
tail rare, and it is the named next measurement.

## Word length is the remaining dial: the phoneme-space question

Edward (2026-08-25): would we use fewer characters per word with a
larger phoneme inventory — and does humility constrain that? Yes on
both, and it is already quantified: a word's character count IS its
syllable count, and monosyllable capacity is the binding
constraint. Raw body space is 10 onsets × 5 vowels = 50 cells;
humility leaves **22 adopted (18 strict, 15 after reserve)**
monosyllabic root bodies (lexgen report). The priced relaxation
menu exists (capacity-ledger.md, conlang-sss): POS-lane reuse
alone reaches ~66 bodies at a simulated cost of 2.5–30 silent
substitutions/10k words depending on syntactic catch rate — i.e.
moving from engineered-rare to natural-language-typical error
rates. Expanding the inventory itself (more onsets/codas) is the
other lever: the script has explicit headroom (18 usable onset
cells vs 11 assigned; 9 vowel positions vs 5), so every added
phoneme shortens the average word at the price of clearing the
confusion matrix. Efficiency-of-page and robustness-of-channel
meet exactly here; the trade lives in the sss ledger, not in the
renderer.

## Status and open work

Adopted (agent-called under the 2026-08-25 delegation; gate
calibration: reversible, rendering-only, zero learner cost beyond
two rules): **D1+D2 as the default rendering**. D3 is the adopted
DIRECTION, blocked on real design work before it can be default:

1. **Brief-tier collision policy** — briefs collide whenever two
   frequent words share (first syllable, final coda); a real
   lexicon needs a bounded brief set (steno precedent: a few
   hundred) with an explicit resolver.
2. **Real frequency tiers** — the demo thresholds at corpus
   freq>=6; the real dial should read corpus statistics.
3. **Width dial** — blocks stay 64u wide; narrower blocks are
   unexplored headroom.
4. Watch-item: frame-only hu/ho are lone horizontal bars — must
   never be readable as detached coda bands at small sizes.

Evidence: all numbers [M] from the prototype renderer; reading-
comprehension cost of each dial position is [H] until tested — the
sound-out ladder argument (every form rule-derived) is the design
rationale, not evidence.
