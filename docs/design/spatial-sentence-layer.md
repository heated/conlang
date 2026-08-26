# The spatial sentence layer — structural bake-off, round 1

(conlang-4j7, 2026-08-26. Edward: "lets build that crazy spatial
reading thing. some experimental direction.")

## What this is

The **spatial sentence layer** is the project's designated sequel
(`docs/design-brief.md` Tier 4; `paper/paper.md` §closing). Its thesis,
from the original design record:

- Reading throughput converges near **~39 bits/s** across languages and
  scripts. The bottleneck is downstream of perception — serial binding
  plus working memory — not the eyes. [H, TODO-verify]
- So a denser script buys **compactness and scannability, not speed**
  (Chinese vs English: ~2× spatial density, same bits/s, shorter
  saccades).
- The exploitable margins are **prediction**, **selection** (make
  structure visible pre-comprehension so you read *less*), and
  **parallelism** (stop being a string). Only the third attacks the wall
  itself: spatial layouts hand relations to parallel vision. Nobody reads
  a subway map or a schematic aloud.
- Precedents on record: ASL assigns referents to locations in signing
  space (pronoun ambiguity becomes architecturally impossible);
  Heptapod B writes propositions as nonlinear rings; math and circuit
  notation.
- **The conlang's specific contribution** is that extraction is
  deterministic. POS coda marks noun/verb/modifier, a closed particle
  class marks oblique roles, and SSM segments words — so the argument
  graph falls out of a parser, not out of an AI approximation.

## Scope discipline (Codex xhigh plan review, blocker 2)

This round is a **structural prototype bake-off**, not an experiment.
One hand-built discourse, one informed judge, no trials, no training
protocol. It can select a promising prototype; it **cannot** validate
parallel binding or any reading-speed claim. Every number below is a
geometric diagnostic [M on these renders], never evidence about
cognition. The behavioural experiment that *could* test the thesis is
specified in "Open work" and has not been run.

## The five layouts

Tool: `tools/spatial_layer.py` (`pages`, `sheet`, `metrics`); images in
`.ship-notes/workshop/spatial-r1/`. Rasterize via `tools/rasterize.py`
— **not** `qlmanage`, which silently crops wide SVGs.

- **S0 linear control** — ordinary wrapped running text.
- **S1 referent lanes** — x = entity (one vertical lane, named ONCE at
  the lane head), y = clause; a clause is a horizontal bar joining its
  participants' lanes; role = cap shape (square agent, arrowhead
  patient, circle+letter oblique); negation strikes the bar. The ASL
  "same entity, same column" steal, drawn as a storyline/subway map.
- **S2 role compass** — role = angle around a central predicate (agent
  W, patient E, time N, locative S…). Reference carried only by tint.
- **S3 proposition rings** — the Heptapod move taken seriously: role
  lives on the **angular** channel, which in principle frees both plane
  axes for topology, so a shared entity can be written once and read as
  agent by one ring and patient by another. A greedy solver places rings
  to satisfy that constraint and reports how many it satisfied.
- **S4 schema grid** — the ablation: a literal table, role = column,
  clause = row. Included so that if the plain table wins, the fancy
  layouts are decoration.
- **S5 the chain** — built after S3 failed, from its residue. The
  legible part of the ring layout was never the circles: it was the
  alternating entity/predicate **path** with a shared entity written
  once at the junction. Running that path in discourse order fixes both
  of S3's disqualifiers — clause order survives (left to right) and a
  complement clause attaches inline in brackets. Role is read off the
  side of the predicate (before = agent, after = patient); modifiers
  hang under their head so they cannot break a junction; a seam bar
  marks a clause boundary wherever two clauses do not share.

