# Atlantic Zonal v0 — the English-zone auxlang (workshop draft)

Status: workshop-stage. Sibling of `romance-zonal-v0.md` (RZ), not a
replacement — second instantiation of the per-zone recipe (RZ §8),
which makes it the recipe's first replication test. Working label
"AZ".

## 0. What is the zonal version *for English*?

Naive answer: pan-Germanic (the Folkspraak project family). Wrong for
this zone: English traded away its sight-readable Germanic vocabulary
centuries ago — an English reader cold-reads German/Dutch *worse* than
Spanish. What the English zone actually possesses is the **Latinate
stratum**: ~60% of English vocabulary, including nearly all of its
formal/written register, shared with the Romance zone. The English
zonal therefore isn't a Germanic mirror of RZ; it lives on the
Anglo-Romance written union — call it the **Atlantic** zone: EN-L1
(~400M) + EN-L2-literate (~1B+) + Romance readers (~900M) via gist.

Two honest products live here:

## 1. AZ-a: controlled Latinate English (recommended for the EN zone)

**English grammar and spelling fully intact; the lexicon constrained
to pan-Latinate word choices wherever a common one exists.** An
EN reader pays exactly zero — it *is* English, in a disciplined
register. A Romance reader gists it the way Edward gisted RZ, but
better, because English morphology is nearly bare (no conjugation
noise) and the Latinate spellings are the shared written forms.

- Rule 1 (lexicon): where English has a common Latinate/Germanic
  synonym pair, use the Latinate member: *commence/start → commence*?
  No — **frequency-bounded**: use the Latinate member when it is
  itself common (begin→start? both Germanic; use *initiate* only in
  formal register). Practical filter: prefer the word whose Romance
  cognate exists AND whose English frequency rank is high enough to
  feel natural. `demonstrate` over `show`, `respond` over `answer`,
  `require` over `need`, `attempt` over `try`, `assist` over `help`.
