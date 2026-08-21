# The tradeoff synthesis: narrow greenfield vs GF-W vs RZ
(the lane-2 capstone — everything measured or computed so far, in one
place; hypothesis-tagged per the epistemic policy)

Columns: **GF-N** (narrow greenfield, the spec'd v0.2 language),
**GF-W** (wide variant, computed sketch), **RZ** (Romance zonal,
6-register corpus). English shown where it anchors intuition.
Tags: [M] measured/computed here · [D] derived arithmetic ·
[H] hypothesis.

## 1. The core table

| dimension | GF-N | GF-W | RZ |
|---|---|---|---|
| phonemes | 16 [M] | 22 [M] | ~26 (inherited) |
| content syllables | 200 [M] | 320 [M] | ~1.5–3k [D] |
| safe monosyllabic roots | 22 [M] (menu to ~66 [H]) | 38 [M] | n/a (inherited lexicon) |
| syllables/word (fable/corpus) | 1.76 [M] | ~2.0 [D] | 1.83 [M] (617-token corpus; different measurement corpora: 617 = the six-register blockquotes at the time of this measurement; 335 = the earlier snapshot of the same blockquote corpus used by gz-sketch.md and rz-chording.md; 690 = the de-duplicated coverage corpus of tools/coverage.py) |
| words/proposition (fable) | 17 [M] | 17 [M] | 22 [M] |
| universal L1 floor | strongest [H] | weakened (voicing/f/z/r remap) [H] | none claimed |
| Romance/EN mnemonic hooks | weak (funnel) [M-ish] | **near-RZ** [H] | native-grade |
| receptive reach at t=0 | 0 | 0 | ~900M gist [H, unmeasured] |
| engineered channels (check, SSM, modes, POS coda) | full | full | dies/partial (see portfolio matrix) |
| script | featural blocks + fused chars (measured floors) | needs wide letter cells (blocks r5y) | Latin primary + display layer (floors fixed, tested) |
| chording | 1 stroke/word [H — no layout yet] | same [H] | ~1/syllable, steno-class [D] |

## 2. What the numbers actually say

1. **GF-W is the interesting middle.** +73% safe roots (22→38 [M]),
   near-RZ hooks [H], full channel machinery — for the price of the
   universal-floor story and a denser confusion graph. If the
   project's real audience is the Romance+English cohort (it is, for
   any early community), GF-W plausibly dominates GF-N: the narrow
   variant's universality premium protects populations the project
   won't reach for years, while GF-W's hook dividend pays immediately
   in learnability — the top-ranked objective.
2. **RZ's costs are now concrete**: 22 words and 40 syllables where
   the greenfields spend 17/30–34; no channel machinery; in exchange,
   its zone reads it at sight (unmeasured but the mechanism is
   Interslavic-precedented) and its lexicon designs itself.
3. **The width decision is the hinge for everything parked**: the
   stroke/fusion script work, the fused-character density story, and
   the GF seed lexicon all change shape at 16 vs 10 onsets. Decide
   width before resuming any of them.
4. **Honest unknowns that gate real conclusions**: no human has read
   any of these (cloze parked by directive); chord layouts don't
   exist (stroke counts are projections); GF-W is a sketch without
   check-bit/digit integration; RZ receptive numbers are borrowed
   from Interslavic's zone, not measured in ours.

## 3. Decision framing for Edward (the one-way doors)

- **Width (GF-N vs GF-W)**: changes spec, script, lexicon; cheap to
  decide now while the lexicon is 37 roots, expensive after. The
  hook dividend argues wide; the universality thesis argues narrow;
  a dual-spec (narrow core ⊂ wide extension, which the spec's §9
  family design anticipated) may capture both at bookkeeping cost.
  UPDATE (conlang-4h1): the door is wider than binary — the computed
  width ladder (width-ladder.md) runs GF-N 22 → GF-ND 28+ → GF-W 38
  → GF-WD ~53 → GF-C ~93 mono roots, all rungs supersets with modes
  identical; the decision is a point (or nested pair) on the GF↔RZ
  axis. Diphthongs are the cheapest capacity (GF-ND matches GF-W's
  syllable count on the 10-consonant floor); GF-WD is the flagged
  upper point short of the cluster rung's phonotactic bill.
  DIRECTIVE (Edward, 2026-08-15): the upper point is now **GZ, the
  greenfield zonal** — channel fruit on a Romance-ish base, loose
  root reuse (gz-sketch.md, conlang-z0s). This moves on the
  *discipline* axis the ladder held fixed, and tentatively resolves
  RZ's role as donor base + receptive sibling.
- **RZ's role**: main track, side track, or method-demo. Its
  development is cheap (the recipe machinery works) but its demand
  case took real damage in the milestone reviews (Interlingua
  overlap, producer absence).
- Neither decision needs to be now; both need to be *before* the
  freeze gate and before resuming the script work.
