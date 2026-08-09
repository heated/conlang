# Script v0.2: the confusion-aware anti-iconic assignment

Decision record for conlang-wqj (delegated by Edward, 2026-08-09:
"i dont care about iconic vs not. use ur best judgement"). Solver:
`tools/assign_glyphs.py` (deterministic; rerun it to reproduce the
table below from `channels.json` confusion data).

## The question

v0.1 mapped articulation to ink (place→base, manner→modifier), so
phonetically close onsets looked alike. The Fable design review showed
this puts the ear's worst pairs (m/p, n/t) on the script's most
erodible features, while creating *new* eye-only confusions (s/t, c/j,
w/p) the lexicon couldn't see. Edward's tentative directive: anti-iconic
assignment — ear-confusable phonemes get maximally distinct marks, the
eye becomes independent redundancy.

## The decision

**Keep the compositional grammar; solve the assignment as an
error-correcting code.** Iconicity was never the load-bearing part of
the featural bet — compositionality was (few primitives, systematic
combination, chord correspondence). What changes is *which* phoneme
gets *which* (base, modifier) cell:

- HARD: every phonetic confusion pair (covered ∪ forbidden ∪ weighted;
  12 pairs) differs in **both** base and modifier — visual distance 2.
  No single degraded feature class can merge an ear-confusable pair.
- HARD: bases and modifiers are all robust contrast classes (full
  strokes, wide doubling, attached caps/crossings — no floating bars,
  breaks, dots, or fill contrasts in the letter grammar).
- HARD: distinct cells; banned cells (circle+doubled, angle+capped —
  no robust realization) unused; 2–3 letters per base; h keeps the
  tick base alone (lightest glyph = particle scaffold).

A perfect solution exists and the ordered DFS finds it in <0.1 s:

| onset | cell | glyph | digit |
|---|---|---|---|
| c | circle plain | ○ | 0 |
| p | vertical plain | ǀ | 1 |
| t | diagonal crossed | ╳ | 2 |
| k | angle doubled | nested ⌐⌐ | 3 |
| m | circle crossed | Ø | 4 |
| n | vertical doubled | ‖ (wide) | 5 |
| s | diagonal doubled | ⫽ (wide) | 6 |
| l | angle plain | ⌐ | 7 |
| w | circle capped | ○ with top bar | 8 |
| j | vertical crossed | + | 9 |
| h | tick doubled | = | — |

**Emergent mnemonic:** base = tens-digit mod 4 (circle 0/4/8, vertical
1/5/9, diagonal 2/6, angle 3/7) — an artifact of digit-ordered search
that makes mode reading trainable by rule.

## Measured outcome (occupancy raster of the onset zone, minimized
over sub-cell sampling phases; `tools/script.py rasterize`, enforced
by `test_script.py`)

- minimum distance over the 12 **phonetic** pairs at 14×14: **0.623**
  (l/w; single-phase 0.714) — v0.1's m/p and n/t differed by a
  floating bar that merges, the collapse class; now every phonetic
  pair differs by base AND modifier
- minimum over **all** 55 onset pairs at 14×14: **0.195** (c/m) — the
  closest pairs are same-base pairs. For a *listener* those are safe
  (phonetically distant); for a silent *reader* phonetic distance is
  no protection (review correction, 2026-08-09), so the same-base
  pairs are listed exhaustively in `script_confusion_pairs` and priced
  by `lexgen strict_with_script`: cost at current inventory is one
  root body (strict 18 → 17). `spec_check` enforces that every
  same-base pair stays listed. w's cap was widened with end-drops
  after review measurement showed c/w vanishing at a 7×7 raster
  (0.000 → 0.250; 14×14 0.231 → 0.348).
- coda marks (full-width strip bars): n/s 1.000, n/l 0.723, s/l 0.600
  phase-min (the n/s 1.000 is partly an interleaved-bands artifact of
  the occupancy metric — flagged for blur-based re-measurement at the
  freeze gate)
- regression floor: all pairs ≥ 0.15, phonetic ≥ 0.55, codas ≥ 0.50,
  phase-minimized, ink window guarded

## What was given up

- The articulation mnemonic ("p and m share a base because both are
  labial"). Assessment: Hangul learners acquire jamo mostly through
  practice, not featural theory; the systematic grammar (11 letters
  from 5 bases × 4 modifiers) is retained, and the digit-mod-4 rule
  replaces the articulation story for the mode subsystem where per-pair
  discrimination actually has no lexical safety net.
- Mishearing→glyph iconicity ("you can see which mishearings a word
  invites"). Replaced by its converse, which is worth more: a
  *misreading* of a same-base pair produces a phonetically implausible
  word (the ear's model rejects it), and a *mishearing* produces a
  visually distant glyph (the eye rejects it). Each channel covers the
  other's weak pairs instead of sharing them.
