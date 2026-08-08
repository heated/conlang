# Exploration: the register and the assignment policy, deconfounded

**Status:** exploration (bead conlang-zec), v2 — revised after
adversarial review (Codex: SOUND-WITH-CAVEATS on machinery; Fable:
UNSOUND-as-argued on the v1 recommendation, both reviews in
`.ship-notes/`). v1 of this note recommended dropping the register
outright; that recommendation rested on a confounded experiment and is
withdrawn. What follows is the deconfounded picture.

Experiment: `tools/explore_noparity.py` (v2). Prompted by Edward's
directive to explore "natural-grade emergent redundancy — no parity, no
mandatory concord, just sane phonotactics, SSM templates, and the
humility to not min-max word length."

## What v1 got wrong (and how v2 fixes it)

v1 compared the current spec (A) against a no-register architecture (B)
— but B also changed the *lexicon assignment policy*, refusing the
high-confusion minimal pairs that A licenses because "the register
catches them." The reviews showed the missing cell, A′ = humility
assignment **with** the register, changes the conclusion; and v1's
lexicon had no morphology, hiding the same-root POS minimal pairs
(∅/n/s codas on every root) that no assignment policy can avoid — which
is exactly where the register does irreplaceable work. v2 adds A′, POS
wordforms with class-conditional frequencies, a shared disyllable pool,
and reports both a conditional and an exposure-weighted metric.

## v2 results

Silent = corrupted percept is a form of a *different* root (wrong
meaning). Syntax = percept is another POS form of the *same* root
(caught by syntactic expectation with some unmodeled probability).
Conditional metric shown; exposure-weighted in parentheses. All rates
are per-substitution-event, **not** absolute mishearing probabilities.

| architecture | listener | parity-flagged | syntax class | **silent** |
|---|---|---|---|---|
| A — spec assignment + register | sensitive | 71% | 0.6% | **3.7%** (2.5%) |
| A — spec assignment + register | deaf | — | 18% | **22.0%** (15.0%) |
| A′ — humility + register | sensitive | 70% | 0.6% | **1.4%** (0.9%) |
| A′ — humility + register | deaf | — | 18% | **3.9%** (2.5%) |
| B — humility, no register | both | — | 18% | **3.9%** (2.5%) |

Ordering robust across error-model weights (W_HIGH swept 0.01–100 by
the code review) and concept-matched by construction.

## The deconfounded conclusions

1. **The assignment policy is the dominant factor.** Licensing
   high-confusion minimal pairs among top-frequency words (the current
   spec's policy) is what produces the 22% deaf-listener silent rate.
   Humility assignment fixes it in every cell, register or not.
   **Recommendation, unconditional: adopt humility assignment.** Cost:
   monosyllabic root bodies drop 34 → 22 (after the 30% reserve, ~15
   initially assignable); ranks ~15–22 of the frequency list go
   disyllabic.
2. **With humility adopted, the register is pure insurance — for
   length-sensitive listeners only.** It buys them: residual silent
   rate 3.9% → 1.4%, and audible flagging of the noun↔verb and
   noun↔modifier POS flips (the 18% syntax mass drops to 0.6%; only the
   n↔s flip escapes the check bits). Length-deaf listeners get exactly
   nothing: A′ ≡ B for them in every cell.
3. **The register's costs fall on everyone**, and hardest on speakers
   of length-less L1s: producing a length contrast their L1 lacks
   (with false-alarm noise for sensitive listeners when they get it
   wrong — though the L2 literature says duration contrasts are
   trainable, so this is a cost, not an impossibility), the
   stress-vs-duration conflict that weakens the SSM boundary cue, the
   erosion exposure of a zero-lexical-load contrast, vowel doubling in
   the orthography, and an extra zone in script and input layers.

## The three-way register decision (Edward's call)

- **Keep (A′).** Best protection for sensitive listeners; graceful
  degradation for everyone else; machine-checkable speech. Pays all
  structural costs. Chooses insurance over simplicity.
- **Drop (B).** Simplest language; stress gets duration back
  (strengthening segmentation for everyone); nobody produces length,
  ever. Sensitive listeners lose 2.5 points of residual insurance and
  the audible POS-flip flag; POS integrity rides on syntax/semantics
  for everyone (as it already does for the length-deaf).
- **Demote to the written layer** (new option, crystallized by this
  round): the check bit remains a *computed, written-and-machine
  channel* — a glyph zone like the planned semantic classifiers, with
  optional realization as length in careful/safety speech registers
  only. Casual speech never carries it; machines and readers always
  have it; the safety register (which already mandates checksums) can
  require it. Costs: the glyph/chord layers keep the zone; the
  "three renderings of one vector" story gains a register-dependent
  asterisk. This retains most of A′'s insurance where it matters and
  most of B's simplicity where people live.

The experiment cannot decide among these — the residuals it measures
are small and the deciding factors (production burden, erosion,
segmentation gains, machine-layer value) are unmodeled qualitative
weights. What it does establish firmly: the humility assignment, and
the fact that the *current* spec's assignment policy is the one
configuration that is strictly wrong for the project's own priority
population.

## Caveats the reviews imposed (carried forward)

Rates are conditional on exactly one substitution; no calibrated human
confusion data (weights are assumptions; ordering is weight-robust);
syntax-class recovery probability unmodeled; insertions/deletions and
segmentation errors out of scope (the tosmabru and echo-vowel rules
address those at assignment time); single seed (deterministic, but one
lexicon draw); POS token-frequency split (0.5/0.3/0.2) assumed.
