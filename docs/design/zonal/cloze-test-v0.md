# RZ cloze test v0 — the first measurement instrument

Workshop draft (conlang-0y7). Goal: a defensible comprehension number
for first-contact Romance readers, before more design happens. The
number is the product (Interslavic's 84% is its best marketing asset
and its design feedback loop).

## Protocol

- **Subjects**: L1 readers of ES / PT / IT / FR / RO, no prior
  exposure, n ≥ 30 per language (crowdsource; friends first).
- **Task**: fill each numbered blank with any word *in your own
  language or English* that fits the meaning. This measures
  *comprehension*, not production — a blank filled with ES "viento"
  for RZ `vento` scores correct.
- **Scoring**: semantic match (accept synonyms); report % correct
  per L1, mean, and per-item failure rates. Items failing across
  all L1s are *design bugs* (lexicon iteration targets), items
  failing in one L1 are weighting bugs.
- **Self-test note**: Edward's own cold read (marked-blocker
  protocol, romance-zonal-v0.md §5) is item-generation input, not a
  data point — he has seen the design.

## Instrument (35 cloze items + 4 gist items, every ~6th content word
deleted)

**Text A — narrative:**

> Le vento del norte e le sol disputava sobre qui era le plus
> __1__, quando un viajator passava, coprite de un __2__ calde. Les
> dos accordava que le prime a facer le viajator __3__ su manto
> seria considerate le plus forte. Le vento del norte comenzava a
> __4__ con tote su forza, ma quanto plus el soplava, tanto plus le
> viajator se __5__ con su manto; e al __6__, le vento abandonava le
> tentativa. Alora le sol comenzava a __7__ caldemente, e
> immediatamente le viajator __8__ su manto. E asi le vento del
> norte deveva __9__ que le sol era le plus __10__ de les dos.

Key: 1 forte/strong · 2 manto/cloak · 3 remover/take off ·
4 soplar/blow · 5 copriva/covered · 6 fin/end · 7 brilar/shine ·
8 removeva/removed · 9 reconocer/admit · 10 forte/strong

**Text B — conversational:**

> — Bon __11__! Como tu sta?
> — Multo __12__, gracias. E tu?
> — Anque ben. Tu vole __13__ un cafe con me?
> — Si, con __14__. Io conoce un bon sitio __15__ de aqui.
> — Perfecte. Alora nos __16__.

Key: 11 dia/day · 12 ben/well · 13 prender/take-have ·
14 placer/pleasure · 15 proxime/near · 16 va/go

**Text C — expository:**

> Iste lingua es un lingua zonal __17__. Si tu parla espaniol,
> portugues, italiano, frances o rumano, tu pote __18__ iste texto
> sin __19__. Le gramatica es __20__: les verbos no cambia con le
> __21__, les adjectivos no cambia con le __22__, e tote le
> ortografia se __23__ como se escribe. Nos mesura le __24__ con
> testes reales, e nos __25__ les resultatos.

Key: 17 romance · 18 leger/read · 19 studiar/studying ·
20 simple/easy · 21 persona/person · 22 genero/gender ·
23 pronuncia/pronounces · 24 comprension/comprehension ·
25 publica/publish

**Text D — news:**

> Le governo anunciava __26__ un nove programa de energia __27__. Le
> plan preve la construccion de __28__ centrales en le sud del
> __29__ durante les proximes cinco annos, con un __30__ total de
> dos miliardes de euros. Segun le ministra de energia, le programa
> va __31__ plus de cuatro mil emplees e va __32__ les emisiones de
> carbon en vinte per __33__. Les organizaciones ambientales
> reciveva le __34__ con optimismo prudente, ma demandava plus
> __35__ sobre le calendario de construccion.

Key: 26 hodie/today · 27 solar · 28 tres/three · 29 pais/country ·
30 investimento/investment · 31 crear/create · 32 reducir/reduce ·
33 cento/percent · 34 anuncio/announcement · 35 transparencia

**Items 36–39 (gist, one per text):** "In one sentence, what was this
text about?" — scored pass/fail.

