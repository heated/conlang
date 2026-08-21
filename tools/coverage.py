#!/usr/bin/env python3
"""Lexical coverage curves for RZ — how much text does the Nth root buy?

The learning-budget ledger prices lexicon acquisition in learner-hours
but has never measured what a root is WORTH. This measures it on the
RZ corpus, and separates two curves that natural languages conflate:

- **surface coverage**: distinct written word-forms needed for X% of
  running tokens (what an irregular language charges);
- **lemma coverage**: distinct STEMS needed, given that RZ's
  morphology is exception-free — a learner who knows `parla` and the
  closed suffix set gets parla/parlava/parlaria/parlar/parlante/
  parlate/parlas for free.

The vertical gap between the curves is the regularity dividend, in
percentage-points of text per root learned. That number is the honest
version of "regular morphology makes it cheaper", and it belongs in
the ledger.

Also reports the closed-class share (function words = the fixed cost
every learner pays in the first hour) and a Zipf extrapolation to
estimate the root count behind coverage targets beyond corpus reach.

Usage: python3 tools/coverage.py [--json]
"""

from __future__ import annotations

import json
import math
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
# CORPUS: cloze-test-v0.md is EXCLUDED — it reproduces the
# romance-zonal-v0 passages with content words blanked out, so
# including it double-counted function words and under-counted content
# (Codex review 2026-08-22, finding 3). Everything below is the
# de-duplicated running-text corpus.
CORPUS_FILES = ("rz-texts.md", "romance-zonal-v0.md", "rz-lite.md")
DERIVED_FILES = ("cloze-test-v0.md",)   # excluded; kept for the audit

# Inflectional suffixes, longest first. RZ's citation form for a verb
# IS the present (stem + class vowel a/e/i, rz-grammar §4), so bare
# -a/-e/-i are NEVER stripped: `parla` is a lemma, not `parl`.
# Participles are stem+te (parlate = parla+te), so -ate/-ite must not
# strip either (Codex review finding 1). Verbal morphology is delegated
# to rz_script.analyze(), which gates -va/-ria on an attested verb-stem
# set — a heuristic strip turns `historia` into `histo`.
NOMINAL_INFLECTIONS = ("es", "s")
VERBAL_TAIL = ("nte", "te", "r")
# derivational suffixes (§9) — these make NEW lemmas, so they are not
# stripped for lemma counting; tracked separately as the multiplier.
# Longest-first, and -itate strips as a unit (nacionalitate -> nacional
# -> nacion) rather than leaving `nacionalit`.
# -ia (domain/state) is deliberately EXCLUDED: it is the least
# productive family here and over-strips inherited words that merely
# end in -ia (materia -> mater, historia -> hist), which is exactly
# the failure mode the review caught on the inflection side.
DERIVATIONS = ("itate", "cion", "mente", "abile", "ibile", "ista",
               "oso", "or", "al")

# Closed class, SELECTION RULE (Codex review finding 2): exactly the
# grammar words enumerated in rz-grammar.md §2-§7 — articles,
# demonstratives, possessives, quantifiers, pronouns (all three
# columns), prepositions, conjunctions/subordinators, negators,
# question words, comparison particles, and the three irregular
# verbs that double as auxiliaries (es/era/seria, va, sta/stava).
# Lexical items that merely feel functional are OUT: greetings
# (bon, gracias, pardon, adeu) and regular verbs (pote, vole, debe,
# face, prende) are open-class content words with ordinary paradigms.
CLOSED = {
    # articles, demonstratives, possessives (§2)
    "le", "les", "la", "las", "un", "une", "del", "al",
    "iste", "istes", "aquel", "aqueles", "mi", "tu", "su",
    "nostre", "vostre", "lor",
    # quantifiers (§2)
    "tote", "totes", "multe", "multo", "poc", "alcun", "necun",
    "cata", "altre", "altres", "mesme",
    # pronouns (§3)
    "io", "me", "te", "el", "ela", "eles", "elas", "nos", "vos",
    "se", "on", "lo",
    # prepositions (§2, §7 usage)
    "de", "a", "en", "con", "sin", "sobre", "por", "entre",
    "desde", "durante", "ante", "tras", "segun", "contra",
    # conjunctions / subordinators (§7)
    "e", "o", "ma", "que", "qui", "si", "porque", "quando", "mentre",
    "aunque", "como", "anque", "ni",
    # negation (§5)
    "no", "nunca", "nada", "nadie",
    # question words (§6)
    "donde", "cuante", "cual", "cuales",
    # comparison (§7)
    "plus", "minus", "tanto",
    # deixis/time adverbs that are grammar words
    "ja", "alora", "aqui", "ala", "hodie", "ora", "ancora", "sempre",
    "antes", "despues",
    # the three irregular verbs (§4), which are also the auxiliaries
    "es", "era", "seria", "va", "sta", "stava", "ha",
}


