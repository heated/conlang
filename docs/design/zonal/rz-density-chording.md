# RZ script density, spacing, and chording (workshop note)

Bead conlang-0y7. Questions (Edward, 2026-08-14): reduce characters
per word/sentence? is spacing necessary? how does chording work — any
channel rearrangement? Measured answers; comparison render in the
density specimen (tools/rz_script.py, sentence_glyphs).

## 1. Density levers (implemented ones marked ✓)

1. ✓ **Function-word logograms** — `le de que a no e …` are ~40–50%
   of running tokens; the top ~15 get quarter-width (42u) marks, the
   `&`-of-English move. Biggest single lever.
2. ✓ **Proportional block widths** — open CV blocks with simple
   onsets narrow to 80u.
3. ✓ **Headstroke + no spaces** (see §2).
4. **Inflectional logograms** (-va, -ria) — needs morphologically
   tagged input; deferred.
5. **Fusion** (one glyph per word, r5y) — halves unit count at
   crowding risk; harder for RZ than greenfield because clusters
   already spend satellite ink. Deferred to r5y's study.
6. **Scribal abbreviation layer** (medieval Latin compressed 30–40%
   with suspension/contraction marks) — precedent-rich but pure
   memorization; last resort, probably never.

Measured on the fable's opening clause (14 words):

| rendering | width | rel. |
|---|---|---|
| v0 plain blocks, spaced | 2512u | 100% |
| dense (1+2), spaced | 2022u | 80% |
| dense + headstroke, no spaces | 1788u | **71%** |

## 2. Spacing

Necessary in v0 — RZ has no self-segregating morphology, so word
boundaries need marking — but a space is the most *expensive*
boundary marker (~25u of blank line). The **headstroke replaces it at
near-zero cost**: words cohere under a shared top rule; the boundary
is the rule break; words abut with a 6u gap. (Design irony recorded:
the layout the greenfield review rejected as its default became RZ's
spacing solution.) Readability of rule-break segmentation at small
sizes goes on the same measurement docket as everything else.

## 3. Chording: no channel rearrangement

The chord banks, the block zones, and the phonology are the *same
factorization* — that identity is the design's core and it survives
RZ intact:

- left bank = onset sub-channels (s-key · base-consonant keys ·
  liquid key · **voicing key**) — voicing is a modifier in ink and a
  key under a finger, but the same sub-channel in both projections;
- thumb bank = nucleus (5 vowel keys; diphthong = two, order by
  thumb position);
- right bank = coda (l n r s + marginal).

The one re-uniting: **logograms get one stroke each** — `-mente` is
two spoken syllables but one written unit, so it chords as one
principled brief (suffix key + selector), and function-word marks
chord as single strokes (they are mostly monosyllables anyway).
Result: **stroke count = glyph-unit count = morphological unit
count** — what you type is what you see. `rapidemente` = 4 strokes =
4 glyph-units (ra·pi·de·MENTE). This also improves the wpm estimate
in rz-chording.md: logogram briefs cut strokes below the syllable
count for exactly the words that are longest.
