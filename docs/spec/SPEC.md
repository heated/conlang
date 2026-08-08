# Language Specification — Tier-1 Core

**Version:** 0.1.0-draft · **Status: NOT FROZEN** (freeze is a human
decision; downstream work may build against this draft and must absorb
pre-freeze changes)

Machine-readable inventory: [`channels.json`](channels.json) — the single
source of truth for indices, IPA values, and assignments.
`tools/spec_check.py` recomputes every number claimed below; run it after
any edit to either file.

Design rationale and provenance: `docs/design-brief.md`,
`docs/archive/2026-08-08-design-chat.md`. Working title of the language:
undecided by design.

---

## 1. The channel model

The primitive unit is the **syllable**, defined as a vector of four
independent channels:

| channel  | values | role |
|----------|--------|------|
| onset    | 11 (10 content + 1 particle) | lexical + word-class boundary |
| vowel    | 5      | lexical |
| coda     | 4      | lexical (non-final) / part-of-speech (word-final) |
| register | 2      | **parity only** — never lexical (§4) |

Everything in the language — words, glyphs, chords, digit codes — is
defined over these coordinates. The written glyph, the typed chord, and the
spoken syllable are three renderings of the same vector; none is derived
from another by convention or memorization.

## 2. Inventory

### 2.1 Onsets

Content onsets (indices are normative; they drive parity and digit codes):

| idx | roman | IPA | digit | notes |
|-----|-------|-----|-------|-------|
| 0 | c | /tʃ/ | 0 | acceptable realizations [tʃ]~[ts]~[ʃ] |
| 1 | p | /p/ | 1 | |
| 2 | t | /t/ | 2 | |
| 3 | k | /k/ | 3 | |
| 4 | m | /m/ | 4 | |
| 5 | n | /n/ | 5 | |
| 6 | s | /s/ | 6 | |
| 7 | l | /l/ | 7 | acceptable realizations [l]~[ɾ] |
| 8 | w | /w/ | 8 | |
| 9 | j | /j/ | 9 | the y-sound (German/Esperanto j) |

Particle onset:

| idx | roman | IPA | notes |
|-----|-------|-----|-------|
| 10 | h | /h/ | reserved for particles; acceptable realizations [h]~[x]~∅ |

Selection rationale: every content onset is present, or has a
non-colliding approximation, in essentially every major L1 phonology. No
voicing pairs (p/b-type contrasts are a known L1 blind spot); no r (l/r
merger); the one deliberate stretch is /tʃ/, needed as the tenth digit
onset, whose drift realizations ([ts], [ʃ]) collide only weakly with /s/
and are additionally protected by spacing (§4.3).

**The h-reservation is deletion-robust.** /h/ is absent from many L1s
(Spanish, French, Italian, Russian, Portuguese speakers variously drop it
or realize it as [x]). Because content syllables never have a zero onset,
a syllable heard with [h], [x], or no onset at all is *still* unambiguously
a particle. The particle onset is "the maximally weak onset," tolerant of
its own deletion.

### 2.2 Vowels

`a e i o u` (indices 0–4), the cross-linguistically safe five-vowel
system. No reduced vowels, no quality contrasts beyond these five.

### 2.3 Codas

| idx | roman | IPA | word-final role (§6) |
|-----|-------|-----|----------------------|
| 0 | ∅ | — | noun |
| 1 | n | /n/ | verb |
| 2 | s | /s/ | modifier |
| 3 | l | /l/ | reserved (no class assigned in v0.1) |

The fifth coda considered in design (ŋ) is rejected: final n/ŋ merge for
too many L1s. Codas s and l are themselves a stretch for Mandarin/Japanese
L1 speakers; the epenthesis hazard this creates is handled by a lexicon
constraint, not by the phonology (§4.3, echo-vowel rule).

### 2.4 Registers

Two values: **short** vs **long** vowel. Romanized by vowel doubling
(`sa` vs `saa`). Register is the parity channel (§4): it never
distinguishes two words.