def corpus_tokens(include_derived=False):
    """Blockquote lines of the de-duplicated corpus docs (blockquotes
    are RZ text; surrounding prose is English commentary)."""
    toks = []
    base = ROOT / "docs" / "design" / "zonal"
    names = CORPUS_FILES + (DERIVED_FILES if include_derived else ())
    for name in names:
        path = base / name
        if not path.exists():
            continue
        for m in re.finditer(r"^> (.*)$", path.read_text(), re.M):
            line = re.sub(r"\([^)]*\)", " ", m.group(1))
            for t in re.findall(r"[a-zA-Z][a-zA-Z-]*", line.lower()):
                if t.isascii():
                    toks.append(t.strip("-"))
    return [t for t in toks if t]


def lemma(word):
    """Surface form -> citation form (present for verbs, singular for
    nouns/adjectives). Verbal morphology comes from rz_script.analyze,
    which gates tense suffixes on an attested verb-stem set."""
    if word in CLOSED:
        return word
    try:
        from rz_script import analyze, verb_stems
    except Exception:                                # pragma: no cover
        analyze, verb_stems = None, None
    if analyze is not None:
        stem, tense, _ = analyze(word)
        if tense:                       # parlava -> parla, gated
            return stem
        stems = verb_stems()
        for suf in VERBAL_TAIL:         # participle/gerund/infinitive
            if word.endswith(suf):
                base = word[: -len(suf)]
                if base in stems:       # parlate/parlante/parlar -> parla
                    return base
    for suf in NOMINAL_INFLECTIONS:     # plural
        if word.endswith(suf) and len(word) - len(suf) >= 3:
            base = word[: -len(suf)]
            if base[-1] in "aeiou" or suf == "es":
                return base
    return word


def root(word):
    """Strip derivation as well as inflection: nacionalitate ->
    nacional -> nacion. Approximate — derivation is iterative (§9)."""
    w = lemma(word)
    changed = True
    while changed:
        changed = False
        for suf in DERIVATIONS:
            if w.endswith(suf) and len(w) - len(suf) >= 4:
                w = w[: -len(suf)]
                changed = True
                break
    return w


# Paradigm sizes are a property of the GRAMMAR, not of a 937-token
# corpus — measure them from the rules (rz-grammar.md §4/§3), because
# corpus sparsity hides the dividend entirely (nearly every content
# word appears once, so forms/lemma measures ~1.0 whatever the
# morphology does).
RZ_PARADIGM = {
    # synthetic (affixed) forms a learner must RECOGNIZE per lemma
    "verb": 7,      # present, -va, -ria, -r inf, -nte ger, -te part,
                    #   +plural agreement is nil (person-invariant)
    "noun": 2,      # sg, -s/-es
    "adjective": 2,  # sg, plural (no gender agreement in RZ)
}
# Reference paradigm sizes for the donor languages, synthetic forms
# only (conservative counts, indicative+subjunctive+imperative, all
# persons/numbers; excludes compound tenses which are analytic in
# both). [D] — standard descriptive grammars.
DONOR_PARADIGM = {
    "spanish_verb": 53, "italian_verb": 49, "french_verb": 42,
    "spanish_noun": 2, "spanish_adjective": 4,   # gender x number
}


def coverage_curve(counter):
    """[(rank, cumulative_share)] over items ordered by frequency."""
    total = sum(counter.values())
    curve, cum = [], 0
    for i, (_, c) in enumerate(counter.most_common(), start=1):
        cum += c
        curve.append((i, cum / total))
    return curve


def items_for(curve, target):
    for rank, share in curve:
        if share >= target:
            return rank
    return None


