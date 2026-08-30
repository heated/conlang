---
title: "Engineering Languages for Learning Speed: A Channel-Coded Greenfield, a Receptive-First Romance Zonal, and the Portable Toolkit Between Them"
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
density inside an otherwise redundant language. The project runs two
tracks: this engineered ("greenfield") design, and a receptive-first
Romance zonal auxlang (RZ) that inherits its surface from the zone and
imports the engineered mechanisms only where they are worth their
measured learning cost — the intended shipping product, with the
greenfield as its laboratory. The generalizable contribution is the
portable toolkit that migration produces: a priced menu of mechanisms
(mode subsystems, error-absorption declarations, closed-class
discipline, chorded input, display-script layers, learning-budget
accounting) applicable to auxiliary-language designs beyond either
track. We argue from the cross-linguistic literature that such designs
can compress learning time substantially while leaving speaking and
reading throughput unchanged, and we outline an evaluation program.
Evidence status, stated plainly: all results to date are computed,
simulated, or corpus-measured; the project has zero external human
subjects, and every learner-facing number is a labeled hypothesis
until the pre-registered comprehension studies run.

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
(both look bounded well below what a notation could plausibly move:
read speech near ~39 bits/s [@coupe2019], and reading — a separate
literature that converges just as hard — near 184 wpm aloud and 238 wpm
silent across 17 scripts, with Chinese the *fastest* in the set
[@irest2012; @brysbaert2019]), and spoken density (the "wide phonology"
branch is rejected in §3.4). The honest pitch is therefore narrow:
large gains in time-to-literacy and input speed, real gains in
compactness, scannability, and machine legibility, and — on the
evidence available — little or no gain in how fast a human can talk or
comprehend. We treat those two as low-prior directions rather than
proven walls; §2 states precisely how much the cited work does and does
not establish, since none of it tested a constructed language.

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
6. A two-track method and its product: a zonal auxlang (RZ) built by
   recipe from the zone with a measured false-friend screen, a
   learning-budget ledger that prices every design decision in
   learner-hours, a mining gate for porting engineered mechanisms into
   a naturalistic surface, and the resulting portable toolkit of
   priced, conditional add-ons for auxiliary languages generally
   (§9b).

## 2. Why not faster speech or reading: the throughput ceiling

