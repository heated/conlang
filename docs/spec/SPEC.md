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
| 0 | c | /tʃ/ | 0 | licensed [tʃ]~[ts]; [ʃ] is unlicensed L1 drift (§4.3 coronal-i rule) |
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

**The h-reservation is substitution-robust, with a normative floor.**
/h/ is absent from many L1s (Spanish, French, Italian, Russian, Portuguese
speakers variously drop it or realize it as [x]). Any audible weak-onset
realization — canonically **[h] ~ [x] ~ [ʔ]** — is acceptable and remains
unambiguously a particle, because no content onset occupies that space.
The floor is the glottal stop: a speaker who cannot produce [h] uses [ʔ],
which every human can produce (it is the universal hiatus-filler). What is
**not** licensed is deleting the onset entirely and resyllabifying across
the boundary (e.g. /tas ha/ surfacing as [ta.sa]) — that destroys the
segmentation guarantee (§5.2). The lexicon additionally carries an
anti-resyllabification constraint (§4.3) so that even this non-canonical
reduction tends to produce a non-parse rather than a wrong parse.

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

Two values: **short** vs **long** vowel; the long target is ≥1.5× the
short duration in careful speech. Romanized by vowel doubling (`sa` vs
`saa`) — optional in romanization, since register is always derivable
from the check bits. Register is the check channel (§4): it never
distinguishes two words. Honest billing: length is the least perceptible
channel for many L1s, it interacts with phrase-final lengthening and with
stress in production, and a contrast carrying no lexical load invites
erosion. The inner code is therefore a careful-register and
machine-facing guarantee that degrades gracefully — a length-deaf
listener or a fast talker falls back to generator spacing, templates, and
repair, never losing content. Realization of long vowels in unstressed
syllables and in CVVC (long + coda) shapes is typologically marked;
production guidance and its perceptual reality are evaluation targets,
not assumptions.

## 3. Syllable template and phonotactics

**C V (C)** — onset mandatory, no clusters, no diphthongs, no vowel-initial
syllables. The mandatory onset is load-bearing: self-segregating
morphology (§5) and the h-robustness argument (§2.1) both depend on it.

Legal syllable count: 11 × 5 × 4 × 2 = **440** raw
(400 content-onset, 40 particle-onset).

## 4. Error correction

### 4.1 The check channel (confusion-weighted register)

Every channel value carries a normative **check bit** (`channels.json`),
and the register of every lexical syllable is computed from them:

> **register = (check(onset) + check(vowel) + check(coda)) mod 2**

What this buys, stated honestly:

- **Register carries zero lexical information.** A listener who cannot
  perceive vowel length (many L1s) loses error-detection capability but
  never content. The design never asks any human to *hear* a distinction
  their L1 didn't give them in order to *identify* any word.
- **Every substitution between two values with different check bits flips
  the register** and lands on a non-word. The check bits are assigned to
  cover the perceptually likely confusions: s/c, p/t, t/k, m/n, n/l, l/j,
  l/w among onsets; e/i and o/u among vowels; ∅/n, ∅/s, n/l, s/l among
  codas (`covered_confusion_pairs`, asserted by `spec_check.py`).
- **Substitutions between same-bit values are invisible to the register**
  (660 such distance-1 pairs across the 200 content triples —
  `spec_check.py` enumerates them). These are deliberately the *unlikely*
  confusions (p/k, a/o, coda n/s, …, `residual_confusion_pairs`), and the
  lexicon generator (conlang-wfs) must not assign both members of any
  such minimal pair as words.

What this is **not**: a uniform minimum-distance-2 code. An earlier draft
claimed that; the claim was wrong (a binary check cannot separate all
values of a ten-valued channel), and the honest uniform-distance-2
alternative — a mod-10 check over the largest channel — would cap the
space at **20** codewords (`uniform_distance2_bound`). The design instead
concentrates the one cheap check bit on the high-probability errors and
delegates the rest to generator-enforced spacing: structured redundancy
where the ears are weak, capacity where they are strong.

Because register is duration, **stress must never be realized as
duration** (§5.1); pitch/intensity only.

Lexical space under the register rule: **200 content + 20 particle**
syllables (register determined for every (onset, vowel, coda) triple).

### 4.2 The anti-check complement

