# Which grammar makes a spatial layer easy? (2026-08-27)

Edward: "compare English's grammar to that of GZ or Chinese for me — is
there some simpler grammar that makes this whole task easier?"

## What the layer actually needs from a grammar

To render a discourse spatially you must first recover, deterministically:
word boundaries, part of speech, which word is the predicate, the role of
each argument, **how many argument slots this predicate even has**,
coreference, tense/aspect, polarity, what each modifier attaches to, and
where clauses begin and end. Every one of those is a place a grammar can
help or refuse to.

## The comparison

| what the renderer needs | English | Chinese | GZ |
|---|---|---|---|
| word boundaries | spaces — free | **none in text**; segmentation is a research task | particle class + prosody give a hard boundary |
| part of speech | covert (*stone* is noun, verb or modifier with no marking) | near-zero morphology; POS is almost purely distributional | **overt ending** (E-scheme -o/-a/-e/-ar/-as/-is), and 63% of Romance content tokens already fit it |
| oblique roles | prepositions, massively polysemous (*in* = place, time, state, or lexically governed) | coverbs 在/从/给/用 — transparent, one role each | **26-member closed clitic class**, one role each, 38% of tokens |
| valency (how many slots) | unpredictable; dative shift, passive, ergative *the window broke* | argument dropping everywhere (zero anaphora) | POS-alternation classes O/A/P/R declared **per root in the lexicon** |
| tense / aspect | auxiliaries plus irregular inflection | particles 了 / 过 / 着, position-fixed — very clean | preverbal particle |
| polarity | do-support; scope famously slippery (*all that glitters is not gold*) | 不 / 没 preverbal — clean | dedicated particle |
| modifier attachment | **PP-attachment ambiguity is the classic parsing problem** | 的 marks it explicitly | POS-marked modifier + fixed position |
| clause boundaries | complementiser *that* is optional | serial verb constructions blur them | complementiser particle |
| coreference | pronouns, ambiguous | worse — arguments simply dropped | ordinary pronouns; **no better than English** |

## Reading the table

**English is the worst of the three for this job**, and the two places it
fails are exactly the two that hurt round 1. Its oblique roles are carried
by prepositions that mean four different things each, which is why the
grid's oblique column degenerated into the grab-bag Edward flagged and had
to become an honest "misc". And its part of speech is covert, so nothing
in the string tells the renderer that *stone* is a modifier here and a noun
two clauses later.

**Chinese is better than English at the sentence level and worse at the
word level.** Its aspect particles, its negation, and especially 的 for
modifier attachment are cleaner than anything English offers — 的 alone
solves a problem English has never solved. But it hands you an unsegmented
character stream and no morphology, so before you can draw anything you
must solve word segmentation and POS tagging, both of which are error-prone.

**GZ is built for this**, mostly by accident: every mechanism that makes it
fast to *learn* also makes it easy to *extract*. An overt POS ending, a
closed particle class with one role per particle, declared valency classes,
and particles rather than inflection for tense and polarity mean the parse
is a lookup, not an inference. This is the "machine-parseable by
construction" claim, and the table is what it cashes out to.

**Nothing helps coreference.** All three are equally bad, which is worth
saying plainly because coreference is the thing the referent-lane layout
was invented to fix. The lane mechanism is doing work no grammar does.

## The awkwardness Edward noticed was not grammar

"*stone come from mountain* being a fairly awkward fit" — that clause is
fine English. What was awkward was my renderer forcing a fixed
agent / predicate / patient / misc frame onto a clause that has no patient,
leaving a hole. Chinese and GZ would leave the same hole.

But the grammar *does* fix it, one level up: because GZ declares valency in
the lexicon, the renderer can know the clause's shape **before** drawing it
and allocate the right frame — two slots for an intransitive, three for a
transitive — instead of a one-size grid with gaps. In English it would need
a valency lexicon and would still guess wrong on alternations.

## Is there a simpler grammar still?

Yes, and it is the one idea worth stealing here: **fixed place structure
per predicate**, as in Lojban, where every predicate declares exactly how
many argument slots it has and what each one means (x1 the agent, x2 the
thing given, x3 the recipient…). Then the spatial frame is *a property of
the word*, not a template imposed on it — the glyph arrives knowing its own
shape.

That is also, independently, what UNLWS does with attachment points, and
what makes its glyph-joining work at all. Two systems reached it from
different directions, which is a decent signal.

GZ's four POS-alternation classes are a weak version of the same idea: they
tell you how a root behaves under noun/verb/modifier alternation, but not
how many arguments it takes. **Extending them to declared place structure
is the cheapest grammar change that would materially help the spatial
layer** — and it costs the learner one fact per root, which is the same
price the alternation class already charges.

## Recommendation

Build the next round on GZ, not English. Concretely, it buys: role marks
that come from a closed set instead of a polysemous preposition; a frame
allocated per clause from declared valency instead of a fixed grid; and
POS available for free in the script layer, which the sketch already notes
costs speech nothing.

Keep an English rendering as the control, since Edward has to be able to
read the thing to judge it — but stop treating English structure as the
thing being tested, because it is the worst of the three and the layer's
difficulties on it are partly its own.

Open question this raises for the language, not the layer: whether GZ
should adopt **declared place structure** per root. That is a real
learner-cost decision and belongs to Edward, not to the rendering lane.
