# Romance Zonal v0 — working design (workshop draft)

Status: workshop-stage, bead conlang-0y7. No name yet ("RZ" below).
Deliberately validator-free at this stage: decisions + samples first,
measurement tooling at the first cloze test, freezing much later.
Companion docs: `../alternatives/zonal-auxlang-survey.md` (evidence),
`../alternatives/zonal-script-pricing.md` (Latin-primary decision).

## 0. The bet, restated

A zonal auxlang wins by being **readable at first contact** by the
~900M Romance-language speakers, the way Interslavic measured 84% mean
cloze comprehension with zero study. The product is *receptive
intelligibility* plus a *regularized productive layer* you can learn in
tens of hours, not hundreds. Everything below is ranked by that: when
cognate recognition and engineering elegance conflict, recognition
wins. (This is the mirror image of the greenfield lang, and exactly
why the two are worth pricing against each other — bead conlang-ow7.)

Positioning vs the incumbents (survey §1): Interlingua has the corpus
but an etymology-heavy orthography and 1950s infrastructure; Neolatino
is scholarly and pan-Romance but conservative (keeps gender/agreement
complexity); LFN is regular but respells away visual cognacy. The open
niche: **Neolatino's pan-Romance lexicon + Interlingua's simplified
grammar + measurement-driven iteration + modern tooling** (chorded
input, spellcheck, parallel texts) — no incumbent has ever *measured*
its comprehension claim. The first published cloze number is the
growth asset.

## 1. Source set and weighting

Primary sources: **ES, PT, IT, FR, RO** (+CA consulted on ties).
Weights ≈ reader-base share of the zone: ES .40, PT .25, IT .15,
FR .15, RO .05. Working rule: a form must be *sight-recognizable* to
readers of a weighted majority; the Ibero cluster (ES+PT = .65) plus
IT usually decides. FR contributes mostly through *written* cognates
(its spellings stayed Latin even where its phonology left), which is
fine — this is a written-first language. RO rarely decides anything
but breaks ties toward the pan-Romance form.

## 2. Orthography: cognate-first, shallow second

Fully regular grapheme→phoneme *reading rules*, but spellings chosen
for **sight cognacy**, not phonemic minimalism (the LFN mistake to
avoid: `sentro` reads as a typo to every Romance reader; `centro`
reads instantly to all of them).

- Five vowels a e i o u, always their Latin values. No silent letters
  anywhere (adeu, FR habits).
- `c` = /k/, but /ts/ before e,i (readers will substitute /tʃ/ or /s/
  per their L1 — all tolerated; the reference value is the compromise).
  Same pattern `g` = /g/, /dʒ/ before e,i. This keeps `centro`,
  `nacion`… wait — see next point.
- Latin `-tion` family: spelled **-cion** (ES `-ción` minus accent;
  PT `-ção`, IT `-zione`, FR `-tion` all sight-map to it). Every
  member of the family is spelled the same way: nacion, nacional,
  nacionalitate.
- No accent marks in v0 (stress is rule-based, §3.5); no ñ/ç/gli
  digraph zoo: `ni` = /ɲ/ intervocalically (Espania), `li` similarly.
- `z` = /ts/ where it occurs before a,o,u (forza, comenzar) — the
  same phoneme `c` carries before e,i.
- `qu` = /k/ before e,i (que, qui as in ES/PT/FR); `ch` reserved,
  unused in core spelling.
- Contractions: exactly two, `del` (de+le) and `al` (a+le) — both
  pan-Romance reflexes; nothing else contracts.

Cost admitted: c/g softening is one (1) reading rule with three
tolerated realizations — a deliberate trade of phonemic purity for
recognition. Greenfield keeps purity; this is a row in the ow7 table.

## 3. Morphology: Interlingua-grade simplicity, Ibero-leaning forms

3.1 **Nouns.** Plural `-s` (after vowel) / `-es` (after consonant).
No case. Natural gender only in animate pairs (fil**io**/fil**ia**);
no grammatical gender system, no agreement.

3.2 **Articles.** Definite `le` (sg) / `les` (pl); indefinite `un`.
Invariant otherwise. (`les` costs one form vs pure invariance and
buys instant FR recognition + plural marking redundancy.)