The 220 syllables violating the register rule are **reserved for mode
payloads** (numbers, dates, times, spell-out — Tier 2, bead conlang-bcq).
Payload register is likewise computed (anti-check), so modes never require
length perception to *decode a payload's value*. Two honest
qualifications. First, a payload syllable differs from its lexical
counterpart **only in length**, so payloads are self-flagging only to
register-sensitive listeners and machines; a length-deaf listener relies
entirely on the mode boundary. The mode-boundary particle must therefore
be robust on its own, and safety registers add a checksum syllable
(priced in conlang-bcq). Second, a single-channel error on a payload
syllable can land back on the lexical side, so payload integrity leans on
the mode boundary plus checksum, not on spacing.

### 4.3 Weighted spacing (v0.1 policy)

Uniform Hamming distance treats all errors as equally likely; ears do not.
v0.1 states the policy qualitatively; the tooling bead (conlang-wfs)
operationalizes it with an explicit confusion matrix:

1. **Register-only contrasts: impossible by construction** (register is
   computed).
2. **Residual-pair rule.** No two *unrelated* lexical words may differ by
   a single substitution within `residual_confusion_pairs` (the
   check-invisible substitutions). Same-root POS alternations are exempt:
   every root's verb/modifier pair differs by coda n/s by design (§6) —
   that is morphology, not a lexical minimal pair, and a misheard class is
   caught by syntax or recovered semantically.
3. **Echo-vowel rule, all positions.** Coda s/l invite epenthesis from
   some L1s (/nas/ → [nasɯ̥]-like). The lexicon must never contain
   confusable /…Cs/-vs-/…Csu/-type pairs, finally or medially.
4. **Fake-geminate rule.** A coda consonant followed by an identical
   onset may not contrast with the single-consonant parse
   (/nas.sa/ vs /na.sa/).
5. **Glide-cell rule.** Syllables `ji` and `wu` are not lexical: the
   glide fuses with its homorganic vowel and the result sounds
   onset-less — which the parser would read as a particle (§2.1). The
   near-homorganic cells (`je`, `wo`) carry extra weighting.
6. **Coronal-i rule.** No t/c or s/c lexical minimal pairs before /i/:
   ti→[tʃi] and si→[ɕi] palatalization (Japanese, Korean, Brazilian
   Portuguese, Quebec French) lands inside c's realization space.
