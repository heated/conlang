# GZ script-engine bake-off — round 1 (conlang-e35, 2026-08-22)

> **Scope correction (Edward, 2026-08-25):** the "GZ-shaped text"
> below is actually **GF-N-shaped** — the narrow v0.2 core
> inventory (10 onsets, 5 vowels), not GZ, which per gz-sketch.md
> inherits Romance's phoneme space (~29-36 onsets incl. clusters,
> 8-14 nuclei, ~2,000-3,000 legal syllables). The engine-level
> findings (structural vs appended-mark vowels, etc.) are
> mechanism properties and stand; every numeric floor and density
> figure is GF-N-scoped. The GZ-width port (3× letterforms via
> extend-by-bases, diphthong frames, cluster onsets, clitic-class
> particles) is open work — see gz-script-efficiency.md.

The program charter left one fork open in the script lane: which
rendering ENGINE carries the GZ script. This round put four
genuinely different engines over the same GZ-shaped specimen
(vowel-minimal word set + a 105-token particle-bearing paragraph),
with raster-floor and density measurements as rails. Tool:
`tools/engine_bakeoff.py`; images surfaced in
`.ship-notes/workshop/gz-engine-r1/` (workshop protocol; verdict is
Edward's). All numbers [M] on the current prototype renderers; all
taste judgments [A]. A Codex xhigh review of the first draft found
four blockers (floating join anchors; non-square, non-comparable
raster cells; density scales that did not equalize letterform size;
an isolation mode presented as the full renderer) — everything
below is post-fix, and the fixes are recorded where they changed a
conclusion.

## The four engines

- **E0 — boxed featural blocks** (v0.2 `script.py`): the incumbent.
  Syllable blocks stack per word; vowel = carrier tick; coda =
  strip mark. Measured in two modes: full renderer, and
  vowel-channel-isolated (register check dot stripped — the dot is
  a whole-syllable function that adds distance to some vowel pairs
  through a side channel).
- **E1 — continuous stroke chain** (`strokes_continuous.py`, the
  conlang-h05 build): letters are stroke programs joined by drawn
  connectors; the vowel IS the join (slope = height, reach =
  backness; word-final = same rule as terminal tail + hook). One
  unbroken figure per word (with an anchors-on-ink regression test
  after the review caught t/s/h anchors floating in whitespace).
- **E2 — fused narrow character** (`fused_v3.py` N1 spine,
  generalized 1-3 syllables): one 64u-wide spine-bound character
  per word; vowel = small right-edge bar.
- **E3 — syllable block with vowel as structure** (the Hangul move,
  new): the vowel is the block's frame — front vowels a right
  vertical bar, back vowels a bottom horizontal bar, *a* the corner
  L; mid height doubles the bar. Onset letterform fills the
  remaining region; coda = bottom radical; blocks stack per word.

## Measured floors [M]

Phase-minimized occupancy distance over one-feature-different
disyllable pairs; square windows, square cells, cell size derived
from each engine's measured median onset-ink span, phases = thirds
of the cell pitch. Two resolutions: the READING raster (stroke ≈ 1
cell, ~12px onsets) is the primary table; the EXTREME raster (~6px
onsets, sub-cell strokes mostly vanish) is a fragility probe.

Reading raster (primary):

| engine | vowel min | vowel med | onset min | onset med | v/o ratio |
|---|---|---|---|---|---|
| E0 vowel-channel | 0.039 | 0.046 | 0.041 | 0.312 | 0.15 |
| E0 full (+dot) | 0.037 | 0.073 | 0.066 | 0.323 | 0.22 |
| E1 | 0.089 | 0.299 | **0.209** | **0.569** | 0.53 |
| E2 | 0.022 | 0.084 | 0.038 | 0.272 | 0.31 |
| E3 | **0.249** | **0.422** | 0.049 | 0.249 | **1.70** |

Extreme raster (fragility probe — zero-distance pair counts):

- **E0**: vowel channel 12/20 pairs render IDENTICALLY; the full
  renderer still leaves 4/20 identical (e/o and i/u, both
  positions) — the check dot partially rescues the vowel channel
  by accident of register parity, which is a side channel, not
  vowel ink. Onset zeros: l/k, p/j, w/c.
- **E2**: total vowel collapse — 20/20 pairs identical — plus
  onset zeros l/k, p/j, w/c, m/c.
- **E1**: one zero (word-final e/i — the terminal-tail slope is
  the scheme's thinnest ink); no onset zeros.
- **E3**: the only engine with NO vowel zeros even here; onset
  zeros l/p, p/j.

Findings:

1. **No engine is broken at reading size, but the margins differ
   by 5-9x.** The tick/appended-bar vowel family (E0 channel
   0.046, E2 0.084) sits an order of magnitude below the
   structural-vowel engines (E1 0.299, E3 0.422) on median, and
   dies outright at the extreme raster.
2. **E3's vowels cannot phase-vanish** — the only engine whose
   vowel channel survives the extreme raster untouched, and the
   only one where a vowel change moves more ink than an onset
   change (ratio 1.7). The price shows up in the onset channel:
   squeezing letterforms into vowel frames leaves E3 the weakest
   onset margins (min 0.049, med 0.249).
3. **E1 owns the onset channel** (min 0.209 = 4-5x everyone else)
   and is the only engine with no extreme-raster onset zeros:
   letter identity leaks into the connector topology, so onset
   contrasts are carried at word scale, not just letter scale.
4. **The recurring onset hazard cells are p/j, l/k, w/c** (single
   stroke vs. same-stroke-plus-one-mark) — the added mark is what
   phase-vanishes. This is the small-mark law showing up inside
   letterforms, not just diacritics.

## Density [M]

105-token paragraph, scales computed so every engine renders
onsets at the same 12px (measured bbox spans, not hand-picked),
fixed 10px inter-word gap. Area per word: **E1 2004 < E2 2678 <
E0 3304 ≈ E3 3313 px²**. E1's ~25-35% lead is robust across
normalization variants tried; the E0-vs-E3 comparison is
normalization-sensitive (they traded places between two reasonable
onset-size metrics), so the honest claim is parity.

## Trades on the table (decision is Edward's)

- **E1** wins onsets + density + continuity; its vowels are good
  (0.299) but not E3's; it is a HORIZONTAL script — wide words,
  against every prior sprawl verdict; codas are a provisional
  underline; word-final e/i is its thin cell.
- **E3** wins the vowel channel outright at incumbent-level
  density; compact designed-character blocks, even ink. Warts:
  weakest onset margins (frames squeeze letterforms), and
  back-vowel + coda syllables pile up horizontal bars (o + s coda
  = four parallel bars — reads monotonous).
- **E2** as built is dominated: weak vowels, weak onsets, mid
  density. Its narrow-spine BODY is still live as a hybrid with
  E3's structural-vowel move — a real candidate for round 2.
- **E0** has the lineage and nothing else measured: weakest vowel
  channel at reading size, dead at extreme, sparsest page (tied
  with E3, which at least buys best-in-class vowels for it).

All reversible; nothing touches the feature grammar or the frozen
letter identities (E1/E3 reuse the stroke-program letterforms).

Shadow pick sealed in `docs/process/workshop-shadow-log.md`.

## Round outcome (Edward, 2026-08-25)

Edward reviewed all four: E1 "interesting" but with blocking look
objections (jarring s-joins; sala/sola not eye-distinguishable;
piton "kinda bad"); E2 better than E0 but "same issue"; E3 like E0
but "leaning into the blockiness... maybe a little better". His
governing point: every page is "still not very efficient per se" —
the missing axis is COMPRESSION, which no transparent rendering can
show. He **delegated the engine call to the agent**.

**Adoption (agent, under that delegation): E3 substrate.** Best
measured vowel channel at every raster, Edward's mild lean, and the
block form composes directly with the compression moves. E1's
connector mechanism is parked as a possible handwriting/ligature
mode, not adopted. The efficiency layer built on this substrate is
`docs/design/gz-script-efficiency.md` — that lane, not further
substrate rounds, is where the script goes next.
