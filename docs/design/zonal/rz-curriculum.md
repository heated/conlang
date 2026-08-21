# Curriculum-shaped grammar (exploration, 2026-08-22, conlang-i78)

Question: if every lesson must leave the learner *immediately more
able to parse real text*, what does RZ's first day buy? Computed by
`tools/coverage.py` (`LESSON_PLAN` + `lesson_curve`) over the
de-duplicated 690-token corpus. Lesson hours are model estimates [H];
coverage is computed **from the explicit lemma sets each block
teaches**, not from a frequency curve with lesson labels pasted on
(that was the first version's error, caught in review).

| cumulative hours | lesson block | open lemmas known | tokens parseable |
|---|---|---|---|
| ~1 | closed-class block (60 words) + spelling/stress | 0 | **45.2%** |
| ~2 | + complete verb system + top-20 lemmas | 20 | **56.7%** |
| ~4 | + next 54 lemmas + derivation families | 74 | **72.6%** |
| ~6 | + number mode + calendar + next 48 lemmas | 122 | **79.6%** |
| ~10 | + topic packs (95 more lemmas) | 217 | 93.3% (in-corpus) |
| ~14 | + tail to corpus edge | 241 | 96.8% (in-corpus) |

Two honesty notes carried in the tool's output:

- **Skills that add no token coverage are marked as such.** The verb
  paradigm, the derivation families, the number mode and the calendar
  are real lesson content, but they multiply what a learner can do
  with lemmas already counted (or live outside running text
  entirely). Only the lemma sets move the coverage column.
- **Rows ≥10h flatter.** In-corpus coverage overstates the real-world
  curve, and the corpus cannot fix that: the Zipf fit is too shallow
  at this sample size to size the tail at all
  (rz-lexicon-coverage.md). The robust part is the head — half the
  tokens in the first hour, and one exceptionless verb table.

Design observations:

1. **The curriculum is a coverage-greedy sort, and RZ's design makes
   that sort teachable.** Natural-language curricula can't front the
   closed class as one block — agreement and conjugation force
   grammar to interleave with vocabulary from lesson one. RZ's
   invariant particles and person-invariant verbs make the greedy
   order actually deliverable.
2. **Every engineered subsystem is a self-contained lesson unit**
   (number mode ~2h, repair mode ~1h, script ~3-5h, chording
   competence ~5-10h): they slot anywhere after hour 2 with no
   dependencies — modular electives, not curriculum spine.
3. **Curriculum shape is itself a design criterion** for the GZ
   bake-off: a scheme that raises total capability but flattens the
   first-ten-hours curve (an E-scheme remap taxing the Romance
   cohort's sight recognition early) trades against the strongest
   adoption asset the zonal strategy has — the first evening. Measure
   candidate schemes by coverage-at-hour-N, not just total hours.

Status: exploration artifact; parse-side only (production curriculum
is dominated by the automatization hours the ledger already carries).
Feeds conlang-z0s (bake-off criterion) and any future primer work.
