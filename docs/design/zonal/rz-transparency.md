# Per-L1 cognate availability of the RZ corpus
(exploration, 2026-08-22, conlang-i78; tool: tools/transparency.py,
data: tools/transparency_data/)

## What this measures — and what it deliberately does not

The receptive-first claim has so far ridden entirely on precedent
(Interslavic's 84% is Interslavic's number, for its zone). This
audit makes the *lexical layer* of RZ's own claim inspectable — but
it is scoped by a methodological correction from Edward (2026-08-22)
that reshaped the instrument:

> AI annotators know ~all the languages, so "judge how this reads
> to someone who only knows Spanish" is contrived — a simulation of
> ignorance, not a measurement of it.

Accepted. The instrument therefore does NOT claim to measure
recognition (a property of readers). It measures **cognate
availability** — properties of the language *pair* that an
annotator who knows both languages is exactly qualified to state:

- does the judged language have an everyday word cognate with the
  RZ form? (**T** — anchor recorded, e.g. `aqua` → ES *agua*)
- is the nearest hook register-restricted or form-obscured — real
  but learned? (**P** — e.g. `cane` → ES *canino*, everyday word
  *perro*)
- is there no usable relative at all? (**O**)
- does the nearest neighbor mean something else — a misleading
  hook? (**F** — e.g. `oficina` vs IT *officina* 'workshop')

Each judgment carries its anchor word, so every cell is auditable
and in principle corpus-checkable (the T/P register line could be
hardened against L1 frequency lists; F against attested false-friend
inventories). Whether an *actual monolingual reader* converts an
available cognate into recognition — and at what rate per class —
is a reader fact this audit cannot supply. The cloze measures it;
until then any recognition inference from these tables is [H], and
the per-class conversion rates are exactly what a cloze pilot
should be designed to estimate.

Evidence labels: judgments [A] (annotator-stated lexical relations,
single-pass, auditable via anchors); aggregation [D]; recognition
implications [H].

## Rubric

Full text: tools/transparency_data/RUBRIC.md. Tie-breaks go
downward (anti-inflation); F outranks P/O whenever a misleading
everyday neighbor exists; English is judged through its
everyday-vs-Latinate stratum split (aqua→*aquatic* is P, not T).

## Results

(populated by `python3 tools/transparency.py`; **status: ES and EN
complete (279/279 lemmas each); PT, IT, FR pending** — their
annotation passes were interrupted by session limits, completion
bead filed)

Token-weighted cognate availability, 628-token corpus:

| L1 | T everyday | T+P (adds learned/obscured hooks) | F misleading | O none | closed-class T | open-class T |
|---|---|---|---|---|---|---|
| ES | **73.4%** | **97.5%** | 2.1% | 0.5% | 69.9% | 76.8% |
| EN | 24.8% | 55.7% | 2.7% | 41.6% | 8.1% | 41.1% |

Per-text everyday-cognate (T) share: rz-texts 71% ES / 21% EN;
romance-zonal-v0 (fable + registers) 77% ES / 29% EN; rz-lite
64% ES / 29% EN.

## Reading the numbers

1. **For a Spanish reader, availability is near-total**: 97.5% of
   running tokens have at least a real hook, only 0.5% have none.
   That is the lexicon recipe doing what it claims — as a
   *pair-level fact*. What fraction of available hooks convert to
   actual recognition is the [H] the cloze must price; these tables
   say the ceiling is high, not that the ceiling is reached.
2. **English rides the Latinate stratum on content, not
   structure**: open-class T is 41% but closed-class T is 8% — the
   function words carrying half the text have almost no everyday
   English hooks. Majority coverage (55.7%) exists only via learned
   hooks. This quantifies, for the first time here, why EN readers
   report gist rather than fluency-feel on RZ text (consistent with
   Edward's own EN-L1 gist-only report in the decisions log —
   n=1, anecdotal).
3. **The E/R/M debate's missing constituency, numerically**: the
   closed class is the transparency floor for out-of-zone readers
   and the transparency *ceiling* barely matters for in-zone ones
   (ES closed-T 69.9% is already below its open-T 76.8%) — function
   words are where zone languages diverged most, which is exactly
   why the closed-class block is the curriculum's hour one.
4. **Availability ≠ absence of hazard**: ES's 2.1% F is small but
   includes structural words (`anque`, see fix-list) where a
   misreading flips clause logic, not just a noun.

## The fix-list

The audit's practical output is the per-language list of
high-frequency O and F lemmas — each is a candidate for re-election
in the lexicon recipe, a mandatory gloss in the S1 reader, or an
accepted cost with a name.

- **`atende` (wait) — F in BOTH judged languages** (ES *atender* =
  serve/pay attention; EN *attend* = be present at). Already
  FLAGged in the texts commentary; now the audit's top re-election
  candidate (candidate: *espera*-family, itself an ES/PT-ward
  trade — needs the recipe run).
- **`anque` (also) — F for ES** (*aunque* = although): a
  clause-logic hazard on a closed-class word; candidates *anche*
  (IT-ward) / *tambien*-family need a recipe pass. High priority
  because closed-class words are unavoidable.
- **`vole` (want) — F for ES** (*vuele/volar* = fly) and `pomo`
  (apple — *pomo* = doorknob/pommel): confirm existing lexicon
  FLAGs with a mechanism (misleading everyday neighbor), not just
  a split-zone note.
- **EN F set** (`ma`→Ma/mom, `sin`→sin, `face`→face, `atende`):
  mostly unfixable without damaging the zone (EN is out-of-zone);
  these become mandatory glosses in any EN-facing reader artifact.
- **ES O set is tiny and peripheral** (`fromage`, `pepe`,
  `sortita` — all singletons, all already FLAGged or coined):
  no re-election urgency from opacity on the ES side.

## Hardening path (filed, not done)

1. **Split the anchor field into data**: translation equivalent +
   hook word + register, as separate machine-readable fields.
2. **Mechanical similarity**: normalized orthographic distance
   (Levenshtein) between RZ form and hook word — the standard
   intercomprehension-literature predictor [TODO-verify primary
   sources] — replacing the T/P boundary with an explicit
   threshold.
3. **Register from corpora**: everyday-vs-learned decided by the
   hook's rank in an L1 frequency list, not by the annotator.
4. **Calibration**: the cloze pilot estimates per-class recognition
   rates, converting availability tables into predicted
   comprehension with error bars.

## Method caveats

- Single-pass, one annotator per language; no inter-annotator
  agreement measured. The anchors are the audit trail.
- The corpus is small (628 tokens) and register-narrow; shares are
  in-corpus facts, not language-wide estimates.
- Inflection familiarity is out of scope: `parlava` is judged at
  lemma `parla`; the -va past is IT-transparent but novel to ES/FR
  readers — a grammar-side question this lexical audit does not
  cover.
