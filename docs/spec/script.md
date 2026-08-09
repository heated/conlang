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
giving 440 written codepoints as *semantic* states (each syllable in a
lexical role and in a payload role). Nothing about the check is spoken
in casual speech; careful/safety registers *may* realize it as vowel
length. The romanization renders channel 4 as per-syllable vowel
doubling in both roles. The native script splits it: the lexical check
renders as the check-slot dot (§6), while payload role is carried by
span membership (the run-rule, §6–§7) plus the computable check — so
the 440 semantic states map to 220 block shapes × {dot, no dot} with
the payload distinction at run level, not 440 distinct block forms.
A doubled vowel in romanized text is ink, not sound.

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
   construction. For a *listener* that means mishearings land on
   visually distant glyphs; for a silent *reader*, phonetic distance
   is no protection at all, so the same-base pairs are the eye's
   residual weak set — they are listed exhaustively in
   `script_confusion_pairs` and priced by `lexgen`'s
   `strict_with_script` policy (cost at current inventory: one root
   body, 18→17 strict), so the lexicon avoids minting unrelated
   minimal pairs on them. Both the distance-2 invariant and the
   same-base⊆listed invariant are machine-checked by `spec_check.py`.
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

- Onsets: 4 content bases × 4 modifiers − 2 banned cells = **14
  content cells** (10 used), plus the fixed h cell; the remaining tick
  cells are reserved to the particle class by policy (the solver
  searches content bases only). The grid is *headroom, not inventory*:
  the renderer implements and visually verifies exactly the cells in
  use and **rejects** the rest (`SUPPORTED_RECIPES`) rather than
  improvising. The wide model (SPEC §9) needs ~20 onsets; that
  requires either unreserving tick cells or new modifiers (any
  addition must pass the robustness bar of §1.3) — a deliberate
  policy change, not free space.
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
  (every phonetic confusion pair differs in base and modifier); the
  **same-base⊆`script_confusion_pairs` invariant** (the eye's weak set
  stays priced); frozen banned cells; injectivity.
- `test_script.py`: determinism; per-zone and whole-block
  distinctness; strip/zone ink bounds; check⇔doubling agreement;
  payload run-rule clearance; CLI (including payload validity); the
  **four-way consistency test** (solver ≡ spec data ≡ frozen tables ≡
  renderer recipes); and the **raster regression floor** — 14×14
  occupancy-grid distances minimized over sub-cell sampling phases,
  with the ink window guarded (all onset pairs ≥ 0.15 against a
  measured phase-min of 0.195; phonetic pairs ≥ 0.55 against 0.623;
  coda marks ≥ 0.50 against 0.600). A geometry change that erodes a
  distinction fails the floor before it reaches a reader. The IoU
  floor is a regression ratchet, not legibility evidence — the
  freeze-gate evaluation should re-measure with multi-resolution and
  blur-based distances (noted on the freeze bead).

Remaining known work: the style/beauty pass (freeze-gate material with
the layout decision); fused disyllabic blocks study (conlang-r5y);
payload-rule typography across multi-word frames (with conlang-6sa/
modes when mode text rendering exists).
