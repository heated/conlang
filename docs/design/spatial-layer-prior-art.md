# Spatial sentence layer: prior art and two corrections

(conlang-4j7, 2026-08-26. Edward: "curious if there's existing spatial
stuff we can draw inspo from… or if AI can help somehow.")

Seven parallel research passes, ~200 searches plus direct retrieval from
Crossref / OpenAlex / Unpaywall / Europe PMC. Everything here is [H]
unless marked. **Sources that could not be obtained are listed at the
end of the survey transcript and must not be cited without checking.**

## Two corrections to premises this lane was built on

**1. The ~39 bits/s figure is about SPEECH, not reading.** Coupé, Oh,
Dediu & Pellegrino, *Science Advances* 5(9):eaaw2594 (2019): 17
languages, 170 speakers, 4.8–8.0 bits/syllable × 4.3–9.1 syllables/s =
**39.15 bits/s (SD 5.10)**. The reading analogue is a separate
literature and converges just as hard — Trauzettel-Klosinski & Dietz,
IReST, *IOVS* 53(9):5452 (2012): 436 subjects, 17 languages, matched
content, **1.42 ± 0.13 texts/min, 184 ± 29 wpm**, and **Chinese was the
fastest language in the set**. Brysbaert 2019 (*JML* 109:104047; 190
studies, 18,573 participants): **238 wpm silent**, and his conclusion is
that reading rate matches maximum *listening* rate and needs no
reading-specific processing. Our docs and `paper/paper.md` cited 39
bits/s as the *reading* wall. Fixed; the convergence claim survives, the
number was the wrong one.

**2. "Parallel vision does the binding" inverts what vision does.**
Binding is the one thing vision does *serially*. Treisman & Gelade:
single features are preattentive and parallel; **conjunctions require
focal attention and are searched serially**. Franconeri et al. (2012)
push this into relational judgment specifically — the visual system
delivers "a serial stream of information about the relations between
objects in a scene, **one relation at a time**." Blackwell (VL'96) made
the same point against visual programming: "decoding an image involves a
sequence of attention — but this is not often noted in VP literature."

**What survives.** Not parallelism. **Larkin & Simon's locality of
search** — diagrams "group together all information that is used
together, thus avoiding large amounts of search" and "use location to
group information about a single element, avoiding the need to match
symbolic labels." Their own caveat is the one nobody quotes: "*nothing
ensures that these inferences must be useful… diagrams are useful only
to those who know the appropriate computational processes for taking
advantage of them.*" So the defensible claim is **reduced search cost
and reduced working-memory load for reference re-access, for a reader who
has learned the conventions** — which is exactly what this lane
measured, and exactly what the Codex direction review independently
reduced it to.

## The decisive natural experiment: ASL

Sign languages already do "referent lanes": discourse referents are
assigned to spatial loci and re-accessed by pointing, gaze, and verb
agreement, so **the number of unambiguous referents grows as space and
memory permit** rather than colliding on a handful of pronouns
(Emmorey, *J. Psycholinguistic Research* 33(4)). That is precisely the
win this project wants, achieved in a real, fully expressive language.

Then the ceiling. Bellugi & Fischer, *Cognition* 1(2–3):173 (1972);
Klima & Bellugi 1979 p.194: ASL produces **~2 signs/second against
English's ~4–5 words/second, and the propositional rate is identical**.
All that spatial simultaneity buys exactly enough compression to offset
a 2× slower articulator. The control is decisive: **Signed English,
which drops the spatial grammar, runs at half ASL's propositional
rate.** So the spatial machinery is **load-bearing for parity, and
parity is the ceiling**.

## The number that should retarget the whole lane

Kuhn, "The Understandability of OWL Statements in Controlled English,"
*Semantic Web* 4(1):101 (2013). N=64, within-subject, counterbalanced,
with an ontograph method that defeats pattern-matching. Controlled
English vs Manchester OWL syntax: accuracy **91.4% vs 86.3%**, total
time **13.72 vs 18.42 min** — and **96% of the time difference came from
the LEARNING phase, only 4% from testing**.

**A better notation does not buy steady-state speed. It buys acquisition
speed.** For a language whose north star is learning speed that is the
right prize, and the wrong prize if the pitch is "reads faster." It
converges with the expertise-reversal effect, with Nesbit & Adesope's
concept-map benefit vanishing for high-verbal-ability readers
(**g = −0.327, ns**), and with Ottensooser et al. (*JSS* 85(3):596,
2012), the one controlled diagram-vs-text comprehension study here:
**text improved comprehension for trained AND untrained readers; the
diagram improved it only for the trained.**

## Hard design constraints, with numbers

- **Readable lane band: ~5–15 concurrent lanes.** ~15 is the metro-map
  comfort zone; ~50 per timestep is documented as broken; StoryFlow's
  authors state their methods "cannot provide legible results when the
  number of entities is in the thousands or even hundreds." Our S1 ran
  8–9 lanes — inside the band, but the fixed-width experiment (lane
  pitch 126px → 71px, 9 → 16 lanes per page) would push it to the edge.
- **~20 elements is where node-link loses to a table.** Ghoniem, Fekete
  & Castagliola (InfoVis 2004): "when graphs are bigger than twenty
  vertices, the matrix-based visualization outperforms node-link
  diagrams on most tasks. **Only path finding is consistently in favor
  of node-link.**" Replicated twice. This is independent confirmation of
  the direction review's "start from the table."
- **Hairball numbers:** minimum-crossing layouts, unlimited time, zoom
  and pan — 100 vertices: 63 s, 85% accuracy; **150 vertices: 184 s,
  39% accuracy**. A 150-word paragraph reads in ~38 s with high
  comprehension.
- **Graph literacy is not free:** Galesic & Garcia-Retamero (*Medical
  Decision Making* 31(3):444), nationally representative — **15–17% of
  US and German adults cannot read the height of a bar on a fully
  labelled, gridlined bar chart**; a third have low graph literacy and
  low numeracy.
- **Never judge a spatial layer by taste.** Roberts et al. found a
  curvilinear Metro map **30–50% faster** across three studies, yet ~50%
  still preferred octolinear *after experiencing the faster map*, and in
  a DLR commission the **most popular prototype produced the most
  errors**. Preference is uncorrelated with performance — which is a
  direct warning about our own shadow-pick protocol.

## The five ideas worth stealing

1. **Retarget to acquisition.** Design the layer as a first-N-hours
   register that a fluent reader graduates out of, and instrument
   time-to-competence, not words-per-minute (Kuhn's 96/4 split).
2. **Formalize the layout channel and use the operators with measured
   effects.** Spatial contiguity **g = 0.63–0.74** (k = 46–58) and
   signaling **g = 0.43** (k = 209) are the largest verified effects in
   the multimedia literature (Noetel et al., *RER* 92:413 — 29 reviews,
   1,189 studies, 78,177 participants). Arrows are the best-attested
   graphical function word (Heiser & Tversky, *Cognitive Science*
   30:581, validated in comprehension *and* spontaneous production).
   Cohn & Campbell (2015) quantify a pure geometry operator: a tall
   panel to the right of a column drops Z-path reading compliance from
   **95% to 31%**.
   And Petre's Catch-22 — the information that makes an expert diagram
   readable sits *outside* the notation — is a gap a **designed**
   language can close, which nobody in this literature could.
3. **Build for discourse relations specifically.** Jiang & Grabe
   (*RFL* 19(1):34) isolate the only well-supported moderator: graphic
   organizers isomorphic to the text's **discourse structure** work;
   generic idea hierarchies do not — Griffin et al. found GOs did not
   beat *a plain list of facts*. Our premise is on the right side of
   that line. Expect a **gist effect of ~0.3–0.5 SD**, and do not
   promise more (Nesbit & Adesope: central ideas g = .596, detail ideas
   g = .204; map vs text g = **.388**, not the widely-quoted 0.6).
4. **Three specific devices.** Bliss's **THING indicator** — an explicit
   abstract/concrete type marker costing one diacritic (`MIND` vs
   `MIND+THING` = brain). Cohn & Wittenberg's **action star** — a panel
   with zero representational content filling an obligatory structural
   slot, proving a spatial notation can have *function words*. And the
   highest-leverage result in the survey: **QA-SRL** (He, Lewis &
   Zettlemoyer, EMNLP 2015) replaces role *codes* with natural-language
   *wh-questions*, getting non-experts to **P .81 / R .86 after under 2
   hours**, against UCCA's 30–40 hours — because the question *is* the
   label and there is nothing to memorize. If lane position or role mark
   can be made **self-describing** rather than coded, that is the single
   biggest learnability lever available to us.
5. **Keep the text authoritative and design the escape hatch now.**
   Graphologue's architecture (diagram generated from marked spans, every
   node traceable to a phrase) is the right dependency direction, and
   Petre observed experienced readers *using the text to guide their
   reading of the graphics*. Then the Peirce lesson: the same man wrote
   the algebra that became universal and the graph notation nobody
   adopted, for the same logic, with provably simpler rules (7 steps vs
   43 for the Praeclarum Theorema). **Being better at the operations was
   not enough.**

## The three strongest reasons to expect failure

1. **Petre 1995 (*CACM* 38(6):33), with expert-vetted layouts:**
   "graphics was slower than text in all conditions… **the mean time for
   graphics conditions was greater than the mean time for text for every
   single subject**." Moher et al.'s replication found "no instances in
   which graphical representations out-performed their textual
   counterparts." Her structural diagnosis applies to us directly:
   "**Unlike text, which is always amenable to a straight, serial
   reading, graphics requires the reader to identify an appropriate
   inspection strategy. There are few cues to navigation.**"
2. **Stenning & Oberlander (*Cognitive Science* 19(1):97): the
   processing benefit IS the expressive loss.** "Graphical
   representations limit abstraction and thereby aid processibility." A
   *sentence* layer must carry negation, disjunction, quantification,
   modality and scope — exactly the expressiveness the theory says
   destroys the benefit. The formal version is Helly's theorem: an Euler
   diagram **forces** relations that are not logically entailed, and
   Shimojima's eye-tracking finds readers exploit the spatial constraint
   **even when it hurts them — they cannot turn it off**. Whatever we
   make the plane mean, the plane's geometry will assert things we did
   not intend.
3. **The throughput ceiling is central, and ASL already hit it** (above).
   Add the 3,300-year A/B test on non-phonographic writing: ~58% of
   frequent Chinese characters are phono-semantic compounds, **~5% are
   pure semantographs**, and every independently invented logography
   converged on a phonetic escape hatch via the rebus principle
   (DeFrancis, *Visible Speech* 1989).

## Closest existing prior art: read this before designing anything

**UNLWS — the Unker Non-Linear Writing System** (Sai & Alex Fink,
`s.ai/nlws`, design essay `s.ai/essays/nlf2dws`). Essentially this
project, built by serious conlangers: glyphs are predicates whose
**attachment points are symbolically related to their argument roles**;
texts are assembled by joining glyphs so shared attachment points mean
shared referents; **no inherent reading order**; connection types for
copular relations, causation, evidentiality, and remote coreference.

Sai's own list of difficulties is a free list of our open problems:
sequential events force linear connections *inside* a non-linear system
("most of our experiences happen within time"); it does not fit a book,
and "chopped up into 8.5×11 chunks" damages comprehension; insertion and
deletion are hard; layout must be planned ahead; "difficult for people
who think linearly / verbally." His comprehension claims are cautious
and unevidenced. **The design space has been walked.**

Heptapod B, for the record, is a ~100-logogram prop dictionary (71 used
on screen) with no grammar. Inspiration, not prior art.

## What does not exist, and would be novel data

Two claims were searched for specifically and not found anywhere:

1. **Any study showing a storyline/narrative chart is read faster than
   the corresponding text.** Two 2025/2026 sources state affirmatively
   that no readability evaluation of storylines exists — and the field's
   three canonical criteria (crossings, wiggle, whitespace) were
   reverse-engineered from a webcomic (xkcd #657) and, per the EuroVis
   2026 STAR over 53 papers, "**this has not been empirically
   evaluated**."
2. **Any study matching propositional content across a spatial/comic
   rendering and prose and measuring time.** The closest
   (Rasamimanana et al., *Cognitive Science* 49(7):e70081, N=40) shows
   comics at 156.9 s vs text at 340.4 s — but the comic carried only
   33–37% of the source word count, comprehension was ~43% in *both*
   formats, and **per-fixation processing was 25% slower in comics**. A
   navigation win, not a comprehension-rate win.

**That second study is the one this project actually needs, and it does
not exist.** Our `study` train/test harness is most of the apparatus for
it.

## One encouraging result

Pagkratidou, Galati & Avraamides (*Discourse Processes*, 2026): using
the location effect, participants tracked a protagonist's spatial shifts
**without instruction** in comics, but only *under* instruction with
text. That is evidence a spatial encoding can make one class of content
**automatic** rather than merely faster — the shape of win worth chasing.
