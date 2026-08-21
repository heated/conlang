# The program — endgame, lanes, and ownership
(Edward directive 2026-08-22; owned by the duke seat. This sits ABOVE
the design brief: the brief says what the languages are; this says
what the project is trying to become.)

## Endgame

**RZ is the language we ship.** The zonal bet wins on total time to
value — a Romance reader gets ~80% comprehension at first contact and
RZ's whole grammar in tens of hours, and no engineered feature set
beats "free" on the learning-speed axis this project exists for.

**GZ is the laboratory and the feature mine.** The greenfield line
(v0.2 core → GZ) is where channel discipline is developed cleanly
enough to *measure*. Features migrate from GZ into RZ exactly when
they are worth their learning cost. GZ also owns the native script
(see Script program below).

**The objective function for RZ**: sit on the Pareto frontier of
*easy to learn* × *featureful in good ways*. The learning-budget
ledger (learning-budget.md, bead caq) is the accounting instrument:
every candidate feature is priced in learner-hours and bought, made
optional, or declined — never adopted unpriced. The one invariant
RZ never trades away is the bootstrap: **first-contact receptive
intelligibility for zone readers**. Any feature that taxes the
first hour is display-layer, opt-in, or dead
(zonal-script-pricing.md is the precedent ruling).

## The mining gate (GZ → RZ)

A GZ mechanism ports into RZ iff:

1. its learner-hour price is on the ledger (measured or honestly
   estimated),
2. its value survives contact with RZ's naturalistic surface
   (no channel purity for its own sake), and
3. it costs the first-contact reader nothing — either invisible
   (input/display layers), optional (registers, modes), or an
   absorption move that makes learner output *more* grammatical.

Already through the gate (the pattern to follow): number/digit mode
(bought — rz-number-mode), error-absorption declarations D1–D7
(bought — grammar §10), repair mode (proposed), chording (free —
input layer), featural display script (free-ish — display-only).
Still in the mine: E/R/M POS-ending scheme (z0s bake-off), hard
particle-class boundary, penult-stress SSM-lite, script-borne
redundancy, escape-phoneme/mode frames beyond numbers (bcq).

## Lanes

**A. RZ excellence** (product lane — the default lane). Grammar,
lexicon, curriculum, error absorption, repair, modes, texts; every
change ledger-priced; the paper records each result. Kill-gate
stays armed: x6t (RZ vs Interlingua vs control, precommitted
criteria) is the honesty check that RZ is actually better, not just
ours.

**B. GZ mine** (lab lane). Develop GZ features to measurable
clarity; port what pays. GZ is not itself a shipping product; it is
allowed to be weird, and it hosts the script thesis.

**C. Bootstrap scenarios** (adoption lane). Explore *realistic*
directions to first users: who reads RZ first, what artifact
delivers value in minute one (graded reader? browser-extension
glosser? the STE-shaped safety register? phrasebook-with-a-secret?),
which precedents actually grew (Interslavic's dual-script
receptive funnel) vs died (Esperanto-shaped "learn a system first"
products). Deliverable: a scenarios doc with 3–5 concrete
first-100-readers stories and what each demands from the spec.

**D. Publication** (thesis lane). Two artifacts:
1. **The thesis**: engineering languages for learnability —
   channels, structured redundancy, error absorption, the
   learning-budget method, measured results. paper/paper.md is the
   living draft; the deliverable is a public, readable write-up.
2. **The language**: RZ's spec + reader pack + curriculum made
   presentable (the repo is already public; publication = a front
   door, not a leak).

**E. The portable toolkit** (generalization lane). Restate RZ's
mechanisms zone-agnostically: a menu of add-ons for ANY zonal /
continental / global auxlang, each with its price tag and evidence
— error-absorption declarations, number/date/time modes, repair
register, closed-class discipline, chord input over any phonology,
display-script layer, cloze-measured zonal fidelity, the ledger
method itself. AZ (Atlantic zonal, bead 3ug) is the second
instantiation that proves the recipe generalizes;
partial-systems.md and english-plus-channels.md are proto-entries.
This lane is the paper's spine: "a few dimensions along which you
can make a language better."

**F. Standing exploration** (bead i78, re-armed). Agent-directed
exploration for further wins — other conlangs' mechanisms worth
stealing (round 1 got SSM, Zipf policy, STE registers, shorthand
projection), and original directions. Findings land as priced
proposals, not adoptions.

## Script program (level-1 ruling, folded in)

- **GZ owns the script.** zonal-script-pricing.md stands: RZ is
  Latin-primary permanently; featural-primary would cost the entire
  zonal bootstrap. The native script is load-bearing only where
  there is no bootstrap to lose — the greenfield line.
- **RZ inherits the display subset.** rz_script's letterforms are
  already declared GZ's base; RZ's dense-display mode and suffix
  logograms are a re-skin of whatever GZ ships. RZ script work is
  maintenance-only until the cloze pilot justifies more.
- **The open fork is the engine**: boxed featural blocks (Hangul
  archetype, rz_script lineage) vs the stroke/join engine
  (shorthand archetype, strokes.py). Edward's two live complaints
  about the block pages — gap/segmentation ambiguity and weak
  compression — are answered *structurally* by the stroke engine
  (connected words make word-internal gaps meaningless; fusion
  bands are the compression dial). Settle by a design-workshop
  bake-off on GZ-shaped text, stroke side entering with the
  continuous-join vowel variant (bead h05).
- Carried laws, binding on both engines: the small-mark law
  (contrast in small added ink phase-vanishes; shape contrast
  survives), extend inventories by bases not modifiers
  (letterform-capacity.md), workshop pipeline + shadow log govern
  all taste calls (design-workshop.md).
- Priority: parked until a workshop round is wanted — script is
  polish on lanes B/D, not on the RZ product.

## Sequencing (near-term order)

1. **GZ→RZ mining audit** — walk every GZ mechanism through the
   gate, produce the priced menu; this turns "grab what's worth it"
   from vibe into a checklist.
2. **Bootstrap scenarios** — cheap, high-information, and it
   back-pressures the spec (what scenario 1 needs gets priority).
3. **Publication packaging** — after the mining audit settles what
   RZ *is*; the paper keeps accreting in the meantime.
4. Toolkit entries fall out of 1+3; steal-pass round 2 and
   exploration run in the gaps; script waits for a workshop round.

## What done looks like

A public thesis + a public RZ that a Romance-zone reader can start
reading today and learn properly in ~50 hours; a toolkit paper any
auxlang designer can shop from; GZ as the documented laboratory
that proved which features pay; the ledger as the receipts.