3.3 **Adjectives.** Agree in **number only** (`-s`/`-es`), never in
gender: `le manto calde`, `les mantos caldes`. Default postposed.
Comparative `plus`, superlative `le plus`. (Decision from the sample
self-audit: fully invariant adjectives — Interlingua's choice — are
the loudest "broken Spanish" signal to naive Romance readers, since
all five sources inflect adjective number; number agreement buys
naturalness for one trivial rule. Gender agreement stays dead: its
absence is far less salient and its cost is the whole gender system.)
Adverbs: adjective + `-mente` (caldemente).

3.4 **Verbs.** Infinitives keep their class vowel: `-ar, -er, -ir`
(cognacy). Conjugation is person-invariant; subject pronouns
obligatory:

| form | shape | example |
|---|---|---|
| present | stem + a/e/i | `io parla`, `el vive` |
| past | + `-va` | `el parlava` |
| future | `va` + inf | `nos va parlar` |
| conditional | + `-ria` | `io parlaria` |
| participle | + `-te` (`-ate/-ite`) | `coperte`, `parlate` |
| passive | `es` + participle | `es considerate` |
| gerund | + `-nte` | `brilante` |

Irregular verbs: exactly three, all pan-Romance sight-words —
`es/era/seria` (be), `va` (go, also the future auxiliary), `sta`
(state/health, as in `como tu sta`). Everything else is regular by
the table. No subjunctive in v0 (use indicative; revisit only if
sample texts read wrong to natives).

3.5 **Stress rule** (for the reference pronunciation): penult if the
word ends in vowel or -s/-n, final otherwise — the pan-Romance
default; no diacritics needed at v0's lexicon size.

3.6 **Pronouns.** `io, tu, el, ela, nos, vos, eles, elas`; object
forms `me, te, le, la, nos, vos, les, las`; possessives `mi, tu, su,
nostre, vostre, lor`.

3.7 **Function words** (weighted-recognition picks): `e` (and), `o`
(or), `ma` (but), `no` (not), `si` (yes/if), `que` (that/which),
`de`, `a`, `en`, `con`, `por`, `sobre`, `quando`, `como`, `qui`
(who), `alora` (then), `anque` (also).

## 4. Lexicon recipe (the replicable per-zone method, step 3 of §8)

For each concept: (1) list the five standard forms; (2) strip each
language's idiosyncratic sound changes back toward the shared Romance
etymon; (3) adopt the shape closest to the *written-cognate
intersection* (usually the Latin accusative stem as it survives in
ES/IT); (4) tie-breaks, in order: weighted sight-recognition → keeps
the derivation family regular (nacion/nacional/nacionalitate must all
work) → shorter. Where the zone split lexically (window: ventana /
janela / finestra / fenêtre / fereastră), take the weighted-majority
*root* (fenestr- has IT+FR+RO+etymology: `fenestra`) and note the
losers as recognized-passively. (5) **False-friend screen**: reject
any form that collides with a high-frequency word of a source
language — the self-audit caught `loco` "place" (Latin locus, IT
luogo) reading as ES/PT "crazy"; `sitio` (ES sitio / PT sítio / IT
sito / FR site) wins instead. The screen is a mandatory recipe step,
not a nice-to-have. Modern/technical vocabulary: the international
Latinate form as-is (`television`, `internet`, `programa`).

## 5. Sample texts (the point of this whole document)

**North Wind and the Sun:**

> Le vento del norte e le sol disputava sobre qui era le plus forte,
> quando un viajator passava, coprite de un manto calde. Les dos
> accordava que le prime a facer le viajator remover su manto seria
> considerate le plus forte. Le vento del norte comenzava a soplar
> con tote su forza, ma quanto plus el soplava, tanto plus le
> viajator se copriva con su manto; e al fin, le vento abandonava le
> tentativa. Alora le sol comenzava a brilar caldemente, e
> immediatamente le viajator removeva su manto. E asi le vento del
> norte deveva reconocer que le sol era le plus forte de les dos.

**Conversational register:**

> — Bon dia! Como tu sta?
> — Multo ben, gracias. E tu?
> — Anque ben. Tu vole prender un cafe con me?
> — Si, con placer. Io conoce un bon sitio cerca de aqui.
> — Perfecte. Alora nos va.

**Expository register (self-description):**

> Iste lingua es un lingua zonal romance. Si tu parla espaniol,
> portugues, italiano, frances o rumano, tu pote leger iste texto
> sin studiar. Le gramatica es simple: les verbos no cambia con le
> persona, les adjectivos no cambia con le genero, e tote le
> ortografia se pronuncia como se escribe. Nos mesura le comprension
> con testes reales, e nos publica les resultatos.

