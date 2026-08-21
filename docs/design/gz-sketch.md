# GZ: the greenfield zonal (Edward directive 2026-08-15, conlang-z0s)

Target adopted for "the GF-W we go with": **grab the low-hanging
channel fruit from a Romance-ish base, then only loosely reuse
roots.** This is a new design point — the width ladder
(width-ladder.md) varied the *inventory* dial while holding channel
*discipline* at maximum; GZ moves on the discipline dial at
near-Romance inventory. The design space is 2D:

```
discipline
  full   | GF-N ── GF-W ── GF-WD ── GF-C
         |                            \
  medium |                             GZ   <- target
  light  |                              \
  none   |                               RZ
         +---------------------------------> inventory width
           10 on          31 units      full Romance
```

GF-C approached GZ from the engineered side ("RZ with channel
discipline"); GZ approaches from the zonal side ("RZ plus the
channels that come cheap"). Nearest precedents: Esperanto (POS-vowel
channel on a European base — the existence proof that this fruit is
real and load-bearing) and Ido (the same, with more Romance-natural
shapes). GZ differs from both by: zonal fidelity as an explicit
measured dial (cloze against the incumbent), the humility *screen*,
script-layer channels, and the mode/digit subsystem.

## Syllable space [M]/[D]

GZ inherits its syllable inventory from the base instead of
designing it. Measured over the RZ six-register corpus (blockquote
text only, glosses stripped; rough onset-maximal syllabifier):
335 word tokens → **171 distinct syllables attested**, drawn from
29 onsets (incl. clusters pr/tr/bl/st...), 14 nuclei (5 vowels +
rising diphthongs), 8 codas (∅ n s l r m + marginal). Cartesian of
attested channels ≈ 3,200; the realistic legal space after
phonotactic pruning is **~2,000-3,000 syllables** — the Spanish
band of the width-ladder comparison table, ~10x GF-N, ~2.5-3x GF-C.
None of it is reserved: no MIS, no capacity tax; the screen prunes
pairs, not space.

## The channels GZ keeps (the fruit) [D]

Spoken: (1) **POS ending channel** — the E/R/M scheme decision;
(2) **particle/clitic closed class** — all grammar words are the
unstressed clitic set (le les a de no va se...), already RZ
practice, GZ makes it a hard class boundary; (3) **fixed penult
stress** — the SSM-lite word-boundary parse; (4) **modes/digits**
— pending the escape-phoneme decision (RZ h is silent).
Display-only: (5) **featural script channels** — place/manner
letterform families, the voicing ground bar, suffix + function-word
logograms (all built and tested in rz_script), plus POS marking in
script under the R/M schemes. Constraint, not channel: (6) the
**humility screen** — dangerous minimal pairs blocked at assignment
(false-friend machinery generalized). Dropped from speech: the
check bit and MIS spacing (script redundancy can carry the former).

## Channel widths and space accounting [M]/[D]

Measured on the RZ blockquote corpus (335 tokens). "Width" = values
the channel distinguishes; "space" = what it consumes of the ~2-3k
legal syllable space.

| channel | width | space consumed |
|---|---|---|
| POS/TAM ending (E-scheme) | ~6 values (-o/-a/-e/-ar/-as/-is), ~2.6 bits/word | compresses content-word final rimes 29 attested → 6 (~80% of final-rime diversity spent on the channel). Measured dividend: **63% of content tokens are already E-scheme-shaped** — Romance final vowels do most of the work for free |
| particle/clitic class | binary flag/word + 26-member closed list (38% of tokens) | ~26 short forms ≈ 1% of syllable space; **no structural reservation** — GF pays 1/11 of onset space (h-) for a perfect marker, GZ pays ~0 and gets a stress/position-carried (probabilistic) marker |
| penult stress | 1 boundary per word (demarcation, not values) | zero segmental space |
| modes/digits | 100 values/syllable inside frames (tens×units) + frame ops | **the vacant h-region** — see below; zero lexicon cost |
| featural script (display) | place(~5)×manner(~4)×voicing(2) per letter | zero new bits — structured redundancy of the phoneme identity |
| logograms (display) | 16 function-word + 4 suffix marks | display only |
| humility screen | 0 (constraint) | blocks pairs, not space |

Aggregate utilization: the corpus attests 171 of ~2,500 legal
syllables; a mature GZ lexicon plausibly uses 500-800. The channels
consume: final-rime space (E-scheme only), ~26 particle forms, and
one vacant onset region. Everything else stays lexical.

## Modes in the silent-h hole [D — proposal, tentative]

