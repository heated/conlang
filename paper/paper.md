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

Constructed languages have historically optimized for expressive
completeness (Ithkuil), logical transparency (Lojban), community
neutrality (Esperanto), or minimalism (Toki Pona). This project optimizes
a single variable those designs treat as incidental: **learning speed** —
time from zero to functional use, for adult second-language learners of
any first language. Every other property is either derived from that
target, priced against it explicitly, or declared a non-goal.

The central design move is to treat the syllable not as an atom but as a
**vector of independent channels** — onset, vowel, coda, register — and
to engineer over that coordinate space the way coding theory engineers
over symbol alphabets: an error-detecting check channel, deliberate
spacing between codewords weighted by human mishearing rather than
uniform Hamming distance, dense closed-domain codes where semantics form
a grid (numbers, dates, times), and generous redundancy where they do
not. Because glyphs, chords, and articulations are all renderings of the
same vector, learning any one of the three renderings teaches the other
two: the writing system, the input method, and the phonology are one
object, not three curricula.

Explicit non-goals, argued in §2: raw speech and reading throughput
(empirically pinned near ~39 bits/s by cognition, not by the code
[@coupe2019]), and spoken density (the "wide phonology" branch is
rejected in §3.4). The honest pitch is therefore narrow: large gains in
time-to-literacy and input speed, real gains in compactness,
scannability, and machine legibility, and approximately zero gains in
how fast a human can talk or comprehend — those walls belong to the
brain, not the notation.

Contributions:

1. A syllable-as-channel-vector phonology with an explicit codespace budget.
2. An error-correction stack for human speech: a confusion-weighted check
   channel, perceptually weighted spacing, cross-syllable checks,
   phonotactic templates, and conversational repair as the outermost free
   layer.
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
through to throughput: Chinese and English readers show similar reading
rates, with Chinese forward saccades about half the length — denser
scripts induce proportionally shorter saccades, holding
information-per-fixation roughly constant [@sun1985].

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
*substitution-robust*: since content syllables never begin with a weak
onset, a particle realized [h], [x], or [ʔ] (the normative floor — full
deletion with resyllabification is not licensed, and the lexicon carries
an anti-resyllabification constraint as backstop) remains unambiguously a
particle. Second, the register channel carries no lexical information at
all (§4), so the many L1s without length contrasts lose only
error-detection, never content. The deliberate stretches are /tʃ/
(required as the tenth digit onset), whose drift realizations are handled
by check-bit coverage and spacing, and codas /s l/, which invite
epenthesis from Mandarin/Japanese-type L1s and are priced by an
echo-vowel constraint on the lexicon.

### 3.3 Codespace budget

The computed register halves the raw space: 200 content + 20 particle
lexical codepoints. Accounting must separate codepoints, wordforms, and
root bodies: the part-of-speech channel (final coda; §5) yields 50
monosyllabic wordforms per class (150 across the three active classes),
but since a root's noun/verb/modifier forms share one onset–vowel body,
only 50 monosyllabic root bodies exist before spacing. The implemented
spacing engine then gives the honest count: after the glide-cell ban (48)
and pairwise confusion constraints, an exact maximum-independent-set
computation yields **34 assignable monosyllabic root bodies** under the
adopted two-tier confusion policy (19 under strict single-tier spacing),
of which 23 are initially assigned and the rest held in reserve for
coinage and drift. Disyllabic capacity (8,496 root bodies before
assignment-time checks) dwarfs the 1,500–3,000-root target, so the
language is disyllable-dominant by consequence: monosyllables cover only
the very top of the Zipf curve, as in Japanese or Hawaiian. Whether this
profile clears the working-memory comfort line is an explicit evaluation
target. [TODO: cite mora inventories, word-length effect @baddeley1975.]

### 3.4 Rejected alternatives, and the expansion path

