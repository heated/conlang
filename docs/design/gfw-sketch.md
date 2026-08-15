# GF-W: the wide greenfield variant (computed sketch)

Numbers from `tools/explore_wide.py` (real lexgen runs on a
programmatically widened spec, humility machinery applied to every
added contrast).

## Inventory

Narrow 10 content onsets + **b d g f z r** = 16 (+h particles).
Vowels stay 5 (the universal sweet spot; adding ə/ɛ-class vowels
prices out far more L1s than consonants do). Codas unchanged
(∅ n s l = the POS system transfers intact).

**L1 pricing of the additions** (each contrast excludes/remaps
someone — the wide bet trades the narrow variant's universal floor
for capacity and hooks):

| added | who pays | mitigation (humility coverage) |
|---|---|---|
| b d g | Mandarin (voicing→aspiration remap), Korean (3-way remap) | p/b, t/d, k/g covered — no unrelated minimal pairs |
| f | Korean, Filipino, some Austronesian (f→p) | f/p covered |
| z | Spanish (z/s merger), many others | z/s covered |
| r | Japanese, Korean (r/l merger); rhotic quality varies wildly | r/l covered; any rhotic accepted |

The humility machinery generalizes cleanly: every added phoneme's
confusion pairs enter the covered set, so speakers who merge a pair
never face an unrelated minimal pair on it. The cost is capacity
below the naive doubling — and the measured result is:

## Computed capacity

| | narrow | GF-W |
|---|---|---|
| content onsets | 10 | 16 |
| content syllables | 200 | 320 |
| candidate bodies | 48 | 78 |
| **adopted-MIS monosyllabic roots** | **22** | **38** |

38 safe monosyllabic roots (× the POS-reuse menu if adopted) moves
the monosyllable band from "pronouns and a handful of cores" to "the
whole conversational core", pulling average word length down toward
~1.3–1.5 syllables — density in speech, and in script (1-syllable
characters dominate, largely dissolving the fusion crowding problem).

## The hook dividend (unexpected, large)

The narrow inventory's 10-onset funnel killed most Romance hooks
(no f r b d g v z). GF-W restores them: *vento* fits as `vento`,
*forte* as `forte`, *luz* as `luz`, *grande* as `gande`~`grande`
(cluster rules pending), *bon* as `bon`. The wide variant is not
just denser — **its lexicon can be dramatically more evocative for
the Romance+English cohort**, converging toward RZ-adjacent shapes
while keeping the engineered channel machinery. GF-W sits *between*
the narrow greenfield and RZ on the reach-vs-engineering spectrum,
and may dominate the middle: near-RZ mnemonics + full channel
discipline.

## Costs, honestly

1. The universal-floor story weakens: some L1 cohorts now hear
   merged pairs everywhere (mitigated but not erased by coverage).
2. Confusion-graph density grows; the check/humility bookkeeping has
   more pairs to cover; per-symbol margins shrink (the narrow bet's
   original rationale).
3. Script letter inventory needs the wide-model cells (the parked
   stroke work's open question — this is the width decision r5y is
   blocked on).
4. Digit-code compatibility: the tens map stays on the narrow 10
   onsets (modes unchanged), so GF-W is a superset, not a fork.

## Same-fable sample (GF-W seed shapes, hook-first)

> vento norte-s ha sol hoon disputa, cu hees la mus forte-s;
> viajor hoon vade, kovri-s his manto kaldo-s.

(vs narrow: `weto nos ha so hoon luta…` — the GF-W line is nearly
sight-readable to the Romance cohort while remaining a channel
language. 17 words, 30 syllables → 17 words, 34 syllables: GF-W
spends a little length to buy recognizability; word count and
character count unchanged.)

## Spec-integration notes (toward a real GF-W spec bump)

- Digits: the tens map stays on the narrow 10 onsets — modes are
  IDENTICAL in GF-N and GF-W (superset property preserved; a frame
  spoken in either is valid in both).
- Check bits for b d g f z r were assigned provisionally in
  explore_wide.py; a real spec bump must re-run the check-coverage
  analysis (covered pairs differing in check bit) over the widened
  confusion graph — machinery exists (spec_check patterns).
- Particles unchanged (h-class untouched). SSM unchanged. POS codas
  unchanged. Script letter cells: needs 6 new onset cells — the
  parked r5y stroke work's first real task if width goes wide.

## Status

Sketch + computed capacities only. Not adopted. Feeds the width
decision that blocks r5y, and the tradeoffs synthesis. Next if
pursued: full spec variant (check bits, digit compatibility
verified, script letter cells), GF-W seed lexicon pass, and the
L1-coverage audit against real population data.
