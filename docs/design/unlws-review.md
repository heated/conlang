# UNLWS reviewed, and what to steal (2026-08-27)

Edward: "review UNLWS & steal its ideas. and show me more of what it is."

> **CORRECTION (2026-08-27, same day).** The first version of this review
> was written from Sai's 2000s-era design manifesto only, and concluded
> that UNLWS leaves negation, quantification, scope, tense and modality
> unsolved. **That is wrong for the system as built.** Having pulled the
> repo and read the actual reference (a published Google Doc behind the
> `s.ai/nlws` iframe), all five are solved, and the solutions are the most
> interesting things here. The struggles section below has been rewritten;
> the steals stand and have grown.

## What I read, and what I did not

**Read in full:** Sai's design manifesto, *Non-Linear Fully-2D Writing
Systems* (`s.ai/essays/nlf2dws`). This is the theory document, and it is
where every mechanism below comes from.

**Now also read:** UNLWS proper. `s.ai/nlws` is a one-line iframe onto a
**published Google Doc**, which is the real reference; and the repo
(`saizai/unlws`, 189 commits, last touched 2026-08-26) carries **131 glyph
PNGs** with self-describing filenames plus the Prayer of St Francis
specimen. A contact sheet of the instructive ones is at
`.ship-notes/workshop/unlws/index.html`.

Sai's status note on the *manifesto* — *"This was never completed, and I've
lost the original accompanying diagrams"* — does not apply to UNLWS, which
is a live system with a Discord community.

## The built system, corrected

Terminology first: the built system says **binding points (BPs)**, not
attachment points.

- **A glyph is a predicate.** *"A glyph expresses a predicate, more or
  less."* There is **no noun/verb distinction** — glyphs are uniformly one
  part of speech.
- **BPs are the argument slots.** *"Each binding point has a meaning,
  referring to one of the participants in the event."* Join two BPs with a
  relation line and *"the entities filling those semantic roles of the
  glyphs involved coincide."*
- **There are no syntactic relations at all.** Subject and object are not
  reified; *all* BPs on a relation line *"have equal status. None of them
  is subordinate to another."* The consequence is startling: the same text
  reads indifferently as *I bought a muffin from Bob* or *Bob sold me a
  muffin*, depending only on traversal. **UNLWS declines the agent/patient
  asymmetry that every one of our layouts is built on.**
- **Rel gaps** — a perpendicular line binding with a small gap — are
  nominalisation and complement clauses: *"X is the fact that an A is B."*
  This is exactly the attachment our proposition rings had nowhere to put.
- **Cartouches** — dotted boundaries — group a region and mark **scope**
  for quantifiers and irrealis, and *"lines penetrate the boundary of a
  cartouche, to make binding points inside and outside coreferential."*
- **Line decorations** carry mood: expectedly, unexpectedly, which-is-good,
  which-is-bad — and *"can take the stroke denoting negation across their
  body"*, so negation composes with mood rather than sitting beside it.
- **TAMs sit inside the glyph**, marking aspect (completive, progressive,
  habitual) and tense.
- **Pronouns are equilateral triangles with different fillings, and they
  exist as a LAYOUT DEVICE** — explicitly to avoid long snaking lines.
  Independent confirmation of the cost problem we measured. Lovely detail:
  a lone pronoun with no match nearby *"raises an implicature that there's
  a part of the text that isn't being shown."*
- **Quotation distinguishes use from mention in the script itself**: double
  quotes for form/inscription, single quotes for meaning.

## What it is