7. **Anti-resyllabification rule** (Lojban's tosmabru class). For any
   lexical word ending in a consonant coda followed by any particle, the
   resyllabified surface string must not parse as a legal word sequence —
   enforced by the generator over the actual lexicon plus particle
   inventory. This is the lexical backstop for the §2.1 boundary floor.

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

### 5.2 Unique-parse property (scope and conditions)

**At the phonemic level, given boundary-preserving realizations,** any
syllable stream segments into words in exactly one way: every stressed
syllable opens a content word; every weak-onset ([h]~[x]~[ʔ]) syllable is
a one-syllable particle; a content word extends from its stressed syllable
to the next stressed or particle syllable (bounded at 3). A mishearing
that breaks a word template is detected by shape before the lexicon is
consulted — segmentation doubles as an error-correction layer.

The conditions are load-bearing and the spec names them rather than
hiding them. (1) The particle onset must surface as *some* audible onset
(§2.1 floor: [ʔ]); full deletion with cross-boundary resyllabification
(/tas ha/ → [ta.sa]) is a non-canonical reduction that the phonology does
not license and the lexicon's anti-resyllabification rule (§4.3) defuses:
the reduced string should fail to parse rather than parse wrongly, and
conversational repair does the rest. (2) Stress detection: stress is the
word-boundary signal; it is realized as pitch/intensity precisely so it
cannot be confused with the register channel, but degraded-stress speech
shifts segmentation onto the particle cues and word templates — and
sequences of monosyllabic words (which Zipf assignment makes frequent)
produce stress clash, which natural speech resolves by destressing,
eroding exactly this cue. The robustness of the parse under both
degradations is a simulation target in the evaluation plan, not an
assumed property.

Particles are structural function words only (mode markers, clause
openers, terminators, case/topic markers, conjunctions). Pro-forms,
correlatives, and other contentful "small words" are content words, not
particles. **The particle namespace width is provisional in v0.1** — 20
lexical slots exist under the current template, but whether 20 suffices is
established by conlang-jbw's enumeration *before* freeze, not assumed.
If it overflows, widening the particle encoding (particle-only diphthongs
or codas) is a real phonotactic change with script- and input-layer costs;
§9 records it as a priced expansion path, and the freeze decision must see
the enumerated inventory first.

### 5.3 Loanwords

Foreign material enters through the spell/phonetic modes (conlang-bcq),
not by coercion into native word templates. SSM constraints therefore
never mangle names (contra Lojban).

## 6. The part-of-speech channel

**The final-syllable coda of a content word encodes its part of speech:**
∅ = noun, n = verb, s = modifier, l = reserved.

Why coda, not the Esperanto final-vowel: both schemes partition the
monosyllable space, but the coda partitions it into **more and larger
classes for this inventory** — 10 onsets × 5 vowels = 50 monosyllabic
wordforms per class (150 across v0.1's three active classes) versus
10 onsets × 4 codas = 40 per class (120 across three) under a final-vowel
scheme: a 25% capacity edge, plus two structural wins. Cross-class
minimal pairs land in different syntactic slots, so class mishearings are
syntax-detectable ("a noun ending where syntax demands a verb" is a
caught error, not a substitution). And derivation becomes a channel
operation — swap the final coda, then recompute the register (§4.1),
since coda check bits differ across classes: `sala` (noun, register
short) → `salaan` (verb) → `salaas` (modifier) are one root's forms,
Esperanto's -o/-i/-a on a cleaner axis. Non-final codas remain fully
lexical.

Because the three class forms of a root share their onset–vowel body,
monosyllabic **root bodies** number 50, not 150 — the 150 are wordforms.
Whether cross-class sharing is obligatory (every monosyllabic body is one
root family, never three unrelated roots) is a grammar decision for
conlang-jbw; the default design intent is obligatory sharing, which is
kinder to learners and to error correction, and the budget below counts
root bodies on that assumption.

Honest costs of parking POS on the coda: noun↔verb and noun↔modifier
flips are register-flagged (coda check bits differ), but the verb↔
modifier flip (n/s, same bit) is check-invisible by construction — it is
exactly the exempted morphological alternation of §4.3, caught by syntax
or absorbed as a near-miss. Worse, coda lenition is a *systematic* L1
process, not noise: Caribbean-Spanish-type s-deletion reads a modifier as
a noun, and noun/modifier confusion inside a noun phrase is often
syntax-blind. The mitigations are the register flag (∅/s bits differ),
semantics, and repair; conlang-jbw must weigh whether high-frequency
modifiers should prefer disyllabic forms whose first syllable carries
disambiguating material. When class l activates (§9), l-vocalization
joins this list (coda l→∅ is check-invisible).

Semantics of the class system (what "the verb of a root" means, argument
structure, whether class l becomes a fourth class) belong to the grammar
bead (conlang-jbw), not the frozen core. The core freezes only: *final
coda = class channel, with ∅/n/s assigned as above.*

## 7. Romanization

- Onsets: `c p t k m n s l w j` + `h`; `c` = "ch as in church" (loosely),
  `j` = the y-sound. These two are the known naive-reader hazards; the
  public-facing rule of thumb is "c → ch, j → y."
- Vowels: `a e i o u`; long register doubles the vowel (`saa`). Doubling
  is derivable from the check bits, so plain spelling without doubling is
  also valid romanization; pedagogical text doubles, casual text may not.
- Codas: `-n -s -l`.
- Stress: unwritten (predictable: word-initial).
- Word boundaries: ordinary spaces.

The romanization is a projection for the installed base, not the script.
The native script (bead conlang-657) renders channel vectors directly.

## 8. Codespace budget

Verified by `tools/spec_check.py` against `channels.json`. The table
separates **codepoints** (syllable-sized slots), **wordforms** (inflected
surface words), and **root bodies** (independently assignable meanings,
given obligatory cross-class derivation, §6):

| quantity | value |
|----------|-------|
| raw syllables | 440 (400 content, 40 particle) |
| lexical codepoints (register computed) | 200 content + 20 particle |
| payload complement | 200 content-shaped + 20 particle-shaped |
| monosyllabic wordforms per POS class | 50 (150 across active classes) |
| monosyllabic **root bodies** | 50, before spacing and reserve |
| disyllabic wordforms (active classes, before constraints) | 30,000 |
| disyllabic **root bodies** (before constraints) | 10,000 |
| uniform-distance-2 bound (why weighted spacing exists) | 20 |
| check-invisible distance-1 pairs (generator must space) | 660 |
| digit pairs needed / available in one payload syllable | 100 / 200 ✓ |
| hour × quarter-hour values / available | 96 / 200 ✓ |
| month × day values / available | 372 / 200 ⇒ two payload syllables |

Weighted spacing (§4.3) will price these down — root bodies are the
scarce resource, and the honest usable counts (after the residual-pair,
echo-vowel, and anti-resyllabification rules) are an *output of the
generator* (conlang-wfs), not a promise of this spec. The root target
(1,500–3,000) still sits far below disyllabic capacity. The syllable
inventory in active use (200 content codepoints) is in Japanese/Hawaiian
territory; whether the working monosyllabic vocabulary lands above the
comfort knee is likewise settled by the generator plus lexicon, not
assumed here. **Zipf policy:** monosyllable slots are assigned strictly
by corpus frequency from the first dictionary draft; everything rarer is
disyllabic by rule.

**Reserved headroom for coinage and drift** (Edward directive,
2026-08-08): the short-form space is never exhausted. At every release, at
least **30% of the generator-approved monosyllabic root bodies** (≥15 if
all 50 survive spacing) remain unassigned, held for future coinage,
borrowed-root nativization, and frequency drift (when a rising word earns
a short form, one is available without evicting anything). Disyllable
assignments likewise keep spacing slack rather than packing optimally.
Drift is absorbed through versioned lexicon releases (governance: bead
conlang-70m) — the reserve is what makes absorbing it cheap. The 30%
figure is adjustable until freeze.

## 9. Extensibility: widening the inventory is a supported evolution

Design directive (Edward, 2026-08-08): keep room to move toward the wider
codepoint model later, or to "push a little." The core is therefore frozen
as a *versioned point in an expansion-compatible family*, not a dead end:

- **Stable under expansion:** the parity rule's form (index-sum mod
  register-count), every existing word's channel vector, the digit and POS
  assignments, and the romanization of existing values. Adding a channel
  value appends an index; it never renumbers existing ones.
- **Cheap expansions** (minor version): a fifth coda (class-l roots or a
  new POS class), additional content onsets, diphthongs as new vowel-channel
  values. Each must price its L1-perception cost against the design-brief
  accessibility constraint when proposed — expansion trades learnability
  deliberately, never accidentally. New values also get check bits, priced
  against the confusion pairs they introduce.
- **Particle-space widening** (minor version, but not free): if the
  structural inventory overflows 20 slots (conlang-jbw settles this before
  freeze), particle-only diphthongs or codas widen the namespace. This is
  a real phonotactic change — the script and input layers must render the
  new shapes — so it rides the same headroom obligations as any widening,
  and the freeze decision must see the enumerated particle inventory
  first.
- **Expensive expansion** (major version): a third register value
  (parity becomes mod-3; the complement doubles relative to the lexical
  side). Supported by the rule's form but touches every downstream table.
- **Headroom obligations on downstream design:** the featural script's
  visual zones and the chord/touch layouts must be compositional with
  capacity for roughly the wide model's counts (~20 onsets, ~10 vowels,
  ~8 codas) rather than saturating at today's inventory. Recorded on beads
  conlang-657 and conlang-6sa.
