# Alternative: a chorded Esperanto-like (cut learning time further)

**Status:** exploration (bead conlang-0y7), revised after adversarial
review (Fable: SOUND-WITH-CAVEATS; caveats folded in below and marked).

## The pitch

Maybe most of the learning-speed target is reachable without any exotic
machinery: take an Esperanto-like language — full regularity, productive
derivation, and (crucially) **a-posteriori roots that a European-language
speaker half-knows already** — and add the one genuinely separable
insight from the channel project: a **systematic chorded input layer**
over a perfectly phonemic orthography. Esperanto's ~150–200h
track record (against ~600h for French; evidence old and weak, but
directionally robust) is the working baseline [H — and a ~B1 bar;
C1 runs 300–500h per the ledger]; the bet is that tooling plus a few
surgical simplifications cuts it further, for the population most
likely to show up.

## Why chording fits Esperanto unusually well

Steno's 2–4-year learning curve comes from arbitrary briefs and
English's non-phonemic spelling — neither exists here. Esperanto is
agglutinative with crisp morpheme boundaries, a small closed affix set,
and spelling that is exactly pronunciation. A chord theory can therefore
be **fully systematic**: phonemic strokes for roots (multi-key onset
banks absorb Esperanto's clusters), dedicated chord real estate for the
closed morphology (-o/-a/-e/-j, tense vowels, mal-, -in-, -ul-, …), one
to two strokes for most words, zero memorized briefs. Nothing like this
ships today — the Plover ecosystem has no mainstream Esperanto theory —
so the niche is open, and the artifact is useful to an existing
community of speakers from day one.

## Two sub-options

- **E1 — strict Esperanto, input layer only.** Zero language design; a
  pure tooling project (chord theory + dictionaries + trainer app,
  desktop and phone). Rides the existing community, corpus, Duolingo
  pipeline. Shippable and testable on real speakers in weeks.
- **E2 — "Esperanto-prime."** The 3–5 highest-value simplifications from
  the design chat (drop the mandatory accusative and adjective
  agreement, tame the worst clusters/ĥ, keep the correlative grid).
  Cleaner, but it forks the community — the Ido lesson says reforms
  historically cost more adoption than their design value returns.

## Honest comparison with the channel-coded design

The uncomfortable observation the original design conversation never
priced: **vocabulary is plausibly the long pole of language learning.**
Grammar regularity saves tens of hours; acquiring 2,000–3,000 roots
costs hundreds. [Review caveat: directionally supported by vocabulary-
acquisition research but uncited here — needs proper grounding before
this drives a decision.] The channel design's a-priori lexicon makes
every root arbitrary for every learner — maximally fair, and maximally
expensive. Esperanto's roots give a large vocabulary discount to
speakers of European languages — but the discount is a steep gradient,
not a constant: the root stock skews Romance, so Spanish/French/Italian
speakers get far more for free than German, English, or especially
Slavic speakers, and everyone else gets little beyond international
scientific vocabulary. [Concrete next step, per review: score cognate
transparency over the ~2,500 official roots against several major L1s
instead of hand-waving a 2–3× figure.]

| | channel-coded (current) | chorded Esperanto-like |
|---|---|---|
| grammar acquisition | excellent (fully regular) | excellent (fully regular) |
| vocabulary, European-language L1 | slow (all roots arbitrary) | **fast (roots half-known)** |
| vocabulary, other L1 | slow, but equal for everyone | slow |
| phonology accessibility | **engineered for any L1** | clusters, r, ĥ — European-tilted |
| script/decoding | featural, self-teaching, but new | Latin, phonemic — zero cost for Latin users |
| chorded/phone input | derived from channel structure | systematic theory, no briefs — comparable |
| machine parseability | engineered (SSM, frame grammar) | none (natural-grade ambiguity) |
| error correction | modes + emergent (see no-parity note) | emergent only; modes **could be added** |
| community/corpus/materials | zero | **large and alive** |
| testability of learning claims | requires building learners | measurable on real Esperantists now |
| research novelty | high | modest (engineering contribution) |

The two designs optimize different objectives that the project brief
currently conflates: *fastest for anyone on Earth* (fairness constraint
→ channel design) versus *fastest for the people who will actually show
up* (adoption-weighted → Esperanto-like). That is a values call, not an
engineering call.

## The hybrid worth taking seriously (option C)

The Tier-2 adoption strategy was always "ship pieces that work inside a
host language." Esperanto could *be* that host: the chord/touch input
engineering, the digit-pair number/date/time modes (as an Esperanto
extension vocabulary), and the trainer app all ship against Esperanto's
existing community — while the channel language continues as the
research track sharing the same input-methods codebase.

Review-imposed honesty about C: (1) the "evaluation vehicle" claim is
mostly false — Esperanto chord data validates the chord-learning-curve
study and almost nothing else in the paper's §11 program (decoding,
digit span, mishearing studies all need the channel language itself);
(2) C roughly doubles project scope while deferring the values question,
and its "reassess later" step is structurally rigged against the
research track (the Esperanto side accrues users and momentum while the
channel side accrues only spec); (3) the brief's existing wedge — modes
and input methods hosted in *English* — was never compared against the
Esperanto host, and English hosting reaches strictly more people.

## Recommendation (revised)

Hold **C** to explicit terms before adopting it: a host comparison
(Esperanto vs English as the wedge's host language) on reach, community
receptivity, and engineering delta; the cognate-transparency scoring to
replace the guessed discount; and pre-committed exit criteria for the
reassessment so the research track cannot be starved by default. E2
(reforming Esperanto) stays rejected on the Ido precedent. Without
those terms, the safe default is the brief's original strategy: one
language, with modes and input methods wedging inside English.
Project-shape change either way — Edward's call (gated with
conlang-w77).
