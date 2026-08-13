# Beauty brief: aesthetics as a design goal (conlang-0eh)

Directive (Edward, 2026-08-13): balance beauty ("elvish, anyone?")
against the other goals — for the language and the script. This brief
turns that into actionable constraints. Style study render:
`.ship-notes/beauty-study.svg`.

## 1. Sound: the greenfield is structurally elvish-compatible

Tolkien's phonaesthetic playbook (what makes Sindarin sound the way
it does): sonorant-heavy running text (l r n m), open syllables,
pure vowels and light diphthongs, cluster avoidance, falling/trochaic
rhythm. Check against our inventory: **5 of 10 content onsets are
sonorants** (m n l w j), all syllables are (C)V(C) with open
syllables dominant, vowels are 5 pure qualities, stress is
word-initial (trochaic music built in), and the echo-vowel rule adds
a vowel-harmony flavor. Nothing structural blocks elvish-grade sound.

**The lever is lexicon assignment (kps), and it costs nothing:**
weight high-frequency words toward sonorant-heavy bodies (la, ma,
ne, li, wa…) so running speech skews liquid; push obstruent-heavy
bodies (ka, te, po…) toward low-frequency/technical vocabulary. This
joins the two existing assignment preferences — confusion spacing
(hard constraint) and Romance mnemonic hooks (soft) — as a third soft
preference. Where hooks and euphony conflict, score both and let the
Zipf band decide: hooks matter most in the learning core, euphony
matters most in the high-frequency running-text band; conveniently
these are the *same* band, so kps must weigh them explicitly
(suggest: euphony breaks ties among adequate hooks, hooks never
override the confusion constraints).

Also free: particles are h-initial and unstressed — the grammatical
scaffold is already the softest sound in the system, which reads as
elvish "flow" rather than Esperanto's clatter of -oj/-aj.

## 2. Script: findings from the style study

1. **Stroke-weight contrast (vertical bold / horizontal light) adds
   warmth at ~0.2–0.25** and is a pure font-level change (no spec
   touch). At 0.45 it destroys the doubled-stroke letters — n and
   m-class ink fuses. The constraint discovered: **contrast budget ≤
   (doubled-stroke gap − stroke width) at the letter's rendered
   scale**, so fused trisyllable letters (0.38 scale) can take almost
   none. Contrast must be scale-aware: full-size letters get the
   style, miniatures stay uniform.
2. **The trisyllable slots are the beauty-critical case** (also the
   legibility-critical one per the fusion study — the two goals point
   at the same target). Style pass priority: redraw the 0.38-scale
   letterforms with simplified ink (Hangul's move: jamo simplify in
   crowded blocks) rather than styling them.
3. Remaining candidates, all font-level: optical centering of the
   check dot (it floats), corner rounding on angle letters (soften
   the drafting-table look), ink-density equalization across
   characters (simple chars slightly bolder — the stroke floor
   already does the reverse direction).
4. Standing rule adopted: **beauty changes live in fonts and
   assignment preferences, never in the feature grammar** — the spec
   defines topology; style is a rendering of it. This keeps the
   beauty pass permanently cheap and reviewable-by-eye.

## 3. What beauty costs (the balance Edward asked for)

Almost nothing, placed correctly: the sound lever is an assignment
preference inside constraints that already bind; the script levers
are font-layer. The only real trade identified: euphony-weighting
the high-frequency band competes with mnemonic hooks for the same
bodies (resolution above), and stroke contrast competes with
doubled-letter legibility (resolution: scale-aware budget). Neither
touches capacity, error rates, or the frozen grammar.

## 4. Next actions

- kps: implement the three-preference scoring (constraints > hooks ~
  euphony with band weighting) when seed assignment starts.
- Script: trisyllable letterform simplification study; then a real
  font pass (contrast 0.22, rounded angle corners, optical dot) as a
  display font — freeze-gate exhibit alongside the layout decision.