**Two published numbers, always** (reader test 01's lesson: "kinda
knew what was going on" is a distinct state): the **specifics score**
(cloze % correct) and the **gist score** (summary pass rate). In-zone
readers should be high on both; out-of-zone Latinate readers (e.g.
English) high-gist/low-specifics. If in-zone readers ever pattern
gist-only, the lexicon is failing its zone — that's the alarm the
single blended number would hide.

## The cross-test matrix (one experiment family, four numbers)

Run the same protocol on **both** languages × **both** populations:

| | Romance-L1 readers | EN-L1 readers |
|---|---|---|
| RZ texts | the zone number (target: Interslavic-class) | measured gist-only (reader test 01 predicts) |
| AZ-a texts | **the open number that decides AZ-b's fate** | ≈100% by construction (control) |

If AZ-a×Romance lands 70%+, the Atlantic strategy collapses happily
into a controlled English register plus tooling and AZ-b/RZ effort
gets re-weighed; if it lands low, RZ (in-zone) and AZ-b (bridge)
each keep their niche. This matrix is the cheapest decision
mechanism the project has — run it before any further zonal design.

## Notes for v1

- 35+4 items is pilot-ready. Before the crowdsourced run, oversample
  the FLAG rows from core-conversational.md (the recipe's genuine
  uncertainties) with a dedicated item block.
- Also collect per-blank confidence (1–3) — separates "recognized"
  from "guessed from context", which prices cognate quality vs
  syntax quality separately.
- Control idea when convenient: same test with Interlingua text on a
  matched sample, so RZ's number has a comparator beyond Interslavic's
  published 84%.

## v1 — the $30 micro-study (2026-08-30, conlang-5i1.1)

Edward's constraints (2026-08-30): Prolific is allowed with a hard
ceiling of **$30 per study**; no LLM-as-reader proxy; "if that's not
enough, don't bother." His doubt, recorded: a cloze may add little if
RZ is basically Interlingua. The agent's read agrees for the
RZ-vs-Interlingua question — the surface deltas are a small-effect
comparison that needs n in the hundreds per language — and re-scopes
the study to the one thing $30 buys that has value on its own.

**Primary outcome (the thing $30 buys).** The first measured
zero-study cloze number for Interlingua-class text among Romance-L1
readers — a data point the baseline has lacked since 1951. Reported
as a mean with a 95% CI, per source language and pooled, with the
gist score alongside (§"Two published numbers").

**Secondary, exploratory, explicitly underpowered.** A within-subject
contrast of RZ orthography/lexicon vs Interlingua orthography/lexicon
on matched passages. With n≈25 the detectable paired effect is on the
order of 15 points on a 10-item passage; a small real delta will read
as noise. The report must say so, and must not present a null as
"no difference."

**Design.**
- Two 10-blank passages per participant: Text A (fable) and Text D
  (news), one rendered in RZ and one in Interlingua, counterbalanced
  in four groups (A-RZ/D-IA, A-IA/D-RZ, and the two orders). 20
  blanks + 2 gist items ≈ 4 minutes.
- Prescreen: first language Spanish, Portuguese, Italian or French
  (Prolific "first language" filter); exclusion question at the end:
  "Have you ever studied Interlingua or another constructed
  language?" (self-report; exclude yes).
- Hosting: a Google Form (free) with a Prolific completion code;
  scoring by hand against the key with semantic matching (the auto
  scorer on the reader page is a demo, not the protocol).
- Interlingua arm: the renderings must be REAL Interlingua, checked
  against the IED/grammar or an Interlingua-community reader — model
  recall is not a source (conlang-7ds). Until checked, the arm is not
  runnable.

**Cost (estimate — verify on Prolific's pricing page before
launch).** £9/hr recommended rate × 4 min = £0.60 per participant;
n=25 → £15.00; Prolific service fee ~33% → ≈£20; ≈$27 at current
rates. Under the ceiling with margin for a 5-minute median. At the
£6/hr minimum (rated "low"), n≈35 for the same money.

**Go / no-go.** Go, on the agent's judgment: one real number with a
wide CI beats zero real numbers, and the cost is inside the ceiling.
The launch itself is Edward's (payment); the agent prepares the full
packet — form text, both renderings, prescreens, consent line,
scoring key, analysis script — and files it for his one-click review.
