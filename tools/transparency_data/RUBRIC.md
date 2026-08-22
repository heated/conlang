# RZ cognate-relation annotation rubric

**Scope correction (Edward, 2026-08-22), binding on interpretation:**
annotators know all the judged languages, so these classes must be
read as ANNOTATOR-STATED LEXICAL RELATIONS between language pairs
(cognate availability — auditable via anchors), NOT as simulated
monolingual reader experience. Recognition rates per class are a
reader fact, estimated only by the cloze. The original task text
below predates the correction; its "would a reader recognize"
phrasing is interpreted per this note.

RZ is a constructed pan-Romance auxiliary language. Its words are elected
from across the Romance zone (Spanish, Portuguese, Italian, French) with an
English-Latinate tiebreak. We are measuring, per reader language, how much
of RZ's corpus vocabulary is recognizable AT SIGHT to an ordinary literate
reader of that language, with no study.

Input: every lemma in the RZ corpus (tools/coverage.py lemmatization)
with its token frequency. Closed-class
= function words; open-class = content words. Verb lemmas are cited in the
present form (stem + class vowel: `parla`, `prende`, `veni` = speak, take,
come). Hyphenated numerals like `dece-sete` are compound numbers (17).

## Judgment rubric (apply mechanically, judge the WRITTEN form for READING)

For each lemma, assign exactly one class for your assigned language(s):

- **T** (transparent): an everyday word of the judged language is a cognate
  whose written form is close enough that an ordinary reader gets the
  intended meaning at sight in running text. Small/systematic spelling
  differences do not block T (ES agua ~ `aqua`; IT treno ~ `tren`).
- **P** (partial): a real hook exists but it is obscured — the cognate is
  register-restricted (learned, technical, archaic: an ES reader reaching
  `cane` (dog) only via *canino*; an EN reader reaching `celo` (sky) via
  *celestial*), or the form has shifted enough that context must do real
  work. An educated-reader hook, not an everyman hook.
- **O** (opaque): no usable hook for an ordinary literate reader; the word
  must simply be learned.
- **F** (false friend): the nearest form in the judged language means
  something DIFFERENT and would actively mislead an ordinary reader about
  the intended meaning (e.g., IT *officina* means workshop, so RZ
  `oficina` = office is F for Italian). F outranks P/O — if a misleading
  hook exists, mark F even if a correct learned hook also exists.

Rules of thumb:
- Judge for an ordinary literate adult reader of the STANDARD language, not
  a linguist. When genuinely torn between two classes, pick the LOWER
  (T > P > O; F whenever misleading).
- Meaning drift counts: if the cognate exists but its everyday meaning in
  your language differs enough to mislead in typical sentences, that is F;
  if the meaning is adjacent enough that context rescues it, T or P per the
  strength of the hook.
- Proper judgments need the intended RZ meaning. Most are obvious pan-
  Romance words; the list includes glosses only through your own knowledge
  of Romance vocabulary — if a lemma's intended meaning is ambiguous to
  you, note that in the evidence field and judge the most plausible reading.
- English judgments: remember English readers hook through the Latinate/
  French stratum (via ~60% Latinate vocabulary), so `veritate` → *verity/
  veritable* is P, `aqua` → *aquatic/aquarium* is P (not T — the everyday
  word is *water*), `tren` → *train* is T.

## Output

Judgments live beside this file as {es,pt,it,fr,en}.json —
{lemma: [class, anchor]} where the anchor is the actual word of the
judged language carrying the hook (or, for O/F, a short note; for F
the misleading word and its real meaning). Aggregation:
tools/transparency.py. These judgments were produced single-pass by
AI annotators (2026-08-22) under this rubric; they are [A] evidence
— auditable annotator calls, not measured reader behavior.
