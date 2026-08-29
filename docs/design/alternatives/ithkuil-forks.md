# Ithkuil: a failure diagnosis, the forks that avoid it, and what to steal

**Status:** exploration (lane F, bead conlang-i78 round 2; Edward
2026-08-30 "get to stealing"). Companion deliverable: the construal
namespace (`../construal-namespace.md`).

**Evidence discipline for this document.** Facts about Ithkuil are
cited to the official grammars (Quijada 2011; New Ithkuil, living web
grammar at ithkuil.net). Claims checked against those sources during
the 2026-08-30 Codex review are marked **[V 2026-08-30]**; claims
written from secondary knowledge and *not* verified carry
TODO-verify. **The failure diagnosis in §2 is [H] throughout** — it
is this project's reading of why Ithkuil has no speakers, not a
measured result. Nobody has run a learner study on Ithkuil, so every
causal arrow below is a hypothesis about design, argued from the
design documents and from the revision history.

## 1. What Ithkuil is trying to do

Stated accurately, because the earlier draft of this document got it
wrong. Quijada's stated purpose **is** communication: to convey
cognitive intent with far greater precision and, secondarily,
concision than natural languages, which he treats as tolerating
vagueness, ambiguity and "illusion" [V 2026-08-30 — official FAQ and
introduction, ithkuil.net]. Ithkuil is explicitly designed as a
**spoken human language**, though for specialised rather than
ordinary use; it is an exercise in what a maximally precise language
would look like, not a proposal that anyone adopt it. Quijada has
been consistent that it is not intended as an auxiliary language and
that fluent speech is not expected.

Three design commitments follow, and they are what §2 examines:
precision expressed grammatically rather than left to periphrasis;
concision, so that the precise form is not merely as short as the
natural-language paraphrase but shorter; and a category inventory
drawn from cognitive linguistics (Lakoff, Langacker, Talmy) rather
than from any language's traditional grammar.

The commonly repeated outcome — that no one, including the designer,
speaks it fluently — is consistent with everything published, but we
found no source in which Quijada states he accepted that as a price,
so the motive attributed to him in the earlier draft is withdrawn.

## 2. The diagnosis [H]

Four design decisions, each verifiable as a *fact about the design*,
which this project believes jointly explain the outcome. The facts
are cited; the causal claim is ours and unmeasured.

| | design fact | why we think it costs [H] |
|---|---|---|
| **R1** | A large mandatory core per word. The 2011 standard formative has **15 slots**; the New Ithkuil formative has **10** [V 2026-08-30 — official morphology chapters]. Not every category is obligatory — both grammars have optional, conditional and adjunct-borne categories, and New Ithkuil deliberately shrank the mandatory core — but a speaker still fills several independent semantic choices to utter any content word | a per-word **selection cost**: composing a word means resolving several decisions the speaker may not have formed an opinion about. This is a production cost no encoding removes, and it is our best candidate for why composition stays slow even for people who know the tables |
| **R2** | Fusion for concision: the `Ca` complex encodes Configuration + Affiliation + Perspective + Extension + Essence in one consonant complex [V 2026-08-30]. It is **systematically assembled** with documented allomorphy and substitution rules — not the pure lookup table the earlier draft claimed | the form is still not transparently decomposable by ear at speed, and a dense assignment leaves little acoustic slack between neighbouring category combinations. Whether real mishearings land on valid forms is **unmeasured** — the coding-theoretic claim in the earlier draft is withdrawn pending a confusion analysis |
| **R3** | A phonology sized to pay for R2: 2011 used ~45 consonants, 13 vowels and 7 tones; New Ithkuil dropped tone and cut the consonant inventory [V 2026-08-30] | no L1 covers that inventory, and the densest channels (tone, voicing series, clusters) are the ones humans discriminate worst under noise. That the 2023 revision cut exactly these is the strongest evidence for the diagnosis |
| **R4** | A category set expanded from theory: 96 cases (2011) → 68 (New Ithkuil); 32 → 36 aspects; 9 phases; 9 valences; 61 biases [V 2026-08-30]. No corpus, learner data, or usage frequency informed the inventory | a generator with no pruning function. The long tail of distinctions costs learning time at the same rate as the head while carrying a fraction of the use. Same failure class as Wilkins 1668 |

