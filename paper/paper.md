---
title: "A Channel-Coded Constructed Language Optimized for Learning Speed"
author: "Edward Swernofsky (with Claude)"
date: 2026-08-08
status: living draft — grows with the build; sections marked [TODO] are stubs
bibliography: references.bib
---

## Abstract

[Draft.] We present the design of a constructed language that treats the
syllable as a vector of independent channels (onset, vowel, coda, register)
and applies coding-theoretic error correction over that space. The design
goal is minimal time-to-fluency for second-language learners, with fast
chorded text input and rapidly-acquired reading falling out of the same
channel architecture rather than being separate systems. We describe (1) a
baseline phonology chosen so that no learner is asked to perceive a contrast
absent from their native language; (2) an error-correcting lexicon built with
perceptually weighted distance rather than uniform Hamming spacing; (3) a
decoupled featural block script in which glyph, chord, and pronunciation are
three renderings of the same channel vector; (4) self-segregating morphology
implemented prosodically; and (5) closed-domain "mode" subsystems that encode
numbers, dates, times, and foreign material at near-information-theoretic
density inside an otherwise redundant language. We argue from the
cross-linguistic literature that such a design can compress learning time
substantially while leaving speaking and reading throughput unchanged, and we
outline an evaluation program.

## 1. Introduction and design goal

[TODO: expand.] The single optimization target is **learning speed** —
time from zero to functional use, for adult second-language learners of any
first language. Explicit non-goals, argued in §2: raw speech and reading
throughput (empirically pinned near ~39 bits/s by cognition, not by the
code [@coupe2019]), and spoken density (the "wide phonology" branch is
rejected in §3.4).

Contributions:

1. A syllable-as-channel-vector phonology with an explicit codespace budget.
2. An error-correction stack for human speech: inner parity, perceptually
   weighted spacing, cross-syllable checks, phonotactic templates, and
   conversational repair as the outermost free layer.
3. A featural block script deterministically coupled to the phonology, with
   chorded (desktop) and touch (phone) input methods derived mechanically
   from the same spec.
4. Mode subsystems: closed semantic grids (numbers, dates, times,
   coordinates, spell-out) encoded in the complement of the lexicon's
   codespace, self-flagging as non-lexical.
5. A governance model: small frozen core, versioned spec, open periphery.

## 2. Why not faster speech or reading: the throughput ceiling

A language designed for *speed* would be optimizing the wrong variable.
Across 17 typologically diverse languages, information rate in speech
converges near ~39 bits/s: languages with information-dense syllables are
spoken proportionally slower, and sparse ones faster, so the product stays
flat [@coupe2019]. The ceiling appears to be cognitive rather than
articulatory — inner speech, silent reading, and deliberate sequential
thought cluster in the same band. Reading tells the same story from the
other side: comprehension of normal prose degrades in proportion to speed
past roughly 400–500 WPM, RSVP presentation demonstrates that eye
movements were never the bottleneck, and subvocalization is load-bearing
for the working-memory rehearsal that comprehension depends on — not a
removable inefficiency [@rayner2016]. Nor does script density pass
through to throughput: denser scripts induce proportionally shorter
saccades, holding information-per-fixation roughly constant. [TODO-verify:
saccade-scaling citation for Chinese/English reading rates.]

What is *not* pinned: time-to-fluency (transparent orthographies reach
accurate decoding in roughly a year of schooling versus two to three times
that for English [@seymour2003]); text input speed (chorded systems
demonstrate 200+ WPM, gated by learning cost, not motor limits); working
memory economy (span is measured in articulatory time, so shorter
high-frequency words buy real capacity [@baddeley1975]); compactness and
scannability of text; and machine legibility. These are the margins this
design spends on.

## 3. Channel phonology

### 3.1 The channel decomposition

A syllable is a vector over four channels: onset × vowel × coda ×
register. The v0.1 inventory (SPEC.md, `channels.json`): ten content
onsets /p t k m n s l w j tʃ/ plus a particle-reserved /h/; five vowels
/a e i o u/; four codas /∅ n s l/; two registers realized as vowel length.
The syllable template is CV(C) with a mandatory onset — a constraint that
self-segregating morphology (§5) and particle identification both lean on.
Raw space: 11 × 5 × 4 × 2 = 440 syllables.

### 3.2 Perceptual accessibility constraint

Every lexical contrast must be perceptible by speakers of essentially any
L1: no voicing pairs, no r/l contrast, no tone, five cardinal vowels. Two
deliberate accommodations go further. First, the particle onset /h/ is
*deletion-robust*: since content syllables never begin with a vowel, a
particle realized [h], [x], or ∅ (the attested L1 drift realizations)
remains unambiguously a particle. Second, the register channel carries no
lexical information at all (§4), so the many L1s without length contrasts
lose only error-detection, never content. The lone stretch is /tʃ/
(required as the tenth digit onset), whose drift realizations are handled
by weighted spacing.

### 3.3 Codespace budget

