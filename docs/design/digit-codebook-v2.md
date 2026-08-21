# Digit codebook v2 (Edward's revised scheme, conlang-bd3)

Directive adopted 2026-08-21. Generator: `tools/digitgen.py`
(deterministic: exhaustive C(20,10) rime search + seeded restart
hill-climb for value assignment). Spec integration is conlang-3mq
(invariant path, Codex review); until then this doc + generator are
the source of truth for v2.

## Architecture (per directive)

- **Tens → onset**, audited: surviving confusable pairs mapped to
  numerically distant values.
- **Units → 10 rimes** chosen from the 20 vowel×coda combos for
  maximal perceptual spacing (replaces vowel×register and its ∅/n
  minimal pairs).
- Codebook = **100 points sparse in 220**; error resistance on
  audible channels alone — no register trick, no extra syllables.
  The anti-parity-complement trick is dead and replaced by this.
- Registers: **casual** = bare syllables, no checksum (target:
  spoken-English-digit reliability at ~1/3 length [H — human test
  parked]); **careful/readback** = disyllabic variants for the worst
  2-3 digits (the Mandarin yāo move) + mod-101 checksum on strings.
- Delimiting: mode opens with the h-particle; **no end mark** — SSM
  stress/h-onset boundaries terminate the payload for free. Minimum
  spoken number = 2 syllables. List-separator particle for sequences.
- Unchanged: base 10, digit pairs per syllable, date/time modes
  (incl. one-syllable hour×quarter), written numbers always exact
  and check-carrying.

## Generated codebook [M — model-optimal under the spec's own confusion data]

Confusion model [D]: forbidden 1.0, covered 0.7, weighted 0.35,
unlisted same-channel 0.05, cross-channel multiplies. Design model,
not measured perception.

**Units rimes** (note: only the corner vowels a/i/u appear — the
optimizer dropped e and o entirely, deleting the e/i, o/u, a/e, a/o
confusion classes from the digit system):

| 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|
| a | un | i | an | us | in | as | u | is | al |

**Tens onsets:**

| 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|
| l | t | m | c | j | p | s | w | n | k |

Audit: every confusable pair now sits ≥3 apart; the worst offenders
got the big gaps (a/al conf 1.0 → distance 9; t/k 0.7 → 8; n/l 0.7 →
8; p/k forbidden → 4, up from 2 in the old map). Example: 42 = `ji`
(no longer `mi`).

**Cost flagged, then RESOLVED at the spec bump (2026-08-22,
conlang-3mq).** The old map was mnemonic-ordered and nearly pessimal
under the audit, and the script's letterform bases encode tens-digit
mod 4 — so audit and mnemonic looked opposed. Computed instead of
assumed: enumerating all 576 tens assignments that preserve the
mod-4 base classes and scoring them jointly shows the best
mnemonic-preserving map has **identical worst-case spacing** (min
value distance 3 over high-confusion pairs) at **15% lower
average-case** weighted spacing. Since the worst case is the safety
property the audit exists to protect, and learnability is the north
star, the **mnemonic-preserving map is adopted**:
`0=m 1=j 2=t 3=l 4=c 5=p 6=s 7=k 8=w 9=n`. The script mnemonic text
survives verbatim (base classes unchanged). The unconstrained
optimum `0=l 1=t 2=m 3=c 4=p 5=j 6=s 7=w 8=n 9=k` is recorded in
spec_check.py as the one-line flip if the mnemonic is ever dropped.

**Careful-register variant candidates** (worst residual pairs):
units 0/9 (a/al, conf 1.0 at max distance but still the hottest
rime pair) and tens 3/6 (c/s at distance 3). These are the yāo-move
targets; concrete disyllabic forms chosen at spec bump.
**SUPERSEDED by the joint optimization below: the determinate
yāo set is units 3, 5, 4, 9 (the coda side of the four bare-vs-coda
pairs).**

## Joint optimization results (conlang-1f2, 2026-08-22) [M]

`tools/digitgen_joint.py` optimizes the full 100-point codebook at
the SYLLABLE level (758 relevant pairs of 4950; cross-channel
products included) instead of per channel. Three findings:

1. **The v2 per-channel codebook was already near-jointly-optimal.**
   Joint hill-climb over (units × tens) together: min value-distance
   over high-conf pairs stays 3; weighted sum improves 0.9% via one
   tens swap (4=p, 5=j instead of 4=j, 5=p). The spec bump adopts
   the joint map; nothing else moves. The per-channel + multiplicative
   architecture priced the cross terms correctly on its own.
