#!/usr/bin/env python3
"""Score and analyse the RZ / Interlingua cloze micro-study.

Design and precommitments: docs/design/zonal/cloze-micro-study-packet.md
Bead: conlang-5i1.1

Usage:
    python3 tools/cloze_analysis.py raw.csv            # score + report
    python3 tools/cloze_analysis.py raw.csv --json     # machine-readable
    python3 tools/cloze_analysis.py --selftest         # synthetic check

Input CSV: one row per participant, one column per item, from the form
export. Column names are matched loosely (see COLUMN_HINTS); anything
unmatched is ignored. Hand-scored gist columns hold 1/0 or pass/fail.

The precommitments this script enforces, so they cannot quietly drift:

  * The RZ arm is PRIMARY: a mean with a 95% CI, pooled and per L1.
  * The RZ-vs-Interlingua contrast is SECONDARY and UNDERPOWERED. The
    report prints the minimum detectable effect next to the observed
    one, and refuses to print the word "difference" for a CI that
    spans zero -- it prints INCONCLUSIVE.
  * Exclusions are applied before any outcome is computed, and the
    count of exclusions is always reported.
"""

import argparse
import csv
import json
import math
import random
import re
import sys
import unicodedata
from collections import defaultdict

# --------------------------------------------------------------------
# The answer key. Each item: the meaning, and accepted surface answers
# across the zone languages plus English. Scoring is by MEANING, so a
# participant may answer in any language (packet section 3).
# --------------------------------------------------------------------

KEY = {
    # Text A -- the fable
    1:  ["forte", "fuerte", "strong", "fort", "puternic", "forta", "stronger"],
    2:  ["manto", "mantello", "cloak", "coat", "cape", "capa", "manteau",
         "abrigo", "manta", "mantle", "mantel", "cloak/coat"],
    3:  ["remover", "remove", "take off", "quitar", "togliere", "enlever",
         "tirar", "sacar", "despir", "scoate", "takeoff", "remove it"],
    4:  ["soplar", "sufflar", "blow", "soffiare", "souffler", "soprar",
         "sufla", "assoprar", "blowing", "to blow"],
    5:  ["copriva", "coperiva", "covered", "cubria", "cubrio", "cubrir",
         "coprire", "couvrir", "cobrir", "cobria", "wrapped", "acopera",
         "wrapped himself", "covered himself"],
    6:  ["fin", "end", "final", "fine", "finally", "fim", "sfarsit", "last"],
    7:  ["brilar", "brillar", "shine", "brillare", "briller", "brilhar",
         "stralui", "glow", "shining", "to shine"],
    8:  ["removeva", "removed", "remove", "quito", "quitar", "took off",
         "tolse", "enleva", "tirou", "scoase", "saco", "take off"],
    9:  ["reconocer", "recognoscer", "admit", "recognise", "recognize",
         "riconoscere", "reconnaitre", "reconhecer", "acknowledge",
         "admitir", "ammettere", "recunoaste", "concede"],
    10: ["forte", "fuerte", "strong", "fort", "puternic", "forta", "strongest"],
    # Text D -- the news item
    26: ["hodie", "today", "hoy", "oggi", "aujourdhui", "hoje", "azi"],
    27: ["solar", "solare", "solaire", "sun", "solara", "sun power"],
    28: ["tres", "three", "tre", "trois", "trei", "3"],
    29: ["pais", "country", "paese", "pays", "tara", "nation", "state"],
    30: ["investimento", "investment", "inversion", "investissement",
         "investitie", "cost", "budget", "spend", "spending"],
    31: ["crear", "creara", "create", "creare", "creer", "criar", "crea",
         "generate", "make", "will create", "provide"],
    32: ["reducir", "reducer", "reducera", "reduce", "ridurre", "reduire",
         "reduzir", "cut", "lower", "reduces", "will reduce", "decrease"],
    33: ["cento", "cent", "percent", "ciento", "per cent", "suta", "100",
         "percentage"],
    34: ["anuncio", "annuncio", "announcement", "annonce", "news",
         "declaration", "declaracion", "statement", "plan", "anunt",
         "announce"],
    35: ["transparencia", "transparency", "trasparenza", "transparence",
         "detail", "details", "detalles", "claritate", "clarity",
         "information", "informacion", "info"],
}

