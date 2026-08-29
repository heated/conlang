# Construal namespace — a project registry of markable distinctions

**Status:** instrument, v0 (2026-08-30). Adoption across the ledger
and toolkit = bead conlang-ma1; the one priced proposal it has
produced = bead conlang-czq. Origin: the Ithkuil steal-pass
(`alternatives/ithkuil-forks.md`) — Edward's framing: "Ithkuil as
taxonomy or namespace might be useful as a reference, sort of like
IPA."

> **Provenance rule, and the reason this document is v0.** Every
> `CN:` identifier is **project-owned**. Nothing here is an official
> Leipzig, UniMorph, or Ithkuil identifier, and a row's `src` column
> records where a *concept* was imported from and how our dimension
> relates to that source — never that the source endorses our code.
> Value inventories reproduced below were checked against the live
> sources during the 2026-08-30 review and are marked
> **[V 2026-08-30]**; unmarked inventories are unverified and must be
> regenerated from a pinned release before use (bead conlang-ma1).
> Ithkuil's own codes drift between published versions (`VER`/`VRF`,
> `PCT`/`PUN`), which is exactly why an unversioned import is unsafe.

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
| `NUM` | number | 8 values in the current UniMorph schema (SG DU TRI PL GRPL GPAUC INVN PAUC) [V 2026-08-30] | UniMorph / exact | RZ `-s`/`-es`; GZ none — plurality by quantifier (gf-grammar §1) |
| `CFG` | configuration — shape of the set | Ithkuil: UPX plus a multi-axis set (similar/dissimilar × separate/connected/fused) — **inventory not reproduced here; regenerate from a pinned grammar** | Ithkuil / local | — (pilot candidate, GZ) |
| `AFL` | affiliation — how members relate | CSL, ASO, COA, VAR | Ithkuil / local | — |
| `PRS` | perspective | M, G, N, A | Ithkuil / local | — |
| `EXT` | extension — which portion of the entity | DEL, PRX, ICP, ATV, GRA, DPL | Ithkuil / local | — |
| `ESS` | essence — real vs represented | NRM, RPV | Ithkuil / local | — (**no RZ or GZ equivalent**; RZ's `si`-conditional is irrealis, a different object) |
| `DEF` | definiteness | DEF INDF SPEC NSPEC | UniMorph / exact | RZ `le/les/un`; GZ none, by design (gf-grammar §6: definiteness left to context) |
| `GEND` | gender / noun class | MASC FEM NEUT + class features [V 2026-08-30] | UniMorph / exact | RZ none — deleted; natural gender in animate pairs only (rz-grammar §2). GZ none |
| `ANIM` | animacy | ANIM INAN HUM NHUM | UniMorph / exact | — |
| `POSS` | possession | possessor person/number features | UniMorph / exact | RZ invariant possessives (§2) |
| `CASE` | semantic/syntactic role | UniMorph's case inventory; Ithkuil's 68 [V 2026-08-30] is a different and much finer object | UniMorph + Ithkuil / overlap | RZ prepositions, no case; GZ adposition particles `hal/hees/his/hol` + word order (gf-grammar §3–4) |

### B. Lexical / derivational

| dim | name | values | src / rel | here |
|---|---|---|---|---|
| `POS` | part of speech | N V ADJ ADV + closed classes | UniMorph / exact | GZ final coda ∅/n/s (SPEC §6); RZ partial — R-scheme script-only marking is adopt-pending-evidence, not shipped |
| `STEM` | stem within a root | 4 stems in New Ithkuil [V 2026-08-30] | Ithkuil / local | — |
| `SPEC` | specification — which facet of the root | BSC, CTE, CSV, OBJ | Ithkuil / local | — (**proposed**, GZ; bead conlang-czq) |
| `FUNC` | function | STA, DYN | Ithkuil / local | GZ's O/A/P/R alternation classes cover part of this (gf-grammar §2) |
| `CTX` | context | EXS, FNC, RPS, AMG | Ithkuil / local | — |
| `VER` | version — process vs goal-attainment (`VRF` in some versions) | PRC, CPT | Ithkuil / local | — (RZ and English lexicalise it: *look for* / *find*) |
| `DERIV` ‡ | derivational family | project-listed affixes | project / local | RZ §9 (`-cion -itate -mente -al -or …`); GZ none yet |

### C. Event structure

| dim | name | values | src / rel | here |
|---|---|---|---|---|
| `TNS` | tense | PRS PST FUT + remoteness | UniMorph / exact | RZ `-va` past, `va` + inf future; GZ `hoon` preverbal past, unmarked = nonpast (gf-grammar §3) |
| `ASP` | aspect | UniMorph's inventory; Ithkuil's 36 [V 2026-08-30] is far finer | UniMorph + Ithkuil / overlap | RZ `sta` + gerund, `tener` + participle |
| `PHS` | phase (`PCT` in the current grammar, `PUN` in older material) | 9 values [V 2026-08-30] | Ithkuil / local | — |
| `VOICE` | voice | ACT PASS MID ANTIP | UniMorph / narrower — **valency-changing features (CAUS APPL RECP REFL) are a separate UniMorph dimension** [V 2026-08-30] | RZ `es` + participle; `se` reflexive |
| `VALN` | valence — relation between co-participants | 9 values [V 2026-08-30] | Ithkuil / local | — |
| `LVL` | level — comparison as a grammatical category | 9 values | Ithkuil / local | RZ periphrastic `plus/minus … que` (§7); GZ `mu-s` + `hees` |
| `EFF` | effect — beneficial/detrimental, and to whom | 9 values, including self-beneficial and self-detrimental [V 2026-08-30] | Ithkuil / local | — |
| `POL` | polarity | POS NEG | UniMorph / exact | RZ preverbal `no` + negative concord (D1) — **the `no`~`lo` hazard is bead conlang-1op**; GZ `haan`, deliberately long and nasal for robustness (gf-grammar §3) |

### D. Speaker stance (clause-level)

| dim | name | values | src / rel | here |
|---|---|---|---|---|
| `ILL` | illocution | 9 values in New Ithkuil, including POT [V 2026-08-30] | Ithkuil / local | GZ partial: `hus` clause-final polar question, bare-verb imperative — **no general illocution channel**. RZ: intonation/`?`, imperative |
| `MOOD` | mood / modality | UniMorph's inventory; Ithkuil's 6 | UniMorph + Ithkuil / overlap | RZ `-ria` conditional, `si` + indicative; no subjunctive (absorbed). GZ `huul` preverbal irrealis/future |
| `EVID` | evidentiality / validation | 12 values in the current UniMorph schema, incl. `VISU` [V 2026-08-30]; Ithkuil's Validation is a parallel 9 | UniMorph + Ithkuil / overlap | — (candidate for GZ's careful/safety register) |
| `EXPT` | expectation — stance toward outcome | COG, RSP, EXE | Ithkuil / local | — |
| `BIAS` | affective / attitudinal stance | 61 entries in the current Ithkuil table [V 2026-08-30] | Ithkuil / local | — (declined for design; precedent only) |
| `REG` | discourse register — parenthetical, exemplary, quoted thought | Ithkuil's set | Ithkuil / local | — |
| `HON` | politeness / honorification | 13 values listed in the current UniMorph schema [V 2026-08-30] | UniMorph / exact | **RZ none** — `tu`/`vos` is a number distinction, not T/V. **GZ none, permanently** (gf-grammar §6 rules honorifics out) |