## 3. Syllable template and phonotactics

**C V (C)** — onset mandatory, no clusters, no diphthongs, no vowel-initial
syllables. The mandatory onset is load-bearing: self-segregating
morphology (§5) and the h-robustness argument (§2.1) both depend on it.

Legal syllable count: 11 × 5 × 4 × 2 = **440** raw
(400 content-onset, 40 particle-onset).

## 4. Error correction

### 4.1 Inner parity

> **register_index = (onset_index + vowel_index + coda_index) mod 2**

Every lexical syllable satisfies this rule. Consequences:

- The register of every word is computed, not chosen: **register carries
  zero lexical information.** A listener who cannot perceive vowel length
  (many L1s) loses error-detection capability but never content. The
  design never asks any human to *hear* a distinction their L1 didn't give
  them in order to *identify* any word.
- Any single-channel mishearing (onset, vowel, or coda substitution)
  flips parity and lands on a non-word — guaranteed minimum distance 2 —
  at the classical cost of exactly half the raw space.
- Because register is duration, **stress must never be realized as
  duration** (§5.1); pitch/intensity only.

Lexical space after parity: **200 content + 20 particle** syllables.

### 4.2 The anti-parity complement

The 220 syllables violating the parity rule are **reserved for mode
payloads** (numbers, dates, times, spell-out — Tier 2, bead conlang-bcq).
Payload syllables are thereby self-flagging: heard in isolation, any
payload syllable is audibly a non-word. Payload register is also computed
(anti-parity), so modes likewise never require length perception.
Known cost, priced in the modes bead: a single-channel error on a payload
syllable can land back on the lexical side, so payload integrity leans on
the mode boundary plus optional checksum, not on raw spacing.

### 4.3 Weighted spacing (v0.1 policy)

Uniform Hamming distance treats all errors as equally likely; ears do not.
v0.1 states the policy qualitatively; the tooling bead (conlang-wfs)
operationalizes it with an explicit confusion matrix:

1. **Register-only contrasts: impossible by construction** (parity).
2. **Echo-vowel rule.** Coda s/l invite epenthesis from some L1s
   (/nas/ → [nasɯ̥]-like). The lexicon must never contain both /…Cs/ and
   /…Csu/-type pairs (a coda consonant vs the same consonant plus an echo
   vowel); weighted distance treats these as near-identical.
3. **Extra spacing between s/c onset minimal pairs** (drift realizations
   of c approach s for some L1s).
4. **Extra spacing between coda n/l minimal pairs.**

Further layers (cross-syllable outer checks in disyllables, prosodic
checksum, register profiles) are Tier 3 and intentionally out of the
frozen core.

## 5. Prosody and self-segregating morphology

### 5.1 Word shapes

| class | shape | onset | stress |
|-------|-------|-------|--------|
| particle | exactly 1 syllable | h | unstressed |
| content word | 1–3 syllables | content onset | first syllable stressed |

Stress is realized as **pitch/intensity, never duration** (duration is the
register channel). Non-initial syllables of content words are unstressed
and have content onsets.

### 5.2 Unique-parse property

Any syllable stream segments into words in exactly one way: every stressed
syllable opens a content word; every h-onset (or onset-less, per §2.1)
syllable is a one-syllable particle; a content word extends from its
stressed syllable to the next stressed or particle syllable (bounded at 3).
A mishearing that breaks a word template is detected by shape before the
lexicon is consulted — segmentation doubles as an error-correction layer.

Particles are structural function words only (mode markers, clause
openers, terminators, case/topic markers, conjunctions). Pro-forms,
correlatives, and other contentful "small words" are content words, not
particles. Budget: 20 lexical particle slots. If the grammar bead
(conlang-jbw) overflows this, the documented escape hatches — particle-only
diphthongs, or a particle-only coda addition — are spoken-layer-local and
do not disturb the content lexicon.

