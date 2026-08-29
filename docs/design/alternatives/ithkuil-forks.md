# Ithkuil: the dead ends, the forks that avoid them, and what to steal

**Status:** exploration (lane F, bead conlang-i78 round 2; Edward
2026-08-30 "get to stealing"). Companion deliverable: the construal
namespace (`../construal-namespace.md`). Evidence labels as
elsewhere: [M] measured, [D] derived, [H] hypothesis. Facts about
Ithkuil are from the published grammars (Quijada 2011; New Ithkuil
2023) and are marked TODO-verify where a count is version-dependent.

## 1. What Ithkuil is trying to do

Quijada's goal is not communication but **overt construal**: a
language whose grammar requires the speaker to say, explicitly and
compactly, everything a natural language lets ride as vagueness —
set shape, boundary, evidence, intention, goal-attainment, stance.
Three commitments follow: (1) semantic precision as an obligation,
not an option; (2) *concision* — the precise form must be shorter
than the natural-language paraphrase, not merely as precise; (3)
categories chosen from the cognitive-linguistics literature (Lakoff,
Langacker, Talmy) rather than from any language's grammar. He
accepted the consequence — no fluent speaker, himself included — as
the price of a proof of concept about the design space.

## 2. Four root decisions, one false premise

The symptoms (unpronounceable, unlearnable, no speakers, three
revisions over twenty years) trace to four decisions:

| | decision | consequence |
|---|---|---|
| **R1** | every category obligatory (~20 slots per formative) | per-word *selection* cost — ~20 decisions per word, most about things the speaker does not care about. A working-memory cost; no encoding fixes it |
| **R2** | lookup-fusion for concision (e.g. the `Ca` cluster encodes Configuration + Affiliation + Perspective + Extension + Essence in one consonant cluster via a table) | forms not decomposable by ear; learning = memorising codebooks; **zero redundancy** — every table cell is a valid form, so any mishearing is a different valid word |
| **R3** | phonology inflated to pay for R2 (2011: ~45 consonants, 13 vowels, 7 tones; 2023 dropped tone and cut consonants — TODO-verify counts) | no L1 covers it; the densest channels (tone, voicing series, clusters) are the ones humans hear worst |
| **R4** | categories chosen from theory, never pruned by use (96 → 68 cases, 32 → 36 aspects; no corpus, no speaker, no frequency data for two decades) | feature accretion with no pruning function; the long tail of distinctions costs as much per word as the head |

Underneath R2/R3 sits a **false premise the brief already names**:
spoken concision buys nothing. Information rate in speech converges
near ~39 bits/s [@coupe2019]; denser syllables are spoken
proportionally slower. A fluent Ithkuil speaker would talk very
slowly at English's bits/s. Its entire compression drive chased a
fixed quantity in the wrong channel — while its *script*, which was
already more compact than its speech, sat in the channel where
compactness pays (skimming, density, machine legibility).

**What Ithkuil got right** (any fork must preserve these): the
category catalogue itself (→ namespace doc); the root × Stem ×
Specification lexical grid (derivation as a matrix); a unified
role-marking system replacing prepositions *and* subordinators;
obligatory evidentiality (fine in Quechua/Tuyuca); "the script
encodes categories, not sounds" — our featural-block insight,
arrived at independently.

## 3. The forks

One per root decision, plus the ones they unlock. Each: what
changes, what it avoids, what it costs, precedent.

**F1 — optional marking with silent defaults** (fixes R1). Every
category gets a zero form that is *absent from the surface*, not a
default morpheme occupying the slot. Ithkuil becomes a strict
superset of a plain language. Avoids the selection cost. Costs the
Whorfian "forced clarity" thesis — recoverable as a **register**
where unmarked forms are illegal (ASD-STE100 precedent). This is the
fork that matters: *the selection cost of obligatory precision is
intrinsic; only optionality removes it.* Quijada faced exactly this
trade and chose the thesis over the users.

**F2 — agglutinate; compress in the script** (fixes R2; R3 falls
out). One morpheme, one meaning, one consistent shape per category.
Words lengthen in speech, which per §2 costs nothing real; compress
in the written serialisation only (our decoupled-script move).
Avoids codebook memorisation, non-decomposability, zero redundancy
(morpheme templates make mishearings land on non-words), and the
phonology inflation. Precedent: Quechua carries evidentiality,
aspect and object agreement agglutinatively and is acquired
normally. *F2′ — structured fusion*: if fusing, make the fused form
computable — each category contributes one phonetic feature to the
segment (a product code, not a codebook; the spoken analogue of a
featural script). Ceiling ≈ 3–4 orthogonal features per segment,
some perceptually weak, so it buys ~3 binary categories per slot
before R3 returns.

