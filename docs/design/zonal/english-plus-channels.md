# Track E: English + channels (workshop sketch)

Bead conlang-0i7. Origin (Edward, 2026-08-14): AZ-a as a *learned*
register is cursed — a subtractive discipline (suppress your own
idioms, the hardest self-monitoring) whose benefit accrues to someone
else's comprehension. Incentive-mismatched disciplines don't
self-sustain (Basic English died; Plain Language needs mandates; STE
survives only under aviation regulation). Resolution: don't change
the language; layer the machinery on the host and put any discipline
in software.

## The stack (every rung free-standing, zero-commitment)

1. **Modes embedded in English** — the strongest rung, already
   designed and built (spec modes.md; encoders/decoders in
   tools/modes.py). The digit-pair / date / time / spell frames are
   self-delimiting (open/close particles), so they drop into English
   speech and text intact, with their density and optional mod-101
   checksum. This is the paper §7 adoption-wedge claim, taken
   literally: the codes function inside a host language without
   learning any lexicon. Deliverable: a one-page "modes in English"
   convention note + input snippets (type `hu 4207 haas`, get the
   syllables); a safety-register pitch (readbacks) comes free.
2. **Chorded input: adopt, don't build.** Plover steno is mature
   (200+ wpm, open source). Our marginal theory contribution for
   *English* is ~zero; the years-to-learn cost is real but is a
   solved ecosystem's problem, not ours. Track E just points at it —
   and gains the option to emit mode frames as chords later.
3. **AZ-a as an editor toggle** ("international mode"), not a
   register anyone learns: write normal English; the tool suggests
   Latinate twins and flags phrasal verbs/idioms inline; accept or
   ignore. The twin table (az-latinate-twins.md) is the suggestion
   dictionary. Learning happens incidentally or never — both fine.
   This absorbs AZ-a's product framing; the cross-test matrix
   (cloze-test-v0.md) still measures how much the toggle actually
   buys with Romance readers before we invest in the tool.
4. **Featural script for English: parked.** English respelling in
   any new script pays the Kolers cost for shorthand-class returns;
   Gregg/Pitman already occupy that niche. Revisit only if the
   greenfield's fused-glyph work (r5y) produces something so good it
   begs for a host.

## What this track is, strategically

The maximum-gradient adoption path: a user can take rung 1 alone
(dense unambiguous numbers/dates in their English), rung 3 alone
(write internationally readable English with zero study), or nothing.
No rung asks for identity change or study time — the opposite pole
from the greenfield, with RZ/AZ between. The portfolio now spans the
full commitment spectrum, which is itself the experiment: where on
the spectrum does real uptake happen?

## Non-goals

Track E does not modify English, does not compete with steno, does
not ship a script. It is conventions + tooling over an unchanged
host.

## Next actions

1. "Modes in English" convention note (one page, with worked
   examples: phone numbers, dates, times, spelling-out; casual vs
   checksummed register).
2. Toggle prototype scope: wordlist lookup + phrasal-verb detector
   over plain text (reuse az-latinate-twins.md), CLI or editor
   extension — after the cross-test matrix says the gist gain is
   worth it.
3. Fold Track E into the ow7 pricing table as the fourth column
   (greenfield / RZ / AZ / English+channels).