Specimens render **English lexemes inside the GF grammar** so that
layout is the only variable the judge evaluates (see "What English
costs").

## Measured diagnostics [M]

Normalized against the **ink** bounding box, never the canvas, so blank
margin cannot improve a score; mention extents are full glyph boxes, not
anchor points; `marks/prop` counts every information-bearing primitive
(caps, bars, connectors), not just text.

| layout | ink area/prop | marks/prop | referent scatter | area to search per referent | crossings |
|---|---|---|---|---|---|
| S0 linear | **8,792 px²** | 6.8 | 0.252 | 31.7% | 0 |
| S1 lanes | 84,146 | 7.9 | **0.124** | **0.6%** | 1 |
| S2 compass | 86,759 | 8.6 | 0.425 | 30.1% | 1 |
| S3 rings | 39,319 | 8.8 | 0.251 | 9.1% | 0 |
| S4 grid | 39,141 | **7.5** | 0.323 | 25.3% | 0 |
| S5 chain | 14,588 | 7.6 | 0.291 | 24.9% | 0 |

The stimulus itself (not any layout) forces a serial binding span of
**7.1 tokens mean / 16 worst** — the working-memory reach a linear
reader holds to bind a referent to its previous mention.

## Essay scale [M] — the scale that actually matters

Edward, 2026-08-26: area "matters a lot more for like at the essay level
and less at the sentence or short paragraph level, although those might
be predictive." He is right that it is predictive and right that the
short-text numbers are the wrong headline. At 24 clauses (~195 words,
the `study` test texts) the ordering holds but the ratios move a lot:

| layout | page at 24 clauses | vs linear | vs its own 8-clause ratio |
|---|---|---|---|
| S0 linear | 0.59 Mpx | 1.0× | — |
| S5 chain | 0.68 Mpx | **1.2×** | improved from 1.7× |
| S4 grid | 1.40 Mpx | 2.4× | improved from 4.5× |
| S1 lanes | 2.64 Mpx | 4.5× | improved from 9.6× |
| S2 compass | 3.05 Mpx | 5.2× | improved from 9.9× |
| S3 rings | 3.25 Mpx | 5.5× | and **5320 px wide** — unusable |

Every spatial layout amortizes as the text grows (fixed scaffolding —
lane heads, column headers — is paid once), so short-text area
penalties are upper bounds. The exception is S3, which grows in one
dimension only and becomes a 5000-pixel ribbon.

## Findings

1. **The selection win is real and large.** To find everything about one
   referent, S1 confines the search to **0.6%** of the page against
   **31.7%** for running text — a ~50× reduction, and it is
   architectural rather than incidental: same entity, same lane, by
   construction. This is the "read less, don't read faster" margin, and
   it is the one structural claim round 1 supports.
2. **The compactness cost is brutal: ~10× the area** (S1 84k vs S0 8.8k
   px² per proposition). Against Edward's standing efficiency axis, every
   spatial layout loses to a string, decisively. Whatever the spatial
   layer is for, it is not saving page space.
3. **"Write each entity once" does not reduce marks.** The intuition
   that lanes and rings collapse repetition is **false** once caps, bars
   and connectors are counted: marks/proposition is flat across all five
   (6.8–8.8), and the plain grid is the *lowest*. A word replaced by a
   cap is still a mark the reader decodes. (This corrected an earlier
   draft that counted only text labels and reported a spurious S1 win.)
4. **S3's angular escape degenerates.** With agent at 180° and patient at
   0°, every agent/patient share places the two rings on the same
   horizontal line, so the rings tile into a **1-D chain** — the plane
   freedom the angular channel was supposed to buy is not realized, and
   the circles become decoration on what is once again a string. Only
   **3 of 7** shares were geometrically satisfiable; the rest fell back
   to duplicated boxes.
5. **S3 is disqualified on information, before taste.** Rings have no
   reading order, so **clause order is lost**, and there is nowhere to
   attach a complement edge. The oracle-coverage gate rejects it
   regardless of how it looks.
6. **S1 has its own hole:** a modifier's cap sits on the modifier's own
   lane with nothing saying which argument it attaches to. Fixable
   (attach the mod cap to the head's cap), but currently lossy.
7. **The grid is the thing to beat.** S4 is complete on oracle coverage,
   lowest in marks, half S1's area — and it is boring on purpose. Any
   fancier layout has to earn its keep against it, and on this discourse
   only S1's search fraction does.
8. **Compactness and selection are in direct tension — the round's
   sharpest result.** S5, built from S3's residue, gets within **1.7×**
   of a plain string (14,588 vs 8,792 px²/prop), keeps clause order and
   complement attachment, and posts zero crossings — but its search
   fraction is **24.9%**, barely better than running text's 31.7%,
   because a chain only collapses *adjacent* shares (2 joins here, 4
   distant mentions still repeated). Meanwhile S1 buys the 50×
   selection win at 9.6× the area. **Nothing measured so far buys both**,
   and that is the shape of the design problem: pinning reference to a
   coordinate costs a whole page dimension, and reclaiming that
   dimension costs the pin.

## The axis constraint, stated narrowly

Tempting overclaim: "the plane has two axes, so you can pin reference or
role but not both." The Codex plan review is right that this is not a
theorem — row/column intersection, nested frames, ports, containment and
faceting all encode two categoricals jointly. The defensible version:

> Given **global axis-aligned lanes and no additional local structure**,
> reference and role cannot both occupy the same axis; whichever is not
> pinned must move to a third channel (cap shape, tint, or angle).

That is what the bake-off actually exhibits: S1 pins reference and pushes
role to cap shape; S2/S4 pin role and push reference to tint; S3 tries to
escape via angle and collapses.

## What using English costs (Edward's question)

Specimens use English lexemes deliberately: the judge can read English,
so layout is isolated from legibility. What that buys and what it costs
(review-checked):

**Transfers to GZ/RZ:** graph topology and solver feasibility;
constraint failures, crossings, duplication; coarse clutter under
fixed-size label boxes; discriminability of caps, angles and lanes.

**Does not transfer:** actual area/compression with fixed-size conlang
blocks (GZ words are ~1–2 blocks where English words are 4–9 glyphs, so
every area number here is pessimistic for the conlang and the *ratios*
between layouts will shift); conlang word recognition and the POS/
particle channel benefits; reading speed, learning time, retention;
whether unfamiliar glyphs stay legible when densely arranged; and —
the sharp one — **whether familiar English semantics let the judge
silently repair an ambiguous layout encoding** (you know a river floods
a valley, not vice versa; a GZ reader would not).

The honest cost is therefore bounded and specific: English is safe for
choosing a layout grammar, unsafe for any claim about density,
legibility or learnability. The named fix before those claims: re-render
survivors with neutral fixed-width entity IDs and semantically
unpredictable predicates, then with real script blocks.

## Direction review (Codex xhigh, 2026-08-26): **PURSUE NARROWLY**

The verdict, and it converges with Edward's own reaction ("it's just a
map of the mechanics of the story… you could just summarize it"):

> The result worth preserving is not "a new way to read language." It is
> a deterministic semantic trace: an optional, generated view for
> inspecting reference, roles, scope, and change. As a compulsory
> notation, it conflicts with the learning-speed north star.

**The finding that guts the headline.** The 0.6% search fraction is not a
reading result — and worse, it is not even a *spatial* result, because
plain text with the referent's mentions highlighted would deliver most of
it for free. "At present, the evidence supports structured indexing — not
a spatial sentence layer." So the distinguishing experiment must hold
selection constant: compare (1) linear text with mentions highlighted,
(2) linear text with filtering and folding, (3) the spatial projection —
and ask *relational* questions (role transitions, scope, multi-clause
inference), never "find all mentions". If the spatial advantage survives
matched selection, parallel binding is supported; if it disappears, "the
project has built an index and should name itself accordingly."

**The honest killer application** is what `ctrl-F` cannot answer: show
every event involving this referent, *the role it occupies in each*, how
that role changes, which embedded propositions depend on it, and what
changed between two versions. Translation checking, semantic diffing,
contracts, procedural texts. Search finds strings; it does not expose
referent identity, role transitions, omitted arguments or scope.

**The strongest version** is a semantic oscilloscope, not a page format:
the canonical language stays linear; only *active or selected* referents
get lanes (nine permanent lanes must not become ninety); roles are shown
locally at the event as well as spatially; the unit is the working set —
an episode or a referent's history, roughly 3–12 clauses — not the whole
discourse; complements are collapsible insets; and the best fit with the
north star is as a **teaching scaffold that fades** as the learner
internalizes the grammar.

**S4 is not an ablation.** "Its boringness is an advantage: tables are
already learned. Start from the table and add only the spatial
affordances that produce measured gains. The winning artifact may be a
table–lane hybrid rather than a novel script." This is also what Edward
reached for unprompted — easiest to learn, most prose-like.

**Precedent ranking:** sheet music is the most instructive (strict
temporal axis, concurrent structure aligned spatially, serves specific
tasks that repay training, never claims to replace prose). Heptapod B is
the trap — its appeal is aesthetic, and circular simultaneity conceals
order, embedding and revision, which is exactly how S3 failed here. ASL
proves spatial reference exists but is embodied, temporal and
interactive, not static parallel reading. Dependency treebanks and node
editors warn that making structure explicit does not make people prefer
it for *consuming* content — their strength is debugging.

**Cut from the core** (adopted): compulsory spatial literacy; free-form
layouts; proposition rings; role compasses as sole encoding; "write each
entity once" as a design goal; any grammar added to serve the display;
any claim that the view replaces ordinary reading. Keep the deterministic
graph and optional projections; promote on evidence only.

**Kill condition, precommitted:** if the trace does not improve accuracy
or time after accounting for training — and especially if its benefit
disappears against *highlighted* linear text — stop developing it as a
notation.

## Open work

Round 2 candidates:

- **Break the compactness/selection tension** (finding 8) — the central
  open question. Candidates: narrow lanes (lane pitch is currently set
  by English word width, which GZ blocks would cut ~3×); lanes that
  carry only *recurring* entities with one-offs inlined; a hybrid that
  chains within a line and pins lanes across lines; or accepting that
  these are two different products (a reading format and a reference
  surface) rather than one layout.
- Fix S1's modifier attachment; add a leader line from the row bar to
  the right-gutter temporal.
- Generated, untuned corpus crossing entity count, coreference distance,
  role switching, shared-entity degree, no-coreference cases, nested
  complements and negated complements — the single hand-built discourse
  is selection-biased toward exactly what lanes are good at.
- Factorial ablation of the tint channel (tint is present in all five
  layouts, which confounds reference cues); monochrome main comparison.
- A layout→oracle **decoder** so coverage is proved rather than asserted.
- Exhaustive small-graph enumeration for any ring/chain variant:
  satisfiability, crossings, duplication, worst case.

Before the spatial layer can be called a language feature rather than an
optional visualization, it needs a behavioural gate: randomized
repeated-measures tasks (selection, binding, integration) after fixed
training, with the precommitment that **the thesis fails if no spatial
condition beats both S0 and S4 on accuracy-adjusted response time and
shows a shallower slope as clause count rises**. Plus a learning-cost
budget — the project's north star is learning speed, and a notation that
improves expert search while costing many hours is a net loss.

Evidence: all tables [M] on these renders; oracle coverage [A] asserted
by inspection; the ~39 bits/s and saccade findings [H, TODO-verify]
inherited from the design chat.
