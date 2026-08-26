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
| 2026-08-25 | gz-efficiency-r2: F-mode fixed 64x82 cell + particle/tick fixes | **adopt F as default page format** (50% area / 55% ink — the ideal is also the measured winner; floors hold at the disyllable squash); D-dial kept as loose/display mode; trisyllable cell + brief collision policy are the open costs | same day: **F "just doesn't really work — squishing some characters into not being very distinguishable"; D3 "looks pretty good overall"** (wants the brief mechanism explained); D0's role unclear to him (it's the control) | **MISS** — F was my pick, rejected on legibility-by-eye; his own fixed-size ideal lost to D3 when he saw the squash cost | D3 is the working format |

| 2026-08-26 | spatial-r1: the spatial sentence layer, S0 linear / S1 referent lanes / S2 role compass / S3 proposition rings / S4 schema grid (.ship-notes/workshop/spatial-r1/) | **S1 referent lanes as the direction**, with **S4 grid as the baseline it must beat** (S4 is complete on oracle coverage, lowest marks, half the area — fancy layouts must earn their keep against it). **S3 rejected on information, not taste**: rings have no reading order so clause order is lost, no complement attachment, and the angular channel degenerates to a 1-D chain (3/7 shares satisfiable). S2 dominated. Reason for S1: the only structural win round 1 actually supports is SELECTION — 0.6% of the page to find every mention of a referent vs 31.7% for a string, architectural rather than incidental. Scored with compression as a first-class criterion per the engine-round lesson, which is why the pick is hedged: **predicting Edward's efficiency axis fires on the ~10× area cost** and that he asks what the layer is FOR (reading vs skimming/reference) rather than accepting it as prose replacement. Secondary prediction: he finds S3's chain-of-circles visually interesting even though it fails the gate, and S2 gets rejected outright | — | — |

Addendum to the spatial-r1 row (logged AFTER the pick was sealed, BEFORE
Edward answered — the pick above stands as written): the S3 post-mortem
said its chain residue was the legible part, so **S5 "the chain" was
built mid-round** and measured. It changes the pick's framing but not
the pick: S5 lands at 1.7x a plain string (vs S1's 9.6x) and keeps
clause order + complement attachment, but buys no selection (24.9% vs
running text's 31.7%). So the round's real result is a TENSION —
compactness and selection trade off directly and nothing measured buys
both — and S1 remains the pick only if the layer's job is
selection/reference rather than prose replacement. That conditional is
exactly what Edward's answer should settle.

Scope error caught by Edward (2026-08-25, after the F round): the
entire engine + efficiency lane rendered the GF-N inventory while
calling it GZ — GZ per gz-sketch.md has Romance's phoneme space
(~10× the syllables, clitic particles, clusters, diphthongs). His
"efficient script" ask was about GZ proper; part of why every page
felt inefficient to him is that GF-N words are structurally 2-3
syllables where GZ words would mostly be 1-2. Lesson: load the
target language's DEFINITION before building rounds on it; the
handles (GF-N / GF-W / GF-C / GZ / RZ) name different design
points, not one greenfield.

Lesson from the F miss: Edward's "fixed-size ideal" was a
hypothesis he wanted tested, not a preference to satisfy — when
uniformity's price (squashed internals) became visible he dropped
it instantly. Distinctness-by-eye dominates geometry ideals.
Metric floors passing (0.366 median, no collapses) did NOT predict
his rejection — the failure was visual crowding, which the
occupancy metric doesn't capture. D3's variable-height tidy page
is the adopted direction.

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
