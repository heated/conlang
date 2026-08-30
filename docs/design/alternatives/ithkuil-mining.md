# Mining Ithkuil: what we take, what it costs, what it broke

**Status:** active mining (lane F, bead conlang-i78). Edward
2026-08-30: *"I do want to mine Ithkuil for stuff and generally try to
improve our languages and steal things"* — with the explicit steer
**not** to invest in documenting Ithkuil as a reference. The failure
analysis lives in `ithkuil-forks.md`; the checklist of markable
distinctions is PARKED in `../construal-namespace.md`. **This file is
where the steals get proposed and priced.**

Everything below is a proposal against the mining gate
(`../zonal/gz-rz-mining-audit.md`): priced in learner-hours, ported
only if it survives contact with the target language's surface, and
costing first contact nothing.

---

## M1 — Conditional obligation *(the best thing in Ithkuil, and it is free)*

**The observation.** Ithkuil's Validation — its evidentiality channel
— is obligatory **only within assertive illocution** [V 2026-08-30].
Ask a question and the evidential choice never arises, because "what
is your evidence for this question?" is incoherent. The category is
mandatory exactly where it carries information and absent everywhere
else.

**The generalised mechanism.** A category can be made obligatory
**conditioned on a feature already present in the utterance**, rather
than either (a) always required, or (b) speaker-optional. This is a
third point on a dial this project has been treating as binary:

| | who decides | cost when it has nothing to say | ambiguity |
|---|---|---|---|
| blanket obligation | grammar | full — you fill the slot anyway | none |
| speaker-optional | speaker | none | "did they mean to omit it?" |
| **conditional obligation** | **the condition** | **none** | **none** |

Where the condition is computable from material already in the
sentence, this strictly dominates both. No selection cost outside the
condition, and no omission ambiguity inside it.

**We already do this twice without having named it.** The check bit is
realised in speech only in careful/safety registers (SPEC §2.4); the
mode checksum is mandatory only in the safety register (modes.md §9).
Both are conditional obligation. Naming the mechanism turns two
one-off decisions into a reusable tool — and into a **portable toolkit
entry** (program lane E), which is the lane's whole purpose.

**Proposals following from it:**

- **GZ evidentials fire on assertions only.** Tier-3 evidentials were
  already on the brief; this settles their shape before they are
  designed. Cost: zero for questions, commands, and every non-assertive
  utterance — which is where a blanket evidential channel would have
  bled learner-hours for nothing.
- **Audit the rest of GZ for categories that should be conditional
  rather than blanket.** The POS coda should *not* be (it is the parse
  channel and must be unconditional). The interesting case is the
  written-layer check on payload syllables.

**Price: ~0 learner-hours.** It is a rule *about* rules; it removes
obligations rather than adding them. **Verdict: ADOPT as a named
design primitive.** Ledger row filed. This is the one steal from
Ithkuil that costs nothing and improves the design immediately.

---

## M2 — Specification as a root multiplier

Ithkuil derives four facets of every root — BSC basic, CTE contential,
CSV constitutive, OBJ objective — from one 4-way alternation in Slot
IV's `Vr` [V 2026-08-30]. GZ's scarcest resource is monosyllabic root
bodies: **22** under the humility rule, **15** assignable after the
30% reserve (SPEC §8).

Already filed and rescoped as **bead conlang-czq**; the ledger row is
**PROPOSED, UNPRICED**, and it stays that way until two blocking
questions are answered:

1. Specification only (4 cells), or the full Stem × Specification grid
   (up to 16, with root-specific lexical content in each)?
2. **Where does the spoken exponent live?** The coda is spent on POS;
   an extra syllable makes it ordinary derivation; a script-only marker
   leaves spoken forms homophonous and breaks four-projections
   determinism.

Note the honest framing, corrected in review: this does **not** create
root bodies. It conditionally reduces semantic pressure per body, and
the multiplier depends on how many cells are usable for a given root —
unmeasured.

---

## M3 — Discourse-register particles *(good idea, blocked by a bug it exposed)*

**The steal.** Ithkuil marks discourse register with adjuncts: NRR
narrative (**the default, marked by nothing**), DSV direct speech, PNT
parenthetical aside, SPF specificative (naming the preceding referent),
EXM exemplificative ("for example…"), CGT cogitant (silent/subjective
thought), END carrier-end — **7 values** [V 2026-08-30].

