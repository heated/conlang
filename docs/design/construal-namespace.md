# Construal namespace — a reference registry of markable distinctions

**Status:** instrument, v0 (2026-08-30; adoption across the ledger
and toolkit = bead conlang-ma1; the one priced proposal it produced
so far, the `CN:SPEC` grid, = bead conlang-czq). Origin: the Ithkuil steal-pass
(`alternatives/ithkuil-forks.md`) — Edward's framing: "Ithkuil as
taxonomy or namespace might be useful as a reference, sort of like
IPA." Evidence labels as elsewhere. Counts sourced from Ithkuil are
pinned to **New Ithkuil (2023)** and marked TODO-verify until
checked against the published grammar.

## 1. What it is, and the IPA analogy

IPA names *sounds* independently of any orthography, so two
languages can be compared on what they contrast rather than how
they spell it. This registry names *grammatical and construal
distinctions* independently of how any language realises them, so
a ledger row, a toolkit entry, a grammar table, or an interlinear
gloss can say **what** a feature marks with a stable identifier —
separately from *how* (affix, particle, tone, word order, glyph
zone, silence).

Uses in this project:

- **Ledger rows** (`learning-budget.md`): "what it buys" becomes
  checkable — `CN:EVID.{OBS,RPR,INF}` is a claim, "adds
  evidentials" is not.
- **Toolkit entries** (program lane E): zone-agnostic by
  construction — "an optional clause-particle set marking
  `CN:EVID`" is portable; "*dizque*" is not.
- **Cross-conlang comparison**: Esperanto's `-o/-a/-i` marks
  `CN:POS`; Lojban's `UI` marks `CN:BIAS` + `CN:EVID`; Toaq's tone
  marks `CN:ROLE`; GZ's final coda marks `CN:POS`.
- **Glosses**: the Leipzig line stays Leipzig; the namespace is the
  ontology *behind* the abbreviation, consulted when an abbreviation
  is ambiguous or missing.

A tag says what is marked, never how, and never that marking it is
a good idea — pricing lives in the ledger.

## 2. Sources and precedence

| source | what it standardises | limit |
|---|---|---|
| **Leipzig Glossing Rules** (Comrie, Haspelmath & Bickel; 2008, rev. 2015) [TODO-verify] | ~80 gloss abbreviations, the de-facto interlinear standard | a glossing convention, not an ontology; silent on construal categories |
| **UniMorph schema** (Sylak-Glassman 2016) [TODO-verify] | ~23 dimensions, ~212 features, for morphological annotation across languages | morphology only (periphrastic marking out of scope); values are a union of attested inflection, not construal |
| **GOLD** ontology, **WALS** feature set | typological feature ontology / survey chapters | coarse; for citation, not tagging |
| **Ithkuil** (Quijada 2011; New Ithkuil 2023) | the most complete catalogue of *construal* categories in one place — set shape, boundary, evidence, stance, goal-attainment | one designer's theory; some dimensions overlap (Phase vs Aspect), several are only attested in Ithkuil itself |
| this project | written-only channels (check, payload role), mode frames | project-specific |

**Precedence rule:** use the UniMorph/Leipzig code where one
exists; fall back to Ithkuil's where the standards are silent (mark
†); coin a project code only for project-specific channels (mark
‡). Never rename a standard code to match Ithkuil or vice versa.

## 3. Identifier scheme

```
CN:<DIM>              a dimension            CN:EVID
CN:<DIM>.<VAL>        a value                CN:EVID.RPR
CN:<DIM>.{A,B,C}      a value subset         CN:EVID.{OBS,RPR,INF}
†  Ithkuil-sourced code      ‡  project-coined code   (bare = standard)
```

Dimension codes ≤ 5 letters; value codes 3–5 letters, uppercase.
Ithkuil's own three-letter abbreviations are reused verbatim where
adopted (they are already stable identifiers in that community).
A tag never carries a realisation; realisation is documented next
to it ("`CN:POS` — realised as the word-final coda, SPEC §6").

## 4. The registry

Columns: dimension · values (count) · source · where it lives here
(GZ / RZ / modes / script / —).

### A. Nominal construal (what kind of thing, how many, how bounded)

