# Compositional stroke system + fusion grammar (workshop draft)

Bead conlang-r5y continuation, per the 2026-08-15 direction chat.
Objective order: learnability > reading ergonomics > density > beauty.
Display-only. The two moves:

## 1. The stroke refoundation

The v0.2 letters were *placed geometric marks* in boxes — the source
of the "algebra look" and the sparse-recursion problem. But every
v0.2 letterform already decomposes into a small stroke algebra, so we
refound the substrate without reassigning the alphabet:

**Primitives (8):** vertical, horizontal, rising diagonal, falling
diagonal, left arc, right arc, top arc, bottom arc — each with a
length parameter.

**Join grammar (4):** `corner` (endpoints meet at an angle), `cross`
(midpoint intersection), `touch` (T-junction: end onto middle),
`gap` (no join — rationed, per robust-ink doctrine).

A letter = a short stroke *program* (1–4 strokes + joins), rendered
as connected paths with round joins — ink that meets, instead of
marks that float. The 11 letter identities are unchanged (p =
vertical; l = corner; t = cross of diagonals; k = nested corners;
m = arc-pair crossed; …): same anti-iconic code, new substrate. The
learnability story *improves*: 8 strokes + 4 joins is the featural
bet one level down, and the measurement floors re-run unchanged.

**Vowels become branches, not satellites**: a short branch stroke
off the letter's spine (position along spine = height: 0.2/0.5/0.8;
side = backness; both = central). Attached ink — no floating stubs.

## 2. The fusion grammar (composable density)

Density without arbitrary memorization: dense forms are *derived by
rule*, decodable slowly at first, read holistically with practice
(fluency, not memorization, is where logogram-speed comes from).
Three operations, applied by **frequency band** (the Zipf dial as
compression aggressiveness):

| band | who gets it | operations |
|---|---|---|
| 0 transparent | tail vocabulary | letters side by side, standard gap |
| 1 connected | mid-frequency | `touch`-join adjacent letters at declared exit/entry anchors — words become connected figures |
| 2 fused | top-frequency band | shared-stroke merge (compatible exit/entry strokes drawn once) + redundancy drops — maximal compression, still rule-derived |

Same word → same form, always; sound-out ladder intact at every band.
Particles/grammar words sit in band 2 by frequency automatically.

## 3. Status & measurements