RZ declares h silent — which means the **h-onset region of syllable
space (14 nuclei × 8 codas = 112 cells) is orthographically vacant**:
no Romance-derived word occupies it. Proposal: mode frames colonize
it. [h] is dead in the lexicon but LIVE in mode frames — spoken,
aspirated, the escape phoneme. 112 cells ≥ 100 digit values + frame
operators; the greenfield mode DSL transfers with tens/units remapped
onto nucleus × coda. Honest cost: h-dropping L1s (French) must
*produce* [h] in frames — mitigated by [h]~[x] licensing (Spanish
speakers' natural repair) and by frames being prosodically marked +
checksummed anyway. This resolves the escape-phoneme decision at
zero cost to the inherited lexicon; flagged tentative until a frame
sample survives reading aloud.

## GZ vs RZ, current delta [D]

RZ optimizes one thing: receptive recognizability to the zone —
channels live only in its display script. GZ spends recognizability
to buy spoken structure. The deltas as of this sketch: fixed penult
stress (RZ inherits source stress); particle class as a hard
boundary (RZ has clitics by habit); POS endings per E/M scheme (RZ
keeps natural endings — 63% incidentally E-shaped); modes/digits in
the silent-h hole (RZ has none); root fidelity as a spendable
budget (RZ treats fidelity as the point). Shared: phonology,
screen machinery, script (GZ adds POS marks), RZ lexicon as donor.
Status asymmetry: RZ is a built language (grammar, ~380 entries,
six-register corpus, tested script); GZ is this sketch. UPDATE
(2026-08-21): RZ has tentatively adopted the number mode in the
silent-h hole (rz-number-mode.md, Edward directive) — RZ now
carries one engineered spoken subsystem, i.e. it has taken the
first step onto the GZ-R path. Under the
R-scheme GZ collapses to nearly "RZ + discipline"; under E it is a
visibly different language with an RZ-shaped vocabulary.

## The fruit, priced [D]

| channel | on a Romance base | price |
|---|---|---|
| POS endings (the Esperanto move) | CHEAP and proven: deterministic final-vowel/ending marks POS | the central dial — see below |
| particle/clitic closed class | CHEAP: Romance already has it (RZ clitics); discipline = particles are exactly the unstressed class | near zero |
| fixed stress (SSM-lite) | CHEAP: penult-always (Polish-proven); word boundaries recoverable | some shapes shift vs source (*teléfono*→*telefóno*) |
| humility as SCREEN (not MIS) | CHEAP: RZ's false-friend screen generalized — block only *dangerous* minimal pairs at assignment; no capacity sacrifice | keeps homophony/near-pairs a curated risk, not a guarantee |
| script-layer channels | FREE-ish: rz_script already does featural letterforms + voicing bar + suffix logograms; POS color/mark in display costs speech nothing | display-only |
| modes / digit syllables | NOT cheap: RZ's h is silent; mode frames need an escape phoneme that Romance ears keep distinct | decision needed: stressed frame word vs restoring [h] vs a click-free alternative |
| check bit | NOT cheap on inherited roots (they don't respect parity) | drop from speech; script can carry redundancy instead |

## The central dial: endings vs recognizability

Deterministic POS endings do violence to Romance shapes (*sol*→
*solo* collides with "alone"; Esperanto's uniform -o reads alien).
Candidate schemes to price with cloze when testing unparks:

- **E-scheme** (Ido-like): -o noun, -a adj, -e adv, -ar/-as/-is
  verb. Fully deterministic; most violence.
- **R-scheme** (RZ-conservative): keep RZ shapes; POS marked only by
  the closed particle class + position + script layer. Zero violence;
  channel lives in writing and syntax only.
- **M-scheme** (middle): verbs and adverbs marked (-r/-mente
  normalized), nouns/adjectives unmarked. Marks the two classes
  whose confusion costs parsing the most.

Root policy per the directive: "only kinda reuse" — adapt the
Romance form when it fits the scheme cheaply, coin (or clip) when
it doesn't or when the screen flags it. RZ's ~380-entry lexicon is
the donor base; RZ itself remains the receptive-decoding sibling.

## Sample (M-scheme, tentative)

> Le vento del norte e le sol disputa-r hoon... — no: TAM stays RZ
> (-va past), particles stay Romance. GZ sample pending scheme pick;
> the fable goes through all three schemes as the comparison text.

## Learning-time model [H — predictions, zero subjects]

Anchors (TODO-verify): FSI ~600-750h to professional proficiency in
Spanish/French for English L1; Esperanto ~150-200h conversational;
Interlingua read-at-sight for Romance L1s.

| learner | RZ | GZ | GF-N |
|---|---|---|---|
| Romance L1 | read ~immediate; speak ~20-50h | read near-immediate; speak ~30-60h | ~100-200h, no discount |
| English L1 | ~100-150h | ~80-120h (channels speed parsing) | ~100-200h |
| non-European L1 | ~300-500h (no design help) | ~150-250h (regularity discount) | ~100-200h, flat for all |

The pattern is the portfolio logic: RZ's speed is zonal-only; GZ
keeps most of the zonal discount and extends the Esperanto-style
regularity discount outward (its case over RZ is the bottom row);
GF-N is worst-case-optimal — nobody gets a vocabulary discount,
everybody gets tiny-phonology + channels, flat across L1s, and it
beats GZ for cohorts that Romance phonotactics punish. The E<->R
scheme dial is the familiarity-vs-channels dial made explicit:
E's measured violence is ~37% of content tokens, final rime only.

## What this resolves and opens

- The width door's upper point is now GZ (tradeoffs.md updated);
  GF-N stays the engineered pole. GF-W/GF-WD/GF-C remain charted
  rungs, not targets.
- RZ's role door: resolved into "donor base + sibling" pending
  Edward's confirmation.
- Parked script work (r5y) unblocks against the GZ inventory
  (Romance-ish letters — rz_script's 18 letterforms are the base).
- Opens: scheme pick (E/R/M), mode escape-phoneme decision,
  GZ fable in all three schemes, screen run over the donor lexicon.