2. **Non-product mapping: DECLINED with numbers.** Freeing the
   bijection (any syllable → any value, breaking v = 10t+u) buys
   +8% weighted sum and ZERO worst-case gain (min distance still 3)
   — against the learnability cliff of 100 rote pairs replacing
   10+10 digit maps. The product structure stands.
3. **The acceptance proxy fails in a sharply structured way — and
   that structure IS the careful-register design.** Bar [D,
   TODO-verify]: English's worst pair (five/nine) sits at value
   distance 4; requiring no conf ≥ 0.7 pair below distance 4 finds
   exactly 40 violations = the four bare-vs-coda rime pairs
   (a/an, i/in, u/us, as/al = unit pairs 0/3, 2/5, 7/4, 6/9) × 10
   onsets, all at distance 3, none adjacent. Reading: the CASUAL
   register genuinely cannot beat English-word digits at 1/3 the
   length on ∅-vs-coda rimes — that is the price of the length
   target, and it is what the yāo-move exists for. Assigning
   disyllabic careful forms to the coda side — **units 3 (-an),
   5 (-in), 4 (-us), 9 (-al)** — kills all four pairs and passes
   the bar by construction. (Sharpened from the directive's "worst
   2-3 digits" to a determinate 4.) Casual register unchanged;
   human read-aloud test stays the real gate.

## The residue-100 splinter — decided [D]

Delegated decision. Both proposed homes fail audit:

1. **Reserved content syllable: none clean exists.** The sparse
   codebook spends the safety margin — every unused rime is one
   forbidden-level substitution from a codeword (il/ul hit bare i/u
   on the ∅/l forbidden pair; every e/o rime hits the fully-used
   a-row at conf 1.0).
2. **The h-row is full**, contra the sketch: all 20 rimes are either
   in use (particles + mode frames) or are length-twins of one
   (han~haan, hes~hees, hul~huul, hil~hiil...). A reserved h-form
   would ride a length distinction in exactly the register where
   robustness matters — and an h-onset inside the payload would
   also puncture the "h terminates the payload" invariant.

**Decision: residue 100 is made unreachable by a chunking rule.**
The list-separator particle the scheme already has doubles as the
escape: *no checksummed chunk may have residue 100; the encoder
splits the string at the latest point where it doesn't.* A split
always exists, because a single digit-pair's residue is its own
value ≤ 99. Cost: ~1% of checksummed chunks pay one separator + one
extra checksum syllable — and chunking long strings is what readback
protocols do anyway. Zero new forms, works identically for integers
and leading-zero codes (where zero-padding would have been
ambiguous), both delimiting invariants intact.

(Elegance note for the spec: mod-101 over base-100 pairs is the
alternating sum, since 100 ≡ −1 (mod 101) — detects all single-pair
errors and all adjacent-pair transpositions; ISBN's mod-11 trick,
one level up.)

## Zonal variant [D]

Same architecture; richer alphabet; digit onsets aligned with
Romance digit initials where possible for first-contact bootstrap:

| digit | onset | source | | digit | onset | source |
|---|---|---|---|---|---|---|
| 0 | z | zero | | 5 | c | cinco/cinque |
| 1 | v | un/uno (v- free, u is a rime) | | 6 | s | seis/sei |
| 2 | d | dos/due | | 7 | p | sept-/sete (s taken; p from FR sept) |
| 3 | t | tres/tre | | 8 | g | leftover (ocho is vowel-initial) |
| 4 | k | cuatro/quattro | | 9 | n | nueve/nove |

Priced honestly: the alignment puts two confusable pairs adjacent —
**d/t at 2/3 and c/s at 5/6 — because the source languages do**
(dos/tres, cinco/seis). The zonal variant trades intra-mode error
distance for guessability, exactly the zonal-vs-engineered trade in
miniature; its careful register leans correspondingly harder on the
checksum. Units rimes: same 10 as the core (all pronounceable in
the zone).

## Open items

- Joint optimization of the full 100-point codebook (current
  generator optimizes channels separately then audits jointly);
  acceptance test = confusion rate ≤ English digits — **model-level
  proxy only until human testing unparks**.
- Careful-register disyllabic forms (candidates above).
- Spec bump + modes.py rework + letterform-mnemonic decision:
  conlang-3mq.
