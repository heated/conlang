# Design workshop pipeline (Edward + agent, est. 2026-08-22)

Standing process for taste-laden design work (script aesthetics,
letterforms, layout, anything where "better" is judgment, not a
metric). Edward: "will prob want a pipeline that involves me more &
surfaces multiple approaches to me at a time. i can aid judgement."
This file is the durable spec; a pointer lives in CLAUDE.md so the
process survives compaction.

## The loop

1. **Agent prepares a ROUND**: 3-5 genuinely different approaches
   to ONE design question (not parameter nudges of one approach —
   different mechanisms). Each approach gets:
   - the same specimen content (a few words AND a full paragraph —
     both scales, always; approaches that win at word scale lose at
     paragraph scale and vice versa);
   - one composite comparison image, labeled V1..Vn, plus per-variant
     full-page renders when scale matters;
   - a 3-6 line decision packet: what varies, my read, what each
     trades away, what's reversible.
2. **Surface**: write the round to `.ship-notes/workshop/<topic>-r<N>/`,
   `open` the composite image, post the packet as a bd comment on the
   round's bead, and STOP that lane — no adopting a winner myself.
3. **Edward judges**: picks, mixes ("V2 but with V4's codas"), or
   redirects. His feedback goes in the bead (or chat).
4. **Agent applies** the pick, re-renders both scales, opens the
   result for confirmation, and only then updates tests/floors/docs.
5. Next round or close.

## Agent self-approximation (between rounds / when Edward is away)

Approximate the judge with fast LOOK loops, not metric loops:
- after EVERY geometry change, render a few words AND a full
  paragraph, rasterize, and actually read the image before deciding
  anything;
- iterate at most 2-3 looks solo, then either checkpoint (commit,
  tests green) or bundle the alternatives into a round for Edward —
  never deep-iterate taste alone;
- metrics (raster floors, margins) are regression rails, not taste:
  passing floors ≠ looks good. The 18s lesson: the overlap metric
  passed while the page read as debris.

## Rules

- Rounds are cheap; adoption is not. Multiple approaches per round,
  one adoption per Edward decision.
- Every round's images stay on disk (`.ship-notes/workshop/`) so a
  later round can re-compare against history.
- Script/visual work is DEPRIORITIZED as a solo lane (Edward
  2026-08-22): no unprompted deep script iteration; script effort
  goes through this pipeline.
- The pipeline generalizes beyond script: lexicon aesthetics, page
  layout, letter-name tables, any taste-heavy call.
