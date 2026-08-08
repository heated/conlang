# Alternative: natural-grade emergent redundancy (no parity register)

**Status:** exploration (beads conlang-zec); recommendation at the end.
Experiment: `tools/explore_noparity.py`; results:
`.ship-notes/noparity-results.json` (not committed; regenerate).

## The proposal

Drop the engineered inner code from the core lexicon entirely — no check
bit, no computed register, no mandatory concord. A syllable is just
onset × vowel × coda (220 codepoints, 200 content + 20 particle). The
core's protection against mishearing comes from what natural languages
use: sane phonotactics, SSM word templates, a lexicon that occupies its
space *sparsely* (the humility to not min-max word length), context, and
conversational repair. Engineered redundancy survives only where it
demonstrably pays: the mode system's frame grammar and checksum.

## Why this became attractive

Both reviews of the core spec already whittled the register down: the
original "distance-2 parity" claim was false; the repaired check-bit
design was honestly billed as a *careful-register and machine-facing*
feature, inaudible to length-deaf listeners; its carrier (vowel length)
is the least perceptible channel, interacts with stress and phrase-final
lengthening, and — carrying zero lexical load — is exactly the kind of
contrast natural speech erodes. The remaining question was whether its
detection value justified its costs. The experiment answers that.

## The experiment

Matched lexicons (monosyllable assignment by exact MIS + ~800 sampled
disyllables kept at distance ≥2, which the huge disyllable space makes
free), Zipf-weighted words, single-channel substitutions weighted by
confusion class, two listener models. Architecture A = current spec
(check-bit register; assignment licenses "covered" minimal pairs because
the register audibly differs). Architecture B = no register; assignment
refuses high-confusion minimal pairs outright ("humility" policy).

Silent-substitution rate (a mishearing that lands on another legal word,
undetected — i.e., wrong meaning delivered):

| | length-sensitive listener | length-deaf listener |
|---|---|---|
| **A** (check-bit, current) | 3.5% | **20.4%** |
| **B** (no parity, humility) | 3.7% | **3.7%** |

Robust across error-model weights (at uniform substitution
probabilities: A-deaf 34% vs B 16%; the ordering never changes).

**The mechanism is damning for A.** A's assignment packs covered
minimal pairs (pa/ta, e/i neighbors…) into the highest-frequency words
*because* the register catches the substitution — but only for listeners
who can hear length. For everyone else, A concentrates the most
confusable pairs exactly where traffic is highest. Parity's ~17-point
marginal protection for sensitive listeners is mostly protection from
the danger its own licensing created: under B's assignment there is
almost nothing left for a register to catch (3.7% residual, nearly all
in the disyllable tail).

## What B wins beyond the numbers

1. **Production accessibility.** A requires every speaker to *produce*
   correct vowel length on every syllable; speakers of length-less L1s
   (Spanish, French, Italian, Mandarin…) will emit noisy registers,
   triggering false alarms in others' error detectors. B asks nobody to
   produce or perceive length, ever. The current design quietly violated
   its own "no distinction your L1 didn't give you" principle on the
   production side.
2. **Stress gets duration back.** With length freed, word-initial stress
   can be realized naturally (pitch + intensity + **duration**), making
   the SSM boundary signal strictly stronger — duration is one of the
   most robust stress cues cross-linguistically. This directly answers
   the language review's concern about stress detection under degraded
   conditions.
3. **Simpler everything.** No vowel doubling in romanization; one fewer
   visual zone in the featural script and one fewer input axis in the
   chord/touch layouts (or: kept as expansion headroom); no CVVC
   superheavies; no unstressed-long-vowel realization questions; the
   spec's §4 shrinks by half. Learning-surface reduction is on-goal.
4. **No erosion time bomb.** A zero-load length contrast invites
   generational erosion; B has nothing to erode.

## What B costs, honestly

1. **Monosyllable capacity: 22 bodies vs 34** (the humility policy
   refuses covered minimal pairs). After the 30% reserve: ~15 initially
   assignable short forms vs ~23. Eight fewer words get monosyllables;
   they go disyllabic. Given the language is disyllable-dominant either
   way, this is a mild word-length tax on ranks ~15–23 of the frequency
   list.
2. **Machine-layer integrity.** A's computed register lets a machine
   validate every syllable in isolation; B's machines validate against
   the lexicon and frame grammar instead (ordinary ASR practice). The
   payload complement's "self-flagging" disappears — but reviews already
   demoted that to a register-sensitive-only property; mode integrity
   lives in the frame grammar + mod-101 checksum, which are untouched.
3. **Careful-register detection for sensitive listeners.** In A, a
   length-sensitive listener hears 67% of substitution events as audibly
   malformed *before* any lexical lookup. In B, detection routes through
   the lexicon. Equal silent rates, but A's detections are earlier and
   more locatable — worth something in high-noise readback settings.
   Counterpoint: the safety register's mandatory checksum already covers
   exactly those settings.

## Impact if adopted (pre-freeze, so cheap)

- `channels.json`: delete registers, check bits, covered/residual
  machinery; `confusion_policy` becomes pure assignment data (the
  humility tier). Spacing rules, glide cells, coronal-i, echo-vowel,
  tosmabru, SSM, POS coda: all unchanged.
- Modes: frame grammar and checksum unchanged; payload syllables lose
  anti-check marking (mode particles were already the real boundary).
  Digit/time/letter codes unchanged.
- Script/input beads: one fewer channel to render (or reserve the zone).
- Spec §4 rewritten around emergent redundancy + assignment policy;
  §2.4 deleted; romanization loses doubling.
- The paper's error-correction contribution reframes as *measured,
  steered emergent redundancy* — more defensible than the algebraic
  story the reviews already forced us to qualify twice.

## Recommendation

**Adopt B for the core lexicon.** The check-bit register fails its own
accessibility test: it protects the listeners who least need it while
actively endangering the length-deaf majority the project optimizes for,
and its production burden violates the design's founding principle. The
engineered-redundancy machinery earns its keep only in the mode system
(frame grammar + checksum), where it should remain. Capacity cost is a
mild word-length tax; every other effect is simplification.

This changes the frozen-core candidate — it is Edward's call
(architecture gate, tracked with the freeze decision conlang-w77).
