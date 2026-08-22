# RZ lexical coverage curves (measured 2026-08-22, conlang-i78)

What is one lemma WORTH, in percent of running text? The learning
budget prices lexicon acquisition in hours but had never measured the
value side. `tools/coverage.py` measures it on the de-duplicated RZ
corpus: **628 tokens** from rz-texts / romance-zonal-v0 / rz-lite
blockquotes.

**Second revision note (2026-08-22, caught while building the
transparency audit).** Two more corpus bugs, both now fixed:
(4) an English design-note *blockquote* in romance-zonal-v0.md §10
was being swept into the "RZ corpus" (~60 English tokens — corpus
convention is blockquote = RZ text, and that quote violated it; the
doc is reformatted). Removing it moves the corpus from 690 → 628
tokens and RAISES the closed-class share from 45.2% → 49.2%
(English content tokens were diluting it). (5) numerals were being
plural-stripped (*tres* → *tre*); a numeral guard now blocks that.

**Revision note (Codex review, same day).** The first run of this
document reported 937 tokens and a 49.4% closed-class share. Both were
wrong, in three separate ways, all now fixed and re-measured:
(1) the corpus double-counted `cloze-test-v0.md`, which reproduces the
romance-zonal-v0 passages with content words blanked — inflating the
function-word share; (2) the closed-class set mixed in lexical items
(greetings, regular verbs like *pote/vole/face*) while omitting real
grammar words (*la, multe, poc, necun*); (3) the lemmatizer stripped
bare class vowels, turning *parla* into *parl* and *parlate* into
*parl*. Verbal morphology is now delegated to `rz_script.analyze()`,
which gates tense suffixes on an attested verb-stem set. Numbers below
are the corrected ones.

## Headline findings

1. **Nearly half the language is 60 grammar words.** The closed class
   — articles, demonstratives, possessives, quantifiers, pronouns,
   prepositions, conjunctions, negators, question words, comparison
   particles, and the three irregular verbs that double as auxiliaries
   — covers **49.2% of running tokens** with 60 words attested. The
   selection rule is explicit: exactly the items enumerated in
   rz-grammar.md §2-§7 (words that merely feel functional, like
   *gracias* or *prende*, are open-class and excluded). This is the
   first-lesson block: one page of grammar words puts every second
   token within reach. Natural-language comparison: English function
   words cover ~40-50% of running text, so RZ sits squarely in the
   natural band.
2. **~124 content lemmas → 70% of content tokens; ~204 → 95%**
   (in-corpus). With the closed class known, the open-class curve is:
   50% at 61 lemmas, 70% at 124, 80% at 156, 90% at 188, 95% at 204.
3. **The corpus CANNOT size the real-world lexicon — and saying so is
   the finding.** A truncated normalized Zipf fit gives exponent
   α ≈ 0.55, shallow enough that the 95%-coverage rank is set almost
   entirely by the assumed vocabulary size V rather than by the data
   (V=1,000 → rank ~900; V=3,000 → ~2,690; V=8,000 → ~7,160). The
   earlier "~470-510 lemmas" figure came from an unnormalized tail sum
   and is **withdrawn**. The honest statement: at this corpus size the
   head of the curve is measured and the tail is unknown; sizing the
   productive lexicon needs a broader corpus, not a better fit.
4. **The regularity dividend is now visible in the curves** — and
   still mostly a grammar fact. Surface-vs-lemma gap: 13 fewer items
   for the same coverage at 80-95% (e.g. 261 surface forms vs 248
   lemmas for 95%). That gap is small only because a 628-token corpus
   shows most content words once. From the grammar instead: an RZ
   lemma carries ~3.67 recognizable forms on average (verb 7, noun 2,
   adjective 2, all exceptionless) vs Spanish's ~19.67 synthetic forms
   (verb 53, noun 2, adjective 4) — **recognition-load ratio ≈ 5.4x**,
   with zero irregulars. For the Romance cohort this is mostly moot
   receptively (they own the donor paradigms already), which is again
   the GZ thesis: regularity pays in the cohorts the zone doesn't
   serve.

## Ledger implication

The shape, not the size, is the transferable result: **60 closed-class
words = ~49% of tokens, then a long shallow content tail.** Curriculum
order follows directly (rz-curriculum.md): closed-class block → ~125
lemma core → topic packs. The absolute size of the C1 lexicon stays as
the ledger already has it — a model estimate, now explicitly NOT
backed by a corpus extrapolation.

## Caveats

- n = 628 tokens of largely translated/parallel material; register
  breadth is narrow, so the tail is underestimated by any fit.
- The lemmatizer is grammar-driven for verbs (shared analyzer with the
  script renderer) but heuristic for nominal plurals; spot-checked
  against rz-grammar §4/§9, not gold-standard annotated.
- Derivation stripping (root curve) merges only 2 items at the head;
  the derivation multiplier remains a grammar-side argument, not a
  corpus measurement. The -ia family is deliberately not stripped
  (it over-strips inherited *materia/historia*).