def zipf_scenario(counter, target, vocab_size):
    """Coverage rank under a TRUNCATED, NORMALIZED Zipf model.

    Codex review 2026-08-22 (finding 4) confirmed the previous version
    was not a valid extrapolation: it summed an unnormalized tail whose
    mass diverges, while its probabilities were normalized to the small
    observed sample, and its "clamp" silently replaced measured ranks
    with larger model ranks. Fixed as an explicit SCENARIO:

      p(r) = r^-a / sum_{k=1..V} k^-a       for a vocabulary of V types

    with `a` fitted on the observed mid ranks (the head decays steeper
    than the content tail, so it is excluded from the fit). V is an
    ASSUMPTION, not a measurement — the caller sweeps it and the
    result is reported as a band. Returns None if the fit is not
    supportable from the sample.
    """
    total = sum(counter.values())
    freqs = [c / total for _, c in counter.most_common()]
    if len(freqs) < 60:
        return None
    r1, r2 = 20, min(150, len(freqs) - 1)
    a = math.log(freqs[r1 - 1] / freqs[r2 - 1]) / math.log(r2 / r1)
    norm = sum(k ** (-a) for k in range(1, vocab_size + 1))
    cum = 0.0
    for r in range(1, vocab_size + 1):
        cum += r ** (-a) / norm
        if cum >= target:
            return r
    return None                       # target unreachable within V


def fit_exponent(counter):
    total = sum(counter.values())
    freqs = [c / total for _, c in counter.most_common()]
    if len(freqs) < 60:
        return None
    r1, r2 = 20, min(150, len(freqs) - 1)
    return math.log(freqs[r1 - 1] / freqs[r2 - 1]) / math.log(r2 / r1)


# Curriculum lesson blocks as EXPLICIT SETS (Codex review finding 5:
# the previous table's named blocks were unvalidated labels on a
# frequency-only curve). Each block lists what it teaches; coverage is
# computed from the union of the sets actually named, and skills that
# add no token coverage (paradigms, modes) are marked as such.
LESSON_PLAN = [
    {"hours": 1.0, "name": "closed-class block + spelling/stress",
     "closed": True, "lemma_ranks": 0,
     "skills": ["orthography", "penult stress"]},
    {"hours": 1.0, "name": "verb system (one table) + top-20 lemmas",
     "closed": False, "lemma_ranks": 20,
     "skills": ["complete verb paradigm — adds forms of lemmas "
                "already counted, not new lemmas"]},
    {"hours": 2.0, "name": "next 54 lemmas + derivation families",
     "closed": False, "lemma_ranks": 74,
     "skills": ["derivation (§9) — generative, not corpus-visible"]},
    {"hours": 2.0, "name": "number mode + calendar + next 48 lemmas",
     "closed": False, "lemma_ranks": 122,
     "skills": ["number mode (own ledger row)", "calendar"]},
    {"hours": 4.0, "name": "topic packs (+95 lemmas)",
     "closed": False, "lemma_ranks": 217, "skills": []},
    {"hours": 4.0, "name": "tail to corpus edge",
     "closed": False, "lemma_ranks": 241, "skills": []},
]


def lesson_curve(toks, open_lemmas, closed_share):
    """Coverage after each lesson block, computed from explicit sets."""
    ranked = [w for w, _ in open_lemmas.most_common()]
    lem_count = Counter(lemma(t) for t in toks)
    n = len(toks)
    rows, hours = [], 0.0
    for block in LESSON_PLAN:
        hours += block["hours"]
        known = set(ranked[: block["lemma_ranks"]])
        covered = sum(lem_count[w] for w in known)
        rows.append({
            "cumulative_hours": hours, "block": block["name"],
            "open_lemmas_known": block["lemma_ranks"],
            "token_coverage": round(closed_share + covered / n, 4),
            "skills_without_token_coverage": block["skills"],
        })
    return rows