**The premise underneath R2/R3.** The concision drive assumes that
denser encoding buys communicative throughput. The best available
evidence weakens that assumption without settling it: Coupé et al.
(2019) measured *read* speech across 17 natural languages and found
information rate clustering near a mean of ~39 bit/s, with denser
syllabic encodings spoken proportionally slower [@coupe2019]. That
is a robust cross-linguistic regularity in a controlled task — it is
**not** a demonstrated universal ceiling, not a proven one-for-one
compensation mechanism, not a measurement of spontaneous
conversation, and not a result about constructed languages, whose
speakers are all L2 learners composing deliberately. Their
information measure is also not the same object as "explicitly
marked semantic distinctions." So the honest statement is: *the
expected return on spoken concision is small and may be zero* [H],
which is enough to make R2/R3 a bad trade against their costs, and
not enough to call the compression pointless. **The same caveat
applies to this project's own paper §2, README, and design brief,
which state the result more strongly than it supports** — filed as
bead conlang-81l.

**What Ithkuil got right** (any fork must preserve these): the
category catalogue (→ namespace doc); the root × Stem ×
Specification lexical grid as a *derivational* device; a unified
role-marking system that replaces prepositions and subordinating
conjunctions at once; grammaticalised evidentiality (unremarkable —
Quechua and Tuyuca do it); and "the script encodes categories, not
sounds," which is our featural-block insight arrived at
independently.

## 3. The forks

One per root decision, plus what they unlock. Each: what changes,
what it avoids, what it costs, precedent.

**F1 — optional marking with silent defaults** (addresses R1). Every
category gets a zero form that is *absent from the surface*, not a
default morpheme occupying a slot, so the language is a strict
superset of a plain one. Cost: the "forced clarity" thesis —
recoverable as a **register** in which unmarked forms are illegal
(ASD-STE100 precedent). Stated carefully: obligatory explicit
marking imposes some production cost on every utterance; optionality
is *this project's preferred* way not to levy it. It is not the only
mitigation — defaults, contextual licensing, syncretism,
lexicalisation, underspecification, and plain automatisation with
practice all reduce the conscious choice, and a fluent speaker's
cost is not a beginner's.

**F2 — agglutinate; compress in the script** (addresses R2; R3 falls
out). One morpheme, one meaning, one consistent shape per category.
Words lengthen in speech, which per §2 is a small or zero real cost;
compress in the written serialisation only (our decoupled-script
move). Avoids codebook-style learning, restores decomposability, and
lets morpheme templates make many mishearings land on non-words.
Precedent: Quechua carries evidentiality, aspect and object
agreement agglutinatively and is acquired normally. *F2′ —
structured fusion*: if fusing, make the fused form computable, each
category contributing one phonetic feature (a product code, not a
codebook — the spoken analogue of a featural script). Ceiling
plausibly ~3–4 orthogonal features per segment before R3 returns
[H, unverified].

