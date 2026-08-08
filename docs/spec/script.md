# Featural Block Script — v0.1 (spec v0.2.0-draft)

Status: **draft, not frozen.** The feature→shape mapping is normative data
in `channels.json` (`script_features`); this document is its prose
companion. Exact stroke metrics live in the reference implementation
(`tools/script.py`) and are illustrative: a conforming font may restyle
proportions freely as long as the feature grammar below stays legible
and compositional.

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
   sits at a fixed position readable at skim distance.

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

Every pair of onsets differs in base, modifier, or both; phonetically
close pairs (differing by one articulatory feature) differ by exactly
one visual feature — the confusion structure of the ear is mirrored, not
hidden, so readers learn the map, and mishearings stay recoverable from
the glyph.

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

- Onsets: 5 places × 6 manners = **30 expressible onset letters** (11
  used). The wide model (SPEC §9) needs ~20; it fits without new visual
  features. Voicing, if ever adopted, is one more modifier (inner dot).
- Vowels: 9 grid positions + rounding modifier (5 used).
- Codas: any onset letter can miniaturize (3 + ∅ used).

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
and all 20 particle syllables — the full 220 — plus sample words and a
payload example.
`tools/test_script.py` asserts determinism, all-blocks distinctness, and
lexical/payload marking; `tools/spec_check.py` validates the feature
data (completeness and injectivity).
