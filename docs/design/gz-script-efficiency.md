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
