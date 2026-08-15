# The width ladder: variants wider than GF-W (conlang-4h1)

Numbers from `tools/explore_wider.py` — real lexgen runs on
programmatically widened specs, humility coverage applied to every
added contrast. Exact MIS for small graphs; `>=` rows are multi-start
greedy **lower bounds**. Calibration: greedy gives >=34 where GF-W's
exact answer is 38, so true values run ~10% above the bounds.

## The ladder [M]

| rung | inventory | content syl | mono roots (adopted-MIS) |
|---|---|---|---|
| GF-N | 10 on x 5 nuc | 200 | 22 (exact) |
| GF-ND | 10 x 8 (+ai au oi) | 320 | >=28 (~31 est) |
| GF-W | 16 on (+b d g f z r) x 5 | 320 | 38 (exact) |
| GF-X | 19 on (+v sh dj) x 5 | 380 | >=36 (~40 est) |
| GF-WD | 16 x 8 | 512 | >=48 (~53 est) |
| GF-XD | 19 x 8 | 608 | >=55 (~60 est) |
| GF-C | 31 onset units (+12 stop-liquid clusters) x 8 | 992 | >=85 (~93 est) |

"Content syl" = onsets × nuclei × 4 codas: the count of distinct
pronounceable content syllables (the 4-coda factor included). "Mono
roots" is much smaller than "content syl" because (a) roots are
bodies (onset×nucleus) — the coda dimension is spent on the POS
channel, ×4 word-forms per root, and (b) the humility MIS discards
~55-60% of bodies for confusion robustness.

Two independent dials (onsets, nuclei) plus the cluster dial — the
rungs form a lattice, not a line. Every rung is a **superset** of the
rungs below it on both dials, and modes/digits stay on the narrow 10
onsets everywhere: a mode frame spoken in any rung is valid in all.

## What each dial costs [D]

