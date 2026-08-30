# RZ is an Interlingua profile — decision record (conlang-wan, 2026-08-30)

**Decision (Edward, 2026-08-30, on the agent's recommendation):** RZ
is declared a *profile* of Interlingua — and, as of this writing, is
*migrating to* one: the normative artifact (rz-grammar.md restated as
a diff against Gode & Blair, plus a canonical delta registry) does not
exist yet, so the enumerations below are the current best list, not a
closed one. RZ is a shallow-orthography,
Ibero-weighted variant that inherits Interlingua's grammar and
lexical base and adds a set of deltas — surface bets, host-neutral
patterns, and RZ-specific artifacts (§2 below) — rather than a fourth
Romance fork beside Interlingua, Neolatino and LFN.

## Why

`conlang-wan` established that RZ is ~80–85% Interlingua at the
grammar level, and *literally* shared rather than merely similar:
`le/un` articles, `-e` adjectives (*calde, forte, prime, nove, tote,
multe, iste, mesme, nostre*), `-te` participles, person-invariant
verbs with obligatory subject pronouns, no gender / case /
subjunctive, `plus` / `le plus`, the whole `-itate / -mente / -al /
-or / -ista / -ia / -bile / re- / des- / in-` derivation family,
`io / tu / nos / vos`, `es / era / va`, the `-va` past, near-identical
weekdays and months.

A fourth fork is the pathology `romance-zonal-v0.md` §7 (item 5)
warns against, and it throws away the one thing no new Romance
auxlang can build in under a decade: Interlingua's 27k-entry
dictionary [@gode1951], its grammar [@godeblair1951], a Wikipedia
edition, and seventy years of periodicals. The profile framing keeps
all of that reachable and matches what the project's contribution
actually is (paper §9b): not a language, but a method, a set of
host-neutral add-on patterns, simulation results about assignment and
repair in an inherited lexicon, and an instrument — applied to
Interlingua as the baseline.

## What "profile" means, concretely

1. **Base = Interlingua (IALA 1951).** Where RZ has not stated a
   difference, the Interlingua form and rule are RZ's — once the
   grammar in `rz-grammar.md` has been restated as a *diff* against
   Gode & Blair (bead conlang-5i1.4). Until that restatement exists,
   the standalone grammar is the spec and "unstated = Interlingua"
   is an intent, not a rule anyone can apply.
2. **The deltas are enumerated in three classes.** They are NOT all
   priced: the ledger currently has rows for the add-ons only, and the
   surface deltas are **UNPRICED [H]**. Pricing them is open work; no
   qualitative stand-in is acceptable, since unpriced-but-adopted is
   exactly the failure the ledger method exists to prevent.
   - *Surface deltas* (change how inherited text looks/reads):
     shallow orthography (`-cion` for `-tion`, no Greek digraphs, no
     double consonants); Ibero lexical weighting (*dos/cuatro/cinco/
     ses/sete/nove; en/por/sobre/necun/aquel/altre* for IA *in/pro/
     super/nulle/celle/altere*); adjective number agreement + `les`;
     analytic future `va` + inf and `-ria` conditional for IA's
     synthetic `-ra/-rea`; negative concord; the `es`/`sta` split;
     `tener`-perfect and `sta`-progressive. **Every one of these is a
     bet that it improves zone comprehension over the baseline, and
     every one is falsifiable by the kill-gate (x6t).** If it does
     not pay, it reverts to the Interlingua form. The same treatment
     applies to any lexicon repair that changes inherited forms
     (conlang-ui7): it is a surface delta, not an invisible add-on,
     and it faces the surface gate.
   - *Host-neutral patterns* (leave ordinary baseline prose
     untouched): closed-class discipline, the error-absorption
     method, the number mode and the frame-particle machinery behind
     the deferred date/time/coord modes, the conversation-repair
     register, chording, the display script, the coinage screen, the
     defining-vocabulary discipline, the spoken reference standard.
     These are the toolkit (program lane E). They are **conditional
     patterns, not drop-in artifacts** — program.md's own definition
     — and running them on unprofiled Interlingua requires an
     Interlingua-specific realization and a fresh price. Concretely:
     the number and repair modes need a vacant phonological region
     for their frame particles, and RZ's is the zone's silent `h`,
     which Interlingua does not straightforwardly offer; the chord
     layout is fitted to RZ phonotactics; the display script encodes
     RZ suffixes. **Portability is a hypothesis, not a property.**
   - *RZ-specific policies and artifacts* (portable only as the
     pattern behind them): the seven absorption declarations as
     written — including the inventory-level *para*→*por* merge and
     optional adjective agreement, both of which presuppose RZ's own
     grammar — the closure of RZ's particular 96-form inventory, and
     the built chord and glyph tables.
3. **Corpus inheritance is a goal with a number.** An Interlingua→RZ
   converter (bead `conlang-5i1.3`) makes the orthographic deltas
   mechanical and measures what fraction of running Interlingua text
   lands on RZ forms without a lexical swap. That fraction is the
   profile's cost of living for an existing Interlingua reader; it
   is reported, not assumed.
4. **Positioning.** "RZ = Interlingua, Ibero profile, plus engineered
   add-ons." Public-facing text (README, `rz-start.md`, the S1
   reader) says so in the first paragraph. Naming stays open, but
   the name must read as a variant, not a rival.

## What this changes downstream

- **The kill-gate (x6t) becomes profile-vs-baseline**, which is a
  cleaner experiment than RZ-vs-incumbent: the same texts in
  Interlingua orthography/lexicon and in RZ's, so every surface
  delta is a treatment with a control. The rule is PER DELTA (paper
  §11 is canonical): a surface delta is kept only if it materially
  raises the share of zone readers above the usability threshold,
  subject to a per-language non-inferiority floor fixed in advance;
  deltas that fail revert individually, so a losing bundle does not
  delete a winning delta. If none passes, RZ collapses to Interlingua
  plus the add-on patterns; the method, the instrument and the
  simulation results stand either way; realizing the patterns on plain
  Interlingua is then work to be done and repriced, not a fallback
  that ships itself.
- **The objective-function question (ym3.2) narrows.** Interlingua's
  three-of-four control rule is a centroid objective; RZ's Ibero
  weighting is the one surface delta that departs from it. Under
  the adopted option C (maximize readers above a usability
  threshold; the cloze data decide the weights), the weighting
  question *is* the profile-vs-baseline measurement.
- **Lexicon spend is redirected.** No further hand-minting of RZ
  entries that Interlingua already has; the recipe becomes
  "Interlingua entry → converter → Ibero re-election only where the
  screen or the weights demand it → false-friend screen."
- **Governance.** The profile has an owner and a versioned spec
  (program.md), which Interlingua lacks (UMI is promotional, the 1951
  standard frozen by inertia). That is a feature of the profile, not
  a claim over the baseline.

## What it does not change

The RZ grammar, lexicon, texts and curriculum as built. The GZ
laboratory line. The ledger method. The bootstrap pick (S1 reader).
The evidence discipline: every learner-facing number stays [H]
until the pilot runs.

## Dependency note

`conlang-wan` formally depended on `ym3.2` and `8zy`. Edward made
the profile call directly on 2026-08-30 ("do all that"); ym3.2 is
adopted at option C the same day; 8zy (restate the weights under
the objective) remains open and is now a profile-internal question.
