# UNLWS reviewed, and what to steal (2026-08-27)

Edward: "review UNLWS & steal its ideas. and show me more of what it is."

## What I read, and what I did not

**Read in full:** Sai's design manifesto, *Non-Linear Fully-2D Writing
Systems* (`s.ai/essays/nlf2dws`). This is the theory document, and it is
where every mechanism below comes from.

**Could NOT read:** UNLWS proper — the system Sai and Alex Fink actually
built. `s.ai/nlws` serves a JavaScript renderer with no text; the GitHub
repo (`saizai/unlws`, 189 commits, **last touched 2026-08-26**, Git-LFS
assets, active Discord) did not render its README to me. So the glyph
inventory, the current grammar, and the worked specimens are **unverified**.
Everything below describes the *design*, and the built system may well have
solved things the essay lists as open. Flagged, not assumed.

Sai's own status note on the manifesto: *"This was never completed, and
I've lost the original accompanying diagrams."*

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

## Three places it demonstrably struggles — design around these

1. **Negation, quantification, scope, tense, modality are unsolved.** They
   appear in the TODO, not the design. This is precisely what Stenning &
   Oberlander predict: graphical systems "limit abstraction and thereby aid
   processibility," so the abstract operators are what a graph gives up.
   Our oracle-coverage gate already catches this class of failure, and it
   should stay the first gate any spatial candidate passes.
2. **Time is linear and the system is not.** Sai concedes it directly:
   *"To write a sequence of events, you will need some sort of (linear)
   connection."* He argues causation is often circular or multithreaded and
   so better served — true, but narrative order is not, and this is exactly
   how our S3 rings failed the oracle gate on clause order.
3. **Reading order, editing, and pagination are all open.** "There is no
   single traversal method"; editing is listed as unsolved and "analogous
   to database problems"; and books are rejected outright — *"A nonlinear
   language would suffer from being chopped up into 8.5×11 chunks."* His
   own TODO even asks *"Will users impose linearity despite design?"* Petre
   1995 answers that: readers of graphical notations lack navigation cues
   and fall back on any text present.

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

## Open

I could not verify the built system. If it matters, the routes are the
UNLWS Discord, the LFS assets in `saizai/unlws`, and Alex Fink's LCC talks.
Worth doing before we implement APs, in case they have already found the
failure modes.
