# Fused word-characters: the one-glyph-per-word study (r5y, v0)

Bead conlang-r5y. Edward's ideal ("more like chinese but ideally one
glyph per word"). Implementation: `tools/fused_script.py`; specimen:
`.ship-notes/fused-specimen.svg`. Workshop-stage (validator-light);
measurements via the raster machinery in `tools/script.py`.

## Design

**The unlock is the abugida move**: delete the vowel carrier bar
(~30% of block width); vowels become miniature carrier *stubs*
attached at the onset letter's right edge — same feature logic
(height = vowel height, tick direction = backness), preserved at ~1/3
size after the full-size in/out ticks proved too fragile in first
render.

Character anatomy (one 100×100 square per word):

- 1–3 syllable-letters left→right (temporal order), scaled by count
  (90% / 55% / 38%);
- **POS strip spans the character bottom** — the final coda *is* the
  word's POS, so the strip was always word-level ink; fusion makes
  that literal;
- medial codas: small bar under their own letter; per-syllable check
  dots above the slots (computed, droppable);
- particles render at 60% — the silhouette grammar (small scaffold,
  square content words) survives fusion;
- **stroke-width floor** (4.4u): sub-pixel ink is fusion's death
  mode; scaling letters must not scale their ink to invisibility.

Codespace, CORRECTED (2026-08-15 review): the legal content space is
**200 non-final × 150 active-final = 30,000 disyllabic wordforms**
(10,000 root bodies before constraints) — the earlier 220² ≈ 48k
figure counted particle syllables and ignored the final-POS
restriction; 48,400 is only a nonlinguistic Cartesian shape count.

## Measured results (point-sampled occupancy, phase-min over 4
alignments — a *harsher* model than antialiased rendering; same
metric family as the v0.2 floors)

The fair frame is **equal line height H** (the practical typesetting
constraint): a stacked disyllable at H gives each block H/2; the
fused character gets the full H.

One-channel-neighbor separability (hardest pairs — words differing in
a single channel of one syllable), disyllables:

| line height | fused min / median | stacked min / median |
|---|---|---|
| 20 px | 0.000 / 0.256 | 0.000 / 0.043 |
| 28 px | **0.041 / 0.292** | 0.000 / 0.159 |
| 40 px | 0.055 / 0.301 | 0.052 / 0.267 |

Trisyllables at 28 px: fused 0.054 / 0.108 vs stacked 0.000 / 0.061.

**RETRACTED (2026-08-15 code review, BLOCKER): the comparison below is
confounded** — equal line height grants the fused square ~n× the area
of the stacked column, the stroke floor was applied only to the fused
side, the experiment was never checked in, and occupancy-IoU is a
regression ratchet being used as legibility evidence. The claim
"fusion wins" is withdrawn pending a fair factorial experiment
(layout × optical floor, equal-height AND equal-area, antialiased
rasters, checked-in generator). Original text follows for the record:
fusion is not a legibility trade at equal line height —
it wins at every measured size and word length. The crowding fear
was calibrated against the wrong baseline: stacking pays H/n per
syllable; fusion pays ~0.55H (disyllables) plus the reclaimed carrier
width, and the stroke floor keeps thin ink alive. Trisyllables are
the strained case for *both* layouts (fused median 0.108 is tight —
the style pass should prioritize the 0.38-scale letterforms).

Also observed while measuring (applies to v0.2 too, previously
untested at full-block scale): the single POS strip bar can vanish
entirely at worst-case pixel alignment at 14 px full-block rendering
(caa/can indistinguishable at one phase). Real renderers antialias —
a hairline survives — but the strip's stroke weight deserves a look
in the next ink pass for both layouts.

## What fusion buys and costs (updated trait sheet)

- One character per word: word count = character count; uniform line
  height (stacking's 1–3-block sawtooth gone); the derivation family
  is *visible* — sala/salaan/salaas share letterforms and differ only
  in the strip.
- Chording alignment improves to the word level: mirrored-hands
  chording types one disyllable per stroke = **one stroke, one
  character, one word** — the motor, visual, and lexical units
  coincide exactly for the dominant word class.
- Cost: per-letter detail at 55%/38% scale demands the stroke floor
  and favors larger body text than unfused blocks would need for
  *single* syllables; the metric says the fused word still beats the
  stacked word at any fixed line height, so this cost only binds
  against non-word baselines.
- Check dots at 4.5r are marginal at small sizes (2D point-sampling
  misses them below ~20 px); acceptable for a computed/droppable
  layer.

## Fair experiment results (2026-08-15, tools/fusion_study.py —
replaces the retracted comparison; full table in
docs/design/fusion-study-data.md, generated)

Antialiased coverage rasters, Soergel distance, phase-min, factorial
layout x stroke-floor x frame. Honest findings at H=28:

1. **Disyllables are layout-indifferent** under this metric: all six
   conditions cluster (min 0.038-0.057) in both frames. The disyllable
   layout choice is therefore free to be decided on density,
   aesthetics, and chording alignment — not legibility.
2. **v1 radical composition measurably wins trisyllables** in BOTH
   frames (equal-height min 0.064-0.085 vs stacked 0.024-0.036;
   equal-area 0.043-0.056 vs 0.024-0.036). Stacking's worst-case
   trisyllable pairs are the weakest cells in the whole design.
3. **The stroke floor is not uniformly good**: it helps v1
   trisyllables (+0.02 min) and hurts stacked/v0 disyllable minima —
   optical weight needs per-layout tuning, not a global constant.
4. Scope: proxy-metric evidence (regression-grade), still not human
   legibility. No "X beats Y" claim beyond this metric is made.

## v1 addendum (same day): radical composition

Edward's review of the v0 specimen: "kinda cursed — less chinese and
somewhat more randomly underline english; variable char size."
Diagnosis confirmed: v0's anatomy (letter row in a box + full-width
POS rule) reads as decorated Latin. v1 (`word_char_v1`) recomposes
hanzi-style: components FILL regions (1-syl = the square; 2-syl =
⿰ halves; 3-syl = left + stacked right, like 湖), the POS becomes a
bottom radical region with SHORT centered marks, medial codas become
corner ticks, and cells get fill-fitted scales for even ink density.
Comparison render: `.ship-notes/fused-v1-comparison.svg`. Verdict:
POS de-underlined and trisyllables now genuinely compose; the
remaining gestalt gap is disyllable unity (still reads as a letter
pair) — next iteration: asymmetric ⿰ split (~40/60), inter-component
interlock, and possibly shared strokes at the midline. Crowding
numbers for v1 to be re-measured after that pass.

## Open items

1. Style/beauty pass on the 0.38-scale trisyllable letterforms (the
   measured weak spot) — feeds bead 0eh.
2. Real-size legibility check with antialiased rendering (the
   point-sampling metric is conservative; confirm the ordering
   holds).
3. Spacing: fused characters are uniform squares — word gaps can
   shrink to ~10u or adopt the RZ headstroke trick; not yet measured.
4. Suffix/particle interaction with modes frames (payload runs in
   fused mode) — with conlang-bcq machinery when mode text rendering
   exists.
5. Freeze-gate: fused mode is now the third layout candidate
   (stacked / headstroke / fused) and, on this evidence, the leading
   one. The paragraph-specimen comparison for the gate should include
   it.