TEXT_A = list(range(1, 11))
TEXT_D = list(range(26, 36))

# Column-name fragments we look for, case-insensitively.
COLUMN_HINTS = {
    "l1": ["first language", "l1", "native language", "lingua"],
    "conlang": ["constructed", "conlang", "interlingua or", "esperanto"],
    "condition_a": ["condition a", "variant a", "text a arm", "a_arm"],
    "condition_d": ["condition d", "variant d", "text d arm", "d_arm"],
    "gist_a": ["gist a", "gist_a", "summary a"],
    "gist_d": ["gist d", "gist_d", "summary d"],
    "duration": ["duration", "time taken", "seconds", "elapsed"],
}

MIN_DURATION_S = 90  # packet section 4: exclude sub-90s completions


# --------------------------------------------------------------------
# scoring
# --------------------------------------------------------------------

def norm(s):
    """Lowercase, strip accents and punctuation, collapse whitespace."""
    if s is None:
        return ""
    s = unicodedata.normalize("NFD", str(s).lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    s = re.sub(r"[^a-z0-9 ]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def accepts(answer, accepted):
    """Semantic match against the key, generously but not blindly.

    Exact normalised match, or a shared 5-character prefix (which
    catches inflection: 'cubrio' vs 'cubrir', 'reduces' vs 'reduce')
    without matching unrelated words.
    """
    a = norm(answer)
    if not a:
        return False
    for v in accepted:
        n = norm(v)
        if not n:
            continue
        if a == n:
            return True
        if len(n) >= 5 and len(a) >= 5 and a[:5] == n[:5]:
            return True
    return False


def find_col(fieldnames, hints):
    for name in fieldnames:
        low = name.lower()
        for h in hints:
            if h in low:
                return name
    return None


def item_col(fieldnames, n):
    """Locate the column holding item n."""
    pat = re.compile(r"(^|[^0-9])%d([^0-9]|$)" % n)
    best = None
    for name in fieldnames:
        if pat.search(name):
            # prefer a column that looks like an item, not a timestamp
            if any(w in name.lower() for w in ("time", "date", "id", "code")):
                continue
            if best is None or len(name) < len(best):
                best = name
    return best


# --------------------------------------------------------------------
# statistics
# --------------------------------------------------------------------

def wilson(k, n, z=1.96):
    """Wilson score interval for a binomial proportion."""
    if n == 0:
        return (0.0, 0.0, 0.0)
    p = k / n
    d = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / d
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (p, max(0.0, centre - half), min(1.0, centre + half))


def bootstrap_mean(values, iters=10000, seed=20260830):
    """Percentile bootstrap CI for a mean over participants."""
    if not values:
        return (0.0, 0.0, 0.0)
    rng = random.Random(seed)
    n = len(values)
    means = []
    for _ in range(iters):
        means.append(sum(rng.choice(values) for _ in range(n)) / n)
    means.sort()
    lo = means[int(0.025 * iters)]
    hi = means[int(0.975 * iters) - 1]
    return (sum(values) / n, lo, hi)


def mde_paired(n, sd_estimate=0.25, alpha=0.05, power=0.80):
    """Minimum detectable paired effect, in proportion points.

    Two-sided, z-approximation. sd_estimate is the SD of the paired
    difference in proportion units; 0.25 is a deliberately optimistic
    stand-in for a 10-item passage and is stated as an assumption.
    """
    if n < 2:
        return float("nan")
    z_a, z_b = 1.959964, 0.8416212
    return (z_a + z_b) * sd_estimate / math.sqrt(n)


# --------------------------------------------------------------------
# pipeline
# --------------------------------------------------------------------

def load(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def analyse(rows, fieldnames):
    col = {k: find_col(fieldnames, h) for k, h in COLUMN_HINTS.items()}
    items = {n: item_col(fieldnames, n) for n in KEY}
    missing = [n for n, c in items.items() if c is None]

    kept, excluded = [], defaultdict(int)
    for r in rows:
        if col["conlang"] and norm(r.get(col["conlang"])) in ("yes", "y", "si", "oui"):
            excluded["self-reported conlang study"] += 1
            continue
        if col["duration"]:
            try:
                if float(r[col["duration"]]) < MIN_DURATION_S:
                    excluded["completed under 90s"] += 1
                    continue
            except (TypeError, ValueError):
                pass
        answered = sum(1 for n, c in items.items()
                       if c and norm(r.get(c)))
        if answered == 0:
            excluded["all blanks empty"] += 1
            continue
        kept.append(r)

    per_participant = []
    item_stats = defaultdict(lambda: {"ok": 0, "n": 0})
    for r in kept:
        rec = {"l1": (r.get(col["l1"]) or "unknown").strip() or "unknown",
               "arms": {}}
        for label, idxs, cond_key, gist_key in (
                ("A", TEXT_A, "condition_a", "gist_a"),
                ("D", TEXT_D, "condition_d", "gist_d")):
            arm = "?"
            if col[cond_key]:
                v = norm(r.get(col[cond_key]))
                if "rz" in v:
                    arm = "RZ"
                elif "ia" in v or "interlingua" in v:
                    arm = "IA"
            ok = n = 0
            for i in idxs:
                c = items.get(i)
                if not c:
                    continue
                n += 1
                good = accepts(r.get(c), KEY[i])
                ok += 1 if good else 0
                item_stats[i]["n"] += 1
                item_stats[i]["ok"] += 1 if good else 0
            gist = None
            if col[gist_key]:
                gist = norm(r.get(col[gist_key])) in ("1", "pass", "yes", "y", "true")
            rec["arms"][label] = {"arm": arm, "ok": ok, "n": n, "gist": gist}
        per_participant.append(rec)

    def arm_scores(arm):
        out = []
        for p in per_participant:
            for a in p["arms"].values():
                if a["arm"] == arm and a["n"]:
                    out.append(a["ok"] / a["n"])
        return out

    def arm_gist(arm):
        vals = [a["gist"] for p in per_participant for a in p["arms"].values()
                if a["arm"] == arm and a["gist"] is not None]
        return vals

    rz, ia = arm_scores("RZ"), arm_scores("IA")
    paired = []
    for p in per_participant:
        got = {a["arm"]: (a["ok"] / a["n"]) for a in p["arms"].values()
               if a["n"] and a["arm"] in ("RZ", "IA")}
        if "RZ" in got and "IA" in got:
            paired.append(got["RZ"] - got["IA"])

    by_l1 = defaultdict(list)
    for p in per_participant:
        for a in p["arms"].values():
            if a["arm"] == "RZ" and a["n"]:
                by_l1[p["l1"]].append(a["ok"] / a["n"])

    diff = bootstrap_mean(paired) if paired else (0.0, 0.0, 0.0)
    return {
        "n_submitted": len(rows),
        "n_kept": len(kept),
        "exclusions": dict(excluded),
        "missing_item_columns": missing,
        "rz": bootstrap_mean(rz), "rz_n": len(rz),
        "ia": bootstrap_mean(ia), "ia_n": len(ia),
        "rz_gist": (sum(arm_gist("RZ")) / len(arm_gist("RZ"))) if arm_gist("RZ") else None,
        "ia_gist": (sum(arm_gist("IA")) / len(arm_gist("IA"))) if arm_gist("IA") else None,
        "by_l1": {k: bootstrap_mean(v) + (len(v),) for k, v in sorted(by_l1.items())},
        "paired_diff": diff,
        "paired_n": len(paired),
        "mde": mde_paired(len(paired)) if paired else float("nan"),
        "items": {i: wilson(s["ok"], s["n"]) + (s["n"],)
                  for i, s in sorted(item_stats.items())},
    }


def pct(x):
    return f"{100 * x:5.1f}%"


def report(a):
    L = []
    w = L.append
    w("=" * 66)
    w("RZ / Interlingua cloze micro-study — results")
    w("=" * 66)
    w(f"Submitted: {a['n_submitted']}    Analysed: {a['n_kept']}")
    for k, v in a["exclusions"].items():
        w(f"  excluded, {k}: {v}")
    if a["missing_item_columns"]:
        w(f"  !! item columns not found: {a['missing_item_columns']}")
    w("")
    w("PRIMARY — zero-study comprehension (specifics score)")
    m, lo, hi = a["rz"]
    w(f"  RZ           {pct(m)}   95% CI [{pct(lo)}, {pct(hi)}]   n={a['rz_n']}")
    m2, lo2, hi2 = a["ia"]
    w(f"  Interlingua  {pct(m2)}   95% CI [{pct(lo2)}, {pct(hi2)}]   n={a['ia_n']}")
    if a["rz_gist"] is not None:
        w(f"  gist: RZ {pct(a['rz_gist'])}" +
          (f"   Interlingua {pct(a['ia_gist'])}" if a["ia_gist"] is not None else ""))
    w("")
    w("  by first language (RZ arm)")
    for l1, (m3, lo3, hi3, n3) in a["by_l1"].items():
        w(f"    {l1[:22]:22} {pct(m3)}  [{pct(lo3)}, {pct(hi3)}]  n={n3}")
    w("")
    w("SECONDARY — RZ minus Interlingua (EXPLORATORY, UNDERPOWERED)")
    if a["paired_n"]:
        d, dlo, dhi = a["paired_diff"]
        w(f"  observed paired difference  {100*d:+.1f} points"
          f"   95% CI [{100*dlo:+.1f}, {100*dhi:+.1f}]   n={a['paired_n']}")
        w(f"  minimum detectable effect at 80% power: ~{100*a['mde']:.0f} points")
        if dlo <= 0 <= dhi:
            w("  VERDICT: INCONCLUSIVE. The interval spans zero. This study")
            w("  cannot distinguish 'no difference' from 'a difference too")
            w("  small for n={}'. Do not report this as a null result."
              .format(a["paired_n"]))
        else:
            w("  VERDICT: interval excludes zero — still exploratory, and")
            w("  requires the confirmatory arm before it is a claim.")
    else:
        w("  no paired observations (condition columns missing?)")
    w("")
    w("PER-ITEM failure rates — a design signal, not an outcome")
    w("  item   correct   95% CI              n")
    for i, (p, lo4, hi4, n4) in a["items"].items():
        flag = "  <-- most miss this" if p < 0.34 and n4 >= 5 else ""
        w(f"  {i:>4}   {pct(p)}   [{pct(lo4)}, {pct(hi4)}]   {n4:>3}{flag}")
    w("")
    w("Reminder (packet section 4): an item most participants miss is a")
    w("lexicon bug; an item one L1 misses is a weighting bug.")
    return "\n".join(L)


def selftest():
    """Synthetic data: a strong RZ reader set with a small IA gap."""
    rng = random.Random(7)
    fieldnames = (["First language", "Condition A", "Condition D",
                   "Gist A", "Gist D", "Duration (s)",
                   "Studied a constructed language"]
                  + [f"Item {i}" for i in KEY])
    rows = []
    for k in range(24):
        rz_first = k % 2 == 0
        r = {"First language": ["Spanish", "Portuguese", "Italian", "French"][k % 4],
             "Condition A": "RZ" if rz_first else "IA",
             "Condition D": "IA" if rz_first else "RZ",
             "Gist A": "1", "Gist D": "1" if k % 3 else "0",
             "Duration (s)": "240",
             "Studied a constructed language": "No"}
        for i in KEY:
            r[f"Item {i}"] = KEY[i][0] if rng.random() < 0.82 else "zzz"
        rows.append(r)
    rows.append(dict(rows[0], **{"Studied a constructed language": "Yes"}))
    rows.append(dict(rows[0], **{"Duration (s)": "20"}))
    a = analyse(rows, fieldnames)
    print(report(a))
    assert a["n_kept"] == 24, a["n_kept"]
    assert a["exclusions"]["self-reported conlang study"] == 1
    assert a["exclusions"]["completed under 90s"] == 1
    assert 0.6 < a["rz"][0] < 0.95, a["rz"]
    assert a["paired_n"] == 24
    print("\nselftest OK — exclusions applied, arms split, CIs computed")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("csv", nargs="?", help="form export")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        selftest()
        return 0
    if not args.csv:
        ap.error("give a CSV, or --selftest")
    rows = load(args.csv)
    if not rows:
        print("no rows", file=sys.stderr)
        return 1
    a = analyse(rows, list(rows[0].keys()))
    print(json.dumps(a, indent=2, default=list) if args.json else report(a))
    return 0


if __name__ == "__main__":
    sys.exit(main())
