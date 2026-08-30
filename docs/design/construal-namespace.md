# Construal namespace — a project registry of markable distinctions

**Status:** instrument, v0 (2026-08-30). Adoption across the ledger
and toolkit = bead conlang-ma1; the one priced proposal it has
produced = bead conlang-czq. Origin: the Ithkuil steal-pass
(`alternatives/ithkuil-forks.md`) — Edward's framing: "Ithkuil as
taxonomy or namespace might be useful as a reference, sort of like
IPA."

> **Provenance rule.** Every `CN:` identifier is **project-owned**.
> Nothing here is an official Leipzig, UniMorph, or Ithkuil
> identifier; a row's `src` column records where a *concept* was
> imported from and how our dimension relates to that source — never
> that the source endorses our code. Every inventory carries a
> verification marker (key at the end of §4): **[V 2026-08-30]** was
> read off the primary source on that date, **[S16]** lives in a
> paper the current site defers to and is *not* pinned, and
> TODO-verify means nobody has checked it. Ithkuil's codes drift
> between published versions (`VER`/`VRF`, `PCT`/`PUN`) and its
> inventories change size in both directions across the revision, so
> an unversioned import is unsafe by default — three successive
> drafts of this file gave three different counts for Bias before
> anyone opened the table.

## 1. What it is, and the limits of the IPA analogy

IPA names *sounds* independently of any orthography, so two languages
can be compared on what they contrast rather than how they spell it.
This registry tries to do the same for *grammatical and construal
distinctions*: a ledger row, toolkit entry, grammar table, or gloss
can name **what** a feature marks with a stable identifier,
separately from *how* it is realised (affix, particle, tone, word
order, glyph zone, silence).

The analogy is loose in one important way. IPA is a standards body's
inventory with an authority behind it; this is one project's working
registry, assembled from three sources that do not agree and were
built for different purposes. It is useful as shared vocabulary
inside this repo. It is not a standard, and should never be
presented as one.

Uses here:

- **Ledger rows** (`learning-budget.md`): "what it buys" becomes
  checkable — `CN:POS` names a claim; "adds part-of-speech marking"
  does not say where.
- **Toolkit entries** (program lane E): zone-agnostic by
  construction — "an optional clause-particle set marking `CN:EVID`"
  is portable; "*dizque*" is not.
- **Cross-conlang comparison**: Esperanto's `-o/-a/-i` and GZ's final
  coda both mark `CN:POS`; Toaq's tone marks `CN:CASE`-adjacent
  argument roles; Lojban's `UI` marks `CN:BIAS`.
- **Glosses** stay Leipzig. The registry is the ontology consulted
  when Leipzig has no abbreviation for what is being marked.

A tag says what is marked — never how, and never that marking it is
a good idea. Pricing lives in the ledger.

## 2. Sources, and what each can and cannot settle

| source | what it actually standardises | why it cannot be the registry |
|---|---|---|
| **Leipzig Glossing Rules** (Comrie, Haspelmath & Bickel; 2008, rev. 2015) | a convention for interlinear glossing plus an appendix of ~80 gloss abbreviations | a glossing convention, not a dimensional ontology; it names values, not dimensions, and is silent on construal categories |
| **UniMorph schema** (Sylak-Glassman 2016; living site) | a cross-linguistic inventory of morphological feature *values* organised into dimensions | morphology only — a language marking a dimension periphrastically has no UniMorph feature; value counts differ between the 2016 paper and the current site |
| **Ithkuil** (Quijada 2011; New Ithkuil, living web grammar) | the most complete single catalogue of *construal* categories: set shape, boundary, evidence, stance, goal-attainment | one designer's analysis; several dimensions overlap; some are attested nowhere else; codes drift across versions |
| this project | written-only channels (check bit, payload role, mode frames), spatial-layer devices | project-specific by definition |

**Precedence rule.** Where a source has an established *value* code,
reuse it verbatim and record the source and the mapping relation.
Dimension identifiers are ours in all cases. Coin a value code only
for project-specific channels, and mark it ‡.

## 3. Identifier scheme

```
CN:<DIM>              a dimension (always project-owned)   CN:EVID
CN:<DIM>.<VAL>        a value                              CN:EVID.RPRT
CN:<DIM>.{A,B}        a value subset                       CN:EVID.{HRSY,INFER}
```

`src` names the system a value inventory was imported from; `rel`
records how our dimension maps onto that source's:

- `exact` — same extension as the source dimension
- `broader` / `narrower` — ours subsumes / is subsumed by it
- `overlap` — partial, documented per row
- `local` ‡ — project-specific, no source dimension

