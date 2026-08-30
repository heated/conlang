# The program — endgame, lanes, and ownership
(Edward directive 2026-08-22; owned by the duke seat. This sits ABOVE
the design brief: the brief says what the languages are; this says
what the project is trying to become.)

## Endgame

**RZ is the language we ship — as a declared Interlingua profile**
(Edward 2026-08-30, conlang-wan; decision record
`zonal/rz-interlingua-profile.md`). Interlingua (IALA 1951) is the
baseline; RZ's differences are enumerated surface deltas (each a
falsifiable bet) plus the add-on toolkit (which ports to plain
Interlingua as host-neutral PATTERNS requiring their own realization
and price there — not as drop-in artifacts). The paper is framed the
same way (§9b): the contribution is method + toolkit + results +
instrument, not a new language; the method, instrument and
simulations survive the kill-gate either way, while toolkit
portability to the unprofiled baseline is a hypothesis, not a
fallback. Landing epic:
conlang-5i1. The zonal bet is the favorite on
total time to value, with the targets stated at their separate bars
and labeled
honestly [H = hypothesis until measured]: zero-study cloze
comprehension for zone readers (Interslavic's published 84% is the
*precedent*; RZ's own number is unmeasured until the cloze pilot
runs); comfortable receptive reading in ~5–10 h [H, ledger]; C1
production ~100–200 h for Romance L1 [H, ledger, C1 bar]. No
engineered feature set beats near-free on the learning-speed axis
this project exists for [H — the premise of the bet, untested].

**GZ is the laboratory and the feature mine.** The greenfield line
(v0.2 core → GZ) is where channel discipline is developed cleanly
enough to *measure*. Features migrate from GZ into RZ exactly when
they are worth their learning cost. GZ also owns the native script
(see Script program below).

**The objective function for RZ** (primary, adopted 2026-08-30,
conlang-ym3.2 option C): **maximize the number of zone readers ABOVE A
USABILITY THRESHOLD** of zero-study comprehension — not mean
comprehension, and not the unweighted centroid. Whether that favours
concentrating on the Ibero bloc or spreading toward Interlingua's
control-language centroid is an empirical question the cloze pilot
answers; the threshold and weights are estimated by the pilot and the
deltas are judged on an independent confirmation set (paper §11).
Secondary, as an accounting constraint rather than the objective: sit
on the Pareto frontier of *easy to learn* × *featureful in good ways*.
The learning-budget
ledger (learning-budget.md, bead caq) is the accounting instrument:
every candidate feature is priced in learner-hours and bought, made
optional, or declined — never adopted unpriced. The bootstrap
invariant — **first-contact receptive intelligibility for zone
readers** — is what RZ never trades away, and it is enforced by two
DIFFERENT gates, which the charter previously conflated:

- **Add-on gate** (mechanisms ported from GZ, or invented): must cost
  the first-contact reader nothing. Any such feature that taxes the
  first hour is display-layer, opt-in, or dead
  (zonal-script-pricing.md is the precedent ruling).
- **Surface gate** (changes to inherited word forms — the profile's
  surface deltas, and any lexicon repair): these DO touch the first
  hour by construction, so "no tax" cannot be the rule. They are
  admitted only as falsifiable bets, kept only if they raise the share
  of readers above the usability threshold on the instrument, subject
  to a per-language non-inferiority floor fixed in advance, and
  reverted to the Interlingua form otherwise.

## The mining gate (GZ → RZ)

A GZ mechanism ports into RZ iff:

1. its learner-hour price is on the ledger (measured or honestly
   estimated),
2. its value survives contact with RZ's naturalistic surface
   (no channel purity for its own sake), and
3. it costs the first-contact reader nothing — either invisible
   (input/display layers), optional (registers, modes), or an
   absorption move that makes learner output *more* grammatical.
   This is the ADD-ON gate. A mechanism that changes inherited word
   forms does not fail here; it leaves this gate and enters the
   SURFACE gate (objective-function section above), where it is a
   measured bet, not a port.

