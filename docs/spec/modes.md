# Mode Subsystems — Tier-2 Specification

**Version:** 0.2.0-draft · **Status: NOT FROZEN.** Mode particle
assignments are **PROVISIONAL** until conlang-jbw fixes the particle
budget; the digit-pair code itself is frozen with the core (SPEC §10).

Encoders, frame decoders, and checksum verification: `tools/modes.py`.
Every table below marked *(generated)* is produced by a `tools/modes.py`
subcommand and asserted **verbatim** by `tools/test_modes.py` — the doc
cannot drift from the code.

## 1. Design principles

1. **Payloads carry the anti-check value in the written layer**
   (SPEC §4.2; since v0.2 the check is a written-layer channel, so this
   marking serves text and machines — casual speech carries no check at
   all). Spoken mode integrity rests on mode *boundaries*, the frame
   grammar, and the checksum — which is why **no payload symbol may use
   the h onset** (an h-shaped payload would differ from a particle only
   by the written check; see §5). With dates at digit-pair syllables
   (learnability beats monosyllable dates — Edward directive), no mode
   needs more than the 200 content-shaped payload points per syllable.
2. **Everything is the one digit-pair code.** No month tables, no hour
   tables: dates reuse the SPEC §10 pairs verbatim; time adds two
   orthogonal rules to the same grid. Learning all core modes ≈
   learning the digit pairs once.
3. **Modes win for payloads of two or more syllables**; casual speech
   uses lexical number words for small counts.

## 2. Frame grammar

```
frame  := particle payload* [close]
close  := haas | hoos checksum-symbol
chunked:= (pair+ hoos checksum-symbol haan)* pair+ hoos checksum-symbol
number := hu pair+                      (base-100, big-endian)
date   := ho pair pair                  (yearless: month, day)
        | ho pair{4} | ho pair{5}       (year 4 or 6 digits + month + day)
time   := hi cell [offset-pair [seconds-pair]]
spell  := he letter+
```

Date wire rule: years are 0-padded to 4 digits (`0026` keeps its
leading pair); payload lengths of 2, 4, or 5 pairs are the only legal
date frames, so year-bearing and yearless dates are length-separated.
Variable-length modes (number, spell) terminate at the close particle,
at a non-payload token, or at utterance end; fixed-shape modes (date,
time) terminate by length.

## 3. Mode particles *(generated: `tools/modes.py particles`)*

| particle | canonical | mode |
|----------|-----------|------|
| h-u | `huu` | number: digit pairs follow, base-100, big-endian |
| h-o | `ho` | date: [year pairs ×2-3] + month pair + day pair |
| h-i | `hii` | time: one hour×quarter syllable [+ offset pair [+ seconds]] |
| h-e | `he` | spell: one letter-name syllable per letter |
| h-e-n | `heen` | phonetic mode — reserved, mechanism only in v0.1 |
| h-i-n | `hin` | coordinates — reserved, design sketched below |
| h-a-s | `haas` | mode close (optional in casual speech) |
| h-o-s | `hoos` | mode close + checksum symbol follows |
| h-a-n | `haan` | chunk separator: next chunk of the same payload (also the residue-100 escape) |

Nine of the twenty particle slots. conlang-jbw budgets the remaining
twelve for grammar; if grammar overflows, mode particles migrate to
coda-bearing slots first.

## 4. Times

One syllable per Edward's directive, as a pure grid over the digit code:
**onset** = digit onset of the hour's last digit; **coda** = hour tens
(∅ = 0x, n = 1x, s = 2x); **vowel** = quarter (a = :00, e = :15,
i = :30, o = :45; u reserved). Exact times append a minute-offset pair
(00–14), then optionally a seconds pair. A decoder knows the first
payload syllable after `hii` is a time cell and any following symbols
are offset pairs — roles are positional per the frame grammar, so the
structural overlap between time cells and digit pairs (80 of 96 cells)
is not an ambiguity.

## 5. Spell mode *(letter table generated: `tools/modes.py letters`)*

| letter | rendering | letter | rendering |
|--------|-----------|--------|-----------|
| A | `cal` | N | `ne` |
| B | `paa` | O | `col` |
| C | `ce` | P | `pee` |
| D | `ta` | Q | `ku` |
| E | `cel` | R | `laa` |
| F | `wa` | S | `see` |
| G | `kaa` | T | `te` |
| H | `kaal` | U | `cuul` |
| I | `ciil` | V | `we` |
| J | `je` | W | `wuu` |
| K | `kee` | X | `saa` |
| L | `lee` | Y | `ja` |
| M | `mee` | Z | `su` |

