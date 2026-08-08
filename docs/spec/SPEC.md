# Language Specification — Tier-1 Core

**Version:** 0.2.0-draft · **Status: NOT FROZEN** (freeze is a human
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

The primitive spoken unit is the **syllable**, a vector of three
independent segmental channels, plus one derived written coordinate:

| channel  | values | role |
|----------|--------|------|
| onset    | 11 (10 content + 1 particle) | lexical + word-class boundary |
| vowel    | 5      | lexical |
| coda     | 4      | lexical (non-final) / part-of-speech (word-final) |
| check    | 2      | **derived, written-layer** (§2.4, §4): computed from the segmental channels and the syllable's frame role; optionally realized in careful speech; absent in casual speech |

Everything in the language — words, glyphs, chords, digit codes — is
defined over these coordinates. The written glyph and the typed chord
render the full four-coordinate vector; casual speech is a projection
onto the three segmental channels. The round trip is still deterministic
with one qualification: hearing a lexical word recovers its check by
computation, while payload syllables recover theirs from mode-frame
context (§4.2).

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

### 2.4 The check zone (registers, demoted to the written layer)

**Tentative decision (Edward, 2026-08-09, conlang-bf2):** the check
channel is a **written-layer channel**. Every syllable's check bit is
computed (§4.1) and always present in the written layer — a glyph zone
in the native script and optional vowel doubling in romanization — but
**casual speech does not carry it**. Spoken realization (long vowel,
≥1.5× the short duration) belongs to careful and safety-critical
registers only, where a speaker may realize the check audibly the way
one spells out a word for confirmation.

Rationale (docs/design/alternatives/no-parity-core.md, v2 experiment +
two adversarial reviews): with humility assignment (§4.3) the spoken
inner code was pure insurance for length-sensitive listeners only,
while its costs — producing a length contrast most L1s lack, the
stress-vs-duration conflict, the erosion exposure of a zero-load
contrast — fell on everyone. Demotion keeps the machine-facing and
careful-register value at zero casual-speech cost, and frees duration
to strengthen the stress signal (§5.1). Re-promotion to a mandatory
spoken channel is a documented minor-version path (§9).

## 3. Syllable template and phonotactics

**C V (C)** — onset mandatory, no clusters, no diphthongs, no vowel-initial
syllables. The mandatory onset is load-bearing: self-segregating
morphology (§5) and the h-robustness argument (§2.1) both depend on it.

Legal spoken syllable count: 11 × 5 × 4 = **220** segmental triples
(200 content-onset, 20 particle-onset). The written layer carries one
computed check bit per syllable on top (§2.4), giving 440 written-layer
codepoints.

## 4. Error correction

### 4.1 The check bit (written-layer, confusion-weighted)

Every channel value carries a normative **check bit** (`channels.json`),
and every syllable's check value is computed from them:

> **check = (check(onset) + check(vowel) + check(coda)) mod 2**

Where it lives (§2.4): always in the written layer and available to
machines; audibly realized (as vowel length) only in careful/safety
speech registers. What it buys, stated honestly:

- **The check carries zero lexical information** — it is computed, so
  no reader, listener, or speaker ever needs it to identify a word, and
  casual speech omits it entirely.
- In the written layer and careful registers, **every substitution
  between two values with different check bits flips the check** and is
  detectable before lexical lookup. The bits are assigned to cover the
  perceptually likely confusions: s/c, p/t, t/k, m/n, n/l, l/j, l/w
  among onsets; e/i and o/u among vowels; ∅/n, ∅/s, n/l, s/l among
  codas (`covered_confusion_pairs`, asserted by `spec_check.py`).
- Substitutions between same-bit values are invisible to the check (660
  such distance-1 pairs across the 200 content triples). In v0.2 this
  matters less than in v0.1, because casual-speech protection no longer
  routes through the check at all — it routes through the humility
  assignment policy (§4.3), which bans high-confusion minimal pairs
  outright.

**Casual speech protection, v0.2:** lexical sparsity under humility
assignment + word templates (§5) + phonotactic rules + context +
conversational repair. The deconfounded simulation
(`tools/explore_noparity.py`) puts residual silent substitution at
~3.9% of mishearing events (conditional; 2.5% exposure-weighted) for
all listeners — versus 22% for length-deaf listeners under the v0.1
policy that licensed covered minimal pairs because the spoken register
"caught" them.

What the check is **not**: a uniform minimum-distance-2 code (a binary
check cannot separate all values of a ten-valued channel; the honest
uniform-distance-2 alternative caps the space at **20** codewords,
`uniform_distance2_bound`).

Stress may be realized with **pitch, intensity, and duration** in casual
speech (§5.1) — duration is free there. In careful registers that
realize the check as length, stress falls back to pitch/intensity.

Lexical space: **200 content + 20 particle** segmental syllables (the
check is determined for every triple).

### 4.2 The anti-check complement (written layer)

In the written layer, payload syllables (mode contents — numbers, dates,
times, spell-out; Tier 2, conlang-bcq) carry the **anti-check** value:
written text and machines can distinguish payload from lexical material
per syllable. In speech this marking exists only in careful registers;
casual spoken payload integrity rests where it honestly always did — on
the mode-boundary particles, the frame grammar, and the checksum
profile (mandatory in safety registers). A single-channel error on a
payload syllable can land on the lexical side either way, so payload
integrity leans on boundaries plus checksum, not on spacing.

### 4.3 Lexicon spacing rules (v0.2)

Uniform Hamming distance treats all errors as equally likely; ears do
not. The rules below are normative (`channels.json spacing_rules`); the
generator (tools/lexgen.py) enforces them:

1. **Check-only contrasts: impossible by construction** (the check is
   computed — no two words differ only in the written check zone).
2. **Humility rule (adopted 2026-08-09, conlang-bf2).** No two
   *unrelated* lexical words may differ by a single **high-confusion**
   substitution — the union of `covered_confusion_pairs` (s/c, p/t,
   t/k, m/n, n/l, l/j, l/w; e/i, o/u; ∅/n, ∅/s, n/l, s/l) and the
   **forbidden** residual pairs (p/k; a/e, a/o; coda ∅/l). The v0.1
   policy licensed covered minimal pairs because the spoken register
   flagged them; the deconfounded experiment showed that policy
   produced a 22% silent-substitution rate for length-deaf listeners
   and it is withdrawn. **Weighted** pairs (p/m, k/m, t/n, w/j; e/o,
   i/u; coda n/s) may form minimal pairs at a scored cost, avoided
   among high-frequency assignments. Capacity: 22 monosyllabic root
   bodies (18 under strict weighted-inclusive spacing;
   `tools/lexgen.py report`). Same-root POS alternations are exempt:
   every root's verb/modifier pair differs by coda n/s by design (§6)
   — that is morphology, not a lexical minimal pair, and a misheard
   class is caught by syntax or recovered semantically.
3. **Echo-vowel rule, all positions.** Coda s/l invite epenthesis from
   some L1s (/nas/ → [nasɯ̥]-like). The lexicon must never contain
   confusable /…Cs/-vs-/…Csu/-type pairs, finally or medially. The
   epenthetic vowel set is normative data
   (`lexical_cell_rules.echo_vowels`: u, i, o — the attested epenthesis
   qualities of the coda-averse L1s).
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

Stress is realized with **pitch, intensity, and duration** — duration
became available to stress when the check moved to the written layer
(§2.4), strengthening the boundary signal. In careful registers that
audibly realize the check as vowel length, stress narrows to
pitch/intensity. Non-initial syllables of content words are unstressed
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
word-boundary signal; in casual speech it may use duration alongside
pitch and intensity (§5.1), but degraded-stress speech
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
wordforms per class (150 across the three active classes) versus
10 onsets × 4 codas = 40 per class (120 across three) under a final-vowel
scheme: a 25% capacity edge, plus two structural wins. Cross-class
minimal pairs land in different syntactic slots, so class mishearings are
syntax-detectable ("a noun ending where syntax demands a verb" is a
caught error, not a substitution). And derivation becomes a channel
operation — swap the final coda, then recompute the written check
(§4.1), since coda check bits differ across classes: `sala` (noun) →
`salaan` (verb) → `salaas` (modifier) are one root's forms (the doubling
is written-layer marking), Esperanto's -o/-i/-a on a cleaner axis. Non-final codas remain fully
lexical.

