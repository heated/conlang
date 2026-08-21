---
title: "A Channel-Coded Constructed Language Optimized for Learning Speed"
author: "Edward Swernofsky (with Claude)"
date: 2026-08-08
status: living draft — grows with the build; sections marked [TODO] are stubs
bibliography: references.bib
---

## Abstract

[Draft.] We present the design of a constructed language that treats the
syllable as a vector of independent channels (onset, vowel, coda, plus a
computed written-layer check bit) and applies coding-theoretic error
correction over that space. The design
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
**vector of independent channels** — onset, vowel, coda, and a computed
check bit — and
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
2. A two-layer error-correction stack: casual speech protected by a
   humility assignment policy (no unrelated minimal pairs on likely
   confusions), word templates, phonotactics, and conversational repair;
   the written layer and careful speech registers add a
   confusion-weighted check bit on top.
3. A featural block script deterministically coupled to the phonology, with
   chorded (desktop) and touch (phone) input methods derived mechanically
   from the same spec.
4. Mode subsystems: closed semantic grids (numbers, dates, times,
   coordinates, spell-out) fenced by reserved boundary particles and a
   provably transposition-catching checksum, with written-layer
   anti-check marking.
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

A syllable is a vector over four channels: onset × vowel × coda, plus a
computed check bit that lives in the written layer (v0.2; §4). The
inventory (SPEC.md, `channels.json`): ten content onsets
/p t k m n s l w j tʃ/ plus a particle-reserved /h/; five vowels
/a e i o u/; four codas /∅ n s l/. The syllable template is CV(C) with a
mandatory onset — a constraint that self-segregating morphology (§5) and
particle identification both lean on. Spoken space: 220 segmental
syllables; the written layer carries the check bit on top (440
codepoints).

### 3.2 Perceptual accessibility constraint

Every lexical contrast must be perceptible by speakers of essentially any
L1: no voicing pairs, no r/l contrast, no tone, five cardinal vowels. Two
deliberate accommodations go further. First, the particle onset /h/ is
*substitution-robust*: since content syllables never begin with a weak
onset, a particle realized [h], [x], or [ʔ] (the normative floor — full
deletion with resyllabification is not licensed, and the lexicon carries
an anti-resyllabification constraint as backstop) remains unambiguously a
particle. Second, the check channel carries no lexical information and
(since v0.2) is not carried in casual speech at all — it lives in the
written layer, optionally realized as vowel length in careful registers
— so no speaker or listener is ever asked to produce or perceive a
length contrast in everyday use. The deliberate stretches are /tʃ/
(required as the tenth digit onset), whose drift realizations are handled
by check-bit coverage and spacing, and codas /s l/, which invite
epenthesis from Mandarin/Japanese-type L1s and are priced by an
echo-vowel constraint on the lexicon.

### 3.3 Codespace budget

