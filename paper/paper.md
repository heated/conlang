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

[TODO: full literature review.] Key findings the design respects:

- Cross-linguistic information rate converges near ~39 bits/s; syllable-rate
  compensates for per-syllable information density [@coupe2019].
- Reading comprehension degrades in proportion to speed past ~400–500 WPM;
  RSVP shows the eyes were never the bottleneck [@rayner2016].
- Subvocalization is load-bearing for working memory during reading, not a
  removable inefficiency.
- Script density does not raise reading throughput: saccades shrink to hold
  information-per-fixation roughly constant across Chinese and English.

Therefore the exploitable margins are: **learning** (transparent
orthography, systematic morphology), **input speed** (chording), 
**compactness and scannability** (dense glyphs, structure visible
pre-comprehension), and **machine legibility** — not throughput.

## 3. Channel phonology

### 3.1 The channel decomposition
[TODO: final inventory from SPEC v0.1 — onsets, vowels, codas, register;
mandatory-onset syllable template; romanization.]

### 3.2 Perceptual accessibility constraint
[TODO: every contrast present in essentially all major L1 phonologies; no
tone; the L1-blind-spot argument against the "wide" inventory.]

### 3.3 Codespace budget
[TODO: raw space arithmetic; parity spend; POS-channel spend; usable
monosyllable count; comparison to Japanese/Hawaiian inventories and the
~200-syllable "knee".]

### 3.4 Rejected alternatives
[TODO: wide (~5k) and much-wider (~50k) inventories; why the ceiling binds
only the spoken channel; Ithkuil and steno as cautionary poles.]

## 4. The error-correction stack

[TODO: inner parity register (distance-2 via parity check, cost exactly 1/q);
perceptually weighted distance over a confusion matrix vs uniform Hamming;
cross-syllable outer checks in disyllables; phonotactic templates;
conversational repair as retransmission; redundancy budget ~10–15% vs 50%
for naive distance-2.]

## 5. Self-segregating morphology

[TODO: particle class on reserved onset; content-word templates; initial
stress as boundary signal; unique-parse property; loanword pass-through via
spell mode (contra Lojban's cluster requirement).]

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
