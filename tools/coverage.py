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
CORPUS_FILES = ("rz-texts.md", "romance-zonal-v0.md", "cloze-test-v0.md",
                "rz-lite.md")

# rz-grammar.md §4/§9: the complete inflectional suffix set. Order
# matters — longest first, so -ria strips before -a.
INFLECTIONS = ("ria", "va", "nte", "ate", "ite", "te", "es", "s",
               "ar", "er", "ir", "a", "e", "i")
# derivational suffixes (§9) — these make NEW lemmas, so they are not
# stripped for lemma counting; tracked separately as the multiplier
DERIVATIONS = ("cion", "itate", "mente", "abile", "ibile", "ista",
               "oso", "or", "al", "ia")

# closed class: particles/determiners/preps/pronouns/conjunctions that
# a learner acquires as a block in the first lesson (rz-grammar §2-7)
CLOSED = {
    "le", "les", "un", "une", "de", "del", "a", "al", "e", "o", "que",
    "qui", "no", "si", "en", "con", "por", "para", "sin", "sobre",
    "su", "se", "io", "tu", "el", "ela", "nos", "vos", "eles", "me",
    "te", "nos", "les", "iste", "aquel", "istes", "aqueles", "ma",
    "plus", "minus", "multo", "ja", "anque", "cata", "tote", "totes",
    "quando", "donde", "como", "cuante", "alora", "aqui", "ala",
    "hodie", "ora", "ancora", "sempre", "nunca", "nada", "nadie",
    "es", "era", "va", "sta", "ha", "durante", "entre", "desde",
    "mentre", "porque", "aunque", "antes", "despues", "pardon",
    "bon", "gracias", "adeu", "seria", "stava", "pote", "vole",
    "debe", "face", "prende", "cual", "cuales",
}


def corpus_tokens():
    """Quoted sample lines from the zonal corpus docs (blockquotes are
    the RZ text; surrounding prose is English commentary)."""
    toks = []
    base = ROOT / "docs" / "design" / "zonal"
    for name in CORPUS_FILES:
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
    """Strip inflection to a stem. Conservative: never strips below 3
    characters, never touches closed-class words (they ARE lemmas)."""
    if word in CLOSED:
        return word
    for suf in INFLECTIONS:
        if word.endswith(suf) and len(word) - len(suf) >= 3:
            return word[: -len(suf)]
    return word


def root(word):
    """Strip derivation as well as inflection: nacionalitate ->
    nacion-ish. Approximate — derivation is iterative in RZ (§9)."""
    w = lemma(word)
    changed = True
    while changed:
        changed = False
        for suf in DERIVATIONS:
            if w.endswith(suf) and len(w) - len(suf) >= 3:
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


def zipf_extrapolate(counter, target):
    """Estimate item count for a coverage target beyond corpus reach,
    fitting a Zipf-Mandelbrot-ish harmonic model to the observed
    distribution. Fit deliberately AVOIDS the head (function words
    decay steeper than the content tail and made the first version
    underestimate below corpus-measured values); exponent comes from
    the mid ranks. Clamped to the corpus-measured count when the
    corpus already reaches the target. Rough by construction, [D]."""
    total = sum(counter.values())
    freqs = [c / total for _, c in counter.most_common()]
    if len(freqs) < 60:
        return None
    r1, r2 = 20, min(150, len(freqs) - 1)
    a = math.log(freqs[r1 - 1] / freqs[r2 - 1]) / math.log(r2 / r1)
    # anchor the model at rank r1, not rank 1 (head is off-model)
    c = freqs[r1 - 1] * r1 ** a
    cum, r = sum(freqs[: r1]), r1
    while cum < target and r < 10 ** 6:
        r += 1
        cum += min(c * r ** (-a), freqs[-1])
    est = r if cum >= target else None
    measured = items_for(coverage_curve(counter), target)
    if est is not None and measured is not None:
        est = max(est, measured)
    return est


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
        "zipf_extrapolation_open_lemmas": {
            f"{t:.0%}": zipf_extrapolate(open_lemmas, t)
            for t in (0.95, 0.98)},
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
    print("\nZipf extrapolation (open-class lemmas, [D] rough, "
          "clamped >= measured):")
    for k, v in out["zipf_extrapolation_open_lemmas"].items():
        print(f"  {k}: {v}")
    print("\ntop lemmas:", ", ".join(
        f"{w}({c})" for w, c in out["top_lemmas"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
