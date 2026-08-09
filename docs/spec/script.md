# Featural Block Script — v0.1 (spec v0.2.0-draft)

Status: **draft, not frozen.** The feature→shape mapping is normative data
in `channels.json` (`script_features`); this document is its prose
companion. Exact stroke metrics live in the reference implementation
(`tools/script.py`) and are illustrative: a conforming font may restyle
proportions freely as long as the feature grammar below stays legible
and compositional.

**Tentative direction (Edward, 2026-08-09), not yet applied:** replace
mouth-shape iconicity with **anti-iconic assignment** — ear-confusable
phonemes get maximally distinct marks, so the eye serves as independent
redundancy — with letterforms optimized for degradation rather than
articulatory storytelling; and grow the character space toward fused
disyllabic blocks (~50k codepoints per character, ~7 components, at the
visual-crowding ceiling), possibly with dedicated number characters.
v0.1 below is the current, implemented mapping; the reassignment study
is v0.2 work and keeps the compositional feature grammar — what changes
is *which* phoneme gets *which* visual feature bundle, chosen against
the measured confusion matrices of ear and eye jointly.

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
   the ~14 visual features yields all 440 written syllables. (Hangul
   precedent, taken further: no shape irregularities at all.)
2. **Block = syllable = channel vector.** One block has four zones —
   onset, vowel, coda, check — mirroring the three segmental channels
   plus the written-layer check (SPEC §2.4, §4.1). The block diagram
   doubles as the chord diagram for input (§7).
3. **Silhouette carries grammar.** Word height = syllable count;
   particle blocks are visibly smaller; the coda zone (= POS, SPEC §6)
   occupies a reserved strip in every block. Under the current
   top-aligned stacking the *final* coda — the POS — sits at the word's
   bottom edge, whose height varies with syllable count: word-entry
   height is fixed, POS position is not. (Bottom-aligning would invert
   that trade; the alignment choice is deliberate v0.2/freeze-gate
   material. Fixed word-entry height and fixed POS baseline are
   mutually exclusive under stacking.)

## 2. Block geometry

A block is a square cell with four zones:

```
+----------------+------+
|                | chk  |   chk : check slot (top-right)
|   ONSET        +------+
|   (top-left)   |  V   |   V   : vowel carrier (right)
|                |  |   |
+----------------+--+---+
|   CODA (bottom strip)  |
+------------------------+
```

- **Onset zone** (top-left): the onset letter, built from §3.
- **Vowel carrier** (right): a vertical bar with a position-coded tick, §4.
- **Coda strip** (bottom): a miniature onset form, or empty for ∅, §5.
- **Check slot** (top-right corner): dot/ring/empty, §6.

Zone positions are fixed; their exact proportions are font-level choices.

## 3. Onset letters: place × manner

An onset letter = **base element** (place of articulation) + **modifier**
(manner). Normative mapping (`script_features.visual_grammar`):

| place | base element |
|---|---|
| labial | circle |
| coronal | vertical stroke |
| palatal | diagonal stroke (rising) |
| velar | top-left angle (⌐ corner) |
| glottal | short horizontal tick |

| manner | modifier |
|---|---|
| stop | plain base |
| nasal | floating bar above |
| fricative | doubled element |
| affricate | mid crossbar |
| approximant | broken stroke (gap in the base) |
| lateral | bottom foot hook |

The 11 onsets (`script_features.onset_features`):

| onset | features | glyph recipe |
|---|---|---|
| p | labial stop | circle |
| m | labial nasal | circle + bar above |
| w | labial approximant | circle broken at top (arc) |
| t | coronal stop | vertical stroke |
| n | coronal nasal | vertical + bar above |
| s | coronal fricative | doubled vertical |
| l | coronal lateral | vertical + foot hook |
| c | palatal affricate | diagonal + mid crossbar |
| j | palatal approximant | broken diagonal |
| k | velar stop | angle |
| h | glottal fricative | doubled tick (=) |

Every pair of onsets differs in base, modifier, or both. The
ear-mirroring is partial, and the asymmetry is favorable: *place*
confusion pairs (p/t, t/k, m/n, n/l) differ by exactly one visual
feature, but three of the ear's worst cross-manner pairs — s/c, l/j,
l/w — differ in base *and* modifier, i.e. they are visually far apart
exactly where the ear is weakest. Conversely the v0.1 ink has visual
collapses at small sizes that the ear never makes (s→t, c↔j, w→p —
measured at 16–24 px); these are recorded as normative data in
`channels.json` (`script_confusion_pairs`) and priced by `lexgen`'s
`strict_with_script` policy so the lexicon is not blind to the eye's
confusion matrix. At current inventory size that protection costs zero
root bodies. The v0.2 ink pass aims to shrink the visual-collapse set
to a subset of the phonetic one (and the tentative anti-iconic
directive, header above, may replace the mapping wholesale).

`h` (particle-only, SPEC §5) is the lightest letter in the script —
appropriate for the unstressed grammatical scaffold, and its doubled-tick
form is unmistakable at skim distance.

## 4. Vowel carrier: height × backness

The carrier is a vertical bar spanning the block's right side. One tick
crosses it; the tick's **vertical position** codes height, its
**direction** codes backness (`script_features.vowel_features`):

| vowel | height | backness | tick |
|---|---|---|---|
| i | high | front | high, leftward |
| u | high | back | high, rightward |
| e | mid | front | mid, leftward |
| o | mid | back | mid, rightward |
| a | low | central | low, both sides |