Because the three class forms of a root share their onset–vowel body,
monosyllabic **root bodies** number 50, not 150 — the 150 are wordforms.
Whether cross-class sharing is obligatory (every monosyllabic body is one
root family, never three unrelated roots) is a grammar decision for
conlang-jbw; the default design intent is obligatory sharing, which is
kinder to learners and to error correction, and the budget below counts
root bodies on that assumption.

Honest costs of parking POS on the coda, v0.2 accounting: in casual
speech there is no check, so ALL class flips (∅/n, ∅/s, n/s) ride on
syntactic expectation, semantics, word shape, and repair — the
deconfounded simulation puts this same-root "syntax class" at ~18% of
mishearing events. Written text and careful registers add the check
flag on top for the ∅/n and ∅/s flips (bits differ); the n/s flip is
check-invisible everywhere. Coda lenition is a *systematic* L1 process,
not noise: Caribbean-Spanish-type s-deletion reads a modifier as a
noun, and noun/modifier confusion inside a noun phrase is often
syntax-blind. conlang-jbw must weigh whether high-frequency modifiers
should prefer disyllabic forms whose first syllable carries
disambiguating material. When class l activates (§9), l-vocalization
joins this list (coda l→∅ is check-invisible even in writing).

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
| spoken segmental syllables | 220 (200 content, 20 particle) |
| written-layer codepoints (incl. derived check) | 440 (400 content, 40 particle) |
| lexical codepoints (check computed) | 200 content + 20 particle |
| payload complement (written-layer marking) | 200 content-shaped + 20 particle-shaped |
| monosyllabic wordforms per POS class | 50 (150 across active classes) |
| high-confusion-free monosyllabic root bodies (humility) | 22 |
| monosyllabic **root bodies** | 50, before spacing and reserve |
| disyllabic wordforms (active classes, before constraints) | 30,000 |
| disyllabic **root bodies** (before constraints) | 10,000 |
| uniform-distance-2 bound (why weighted spacing exists) | 20 |
| check-invisible distance-1 pairs (generator must space) | 660 |
| digit pairs needed / available in one payload syllable | 100 / 200 ✓ |
| hour × quarter-hour values / available | 96 / 200 ✓ |
| month × day values / available | 372 / 200 ⇒ two payload syllables |

