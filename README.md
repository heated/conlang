# conlang

An engineered constructed language optimized for one thing: **learning
speed** — with fast chorded typing and rapidly-acquired reading falling out
of the same architecture for free.

The core idea: treat a syllable as a vector of independent channels
(onset × vowel × coda × register) and engineer over that space —
coding-theoretic error correction in the lexicon, a Hangul-style featural
script whose glyphs are their own pronunciation guides, self-segregating
morphology, and dense closed-domain "modes" for numbers, dates, and times.
Glyph, chord, and sound are three renderings of the same channel vector:
learning any one teaches the other two.

The language's name is intentionally undecided until the phonaesthetics
pass; `conlang` is a working handle.

## Layout

- `docs/design-brief.md` — the north star: goals, architecture, tiers,
  key numbers, decisions on record.
- `docs/archive/` — provenance: the original design conversation.
- `docs/spec/` — the versioned language specification (frozen core).
- `paper/` — living research paper, grows with the build.
- Issue tracking lives in [beads](https://github.com/steveyegge/beads)
  (`.beads/`), not GitHub issues.

## Status

Early: design brief and roadmap are in place; the Tier-1 core spec
(channel inventory, error correction, morphology) is being written and
frozen first. Everything else budgets against it.