Prototype: `tools/strokes.py` (stroke programs for the 11 onsets,
branch vowels, band-0/1/2 word rendering). Floors to re-run on the
stroke substrate: 11-letter pairwise distinctness (must not regress
vs v0.2's), band-2 fused-word distinctness on the seed lexicon.
Everything here is workshop-stage prototype; the real font (OpenType
contextual machinery, positional variants, optical balance) is the
eventual carrier — this prototype exists to test the *grammar*, not
to be the font.

## 4. First prototype findings (2026-08-15)

Rendered (.ship-notes/stroke-specimen.svg): the substrate delivers —
band 1/2 words are connected figures, visibly more organic than the
boxed compositions. Letter floors healthy after a stroke-weight fix
(worst pair c/m 0.167, all others >= 0.286 at 12px phase-min; the
initial W=4.6 let single strokes phase-vanish — W=5.4 guarantees
cell coverage). Two defects, with fix directions:

1. **Band-2 over-merge**: the shared-stroke rule dropped j's vertical
   spine in `wajone`, leaving a bare crossbar — merges must be
   identity-preserving (never drop a stroke that alone carries the
   letter's contrast; only merge truly coincident strokes).
2. **Vowel pairs are fusion's weak cell** (sala/sela 0.057 vs
   sala/sata 0.534, sala/weto 0.842): branch ticks are small ink.
   Fix direction worth exploring next: vowels modulate the JOIN
   TOPOLOGY (branch position shifts the inter-letter join point), so
   a vowel change reshapes the whole word figure instead of moving a
   tick — topology survives sizes that ticks do not.

Also cosmetic: arcs are 10-chord polygons (octagon look) — raise
chord count for display renders.

## 5. Vowels as join topology — BUILT AND MEASURED (2026-08-22)

§4.2's parked fix direction is now implemented and tested
(`tools/strokes_topology.py`, sheet in
`.ship-notes/workshop/vowel-topology-r1/`). The vowel's two features
map onto the JOIN into the next letter instead of onto a tick:
**height → the y-offset at which the next letter attaches**
(high −14u / mid 0 / low +14u), **backness → horizontal tuck**
(front pulls the next letter in 8u, back pushes it out 8u). Three
schemes measured against the tick control, phase-minimized occupancy
distance over 20 one-vowel-different and 90 one-onset-different
disyllable pairs:

| scheme | vowel min | vowel median | onset min | onset median | vowel/onset ratio |
|---|---|---|---|---|---|
| T0 ticks (control) | **0.0000** | 0.0357 | 0.0000 | 0.4857 | 0.074 |
| T1 join topology only | 0.0690 | 0.1579 | 0.1379 | 0.5161 | 0.306 |
| T2 topology + small tick | 0.0645 | **0.2000** | 0.1250 | 0.4848 | **0.412** |

(Medians in this table use the upper-middle-value convention and
pre-date the anchor correction — both fixed in §6; kept as the
record of what round 1 was judged on.)

Findings:

1. **The defect is worse than §4.2 reported and is now confirmed at
   zero.** Under ticks, some vowel-different word pairs render
   *identically* at this raster (min 0.0000, not 0.057) — the
   branch tick can phase-vanish entirely. Any claim that the stroke
   substrate distinguishes vowels at reading size was false.
2. **Topology fixes it.** T1 lifts the worst vowel pair off zero
   (0.069) and quadruples the median; T2 (topology plus a reduced
   7u tick) is best, **5.6x the control's vowel median** and a
   vowel/onset ratio of 0.41 against 0.07 — vowels stop being
   second-class ink.
3. **Onset distances are unharmed** (median 0.485 vs 0.486 control):
   the fix is free in the channel it doesn't touch. T1 even helps
   the onset minimum, because vowel-driven offsets de-align
   otherwise-similar figures.
4. **Confirmed by eye, not just by metric**: in the sheet's T0 row
   *sala/sela/sila/sola/sula* are one shape five times; in T1/T2 each
   vowel gives the word a distinct silhouette (the second letter
   rides high, level, or low, and tucks in or out).

Consequences to decide before adopting (all real, none blocking):

- **Word-final vowels have no following letter**, so they keep a
  terminal tick under every scheme — the system is inherently
  hybrid: medial vowels are topology, final vowels are ink. Not a
  defect (final position is the most robust anyway) but it must be
  taught as one rule, not two.
- **Vertical bounding box grows** (±14u of join offset), so line
  pitch pays a little; measure against the density claims before
  the layout gate.
- Interaction with the fusion bands is untested: band 2's
  shared-stroke merge assumes aligned junctions, which topology
  deliberately breaks. Band 2 may need per-vowel merge rules or may
  simply stop merging where the offset is large.

Recommendation (agent, shadow-logged): **T2**. It wins the metric,
keeps a visible vowel mark for large-size reading and for the
word-final case (so one rule covers both positions), and the tick's
cost is small ink at a position that already exists.

## 6. Continuous joins — the h05 reconciliation (2026-08-22)

Edward's round verdict rejected T1/T2 ("all over the place"; "a
worse version of T0, maybe just from alignment") while preferring
T0's continuity — but T0's vowel floor is 0.000. His "maybe just
from alignment" hypothesis is now built and measured
(`tools/strokes_continuous.py`, scheme **C**): the next letter still
rides high/level/low (height) and tucks/extends (backness), but the
junction is a DRAWN connector stroke from exit anchor to entry
anchor — ink never breaks, so the word stays one continuous figure;
there is no step-jump to misalign. Word-final vowels use the same
rule: the connector becomes a terminal tail (slope = height, length
= backness) with an end-hook 70° off the tail for front/back —
sized above the raster cell pitch because pure tail-length is
subset-ink and phase-vanishes (measured: the first C build hit
0.000 on final e/o exactly that way). One rule covers medial and
final position; the T-scheme's hybrid tick asymmetry disappears.

The build surfaced two measurement corrections that apply to the
whole lane (both from the 2026-08-22 Codex review): the t/s/h
letters' entry/exit anchors were never ON their ink (so all joined
schemes drew connectors from whitespace — fixed in strokes.py, with
an anchors-on-ink regression test), and published "medians" were
upper-middle values (even-n samples now use the conventional
mean-of-middle-two). Re-measured on the §5 pair families and
windows with both fixes:

| scheme | vowel min | vowel median | onset min | onset median | ratio |
|---|---|---|---|---|---|
| T0 | 0.0000 | 0.0351 | 0.0000 | 0.4815 | 0.073 |
| T1 | 0.0690 | 0.1289 | 0.1379 | 0.5156 | 0.250 |
| T2 | 0.0645 | 0.1469 | 0.1250 | 0.4838 | 0.304 |
| **C** | 0.0606 | **0.2269** | 0.0741 | **0.5385** | **0.421** |

C clears the vowel floor at T2's level, posts the best median and
vowel/onset ratio of any scheme, and keeps the one-continuous-
character quality Edward picked T0 for. One recorded fragility: at
the coarser cross-engine "extreme raster" (~6px onsets,
engine-bakeoff grids) C's word-final e/i pair still collapses —
the terminal-tail slope contrast is the scheme's thinnest ink.
Surfaced for verdict in the gz-engine-r1 bake-off (as engine E1);
adoption is Edward's call.
