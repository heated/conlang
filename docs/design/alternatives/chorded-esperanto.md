# Alternative: a chorded Esperanto-like (cut learning time further)

**Status:** exploration (bead conlang-0y7); three-way comparison and
recommendation at the end.

## The pitch

Maybe most of the learning-speed target is reachable without any exotic
machinery: take an Esperanto-like language — full regularity, productive
derivation, and (crucially) **a-posteriori roots that a European-language
speaker half-knows already** — and add the one genuinely separable
insight from the channel project: a **systematic chorded input layer**
over a perfectly phonemic orthography. Esperanto's ~150–200h
track record (against ~600h for French; evidence old and weak, but
directionally robust) is the proven baseline; the bet is that tooling
plus a few surgical simplifications cuts it further, for the population
most likely to show up.

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
priced: **vocabulary is the long pole of language learning.** Grammar
regularity saves tens of hours; acquiring 2,000–3,000 roots costs
hundreds. The channel design's a-priori lexicon makes every root
arbitrary for every learner — maximally fair, and maximally expensive.
Esperanto's Euro-familiar roots give perhaps a 2–3× vocabulary discount
to speakers of European languages (a billion-plus people, and the
realistic early-adopter pool) while giving others nothing.

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
host language." Esperanto can *be* that host: the chord/touch input
engineering, the digit-pair number/date/time modes (as an Esperanto
extension vocabulary), and the trainer app all ship against Esperanto's
existing community as the wedge — while the channel language continues
as the research track sharing the same input-methods codebase. E1 is
then not a rival but the channel project's distribution channel, and
real usage data from it (chord learning curves, mode adoption) feeds the
paper's evaluation section with subjects who already exist.

## Recommendation

Pursue **C**: build the input layer Esperanto-first (E1 scope, no
language reforms — the Ido lesson stands), explicitly as the adoption
wedge and evaluation vehicle for the shared input engineering; keep the
channel language as the research artifact. Reassess after real chord
learning-curve data whether the channel language's from-scratch
vocabulary cost is defensible for its fairness and machine-legibility
wins. This reshapes the input-methods bead (conlang-6sa) into a
two-target deliverable and adds an Esperanto chord-theory work item —
project-shape change, Edward's call (gated with conlang-w77).