Already through the gate (the pattern to follow): number/digit mode
(bought — rz-number-mode), error-absorption declarations D1–D7
(bought — grammar §10), chording (free — input layer), featural
display script (free-ish — display-only). Still in the mine: repair
mode (recommend-buy on the ledger; purchase waits on its own test),
E/R/M POS-ending scheme (z0s bake-off), hard particle-class
boundary, penult-stress SSM-lite, script-borne redundancy,
escape-phoneme/mode frames beyond numbers (bcq).

**Evidence discipline** (what "worth it" means until calibration):
the ledger's absolute hours are uncalibrated [H] pending the C1
calibration bead (pym), so gate verdicts are *provisional prices*,
not settled facts. Per the gate-calibration convention, pure-upside
moves (no preferred-form change, reversible, no first-hour tax) are
agent-callable immediately; anything else is adopt-pending-evidence
or an Edward call. The bootstrap invariant is operationalized through
the surface gate: a feature that touches RZ's surface is kept only if
it raises the share of zone readers above the usability threshold,
subject to a per-language non-inferiority floor fixed in advance.
**Human-testing directive, revised (Edward 2026-08-30):** the
2026-08-15 deferral is lifted for CHEAP paid studies — Prolific
micro-studies with a hard ceiling of **$30 per study**; if a question
cannot be answered for that, do not run it. **LLM-as-reader proxies
are ruled out** (Edward 2026-08-30) — no model-scored cloze stands in
for a human number, not even for ordering. Until a study actually
runs, every outcome claim stays hypothesis-labeled, in the paper and
in anything published.

## Lanes

**A. RZ excellence** (product lane — the default lane). Grammar,
lexicon, curriculum, error absorption, repair, modes, texts; every
change ledger-priced; the paper records each result. Kill-gate
stays armed and is now a PROFILE-VS-BASELINE design: x6t renders the
same texts with each surface delta isolated (orthography-only,
lexicon-only, grammar-only) against plain Interlingua and a control,
so each delta is a treatment with a control rather than a whole-
language beauty contest. It is the honesty check that RZ's departures
from the baseline are actually better, not just ours.

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
method itself. Toolkit entries are **conditional patterns, not
universal prescriptions**: each carries its evidence and requires
repricing against the target language's phonology, orthography,
and learner cohorts. AZ (Atlantic zonal, bead 3ug) is the
**replication test** — a second, related zone that tests whether
the recipe transfers; it cannot prove universality.
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
  maintenance-only; its unpark condition is a workshop round with
  renderer-specific reading/segmentation criteria on GZ-shaped
  text — NOT the cloze pilot, which tests Latin-surface lexical
  comprehension and says nothing about the display script.
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

1. **Bootstrap scenario decision packet** first — it's cheap, and
   the chosen audience/artifact assigns radically different value
   to modes, repair, and display features; the audit's weights
   come from it.
2. **GZ→RZ mining audit** — walk every GZ mechanism through the
   gate, weighted by the scenario packet; verdicts are provisional
   prices (see Evidence discipline): pure-upside buys land now,
   everything else lands as adopt-pending-evidence.
3. **Publication packaging** — after the audit settles what RZ
   *is*; outcome claims stay hypothesis-labeled until the cloze /
   x6t baseline runs. The paper keeps accreting in the meantime.
4. Toolkit entries fall out of 2+3; steal-pass round 2 and
   exploration run in the gaps; script waits for a workshop round.

## What done looks like

A public thesis + a public RZ that a Romance-zone reader can start
reading today, with measured (no-longer-[H]) numbers at each bar —
zero-study cloze, ~5–10 h receptive reading, C1 in the low
hundreds of hours; a toolkit paper any auxlang designer can shop
from, each entry priced and conditional; GZ as the documented
laboratory that showed which features priced out; the ledger as the
receipts, calibrated.