Parity halves the raw space: 200 content + 20 particle lexical syllables.
The part-of-speech channel (final coda; §5) partitions content
monosyllables into 50 forms per class — 150 usable under the three active
classes. Disyllable space (40,000 lexical points before spacing) dwarfs
the 1,500–3,000-root target. The resulting profile — a few hundred
monosyllables, Zipf-assigned; content words averaging under two syllables
— sits in Japanese/Hawaiian territory, above the ~200-usable-syllable knee
below which working-memory and recognition costs bite. [TODO: cite mora
inventories, word-length effect @baddeley1975.]

### 3.4 Rejected alternatives
[TODO: wide (~5k) and much-wider (~50k) inventories; why the ceiling binds
only the spoken channel; Ithkuil and steno as cautionary poles.]

## 4. The error-correction stack

The inner code is a parity check: register := (onset + vowel + coda) mod 2
over channel indices. This is the classical optimal distance-2
construction — any single-channel substitution yields a non-word — at the
classical price (half the raw space), but with a design twist: by spending
the *perceptually weakest* channel on parity, the code never asks a
listener to hear vowel length to identify a word, only to detect
corruption. The anti-parity complement is reserved for closed-domain mode
payloads (§7), making payload syllables audibly non-lexical.

Above the parity floor, distance is measured perceptually rather than
uniformly [TODO: confusion-matrix construction, tooling]: register-only
contrasts are impossible by construction; coda consonants and their
echo-vowel epentheses (/nas/ ~ [nasɯ̥]) are treated as near-identical, so
the lexicon never contains both members of such a pair; drift-prone onset
pairs (s/tʃ) and coda pairs (n/l) get extra spacing. Outer layers —
cross-syllable checks in disyllables, prosodic checksums, register
profiles with mandatory checksums for safety-critical speech — are
deliberately outside the frozen core. Conversational repair ("what?") is
the free outermost retransmission layer; casual speech buys detection and
lets repair do correction.

## 5. Self-segregating morphology

Two word classes with disjoint shapes: particles are exactly one
unstressed /h/-initial syllable; content words are one to three syllables
with initial stress (realized as pitch/intensity — never duration, which
is the register channel's carrier). Any syllable stream then has exactly
one parse: stressed syllables open content words, /h/-syllables are
particles, and a content word runs to the next stressed or particle
syllable. Segmentation doubles as error detection — a mishearing that
breaks a word template is caught before lexical lookup.

The final-syllable coda of a content word encodes part of speech (∅ noun,
n verb, s modifier, l reserved), which partitions rather than shrinks the
monosyllable space, makes cross-class mishearings syntax-detectable, and
turns derivation into a channel operation (sala → salan → salas).
Loanwords bypass the templates entirely via the spell/phonetic modes,
avoiding Lojban's loanword-mangling failure mode.

## 6. The decoupled featural script

[TODO: morpheme = glyph = chord; Hangul-style blocks; deterministic two-way
spell-out; silhouette skimming (POS/particle visual segregation); why
transparency accelerates acquisition (Finnish-vs-English decoding
literature) without claiming expert reading speedups.]

## 7. Mode subsystems

[TODO: reserved-onset mode particles; digit-pair base-100 numbers; date,
time (hour×quarter in one syllable), coordinate, spell-out modes;
complement-restricted payloads (anti-parity points) and their failure
pricing; checksum syllables; casual/careful/safety-critical registers;
modes as standalone adoption wedges inside English.]

## 8. Input methods

[TODO: chord layout derived from channel structure; expected WPM band and
the steno comparison; **phone/touch input** as a first-class target —
channel-per-gesture-axis designs; number/date modes as standalone mobile
keyboard wedge.]

## 9. Morphology and lexicon design

[TODO: closed core of roots + fully productive derivation; correlative
grids for all closed paradigms; Zipf assignment of monosyllables as designed
policy rather than diachronic erosion; governance.]

## 10. Related systems

[TODO: Esperanto (learning-time evidence, correlative grid, POS vowel,
governance failure modes); Lojban (machine parseability achieved, semantics
soft, phonotactic confusability); Toaq (syntax-on-a-channel validated; tone
as the wrong carrier); Toki Pona (floor of the size-vs-precision curve);
Ithkuil (completeness death); Hangul; shorthand systems; ASD-STE100 and
aviation English; Solresol; talking drums and Silbo Gomero.]

## 11. Evaluation plan

[TODO: define measurable claims — e.g. decoding-accuracy hours vs matched
orthographies; digit-span with monosyllabic digit pairs; simulated
mishearing (channel-noise) word-recovery rates vs Esperanto/English
wordlists; chord-entry learning curves vs QWERTY/steno; all pre-registered
where feasible.]

## 12. Discussion and limitations

[TODO: meaning stays soft (Lojban's lesson); community adoption dominates
design quality; what the sequel project (spatial sentence layer) would ask.]

## References

[Managed in `references.bib`. Claims imported from the design conversation
are marked TODO-verify until checked against primary sources.]
