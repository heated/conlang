# Design Brief — engineered conlang (working title: TBD)

Distilled from the 2026-08-08 design conversation (full transcript:
`docs/archive/2026-08-08-design-chat.md`). This is the project's north star.
The name is deliberately undecided; the spec uses a placeholder until the
phonaesthetics pass (Tier 4).

## Goal

A language that is **maximally fast to learn**, where fast **typing**
(chording) and fast-to-acquire **reading** (featural script) fall out of the
architecture for free. Explicit non-goals: raw speaking/reading throughput
(pinned by cognition at ~39 bits/s regardless of code), speech density (the
"wide phonology" branch is dead), full FEC in casual speech.

## Core architecture

A syllable is a **channel vector**: onset × vowel × coda × register. Everything
else is defined over these coordinates.

1. **Channel phonology, baseline size.** ~10 content onsets
   (`p t k m n s l w j h` territory; `h` reserved for particles), 5 vowels
   (`a e i o u`), ~4–5 codas (`∅ n s l` core), 2 registers. Every phoneme sits
   inside essentially every L1's comfort zone — nobody is asked to hear a
   distinction their native language didn't give them.
2. **Decoupled featural script.** Written unit = morpheme = one block glyph =
   one chord; glyph components ARE the syllables of its pronunciation
   (Hangul-style blocks, zero exceptions). Deterministic two-way spell-out
   between glyph and the small spoken syllable inventory. Speech is the
   verbose serialization; text the compressed one.
3. **Error correction as structured redundancy, not uniform spacing**
   (v0.2 shape, post conlang-bf2): casual speech is protected by the
   HUMILITY ASSIGNMENT (no unrelated minimal pairs on high-confusion
   substitutions), word templates, phonotactics, context, and repair;
   the confusion-weighted check bit lives in the WRITTEN LAYER (glyph
   zone / romanization doubling), always machine-checkable, optionally
   realized as vowel length in careful/safety registers only. Mode
   frames carry their own grammar + mod-101 checksum.
4. **Self-segregating morphology, prosodic implementation.** Particles =
   single syllable with reserved onset `h`; content words 1–3 syllables,
   first-syllable stress as the boundary signal; exactly one legal parse of
   any syllable stream. Prefer stress-plus-boundary-marker over Lojban-style
   cluster requirements (loanwords pass through spell mode untouched).

## Tiered roadmap (from the conversation's priority ranking)

- **Tier 1 (frozen core, spec first):** channel inventory; featural
  block script + deterministic spell-out; humility assignment + the
  derived written-layer check bit (v0.2); SSM. Freeze early, version
  the spec, own the spec.
- **Tier 2:** mode particles (numbers/dates/times/coords/spell-out on
  reserved `h-` onset); Esperanto-style systematic derivation + correlative
  grids for all closed paradigms; part-of-speech on a dedicated channel
  (decide early — constrains word shapes); Zipf assignment of monosyllables.
- **Tier 3:** cross-syllable outer code + register profiles (casual /
  careful / safety-critical); chorded keyboard **and phone/touch input**;
  semantic-classifier zone (written-only); evidentials, attitudinals, spoken
  punctuation.
- **Tier 4 / spin-offs:** phonaesthetics pass + true name; degraded modes
  (whistled/drummed), shorthand projection, accessibility serializations;
  spatial sentence layer (**designated sequel project**, not this one).

## Key numbers & findings to respect

- Settled (v0.2): 220 spoken segmental syllables (200 content), 440
  written-layer codepoints; 22 monosyllabic root bodies under humility
  assignment (15 assignable after reserve), ~8.5k disyllabic bodies —
  disyllable-dominant, Japanese-like profile. (The chat-era 400–900 /
  200–600 estimates are historical.)
- Content vocabulary ~1,500–3,000 closed-core roots + productive derivation;
  content words average ~1.6–1.8 syllables spoken; monosyllables assigned by
  corpus frequency (Zipf policy) from the first dictionary draft.
- Numbers: digit-pairs, base-100 positional; tens→onset, units→rime; 0–99 in
  one syllable. Dates: month/day gridded onto channels. Time: hour ×
  quarter-hour = 96 values targeted at ONE syllable (user directive);
  minutes mode only for exact times.
- Mode payloads carry anti-check polarity **in the written layer**
  (self-flagging for text and machines); casual spoken payload integrity
  = boundary particles + frame grammar + mod-101 checksum (mandatory in
  safety registers).
- Modes win for payloads of 2+ syllables; casual speech uses lexical number
  words for small numbers.

## Design lessons imported (steal list)

- Esperanto: correlative grid mechanism for ALL closed paradigms; POS on a
  dedicated channel; systematic derivation; governance failure = unregulated
  borrowing (so: closed core, owned spec, versioned releases).
- Lojban: spoken punctuation/terminators as particles; machine-parseability
  worked, semantic-logic half didn't; phonotactics botched confusability.
