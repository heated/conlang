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