Weighted spacing (§4.3) prices these down — root bodies are the scarce
resource. Generator outputs (`tools/lexgen.py report`, current spec
data): **22 monosyllabic root bodies** under the adopted humility
policy (18 under strict weighted-inclusive spacing; 48 raw after the
glide-cell ban), of which **15 are assignable** after the 30% reserve;
**8,496 disyllabic root bodies** upper bound before assignment-time
checks (echo-vowel, tosmabru, pairwise spacing). The root target
(1,500–3,000) still sits far below disyllabic capacity. The syllable
inventory in active use (200 content codepoints) is in
Japanese/Hawaiian territory; the working monosyllabic vocabulary (~15
words initially) covers only the very top of the Zipf curve — the
language is disyllable-dominant by consequence, not accident. **Zipf policy:** monosyllable slots are assigned strictly
by corpus frequency from the first dictionary draft; everything rarer is
disyllabic by rule.

**Reserved headroom for coinage and drift** (Edward directive,
2026-08-08): the short-form space is never exhausted. At every release, at
least **30% of the generator-approved monosyllabic root bodies** (7 of
the current 22) remain unassigned, held for future coinage,
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
  touching the spoken core. The check zone itself is now such a channel
  (§2.4); **re-promoting it to a mandatory spoken register** is a
  minor-version path (the demotion is tentative), as is the converse —
  deleting it outright if the written layer's checkability proves
  unearned.

## 10. Digit assignment (normative preview)

Numbers are a Tier-2 mode (conlang-bcq), but the digit code is frozen with
the core because the onset indices are load-bearing:

- **Tens digit → onset:** 0=c 1=p 2=t 3=k 4=m 5=n 6=s 7=l 8=w 9=j
- **Units digit → rime:** 0=a 1=e 2=i 3=o 4=u 5=an 6=en 7=in 8=on 9=un
- A digit pair (00–99) is one syllable; multi-pair numbers are positional
  base-100. In the written layer, payload syllables carry the
  anti-check value (§4.2); casual speech carries no check either way.

Example: 42 = `mi`, 4207 = `mi cin` (pairs 42, 07) — both written-layer
payload check values compute short here (check sums are odd, so the
anti-check value is 0); doubling, where it appears in payload
romanizations, is written-layer marking, silent in casual speech.

**Known weak digit cells** (the grid freezes with the core, so these are
priced, not hidden — conlang-bcq must test the full set under the
confusion model and design the checksum profile around them):
c/s tens confusion (digits 0X vs 6X; check bits differ, but the flip
lives in the written layer — casual spoken digits rely on checksum and
context); the coronal-i column (02 `ci`,
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

- **0.2.0-draft** (2026-08-09): humility assignment adopted (covered
  minimal pairs banned for unrelated words; 22 root bodies, 15
  assignable); check channel tentatively demoted to the written layer
  (casual speech carries no register; stress gains duration; careful/
  safety registers may realize the check as length). Decisions:
  conlang-bf2, evidence in docs/design/alternatives/no-parity-core.md.
- **0.1.0-draft** (2026-08-08): initial draft for freeze review.