**F3 — scope-sort the categories** (also addresses R1). Clause-level
categories (Illocution, Validation, Mood, Bias) → one particle
complex per clause (Lojban's attitudinals); phrase-level → optional
modifiers; word-level → a small residue. Per-word load drops to what
genuinely varies per word. New Ithkuil's adjuncts move this way.

**F4 — frequency-prune the category set** (addresses R4). Zipf
applied to grammar: annotate a corpus for the construal distinctions
speakers actually make, grammaticalise the head, push the tail to
lexicon and periphrasis. The catalogue survives *as a catalogue*
(→ namespace doc). The obvious quantitative version of this — "a
small number of cases covers most role-marking" — is folklore until
someone measures it; stating a threshold requires naming the
languages, corpora, and unit of analysis first, so no number appears
here (bead-able as a preregistered corpus question).

**F5 — exact in writing, projective in speech.** Written form: every
category marked, maximally compact (Ithkuil's script, kept). Spoken
form: a lossy projection with silent defaults, context-recoverable,
human-floor phonology. Reading is exact; speech is good-enough and
repairable. Chinese does a weak version; our four-projections
architecture is the strong version. Ithkuil had both layers carrying
everything, so the script's compactness bought nothing the speech
did not already pay for.

**F6 — design the redundancy in** (addresses R2's fragility). Leave
the morphological code *sparse*, so single-feature errors tend to
land on invalid forms (our humility rule and sparse digit codebook),
or use **concord as parity** — mark clause-level categories twice
(verb + clause particle) so a mismatch is detectable (cf.
conlang-int, the absorption/parity dial).

**F7 — lexicon from usage, not taxonomy.** Keep the Stem ×
Specification grid, populate it demand-driven by translating texts,
and consider a-posteriori roots for the mnemonic hook. The Esperanto
compromise — the one auxlang lexicon that got learned at scale.

**F8 — onion release.** A Toki-Pona-sized core (a handful of
categories, silent defaults elsewhere) that is a strict subset of
the full grammar, with every further category an add-on in a
reserved slot. Usable in a week, grows into precision. Our
expansion-compatible-family idea (SPEC §9) applied to grammar
instead of phonology.

**F9 — a testing loop from year one.** Ithkuil ran two decades
without learner data. New Ithkuil was developed with community
involvement [V 2026-08-30] and the revision cut tone and 28 cases —
consistent with the loop working, though we have no source showing
the community process *caused* those specific cuts, so this is
suggestive, not evidence.

**F10 — reframe: a notation, not a language.** Precision of construal
does not require speakability. **Ithkuil-as-notation**: a
written-only annotation layer (mathematical-notation class), which
drops the phonological constraint entirely and opens non-linear
layout (UNLWS-class) — possibly the only medium in which a dozen
categories per node is readable. **Ithkuil-as-host-layer**: the
categories as a small particle set usable *inside* an existing
language (§6; illustration only, not a project deliverable — Edward
2026-08-30).

### Four coherent alternative Ithkuils

| bundle | forks | keeps | gives up |
|---|---|---|---|
| **Ithkuil-A** (agglutinative) | F1 F2 F6 + human-floor phonology | the category set, evidentiality, the grid lexicon | spoken concision (small or zero real value per §2) |
| **Ithkuil-W** (written-exact) | F5 F2 F6 | the script and its compactness where compactness pays; "everything explicit" in text | spoken precision — speech becomes projective and repairable |
| **Ithkuil-L** (layered) | F1 F3 F4 F8 F9 | an on-ramp; precision opt-in; plausibly learnable | "everything always marked"; most of the case and aspect tables move to the lexicon |
| **Ithkuil-H** (host-layer / notation) | F10 (+F4) | precise construal as a tool inside existing languages, or as a 2D notation | being a language at all |

**The counterfactual, stated as ours rather than his:** *if* the
objective were compact written construal rather than a spoken-language
demonstration, Ithkuil-W is the design that follows — the script is
the component whose value survives every criticism above, and the
phonology is where the costs concentrate. That is a preference of
this project, not a correction of Quijada, whose goal was a spoken
language and who is entitled to it. Whether the script "worked"
while the speech "failed" has no operational success criterion; the
weaker and defensible version is that the script's costs are
demonstrably lower.

### What no fork fixes

- Obligatory explicit marking costs something per utterance;
  optionality relocates the cost rather than abolishing it (you now
  decide *whether* to mark).
- Precision versus vagueness is a real trade. Vagueness does work —
  politeness, honest ignorance, Gricean economy — so a language
  where saying less is ungrammatical fights pragmatics.
- The Whorfian payoff is unmeasured for every bundle, and nothing
  here should be read as claiming one.

## 4. Steal verdicts (the mining gate, GZ side)

| mechanism | verdict | where it lands |
|---|---|---|
| **Specification as a derivational channel** (basic / contential / constitutive / objective per root) | **STEAL — price it.** Attacks GZ's monosyllabic-root scarcity by reducing semantic pressure per root body. Open, and load-bearing: the full Stem × Specification grid is up to 16 cells with root-specific content, not one four-way rule; and every spoken distinction needs an exponent the phonology has not budgeted (the coda is spent on POS) | bead conlang-czq; ledger row PROPOSED |
| **The category catalogue as a reference namespace** | **STEAL — as instrument, not language feature**: a registry so ledger rows, toolkit entries and glosses can name *what* a feature marks with a stable ID | `../construal-namespace.md`; bead conlang-ma1 |
| **Validation (evidentiality)** as an optional clause-particle set | **CATALOGUE; candidate for GZ's careful/safety register** (Tier-3 evidentials were already on the brief). No new bead | namespace, EVID row |
| **Configuration** as an optional nominal channel | **CATALOGUE; cheap pilot candidate for GZ** — a distinction Romance and English both lack; value unproven; never obligatory | namespace, CFG row |
| **Bias / attitudinal layer** | **DECLINE for design; NOTE as precedent** — text lost the affect channel and users grew a marker set for it without a designer (§6) | §6 |
| **The case / aspect / phase / valence tails** | **DECLINE.** Catalogue only | namespace |
| **Lookup-heavy fusion, tone as a grammatical channel, a large mandatory core** | **DECLINE — the warnings the brief already carries** (R1–R3) | design-brief steal list |
| **Ithkuil-W as an architecture** | **already ours** — the written-layer check bit, mode anti-check marking, and the R3 citation register (conlang-pgh) are Ithkuil-W moves | — |

## 5. Pointer: the catalogue

Ithkuil's durable value to this project is *nominal* — it names
distinctions carefully. The inventory, with stable IDs and explicit
source/mapping provenance, lives in
`docs/design/construal-namespace.md`.

## 6. Illustration only: what a host layer would look like

Not a deliverable (Edward 2026-08-30: "don't need it in GZ or
anything"). Kept because it is the clearest picture of F10 and of
why some categories port into a host language and others do not.

Take the dimensions the host lacks a compact form for, give each an
optional short tag, scope it to the clause, allow stacking, and let
the unmarked form mean nothing-claimed. English has no grammatical
evidentiality, no representative/real distinction, and no set-shape
marking; it handles degree, illocution and most aspect adequately,
so those do not port.

```
plain:   The bridge is closed.
EVID:    The bridge is closed [saw].     I have direct evidence
         The bridge is closed [told].    reported to me
         The bridge is closed [infer].   inferred (the road is empty)
         The bridge is closed [assume].  assumed by convention
ESS:     The bridge is closed [as-if].   in the plan / the film / the drill
CFG:     tree [one] / tree [set] / tree [mix] / tree [mass]
         = a tree / a grove / a mixed stand / forest
stack:   They cancelled it [told][as-if]?
```

Two observations, stated at the strength the evidence supports.
First, host layers for a genuinely missing channel do get adopted
without anyone designing them: online writing grew a set of
affect/intent markers (`/s`, `/j`, `/srs`, `/gen`) after plain text
proved unable to carry tone. We have not checked the origin,
inventory, or adoption path of that set, so it is offered as an
existence example, not as evidence for a mechanism [TODO-verify].
Second, the evidential slot is the one with real natural-language
support: Latin-American Spanish and Portuguese *dizque* / *diz que*
is a well-described reportative marker, while Italian *pare* and
Spanish *parece* are verbs with epistemic/evidential readings rather
than particles — the construction, not the word, does the work
[TODO-verify dialect and construction detail].

What the sketch shows about the forks: only F1 (optional), F3
(clause-scoped) and F4 (pruned to the host's actual gaps) survive
contact with a host language. Fusion, a mandatory core, and a
bespoke phonology are all incompatible with living inside someone
else's grammar.
