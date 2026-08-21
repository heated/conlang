# Curriculum-shaped grammar (exploration, 2026-08-22, conlang-i78)

Question: if every lesson must leave the learner *immediately more
able to parse real text*, what does RZ's first day buy? Computed
from the coverage counters (tools/coverage.py) with model lesson
times [H]; receptive (parse) coverage of running corpus tokens:

| cumulative hours | lesson block | tokens parseable |
|---|---|---|
| ~1 | closed-class block (62 words) + spelling/stress | **49.4%** |
| ~2 | + complete verb system (one table) + top-20 lemmas | **61.5%** |
| ~4 | + next 54 lemmas + the derivation families | **74.8%** |
| ~6 | + number mode + calendar + next 48 lemmas | **84.8%** |
| ~10 | + 95 more lemmas (topic packs) | 95.0% (in-corpus) |
| ~14 | + tail to corpus edge | 97.5% (in-corpus) |

Honesty: rows ≥10h flatter — in-corpus coverage overstates the
real-world curve (rz-lexicon-coverage.md: the 95% band is ~500
lemmas by Zipf, so real-world hour-10 is nearer ~85-90%). The
robust part is the head: **half the language in the first hour is
a structural fact** (closed-class share), and the whole verb
system genuinely is one exceptionless table.

Design observations:

1. **The curriculum is a coverage-greedy sort, and RZ's design
   makes that sort steep.** Natural-language curricula can't front
   the closed class as one block (agreement and conjugation force
   grammar interleaving); RZ's invariant particles and one-table
   verbs make the greedy order actually teachable.
2. **Every engineered subsystem is a self-contained lesson unit**
   (number mode ~2h, repair mode ~1h, script ~3-5h, chording
   competence ~5-10h): they slot anywhere after hour 2 without
   dependencies — modular electives, not curriculum spine.
3. **Curriculum shape is itself a design criterion** for the GZ
   bake-off: a scheme change that raises total capability but
   flattens the first-10-hours curve (e.g. an E-scheme remap
   taxing the Romance cohort's sight-recognition early) trades
   against the strongest adoption asset the zonal strategy has —
   the first evening. Measure candidate schemes by
   coverage-at-hour-N, not just total hours.

Status: exploration artifact; parse-side only (production
curriculum is dominated by the automatization hours the ledger
already carries). Feeds conlang-z0s (bake-off criterion) and any
future primer/lesson work.