A "wide" inventory (~20 onsets with voicing pairs, ~10 vowels, more codas,
~5,000 raw syllables — roughly Cantonese/Vietnamese territory) buys mostly
monosyllabic content vocabulary at a precise cost: each added contrast
lands in some population's L1 perceptual blind spot (voicing pairs, i/ɪ,
tone contours), degrading "learnable by anyone quickly" to "learnable with
an accent and persistent mishearings." A "much wider" scheme (~50,000 via
contour tones, phonation, secondary articulation — Ithkuil's neighborhood)
fails structurally: the channels stop being independent in the mouth and
ear, and natural languages empirically cap around 10–15k syllables. Both
were rejected for the spoken layer — but only the ear ever imposed the
limit. The written/typed layer can carry arbitrarily many codepoints, which
is exactly what the decoupled script exploits (§6), and the spec freezes
the core as an expansion-compatible family (SPEC §9): channel values append
without renumbering, so a deliberate later widening — or a small push, a
fifth coda, an eleventh content onset — is a versioned decision rather
than a redesign.

## 4. The error-correction stack

The inner code is a **confusion-weighted check bit**: every channel value
carries a normative bit, and register := (check(onset) + check(vowel) +
check(coda)) mod 2. A uniform minimum-distance-2 code over this space is
not available at this price — a binary check cannot separate all values
of a ten-valued channel, and the honest distance-2 construction (a mod-10
check over the largest channel) collapses the space to 20 codewords. The
design instead chooses *which* substitutions the one cheap bit catches:
check bits are assigned so that the perceptually likely confusions (s/tʃ,
p/t, t/k, m/n, n/l, e/i, o/u, coda ∅/n, ∅/s, n/l, s/l) all flip the
register, while the invisible distance-1 pairs (660 of them, enumerated
mechanically) are deliberately the unlikely confusions, which the lexicon
generator refuses to assign as minimal pairs. Two properties fall out.
The weakest perceptual channel (length) carries only redundancy — a
listener who cannot hear it loses detection, never content. And the
anti-check complement is reserved for closed-domain mode payloads (§7):
payload syllables are non-lexical by construction, though audibly so only
to register-sensitive listeners, so mode boundaries must be independently
robust.

Above the check-bit floor, distance is measured perceptually rather than
uniformly [TODO: confusion-matrix construction, tooling]: register-only
contrasts are impossible by construction; check-invisible minimal pairs
are forbidden outright; coda consonants and their echo-vowel epentheses
(/nas/ ~ [nasɯ̥]) are treated as near-identical, so the lexicon never
contains both members of such a pair; and word+particle sequences whose
resyllabification would spell another word are excluded (the Lojban
tosmabru class). Outer layers — cross-syllable checks in disyllables,
prosodic checksums, register profiles with mandatory checksums for
safety-critical speech — are deliberately outside the frozen core.
Conversational repair ("what?") is the free outermost retransmission
layer; casual speech buys detection and lets repair do correction.

## 5. Self-segregating morphology

