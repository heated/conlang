# conlang — engineering languages for learning speed

Can a language be *engineered* the way codes are engineered — so that
an adult learner gets to functional use in a fraction of the usual
time? This project builds two languages to find out, and prices every
design decision in learner-hours.

## Read one of them right now

> Le vento del norte e le sol disputava sobre qui era le plus forte,
> quando un viajator passava, coprite de un manto calde. Les dos
> accordava que le prime a facer le viajator remover su manto seria
> considerate le plus forte.

If you read Spanish, Portuguese, Italian, French, Catalan, or
Romanian — or caught the story through English's Latinate stratum —
you just experienced the effect **RZ** is designed to produce.
(Whether it generalizes across the target zone is unmeasured; the
mechanism is precedented, the number is a hypothesis.) RZ is a
Romance zonal auxiliary language whose words are selected by a
weighted zone-recognizability recipe and screened against false
friends. Start here: **[Read RZ today](docs/rz-start.md)**.

## The two tracks

- **RZ** (`docs/design/zonal/`) — the shipping bet, and a declared
  **profile of Interlingua** (IALA, 1951): Interlingua's grammar and
  lexical base (the normative diff and converter that make that
  inheritance mechanical are pending), a shallow orthography, an
  Ibero-weighted lexicon, a few grammatical deltas (each a falsifiable
  bet, to be tested against the baseline on matched texts), and a set
  of engineered add-ons built as host-neutral patterns
  (`docs/design/zonal/rz-interlingua-profile.md`). Receptive-first:
  designed so the zone reads it at sight. Its 96-form closed function-word
  inventory — 60 forms attested in the current corpus — covers 49.2%
  of its 628 tokens; the curriculum models that block at ~1 hour,
  with the complete verb system arriving by ~2 hours (coverage is
  in-corpus arithmetic; hour estimates are modeled).
- **GZ and the greenfield line** (`docs/spec/`, `docs/design/`) — the
  laboratory. A from-scratch design that treats the syllable as a
  vector of independent channels (onset × vowel × coda) and applies
  coding theory over that space: error-correcting word spacing,
  self-segregating morphology, a featural script whose glyphs are
  their own pronunciation guides, dense closed-domain "modes" for
  numbers/dates/times, and a projected mirrored chording design
  with one syllable per hand — up to two syllables per stroke.

The two tracks are connected by a **mining gate**: every greenfield
mechanism is priced in learner-hours and ported to RZ only if it
survives RZ's naturalistic surface and costs first contact nothing
(`docs/design/zonal/gz-rz-mining-audit.md`). What migration produces
is the generalizable result — a priced menu of *patterns* another
auxiliary-language design can adopt, each needing its own realization
and a fresh price on the new host.

## Evidence discipline

The project's design documents use three evidence labels: **[M]**
measured/computed here, **[D]** derived arithmetic, **[H]**
hypothesis. The project so far has **zero external human
subjects** — corpus numbers are real,
learner-facing numbers are labeled hypotheses until the
pre-registered comprehension studies run. The receptive mechanism is
precedented (Interslavic measured 84% zero-study comprehension in its
zone); RZ's own number is unmeasured. The full accounting instrument
is the learning-budget ledger (`docs/design/learning-budget.md`).

## Map

| you are | start at |
|---|---|
| curious reader | [`docs/rz-start.md`](docs/rz-start.md) — read RZ in ten minutes |
| after the thesis | [`paper/paper.md`](paper/paper.md) — the living research paper |
| a language designer | [`docs/design/zonal/gz-rz-mining-audit.md`](docs/design/zonal/gz-rz-mining-audit.md) + [`docs/design/learning-budget.md`](docs/design/learning-budget.md) — the priced feature menu |
| here for the engineering | [`docs/spec/SPEC.md`](docs/spec/SPEC.md) (greenfield core) · [`docs/design/zonal/rz-chording.md`](docs/design/zonal/rz-chording.md) (chorded input) · [`docs/design/stroke-system.md`](docs/design/stroke-system.md) (script engine) |
| after project structure | [`docs/design/program.md`](docs/design/program.md) (charter) · [`docs/design-brief.md`](docs/design-brief.md) (north star + decisions log) |

Provenance: `docs/archive/` holds the original design conversations.
Issue tracking lives in [beads](https://github.com/steveyegge/beads)
(`.beads/`), not GitHub issues. The project is built by AI agents
under Edward Swernofsky's direction; the receipts culture above is
how that stays honest.

## Status

Active. RZ has a complete v0.2 grammar, a recipe-generated lexicon
with false-friend screening, a multi-register reader pack, a
transactional subset (`rz-lite`), a curriculum with a measured
in-corpus coverage curve, a tentative number mode, and a proposed
repair-mode design. The greenfield line has a v0.2 draft core spec
(not yet frozen), a featural block script with a stroke-based
engine under workshop, and a chording design anchored to published
Velotype/steno data.
Names are intentionally undecided until the phonaesthetics pass;
`conlang`, `RZ`, `GZ` are working handles.