(Reader test protocol for Edward: read all three cold, mark every
word that blocked you, note total blockers and whether the meaning
survived. That marked-up list is the first data point and directly
drives the next lexicon iteration.)

## 6. What the Romance constraint does to the engineered traits
(seed for conlang-ow7 — the greenfield-vs-zonal pricing)

| engineered trait (greenfield) | fate under RZ | note |
|---|---|---|
| 220-syllable channel grid | dies | Romance needs ~1.5–3k syllables |
| computed check / register | dies in-language | survives only in tooling (spellcheck) |
| self-segregating morphology | dies | word boundaries by dictionary, not code |
| mode subsystems (digit pairs, 1-syl times) | dies as phonology; portable as *conventions* | could ship as an opt-in "numeric register" but loses density |
| chorded input, 1 stroke/syllable | **survives** | steno proves it for natural langs; regular orthography makes chord theory cleaner than English steno |
| chorded input, 1 stroke/word | weakened | needs briefs (dictionary memorization) — the steno cost returns |
| featural script primacy | dead by decision | Latin-primary (pricing doc); featural ships as input layer + optional display |
| one glyph per word | dies for RZ | Latin text; the fused-character ideal is greenfield-only |
| silhouette/POS-at-a-glance | weakened | Romance suffixes correlate with POS but nothing is guaranteed |
| humility rule / engineered confusion spacing | dies | lexicon is inherited, minimal pairs included |
| learning speed | inverted profile | receptive ≈ 0 h for the zone (~900M); productive est. 30–100 h; outside the zone: no discount |
| beauty | prepaid | Romance euphony comes free; the greenfield must engineer it |

The honest headline: RZ keeps roughly **one** of the greenfield's
engineered traits fully (chorded syllabic input) and trades every
other one for the zero-hour receptive bootstrap. They are different
products: RZ is a *reach* product (billion-reader surface, shallow
ceiling), the greenfield is a *ceiling* product (every trait maxed,
zero-reader start). ow7 should quantify the middle ground (e.g. could
a "greenfield with Romance-skinned lexicon" exist?) before we spend
further.

## 7. Bootstrap mechanics (what actually grows it — survey §3)

1. **Measure early, publish the number.** A 40-item cloze test over
   the three sample registers, n≥30 per source language, before any
   more design. The number (whatever it is) becomes the pitch, as
   84% is Interslavic's.
2. **Readable homepage** — a page in RZ *is* the demo; no "learn
   first" wall anywhere.
3. **Writer tooling before reader tooling** — writers are the
   bottleneck (survey finding): spellchecker, chorded/predictive
   input, a 2k-root dictionary with derivation families.
4. **Parallel texts** (RZ + the five sources side by side) as the
   canonical content format; every text doubles as a comprehension
   advertisement.
5. **Merged authority**: one spec repo, versioned, with a decision
   log — avoid the Interlingua/Neolatino/LFN fork pathology.

## 8. The replicable per-zone recipe (abstracted)

1. Pick the zone and source standards; set reader-base weights.
2. Fix a sight-cognate orthography (shallow rules, familiar shapes).
3. Build the lexicon by weighted written-cognate intersection with
   the §4 tie-breaks.
4. Regularize morphology to person/gender-invariant forms with the
   zone's most recognizable exponents.
5. Draft the three registers (narrative / conversational /
   expository); run cloze tests; iterate lexicon where blockers
   cluster.
6. Ship writer tooling; publish parallel texts + the measured number.

Romance is the pilot; the Sanskritic Interlingua (conlang-4hg) is the
replication test of exactly these eight lines.

## 9. Open questions (parked for Edward, non-blocking)

- Reference pronunciation flavor for c/g before e,i (/ts/ vs /tʃ/ vs
  /s/) — cosmetic for the written-first bootstrap, decide at audio
  time.
- `les` vs invariant `le` — currently `les` (FR recognition +
  redundancy) at the cost of one form.
- Subjunctive: none in v0; revisit if natives report register damage.
- `voler`/`poter` (IT/FR + derivation families: voluntate, potente)
  vs `querer`/`poder` (the .65 Ibero majority) — currently the former;
  the first cloze test should decide, not taste.
- Known blocker-candidates already flagged for the reader test:
  `soplar` (weak for IT/FR readers), `fenestra` vs ES `ventana`.
- Name. (Deliberately unpicked.)
