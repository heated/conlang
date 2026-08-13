# Capacity bottleneck ledger (conlang-sss)

The standing account of what limits the monosyllabic root count and
what each relaxation rung costs, priced against the silent-mishearing
metric (the project's ground truth). Simulation:
`tools/explore_posreuse.py` (Monte Carlo, per-channel confusion rates
in the no-parity study's sensitive-listener ballpark: onset 1.0%,
vowel 0.6%, coda 1.5% toward confusable neighbors).

## The bottleneck stack (why 22 and not 50)

1. Raw bodies: 10 onsets × 5 vowels − glide cells = **50**.
2. Humility rule (covered ∪ forbidden pairs never mint unrelated
   minimal pairs): MIS = **22** (adopted policy).
3. Weighted-pair caution (strict): 18. Eye pairs (strict_with_script):
   17. Reserve for drift (30%): **15 assignable now**.

## The relaxation rungs, priced

| rung | roots | silent subs / 10k words | notes |
|---|---|---|---|
| baseline (adopted) | 22 | **0.6–0.7** | residual = double mishearings landing on words |
| + POS-lane reuse ×3 | **66** | q=0.80: 30.3 · q=0.90: 14.8 · q=0.95: **7.4** · q=0.99: 2.5 | q = probability a syntactic slot rejects a wrong-POS form |
| + partial domain partitioning | ~80–130 | same mechanism, domain-checkability replacing q | not yet simulated; structurally identical pricing |

(Also measured: repair burden — caught errors — rises from ~1.6% of
words to ~2.8–3.1% under reuse: more collisions land on valid words
and get syntax-caught rather than being non-word repairs. "Harmless"
same-root inflection errors, ~1.5% of words, are unchanged and
typically syntax-caught too.)

## Reading the numbers honestly

- The new silent class scales as (1−q) × coda-flip rate. Driving it
  back to the baseline's ~0.7/10k would need q ≈ 0.998 — no natural
  syntax checks that hard.
- But the simulation prices **syntactic** catching only. A cross-lane
  substitution passes syntax as a *semantically unrelated* word in
  context (hearing an unrelated verb where an unrelated noun's lane
  was meant); the semantic-implausibility filter that natural
  languages run catches most of the remainder. English carries vastly
  denser homophony than 7/10k and functions.
- The POS outer code is doing real work: without it (if wrong-POS
  forms were never checkable, q=0), reuse would cost ~150/10k —
  syntax buys a 20–60× reduction.

## Verdict on the 80–120 claim

**Validated as reachable, with a real but ordinary-language-sized
price.** 22 → 66 via POS-lane reuse costs 2.5–30 silent
substitutions per 10k words depending on syntactic checkability
(likely 5–10 at realistic q≈0.93–0.96, before semantic filtering);
the remaining gap to 80–120 comes from partial domain partitioning
under the same pricing logic. The original framing ("without touching
the phonology") holds — no inventory change — but the cost is not
zero: it is a shift from *engineered-rare* silent errors to
*natural-language-typical* ones, plus roughly a doubling of the
repair/confirmation burden. That trade is a **product-positioning
decision** (engineered-reliability identity vs lexicon room) and goes
to the freeze gate, not to a workshop default.

## Ledger upkeep

New rungs and re-pricings append here. Next candidates: domain
partitioning simulation (needs a domain-tagged seed lexicon — after
kps starts); disyllable-capacity interaction (reuse relieves pressure
on monosyllables, changing how many disyllables the Zipf assignment
needs); echo-vowel/tosmabru cost re-derivation at reuse-scale.