- Rule 2 (grammar): standard English, restricted: SVO only, no
  idioms, no phrasal verbs (*continue*, not *keep on*; *remove*, not
  *take off* — phrasal verbs are the #1 opacity for non-EN readers),
  no contractions, simple tenses preferred.
- Rule 3 (names/numbers/dates): ISO-ish unambiguous formats.
- Germanic bedrock without Latinate twins (sun, wind, water, house,
  day…) stays — the honest limit of the zone overlap; Romance readers
  bridge via frame, exactly as Edward bridged RZ's `quando/era`.

This is ASD-STE100's move (controlled register) pointed at
cross-zone readability instead of aviation safety. It is *buildable
as tooling*: a linter that flags non-Latinate choices and suggests
the twin, a dictionary of preferred forms, a style checker. Chorded
input for it is solved — it's English; steno exists.

**AZ-a fable (same content as RZ's, for A/B reading):**

> The north wind and the sun disputed over which of them was the
> more powerful, when a traveler passed, covered in a warm mantle.
> The two accorded that the first to cause the traveler to remove
> his mantle would be considered the more powerful. The north wind
> commenced to blow with total force, but the more it blew, the more
> the traveler covered himself with his mantle; and finally, the
> wind abandoned the attempt. Then the sun commenced to radiate
> warmly, and immediately the traveler removed his mantle. And so
> the north wind was obliged to concede that the sun was the more
> powerful of the two.

(Note what happened: *disputed, covered, accorded, considered,
commenced, force, abandoned, attempt, radiate, immediately, removed,
obliged, concede* — a Romance reader recovers the entire event
skeleton from cognates; the Germanic residue — wind, sun, warm, blow
— is frame-inferable. This is RZ's gist-channel, reversed.)

**AZ-a, remaining registers (same content as RZ §5, for A/B):**

> — Good day! How are you?
> — Very well, thank you. And you?
> — Also well. Do you desire to take a coffee with me?
> — Yes, with pleasure. I know an excellent location in proximity.
> — Perfect. Then we proceed.

> This language is a controlled register of English. If you read
> English, you read it already, with zero study. If you read Spanish,
> Portuguese, Italian, French or Romanian, you can comprehend the
> majority of this text without study: the vocabulary is selected to
> maximize the part of English that your language also possesses. We
> measure the comprehension with real tests, and we publicate the
> results. *(publicate → publish: the linter would flag this — the
> Latinate form must also be real English; "publish" is already
> Latinate. Left in as a worked example of the failure mode.)*

> The government announced today a new program of solar energy. The
> plan provides for the construction of three centrals in the south
> of the country during the proximate five years, with a total
> investment of two billion euros. According to the minister of
> energy, the program will create more than four thousand employments
> and will reduce carbon emissions by twenty percent. Environmental
> organizations received the announcement with prudent optimism, but
> demanded more transparency about the calendar of construction.

(The news register is nearly ordinary English — which is the point:
formal English *already is* Atlantic. The dialogue is where AZ-a
strains: "desire to take a coffee" is stilted English purchased for
Romance decode; the exact stiltedness budget is a design dial, and
the cloze numbers on both populations will price it.)

### 1.1 Learning model: how an English speaker learns to *produce* AZ-a

Not language learning — **style-guide learning**: the vocabulary is
already known; what's acquired is selection discipline (cost sits in
attention, not memory). Three routes, in deployment order:

1. **Linter-as-teacher** (primary): write English, get flagged
   (*find out → discover*; every phrasal verb). Spellcheck-style
   point-of-production feedback; the real-world controlled-language
   model (ASD-STE100 is used via checkers, not memorization). The
   long tail stays tool-assisted permanently, by design.
2. **Rules + top-100 twins**: the structural register teaches in ~1h;
   the hard skill is *noticing your own phrasal verbs and idioms* —
   they are cognitively invisible to natives (the known ESL-teacher
   training problem). Est. 5–20 h of assisted practice to ~90%
   unassisted compliance.
3. **Register immersion**: reading AZ-a tunes producing it;
   register-switching is a native skill everyone already has.

Failure modes, priced: (a) hypercorrection into non-English
Latinisms (*publicate*) — the subset-of-English constraint is
load-bearing and the linter flags both directions; (b) **speech
trails writing** — no linter in your mouth; real-time selection
discipline is effortful (the lived STE experience). AZ-a is a
written-first product.

Adoption asymmetry worth exploiting: the register already exists in
the wild — Romance-L1 writers of English produce near-AZ-a naturally
(Latinate reach, no phrasal verbs; "EU institutional English"), and
academic English is Latinate-heavy. AZ-a codifies and tools a
register millions of people half-speak.

Portfolio productive-cost comparison: AZ-a ≈ 1–3 h rules + 5–20 h
assisted practice; RZ ≈ 30–100 h; greenfield ≈ full acquisition from
zero (priced against its engineered ceiling).

## 2. AZ-b: the EN-weighted interlanguage (the bridge variant)

Rerun the RZ recipe with weights EN .45, FR .15, ES .15, IT .10,
PT .10, RO .05 and the same false-friend screen. The result converges
toward Interlingua-with-English-spelling-habits: `le governo
announced hodie...` — a genuinely new language that costs the EN
reader a small tax (~90% sight) and pays the Romance reader more than
AZ-a does. Strictly worse than AZ-a *for the EN zone* (nothing beats
zero cost), strictly better as a single shared Atlantic standard.
Park until AZ-a's Romance-reader numbers exist: if AZ-a already
scores 70%+ with Romance readers, AZ-b has no niche; if it scores
40%, AZ-b is the product.

## 3. Relationship to RZ and the greenfield

- RZ optimizes for Romance-L1 readers; AZ-a for EN readers (trivially)
  with Romance gist as the bonus; they share the Latinate stratum, so
  **the same cloze instrument can test both** on both populations —
  four numbers, one experiment family: RZ×Romance (its zone), RZ×EN
  (Edward's gist result, measured), AZ-a×EN (≈100% by construction),
  AZ-a×Romance (the open number that decides AZ-b's fate).
- The greenfield is untouched by all of this; the cognate tables
  built for RZ/AZ feed its mnemonic-hook heuristic (kps note).
- The recipe (RZ §8) held for a second zone with one amendment: step
  2's "sight-cognate orthography" generalizes to "the zone's existing
  orthography when the zone already shares one" — for the EN zone,
  respelling anything would only destroy recognition (the Kolers
  lesson yet again).

## 4. Next actions on this thread

1. Draft the AZ-a controlled-register spec: the ~200-entry preferred
   lexicon (Latinate twin table), the grammar restriction list, and
   the remaining three sample texts (dialogue, expository, news —
   news will be nearly unchanged from ordinary English, which is
   itself the point).
2. Add AZ-a items to the cloze program: test the fable above on
   Romance-L1 readers alongside RZ's — the comparison decides where
   the Atlantic effort goes.
3. Tooling seed (cheap, high-leverage): the Latinate-twin linter —
   a wordlist + suggestion table is a weekend artifact and doubles as
   the lexicon deliverable.