A language designed for *speed* would be optimizing a variable the
evidence says is hard to move. Across 17 typologically diverse languages,
information rate in *read* speech clusters near a mean of ~39 bits/s:
languages with information-dense syllables are read proportionally
slower, and sparse ones faster, so the product stays roughly flat
[@coupe2019]. Because this premise is load-bearing for the whole design,
its limits belong in the same breath as the number. It is a controlled
reading task rather than spontaneous conversation; the compensation is a
cross-linguistic correlation, not a demonstrated mechanism; the measure
is information-theoretic, which is not the same object as the count of
semantic distinctions a grammar marks explicitly; and no constructed
language was in the sample, so extending it to one whose speakers are all
deliberate L2 composers is an extrapolation [H]. What the result
does support is that the *expected return* on engineering for raw spoken
throughput is small and may be zero — enough to make it a non-goal,
not enough to call the gain impossible. The authors read the bound as
cognitive rather than articulatory, and inner speech, silent reading and
deliberate sequential thought do cluster in the same band, though that
convergence is assembled from separate literatures rather than measured
as one constant. Reading tells the same story from the
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
raster floor in the test suite enforces the measured raster distances
(a proxy for legibility, not legibility itself)
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
no human legibility data yet). A four-engine bake-off on identical
specimen text (`docs/design/gz-engine-bakeoff.md`) subsequently
sharpened the question: engines that carry the vowel as a small
appended mark — including the v0.2 boxed default — hold vowel
distances an order of magnitude below their onset distances at a
reading-size raster (median 0.05–0.08 against 0.25–0.57), and at
a ~6px extreme raster their isolated vowel channels collapse
outright (12/20 to 20/20 of vowel-different word pairs rendering
identically under phase-minimized occupancy distance). The two
engines that promote the vowel to word-level structure — a drawn
inter-letter connector whose slope and reach encode the vowel, and
a Hangul-style block whose frame the vowel constitutes — hold
vowel medians of 0.30–0.42 at reading size, and the block engine's
vowel channel survives even the extreme raster with no collapsed
pairs. The chain engine is also the densest page at equal measured
letterform size (~25–35% less area per word than the incumbent);
the block engine is density-parity with it. The design lesson
generalizes beyond this script: a phonological channel is only as
robust as the *scale* of the ink it modulates, and diacritic-scale
ink fails first. On the adopted block substrate, a rule-derived
compression dial (`docs/design/gz-script-efficiency.md`) then
prices page efficiency directly: rendering the closed particle
class as bare vowel frames (its constant onset carries no
information within the class), squashing multisyllable blocks
vertically, and abbreviating high-frequency words to their first
block plus a brief mark takes the same text to 77% of the
transparent page area and 59% of its ink; fixing every content
word into one uniform character cell — the CJK move — reaches 50%
of the area at 55% of the ink. The measured distinctness price is
real but modest (the squash costs ~12% of the vowel-channel
median, with no pair collapses at reading raster); the
reading-comprehension cost of each dial position remains an
untested hypothesis. (All of these figures are measured on the
narrow-core inventory; the port to the greenfield-zonal's
Romance-sized syllable space — roughly ten times the syllables,
with cluster onsets and diphthongs — is open work, and its larger
monosyllabic vocabulary changes the compression arithmetic in the
page's favor.) The feature grammar has headroom by
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
*huu cii mu* (3 syllables against roughly ten in English); 2026-08-08 =
*ho ta taas miis miis*; 14:30 = *hii cin*.

The density is honestly priced. In the v1 code, digit payloads used
the full grid: 87.5% of single-channel mishearings of a digit syllable
yielded another valid digit (60% of those flipped the computed check —
detectable in writing and careful registers; in casual speech all were
silent until the checksum). The v2 revision abandons that
register-parity defense for sparsity: the codebook is 100 syllables
chosen from the 200 content-shaped payload points (the h-onset row is
reserved for frames) — units use ten rimes selected by exhaustive
search
for perceptual spacing (only the corner vowels a/i/u appear; the
e/i, o/u, a/e, a/o confusion classes are simply absent from digits),
and a confusion-matrix audit maps the surviving confusable pairs of
both channels to numerically distant values (every audited pair ≥3
apart; the worst at distance 8–9). Error resistance now rides on
audible channels alone — and sparsity pays a second time: because
half the payload grid is not a codeword, 280 of 1600 single-channel
corruptions now fall outside the code and are caught by the frame
grammar, against 200 under the dense v1 code. The residue-100 corner case of the mod-101
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

*Program note (2026-08-22): the tracks' roles have inverted. The
zonal language (RZ) is now the intended shipping product — the
receptive bootstrap is hypothesized to win on total time-to-value
[H] — and the
engineered greenfield line serves as the laboratory and feature
mine: mechanisms migrate into RZ exactly when their measured value
justifies their learner-hour price (the mining gate; e.g. the
number mode and the error-absorption declarations already ported,
each priced in the learning-budget ledger). The greenfield also
retains ownership of the featural script, which RZ consumes only as
an optional display layer. A further generalization lane restates
each ported mechanism zone-agnostically, as a priced toolkit of
add-ons applicable to any zonal, continental, or global auxlang;
that toolkit is the intended spine of this paper's contribution.
Charter: docs/design/program.md.*

*The program's first two steps ran 2026-08-22. The bootstrap
scenario packet (rz-bootstrap-scenarios.md) recommends a
receptive-first funnel — a graded web reader with an embedded
self-scoring cloze, launched through the thesis publication
(hypothesis: a paper can serve as the media moment), with
production tooling staged to catch inbound writers, and governance
plus legitimacy tokens as explicit prerequisites — the five growth
factors of the only measured zonal growth loop (Interslavic). The
GZ→RZ mining audit (gz-rz-mining-audit.md) then walked every
greenfield mechanism through the port gate under those weights.
Outcome: one pure-upside purchase (a closed-class guarantee: the
96-form function-word inventory is closed by rule — a lexical
policy, distinct from the greenfield's unported prosodic clitic
channel; 60 of the 96 forms are corpus-attested and carry 49.2% of
running tokens), one policy-now/instrument-pending purchase (an
acoustic-confusion screen on minted vocabulary), and structural
declines with a shared reason: POS-ending remapping and
penult-always stress fail the first-contact invariant regardless of
their measured value, narrowing RZ's POS dial to the display-only
R-scheme (itself pending evidence behind the script workshop gate)
while the dial remains genuinely open for the greenfield. The
audit's shape is itself a finding: every mechanism that ports
cheaply is cohort-flat and lexicon-free; every decline touches
inherited surfaces — word shapes or word stress.*

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
shape. All of this is now regression-tested with phase-minimized
raster distances at small type sizes — the same instrument the
engineered script uses, and the same caveat: occupancy distance is a
proxy used to compare conditions, not to certify human reading —
after measurement showed one
suffix-logogram pair fully collapsed (distance 0.000) at seven
pixels in the shipped v0.

Joint optimization subsequently reproduced the codebook's
architecture (agreement between two computations, not external
validation): optimizing all hundred syllable-values together at
the syllable level (cross-channel confusion products included)
reproduces the per-channel solution to within one swap, freeing
the code from its product structure buys an eight-percent
average-case improvement with no worst-case gain — declined
against the learnability cliff of a hundred rote pairs — and the
English-digit acceptance bar fails in exactly one structured
place, the four bare-versus-coda rime pairs, which converts the
careful register's "disyllables for the worst few digits" from a
gesture into a determinate assignment.

The learning-budget ledger's value side acquired its first
measurement, and two instructive corrections. Coverage curves over
the de-duplicated ~628-token zonal corpus show the closed class —
sixty articles, pronouns, prepositions, conjunctions and auxiliaries,
selected by the explicit criterion of appearing in the grammar's
function-word sections — covering 49.2% of running tokens, with
roughly a hundred and twenty-five content lemmas reaching 70% of
content-token coverage. An adversarial review of the first version
found three defects worth recording as method: the corpus
double-counted a cloze test that reproduces its source passages with
content words blanked, inflating the function-word share; the
closed-class set had been curated by intuition rather than by rule,
admitting greetings and ordinary verbs; and the lemmatizer stripped
the class vowels that *are* the citation form, reducing *parla* to
*parl*. A later audit pass found a fourth defect of the same
family: an English design-note blockquote inside a corpus file was
being swept in as RZ text (the corpus convention is that blockquotes
*are* the text), silently diluting the function-word share by four
points — the kind of contamination that flatters nothing and still
corrupts everything downstream. The corrected curves are lower than
the first version's and the extrapolation is gone entirely: at this sample size the fitted Zipf exponent is too
shallow for the tail to be data-determined, so the size of the
95%-coverage lexicon is reported as unknown rather than estimated.
What survives is the shape — half the tokens reachable from one page
of grammar words — and a dividend that was never a corpus quantity
to begin with: an RZ lemma carries about 3.7 exceptionless
recognizable forms against about 20 synthetic forms for a Spanish
lemma — a five-fold reduction in *forms to recognize*, a grammar
fact [D] rather than a measured learning effect — accruing precisely to
the cohorts the zone's cognate transfer does not serve
(docs/design/zonal/rz-lexicon-coverage.md).

Two further explorations extend the same machinery. A
conversation-repair mode adapts aviation's readback protocol —
say-again, correction, confirm, an acrophonic spelling convention
that names letters with words the learner already knows — as seven
frame particles in the same reserved h-region as the number mode,
completing a three-layer error budget: the humility screen
prevents confusions at assignment time, the codebook spaces them
at signal time, and the repair protocol recovers the residue in
conversation. And ordering lessons by parse coverage shows the
zonal design makes a coverage-greedy curriculum actually
teachable: the invariant closed class alone puts roughly half of
running tokens within reach in a first lesson block priced at ~1h
[H — coverage is corpus-measured, the hour axis is a model
estimate], the exceptionless verb table brings the second block
past sixty percent — a curve natural
languages cannot offer because agreement and conjugation force
grammar to interleave with vocabulary, and one that becomes a
design criterion in its own right (a scheme that flattens the
first evening trades against the zonal strategy's strongest
adoption asset).

A companion exploration treats the learner's *errors* as a design
surface in their own right. Scoring the zonal grammar against the
documented top error classes of Romance second-language acquisition
shows seven of fifteen classic traps — grammatical gender,
person agreement, the subjunctive, the preterite–imperfect
distinction, irregular conjugation at scale, question inversion,
false friends — already structurally unmakeable, which is the
regularity dividend restated in error space. For most of the rest
there is a move available only to engineered languages: declare
the learner's most probable deviation grammatical variation rather
than error, at zero cost to the preferred register — single
negation alongside negative concord, article omission as
telegraphic register, optional adjective agreement (spoken French
is the precedent that such variation reads as accent, not
brokenness), free adjective position, a one-clitic rule that
deletes ordering errors instead of regulating them. Each
declaration forgives one first-language family's signature error;
all seven declarations were subsequently adopted as normative
grammar — including the inventory-level merge of *para* into *por*,
deleting the zone's most famous preposition trap outright
(docs/design/zonal/rz-error-absorption.md; rz-grammar.md §10).

Where the zonal language merely *happened* to fit the per-hand
chord space, the greenfield-zonal target can be co-designed with
it: defining its phonotactics as the chord banks themselves (36
onsets, 8 nuclei, 3 glides, 6 codas) yields 5,184 raw syllable
cells, and the humility screen's independently measured ~40%
survival rate lands the usable inventory at ~2,100 — inside the
2,000–3,000 target derived from the donor languages. Three
independently derived quantities close on each other, and typing
becomes an isomorphism rather than an encoding. The co-design also
opens a channel no prior system has: because the designer chooses
which cells survive, the confusion screen can audit the *motor*
graph (chords one directional slip apart) jointly with the
acoustic one — computed on the digit bank [D], where a hill-climbed
assignment places all numerically close digit pairs at motor
distance ≥2 while a naive layout incurs ten violations
(docs/design/gz-chord-fit.md).

The width decision itself generalizes from a binary to a ladder.
Running the same capacity machinery over progressively widened
inventories (diphthong nuclei ai/au/oi; onsets to 19 with v/ʃ/dʒ;
twelve stop–liquid clusters with licensed epenthesis) yields a
lattice of superset variants — GF-N 22 → GF-ND ≥28 → GF-W 38 →
GF-WD ≥48 → GF-C ≥85 humility-safe monosyllabic roots — in which
the digit/mode subsystem, pinned to the narrow ten onsets, is valid
at every rung. Diphthongs compute out as the cheapest capacity on the
board (matching GF-W's syllable count without touching the
10-consonant universal floor), added onsets saturate quickly after
GF-W, and the cluster rung converges on Romance word shapes — the
limit of the ladder is the zonal strategy itself. Width is thus a
position on a single greenfield↔zonal axis, and the open design
decision is which point, or nested pair of points, to commit to
(docs/design/width-ladder.md).

## 10. Related systems

Every load-bearing mechanism here has a precedent that demonstrates
the mechanism *elsewhere* and a failure that locates its limit.
Esperanto demonstrates designed-language learnability (~150–200 hours
to conversational use — a ~B1 bar; the C1 bar runs 300–500h — versus
~600+ for natural Romance languages [TODO-verify @fsi;
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
register bit. Hangul is the standard citation for fast featural-script
decoding acquisition ("learnable in days" [H, TODO-verify]);
Chinese radicals demonstrate semantic-plus-phonetic glyph composition at scale
and, at 30% phonetic reliability, price the cost of letting the mapping
decay. Stenotype proves one-chord-per-unit motor performance (200+ WPM)
and locates its own bottleneck in arbitrary briefs and irregular
orthography — precisely what a regular channel grammar removes. Toki Pona
marks the floor of the inventory-size curve (conversation slows when
paraphrase becomes constant); Ithkuil marks the ceiling: every content
word is grammatically specified for about a dozen dimensions — stem,
version, function, specification, context, and the five categories
bundled into its `Ca` complex — fused for a concision whose spoken
payoff §2 gives reason to doubt, over a phonology sized to pay for that
fusion. Its own revision history, which dropped tone and a third of the
case inventory, is the most direct evidence available that these were
the expensive choices
[@quijada2011; @quijada2023]. Our reading of that failure and the
design forks that avoid it is a hypothesis, not a measurement
(docs/design/alternatives/ithkuil-forks.md); what survives the pass
is the category catalogue, kept as a registry of markable
distinctions alongside the Leipzig and UniMorph conventions
[@leipzig2015; @sylakglassman2016], and a specification-grid
proposal entered on the ledger — as an open question about the
greenfield's scarce root bodies, not yet a price. Solresol's seven notes sit below the articulatory
floor while prefiguring multimodal serialization of one code. ASD-STE100
and aviation English show institutions adopt constrained registers when
reliability wins are legible — the model for this design's safety-critical
register profile.

## 11. Evaluation plan

The design makes falsifiable claims; each maps to a measurable study, and
several run without human subjects. To restate the evidence status: **no
human study below has run — the project has zero external subjects** —
and the two studies that gate the program (the RZ cloze pilot and the
comparative kill-gate) are armed, not scheduled.

**Simulation studies (no subjects, run against the implemented spec):**

- *Channel-noise robustness.* Corrupt syllable streams with an
  L1-parameterized confusion model (e.g. a speaker who realizes /tʃ/ as
  [ʃ]); measure the fraction of errors that are (a) detected by
  lexical-gap and template/segmentation violations (casual layer),
  (b) additionally flagged by the written-layer check (text and careful
  registers), (c) silent word substitutions. Baselines: Esperanto and
  English wordlists under matched noise. Claim under test: humility
  assignment yields fewer silent substitutions per unit of codespace
  than uniform spacing or natural lexicons — supported in simulation
  (§12) under assumed confusion weights, pending calibrated data.
- *Segmentation stress test.* Generate syllable streams with and without
  the prosodic boundary signal degraded; verify the unique-parse property
  holds and measure how gracefully parsing degrades when stress detection
  is unreliable. Claim: SSM parsing needs only local information.
- *Zipf coverage.* With the seed lexicon, compute expected syllables per
  word over a reference corpus frequency distribution; compare against
  Japanese/Hawaiian empirical averages. Claim: mean word length stays
  under ~2 syllables despite the small inventory.

**Human studies (small-N first, pre-registered where feasible):**

- *RZ zero-study cloze pilot (the program's first gate).* Interslavic-
  style 7-word cloze + gist on Romance-L1 readers with zero study,
  against the specified instrument (cloze-test-v0.md). Claim: RZ lands
  in the Interslavic-class comprehension band; RZ currently has NO
  measured number of its own.
- *Comparative kill-gate (precommitted).* Same texts in RZ vs
  Interlingua vs a control (plain Spanish or MT), measuring cloze +
  gist + confidence + reading time + preference, plus a small
  production arm. Precommitment: if RZ does not materially beat the
  best incumbent, stop designing a new Romance standard and redirect
  the measurement/tooling program to the incumbent.
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
supports is the humility policy — under the simulation's assumed
confusion weights, single seed, and assumed POS token-frequency
split — and that the original
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
it is the only direction that attacks the throughput bound itself rather
than routing around it. That framing now needs one correction and one
retreat. The correction: the ~39 bits/s figure is a *read-speech* result
[@coupe2019] and licenses less than we asked of it (§2); reading
converges separately, on its own evidence, and just as hard. The
retreat is larger — the mechanism we assumed, that parallel vision
would perform the relational binding, inverts the psychophysics.
Feature-integration and relational-judgment work find that binding is
precisely what vision does *serially*, one relation at a time. What
survives is Larkin and Simon's locality-of-search argument: a diagram
groups information that is used together and so avoids search, for a
reader who already knows how to read it. And the natural experiment is
unencouraging about the ceiling: signed languages do assign referents
to spatial loci, yet produce roughly half as many signs per second as
English produces words at an identical propositional rate, while a
signed register that drops the spatial grammar halves that rate again.
The spatial machinery buys parity, not surplus. A first structural bake-off has now been run
(`docs/design/spatial-sentence-layer.md`): a deterministic parse of the
grammar (POS coda, particle roles, SSM) into a clause graph, rendered
by five spatial grammars — linear control, referent lanes (x = entity,
the ASL move), role compass, Heptapod-style proposition rings, and a
schema-grid ablation — with diagnostics computed from the placed
geometry. Three results are worth recording, all [M] on the renders and
none of them evidence about cognition. First, the **selection** margin
is real and architectural: referent lanes confine the search for every
mention of an entity to 0.6% of the page against 31.7% for running
text. Second, the intuition that spatial layouts economize by writing
each entity once is **false** once caps, bars and connectors are
counted as marks — marks per proposition is flat across all layouts and
the plain table is lowest. Third, and most usefully, **compactness and
selection trade off directly**: pinning reference to a coordinate costs
roughly a 10× area penalty, while a chain layout that reclaims that
area (1.7× a plain string, clause order and complement attachment
intact) buys essentially no selection, because a chain collapses only
adjacent coreference. The Heptapod ring fails outright — with agent and
patient at opposite angles every share forces collinearity, so the
rings degenerate into a 1-D chain, and rings have no reading order, so
clause order and complement attachment are lost. Whether the layer is a
reading format at all, or a reference/skimming surface beside ordinary
text, is the open question; a behavioural gate (randomized selection,
binding and integration tasks after fixed training, with the
precommitment that the thesis fails unless a spatial condition beats
both the string and the table on accuracy-adjusted response time with a
shallower slope in clause count) has been specified and not run.

## References

[Managed in `references.bib`. Claims imported from the design conversation
are marked TODO-verify until checked against primary sources.]
