# Read RZ today

No vocabulary list, no grammar lesson. Just read:

> Le vento del norte e le sol disputava sobre qui era le plus forte,
> quando un viajator passava, coprite de un manto calde. Les dos
> accordava que le prime a facer le viajator remover su manto seria
> considerate le plus forte. Le vento del norte comenzava a soplar
> con tote su forza, ma quanto plus el soplava, tanto plus le
> viajator se copriva con su manto; e al fin, le vento abandonava le
> tentativa. Alora le sol comenzava a brilar caldemente, e
> immediatamente le viajator removeva su manto. E asi le vento del
> norte deveva reconocer que le sol era le plus forte de les dos.

And a conversation:

> — Bon dia! Cuante costa istes pomos?
> — Dos euros le kilo. Es multo bon, de le region.
> — Alora io prende tres kilos. E aquel fromage, cuante?
> — Doze euros e cincuenta le kilo, ma io te face un precio: onze.
> — Perfecte. Con le pomos, cuante io te debe?
> — Ses e dece-sete… vinte-tres euros e cincuenta.
> — Aqui tene vinte-cinco.
> — E un euro e cincuenta de retorno. Gracias, e a lunedi!

## What just happened

If your reading languages include Spanish, Portuguese, Italian,
French, Catalan, or Romanian — or if English's borrowed Latinate
vocabulary carried you through the fable's plot and the market
haggling — you just experienced the effect this language is designed
to produce. Whether that effect generalizes across the target zone
is exactly the unmeasured claim the project is built to test.

The language is **RZ** (working name: "Romance zonal"), a constructed
auxiliary language designed *receptive-first*: before anyone studies
it, its target zone — roughly 800 million Romance-language readers —
should already be able to read it. Honesty about that claim: the
mechanism is precedented (Interslavic, the same design move for the
Slavic zone, measured **84%** zero-study comprehension in a
large-sample test), but RZ's own number has not been measured yet.
Everything learner-facing in this project is a labeled hypothesis
until the comprehension studies run.

## Why it reads at sight

1. **Words are elected, not invented.** Each concept's form comes
   out of a weighted-recognizability recipe over the Romance zone,
   with derivational-family and international-cognate tie-breaks;
   choices that split the zone are flagged for testing, and a word
   that would mislead a major language's readers is rejected as a
   false friend.
2. **The grammar never surprises you mid-sentence.** Regular verbs
   share one person-invariant table (`io prende, tu prende, el
   prende`); the complete system separately lists three irregular
   auxiliaries (`es`, `va`, `sta`); particles are invariant.
3. **A tiny closed class does the structural work.** The function
   words — articles, prepositions, pronouns, question words — form a
   closed inventory of under a hundred short forms, carrying
   **49.2% of the tokens in the current 628-token project corpus**.
4. **Common learner errors are absorbed, not punished.** Where L2
   speakers of Romance languages typically err, RZ's grammar is
   built so the "error" is either already grammatical or harmlessly
   understood (`docs/design/zonal/rz-error-absorption.md`).

## The on-ramp, by time invested

| you have | do this | you get |
|---|---|---|
| 10 minutes | this page | reading gist (you just did it) |
| an afternoon | [`rz-lite`](design/zonal/rz-lite.md) — ~200 words, 10 patterns | transactional speech: order, ask prices, get directions |
| ~1 hour of study | the closed-class block ([curriculum](design/zonal/rz-curriculum.md)) | ~49% of running text parseable by rule, not guesswork |
| ~4–6 hours | + verb table, top lemmas, derivation families, numbers | ~77–85% of the corpus, full arithmetic and calendar |
| more | [grammar](design/zonal/rz-grammar.md) · [lexicon](design/zonal/rz-lexicon.md) · [texts](design/zonal/rz-texts.md) | the whole language (v0.2) |

(Coverage percentages are measured on the project's 628-token
corpus and flatter toward the high rows — real-world text has a
longer tail. Hour figures are model estimates. Both caveats are
carried in the curriculum doc itself.)

## Where this project goes deeper

RZ is one of two tracks. The other is a from-scratch engineered
language used as a laboratory — channel-coded phonology, a featural
script, a projected chording design at one syllable per hand — and
a **mining gate** ports its mechanisms into RZ only when they
justify their learner-hour price, currently model-estimated [H]
pending calibration. The thesis lives in
[`paper/paper.md`](../paper/paper.md); the project charter in
[`design/program.md`](design/program.md).

Feedback, corrections, and especially "I read X% of the fable and
I'm an L1 speaker of Y" reports are welcome — that is exactly the
data the project is missing.