**F3 — scope-sort the categories** (also fixes R1). Clause-level
categories (Illocution, Validation, Expectation, Mood, Bias) → one
particle complex per clause (Lojban's attitudinals); phrase-level →
optional modifiers; word-level → a small residue. Per-word load
drops to what genuinely varies per word. New Ithkuil's adjuncts are
a late move here.

**F4 — frequency-prune the category set** (fixes R4). Zipf applied
to grammar: annotate a corpus for the construal distinctions
speakers *actually* make; grammaticalise the head, push the tail to
lexicon/periphrasis. ~8 cases cover ~95% of role-marking in any
language [H — verify against a case-language corpus]; those get
morphology, the other 60 become adpositions. The catalogue survives
*as a catalogue* (→ namespace doc). Same failure class as Wilkins
1668: a generator with no pruning function.

**F5 — exact in writing, projective in speech** (the throughput
resolution). Written form: every category marked, maximally
compact (Ithkuil's script, kept). Spoken form: lossy projection with
silent defaults, context-recoverable, human-floor phonology.
Reading is exact; speech is good-enough and repairable. Chinese does
a weak version; our four-projections architecture is the strong
version. Ithkuil had both layers carrying everything, so the
script's compactness was wasted.

**F6 — design the redundancy in** (fixes R2's fragility). Leave the
morphological code *sparse* so single-feature mishearings land on
invalid forms (humility rule / sparse digit codebook), or use
**concord as parity** — mark clause-level categories twice (verb +
clause particle) so mismatch is detectable (cf. conlang-int, the
absorption/parity dial).

**F7 — lexicon from usage, not taxonomy.** Keep the Stem ×
Specification grid (good), populate it demand-driven by translating
texts, and consider a-posteriori roots for the mnemonic hook. The
Esperanto compromise — the one auxlang lexicon that got learned.

**F8 — onion release.** A Toki-Pona-sized core (five categories,
silent defaults elsewhere) that is a strict subset of the full
grammar; every further category an add-on in a reserved slot.
Usable in a week; grows into precision. Ithkuil's day one required
the full matrix, which is why there was no day two. Our
expansion-compatible-family idea applied to grammar.

**F9 — a testing loop from year one.** The kill signal was
available in ~1990: *the designer cannot speak it.* New Ithkuil
(2023) ran the loop belatedly and immediately dropped tone and 28
cases — evidence the loop works and that R3/R4 would have fallen
decades earlier with it.

**F10 — reframe: a notation, not a language.** The construal goal
never needed speakability. Two limits: **Ithkuil-as-notation** — a
written-only annotation layer for thought (mathematical-notation
class), which removes the phonological constraint entirely and opens
non-linear layout (UNLWS-class), possibly the only medium where 20
categories per node is readable; and **Ithkuil-as-host-layer** —
the categories as a small particle set usable *inside* English or
any host language (sketch in §6; illustration only, not a project
deliverable — Edward 2026-08-30).

### Four coherent alternative Ithkuils

| bundle | forks | keeps | gives up |
|---|---|---|---|
| **Ithkuil-A** (agglutinative) | F1 F2 F6 + human-floor phonology | full category set, evidentiality, grid lexicon | spoken concision (illusory anyway) |
| **Ithkuil-W** (written-exact) | F5 F2 F6 | the script and its compactness where it matters; "everything explicit" in text | spoken precision — speech becomes projective and repairable |
| **Ithkuil-L** (layered) | F1 F3 F4 F8 F9 | a real on-ramp; precision opt-in; learnable | "everything always marked"; ~85% of the case/aspect tables move to the lexicon |
| **Ithkuil-H** (host-layer / notation) | F10 (+F4) | the cognitive goal, as a tool inside existing languages or a 2D notation | being a language at all |

Given the stated goal (cognitive precision, not communication), the
one Quijada should have built is **Ithkuil-W** or its notation
limit: the script was the part that worked, speech the part that
failed, and the goal never needed speech.

### What no fork fixes

- The selection cost of obligatory precision is intrinsic; F1
  removes the obligation, not the cost of choosing when you do
  choose.
- Precision vs vagueness is a real trade. Vagueness does work
  (politeness, honest ignorance, Gricean economy); a language where
  saying less is illegal fights pragmatics. The humane version marks
  *over*-specification as the unusual move.
- The Whorfian payoff is unmeasured for every bundle.

## 4. Steal verdicts (the mining gate, GZ side)

| mechanism | verdict | where it lands |
|---|---|---|
| **Root × Stem × Specification grid** — 3–4 specifications (basic / content / form / object) per root as a derivational channel | **STEAL — price it**: directly attacks GZ's 22-root-body bottleneck without touching phonology; the open questions are where the marker lives (coda? derivational syllable? script-only?) and how it composes with gf-grammar's O/A/P/R alternation classes, which already cover part of Function/Specification | bead conlang-czq |
| **The category catalogue as a reference namespace** | **STEAL — as instrument, not language feature**: an IPA-like registry so ledger rows, toolkit entries and glosses can say *what* a feature marks with a stable ID | `../construal-namespace.md`; bead conlang-ma1 |
| **Validation (evidentiality)** as an optional clause-particle set, ~6 values | **CATALOGUE; candidate for the GZ careful/safety register** (Tier-3 evidentials were already on the brief) — no new bead; the namespace entry is the deliverable | namespace §EVID |
| **Configuration** (uniplex / duplex / multiplex-similar / -dissimilar / -fuzzy) as an optional nominal channel | **CATALOGUE; cheap pilot candidate for GZ** — a distinction Romance and English both lack; value unproven; never obligatory | namespace §CFG; folded into the grid bead as a note |
| **Bias / tone-indicator layer** | **DECLINE for design; NOTE as precedent** — the internet grew one organically (`/s /j /srs /gen`); the lesson is that host layers *do* get adopted when they fix a real channel loss (affect in text), and that the organic set is the one to study, not replace | §6 |
| **68 cases / 36 aspects / 9 levels / 9 phases / 9 valences** | **DECLINE**: the tail. Catalogue only | namespace |
| **Lookup-fusion (`Ca`-style codebooks), tone as a grammatical channel, obligatory marking** | **DECLINE — these are the warnings the brief already carries** (R1–R3) | design-brief steal list |
| **Ithkuil-W as an architecture** | **already ours** — GZ's written-layer check bit, mode anti-check marking, and the R3 citation register (conlang-pgh) are Ithkuil-W moves; no new work | — |

Ledger: one proposed row (the grid) in `learning-budget.md`, not
bought. Paper touch: §10.

## 5. Pointer: the catalogue

The value of Ithkuil to this project is mostly *nominal* — it names
distinctions. The full category inventory, with stable IDs and
cross-references to the Leipzig/UniMorph standards, lives in
`docs/design/construal-namespace.md`.

## 6. Illustration only: what Ithkuil-as-host-layer would look like

Not a deliverable (Edward 2026-08-30: "don't need it in GZ or
anything"). Kept here because it is the clearest picture of F10 and
of why some categories port into a host and others do not.

The move: take the ~3 dimensions a host language lacks compact forms
for, give each a one-syllable optional clause particle (speech) or
short tag (text), scope = the clause, stackable, silent default =
unmarked. English lacks grammatical **evidentiality**, **essence**
(real vs represented), and **configuration** (set shape); it has
adequate **level**, **illocution**, and most **aspect**, so those
stay lexical.

```
plain:      The bridge is closed.
+EVID:      The bridge is closed [saw].        observational
            The bridge is closed [told].       reportive
            The bridge is closed [infer].      inferential (the road's empty)
            The bridge is closed [assume].     conventional/presumptive
+ESS:       The bridge is closed [as-if].      representative: in the film / in the plan
+CFG:       tree [one] / tree [set] / tree [mix] / tree [mass]
            = a tree / a grove / a mixed stand / forest
stacked:    They cancelled it [told][as-if]?   "so the story goes, hypothetically?"
```

Spoken forms would be a-posteriori in a Romance host — Latin-
American Spanish and Portuguese already have a reportive particle
(*dizque* / *diz que*), Italian and Spanish an inferential (*pare* /
*parece*) — and the tone-indicator set (`/s /j /srs /gen`) is the
existence proof that a text-channel host layer for a missing
category gets adopted without anyone designing it. What the sketch
shows about the forks: only F1 (optional), F3 (clause-scoped) and
F4 (pruned to the host's gaps) survive contact with a host; every
other Ithkuil commitment is incompatible with living inside someone
else's grammar.