**Why it is attractive for GZ specifically.** These are distinctions
prose marks badly with punctuation and speech barely marks at all —
quotation, asides, worked examples, interior monologue. GZ is designed
for machine parseability and already has an unstressed particle class
that would carry them at one syllable each. DSV in particular would
let a parser find speech boundaries without quotation marks, which is
a real win for a language whose selling points include unambiguous
parsing. And NRR-as-silent-default is M1's pattern again.

**What pricing it uncovered — a P1 bug, `conlang-39z`.** GZ's particle
space is `h` × 5 vowels × 4 codas = **20 cells**, and the audit says:

```
occupied: 20 / 20        genuinely free cells: ZERO
COLLISIONS: h-a-n  →  modes.md "chunk separator"
                   +  gf-grammar.md §3 "NEGATION"
```

Modes own 9 cells, the grammar 11 (including the collided `haan`) plus
`h-i-l` nominally reserved. Two consequences:

1. **`haan` is double-assigned**, and one of its two jobs is negation —
   the highest-stakes bit in any utterance, which gf-grammar
   deliberately gave the most robust form precisely because
   mishearing it inverts meaning. Compare `conlang-1op`, where RZ's
   unprotected polarity bit is already P1.
2. **SPEC §5.2's pre-freeze question is now answered, and the answer is
   no.** The spec says whether 20 particle slots suffice "is
   established by conlang-jbw's enumeration *before* freeze, not
   assumed." The enumeration has effectively happened: the space is
   exactly full, with a collision, **before adding a single new
   mechanism**. That is freeze-gate material.

**Verdict: M3 is DEFERRED behind `conlang-39z`, not declined.** The
mechanism is cheap and genuinely useful; there is simply nowhere to
put it. If the resolution of 39z is to widen the particle namespace
(SPEC §9's documented minor-version path), M3 should be re-costed as
part of that decision rather than separately — a widening that buys
only breathing room is a worse deal than one that also buys registers.

**Price if space existed: ~0.5–1 h [H]**, cohort-flat, optional at
first contact (the default register is unmarked, so a learner who
never uses them writes correct GZ). Only DSV and CGT look clearly
worth their slot; SPF, EXM and END are periphrasable.

---

## M4 — Configuration *(cheap, optional, unproven)*

Set shape as a nominal channel: one/pair/set-of-similar/set-of-
dissimilar/mass, plus separate/connected/fused — 20 values in New
Ithkuil, 9 in 2011 [V 2026-08-30]. Neither Romance nor English marks
this; both lexicalise it (*tree / grove / forest / orchard*).

A 3–4 value subset (one / set-of-same / set-of-mixed / mass) is the
interesting part; the 20-value grid is not. Attractive because it is
**optional by construction** — an unmarked noun is simply
unspecified for shape — so it cannot tax first contact.

**Verdict: PILOT CANDIDATE for GZ, unpriced.** Lower priority than
M1–M3; no bead until something needs it. Worth remembering that GZ has
no grammatical number at all (plurality by quantifier, gf-grammar §1),
so Configuration would be its *only* set-shape machinery and competes
with simply having a plural.

---

## Declined

| mechanism | why |
|---|---|
| the case / aspect / phase / valence / bias tails (68 cases, 36 aspects, 61 biases) | the long tail costs learning time at the head's rate for a fraction of the use. This is R4, the failure we are mining *around* |
| Level (9-way scalar comparison) | RZ's `plus/minus … que` and GZ's `mu-s` already cover the useful middle; a 9-point scale is precision nobody asked for |
| lookup-heavy fusion, tone as a grammatical channel | R2/R3 — the warnings, already in the design brief |
| Bias / attitudinal layer | declined for design. Retained only as precedent that text-channel markers get adopted when they fix a real loss |

---

## What this pass actually produced

One free mechanism worth adopting (M1), one capacity question already
in flight (M2), one good idea blocked by a P1 bug it exposed (M3), one
pilot candidate (M4) — and `conlang-39z`, which is the most valuable
output and has nothing to do with Ithkuil. Pricing a steal against a
real budget is how you find out the budget is broken.