| dim | name | values | src | here |
|---|---|---|---|---|
| `NUM` | number | SG DU TRI PAUC PL GRPL (6) | UniMorph | RZ `-s`; GZ none (quantifiers) |
| `CFG` † | configuration — shape of the set | UPX; then {D,M} × {S similar, D dissimilar, F fuzzy} × {S separate, C connected, F fused} → DPX MSS MSC MSF MDS MDC MDF MFS MFC MFF DSS DSC DSF DDS DDC DDF DFS DFC DFF (20) [TODO-verify] | Ithkuil | — (pilot candidate, GZ) |
| `AFL` † | affiliation — how members relate | CSL consolidative, ASO associative, COA coalescent, VAR variative (4) | Ithkuil | — |
| `PRS` † | perspective | M monadic, G agglomerative, N nomic, A abstract (4) | Ithkuil | — (nomic ≈ RZ generic article use) |
| `EXT` † | extension — which part of the entity | DEL delimitive, PRX proximal, ICP inceptive, ATV attenuative, GRA graduative, DPL depletive (6) | Ithkuil | — |
| `ESS` † | essence — real vs represented | NRM normal, RPV representative (2) | Ithkuil | — (RZ conditional/`si` covers part) |
| `DEF` | definiteness | DEF INDF SPEC NSPEC (4) | UniMorph | RZ articles; GZ none |
| `GEND` | gender / noun class | M F N + class indices | UniMorph | RZ none (deleted); GZ none |
| `ANIM` | animacy | ANIM INAN HUM NHUM (4) | UniMorph | — |
| `POSS` | possession | possessor person/number features | UniMorph | RZ possessives |
| `CASE` | semantic/syntactic role | UniMorph ~40 (NOM ACC ERG ABS DAT GEN INS COM LOC ALL ABL …); Ithkuil 68 in 9 groups [TODO-verify] | UniMorph; † for the tail | RZ prepositions (no case); GZ particles + order |

### B. Lexical / derivational (how a root yields words)

| dim | name | values | src | here |
|---|---|---|---|---|
| `POS` | part of speech | N V ADJ ADV + closed classes | UniMorph | GZ final coda (SPEC §6); RZ endings (partial, R-scheme pending) |
| `STEM` † | stem within a root | S0 S1 S2 S3 (4) | Ithkuil | — |
| `SPEC` † | specification — which facet of the root | BSC basic, CTE contential, CSV constitutive, OBJ objective (4) | Ithkuil | — (**proposed** for GZ: the grid bead) |
| `FUNC` † | function | STA stative, DYN dynamic (2) | Ithkuil | GZ O/A/P/R alternation classes cover part |
| `CTX` † | context | EXS existential, FNC functional, RPS representational, AMG amalgamative (4) | Ithkuil | — |
| `VER` † | version — process vs goal-attainment | PRC processual, CPT completive (2) | Ithkuil | — (English/RZ lexicalise: *look for / find*) |
| `DERIV` ‡ | derivational family | project-listed affixes (`-cion -itate -mente -al -or …`) | project | RZ §9; GZ none yet |

### C. Event structure (how the event unfolds)

| dim | name | values | src | here |
|---|---|---|---|---|
| `TNS` | tense | PRS PST FUT (+ remoteness) | UniMorph | RZ `-va`, `va +inf` |
| `ASP` | aspect | UniMorph: IPFV PFV PRF PROG PROSP ITER HAB (7); Ithkuil 36 [TODO-verify] | UniMorph; † tail | RZ `sta +nte`, `tener +te` |
| `PHS` † | phase — internal temporal texture | PUN ITR REP ITM RCT FRE FRG VAC FLC (9) | Ithkuil | — |
| `VOICE` | voice / valency change | ACT PASS MID ANTIP CAUS APPL RECP REFL | UniMorph | RZ `es +te`, `se` |
| `VALN` † | valence — relation between co-participants | MNO PRL CRO RCP CPL DUP DEM CNG PTI (9) | Ithkuil | — |
| `LVL` † | level — comparison built in | MIN SBE IFR DFT EQU SUR SPL SPQ MAX (9) | Ithkuil | RZ `plus/minus … que` (periphrastic) |
| `EFF` † | effect — beneficial/detrimental to whom | 1:BEN 2:BEN 3:BEN UNK 3:DET 2:DET 1:DET (7–9) [TODO-verify] | Ithkuil | — |
| `POL` | polarity | POS NEG | UniMorph | RZ `no` + concord (D1); GZ negation particle (1op: unprotected — see bead) |

### D. Speaker stance (clause-level; the natural particle layer)

