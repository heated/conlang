#!/usr/bin/env python3
"""Per-L1 COGNATE AVAILABILITY of the RZ corpus (conlang-i78).

Scope correction (Edward, 2026-08-22): annotators who know all the
languages cannot simulate a monolingual reader's experience — so
this tool does NOT claim to measure recognition. It aggregates
annotator-stated LEXICAL RELATIONS between each RZ lemma and each
reader language — facts about the language pair, auditable via the
recorded anchor words:

  T  an everyday cognate exists (aqua -> ES agua)
  P  the nearest hook is learned-register or form-obscured
  O  no usable relative
  F  the nearest neighbor means something else (misleading hook)

Evidence status: judgments [A] (single-pass annotator-stated
relations, anchors recorded); aggregation [D]; any inference to
actual reader recognition is [H] until the cloze estimates
per-class conversion rates. See rz-transparency.md for the full
framing and the hardening path (mechanical orthographic distance,
corpus-derived register).

Data: tools/transparency_data/{es,pt,it,fr,en}.json —
{lemma: [class, anchor]}.

Usage: python3 tools/transparency.py [--json]
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from coverage import CLOSED, corpus_tokens_by_file, lemma  # noqa: E402

DATA = Path(__file__).resolve().parent / "transparency_data"
ALL_LANGS = ("es", "pt", "it", "fr", "en")
CLASSES = ("T", "P", "O", "F")


def langs_present():
    """Aggregate only languages whose data files exist; the rest are
    reported as pending (PT/IT/FR annotation was interrupted by
    session limits on 2026-08-22 — bead tracks completion)."""
    return tuple(l for l in ALL_LANGS if (DATA / f"{l}.json").exists())


def load_judgments():
    out = {}
    for lang in langs_present():
        path = DATA / f"{lang}.json"
        raw = json.loads(path.read_text())
        judged = {}
        for lem, val in raw.items():
            cls = val[0].upper()
            if cls not in CLASSES:
                raise ValueError(f"{lang}:{lem}: bad class {val[0]!r}")
            judged[lem] = (cls, val[1] if len(val) > 1 else "")
        out[lang] = judged
    return out


def shares(lem_counts, judged):
    """Token- and type-weighted class shares for one language."""
    tok_total = sum(lem_counts.values())
    tok = Counter()
    typ = Counter()
    missing = []
    for lem, c in lem_counts.items():
        j = judged.get(lem)
        if j is None:
            missing.append(lem)
            continue
        tok[j[0]] += c
        typ[j[0]] += 1
    return {
        "token_share": {c: round(tok[c] / tok_total, 4) for c in CLASSES},
        "token_share_T_plus_P": round((tok["T"] + tok["P"]) / tok_total, 4),
        "type_share": {c: round(typ[c] / len(lem_counts), 4)
                       for c in CLASSES},
        "unjudged_lemmas": missing,
    }


def worst(lem_counts, judged, cls, n=8):
    rows = [(lem, c, judged[lem][1]) for lem, c in lem_counts.items()
            if lem in judged and judged[lem][0] == cls]
    rows.sort(key=lambda r: -r[1])
    return rows[:n]


def report():
    by_file = corpus_tokens_by_file()
    all_toks = [t for toks in by_file.values() for t in toks]
    lem_all = Counter(lemma(t) for t in all_toks)
    lem_closed = Counter({w: c for w, c in lem_all.items() if w in CLOSED})
    lem_open = Counter({w: c for w, c in lem_all.items()
                        if w not in CLOSED})
    judged = load_judgments()

    out = {
        "corpus_tokens": sum(lem_all.values()),
        "distinct_lemmas": len(lem_all),
        "evidence": "judgments [A] annotator calls; aggregation [D]; "
                    "reader comprehension implications [H] until cloze",
        "by_language": {},
        "per_file_T_token_share": {},
        "highest_frequency_opaque_or_false": {},
    }
    out["pending_languages"] = [l for l in ALL_LANGS
                                if l not in langs_present()]
    for lang in langs_present():
        out["by_language"][lang] = {
            "all": shares(lem_all, judged[lang]),
            "closed_class": shares(lem_closed, judged[lang]),
            "open_class": shares(lem_open, judged[lang]),
        }
        out["highest_frequency_opaque_or_false"][lang] = {
            "O": worst(lem_all, judged[lang], "O"),
            "F": worst(lem_all, judged[lang], "F"),
        }
    for name, toks in by_file.items():
        counts = Counter(lemma(t) for t in toks)
        out["per_file_T_token_share"][name] = {
            lang: shares(counts, judged[lang])["token_share"]["T"]
            for lang in langs_present()}
    return out


def main():
    out = report()
    if "--json" in sys.argv:
        print(json.dumps(out, indent=2))
        return 0
    print(f"corpus: {out['corpus_tokens']} tokens, "
          f"{out['distinct_lemmas']} lemmas   ({out['evidence']})")
    print("\ntoken-weighted cognate availability by reader L1 "
          "(T = everyday cognate; T+P adds learned/obscured hooks):")
    if out["pending_languages"]:
        print(f"  PENDING (no data yet): "
              f"{', '.join(out['pending_languages'])}")
    print("lang     T     T+P     F     O    | closed-T  open-T")
    for lang in out["by_language"]:
        d = out["by_language"][lang]
        a = d["all"]["token_share"]
        tp = d["all"]["token_share_T_plus_P"]
        print(f"  {lang}  {a['T']:6.1%} {tp:6.1%} {a['F']:5.1%} "
              f"{a['O']:5.1%}  |  {d['closed_class']['token_share']['T']:6.1%}"
              f"  {d['open_class']['token_share']['T']:6.1%}")
        miss = d["all"]["unjudged_lemmas"]
        if miss:
            print(f"      UNJUDGED ({len(miss)}): {', '.join(miss[:12])}")
    print("\nper-text at-sight (T) token share:")
    for name, row in out["per_file_T_token_share"].items():
        print(f"  {name}: " + "  ".join(f"{lang} {v:.0%}"
                                        for lang, v in row.items()))
    print("\nhighest-frequency problem lemmas (fix-list):")
    for lang in out["by_language"]:
        hf = out["highest_frequency_opaque_or_false"][lang]
        f_str = ", ".join(f"{w}({c}: {a})" for w, c, a in hf["F"][:4])
        o_str = ", ".join(f"{w}({c})" for w, c, _ in hf["O"][:6])
        print(f"  {lang}  F: {f_str or '—'}")
        print(f"      O: {o_str or '—'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
