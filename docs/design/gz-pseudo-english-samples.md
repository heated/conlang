# GZ grammar in pseudo-English (2026-08-27)

Edward: "show me examples of GZ grammar in pseudo-english."

English roots run through GZ's actual machinery, so the grammar is visible
without the vocabulary getting in the way. The three schemes below are the
**open decision** in `gz-sketch.md` ("the central dial: endings vs
recognizability"), not three of my inventions — the sketch defines them and
parks the pick.

## The machinery

- **Analytic SVO, head-initial, no inflection.** No number, no gender, no
  agreement, no case (gf-grammar §1).
- **Modifiers POSTPOSED** — this is the most visibly non-English thing:
  *bridge stone*, not *stone bridge*.
- **Grammar words are the Romance clitic class** (gz-sketch §"the fruit"):
  `le` the, `de` of/from, `a` to/at, `no` not, `va` past, `que` that.
  26 members, ~38% of running tokens.
- **POS marking is the dial**, below.

## The same paragraph, three schemes

> The engineer built a stone bridge in the valley. The bridge crosses the
> river. The river flooded the valley in spring. The flood did not damage
> the bridge. The engineer says the stone held. The stone came from the
> mountain. The village praised the engineer.

### E-scheme — Ido-like: `-o` noun, `-a` adjective, `-e` adverb, `-ar/-as/-is` verb

```
Le engineero buildis le bridgeo stona a le valleyo.
Le bridgeo crossas le rivero.
Le rivero floodis le valleyo a le springo.
Le floodo no damagis le bridgeo.
Le engineero sayas que le stoneo holdis.
Le stoneo comis de le mountaino.
Le villageo praisis le engineero.
```

Fully deterministic: **the last letter of every content word is its part of
speech**, and `-is` vs `-as` carries tense on the verb itself. The sketch's
verdict is that this does "most violence" to Romance shapes (*sol* → *solo*
collides with "alone", and uniform `-o` "reads alien").

### M-scheme — middle: verbs and adverbs marked, nouns and adjectives bare

```
Le engineer va buildar le bridge stone a le valley.
Le bridge crossar le river.
Le river va floodar le valley a le spring.
Le flood no va damagar le bridge.
Le engineer sayar que le stone va holdar.
Le stone va comar de le mountain.
Le village va praisar le engineer.
```

Marks "the two classes whose confusion costs parsing the most". Nouns keep
their Romance shape; tense moves out to the `va` particle.

### R-scheme — RZ-conservative: nothing marked in speech

```
Le engineer va build le bridge stone a le valley.
Le bridge cross le river.
Le river va flood le valley a le spring.
Le flood no va damage le bridge.
Le engineer say que le stone va hold.
Le stone va come de le mountain.
Le village va praise le engineer.
```

POS is carried by the particle class, by position, and **by the script
layer only** — verb = full underbar, adjective = leading half-bar, already
prototyped in `rz-script-adaptation.md` §3b. Zero violence to Romance
shapes; the channel exists in writing and syntax but not in sound.

## What this buys the spatial layer

Under **E**, a renderer needs no lexicon at all: `buildis` ends in `-is`, so
it is the predicate, full stop. Under **M** it needs one rule. Under **R**
the spoken form is ambiguous and the renderer depends on the script layer —
which is fine, because the spatial layer *is* a script layer, so R costs it
nothing either. That is worth noticing: **the scheme choice matters much
less to the spatial layer than to speech**, because a rendering can always
read the written channel.

Two open details I could not settle from the docs, flagged rather than
invented: whether `va` is a preverbal particle or a suffix (the sketch
writes "-va past" with a hyphen but lists `va` among the clitics), and how
plurality works given that `les` appears in the clitic list while the
grammar declares no grammatical number.

## Coreference, and why no grammar here helps

**Coreference** is two mentions pointing at the same thing. *The engineer
built a bridge. He crossed it.* — `he` is the engineer, `it` is the bridge.
Readers resolve this constantly without noticing.

The spatial layer cannot avoid it: a referent lane means *same entity, same
lane*, so the renderer must know that mention 7 and mention 23 are the same
bridge before it can draw either. **Our prototype got this for free and
therefore fake** — the test texts repeat the identical lexeme every time, so
matching strings was enough. Real text says *it*, *the structure*, *the
span*, or nothing at all, and none of those match.

Why the three grammars are equally unhelpful: English pronouns are
ambiguous (*it* could be the bridge or the river); Chinese is worse, because
it simply drops the argument (*打了* — "[someone] hit [something]"); and GZ
inherits ordinary Romance pronouns. None of them mark "this is the referent
I mentioned four clauses ago."

**But some languages do mark it, and that is the real answer to the
question.** Two mechanisms exist:

- **Switch-reference** (widespread in Papuan and North American families):
  a clause marks whether the *next* clause's subject is the SAME referent
  or a DIFFERENT one. Coreference becomes a grammatical fact rather than an
  inference.
- **Obviation** (Algonquian): when two third persons are in play, one is
  proximate and the other obviative, and the marking persists across
  clauses — so *he* and *the other he* are formally distinct.

Either would hand the renderer its lanes for free, and neither is exotic
enough to be unlearnable. Switch-reference in particular is one bit per
clause. Filed as its own question, because adding it changes what the
language is, not how it renders.