- Toaq: syntax-on-a-channel is validated — but put it in the glyph layer /
  particle class / one register bit, NOT tone (tone = worst-perceived
  channel; syntax = worst cargo for it). Versioned releases + single design
  authority + community dictionary process.
- Hangul: featural glyphs learnable in days. Chinese radicals: semantic
  classifier zone, but at 100% reliability (written-only channel). Zipf:
  design the erosion in from day one. Talking drums / Silbo: degraded modes
  via conventional redundancy. ASL: spatial reference tracking (bridge to
  sequel). Solresol: multimodal serialization ambition, but never below the
  articulatory floor (~20–25 usable syllables absolute minimum).
- Sociology: adoption gradients beat cliffs — ship number/date/time modes and
  input methods as standalone tools usable inside English. A language ships
  better inside a world (stories, beauty budget at Tier 4). Ithkuil died of
  completeness: pick the load-bearing set, resist feature accretion.

## User directives on record

- 2026-08-08: try complement-restricted mode payloads; single-syllable
  hour+quarter time; name decision deferred ("don't care about the name rn");
  **consider phone text input** as a first-class input method.
- 2026-08-08 (later): complement-payload directive is a soft preference,
  "not hard at all" — modes bead weighs it freely. **Do not sacrifice
  learnability for monosyllable dates.** **Keep room to switch to the wider
  codepoints model later, or to push the inventory a little** — the core
  freezes as an expansion-compatible family (SPEC §9); script and input
  layers carry explicit headroom obligations.
- 2026-08-08 (later still): **reserve codespace for new words and language
  drift** (SPEC §8 headroom policy: ≥30% of monosyllable slots per class
  unassigned at every release). **Occasional Fable review for
  language-design substance**, alongside the Codex code-review policy.
- 2026-08-09: conlang-bf2 decisions — **humility assignment adopted**;
  **register tentatively demoted to the written layer**; alternative
  track reframed as a **zonal auxlang program** (pick the zone with the
  best bootstrap/adoption mechanics; start with a Romance zonal lang).
- 2026-08-09 (later): zonal program shape — **a replicable per-zone
  method, not a generator** ("we just generate for the next zone if it
  works"; don't build or manage that automation); **tentatively use the
  wide chorded script for the zonal lang** (flagged: tension with the
  receptive-first bootstrap — proposed resolution is Latin primary +
  chorded script as input/optional dense layer); add a **Sanskritic
  Interlingua** (Indo-Aryan zone) as a lower-priority second zone.
- 2026-08-08 (later still): **standing permission to explore alternative
  paths to the whole endeavor** while building — alternatives at any
  level (architecture, error correction, script, or a different framing
  of the project) may be investigated and proposed, not just the settled
  design. Tracked as a standing bead; findings land in the paper's
  alternatives/discussion sections and as design proposals.
- 2026-08-09 (script steering, post-review): script directions, all
  **tentative** — (1) **anti-iconic assignment**: ear-confusable
  phonemes get maximally distinct marks (eye = independent redundancy);
  letterforms optimized for degradation, not articulatory storytelling.
  (2) **~50k codepoints per character** via fused disyllabic blocks
  (~7 components, at the crowding ceiling); maybe special characters
  for numbers. (3) **Four-projections architecture**: every morpheme is
  a channel vector; block glyph = 2D projection; romanization = linear
  projection (check as doubling); chords = motor projection (mirrored
  hands, one syllable each, one stroke per morpheme); skeleton input =
  lossy projection (channel-subset briefs, onsets-first, IME-resolved —
  no per-word memorization). Commitments: visible POS zone, mode
  payloads visually flagged. Priced ceilings: density buys compactness
  and skimming, never WPM; ~1–3k chord inventory saturates composition
  at ~39 bits/s, so the chording layer is optimal. Deliverables (font
  pipeline, IME, chord engine) run **alongside and lower priority than
  straightening out the script itself**.
- 2026-08-09 (capacity steering): explore a **cross-POS humility
  exemption** — POS-inconsistent coda mishearings are rejected by the
  parse (syntax as an outer code); if simulation confirms reliable
  catch rates, unrelated words differing only in a high-confusion coda
  may be exempted. **Maintain a bottleneck ledger** for the codepoint
  count; price each relaxation rung (syntax exemption, context
  partitioning, …) against the silent-mishearing metric; validate the
  claimed 80–120 monosyllabic-root range reachable without touching
  the phonology.

## Decisions log (previously open questions)

- Inventory: 10+1 onsets (c added for digit-0), a e i o u, ∅/n/s/l —
  settled in SPEC v0.1; digits/dates reuse one digit-pair code.
- POS channel: final coda (∅ noun / n verb / s modifier) — settled.
- Assignment policy: humility (conlang-bf2, 2026-08-09) — settled.
- Check/register: demoted to written layer with optional careful-speech
  realization — **tentative**; re-promotion or deletion are documented
  minor-version paths (SPEC §9). The one genuinely open core question.
- Payloads: written-layer anti-check marking + frame grammar — settled.
