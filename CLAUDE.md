# conlang — Agent Instructions

An engineered conlang optimized for learning speed and other things. North star:
`docs/design-brief.md`; program charter (endgame + lanes, Edward
2026-08-22): `docs/design/program.md` — RZ ships, GZ is the feature
mine and owns the script. Versioned spec: `docs/spec/`. Living
research paper: `paper/paper.md`. 

## Conventions

- **Paper:** every substantive bead updates its section of `paper/paper.md`
  as part of the bead (tracker: conlang-8c2). Citations seeded from the
  design chat stay marked TODO-verify until checked against primary sources.
- **Notes/plans/audits:** gitignored `.ship-notes/` (never `.claude/` in-repo).
- **Bead scopes:** `scope:arch` (spec/design), `scope:tooling`, `scope:build`.
- **Review policy (Edward, 2026-08-08):** one combined duke+crew seat.
  Code review = exactly one Codex reviewer (`gpt-5.6-sol`, reasoning
  `xhigh`) for substantive changes (behavior, architecture, invariants,
  security/privacy, persistence/wire formats, public APIs, nontrivial
  algorithms, risky refactors); skip for trivial docs/format/lint/naming/
  mechanical edits. No multi-agent review tiers unless Edward changes this.
  Addendum (Edward, 2026-08-08): additionally run an **occasional Fable
  review for language-design substance** (fresh Fable agent; at minimum at
  major linguistic milestones — core spec, grammar, lexicon, modes).
- **Invariant-bearing paths** (full playbook, no narrow lane): `docs/spec/`
  and anything that changes frozen-core language definitions.
- **Gate calibration (Edward, 2026-08-22, from the D1-D7 ruling):**
  decisions that are "basically just a win and don't negatively affect
  much" (mostly-upside, preferred forms unchanged, reversible) may be
  called by the agent directly — adopt, document, and report. The human
  gate is for real trades (inventory removals were flagged correctly;
  even that one Edward approved and reclassified as callable).
- **Design-workshop pipeline (Edward, 2026-08-22):** taste-laden design
  work (script aesthetics, layout, letterforms) goes through rounds of
  3-5 labeled approaches surfaced to Edward with comparison images +
  decision packets — full process in `docs/process/design-workshop.md`.
  Script work is deprioritized as a solo lane; when approximating the
  judge solo, use fast LOOK loops (render words AND a full paragraph,
  read the image, ≤2-3 solo iterations before checkpointing or surfacing
  a round). Agent taste SHADOWS Edward's, never replaces it: every round
  carries a sealed shadow pick logged in
  `docs/process/workshop-shadow-log.md` before Edward answers, scored
  against his verdict over time (Edward 2026-08-22).