Headroom: the 3×3 height–backness grid yields 9 positions; a rounding
modifier (second tick) is reserved for the wide model.

## 5. Coda strip: miniature onsets

The coda (n, s, l) renders as a **miniature of the corresponding onset
letter** in the bottom strip — the same letter shrunk, so the coda
channel costs zero new letters to learn. ∅ leaves the strip empty.
Because final coda = POS (SPEC §6), the strip is the POS marker:

- empty strip → noun
- mini n (vertical + bar) → verb
- mini s (doubled vertical) → modifier
- mini l → reserved

## 6. Check slot

The written-layer check (SPEC §2.4, §4.1) renders in the top-right slot:

- **filled dot** — lexical syllable, check bit 1
- **ring** — mode-payload syllable, polarity 1
- **empty** — bit 0 (either layer)

This is the glyph-level equivalent of romanization vowel doubling: dot ⇔
doubled vowel. It is computed, never distinctive, and a font may render
it faintly; casual handwriting may drop it (it is recoverable), matching
the check's demoted, written-layer status. Dot vs ring keeps lexical and
payload marking visually disjoint, mirroring the romanization rule that
doubling means different bits in the two parses.

Honest scoping of the detectability claims (SPEC §4.1–4.2): they hold
**for machines and at print sizes**. Dot-vs-ring is a fill contrast and
is not reliably distinguishable below ~24 px; and since only bit-1
states are marked, a payload syllable with anti-check 0 shows an empty
slot identical to a check-0 lexical syllable — per-syllable layer
identification by a human reader requires computing the check. Payload
*runs* are delimited by mode particles (SPEC modes.md), which is where
frame integrity actually lives; a run-level payload marking (continuous
rule alongside the span) is a v0.2 candidate.

## 7. Word assembly

- **Content words: vertical stacking.** Syllable blocks stack top-to-
  bottom into one tall glyph; initial (stressed) syllable on top. Word
  height = 1–3 blocks. Words sit side by side along the line with clear
  inter-word gaps (SPEC §5: spacing is structural).
- **Particles: single block at ~70% scale**, vertically centered. A
  particle is short and light; content words are tall. Sentence
  structure is visible in silhouette before any letter is read.
- The **top block** of a content word carries stress implicitly (initial
  stress, SPEC §5); no stress mark is needed.

**Documented alternative (not adopted): horizontal shared headstroke.**
Devanagari-style — syllables run left-to-right under a shared top rule,
words cohere by connection, line height stays constant. Preserves the
featural grammar unchanged; trades the height-silhouette channel for
conventional line metrics. The renderer's geometry is parameterized so
this is a layout change, not a redesign. Revisit at freeze if vertical
stacking proves awkward for long-form text.

## 8. Chord compatibility

The block is the chord diagram: onset zone ↔ onset keys, carrier ↔
vowel keys, strip ↔ coda keys. A chorded input stroke selects one value
per zone and emits the block (or its romanization). Key layouts belong
to the input-methods track (bead conlang-6sa); the script commits only
to the zone↔axis correspondence.

## 9. Headroom and the wide model

- Onsets: 5 places × 6 manners = **30 grid cells** (11 implemented).
  The grid is *headroom, not inventory*: the renderer implements and
  visually verifies exactly the 11 recipes in use and **rejects** the
  other 19 cells rather than improvising them (`SUPPORTED_RECIPES` in
  `tools/script.py`). The wide model (SPEC §9) needs ~20 onsets; the
  feature grammar accommodates that without new visual features, but
  each new cell is a designed-and-verified recipe, not a free lunch.
  Voicing, if ever adopted, is one more modifier (inner dot).
- Vowels: 9 grid positions + rounding modifier (5 used).
- Codas: any implemented onset letter can miniaturize (3 + ∅ used).

The same feature grammar is the substrate for the zonal auxlang's wide
chorded script (as an input method / optional display layer, per the
pricing note in `docs/design/alternatives/zonal-script-pricing.md` —
Latin stays primary there).

## 10. Reference implementation

`tools/script.py` (stdlib-only SVG):

```
python3 tools/script.py word sala salaan salaas   # stacked word glyphs
python3 tools/script.py particle hu               # particle block
python3 tools/script.py payload mi                # payload marking (ring)
python3 tools/script.py specimen --out specimen.svg
```

The specimen sheet renders all 200 content syllables (including
phonotactically banned glide cells — visual completeness is deliberate)
and all 20 particle syllables — the full 220 — plus sample words, both
payload cases (ring and honest empty slot), and a running pseudo-lexicon
sentence in the stacking layout. `tools/test_script.py` asserts
determinism, per-zone and whole-block distinctness (independent of the
derived check mark), coda-strip ink bounds, check/romanization
agreement via parsed XML, CLI behavior, and rejection of unimplemented
grid cells; `tools/spec_check.py` freezes the feature tables and visual
grammar and validates `script_confusion_pairs`.

Known v0.2 ink work (from the 2026-08-09 reviews, kept as an honest
defect list): modifier rescale (floating bars, breaks, and the dot are
below the small-size legibility floor — the feature classes typographic
history erodes first), strip-native coda marks (full-width, legible at
16 px), payload run-marking, raster-distance regression tests, the
stacking-vs-headstroke layout decision with a paragraph specimen in
both, and a gestalt-diversity/style pass. The anti-iconic reassignment
study (header) may subsume the modifier rescale.