### E. Reference and discourse

| dim | name | values | src / rel | here |
|---|---|---|---|---|
| `PERS` | person, with clusivity | 1 2 3, INCL, EXCL | UniMorph / exact | RZ pronouns (§3); GZ pronouns as content words (SPEC §5.2) |
| `OBV` | proximate / obviative | PROX, OBV | typological literature / local — not a Leipzig dimension | — (bead conlang-ax3) |
| `SWREF` | switch reference | SS, DS | typological literature / local | — (bead conlang-ax3) |
| `DEIX` | deictic distance | PROX, MED, DIST | typological literature / local | RZ two-way: `iste` / `aquel` (§2) |
| `INFO` ‡ | information structure | TOP, FOC, CONTR | project / local — assembled from the information-structure literature, not from a single standard | **neither language marks it today**: GZ has no topic particle (its 11 particles are listed in gf-grammar §3) and defers discourse particles to future work |
| `COREF` ‡ | coreference device | pronoun; miniature/"hashing" (UNLWS); lane | project / local | spatial layer (bead conlang-v9m) |

### F. Written-only and meta channels

| dim | name | values | src / rel | here |
|---|---|---|---|---|
| `CHK` ‡ | integrity check | computed check bit; mod-101 checksum | project / local | GZ written layer (SPEC §4.1); modes §8 |
| `PAYLD` ‡ | payload vs lexical role | LEX, PAY | project / local | modes anti-check marking (SPEC §4.2) |
| `MODE` ‡ | closed-domain frame | NUM DATE TIME SPELL PHON COORD | project / local | `docs/spec/modes.md`; RZ number mode |
| `USEM` ‡ | use vs mention (form-quote vs meaning-quote) | FORM, MEAN | UNLWS / local — **distinct from Leipzig's `QUOT`**, which glosses a reported-speech quotative | — (unlws-trailhead: to evaluate) |
| `SCOPE` ‡ | drawn scope for quantifiers and irrealis | cartouche | UNLWS / local | spatial layer (to evaluate) |
| `CLASS` ‡ | semantic classifier zone | open | project / local (Chinese radicals as precedent) | reserved script channel (SPEC §9) |

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
