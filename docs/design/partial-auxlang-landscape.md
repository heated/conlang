# Trailhead: the global partial-auxlang landscape
(Edward-supplied design-chat excerpt, 2026-08-22. Adoption figures
are chat-sourced estimates — ALL TODO-verify per citation policy;
nobody measures "IPA literacy" directly. Kept near-verbatim as a
trailhead: an entry point for future exploration, not settled
research.)

The question: what are the competing global PARTIAL auxlangs — not
full languages, but adopted sub-language conventions (NATO alphabet,
Roman numerals, IPA) — how big is each, which way are they trending,
and where is there room to compete?

## Inventory, tiered by rough adoption [all figures H, TODO-verify]

- **Billions**: Hindu-Arabic numerals (essentially all literate
  humans — the most successful constructed convention ever; took
  ~500 years to displace Roman numerals in Europe), basic arithmetic
  notation, SI units (official everywhere except the US plus
  fragments), emoji (~5B smartphone users passively; standardized
  via Unicode since 2010), and the Latin script itself as a
  universal romanization layer.
- **Hundreds of millions**: traffic signage (a frozen standards war:
  Vienna Convention pictograms vs US-style MUTCD text signs),
  chemical element symbols, Western staff notation (order 100–300M
  read it at some level), ISO 8601 dates (spreading through software
  defaults, not human preference).
- **Tens of millions**: NATO phonetic alphabet (active fluency in
  aviation/military/telecom/healthcare; passive recognition far
  wider), algebraic chess notation (post-boom, maybe 50M+ readers),
  knitting/crochet chart notation (genuinely large, and a live
  competition: Japanese JIS symbol charts are gaining on written-out
  Western patterns because charts are language-independent).
- **Millions**: IPA (productive competence maybe 1–5M: linguists,
  SLPs, classical singers, lexicographers; passive dictionary use
  wider but shallow), ICAO standard phraseology (~1M pilots and
  controllers), IMO Seaspeak/SMCP (~2M seafarers), Braille (~1M
  active readers; trend contested — literacy rates down, refreshable
  displays partially reviving it), ham Q codes.
- **Declining or dead**: Morse (sub-1M; hobbyists plus beacon
  idents), shorthand (millions of stenographers to near zero in two
  generations, killed by audio recording — the most instructive
  death in the whole set), police ten-codes (agencies moving to
  plain language after interop failures), semaphore and signal
  flags (vestigial).

## Trends: two forces decide everything now

1. **Machine mediation**: if software does the job, the human code
   dies (Morse, shorthand, flags); if software ships your code as a
   default, you win without persuading anyone (ISO 8601, emoji, QR).
2. **Institutional mandate**: UN GHS hazard pictograms went global
   in ~15 years because regulators required them; ICAO phraseology
   holds by treaty.

Grassroots adoption essentially never wins anymore.

## Room for competition: four specific shapes

1. **Revision inside institutions.** The NATO alphabet itself
   replaced Able Baker in 1956 after intelligibility testing —
   wholesale replacement via ICAO is precedented, just currently
   unmotivated.
2. **Unclaimed channels.** Emoji won the affect channel because
   nothing occupied it. Currently open: pronunciation respelling
   for learners (IPA has terrible UX and every dictionary rolls its
   own respelling — a real coordination failure), gesture
   vocabulary for VR, structured voice input.
3. **Riding defaults.** Get encoded in Unicode or shipped in an OS
   and adoption is free. Game ping systems are the live example: a
   machine-mediated gestural auxlang invented around 2019, now
   understood by hundreds of millions of players.
4. **Density plays in niches.** The realistic path for something
   like the mode-particle number/date/coordinate subsystems is not
   displacing convention but owning a domain where people produce
   that data type constantly and tooling hands out the advantage
   for free.

Structural observation: spoken partial auxlangs are rare (NATO,
ICAO, SMCP) because they only pay off in real-time cross-lingual
audio, i.e. radio. Everything else lives at the script/symbol
level, where **Unicode is now the gatekeeper. Getting your symbols
encoded is the modern form of winning.**

## Hooks into this project (duke annotations, same date)

- **partial-systems.md** reached the same wall from the other side
  ("partial systems win via mandated trained domains, institutional
  written conventions, or maintained broadcast registers — never
  via individual study decisions"); this trailhead adds the
  *machine-mediation* force and the four competition shapes to that
  finding.
- **Bootstrap scenarios** (rz-bootstrap-scenarios.md): "riding
  defaults" is S5's deep version — production tooling not as
  community accessory but as the adoption mechanism itself; the
  shorthand death (audio recording removed the job) is the standing
  threat model for the chording lane and belongs in any honest S6
  framing.
- **Mode subsystems** (number/date/time modes): the density-play
  shape says their realistic bootstrap is a *domain* (a tool
  emitting/reading mode-formatted data constantly), not general
  adoption. Candidate framing for the toolkit paper.
- **Spoken standard** (rz-spoken-standard.md): "pronunciation
  respelling for learners" is an unclaimed channel adjacent to RZ's
  orthography-transparent realization — RZ spelling is already a
  regular respelling of itself; whether a zonal respelling
  convention could serve dictionaries beyond RZ is an open
  exploration thread.
- **Script lane**: the Unicode-gatekeeper observation is a concrete
  long-horizon requirement for the featural script (private-use
  area → conscript registry → formal proposal is the standard
  ladder) — relevant to any script bake-off verdict (e35).