**Diphthongs (ai au oi) — the cheapest capacity on the board.**
Near-universal: most L1s have ai/au-like sequences or transparent
a+i composition; no new vowel qualities. GF-ND matches GF-W's 320
syllables while keeping the 10-consonant universal floor intact —
if the narrow bet's universality is the point, this is the rung that
widens without betraying it. Costs: diphthong syllables are longer
in duration (capacity is not free in seconds), and the hook dividend
is vowel-shaped only (*aire, auto, causa* come back; *forte* still
doesn't). Covered: ai/a ai/e, au/o au/a, oi/o oi/e, ai/oi
(monophthongization cohorts).

**Onsets past GF-W (+v sh dj).** Diminishing returns: +3 onsets buys
only ~2-4 roots because the newcomers arrive densely covered (v
against w/b/f; sh against s/c — and sh requires tightening c's
licensed [ʃ] drift; dj against c/j/z/d). The onset dial is near
saturation after GF-W; th/x/ng were rejected outright (th rare, x
collides with the h particle channel, ng un-onsetable for many).

**Clusters (12 stop/f+liquid) — the big rung.** ~93 roots is "the
whole conversational core plus most of Swadesh, monosyllabic," and
the hook dividend maxes out: *grande, libro, tren, forte, fror->flor*
fit as-is; word shapes converge on Romance. Price: CJK/Austronesian
phonotactics. The engineered mitigation is **licensed epenthesis**:
declare cluster ~ C-echo-vowel-C as a licensed realization (gurande
IS grande), which moves the cost from "some speakers can't say it"
to "each cluster root shadows its epenthesized disyllable" —
i.e. it spends *disyllable* inventory, not monosyllable count. That
cross-length conflict is NOT yet in the model: treat the GF-C row as
an upper bound in that respect. Modeling it = extending
echo_vowel_conflict to onset position (bounded, known work).

## Axes explicitly rejected [D]

- **Vowel qualities (e/ɛ, o/ɔ, ə):** prices out the entire 5-vowel
  world (Spanish, Japanese, Swahili, Greek...) for modest capacity;
  the 5-vowel floor is the single most universal thing in the spec.
- **Contrastive length in content words:** structurally blocked —
  vowel doubling is already the written register/check machinery
  (`parse_word` treats a doubled vowel as a register assertion), and
  particles already spend length on robustness (haan/hoon/huul).
  Repricing doubling would cost the check channel to buy nuclei.
- **Tone/pitch accent:** production floor for non-tonal L1s violates
  learnability-first; also breaks the superset tower (existing forms
  would need tone assignments; "default tone" recovers supersets but
  then tone-bearing forms are second-class).
- **h-onset content words:** h is the particle channel; spending it
  on content buys ~5 bodies and costs the cleanest structural signal
  in the language.
- **More codas (-m, -k, -r...):** widens the *grammar* channel, not
  the root space — a 5th coda is a 5th POS projection per root, a
  different dial entirely (interesting for a derivational channel;
  out of scope for the width question).

## What humility costs, and what natural languages do instead [M]/[H]

The adopted MIS is a *guarantee* (no two unrelated monosyllables one
confusable substitution apart), not a capacity ceiling. Relaxing to
the pre-adoption forbidden-only policy (computed, same machinery):

| rung | humility MIS | forbidden-only MIS | ×4 codas = word-forms |
|---|---|---|---|
| GF-N | 22 | 34 | 136 |
| GF-W | 38 | 58 | 232 |
| GF-WD | >=48 | >=103 | 412 |
| GF-C | >=85 | >=208 | 832 |

Natural-language syllable inventories for scale (ballparks,
TODO-verify against primary phonotactic surveys):

| language | ~distinct syllables | how |
|---|---|---|
| Hawaiian | ~160 | tiny inventory, CV only |
| Japanese | ~110 morae / ~400 syl | tiny inventory, CV(n) |
| Mandarin | ~410 segmental, ~1,300 with tone | tone triples capacity; heavy homophony (~12 morphemes/toned syl in running lexicon) |
| Spanish | ~1,500-3,000 | clusters, codas |
| English | ~10,000-16,000 attested | ~24 C onsets + rich clusters, ~15 nuclei, coda clusters (CCCVCCC: *strengths*) |
| GF-N / GF-C | 200 / 992 | this ladder |

English's 10k+ is bought with exactly what we priced out: giant
onset/coda cluster inventories (brutal for most L2 cohorts) and ~15
vowel qualities. Mandarin's effective capacity is bought with tone
(rejected) **plus massive homophony** — natural languages let
context do error correction after the fact; the humility policy
buys it up front and pays in capacity. Three stacked disciplines
account for the whole gap: small universal inventory, the coda
dimension spent on grammar instead of lexicon, zero
homophony/near-pair guarantees.

The design consequence is Mandarin's, deliberately: the language is
**disyllable-shaped** (~70% of Mandarin words are disyllabic
compounds). Monosyllables are the elite frequency band everywhere —
English puts its top few thousand words there; GF puts its top
~90-370 forms there and composes the rest in a disyllable space that
is effectively unbounded (hundreds of thousands of legal
combinations before rules). The scarce resource was never "words";
it is "words of length one."

## Where the ladder ends [H]

The limit of widening is RZ: unrestricted natural-syllable shapes,
maximal hooks, zero engineered floor. Each rung up trades universal
floor for density+hooks and lands closer to Romance word shapes —
GF-C is recognizably "RZ with channel discipline." So **width is not
a binary door (GF-N vs GF-W); it is a position on the GF<->RZ
axis**, and the real decision is which 1-2 points on that axis the
project commits to. The superset tower makes a nested pair cheap:
e.g. GF-N core ⊂ GF-WD extension — one lexicon discipline, two
communities, lower rung always valid in the upper.

Recommendation to price further (not adopted): **GF-WD** as the
preferred upper point if one is taken — it collects the two cheap
dials (wide onsets + diphthongs, ~53 mono roots, 512 syllables)
while stopping short of the cluster rung's phonotactic bill and
unmodeled cross-length costs.

## Status

Computed sketch; nothing adopted. Feeds the width one-way door
(tradeoffs.md) — the door is now "pick a point (or nested pair) on
the ladder," not "narrow vs wide." Next if pursued: exact MIS for
the starred rungs (better solver), cluster epenthesis modeling,
GF-WD seed-lexicon pass to see the hook dividend at assignment level.