A writing system that is **a multigraph, not a tree** — explicitly not
sentence diagrams, not parse trees, not Hangul-style blocks (which "could be
linearized without loss"), and pointedly **not grid-based**, because grids
create "severe constraints." Non-linearity is "a completely suffusive
feature." Speech is "very low priority": *"no sacrifices will be made for
the benefit of speech, if they impede a more powerful or elegant writing
system."*

### The core mechanism: attachment points

Symbols carry **attachment points (APs) "that are symbolically related to
their roles."** A verb glyph has a distinct AP for each participant, and
joining two glyphs at an AP is what expresses shared reference.

The consequence Sai draws is the one that matters to us:

> "Changes in role requirements… would be visually represented as a simple
> presence or absence of those attachment-points."

**Valency is drawn, not implied.** An intransitive glyph simply lacks a
patient AP. There is no empty slot, because there was never a slot.

### Frames as single symbols

The ambitious version: a whole *frame* — his example is a commercial
transaction — is one symbol, and **buy / sell / lease / borrow / rent /
cost are morphological variations of it**, produced by "fairly obvious and
simple morphological changes to particular nodes, or to the
position/orientation/shape of APs." One glyph, six verbs, distinguished by
which participant is foregrounded.

### Typed connections

Lines are not one thing. Six **copular** types — equation, attribution,
proper inclusion, locational, possessive, existential — carried by
"different squiggles on the line." Plus **conceptual** connections:
causation, theory/data support, argument structure, source attribution,
emotional association, generic association. And **meta-modifications** on
top: metaphoricity, and evidentiality (perceived / reported / tautological
/ habitual).

### Three ways to refer at a distance

1. **Pronouns** — "a closed set of symbols that stands for B".
2. **Hashing** — "a hash pronoun would look like its target, but a somehow
   simplified version."
3. **Pointing** — "as simple as an arrow pointing in the direction of B."

### Levels of detail

"As you look at a large writing from different zooms, you easily make out
different structures" — zoomed out, "the flow of major arguments, of major
figures interconnected"; zoomed in, "what exactly those connections are."
The stretch goal is pointillist: a zoomed-out cluster "looks like" its own
overall meaning.

### Massively fusional variant

Instead of explicit connecting lines, use orientation, shape change and
fusion, so that "single strokes would be part of multiple subparts" and it
becomes "difficult (if at all possible) to give firm dividing lines between
where one character ends and another begins."

## The five ideas to steal, ranked

1. **Attachment points instead of a fixed frame.** This is the fix for the
   exact defect Edward hit — *"stone come from mountain"* looked wrong
   because my renderer forced an agent/predicate/patient/misc grid onto a
   clause with no patient. With APs the predicate glyph carries its own
   slots and an intransitive has no patient slot to leave empty. This is
   `conlang-7j7` (declared place structure) seen from the rendering side:
   the same fact, once in the lexicon, once in the glyph.
2. **Hashing for distant coreference — and it beats our lanes.** A hash
   pronoun is a *simplified miniature of its referent*, drawn locally. Cost
   is O(1) ink wherever it appears. A referent lane costs O(distance): it
   must physically span the page, which is precisely why lanes measured
   3.15× prose in the character test and 4.5× in area. Hashing gets the
   reference-tracking win without paying for the line, and unlike a pronoun
   it is self-identifying. **This is the most valuable single steal here.**
3. **Typed connections.** All our layouts use exactly one line type. UNLWS
   types it — six copulas, a conceptual set, plus evidentiality and
   metaphor as line modifiers. Line style is a channel we are simply not
   using, and it is free.
4. **Levels of detail.** One artifact serving both scales answers the
   direction review's "working set of 3–12 clauses" *and* Edward's "test it
   on longer things" without choosing between them. It also matches the
   only encouraging empirical result in the prior-art survey (spatial
   encoding making something automatic rather than faster).
5. **Frames as symbols.** Too ambitious for us now, but the underlying move
   — one glyph, several verbs, distinguished by which participant is
   foregrounded — is a compression mechanism we have not considered and it
   is not obviously expensive.

## Where it is genuinely open — design around these

Not the abstract operators; those are solved, and better than in our
prototypes. What remains open is navigational and practical.

1. **Reading order is undefined on purpose, and only weakly repairable.**
   *"Reading order is intentionally not defined."* Information structure is
   marked only by *"focus indicated by bolding lines."* Petre 1995 is the
   warning: readers of graphical notations lack navigation cues, work
   visibly harder, and fall back on any text present. Sai's own TODO asks
   *"Will users impose linearity despite design?"*
2. **Editing, insertion and pagination.** Listed as unsolved and
   *"analogous to database problems"*; books are rejected outright — *"A
   nonlinear language would suffer from being chopped up into 8.5×11
   chunks."*
3. **Evidence of readership.** There is a community and a Discord, but no
   comprehension study, no learning-time measure, and little running text.
   Our train/test harness is the thing that could actually supply this,
   for UNLWS as much as for us.

On time specifically, Edward's framing is better than Sai's: *time tends to
be linear but it's not always there, or not there enough to be linear.*
Narrative needs sequence; definitions, taxonomies, specifications and
arguments largely do not. Every text we have tested has been narrative,
which is the case that most favours a linear control. **Non-narrative
content is untested and is where a spatial layer should be strongest.**

## One genuine disagreement to record

UNLWS rejects grids because they impose "severe constraints." Our evidence
points the other way: the schema grid is the layout Edward found "easiest
to learn" and "most similar to prose," Ghoniem found node-link loses to
matrix representations above ~20 vertices on every task except path-tracing,
and the direction review's conclusion was to start from the table.

Both can be right, and the reconciliation is the interesting part: grids
constrain *expressiveness* and buy *learnability*. UNLWS optimizes the first
and pays in the second — a system whose author says it is "difficult for
people who think linearly / verbally" and which has produced very little
running text. For a language whose north star is learning speed, we should
take the opposite side of that trade, and steal UNLWS's *mechanisms* (APs,
hashing, typed lines) into a grid-shaped host rather than adopting its
topology.

## Where this goes

`docs/design/unlws-trailhead.md` is the standing entry point for mining
UNLWS features into GZ.