- A written-only channel (a visual zone with no spoken counterpart, e.g.
  the semantic-classifier zone) remains available at any time without
  touching the spoken core.

## 10. Digit assignment (normative preview)

Numbers are a Tier-2 mode (conlang-bcq), but the digit code is frozen with
the core because the onset indices are load-bearing:

- **Tens digit → onset:** 0=c 1=p 2=t 3=k 4=m 5=n 6=s 7=l 8=w 9=j
- **Units digit → rime:** 0=a 1=e 2=i 3=o 4=u 5=an 6=en 7=in 8=on 9=un
- A digit pair (00–99) is one syllable; multi-pair numbers are positional
  base-100. Payload syllables live on the anti-check side (§4.2), with
  register computed accordingly.

Example: 42 = `mi`, 4207 = `mi cin` (pairs 42, 07) — both payload
registers compute short here (check sums are odd, so the anti-check
register is 0).

**Known weak digit cells** (the grid freezes with the core, so these are
priced, not hidden — conlang-bcq must test the full set under the
confusion model and design the checksum profile around them):
c/s tens confusion (digits 0X vs 6X; check bits differ, but the flip is
inaudible to length-deaf listeners); the coronal-i column (02 `ci`,
22 `ti`, 62 `si` merge under palatalizing L1s — prescribed realizations:
c strictly affricate); the glide-fusion cells (84 `wu`, 92 `ji` — 
prescribed fortified realizations [β̞u], [ʝi], since the lexical
glide-cell ban cannot apply inside the frozen grid); and the units 5–9
final /n/, which is fragile in noise (the aviation "niner" lesson —
careful-register digit readout is a conlang-bcq deliverable).

## 11. Out of scope for the frozen core

Deferred to their beads, with the core deliberately silent: mode-particle
assignments and payload grammar (bcq); the glyph geometry (657);
derivational semantics and particle inventory (jbw); lexicon content
(kps); input methods (6sa); everything Tier 3+ (qmg, d47).

## Version history

- **0.1.0-draft** (2026-08-08): initial draft for freeze review.