The segmental space is 200 content + 20 particle codepoints (the
written-layer check bit is computed, never free). Accounting must separate codepoints, wordforms, and
root bodies: the part-of-speech channel (final coda; §5) yields 50
monosyllabic wordforms per class (150 across the three active classes),
but since a root's noun/verb/modifier forms share one onset–vowel body,
only 50 monosyllabic root bodies exist before spacing. The implemented
spacing engine then gives the honest count: after the glide-cell ban
(48) and the humility policy adopted after the deconfounding study
(§12) — no unrelated minimal pairs on high-confusion substitutions — an
exact maximum-independent-set computation yields **22 monosyllabic root
bodies** (18 under strict weighted-inclusive spacing), of which 15 are
initially assigned and the rest held in reserve for coinage and
drift. Disyllabic capacity (8,496 root bodies before
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

The inner code is a **confusion-weighted check bit**: every channel
value carries a normative bit, and check := (check(onset) +
check(vowel) + check(coda)) mod 2. Since v0.2 it is a *written-layer*
channel — always present in glyphs and available to machines,
optionally realized as vowel length in careful and safety-critical
speech registers, absent from casual speech, whose protection instead
comes from the humility assignment policy, templates, context, and
repair (§12). A uniform minimum-distance-2 code over this space is
not available at this price — a binary check cannot separate all values
of a ten-valued channel, and the honest distance-2 construction (a
mod-10 check over the largest channel) collapses the space to 20
codewords. The check bits are instead assigned so that the perceptually
likely confusions (s/tʃ, p/t, t/k, m/n, n/l, e/i, o/u, coda ∅/n, ∅/s,
n/l, s/l) all flip the written check, giving text and careful speech
pre-lexical error detection exactly where ears fail.

Casual speech is protected differently — by the lexicon itself. The
**humility assignment policy** bans any two unrelated words from
differing by a single high-confusion substitution (the covered set
above plus the forbidden residual pairs p/k, a/e, a/o, coda ∅/l);
mildly confusable pairs (p/m, k/m, t/n, w/j, e/o, i/u, coda n/s) are
licensable at a scored cost and avoided among high-frequency words.
Layered on that: echo-vowel epenthesis pairs (/nas/ ~ [nasɯ̥]) are never
both lexical, word+particle sequences whose resyllabification would
spell another word are excluded (the Lojban tosmabru class), and
conversational repair ("what?") is the free outermost retransmission
layer. Outer engineered layers — cross-syllable checks, prosodic
checksums, mandatory checksums for safety-critical speech — live in the
register-profile periphery, not the core.

## 5. Self-segregating morphology

Two word classes with disjoint shapes: particles are exactly one
unstressed weak-onset ([h]~[x]~[ʔ]) syllable; content words are one to
three syllables with initial stress (realized with pitch, intensity, and
— since the check left casual speech — duration, the most robust stress
cue; careful registers that realize the check as length narrow stress to
pitch/intensity). At the phonemic
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

The final-syllable coda of a content word encodes part of speech (∅
noun, n verb, s modifier, l reserved): 50 monosyllabic wordforms per
class against 40 under an Esperanto-style final-vowel scheme,
cross-class mishearings are caught by syntactic expectation (with a
written-layer check flag on the ∅/n and ∅/s flips), and derivation is a
channel operation — swap the coda, recompute the written check (sala →
salaan → salaas, the doubling being written marking). Loanwords bypass the templates entirely via the spell/phonetic
modes, avoiding Lojban's loanword-mangling failure mode.

## 6. The decoupled featural script

The script (spec: `docs/spec/script.md`, v0.2) is featural with zero
exceptions: every glyph is computed from the syllable's channel values,
so learning five bases, four modifiers, and one assignment table yields
the entire written inventory. A syllable is one square block with four
zones mirroring the channel vector — onset top-left, vowel carrier at
right, coda strip at bottom, and a small check slot in the top-right
corner. The compositional grammar follows Hangul's featural insight
[@sampson1985] minus its residual irregularities — but where Hangul
maps articulation to ink, this script inverts the principle. The v0.1
draft was articulatorily iconic (place → base shape, manner →
modifier); design review showed that this hands the ear's most
confusable pairs the script's most erodible visual distinctions while
minting eye-only confusions the lexicon cannot see. v0.2 therefore
assigns phonemes to (base, modifier) cells as an **error-correcting
code**: every phonetic confusion pair in the spec differs in both base
and modifier (visual distance 2), so no single degraded feature class
can merge an ear-confusable pair; the letter grammar uses only
degradation-robust contrasts (full strokes, wide doubling, attached
caps and crossings — no floating bars, breaks, dots, or fill
contrasts, the feature classes typographic history erodes first); and
the visually closest pairs are, by construction, phonetically distant.
The channels end up covering each other's weak pairs symmetrically: a
misreading yields a phonetically implausible word, a mishearing yields
a visually distant glyph. The assignment is solved deterministically
from the spec's confusion data, is frozen as normative data, and
yields a free regularity for the mode subsystem — glyph base = tens
digit mod 4 — exactly where per-pair discrimination has no lexical
safety net. Two guards make the property durable. An occupancy-grid
raster floor in the test suite enforces the achieved distances
(minimum 0.62 across phonetic pairs at a phase-minimized 14×14
raster, against near-collapse for the v0.1 equivalents). And because
phonetic distance protects listeners but not silent readers, the
eye's residual weak set — exactly the same-base pairs — is enumerated
in the spec data and priced by the lexicon generator, which costs one
root body at the strict tier; the spec checker enforces that the
enumeration stays complete.

Two grammatical facts are visible before any letter is read. The coda
strip is the part-of-speech marker (§5), and it deliberately gets the
loudest ink in the block — full-width strip bars (empty = noun, single
= verb, double = modifier) — because the POS channel is simultaneously
check-invisible and lenition-prone in speech, making the eye its main
defense. And word assembly makes syntax skimmable by silhouette —
content words stack their blocks vertically into glyphs one to three
blocks tall, while particles render as single blocks at ~70% scale, so
the grammatical scaffold reads as a height rhythm. The written-layer
check bit (§4) occupies the check slot as a computed filled dot, the
glyph-level equivalent of romanization vowel doubling; mode-payload
spans are flagged by a continuous run-rule beside the glyph stack
rather than per-block marks, matching where frame integrity actually
lives (§7).

The learnability claim is deliberately asymmetric. Orthographic
transparency demonstrably accelerates *decoding* acquisition — regular
shallow orthographies reach accurate word reading years earlier than
deep ones [@seymour2003], and a compositional featural system is the
transparent limit of that scale — but fluent reading runs on a trained
whole-word visual lexicon that any novel script resets to zero, so we
claim fast decoding acquisition and make no expert-speed claims beyond
the saccade-scaling observation of §2 [@rayner2016]. The script is also
where this design parts company with Toaq's tone-grammar insight (§10):
grammar-on-a-channel is kept, but relocated from the worst-perceived
auditory channel to the best-perceived visual ones — height, position,
and silhouette.

Layout is an open, measured question: stacked blocks are the spec
default; a fused one-character-per-word mode and a shared-headstroke
mode exist as measured prototypes (a fair factorial comparison found
disyllable layouts statistically indistinguishable under the proxy
metric, with the fused radical composition ahead for trisyllables;
no human legibility data yet). The feature grammar has headroom by
construction: 18 usable onset cells against 11 assigned, nine vowel grid positions against five, so
the wider codepoint model (§12) fits, with any new modifier required to
pass the same robustness bar. The block diagram is simultaneously the
chord diagram — one input axis per zone — which is what makes glyph,
chord, and pronunciation three projections of one channel vector
rather than three systems to learn (a fourth, lossy projection —
channel-subset "skeleton" input resolved by an IME — is on the
roadmap). The mapping is enforced, not aspirational: the assignments
are normative data in `channels.json`; `spec_check.py` machine-checks
the distance-2 invariant itself, so a reassignment that put two
confusable phonemes on overlapping visual features would fail the spec
build; and the renderer's test suite asserts pairwise distinctness of
all 220 syllable blocks plus the raster floor above.

## 7. Mode subsystems

Where the semantic space is a grid rather than a fuzzy web — numbers,
dates, times, letter sequences — the language drops redundancy and uses
the raw channel product, fenced off by reserved-onset mode particles.
In the written layer payloads carry the anti-check polarity, so text and
machines separate them from the lexicon per syllable; in casual speech a
payload syllable and a lexical one can share a segmental shape, and the
boundary particles, frame grammar, and checksum carry the burden (§4);
a digit pair 00–99 is one syllable (tens→onset, units→rime, the code frozen with the core), and
larger numbers are positional base-100. Dates and coordinate digits
reuse the same pairs verbatim — no month names, no separate tables — and
clock time is a single syllable via two orthogonal rules on the same
grid (onset = hour's last digit, coda = hour's tens, vowel = quarter
hour). Sample renderings (machine-generated from the spec): 4,207 =
*huu mi cin* (3 syllables against roughly ten in English); 2026-08-08 =
*ho ta teen coon coon*; 14:30 = *hii miin*.

The density is honestly priced. In the v1 code, digit payloads used
the full grid: 87.5% of single-channel mishearings of a digit syllable
yielded another valid digit (60% of those flipped the computed check —
detectable in writing and careful registers; in casual speech all were
silent until the checksum). The v2 revision abandons that
register-parity defense for sparsity: the codebook is 100 syllables
chosen from 220 — units use ten rimes selected by exhaustive search
for perceptual spacing (only the corner vowels a/i/u appear; the
e/i, o/u, a/e, a/o confusion classes are simply absent from digits),
and a confusion-matrix audit maps the surviving confusable pairs of
both channels to numerically distant values (every audited pair ≥3
apart; the worst at distance 8–9). Error resistance now rides on
audible channels alone. The residue-100 corner case of the mod-101
checksum is handled structurally: no checksummed chunk may carry
residue 100 — a legal split under the list-separator particle always
exists, since a lone digit pair's residue is its own value. The mode
system
therefore carries its own outer code: an optional closing checksum
syllable — a position-weighted sum mod 101 over per-symbol values, which
provably changes under every single-symbol substitution and every
transposition — mandatory in a safety-critical register profile, in the
tradition of aviation readbacks and ASD-STE100. Casual speech omits it and leans on conversational
repair, which costs nothing until an error actually occurs.

Modes double as the project's adoption wedge: the number, date, and time
codes function inside a host language without learning the lexicon, and
the chorded/touch input methods (§8) can ship them as standalone tools —
adoption gradients rather than cliffs.

## 8. Input methods

[TODO: chord layout derived from channel structure; expected WPM band and
the steno comparison; **phone/touch input** as a first-class target —
channel-per-gesture-axis designs; number/date modes as standalone mobile
keyboard wedge.]

## 9. Morphology and lexicon design

[TODO: closed core of roots + fully productive derivation; correlative
grids for all closed paradigms; Zipf assignment of monosyllables as designed
policy rather than diachronic erosion; governance.]

## 9b. The zonal program (companion track)

Alongside the engineered language, the project runs a receptive-first
track: a Romance zonal auxlang (RZ) with a six-register parallel
corpus, a complete regularized grammar (person-invariant verbs,
number-only agreement, three irregular verbs), a recipe-driven
lexicon with a mandatory false-friend screen, and a Latin-primary
orthography with an optional featural display layer. A controlled
Latinate-English register and host-language mode conventions extend
the same machinery toward the English zone. The zonal track's claims
are deliberately modest pending human testing: its comprehension
instrument (cloze + gist, incumbent-controlled) is specified but
unrun; the milestone reviews correctly note that the entire program
has zero external subjects to date, and that its niche overlaps
Interlingua's. Full designs and measurements: the repository's
docs/design/zonal/ tree; a wide-inventory greenfield variant (GF-W:
16 onsets, 320 syllables, 38 humility-safe monosyllabic roots,
computed) bridges the two tracks and frames the width decision.

The zonal track has since tentatively adopted the engineered number
mode: because the zonal orthography declares h silent, the h-onset
region of syllable space is vacant, and mode frames colonize it at
zero cost to the inherited lexicon ([h] is dead in words, live in
frames). Its digit onsets align with Romance number-word initials
where possible (six of ten guessable at first contact), a trade
that knowingly places two confusable pairs at adjacent values
because the source languages do (dos/tres, cinco/seis) and leans on
the checksum register to compensate. The mode is the one zonal
component whose learning cost is flat across L1 cohorts.

The zonal display script subsequently absorbed three consequences of
these decisions in one hardening pass. The number mode's pronounced
[h] forced a letterform into a script that had treated h as purely
silent — resolving a reviewer-flagged contradiction, since the
script writes phonemes and [h] now exists exactly where it is
spoken. The regularized verb morphology turned out to be strong
enough to drive tense logograms (past and conditional marks) from a
lexicon-harvested verb-stem set alone, with no hand tagging: the
suffix fires only when stripping it leaves a known verb stem, so
*parlava* segments and *materia* does not. And the open
part-of-speech question (deterministic endings versus script-only
marking) acquired its first concrete artifact: an optional underline
channel — verbs fully underscored, adjectives half — that marks
word class in writing without touching a single inherited word
shape. Legibility claims for all of this are now regression-tested
with phase-minimized raster distances at small type sizes, the same
instrument the engineered script uses, after measurement showed one
suffix-logogram pair fully collapsed (distance 0.000) at seven
pixels in the shipped v0.

The learning-budget ledger's value side acquired its first
measurement: coverage curves over the ~940-token zonal corpus show
the closed class — 62 particles, determiners, prepositions and
copulas — covering 49.4% of running tokens, with ~120 content
lemmas reaching 70% of content-token coverage and a Zipf band
placing the 95%-coverage lexicon near five hundred open lemmas.
The corpus is too small to exhibit the inflectional dividend
directly (nearly every content word appears once), so that number
comes from the grammar instead: an RZ lemma carries ~3.7
exceptionless recognizable forms against ~20 synthetic forms for a
Spanish lemma, a five-fold recognition-load reduction that accrues
precisely to the cohorts the zone's cognate transfer does not serve
— the same asymmetry the ledger identifies as the greenfield-zonal
thesis (docs/design/zonal/rz-lexicon-coverage.md).

The width decision itself generalizes from a binary to a ladder.
Running the same capacity machinery over progressively widened
inventories (diphthong nuclei ai/au/oi; onsets to 19 with v/ʃ/dʒ;
twelve stop–liquid clusters with licensed epenthesis) yields a
lattice of superset variants — GF-N 22 → GF-ND ≥28 → GF-W 38 →
GF-WD ≥48 → GF-C ≥85 humility-safe monosyllabic roots — in which
the digit/mode subsystem, pinned to the narrow ten onsets, is valid
at every rung. Diphthongs prove to be the cheapest capacity on the
board (matching GF-W's syllable count without touching the
10-consonant universal floor), added onsets saturate quickly after
GF-W, and the cluster rung converges on Romance word shapes — the
limit of the ladder is the zonal strategy itself. Width is thus a
position on a single greenfield↔zonal axis, and the open design
decision is which point, or nested pair of points, to commit to
(docs/design/width-ladder.md).

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
  L1-parameterized confusion model (e.g. a speaker who realizes /tʃ/ as
  [ʃ]); measure the fraction of errors that are (a) detected by
  lexical-gap and template/segmentation violations (casual layer),
  (b) additionally flagged by the written-layer check (text and careful
  registers), (c) silent word substitutions. Baselines: Esperanto and
  English wordlists under matched noise. Claim under test: humility
  assignment yields fewer silent substitutions per unit of codespace
  than uniform spacing or natural lexicons — established in
  simulation (§12), to be replicated with calibrated confusion data.
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

## 12. Discussion, limitations, and live alternatives

Two structural humilities bound everything above: meaning stays soft no
matter how hard the form layer is engineered (Lojban's lesson), and
community adoption historically dominates design quality (Esperanto and
Klingon outlived better-engineered rivals). Two design explorations,
conducted adversarially against our own architecture, sharpen both.

**Does the inner code earn its keep?** A simulation over matched,
morphology-inclusive Zipf-weighted lexicons (tools/explore_noparity.py,
itself twice adversarially reviewed) separates two decisions the
original design conflated: the *assignment policy* and the *register*.
The assignment policy dominates. Licensing high-confusion minimal pairs
among the most frequent words — which the check bit invites, since the
register "catches" those substitutions — produces a 22% silent-
substitution rate (conditional on a mishearing event; 15% exposure-
weighted) for length-deaf listeners, the design's own priority
population. A humility policy that refuses such pairs cuts this to 3.9%
with or without the register, at a capacity cost of 34→22 monosyllabic
root bodies. With humility assignment adopted, the register is pure
insurance for length-sensitive listeners — residual silent rate 3.9% →
1.4%, and audible flagging of noun↔verb/noun↔modifier morphology flips
— while delivering exactly nothing to length-deaf listeners and taxing
all speakers (length production, a stress-duration conflict, erosion
exposure of a zero-load contrast). Whether that insurance justifies its
costs, or belongs only in the written layer and a careful-speech
register, is a values decision the simulation cannot make; what it
establishes firmly is the humility policy, and that the original
configuration was the one choice strictly wrong for the population the
design claims to serve. [Resolution, adopted tentatively: humility
assignment in the core, the check bit demoted to a written-layer
channel with optional careful-register realization — the configuration
described throughout this paper. Re-promoting the check to a mandatory
spoken channel, or deleting it outright, remain documented
minor-version paths in the spec.]

**Is the a-priori lexicon worth it?** Vocabulary, not grammar, is
plausibly the long pole of adult language learning: full regularity
saves tens of hours while thousands of arbitrary roots cost hundreds
[TODO-verify: vocabulary-acquisition rate literature]. An
Esperanto-like alternative — a-posteriori roots partially known to
European-language speakers (a steep Romance-tilted gradient, not a flat
discount), plus the same systematic chording layer over an
already-phonemic orthography — plausibly beats this design on raw
time-to-use for the realistic early-adopter population, while losing
global phonological fairness, machine parseability, and the featural
script. The designs optimize different objectives — fastest for anyone
on Earth versus fastest for those who show up — and that is a values
choice, not an engineering result. A hybrid (ship the input engineering
and mode subsystems into an existing host language as the adoption
wedge, keeping the channel language as the research artifact) is
attractive but underdetermined: the host could as easily be English as
Esperanto, and the hybrid defers rather than answers the values
question. We record it as an open program decision rather than a
conclusion.

The spatial sentence layer — rendering argument structure for parallel
vision rather than the serial channel — remains the designated sequel:
it is the only direction that attacks the ~39 bits/s wall itself rather
than routing around it.

## References

[Managed in `references.bib`. Claims imported from the design conversation
are marked TODO-verify until checked against primary sources.]
