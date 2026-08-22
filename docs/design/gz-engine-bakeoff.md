# GZ script-engine bake-off — round 1 (conlang-e35, 2026-08-22)

The program charter left one fork open in the script lane: which
rendering ENGINE carries the GZ script. This round put four
genuinely different engines over the same GZ-shaped specimen
(vowel-minimal word set + 99-token particle-bearing paragraph),
with raster-floor and density measurements as rails. Tool:
`tools/engine_bakeoff.py`; images surfaced in
`.ship-notes/workshop/gz-engine-r1/` (workshop protocol; verdict is
Edward's). All numbers [M] on the current prototype renderers; all
taste judgments [A].

## The four engines

- **E0 — boxed featural blocks** (v0.2 `script.py`): the incumbent.
  Syllable blocks stack per word; vowel = carrier tick; coda =
  strip mark.
- **E1 — continuous stroke chain** (`strokes_continuous.py`, the
  conlang-h05 build): letters are stroke programs joined by drawn
  connectors; the vowel IS the join (slope = height, reach =
  backness; word-final = same rule as terminal tail + hook). One
  unbroken figure per word.
- **E2 — fused narrow character** (`fused_v3.py` N1 spine,
  generalized 1-3 syllables): one 64u-wide spine-bound character
  per word; vowel = small right-edge bar.
- **E3 — syllable block with vowel as structure** (the Hangul move,
  new): the vowel is the block's frame — front vowels a right
  vertical bar, back vowels a bottom horizontal bar, *a* the corner
  L; mid height doubles the bar. Onset letterform fills the
  remaining region; coda = bottom radical; blocks stack per word.

## Measured floors [M]

Phase-minimized occupancy distance, one-feature-different
disyllable pairs, cell size ~ letterform/6 (comparable across
engines):

| engine | vowel min | vowel med | onset min | onset med |
|---|---|---|---|---|
| E0 | 0.000 | 0.000 | 0.000 | 0.321 |
| E1 | 0.069 | 0.313 | 0.143 | 0.512 |
| E2 | 0.000 | 0.000 | 0.000 | 0.226 |
| E3 | 0.071 | 0.340 | 0.000 | 0.243 |

Findings:

1. **The tick/appended-mark vowel family is disqualified as
   built**: E0 and E2 render MOST vowel-different word pairs
   identically at reading raster (median 0.000, not just min).
   This generalizes the §5 stroke-system finding to the boxed
   incumbent — it was never measured at word scale before.
2. **The onset zeros are one hazard cell, p/j** (bare vs crossed
   vertical; the crossbar phase-vanishes at block scale). E1 alone
   survives it because j's exit anchor reshapes the connector —
   letter identity leaking into word topology is a structural
   robustness property of join-based engines.
3. **E3 is the only engine where a vowel change moves more ink
   than an onset change** (ratio 1.4) — structural vowels cannot
   phase-vanish, by construction rather than by tuning.

## Density [M]

99-token paragraph at equal letterform size (~12px), area per word:
**E1 2156 < E2 2475 < E3 3001 < E0 3506 px²**. The incumbent is
simultaneously the sparsest and the least distinct — it loses both
axes it was meant to trade between.

## Trades on the table (decision is Edward's)

- E1 wins floors + density + continuity but is a horizontal script
  — wide words, against every prior sprawl verdict; coda underline
  provisional.
- E3 wins gestalt-by-construction (compact designed-character
  blocks, first-class vowels, even ink) at mid density; warts: the
  p/j cell, and horizontal-bar pileup on back-vowel + coda
  syllables.
- A live hybrid for round 2: E2's spine/narrow-character body with
  E3's structural-vowel move.
- E0 has no measured virtue left; its case is lineage only.

Shadow pick sealed in `docs/process/workshop-shadow-log.md`.
