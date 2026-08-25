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
| D3 | 2296 | **77%** | 176 | **59%** |

Distinctness price (reading-raster pair floors on the
PAGE-CONSISTENT grid — an earlier draft measured on a 4/3-finer
raster and understated this; Codex review r2): squash moves vowel
median 0.422→0.371 and vowel minimum 0.249→0.197 (onset median
0.249→0.227). A real but modest cost — ~12% of vowel margin, no
collapses. D1/D3 change lexical recovery, not pair geometry.

## Round 2: the fixed cell (Edward's r1 review, 2026-08-25)

Edward's r1 verdicts: D0 readable but inter-line gaps blur against
intra-word gaps when 3-tall words stack; D1 particle marks read as
floating inside an invisible box and too light; D2 readable, "a
little uglier"; D3 fine except residual 3-tall words cap the space
gain and the brief tick sometimes clipped block ink. And the
standing ideal, named explicitly: **fixed-size characters** ("seems
nicer, more beautiful, more perfect").

**F-mode** builds that ideal: every content word occupies exactly
one 64×82 cell — a 64u body plus an 18u band. 1-syllable words
fill the body, n-syllable words squash n blocks into it, briefs
are one block with shortened coda bars and the brief tick side by
side INSIDE the band (fixing the r1 tick clipping), and particles
are ink-centered full-weight small marks (fixing both r1 particle
complaints). Uniform cell → uniform line pitch, which dissolves
the D0 line-gap ambiguity and removes the 3-tall outliers by
construction.

| mode | area/word | vs D0 | ink/word | vs D0 |
|---|---|---|---|---|
| D3 (variable) | 2296 px² | 77% | 176 u | 59% |
| **F fixed cell** | **1480** | **50%** | 165 | 55% |

The cell is honestly enclosing: a bounds regression test verifies
every mode's ink stays inside its reported (w, h) — the first F
draft returned a 78u cell for ~96u of coda-brief ink and only
looked right because line leading absorbed the overhang (Codex
review r2 blocker; the band was redesigned so coda bars and the
brief tick sit INSIDE it). Floors (page-consistent grid): the F
disyllable squash holds — vowel median 0.366 vs 0.422 baseline,
minimum 0.220 vs 0.249, onset median 0.205 vs 0.249, no collapses.
The measured pair families are disyllabic; the trisyllable cell
(squash 0.327) is NOT floor-covered yet and visibly darkens (the m
ring squashes toward a blob) — briefs keep that tail rare, and it
is the named next measurement.

## Round 2 verdict (Edward, 2026-08-25)

**F is rejected** — "it just doesn't really work... squishing some
characters into not being very distinguishable." The uniform cell's
price (compressed internals) fails by eye even though the pair
floors pass — a recorded case of the occupancy metric not
capturing visual crowding. **D3 is the preferred page format**
("looks pretty good overall"). D0 remains only as the measurement
control. Standing adoption: D1+D2+briefs-direction (D3), F parked
with its measurement as the bound on what uniform cells would buy
(50% area) if a future letterform redesign survives squashing.

## SCOPE CORRECTION (Edward, 2026-08-25): this lane ran on GF-N,
## not GZ

Edward caught a session-long naming error: every round in this
lane (the engine bake-off, the compression dial, F-mode) rendered
the **GF-N inventory** — the narrow v0.2 core, 10 onsets × 5
vowels × 4 codas, raw space 200 (width-ladder.md; 320-512 on the
diphthong/wide rungs). **GZ is not that language.** Per gz-sketch.md
(Edward directive 2026-08-15), GZ is the greenfield ZONAL: it
inherits its syllable inventory from the Romance base — ~29-36
onsets including clusters, 8-14 nuclei (vowels + rising
diphthongs), 6-8 codas — a legal space of **~2,000-3,000
syllables** (chord co-design: 5,184 raw, ~2,073 after the humility
screen), roughly **10× GF-N**. And in GZ "the screen prunes pairs,
not space": nothing is reserved.

Consequences for the phoneme-space question Edward asked: in GZ it
dissolves. With thousands of usable syllables, the core vocabulary
can live at 1-2 syllables per word — the word-shortening that GF-N
could only buy through the sss capacity ledger (22 bodies → ~66
via priced POS-lane reuse) is GZ's *starting condition*. The
GF-N numbers in earlier drafts of this section (raw 50 bodies, 22
adopted) describe GF-N only.

Consequences for the script results in this doc and
gz-engine-bakeoff.md — what survives the re-scope and what does
not:

- **Substrate-level findings survive** [D]: appended-mark vowels
  phase-vanish, structural (frame) vowels cannot, briefs and
  fixed-cell trade the way they trade. These are properties of the
  rendering mechanisms, measured on GF-N letterforms.
- **All numeric floors and density figures are GF-N-scoped** [M on
  GF-N]. GZ needs ~3× the onset letterforms (extend-by-bases law,
  letterform-capacity.md — the wide-inventory question was already
  flagged there as GF-W's blocker), diphthong frames (the vowel
  grid has 9 positions for 5 assigned — headroom, but rising
  diphthongs need a glide mark), and cluster onsets (compositional:
  base + liquid mark is the natural move). Distinctness gets
  HARDER at that width; nothing measured here licenses GZ floors.
- **D1 does not port as-is**: GF-N's "h is the only particle
  onset" is false in GZ, whose grammar words are the Romance
  clitic set (le, les, a, de, no, va, se...) with varied onsets.
  The particle move must become a class-styling tier (small cell,
  full weight) justified by closed-class membership, not by a
  redundant onset.
- **Briefs port cleanly** (frequency logic is inventory-agnostic),
  and matter LESS: with mostly 1-2-syllable words, the brief
  tier's gain shrinks.

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