### 5.3 Loanwords

Foreign material enters through the spell/phonetic modes (conlang-bcq),
not by coercion into native word templates. SSM constraints therefore
never mangle names (contra Lojban).

## 6. The part-of-speech channel

**The final-syllable coda of a content word encodes its part of speech:**
∅ = noun, n = verb, s = modifier, l = reserved.

Why coda, not the Esperanto final-vowel: the coda **partitions** the
monosyllable space instead of shrinking it — 10 onsets × 5 vowels = 50
monosyllabic forms *per class* (150 usable under v0.1's three active
classes, 200 when class l is assigned) versus 40 total under a final-vowel
scheme. Cross-class minimal pairs land in different syntactic slots, so
class mishearings are syntax-detectable ("a noun ending where syntax
demands a verb" is a caught error, not a substitution). And derivation
becomes a channel operation: `sala` (noun) → `salan` (verb) → `salas`
(modifier) are one root's forms — Esperanto's -o/-i/-a on a cleaner axis.
Non-final codas remain fully lexical.

Semantics of the class system (what "the verb of a root" means, argument
structure, whether class l becomes a fourth class) belong to the grammar
bead (conlang-jbw), not the frozen core. The core freezes only: *final
coda = class channel, with ∅/n/s assigned as above.*

## 7. Romanization

- Onsets: `c p t k m n s l w j` + `h`; `c` = "ch as in church" (loosely),
  `j` = the y-sound. These two are the known naive-reader hazards; the
  public-facing rule of thumb is "c → ch, j → y."
- Vowels: `a e i o u`; long register doubles the vowel (`saa`).
- Codas: `-n -s -l`.
- Stress: unwritten (predictable: word-initial).
- Word boundaries: ordinary spaces.

The romanization is a projection for the installed base, not the script.
The native script (bead conlang-657) renders channel vectors directly.

## 8. Codespace budget

Verified by `tools/spec_check.py` against `channels.json`:

| quantity | value |
|----------|-------|
| raw syllables | 440 (400 content, 40 particle) |
| lexical after parity | 200 content + 20 particle |
| payload complement | 200 content-shaped + 20 particle-shaped |
| content monosyllables per POS class | 50 |
| usable content monosyllables (3 active classes) | 150 |
| disyllable lexical points (before spacing) | 40,000 |
| digit pairs needed / available in one payload syllable | 100 / 200 ✓ |
| hour × quarter-hour values / available | 96 / 200 ✓ |
| month × day values / available | 372 / 200 ⇒ two payload syllables |

Weighted spacing (§4.3) will price some of the 150 monosyllables and a
fraction of disyllable space; the root target (1,500–3,000) sits orders of
magnitude below capacity. **Zipf policy:** monosyllable slots are assigned
strictly by corpus frequency from the first dictionary draft; everything
rarer is disyllabic by rule.

## 9. Digit assignment (normative preview)

Numbers are a Tier-2 mode (conlang-bcq), but the digit code is frozen with
the core because the onset indices are load-bearing:

- **Tens digit → onset:** 0=c 1=p 2=t 3=k 4=m 5=n 6=s 7=l 8=w 9=j
- **Units digit → rime:** 0=a 1=e 2=i 3=o 4=u 5=an 6=en 7=in 8=on 9=un
- A digit pair (00–99) is one syllable; multi-pair numbers are positional
  base-100. Payload syllables live on the anti-parity side (§4.2), with
  register computed accordingly.

Example (romanized, register marking omitted): 42 = `mi`, 4207 = `mi cin`
(pairs 42, 07).

## 10. Out of scope for the frozen core

Deferred to their beads, with the core deliberately silent: mode-particle
assignments and payload grammar (bcq); the glyph geometry (657);
derivational semantics and particle inventory (jbw); lexicon content
(kps); input methods (6sa); everything Tier 3+ (qmg, d47).

## Version history

- **0.1.0-draft** (2026-08-08): initial draft for freeze review.
