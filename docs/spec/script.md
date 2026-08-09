# Featural Block Script — v0.2 (spec v0.2.0-draft)

Status: **draft, not frozen.** The feature→shape mapping is normative data
in `channels.json` (`script_features`); this document is its prose
companion. Exact stroke metrics live in the reference implementation
(`tools/script.py`) and are illustrative: a conforming font may restyle
proportions freely as long as the feature grammar below stays legible
and compositional, and the raster-distance floor (§10) still passes.

v0.2 replaces v0.1's articulatory-iconic mapping with a
**confusion-aware anti-iconic code** (decision record:
`docs/design/script-v02-assignment.md`; directive: Edward 2026-08-09,
resolution delegated). Still tentative for later iterations: growing
the character space toward fused disyllabic blocks (~50k codepoints per
character, ~7 components, at the visual-crowding ceiling), possibly
with dedicated number characters (bead conlang-r5y).

## 0. Layers: what is spoken vs. what is written

Casual speech carries **three** channels per syllable: onset, vowel,
coda — 220 spoken segmental syllables. The written layer carries
**four**: those three plus the computed check bit (SPEC §2.4, §4.1),
giving 440 written codepoints (each syllable × two check-slot states:
its lexical form and its payload form). Nothing about the check is
spoken in casual speech; careful/safety registers *may* realize it as
vowel length. The romanization renders channel 4 as vowel doubling;
the native script renders it as the check slot (§6). Same bit, two
costumes — a doubled vowel in romanized text is ink, not sound.

## 1. Design goals

1. **Featural, zero exceptions.** Every glyph is computed from the
   syllable's channel values. Nothing is memorized per-glyph; learning
   5 bases + 4 modifiers + the assignment table yields all 440 written
   syllables. (Hangul's compositional insight, minus its
   irregularities.)
2. **The eye is independent redundancy, not a mirror of the ear.**
   Every phonetic confusion pair (covered ∪ forbidden ∪ weighted,
   SPEC §4.3) sits at **visual distance 2** — different base AND
   different modifier — so no single degraded visual feature class can
   merge an ear-confusable pair. Conversely, the visually closest
   pairs (same base, different modifier) are phonetically distant by
   construction: a misreading yields a phonetically implausible word,
   a mishearing yields a visually distant glyph. Each channel covers
   the other's weak pairs. Machine-checked by `spec_check.py`.