def report():
    toks = corpus_tokens()
    surface = Counter(toks)
    lemmas = Counter(lemma(t) for t in toks)
    open_toks = [t for t in toks if t not in CLOSED]
    open_lemmas = Counter(lemma(t) for t in open_toks)

    sc = coverage_curve(surface)
    lc = coverage_curve(lemmas)
    oc = coverage_curve(open_lemmas)

    closed_share = 1 - len(open_toks) / len(toks)
    forms_per_lemma = len(surface) / len(lemmas)

    targets = (0.50, 0.70, 0.80, 0.90, 0.95)
    rows = []
    for t in targets:
        s, l = items_for(sc, t), items_for(lc, t)
        rows.append({
            "target": t, "surface_forms": s, "lemmas": l,
            "dividend_forms_saved": (s - l) if (s and l) else None,
        })

    roots = Counter(root(t) for t in open_toks)
    rc = coverage_curve(roots)

    # the regularity dividend is a grammar fact, not a corpus fact:
    # forms a learner must acquire per lemma, RZ vs donors
    rz_avg = (RZ_PARADIGM["verb"] + RZ_PARADIGM["noun"] +
              RZ_PARADIGM["adjective"]) / 3
    donor_avg = (DONOR_PARADIGM["spanish_verb"] +
                 DONOR_PARADIGM["spanish_noun"] +
                 DONOR_PARADIGM["spanish_adjective"]) / 3

    out = {
        "corpus_tokens": len(toks),
        "distinct_surface_forms": len(surface),
        "distinct_lemmas": len(lemmas),
        "distinct_open_roots": len(roots),
        "forms_per_lemma_in_corpus": round(forms_per_lemma, 3),
        "corpus_sparsity_caveat":
            "forms/lemma ~1.0 is a corpus-size artifact (most content "
            "words appear once); the inflectional dividend is measured "
            "from the grammar, below",
        "closed_class_token_share": round(closed_share, 4),
        "closed_class_size_in_corpus": len(
            [w for w in surface if w in CLOSED]),
        "coverage": rows,
        "open_class_lemmas_for_targets": {
            f"{t:.0%}": items_for(oc, t) for t in targets},
        "open_class_roots_for_targets": {
            f"{t:.0%}": items_for(rc, t) for t in targets},
        "zipf_scenarios_open_lemmas": {
            "fitted_exponent": (round(fit_exponent(open_lemmas), 3)
                                if fit_exponent(open_lemmas) else None),
            "note": "V (vocabulary size) is an ASSUMPTION swept as a "
                    "band, not a measurement; model is a truncated "
                    "normalized Zipf. Corpus-measured ranks are "
                    "reported separately above and are NOT replaced.",
            "ranks": {f"V={V}": {f"{t:.0%}": zipf_scenario(
                open_lemmas, t, V) for t in (0.90, 0.95)}
                for V in (1000, 3000, 8000)},
        },
        "lesson_curve": lesson_curve(toks, open_lemmas, closed_share),
        "corpus_files": list(CORPUS_FILES),
        "excluded_as_derived": list(DERIVED_FILES),
        "paradigm": {
            "rz": RZ_PARADIGM, "donors": DONOR_PARADIGM,
            "rz_mean_forms_per_lemma": round(rz_avg, 2),
            "spanish_mean_forms_per_lemma": round(donor_avg, 2),
            "recognition_load_ratio": round(donor_avg / rz_avg, 2),
            "rz_forms_are_exceptionless": True,
        },
        "top_lemmas": lemmas.most_common(15),
    }
    return out


def main():
    out = report()
    if "--json" in sys.argv:
        print(json.dumps(out, indent=2))
        return 0
    print(f"corpus: {out['corpus_tokens']} tokens, "
          f"{out['distinct_surface_forms']} surface forms, "
          f"{out['distinct_lemmas']} lemmas "
          f"({out['forms_per_lemma_in_corpus']} forms/lemma — "
          f"corpus artifact, see caveat)")
    print(f"closed-class share of tokens: "
          f"{out['closed_class_token_share']:.1%} "
          f"({out['closed_class_size_in_corpus']} words attested)")
    print("\ntarget  surface-forms  lemmas  dividend")
    for r in out["coverage"]:
        print(f"{r['target']:>5.0%}  {str(r['surface_forms']):>13}  "
              f"{str(r['lemmas']):>6}  {str(r['dividend_forms_saved']):>8}")
    print("\nopen-class lemmas alone (closed class assumed known):")
    for k, v in out["open_class_lemmas_for_targets"].items():
        print(f"  {k}: {v}  (roots after derivation: "
              f"{out['open_class_roots_for_targets'][k]})")
    p = out["paradigm"]
    print(f"\nparadigm load: RZ {p['rz_mean_forms_per_lemma']} forms/"
          f"lemma (exceptionless) vs Spanish "
          f"{p['spanish_mean_forms_per_lemma']} — ratio "
          f"{p['recognition_load_ratio']}x")
    z = out["zipf_scenarios_open_lemmas"]
    print(f"\nZipf SCENARIOS (open lemmas; fitted exponent "
          f"{z['fitted_exponent']}; V is an assumption, not a "
          f"measurement):")
    for vk, targets in z["ranks"].items():
        print(f"  {vk}: " + ", ".join(f"{t} at rank {r}"
                                      for t, r in targets.items()))
    print("\nlesson curve (coverage computed from explicit sets):")
    for r in out["lesson_curve"]:
        print(f"  ~{r['cumulative_hours']:>4.0f}h  "
              f"{r['token_coverage']:6.1%}  {r['block']}")
    print("\ntop lemmas:", ", ".join(
        f"{w}({c})" for w, c in out["top_lemmas"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
