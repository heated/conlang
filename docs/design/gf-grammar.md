# Greenfield grammar v0 (workshop draft — conlang-jbw)

The channel language's first grammar: enough to write real sentences,
gloss them, and measure efficiency against RZ and English. Workshop-
stage; freeze-gate material only after revision. Decisions are made
decisively below and flagged where tentative.

## 1. Typological frame

Analytic SVO, head-initial, modifiers postposed, **no grammatical
number, no gender, no agreement, no case**. Plurality via quantifiers
when it matters (Chinese-proven). All grammar lives in: word order,
the POS coda, and 11 particles.

## 2. POS-alternation semantics (the review's demand: uniform per
declared class)

Every root is typed at assignment with one of four **alternation
classes**; the ∅/n/s coda mapping is uniform GIVEN the class:

| class | noun (∅) | verb (-n) | modifier (-s) |
|---|---|---|---|
| O (object) | the object | use/apply it to the theme | of-it / made-of-it |
| A (action) | the act/event | do the act | characterized by doing it |
| P (property) | the quality | be/become it (copular) | plain adjective |
| R (relation) | the relation | stand in it to the object | relational adj |

`stone/to stone/stony` is *not* uniform in English because English
mixes classes covertly; here the class is declared in the lexicon
entry (one bit of learning per root, four rules total). Property-verbs
absorb the copula for predication (`sky blue-VERB` = the sky is
blue); an equative root (class R, "same/identity") covers noun-noun
predication.

## 3. Particles (11 of 12 free slots; 1 held in reserve)

All particles: single unstressed h-syllable, [h]~[ʔ] onset, no POS
coda (particles are their own class). Modes own hu ho hi he heen hin
haas hoos. Assignment principle: **robustness before brevity for
semantically dangerous items** (negation gets the long nasal form,
not the short one), frequency gets the rest.

| form | function | notes |
|---|---|---|
| `ha` | and (NP and clause) | highest frequency, shortest form |
| `haan` | negation (preverbal) | deliberately long+nasal: a misheard negation inverts meaning, so it gets the most robust form |
| `hal` | to / for (dative-allative) | |
| `hees` | of / from (genitive-ablative) | |
| `hel` | that / which (complementizer + relativizer, RZ-que-style universal) | |
| `his` | with / by (instrumental-comitative) | |
| `hol` | at / in / on (general locative) | |
| `hoon` | past (preverbal TAM) | unmarked = nonpast |
| `hun` | or | |
| `hus` | yes/no question (clause-final, Chinese-ma-style) | |
| `huul` | irrealis / future / would (preverbal TAM) | |
| `hiil` | — RESERVED (drift/expansion) | |

Overflow policy: further closed-class items (but, while, if…) are
**stressed content words**, not particles — the particle class is the
unstressed scaffold and is capacity-capped by design. `but` = adverb
root; `if` = `hel` + irrealis in the protasis (flagged tentative).

## 4. Syntax

- **Clause**: S (TAM) V O (obliques). Obliques = particle + NP, after
  the object.
- **NP**: N + modifiers (postposed -s words) + relative clause
  (`hel` + clause, postposed). Quantifiers/numerals precede the noun.
- **Questions**: yes/no = clause + `hus`. Content questions: QW
  in-situ (no movement). QW root: `cu` (what/which; correlative grid
  expands from it — jbw next phase).
- **Imperative**: bare verb clause, subject omitted.
- **Predication**: property/relation verbs (class P/R) carry the
  copula; no separate "be" for adjectives.
- **Comparative**: `mu-s` (more, from `mu` many) before the modifier;
  standard marked with `hees` (than = from). Superlative: `to mu-s`
  (all-more). Flagged tentative.
- **Subordination**: `hel` clauses as complements (after verb) and
  relatives (after noun); adverbial clauses via particle + `hel`
  (e.g. `hol hel` "at-that" = when — flagged, may deserve own word).
- **Serialization**: V V sequences allowed with shared subject
  (aspect/direction verbs: begin, finish, go-do); the second verb
  keeps its -n coda. Tentative.

## 5. Prosody recap (from SPEC)

Content words: 1–3 syllables, initial stress. Particles: unstressed.
SSM gives the parse; the grammar above never needs punctuation-like
particles beyond `hus` (Lojban's terminator clutter avoided by
configurationality + the POS channel).

## 6. What v0 deliberately omits

Aspect morphology (serialization + adverbs carry it), evidentials
(Tier 3), honorifics (none, ever), articles/definiteness (context),
voice (word order + relation roots; passive candidate: patient-
fronting with `hees` agent — flagged for v1), correlative grid
completion, discourse particles.