3. **Letterforms optimized for degradation.** The letter grammar uses
   only robust contrast classes: full-length strokes, wide-offset
   doubling, attached caps and crossings. No floating bars, small
   breaks, dots, or fill contrasts (the feature classes typographic
   history erodes first — Hangul's 1446 vowel dots became strokes).
4. **Block = syllable = channel vector.** One block, four zones —
   onset, vowel, coda, check — mirroring the three segmental channels
   plus the written-layer check. The block diagram doubles as the
   chord diagram for input (§8).
5. **Silhouette carries grammar.** Word height = syllable count;
   particle blocks are visibly smaller; the coda strip (= POS, SPEC §6)
   gets the loudest ink in the block (§5). Under top-aligned stacking,
   word-entry height is fixed and the POS strip sits at the word's
   variable bottom edge; the alignment choice is deliberate freeze-gate
   material (fixed word-entry height and fixed POS baseline are
   mutually exclusive under stacking).

## 2. Block geometry

A block is a square cell with four zones:

```
+----------------+------+
|                | chk  |   chk : check slot (top-right)
|   ONSET        +------+
|   (top-left)   |  V   |   V   : vowel carrier (right)
|                |  |   |
+----------------+--+---+
|   CODA (full-width strip)|
+--------------------------+
```

Zone positions are fixed; their exact proportions are font-level
choices.

## 3. Onset letters: base × modifier, anti-iconic assignment

An onset letter = **base** + **modifier** — a cell in a 5×4 grid.
The assignment of phonemes to cells is normative data solved as an
error-correcting code (`tools/assign_glyphs.py`; decision record in
`docs/design/script-v02-assignment.md`):

| base | realization |
|---|---|
| circle | closed ring |
| vertical | full-height vertical stroke |
| diagonal | full rising diagonal stroke |
| angle | top-left corner (top arm + left arm) |
| tick | short horizontal tick (particle h only) |

| modifier | realization |
|---|---|
| plain | base alone |
| crossed | full attached stroke crossing the base through its center |
| doubled | wide-offset parallel copy |
| capped | full attached horizontal stroke at the top |

Banned cells (no robust realization): circle+doubled, angle+capped.

The 11 onsets:

| onset | cell | glyph sketch | digit tens |
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

**Digit mnemonic (emergent, worth teaching):** base = tens-digit
mod 4 — circle 0/4/8, vertical 1/5/9, diagonal 2/6, angle 3/7. Mode
payloads have no lexical safety net, so this rule-governed structure is
where the assignment's discrimination guarantees matter most.

`h` remains the lightest letter in the script — appropriate for the
unstressed grammatical scaffold, unmistakable at skim distance.

## 4. Vowel carrier: height × backness

Unchanged from v0.1 (the design review's verdict: the vowel system is
the strongest part of the script). The carrier is a vertical bar at the
block's right; one tick crosses it — vertical position codes height,
direction codes backness:

| vowel | height | backness | tick |
|---|---|---|---|
| i | high | front | high, leftward |
| u | high | back | high, rightward |
| e | mid | front | mid, leftward |
| o | mid | back | mid, rightward |
| a | low | central | low, both sides |

The direction-confusable glyph pairs (e/o, i/u) land on phonetically
weighted pairs, so vowel visual confusion is already lexicon-protected.
Headroom: 3×3 grid + a rounding modifier reserved for the wide model.

## 5. Coda strip: POS gets the loudest ink

The coda (= POS, SPEC §6) renders as a **full-width strip-native
mark** — the most legible ink in the block, because the POS channel is
simultaneously check-invisible (∅/n flips) and lenition-prone in
speech, so the eye is its main defense:

- empty strip → ∅, noun
- single full-width bar → n, verb
- double full-width bar → s, modifier
- hooked bar → l, reserved

(v0.1's miniature-onset codas were replaced: at 0.42 scale their
distinctions fell below the legibility floor, and "same letter shrunk"
stopped being true in the actual ink. The strip marks are three
shapes learned once, legible at 16 px, measured n/s at raster distance
1.0.)

## 6. Check slot

The written-layer check (SPEC §2.4, §4.1) renders in the top-right
slot as a **filled dot when the lexical check bit is 1**, empty
otherwise — the glyph-level equivalent of romanization vowel doubling
(dot ⇔ doubled vowel). It is computed, never distinctive; a font may
render it faintly and casual handwriting may drop it.

**Payload marking is a run-level feature, not a per-block one:** a
payload span carries a continuous light rule beside the glyph stack
(§7), and its blocks carry no slot mark. Rationale: per-syllable
dot-vs-ring was a fill contrast (illegible below ~24 px), and payload
syllables with polarity 0 carried no mark anyway — frame integrity
lives at the span level (mode particles + checksum, modes.md), so the
ink now says so. Machines separate layers by computing the check;
romanization doubling remains per-syllable in both layers as before.

## 7. Word assembly

- **Content words: vertical stacking** (v0.2 default). Syllable blocks
  stack top-to-bottom; initial (stressed) syllable on top. Word height
  = 1–3 blocks; words sit side by side with clear gaps; sentence
  structure is visible as a height rhythm before any letter is read.
- **Particles: single block at ~70% scale**, no headstroke.
- **Payload spans: a continuous run-rule** along the stack's left edge
  (§6).
- **Documented alternative: horizontal shared headstroke** —
  implemented in the renderer (`word_glyph_horizontal`) for the
  freeze-gate comparison: blocks run left-to-right under a shared top
  rule, words cohere by connection, line height is constant, page area
  is ~1.5–2× denser for disyllable-dominant text. The specimen renders
  the same sentence in both layouts. The layout decision is deferred
  to the freeze gate with this evidence in front of the human.

## 8. Chord compatibility

The block is the chord diagram: onset zone ↔ onset keys, carrier ↔
vowel keys, strip ↔ coda keys. A chorded input stroke selects one value
per zone and emits the block (or its romanization). Key layouts belong
to the input-methods track (bead conlang-6sa); the script commits only
to the zone↔axis correspondence. (The four-projections architecture —
glyph / romanization / chords / skeleton input — is recorded in the
design brief, 2026-08-09.)

## 9. Headroom and the wide model

- Onsets: 5 bases × 4 modifiers − 2 banned cells = **18 cells**
  (11 used). The grid is *headroom, not inventory*: the renderer
  implements and visually verifies exactly the cells in use and
  **rejects** the rest (`SUPPORTED_RECIPES`) rather than improvising.
  The wide model (SPEC §9) needs ~20 onsets; further modifiers (e.g.
  an inner-dot voicing mark was the v0.1 idea — any addition must pass
  the robustness bar of §1.3) extend the grid when needed.
- Vowels: 9 grid positions + rounding modifier (5 used).
- Codas: strip marks generalize by stroke count/shape (3 + ∅ used).

## 10. Reference implementation and verification

`tools/script.py` (stdlib-only SVG):

```
python3 tools/script.py word sala salaan salaas   # stacked word glyphs
python3 tools/script.py particle hu               # particle block
python3 tools/script.py payload mama              # run-rule marking
python3 tools/script.py specimen --out specimen.svg
```

The specimen renders all 220 syllables, sample words, a payload
example, and the same running sentence in both layouts. Verification
is layered:

- `spec_check.py`: frozen feature tables; **the distance-2 invariant**
  (every phonetic confusion pair differs in base and modifier);
  banned-cell avoidance; injectivity.
- `test_script.py`: determinism; per-zone and whole-block
  distinctness; strip/zone ink bounds; check⇔doubling agreement;
  payload run-rule; CLI; and the **raster regression floor** — 14×14
  occupancy-grid distances (all onset pairs ≥ 0.20, phonetic pairs
  ≥ 0.60, coda marks ≥ 0.55), which is what keeps
  `script_confusion_pairs` empty. A geometry change that erodes a
  distinction fails the floor before it reaches a reader.

Remaining known work: the style/beauty pass (freeze-gate material with
the layout decision); fused disyllabic blocks study (conlang-r5y);
payload-rule typography across multi-word frames (with conlang-6sa/
modes when mode text rendering exists).
