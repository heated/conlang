# Workshop shadow log

Sealed agent picks vs Edward's verdicts (protocol:
design-workshop.md §Shadow judgment). One row per round decision.
Agent picks are recorded BEFORE Edward's answer; "settled by" is
filled only when something objective later adjudicates.

| date | round / question | agent shadow pick (sealed, reason) | Edward's verdict | agree? | settled by |
|---|---|---|---|---|---|
| 2026-08-22 | beauty variants V1-V5 (pre-protocol, recorded retroactively) | V2 light for text; V5 light-headstroke "the aesthetic surprise" | Explicit verdict on the sheet itself: V4/V5 headstroke "just aren't very useful... looks like a continuous line with occasional gaps"; V3 worse; V2's gaps "kind of ridiculous"; gaps as a format "don't work very well" (particle segmentation); ground bar over-bold (already fixed by two-weight); wants MORE COMPRESSION | split — V2-direction right, V5 WRONG again; new signal: gaps/segmentation and compression are his axes | — |
| 2026-08-22 | fused-unity-r1: disyllable unity mechanism U0-U4 | **U2 interlock** (reading-size density, zero new machinery); called U4 "worst unity" | **U3 spine** ("makes each character more recognizable") and **U4 stack** ("less like sprawling English"); disliked alternating dots, underlines colliding upward; whole sheet still "wide algebra-looking clusters", "Hanzi unoptimized for squishing together" | **WRONG** — and inverted on U4 | — |
| 2026-08-22 | vowel-topology-r1: T0 ticks / T1 join topology / T2 topology+tick | **T2** — best measured vowel median (0.200 vs 0.036) | **T0** — "one continuous character"; T1 "all over the place", T2 "a worse version of T0, maybe just from alignment" | **WRONG** | open conflict: metric says T0's vowels are literally indistinguishable (0.000). Edward's "maybe just from alignment" is the reconciling hypothesis — re-implement topology with continuous joins before re-judging |
| 2026-08-22 | fused-narrow-r2: narrow vertical composition N0-N3 (.ship-notes/workshop/fused-narrow-r2/) | **N1 spine stack**, runner-up N3; N2 rejected as muddy (shared stroke reads as strike-through). First pick scored on Edward's gestalt criteria (one figure > compact > even ink > survives small) instead of metric distance — this row tests whether the shadow track learned | pending | | |
| 2026-08-22 | gz-engine-r1: engine bake-off E0 blocks / E1 continuous chain / E2 narrow spine char / E3 Hangul-move syllable block (.ship-notes/workshop/gz-engine-r1/) | **E3**, runner-up E1. Scored on the gestalt criteria: E3 is the only engine whose vowels are full-size structural ink (blocks read as designed characters, survive small); E1 wins floors+density and is truly one continuous figure, but it is horizontal/wide — every prior Edward comment cut against width. Predicting he picks E3 or asks for E2xE3 hybrid (spine + structural vowel) | pending | | |

## Scoring so far (2026-08-22): 0 for 2

Both misses share one cause: **I optimized a mechanism/metric;
Edward judges GESTALT — does it read as a designed character rather
than sprawling algebra?** He rejected width and sprawl in every
comment and rewarded vertical compression (U3/U4) and continuity
(T0). Concretely, my scoring function should weight, in this order:
(1) is the word ONE figure, (2) is it compact/narrow, not wide,
(3) is the ink even — no huge-vs-tiny subletter contrast, no
floating dots, (4) does it survive small sizes without blobbing.
Metric distance is a floor-check, NOT the objective — that inversion
is exactly what both misses look like.
