# Letterform capacity: can the script carry a wide inventory?
(exploration, 2026-08-22; `tools/letterform_capacity.py`)

width-ladder.md left GF-W with a blocking question: the wide
greenfield wants 16-19 onsets, GF-N's script has 11 letters, and
"it forces the script letter-inventory question — exactly what
blocks the parked stroke work." Nobody had put numbers on it. Now
measured, with the same instrument as every other floor in the repo
(occupancy rasters, phase-minimized over 9 alignments, 14px letter
box, the v0.2 letter floor of 0.15).

## Result 1: the script does not block GF-W

| grid | implemented cells | letters certified ≥0.15 | worst pair | % of all pairs below floor |
|---|---|---|---|---|
| shipped (5 bases × 4 modifiers) | 16 | **15** | 0.208 | 0.8% |
| +2 modifiers (5 × 6) | 26 | 21 | 0.167 | 2.2% |
| **+3 bases (8 × 4)** | 23 | **22** | 0.179 | **0.4%** |
| full candidate grid (8 × 6) | 39 | 30 | 0.167 | 1.9% |

Two readings:

- **GF-N is already running under capacity.** The shipped feature
  grid certifies 15 letters at the reading floor; GF-N uses 11. Four
  letters of headroom exist today with no new shapes at all — enough
  for the GF-ND rung.
- **GF-W's 16-19 onsets fit comfortably via three new bases**
  (arc, chevron, box): 22 certified, and the *lowest* collision rate
  of any scenario. The script is not the constraint on the width
  ladder. The parked stroke work can be unblocked on this evidence.

## Result 2: bases are the safe axis, modifiers are where letters die

Pairs that differ in exactly one feature, across the full candidate
grid:

| differ only in… | mean distance | min |
|---|---|---|
| **base** (n=115) | **0.815** | 0.425 |
| **modifier** (n=79) | 0.358 | **0.000** |

A base change is worth 2.3x a modifier change on average, and never
drops near the floor. A modifier change can vanish completely.

**Every one of the 14 sub-floor modifier pairs is a plain-vs-small-
mark pair** — the two candidate modifiers I added (`dotted`,
`hooked`) against plain: angle plain/dotted measures **0.000**
(identical at reading size), box, circle, chevron, vertical and arc
all follow at 0.06-0.10. The four shipped modifiers (plain, crossed,
doubled, capped) never collide, because each of them *spans the
cell*: crossed lays a stroke across the whole box, doubled
duplicates the base across it, capped adds a full-width bar.

## The law this makes explicit (measured twice, independently)

> **Contrast that changes the SHAPE survives reading size; contrast
> carried by a small added mark does not.**

The same finding fell out of the stroke-system experiment the same
day (stroke-system.md §5): vowel branch ticks measured **0.000** at
worst case, and moving the vowel into *join topology* — a change to
the figure's shape — lifted it off zero and multiplied the median by
5.6x. Two different subsystems, two different failure cases, one
cause: **small ink phase-vanishes; structure does not.**

Design consequences:

1. **Extend the inventory by bases, not modifiers.** The featural
   bet says modifiers should be cheaper to *learn* (one new mark
   reused across N bases yields N new letters, versus one base
   yielding M). That learnability argument still holds — but it now
   carries a measured legibility price, and the modifier vocabulary
   is nearly exhausted: the four shipped modifiers are the cell-
   spanning marks that exist. A fifth would have to be invented
   *as a cell-spanning transform*, not as a dot or a hook.
2. **Audit any future modifier against the plain cell specifically.**
   The collisions are not modifier-vs-modifier; they are
   modifier-vs-plain. Plain is the dangerous neighbor.
3. **This retro-justifies a shipped choice**: v0.2's ban on
   circle+doubled and angle+capped was made on geometric intuition;
   the measurement says the real risk was elsewhere, and the shipped
   set survives because its modifiers all happen to be structural.

## Caveats

- The three candidate bases (arc, chevron, box) are workshop
  geometry, not designed letterforms; a real assignment pass would
  redraw them and re-run. Their *distances* are what matters here,
  and those are generous (min 0.425 base-only).
- Occupancy IoU is a proxy for legibility, not legibility. It is the
  repo's standard regression instrument and is used here the same
  way: to compare conditions, not to certify human reading.
- Certification is greedy (most-robust-first) and therefore a lower
  bound on the maximum inventory.
