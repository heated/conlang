# conlang — Agent Instructions

An engineered conlang optimized for learning speed. North star:
`docs/design-brief.md`. Versioned spec: `docs/spec/`. Living research paper:
`paper/paper.md`. The duke seat owns project shape and translates human
direction into beads.

- Duke role: load the `duke` skill (`/duke`) and `human-gates`.
- Issue tracking: **bd** (beads). `bd ready`, `bd create`, `bd show`, `bd close`.
- Land work on `origin/main`; don't let branches accumulate.
- This file is the source of truth for project conventions; grow it as the
  project takes shape.

## Conventions

- **Remotes:** `origin` = local crew landing target (bare repo); `github` =
  public mirror (github.com/heated/conlang). After landing on `origin/main`,
  also `git push github main`. The repo is PUBLIC — nothing sensitive in
  commits.
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

<!-- BEGIN BEADS INTEGRATION v:1 profile:minimal hash:ca08a54f -->
## Beads Issue Tracker

This project uses **bd (beads)** for issue tracking. Run `bd prime` to see full workflow context and commands.

### Quick Reference

```bash
bd ready              # Find available work
bd show <id>          # View issue details
bd update <id> --claim  # Claim work
bd close <id>         # Complete work
```

### Rules

- Use `bd` for ALL task tracking — do NOT use TodoWrite, TaskCreate, or markdown TODO lists
- Run `bd prime` for detailed command reference and session close protocol
- Use `bd remember` for persistent knowledge — do NOT use MEMORY.md files

## Session Completion

**When ending a work session**, you MUST complete ALL steps below. Work is NOT complete until `git push` succeeds.

**MANDATORY WORKFLOW:**

1. **File issues for remaining work** - Create issues for anything that needs follow-up
2. **Run quality gates** (if code changed) - Tests, linters, builds
3. **Update issue status** - Close finished work, update in-progress items
4. **PUSH TO REMOTE** - This is MANDATORY:
   ```bash
   git pull --rebase
   bd dolt push
   git push
   git status  # MUST show "up to date with origin"
   ```
5. **Clean up** - Clear stashes, prune remote branches
6. **Verify** - All changes committed AND pushed
7. **Hand off** - Provide context for next session

**CRITICAL RULES:**
- Work is NOT complete until `git push` succeeds
- NEVER stop before pushing - that leaves work stranded locally
- NEVER say "ready to push when you are" - YOU must push
- If push fails, resolve and retry until it succeeds
<!-- END BEADS INTEGRATION -->
