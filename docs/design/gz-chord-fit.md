# GZ ⇄ chord-space co-design (exploration, 2026-08-22, conlang-i78)

RZ *happened* to fit the per-hand directional-cluster space uncut
(rz-chording §4e/§4g). GZ is greenfield — it doesn't have to hope
for a fit; its phonotactics can be **defined as the chord
dimensions**, making chord entry an isomorphism instead of an
encoding. Computed in `tools/gz_chord_fit.py`.

## 1. The exact-fit inventory

Define GZ syllables = the per-hand banks:

| channel | inventory | chord bank |
|---|---|---|
| onset | ≤35 + null (simple + clusters, one table) | index×middle = 36 |
| nucleus | 5 vowels + ai au oi = 8 | thumb (9th state = command region) |
| glide | ∅ / i- / u- = 3 | ring: 3 glide states (the ring's other ×2 is the cross-word **boundary flag** — a non-lexical chord state, so it multiplies the CHORD space to 6 but not the syllable space) |
| coda | ∅ n s r l m = 6 | pinky |

Raw **phonological** space: 36 × 8 × 3 × 6 = **5,184 syllable cells** (the boundary flag is excluded — it distinguishes strokes, not words). The chord space proper is twice that at 11,664 states/hand, per rz-chording §4e.

## 2. The slack funds the humility screen [M]

The GZ sketch targets 2,000–3,000 usable syllables. Against 5,184
raw cells that implies a survival rate of **39–58%** — and the
width-ladder work *measured* the humility screen passing ~40% of
raw space. 5,184 × 0.40 = **2,073 survivors: inside the target
band.** Reading: the chord space is not a constraint on GZ at all;
its 2.5x slack over the target is exactly the rejection budget the
humility screen needs. The three numbers (chord capacity, humility
survival, GZ syllable target) were derived independently and they
close — the design is over-determined in the good way.

## 3. The motor-confusion channel (new design rule)

Because GZ chooses *which* cells survive, the humility screen can
audit **two confusion graphs jointly**: the acoustic graph (the
existing screen) and the **motor graph** — chords one directional
slip apart (a finger one ring-step off, an over-push to press, a
missed press to null). RZ can't do this (inherited word shapes);
GF audits acoustics only. GZ is the first system where "easily
mis-struck" can be a reason two meanings never sit on adjacent
cells.

**Demonstrated on the digit bank** (the highest-stakes confusions):
the audit demands numerically close digits (circular distance ≤2)
be motor-DISTANT — the chord-layer analog of digitgen's principle
(confusable → far apart in value). Results:

- naive row-major layout: min close-pair motor distance 1,
  **10 violations**;
- hill-climbed assignment: min distance 2, **0 violations**, mean
  close-pair distance 2.80 (of max 4).

So the constraint is comfortably satisfiable. Since the other ~25
onsets don't constrain digit-pair distances, the digit onsets'
cells can be fixed first and the rest of the onset layout filled
by frequency→ergonomics + the speech-side joint audit. The full
joint optimization (all onsets, acoustic × motor × frequency)
belongs to the input prototype bead (conlang-6sa).

## 4. Escape regions align across layers

In RZ the escape regions rhyme (h-row in speech, nucleus-less in
chords); in GZ they can **coincide by construction**: the h-onset
cell of the onset table ↔ mode frames in speech ↔ the same cell in
every chord; thumb-null ↔ the command layer. One reserved-region
decision, made once, surfaces identically in phonology, script,
and input. The design rule ("every layer keeps a structurally
unreachable escape region") upgrades to: **in a greenfield, make
it the same region.**

## 5. What this prices on the E/R/M dial

At 2 syllables/stroke, strokes/word = syllables/word ÷ 2 — so any
scheme that adds syllables taxes typing directly. E-scheme endings
add a syllable only to consonant-final remaps (most Romance stock
is already vowel-final; 63% of tokens are already E-shaped), so
the tax is small but real — and now measured on the corpus [M]:
POS-free lower bound (consonant-final content tokens gain a vowel
under any deterministic final-vowel scheme; verb infinitives
excluded — Ido-style -ar/-er/-ir already IS the verb mark):
**+4.4% spoken length / strokes** (1.85 → 1.93 syl/word), driven
by the -cion/-sion action-noun family and -al/-or/-on nouns.
R-scheme (script-only POS) is typing-free. A new column for the
E/R/M bake-off (conlang-z0s).

## Status

Exploration artifact — numbers [M] where computed (space
arithmetic, motor audit), [D]/[H] where modeled (survival transfer
from width-ladder, E-scheme tax). Feeds conlang-z0s (GZ scheme
pick) and conlang-6sa (layout optimization). Ledger row in
learning-budget.md.
