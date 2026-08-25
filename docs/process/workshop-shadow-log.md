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
| 2026-08-22 | fused-narrow-r2: narrow vertical composition N0-N3 (.ship-notes/workshop/fused-narrow-r2/) | **N1 spine stack**, runner-up N3; N2 rejected as muddy (shared stroke reads as strike-through). First pick scored on Edward's gestalt criteria (one figure > compact > even ink > survives small) instead of metric distance — this row tests whether the shadow track learned | 2026-08-25, via the E2 row of gz-engine-r1 (E2 = N1 generalized): "looks better than E0 but kind of still has the same issue" — mildly positive on the mechanism, blocked on the efficiency axis | ~agree (N1 direction acceptable, not sufficient) | superseded by the engine round |
| 2026-08-22 | gz-engine-r1: engine bake-off E0 blocks / E1 continuous chain / E2 narrow spine char / E3 Hangul-move syllable block (.ship-notes/workshop/gz-engine-r1/) | **E3**, runner-up E1. Scored on the gestalt criteria: E3 is the only engine whose vowels are full-size structural ink (blocks read as designed characters, survive small); E1 wins floors+density and is truly one continuous figure, but it is horizontal/wide — every prior Edward comment cut against width. Predicting he picks E3 or asks for E2xE3 hybrid (spine + structural vowel) | 2026-08-25: E1 "interesting" but BLOCKING objections (s-join jarring; sala/sola not distinguishable to the eye; piton "kinda bad"); E2 better than E0, same issue; E3 "kinda looks like E0... leaning into the blockiness... maybe a little better". Overall: "still not very efficient per se" — the missing axis is COMPRESSION, and he DELEGATED the engine call to the agent ("I'm not just gonna tell you which engine... ideally you own that") | **partial agree** — first non-miss: E3-lean matches the sealed pick; runner-up E1 rejected on look | agent owns the call (below) |

| 2026-08-25 | gz-efficiency-r1: compression dial D0-D3 on the E3 substrate (.ship-notes/workshop/gz-efficiency-r1/) | **adopt D1+D2 now** (79% area / 82% ink vs transparent, floors nearly unchanged, rule-derived, zero memorization), **D3 as direction** (77% area / 59% ink) pending a bounded brief tier + collision policy. Scored with compression as first-class criterion per the engine-round lesson | same day: D0 readable (line-gap ambiguity with 3-tall stacks); D1 particles float in ghost box + too light; D2 readable but uglier; D3 fine except residual 3-tall words + tick clipping; and the standing ideal named: FIXED-SIZE characters | ~agree on substance (dial accepted as direction); missed that his ideal (fixed cell) was the real target — built as F-mode in r2 | r2 |
| 2026-08-25 | gz-efficiency-r2: F-mode fixed 64x78 cell + particle/tick fixes | **adopt F as default page format** (48% area / 57% ink — the ideal is also the measured winner; floors hold at the disyllable squash); D-dial kept as loose/display mode; trisyllable cell + brief collision policy are the open costs | pending | | |

**Agent adoption call (delegated, 2026-08-25): E3 substrate.**
Reasons: Edward's lean; only engine whose vowel channel survives
every raster; blocks compose naturally with the compression moves
(frame-only particles, squash, briefs) that his "still not very
efficient" verdict makes the next axis. E1's connector idea is
parked, not dead (candidate for a handwriting/ligature mode).
Reversible: substrate choice touches renderers only, never the
feature grammar.

## Scoring so far (2026-08-25): 0 for 2, then 1 partial in 1
after switching to gestalt-criteria scoring — and the new signal
from the engine round: gestalt criteria were necessary but not
sufficient; Edward's standing axis is EFFICIENCY (compression on
the page), which transparent rendering can't satisfy at any
substrate. Score future picks with compression as a first-class
criterion alongside the four gestalt ones.

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