| dim | name | values | src | here |
|---|---|---|---|---|
| `ILL` † | illocution | ASR assertive, DIR directive, DEC declarative, IRG interrogative, VRF verificative, ADM admonitive, HOR hortative, CNJ conjectural (8) | Ithkuil (UniMorph folds into MOOD) | RZ intonation/`?`, imperative; GZ clause particles |
| `MOOD` | mood / modality | UniMorph ~19 (IND SBJV COND IMP OPT POT IRR DEB OBLIG …); Ithkuil FAC SUB ASM SPC COU HYP (6) | UniMorph; † | RZ `-ria`, `si` (no subjunctive — absorbed) |
| `EVID` | evidentiality / validation | UniMorph: FH NFH DRCT SEN NVSEN AUD HRSY QUOT RPRT INFER ASSUM (11); Ithkuil: OBS REC PUP RPR USP IMA CVN ITU INF (9) [TODO-verify] | UniMorph; † | — (Tier-3 candidate, GZ careful/safety register) |
| `EXPT` † | expectation — stance toward outcome | COG cognitive, RSP responsive, EXE executive (3) | Ithkuil | — |
| `BIAS` † | affective / attitudinal stance | Ithkuil ~57 (ACC ADM ANN APB APH ARB … VEX) [TODO-verify]; organic internet set `/s /j /srs /gen /lh /hj …` | Ithkuil; folk | — (declined; precedent only) |
| `REG` † | discourse register — parenthetical, example, quoted thought… | DSV PNT SPF EXM CGT (5–6) [TODO-verify] | Ithkuil | — |
| `HON` | politeness / honorific | UniMorph ~12 (INFM FORM ELEV HUMB POL …) | UniMorph | RZ `tu/vos` (2 values) |
| `INTQ` | interrogativity marking | Q polarity-Q content-Q | Leipzig `Q` | RZ fronting, no inversion |

### E. Reference and discourse (who is who across the text)

| dim | name | values | src | here |
|---|---|---|---|---|
| `PERS` | person (+ clusivity) | 1 2 3, INCL EXCL, 1+2 … | UniMorph | RZ pronouns; GZ pronouns (content words) |
| `OBV` | proximate / obviative | PROX OBV | Leipzig | — (bead ax3: coreference marking) |
| `SWREF` | switch reference | SS DS | Leipzig | — (bead ax3) |
| `DEIX` | deixis / demonstrative distance | PROX MED DIST | Leipzig | RZ `iste / aquel` (2) |
| `INFO` | information structure | TOP FOC CONTR | Leipzig | GZ topic particle (gf-grammar) |
| `COREF` ‡ | coreference device | pronoun, hashing/miniature (UNLWS), lane | project | spatial layer (v9m) |

### F. Written-only and meta channels (no spoken counterpart)

| dim | name | values | src | here |
|---|---|---|---|---|
| `CHK` ‡ | integrity check | computed check bit; mod-101 checksum | project | GZ written layer (SPEC §4); modes §8 |
| `PAYLD` ‡ | payload vs lexical role | LEX PAY | project | modes anti-check (SPEC §4.2) |
| `MODE` ‡ | closed-domain frame | NUM DATE TIME SPELL PHON COORD | project | modes.md; RZ number mode |
| `QUOT` | use vs mention | form-quote, meaning-quote | Leipzig `QUOT`; UNLWS | — (unlws-trailhead: to evaluate) |
| `SCOPE` ‡ | drawn scope (quantifier, irrealis) | cartouche | UNLWS | spatial layer (to evaluate) |
| `CLASS` ‡ | semantic classifier zone | open | project (Chinese radicals precedent) | reserved script channel (SPEC §9) |

## 5. How to use it here

1. **Ledger rows**: add a `marks:` clause to "what it buys" —
   `marks: CN:POS (final coda)`. Retro-tag existing rows (bead).
2. **Toolkit entries** (lane E): the entry's *name* is its
   namespace tag plus realisation class: "clause-particle set for
   `CN:EVID`", "coda channel for `CN:POS`", "frame for
   `CN:MODE.NUM`".
3. **Grammar tables**: a `CN:` column on GZ's particle table and
   RZ's verb table, so two grammars can be diffed on what they
   mark.
4. **Comparisons with other conlangs** (steal-pass rounds): tag the
   stolen mechanism before pricing it, so the ledger never says
   "adds an Ithkuil thing."
5. **Glosses** stay Leipzig; use the namespace when Leipzig has no
   abbreviation (write the tag in the gloss line, e.g. `bridge
   closed-EVID.RPR`).

## 6. Limits, stated

- Ithkuil's dimensions are one designer's analysis; several overlap
  (`PHS` vs `ASP`; `LVL` vs comparison; `EXPT` vs `MOOD`) and some
  are attested nowhere else. The registry records them; it does
  not claim they are universal or even distinct.
- UniMorph is morphology-only, so a language that marks a
  dimension periphrastically ("I heard that…") has the dimension
  in the namespace but no UniMorph feature. The namespace does not
  care; tagging is about what is marked, not by what.
- Counts marked TODO-verify were written from memory of the
  published grammars and must be checked against the 2023 grammar
  before any of them appears in the paper.
- The namespace is a catalogue, not a menu: listing a dimension is
  not a proposal to mark it. Proposals go through the ledger.