Two word classes with disjoint shapes: particles are exactly one
unstressed weak-onset ([h]~[x]~[ʔ]) syllable; content words are one to
three syllables with initial stress (realized as pitch/intensity — never
duration, which is the register channel's carrier). At the phonemic
level, given boundary-preserving realizations, any syllable stream has
exactly one parse: stressed syllables open content words, weak-onset
syllables are particles, and a content word runs to the next stressed or
particle syllable. Segmentation doubles as error detection — a mishearing
that breaks a word template is caught before lexical lookup. The
conditions are stated, not assumed: the particle onset's normative floor
is the glottal stop (full deletion with cross-boundary resyllabification
— /tas ha/ surfacing as [ta.sa] — is unlicensed, and the lexicon's
anti-resyllabification constraint makes such reductions fail to parse
rather than parse wrongly), and parse robustness under degraded stress is
an explicit simulation target (§11) rather than a theorem about
connected speech.

The final-syllable coda of a content word encodes part of speech (∅ noun,
n verb, s modifier, l reserved): 50 monosyllabic wordforms per class
against 40 under an Esperanto-style final-vowel scheme, cross-class
mishearings become syntax-detectable, and derivation is a channel
operation — swap the coda, recompute the register (sala → salaan →
salaas). Loanwords bypass the templates entirely via the spell/phonetic
modes, avoiding Lojban's loanword-mangling failure mode.

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

Every load-bearing mechanism here has a precedent that validates the
mechanism and a failure that locates its limit. Esperanto demonstrates
designed-language learnability (~150–200 hours to conversational use
versus ~600+ for natural Romance languages [TODO-verify @fsi;
@cherpillod]) and already channel-codes one subsystem — the correlative
table's 5×9 semantic grid, which speakers report as the easiest part of
the language; its governance failure (unregulated borrowing duplicating
derivable words) motivates the frozen-core/owned-spec discipline. Lojban
proved a spoken language can be fully machine-parseable and that
self-segregating morphology works, while its phonotactics illustrate the
confusability mistake weighted spacing exists to avoid; its loanword
mangling motivates our spell-mode pass-through. Toaq is the strongest
validation of grammar-on-a-channel — tone marking syntactic role deletes
Lojban's terminator clutter — and simultaneously the argument against
spending the worst-perceived channel on syntax; this design relocates the
insight to the glyph layer, the particle class, and (optionally) the
register bit. Hangul proves featural scripts are learnable in days;
Chinese radicals prove semantic-plus-phonetic glyph composition at scale
and, at 30% phonetic reliability, price the cost of letting the mapping
decay. Stenotype proves one-chord-per-unit motor performance (200+ WPM)
and locates its own bottleneck in arbitrary briefs and irregular
orthography — precisely what a regular channel grammar removes. Toki Pona
marks the floor of the inventory-size curve (conversation slows when
paraphrase becomes constant); Ithkuil marks the ceiling (completeness
kills speakability); Solresol's seven notes sit below the articulatory
floor while prefiguring multimodal serialization of one code. ASD-STE100
and aviation English show institutions adopt constrained registers when
reliability wins are legible — the model for this design's safety-critical
register profile.

## 11. Evaluation plan

The design makes falsifiable claims; each maps to a measurable study, and
several run without human subjects.

**Simulation studies (no subjects, run against the implemented spec):**

- *Channel-noise robustness.* Corrupt syllable streams with an
  L1-parameterized confusion model (e.g. a listener who merges vowel
  length, or realizes /tʃ/ as [ʃ]); measure the fraction of errors that
  are (a) detected by parity, (b) detected by template/segmentation
  violations, (c) silent word substitutions. Baselines: Esperanto and
  English wordlists under matched noise. Claim under test: structured
  redundancy yields fewer silent substitutions per unit of codespace
  spent than uniform spacing or natural lexicons.
- *Segmentation stress test.* Generate syllable streams with and without
  the prosodic boundary signal degraded; verify the unique-parse property
  holds and measure how gracefully parsing degrades when stress detection
  is unreliable. Claim: SSM parsing needs only local information.
- *Zipf coverage.* With the seed lexicon, compute expected syllables per
  word over a reference corpus frequency distribution; compare against
  Japanese/Hawaiian empirical averages. Claim: mean word length stays
  under ~2 syllables despite the small inventory.

**Human studies (small-N first, pre-registered where feasible):**

- *Decoding acquisition.* Hours of instruction to accurate pseudo-word
  reading in the featural script, versus matched training on Finnish-style
  Latin orthography (the transparent-orthography gold standard
  [@seymour2003]). Claim: featural blocks reach criterion at least as
  fast, despite novel glyph shapes.
- *Digit-pair span.* Auditory digit span with monosyllabic digit pairs
  versus the subject's L1 number words; the word-length effect
  [@baddeley1975] predicts a measurable span increase.
- *Chord-entry learning curve.* WPM over practice hours on the chorded
  layout versus QWERTY novices and steno students; claim: the curve's
  early segment (first ~20 hours) beats steno's by a wide margin because
  there are no arbitrary briefs to memorize.
- *Mishearing repair.* Minimal-pair identification in noise across L1
  groups; claim: no lexical contrast depends on a distinction any tested
  L1 group cannot hear.

**Negative controls the design predicts:** expert reading speed in the
dense script should NOT exceed matched Latin-orthography reading
[@rayner2016]; conversational speech rate in bits/s should sit near the
cross-linguistic band [@coupe2019]. Finding otherwise would falsify the
throughput-ceiling framing, not vindicate the design.

## 12. Discussion and limitations

[TODO: meaning stays soft (Lojban's lesson); community adoption dominates
design quality; what the sequel project (spatial sentence layer) would ask.]

## References

[Managed in `references.bib`. Claims imported from the design conversation
are marked TODO-verify until checked against primary sources.]