Dimension codes ≤ 5 letters, value codes 3–5 letters, uppercase.
A tag never carries a realisation; realisation is documented beside
it ("`CN:POS` — realised as the word-final coda, SPEC §6").

## 4. The registry

`here` states where the dimension is marked in our languages **today**,
verified against the checked-in specs and grammars. "—" means not
marked; proposals are labelled as such and are not evidence of a
facility.

### A. Nominal construal

| dim | name | values | src / rel | here |
|---|---|---|---|---|
| `NUM` | number | UniMorph: SG DU TRI PL GRPL GPAUC INVN PAUC (8) [S16 — not on the current site, which defers per-dimension values to Sylak-Glassman 2016] | UniMorph / exact | RZ `-s`/`-es`; GZ none — plurality by quantifier (gf-grammar §1) |
| `CFG` | configuration — shape of the set | New Ithkuil: UPX DPX MSS DSS MSC DSC MSF DSF MDS DDS MDC DDC MDF DDF MFS DFS MFC DFC MFF DFF (**20**) [V 2026-08-30]. **2011 had 9** — the revision grew this one | Ithkuil / local | — (pilot candidate, GZ) |
| `AFL` | affiliation — how members relate | CSL ASO COA VAR (4) [V 2026-08-30] | Ithkuil / local | — |
| `PRS` | perspective | M G N A (4) [V 2026-08-30] | Ithkuil / local | — |
| `EXT` | extension — which portion of the entity | DEL PRX ICP ATV GRA DPL (6) [V 2026-08-30] | Ithkuil / local | — |
| `ESS` | essence — real vs represented | NRM RPV (2) [V 2026-08-30] | Ithkuil / local | — (**no RZ or GZ equivalent**; RZ's `si`-conditional is irrealis, a different object) |
| `DEF` | definiteness | UniMorph dimension [V 2026-08-30 — dimension list]; values [S16] | UniMorph / exact | RZ `le/les/un`; GZ none, by design (gf-grammar §6: definiteness left to context) |
| `GEND` | gender / noun class | UniMorph: MASC FEM NEUT + class features [S16] | UniMorph / exact | RZ none — deleted; natural gender in animate pairs only (rz-grammar §2). GZ none |
| `ANIM` | animacy | UniMorph dimension [V 2026-08-30]; values [S16] | UniMorph / exact | — |
| `POSS` | possession | possessor person/number features [S16] | UniMorph / exact | RZ invariant possessives (§2) |
| `CASE` | semantic/syntactic role | UniMorph: **39 features — the schema's largest dimension** [V 2026-08-30]. Ithkuil: 96 (2011) → **68** (New Ithkuil), a much finer and differently-cut object | UniMorph + Ithkuil / overlap | RZ prepositions, no case; GZ adposition particles `hal/hees/his/hol` + word order (gf-grammar §3–4) |

### B. Lexical / derivational

| dim | name | values | src / rel | here |
|---|---|---|---|---|
| `POS` | part of speech | UniMorph dimension [V 2026-08-30]; values [S16] | UniMorph / exact | GZ final coda ∅/n/s (SPEC §6); RZ partial — R-scheme script-only marking is adopt-pending-evidence, not shipped |
| `STEM` | stem within a root | New Ithkuil: Stems 0–3 (**4**), carried in slot IV's Vr [V 2026-08-30] | Ithkuil / local | — |
| `SPEC` | specification — which facet of the root | BSC CTE CSV OBJ (**4**), carried in slot IV's Vr alongside Function and Context [V 2026-08-30] | Ithkuil / local | — (**proposed**, GZ; bead conlang-czq) |
| `FUNC` | function | STA DYN (2), slot IV | Ithkuil / local | GZ's O/A/P/R alternation classes cover part of this (gf-grammar §2) |
| `CTX` | context | 2011: 4 Contexts [V 2026-08-30]; New Ithkuil carries Context in slot IV | Ithkuil / local | — |
| `VER` | version — process vs goal-attainment (`VRF` in some published material) | PRC CPT (2) | Ithkuil / local | — (RZ and English lexicalise it: *look for* / *find*) |
| `DSGN` | designation | 2011 only: 2 values [V 2026-08-30]. **Dropped in New Ithkuil** — recorded because a category disappearing is itself data about the pruning question | Ithkuil (2011) / local | — |
| `DERIV` ‡ | derivational family | project-listed affixes | project / local | RZ §9 (`-cion -itate -mente -al -or …`); GZ none yet |

### C. Event structure

| dim | name | values | src / rel | here |
|---|---|---|---|---|
| `TNS` | tense | UniMorph dimension [V 2026-08-30]; values [S16] | UniMorph / exact | RZ `-va` past, `va` + inf future; GZ `hoon` preverbal past, unmarked = nonpast (gf-grammar §3) |
| `ASP` | aspect | UniMorph dimension [V 2026-08-30]; Ithkuil: **36** (32 in 2011 — this one also grew) [V 2026-08-30] | UniMorph + Ithkuil / overlap | RZ `sta` + gerund, `tener` + participle |
| `AKT` | Aktionsart | UniMorph dimension, distinct from aspect [V 2026-08-30]; values [S16] | UniMorph / exact | — (no RZ or GZ marking) |
| `PHS` | phase | PCT ITR REP ITM RCT FRE FRG VAC FLC (**9**) [V 2026-08-30]. Punctual is `PCT`; older material uses `PUN` | Ithkuil / local | — |
| `VOICE` | voice | UniMorph: ACT PASS MID ANTIP etc. [S16] | UniMorph / narrower | RZ `es` + participle; `se` reflexive |
| `VLNC` | valency | **A UniMorph dimension in its own right, separate from voice** [V 2026-08-30] — CAUS/APPL/RECP/REFL live here, not under `VOICE` | UniMorph / exact | RZ `se`; GZ none |
| `VALN` | valence — relation between co-participants (Ithkuil's category, unrelated to UniMorph valency) | MNO PRL CRO RCP CPL DUP DEM CNG PTI (**9**) [V 2026-08-30] | Ithkuil / local | — |
| `LVL` | level — comparison as a grammatical category | MIN SBE IFR DFT EQU SUR SPL SPQ MAX (**9**) [V 2026-08-30]. UniMorph has a separate `comparison` dimension | Ithkuil / local | RZ periphrastic `plus/minus … que` (§7); GZ `mu-s` + `hees` |
| `EFF` | effect — beneficial/detrimental, and to whom | 1:BEN 2:BEN 3:BEN **SLF:BEN** UNK **SLF:DET** 3:DET 2:DET 1:DET (**9**) [V 2026-08-30] | Ithkuil / local | — |
| `POL` | polarity | UniMorph dimension [V 2026-08-30]: POS NEG | UniMorph / exact | RZ preverbal `no` + negative concord (D1) — **the `no`~`lo` hazard is bead conlang-1op**; GZ `haan`, deliberately long and nasal for robustness (gf-grammar §3) |

### D. Speaker stance (clause-level)

| dim | name | values | src / rel | here |
|---|---|---|---|---|
| `ILL` | illocution | Ithkuil's set — **count not verified**; the adjuncts and verb chapters fetched on 2026-08-30 did not enumerate it [TODO-verify] | Ithkuil / local | GZ partial: `hus` clause-final polar question, bare-verb imperative — **no general illocution channel**. RZ: intonation/`?`, imperative |
| `MOOD` | mood / modality | UniMorph dimension [V 2026-08-30]; Ithkuil: FAC SUB ASM SPC COU HYP (**6**) [V 2026-08-30] | UniMorph + Ithkuil / overlap | RZ `-ria` conditional, `si` + indicative; no subjunctive (absorbed). GZ `huul` preverbal irrealis/future |
| `EVID` | evidentiality / validation | UniMorph dimension [V 2026-08-30]; values [S16]. Ithkuil's Validation is a parallel set — **count not verified** [TODO-verify] | UniMorph + Ithkuil / overlap | — (candidate for GZ's careful/safety register) |
| `EXPT` | expectation — stance toward outcome | COG RSP EXE (3) | Ithkuil / local | — |
| `BIAS` | affective / attitudinal stance | **66** entries, ACC…VEX, carried by Bias adjuncts [V 2026-08-30]. (Earlier drafts said ~57 and 61; both wrong — this is why rows get read off the source) | Ithkuil / local | — (declined for design; precedent only) |
| `REG` | discourse register — parenthetical, exemplary, quoted thought | Ithkuil's set [TODO-verify] | Ithkuil / local | — |
| `HON` | politeness / honorification | UniMorph dimension [V 2026-08-30]; values [S16] | UniMorph / exact | **RZ none** — `tu`/`vos` is a number distinction, not T/V. **GZ none, permanently** (gf-grammar §6 rules honorifics out) |
| `INTQ` | interrogativity | UniMorph dimension [V 2026-08-30] | UniMorph / exact | RZ fronting, no inversion (§6); GZ clause-final `hus` |
| `FIN` | finiteness | UniMorph dimension, **2 features — the schema's smallest** [V 2026-08-30] | UniMorph / exact | RZ infinitive vs finite; GZ none (no agreement to be finite about) |

### E. Reference and discourse

| dim | name | values | src / rel | here |
|---|---|---|---|---|
| `PERS` | person, with clusivity | UniMorph dimension [V 2026-08-30]; values [S16] | UniMorph / exact | RZ pronouns (§3); GZ pronouns as content words (SPEC §5.2) |
| `SWREF` | switch reference | **A UniMorph dimension** [V 2026-08-30] — the earlier draft wrongly filed this as non-standard | UniMorph / exact | — (bead conlang-ax3) |
| `DEIX` | deictic distance | **A UniMorph dimension** [V 2026-08-30]; values [S16] | UniMorph / exact | RZ two-way: `iste` / `aquel` (§2) |
| `INFO` | information structure | **A UniMorph dimension** [V 2026-08-30]; values [S16] | UniMorph / exact | **neither language marks it today**: GZ has no topic particle (its 11 particles are listed in gf-grammar §3) and defers discourse particles to future work |
| `OBV` | proximate / obviative | typological literature; **not a UniMorph dimension of its own** (obviation surfaces under person/argument marking) | literature / local | — (bead conlang-ax3) |
| `COREF` ‡ | coreference device | pronoun; miniature/"hashing" (UNLWS); lane | project / local | spatial layer (bead conlang-v9m) |

### F. Written-only and meta channels

| dim | name | values | src / rel | here |
|---|---|---|---|---|
| `CHK` ‡ | integrity check | computed check bit; mod-101 checksum | project / local | GZ written layer (SPEC §4.1); modes §8 |
| `PAYLD` ‡ | payload vs lexical role | LEX PAY | project / local | modes anti-check marking (SPEC §4.2) |
| `MODE` ‡ | closed-domain frame | NUM DATE TIME SPELL PHON COORD | project / local | `docs/spec/modes.md`; RZ number mode |
| `USEM` ‡ | use vs mention (form-quote vs meaning-quote) | FORM MEAN | UNLWS / local — **distinct from Leipzig's `QUOT`**, which glosses a reported-speech quotative | — (unlws-trailhead: to evaluate) |
| `SCOPE` ‡ | drawn scope for quantifiers and irrealis | cartouche | UNLWS / local | spatial layer (to evaluate) |
| `CLASS` ‡ | semantic classifier zone | open | project / local (Chinese radicals as precedent) | reserved script channel (SPEC §9) |

**Verification key.** `[V 2026-08-30]` = read directly off the cited
primary source on that date. `[S16]` = the value inventory lives in
Sylak-Glassman (2016); the current UniMorph site publishes the
**23 dimensions and "over 212 features"** totals but defers
per-dimension values to that paper, which reports a larger feature
count — so any `[S16]` row must be pinned to a release before its
numbers are quoted anywhere (bead conlang-ma1). No `[S16]` count is
reproduced above for exactly this reason, except `NUM`, which is
flagged as unpinned.

## 5. How to use it here

1. **Ledger rows**: add a `marks:` clause to "what it buys" —
   `marks: CN:POS (word-final coda)`. Retro-tagging is bead
   conlang-ma1.
2. **Toolkit entries** (lane E): name each entry by tag plus
   realisation class — "clause-particle set for `CN:EVID`", "coda
   channel for `CN:POS`", "frame for `CN:MODE.NUM`".
3. **Grammar tables**: a `CN:` column on GZ's particle table and RZ's
   verb and negation tables, so two grammars can be diffed on what
   they mark.
4. **Steal-passes**: tag a stolen mechanism before pricing it, so a
   ledger row never reads "adds an Ithkuil thing."
5. **Glosses** stay Leipzig; reach for a `CN:` tag only where Leipzig
   has no abbreviation for the distinction.

## 6. Limits, stated

- **This is a project registry, not a standard.** Bare codes look
  authoritative; they are not. The `src`/`rel` columns exist so that
  no row can be mistaken for an endorsement by Leipzig, UniMorph, or
  Quijada.
- **Unverified inventories are the main defect of v0.** Rows without
  [V 2026-08-30] were written from secondary knowledge. Regenerate
  every one from a pinned UniMorph release, the 2015 Leipzig
  appendix, and a dated New Ithkuil snapshot before any count reaches
  the paper (bead conlang-ma1).
- **Ithkuil's dimensions are one analysis.** Several overlap (`PHS`
  vs `ASP`, `LVL` vs comparison, `EXPT` vs `MOOD`) and some are
  attested nowhere else. Listing them records them; it does not
  claim they are universal, distinct, or well-founded.
- **UniMorph is morphology-only**, so a language marking a dimension
  periphrastically appears here with no UniMorph feature. That is
  fine: tagging is about what is marked, not by what means.
- **A catalogue is not a menu.** Listing a dimension is not a
  proposal to mark it. Proposals go through the ledger.
