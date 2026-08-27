# UNLWS → GZ: research trailhead

Standing entry point for mining UNLWS mechanisms into GZ. Opened by Edward
2026-08-27 ("we're gonna need an official trailhead for more research on
exploring UNLWS features for GZ, high-ish priority"). Tracker epic:
**conlang-r8u**.

Background and the corrected review: `unlws-review.md`. Contact sheet of
real glyphs: `.ship-notes/workshop/unlws/index.html`.

## The framing this operates under (Edward, 2026-08-27)

> "I'd like you to see the language as composed of modular systems. A
> writing system that spends learning time to buy something is something
> I'm willing to entertain."

This supersedes how the spatial-layer docs had been arguing. Earlier drafts
kept concluding "X cuts against the learning-speed north star" and treating
that as decisive. It is not. GZ is a portfolio of subsystems, each of which
may **spend** learner hours if it **buys** something worth the hours. So the
question for every mechanism below is not "is it free?" but **"what does it
buy, and is that worth its price?"** — the same purchase-ledger logic
`learning-budget.md` already applies elsewhere.

## Sources, and their status

| source | status |
|---|---|
| UNLWS reference (published Google Doc behind the `s.ai/nlws` iframe) | read, primary |
| `saizai/unlws` repo — 131 glyph PNGs, self-describing filenames, St Francis specimen | pulled, partially read |
| Sai's manifesto `s.ai/essays/nlf2dws` | read in full; predates the built system, **do not cite for current mechanisms** |
| UNLWS Discord (`s.ai/nlws/discord`); `#tech_chat`, "meta meta conversation" | **not read** — the README points here for current work |
| Alex Fink's LCC talks | not read |
| `francis_explanation.png` (2550×3300 annotated specimen) | pulled, not yet studied |

## Mechanism inventory, with steal status

| mechanism | what it is | status for GZ |
|---|---|---|
| **Binding points** | every glyph carries one BP per semantic argument; joining BPs makes the roles coincide | **live** — the rendering face of `conlang-7j7` (declared place structure) |
| **Pronouns as layout device** | triangles with fillings, used explicitly to avoid long snaking lines; hashing in the manifesto | **live** — `conlang-v9m`, the answer to lane cost |
| **Rel gaps** | perpendicular line + small gap = nominalisation / complement clause | **to evaluate** — solves what our rings could not attach |
| **Cartouches** | dotted boundary marking scope for quantifiers and irrealis; lines cross it to stay coreferential | **to evaluate** — the only scope mechanism we have seen that is drawn rather than assumed |
| **Line decorations** | mood (expectedly / unexpectedly / good / bad); negation strikes *through* the decoration | **live** — `conlang-hk4`, typed lines |
| **TAM inside the glyph** | aspect and tense in a region of the glyph | to evaluate against GZ's particle TAM |
| **No noun/verb distinction** | glyphs are uniformly predicates | probably reject — GZ's POS channel is load-bearing elsewhere |
| **No subject/object** | all BPs equal status; *I bought from Bob* ≡ *Bob sold me* | **open question, and the sharpest one** — see below |
| **Quotation** | double quotes = form, single = meaning; use/mention in the script | to evaluate — cheap, and nothing else in GZ does it |
| **Levels of detail / zoom** | same text readable at several scales | to evaluate |
| **Frames as one symbol** | buy/sell/lease/rent as morphological variants of one transaction glyph | parked — ambitious |

## The sharpest open question

UNLWS has **no syntactic relations at all**: subject and object are not
reified, and every binding point on a relation line has equal status, so a
text reads indifferently as *I bought a muffin from Bob* or *Bob sold me a
muffin*. Every layout we have built assumes the opposite — agent and patient
are asymmetric, and that asymmetry is what our caps, columns and sides
encode.

Two live possibilities, and they lead different places:

- The asymmetry is **real and worth keeping**, in which case UNLWS pays for
  its symmetry with reading-order ambiguity, and we should say so.
- The asymmetry is **an artefact of the languages we know**, in which case
  a large part of what our layouts spend ink on is encoding something the
  reader could recover for free.

This is testable with the train/test harness and is worth testing before
committing to place structure, because declared places bake the asymmetry
in.

## What is untested and probably matters most

Every specimen we have built is **narrative**. Per Edward, 2026-08-27:
*time tends to be linear but it's not always there or there enough to be
linear.* Definitions, taxonomies, specifications, arguments and procedures
have little or no temporal sequence, and that is precisely the content where
a linear control is weakest and a spatial layer should be strongest. It is
also where the direction review put the killer application (contracts,
procedural texts, semantic diffing).

**Next round should test non-narrative content**, not longer narratives —
`conlang-8zd`, and the highest-priority child of the epic.

## Open threads

1. Read the Discord — the README points there for current work, and it is
   the only route to what the community has already found painful.
2. Study `francis_explanation.png` — a real annotated page is worth more
   than the reference for learning how it reads at length.
3. Build the hashing experiment (`conlang-v9m`) and measure against lanes.
4. Declare place structure for the seed lexicon and render from it
   (`conlang-7j7`) — Edward has approved gathering evidence.
5. Price each adopted mechanism in the learning budget, per the modular
   framing above, rather than asking whether it is free.