Design rules: onset-matching consonants use onset + e; the five vowel
letters use c + vowel + coda l (c as a neutral carrier; coda l never
occurs in digit rimes); remaining consonants take a nearest-sound onset
+ a (or + u where + a is taken); **no letter uses the h onset** — an
h-shaped payload differs from a mode particle only by the written-layer
check, which speech does not carry, so h-shapes are banned from all
open-ended payloads. Table is PROVISIONAL pending a naive-listener
confusion pass.

## 6. Coordinates (reserved sketch)

`hin` + hemisphere marker + degree digit pairs per axis. Not normative
in v0.1; deliberately unimplemented until the safety register profile is
exercised, since coordinates are a safety-register payload almost by
definition. Hemisphere markers will come from the spell letters
(N/S/E/W), not from h-shapes.

## 7. Worked examples *(generated: `tools/modes.py examples`)*

| value | rendering |
|-------|-----------|
| 42 | `huu cii` |
| 4207 | `huu cii mu` |
| 4207 with checksum | `huu cii mu hoos pas` |
| 0 | `huu maa` |
| 1000000 | `huu muun maa maa maa` |
| date 2026-08-08 | `ho ta taas miis miis` |
| date 08-08 (yearless) | `ho miis miis` |
| time 14:30 | `hii cin` |
| time 14:37 | `hii cin mu` |
| time 08:00 | `hii wa` |
| time 23:45 | `hii los` |
| spell NTNU | `he ne te ne cuul` |
| spell ZOE | `he su col cel` |

Every doc example is round-tripped through the frame decoder at
generation time. For comparison: "four thousand two hundred and seven"
(~10 English syllables) vs `huu mi cin` (3); "August eighth, twenty
twenty-six" (~9) vs `ho ta teen coon coon` (5); "half past two pm" vs
`hii miin` (2).

## 8. Checksum

Every payload symbol has a **checksum value ≤ 100**: digit and offset
pairs use the pair value, a time cell uses 4·hour + quarter-index
(0–95), letters use A=0…Z=25. The checksum is the position-weighted sum
Σ (i+1)·vᵢ mod **101** over the payload, frames capped at 100 symbols,
emitted as one symbol after `hoos` (values 0–99 as a digit pair). **Residue 100 has no symbol**: the v2 sparse codebook spends its margin, so no clean 101st syllable exists (`cas` is now digit 36). Instead residue 100 is made unreachable — a payload whose residue is 100 is split at the latest point where no chunk has residue 100, chunks joined by `haan`, each carrying its own checksum. A split always exists because a single pair's residue is its own value ≤ 99. Cost: ~1% of checksummed payloads pay one separator plus one extra checksum syllable. Because 101 is prime and strictly exceeds every legal value and
every position weight, **every single-symbol substitution within a
symbol class and every transposition — adjacent or not — changes the
checksum** (both deltas are products of nonzero residues mod a prime).
This replaces an earlier mod-97 design whose ±97 value deltas were
silent. `tools/test_modes.py` proves the claim exhaustively for
substitutions and all transpositions at the tested lengths.

## 9. Error budget and register profiles

The v2 digit codebook is **sparse**: 100 of the 200 content-shaped payload points, so a single-channel corruption often lands outside the codebook and the frame grammar catches it (280 of 1600 vs the dense code's 200 — a free detection gain from the spacing choice). Generated analysis *(generated: `tools/modes.py confusion`)*:

> total single-channel corruptions: 1600; silent digit substitutions: 1320 (82%); caught by the frame grammar: 280; silent but register-flagged: 780 (59% of silent)

(The register-flagged fraction is a written-layer and careful-register
property in v0.2; casual spoken digits rely on the frame grammar,
checksum, and repair.) The checksum is therefore load-bearing, not
decorative. **Register
profiles:** casual — checksum optional, conversational repair does
correction. Careful/readback — repeat the payload. Safety-critical —
checksum mandatory, fortified realizations for the known-weak digit
cells (SPEC §10), and a dedicated careful-register digit readout
("niner"-style distinct digit names) remains an open design item
tracked here.

## 10. Relation to the frozen core

Modes consume: the digit-pair assignments (SPEC §10, freeze
candidate), the written-layer anti-check convention (SPEC §4.2 v0.2 —
itself subject to the tentative check-demotion decision, which this
document tracks), and eight provisional particle slots. The h-onset
payload ban (§5) is a modes policy, not a core change. Nothing here
constrains the lexicon beyond the current SPEC draft.
