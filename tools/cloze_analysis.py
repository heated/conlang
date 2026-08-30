#!/usr/bin/env python3
"""Score and analyse the RZ / Interlingua cloze micro-study.

Design and precommitments: docs/design/zonal/cloze-micro-study-packet.md
Bead: conlang-5i1.1

THE PROTOCOL IS TWO-STAGE, AND THIS TOOL DOES NOT SCORE.

The packet commits to semantic scoring "by hand, blind to condition",
accepting an answer in any language. A finite allow-list cannot
implement that — an earlier version of this file tried, and a review
found ten false positives (`mantener` scored as *manteau*, `decree`
as *decrease*, `clarinet` as *clarity*) and ten false negatives
(`retirar`, `ôter`, `pelerină`, `el más fuerte`, `astăzi`) in a single
pass. So the machine no longer decides:

    stage 1   export-blind   responses shuffled, condition stripped,
                             one row per (participant, item), with an
                             optional non-binding `suggestion` column
    stage 2   [a human]      fills the `correct` column with 0/1
    stage 3   analyse        joins conditions back, applies the
                             precommitted exclusions, reports

Usage:
    python3 tools/cloze_analysis.py export-blind raw.csv -o blind.csv
    python3 tools/cloze_analysis.py analyse raw.csv blind.csv
    python3 tools/cloze_analysis.py analyse raw.csv blind.csv --json
    python3 tools/cloze_analysis.py selftest

Everything that could silently change the published number is fatal:
a missing or duplicated item column, an unrecognised condition value,
a participant without exactly one RZ and one IA passage, a missing or
unparseable duration, an unrecognised hand-score. The tool refuses to
produce a number it cannot stand behind.
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
# The answer key: the committed meaning of each blanked slot. These are
# HINTS for the human scorer, never a scoring rule. Adding a surface
# form here does not change any published number.
# --------------------------------------------------------------------

MEANING = {
    1:  "strong (predicative, 'the stronger of the two')",
    2:  "cloak / coat / outer garment",
    3:  "to take off / remove (the cloak)",
    4:  "to blow (of wind)",
    5:  "covered / wrapped himself (reflexive past)",
    6:  "the end / finally / at last",
    7:  "to shine (of the sun)",
    8:  "removed / took off (past)",
    9:  "to admit / acknowledge / concede",
    10: "strong (superlative, 'the strongest')",
    26: "today",
    27: "solar",
    28: "three",
    29: "country",
    30: "investment / total cost",
    31: "create (jobs)",
    32: "reduce / cut (emissions)",
    33: "per cent",
    34: "announcement / the statement just made",
    35: "transparency / openness about the schedule",
}

# Suggestion lists only. Deliberately generous; the human adjudicates.
HINTS = {
    1:  ["forte", "fuerte", "strong", "fort", "puternic"],
    2:  ["manto", "mantello", "cloak", "coat", "cape", "capa", "manteau", "pelerina"],
    3:  ["remover", "remove", "take off", "quitar", "retirar", "togliere", "enlever", "oter"],
    4:  ["soplar", "sufflar", "blow", "soffiare", "souffler", "soprar", "sufla"],
    5:  ["covered", "cubrir", "coprire", "couvrir", "cobrir", "wrapped"],
    6:  ["fin", "end", "final", "fine", "fim", "sfarsit"],
    7:  ["brillar", "shine", "brillare", "briller", "brilhar", "splendere", "luire"],
    8:  ["removed", "quitar", "took off", "togliere", "enlever", "tirar"],
    9:  ["reconocer", "admit", "recognise", "riconoscere", "reconnaitre", "admettre"],
    10: ["forte", "fuerte", "strong", "fort", "puternic"],
    26: ["hodie", "today", "hoy", "oggi", "hoje", "astazi"],
    27: ["solar", "solare", "solaire"],
    28: ["tres", "three", "tre", "trois", "trei", "3"],
    29: ["pais", "country", "paese", "pays", "tara", "nation"],
    30: ["investimento", "investment", "inversion", "investissement", "cost"],
    31: ["crear", "create", "creare", "creer", "criar", "generate"],
    32: ["reducir", "reduce", "ridurre", "reduire", "reduzir", "cut", "diminuir"],
    33: ["cento", "percent", "ciento", "per cent", "suta", "hundred"],
    34: ["anuncio", "announcement", "annonce", "news", "statement"],
    35: ["transparencia", "transparency", "trasparenza", "transparence", "clarity"],
}

TEXT_A = list(range(1, 11))
TEXT_D = list(range(26, 36))
ALL_ITEMS = TEXT_A + TEXT_D

# The export schema. Exact names — no fuzzy matching, because a wrong
# guess here silently changes the only number this project publishes.
COL_PID = "participant_id"
COL_L1 = "first_language"
COL_CONLANG = "studied_conlang"
COL_DURATION = "duration_seconds"
COL_COND = {"A": "condition_A", "D": "condition_D"}
COL_GIST = {"A": "gist_A", "D": "gist_D"}


def item_col(n):
    return f"item_{n}"


REQUIRED = ([COL_PID, COL_L1, COL_CONLANG, COL_DURATION]
            + list(COL_COND.values()) + list(COL_GIST.values())
            + [item_col(n) for n in ALL_ITEMS])

L1_CANON = {
    "es": "ES", "spanish": "ES", "espanol": "ES", "castellano": "ES",
    "pt": "PT", "portuguese": "PT", "portugues": "PT",
    "it": "IT", "italian": "IT", "italiano": "IT",
    "fr": "FR", "french": "FR", "francais": "FR",
    "ro": "RO", "romanian": "RO", "romana": "RO",
}
YES = {"yes", "y", "true", "1", "si", "sim", "oui", "da"}
NO = {"no", "n", "false", "0", "non", "nu", "nao"}
ARMS = {"rz": "RZ", "ia": "IA", "interlingua": "IA"}

MIN_DURATION_S = 90         # packet §4, per participant
MIN_N_FOR_CI = 8            # below this an interval is not reported
MDE_SD_ASSUMED = 0.25       # stated, not hidden


class DataError(Exception):
    """A data problem serious enough that no number should be printed."""


# --------------------------------------------------------------------
# normalisation (used ONLY for suggestions and for parsing enums)
# --------------------------------------------------------------------

def norm(s):
    if s is None:
        return ""
    s = unicodedata.normalize("NFD", str(s).lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    s = re.sub(r"[^a-z0-9 ]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def suggest(answer, item):
    """A non-binding hint for the human scorer. Exact match only —
    a prefix rule produced `decree` for `decrease`, so there isn't one."""
    a = norm(answer)
    if not a:
        return ""
    return "likely" if any(a == norm(h) for h in HINTS.get(item, [])) else ""


# --------------------------------------------------------------------
# loading and validation — everything here is fatal
# --------------------------------------------------------------------

def read_raw(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        first = f.readline()
        f.seek(0)
        header = next(csv.reader([first]))
        dupes = {h for h in header if header.count(h) > 1}
        if dupes:
            raise DataError(
                f"duplicate column names in {path}: {sorted(dupes)} — "
                "csv.DictReader would silently keep only the last, so "
                "fix the export before analysing")
        rows = list(csv.DictReader(f))

    missing = [c for c in REQUIRED if c not in header]
    if missing:
        raise DataError(
            f"{path} is missing required columns: {missing}\n"
            f"expected exactly the schema in the packet: {REQUIRED}")
    if not rows:
        raise DataError(f"{path} has no data rows")

    seen = set()
    for r in rows:
        pid = (r.get(COL_PID) or "").strip()
        if not pid:
            raise DataError("a row has an empty participant_id")
        if pid in seen:
            raise DataError(f"duplicate participant_id: {pid}")
        seen.add(pid)
        for label, col in COL_COND.items():
            v = norm(r.get(col))
            if v not in ARMS:
                raise DataError(
                    f"participant {pid}: {col} = {r.get(col)!r}; "
                    f"expected one of {sorted(set(ARMS))}")
        arms = {ARMS[norm(r[c])] for c in COL_COND.values()}
        if arms != {"RZ", "IA"}:
            raise DataError(
                f"participant {pid} has arms {sorted(arms)}; the design "
                "gives every participant exactly one RZ and one IA passage")
    return rows


def parse_duration(v, pid):
    s = (v or "").strip()
    if not s:
        raise DataError(f"participant {pid}: empty duration_seconds — "
                        "the exclusion cannot be applied, so nothing is scored")
    m = re.fullmatch(r"(\d+):([0-5]?\d)", s)      # mm:ss
    if m:
        return int(m.group(1)) * 60 + int(m.group(2))
    try:
        x = float(s)
    except ValueError:
        raise DataError(f"participant {pid}: duration_seconds = {s!r} "
                        "is not a number or mm:ss")
    if not math.isfinite(x) or x < 0:
        raise DataError(f"participant {pid}: duration_seconds = {s!r}")
    return x


def parse_bool(v, pid, what):
    n = norm(v)
    if n in YES:
        return True
    if n in NO:
        return False
    raise DataError(f"participant {pid}: {what} = {v!r}; expected a "
                    f"yes/no value from the form's closed choices")


# --------------------------------------------------------------------
# stage 1 — the blinded export
# --------------------------------------------------------------------

def export_blind(rows, out_path, seed=20260830):
    """One row per (participant, item), shuffled, condition stripped."""
    recs = []
    for r in rows:
        pid = r[COL_PID].strip()
        for n in ALL_ITEMS:
            recs.append({
                "response_id": f"{pid}::{n}",
                "item": n,
                "meaning_committed": MEANING[n],
                "response": (r.get(item_col(n)) or "").strip(),
                "suggestion": suggest(r.get(item_col(n)), n),
                "correct": "",
            })
    random.Random(seed).shuffle(recs)
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(recs[0].keys()))
        w.writeheader()
        w.writerows(recs)
    return len(recs)


def read_scores(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    scores, blank = {}, 0
    for r in rows:
        rid = (r.get("response_id") or "").strip()
        raw = (r.get("correct") or "").strip()
        if not rid:
            raise DataError("a scored row has no response_id")
        if raw == "":
            blank += 1
            continue
        n = norm(raw)
        if n in YES:
            scores[rid] = True
        elif n in NO:
            scores[rid] = False
        else:
            raise DataError(f"{rid}: correct = {raw!r}; expected 0/1")
    if blank:
        raise DataError(f"{blank} responses are unscored — every response "
                        "must carry a human 0/1 judgment before analysis")
    return scores


# --------------------------------------------------------------------
# statistics
# --------------------------------------------------------------------

def wilson(k, n, z=1.96):
    if n == 0:
        return None
    p = k / n
    d = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / d
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (p, max(0.0, centre - half), min(1.0, centre + half))


def bootstrap_mean(values, iters=10000, seed=20260830):
    """Percentile bootstrap over PARTICIPANTS. Returns None when the
    interval would not be meaningful, rather than a zero-width one."""
    n = len(values)
    if n == 0:
        return None
    mean = sum(values) / n
    if n < MIN_N_FOR_CI or len(set(values)) < 2:
        return (mean, None, None)
    rng = random.Random(seed)
    means = sorted(sum(rng.choice(values) for _ in range(n)) / n
                   for _ in range(iters))
    return (mean, means[int(0.025 * iters)], means[int(0.975 * iters) - 1])


def mde_paired(n, sd=MDE_SD_ASSUMED, alpha=0.05, power=0.80):
    """Minimum detectable paired difference, normal approximation.

    Uses the supplied alpha and power (the previous version ignored
    them). Exact paired-t is slightly larger — about 14.6 points where
    this gives 14.0 at n=25 — so this is the optimistic end, which is
    why the report prints the assumption and a sensitivity range.
    """
    if n < 2:
        return None
    from statistics import NormalDist
    z_a = NormalDist().inv_cdf(1 - alpha / 2)
    z_b = NormalDist().inv_cdf(power)
    return (z_a + z_b) * sd / math.sqrt(n)


# --------------------------------------------------------------------
# stage 3 — analysis
# --------------------------------------------------------------------

def analyse(rows, scores):
    expected = {f"{r[COL_PID].strip()}::{n}" for r in rows for n in ALL_ITEMS}
    if set(scores) != expected:
        missing = sorted(expected - set(scores))[:5]
        extra = sorted(set(scores) - expected)[:5]
        raise DataError(f"scored file does not match the raw file. "
                        f"missing e.g. {missing}; unexpected e.g. {extra}")

    kept, excluded = [], defaultdict(int)
    for r in rows:
        pid = r[COL_PID].strip()
        if parse_bool(r.get(COL_CONLANG), pid, COL_CONLANG):
            excluded["self-reported conlang study"] += 1
            continue
        if parse_duration(r.get(COL_DURATION), pid) < MIN_DURATION_S:
            excluded[f"completed under {MIN_DURATION_S}s"] += 1
            continue
        if all(not (r.get(item_col(n)) or "").strip() for n in ALL_ITEMS):
            excluded["all blanks empty"] += 1
            continue
        kept.append(r)
    if not kept:
        raise DataError("every participant was excluded; nothing to report")

    # cells: arm x passage x L1
    cells = defaultdict(list)          # (arm, passage, l1) -> [score]
    gist = defaultdict(list)           # (arm, passage, l1) -> [bool]
    items = defaultdict(lambda: {"ok": 0, "n": 0})   # (arm, item)
    paired, by_arm, by_arm_l1 = [], defaultdict(list), defaultdict(list)

    for r in rows:
        if r not in kept:
            continue
        pid = r[COL_PID].strip()
        l1raw = norm(r.get(COL_L1))
        l1 = L1_CANON.get(l1raw, "other")
        got = {}
        for label, idxs in (("A", TEXT_A), ("D", TEXT_D)):
            arm = ARMS[norm(r[COL_COND[label]])]
            ok = sum(1 for n in idxs if scores[f"{pid}::{n}"])
            for n in idxs:
                items[(arm, n)]["n"] += 1
                items[(arm, n)]["ok"] += 1 if scores[f"{pid}::{n}"] else 0
            frac = ok / len(idxs)
            cells[(arm, label, l1)].append(frac)
            gist[(arm, label, l1)].append(
                parse_bool(r.get(COL_GIST[label]), pid, COL_GIST[label]))
            by_arm[arm].append(frac)
            by_arm_l1[(arm, l1)].append(frac)
            got[arm] = frac
        paired.append(got["RZ"] - got["IA"])

    diff = bootstrap_mean(paired)
    ci_estimable = diff is not None and diff[1] is not None
    verdict, inconclusive = "not estimable", True
    if ci_estimable:
        if diff[1] <= 0 <= diff[2]:
            verdict = ("INCONCLUSIVE — the interval spans zero. This study "
                       "cannot tell 'no difference' from 'a difference too "
                       "small to detect at this n'. It is not evidence of a "
                       "null.")
        else:
            verdict = ("interval excludes zero — still exploratory, and it "
                       "requires the confirmatory arm before it is a claim.")
            inconclusive = False

    def pack(v):
        if v is None:
            return None
        m, lo, hi = v
        return {"mean": m, "lo": lo, "hi": hi}

    return {
        "protocol": "two-stage: blinded human scoring, then analysis",
        "n_submitted": len(rows),
        "n_analysed": len(kept),
        "exclusions": dict(excluded),
        "arms": {a: dict(pack(bootstrap_mean(v)), n=len(v))
                 for a, v in sorted(by_arm.items())},
        "by_arm_l1": {f"{a}/{l}": dict(pack(bootstrap_mean(v)) or {}, n=len(v))
                      for (a, l), v in sorted(by_arm_l1.items())},
        "by_cell": {f"{a}/{p}/{l}": {"mean": sum(v) / len(v), "n": len(v)}
                    for (a, p, l), v in sorted(cells.items())},
        "gist": {f"{a}/{p}/{l}": {"pass": sum(v) / len(v), "n": len(v)}
                 for (a, p, l), v in sorted(gist.items())},
        "paired": dict(pack(diff) or {}, n=len(paired)),
        "ci_estimable": ci_estimable,
        "inconclusive": inconclusive,
        "verdict": verdict,
        "mde": mde_paired(len(paired)),
        "mde_assumptions": {
            "sd_paired_difference_assumed": MDE_SD_ASSUMED,
            "alpha": 0.05, "power": 0.80,
            "sensitivity": {str(sd): mde_paired(len(paired), sd)
                            for sd in (0.20, 0.25, 0.30, 0.35)},
            "note": "normal approximation; exact paired-t is slightly larger",
        },
        "items": {f"{a}/{n}": dict(zip(("p", "lo", "hi"),
                                       wilson(s["ok"], s["n"]) or (None,) * 3),
                                   n=s["n"])
                  for (a, n), s in sorted(items.items())},
        "min_n_for_ci": MIN_N_FOR_CI,
    }


def pc(x):
    return "  n/a " if x is None else f"{100 * x:5.1f}%"


def report(a):
    L = []
    w = L.append
    w("=" * 70)
    w("RZ / Interlingua cloze micro-study")
    w("scored by hand, blind to condition; this tool did not judge answers")
    w("=" * 70)
    w(f"Submitted {a['n_submitted']}   analysed {a['n_analysed']}")
    for k, v in a["exclusions"].items():
        w(f"  excluded, {k}: {v}")
    w("")
    w("PRIMARY — zero-study comprehension, by arm")
    for arm, d in a["arms"].items():
        ci = (f"  95% CI [{pc(d['lo'])}, {pc(d['hi'])}]" if d.get("lo") is not None
              else f"  (CI not estimable, n<{a['min_n_for_ci']} or no variance)")
        w(f"  {arm:<12}{pc(d['mean'])}{ci}   n={d['n']}")
    w("")
    w("  by arm and first language")
    for k, d in a["by_arm_l1"].items():
        ci = (f" [{pc(d['lo'])}, {pc(d['hi'])}]" if d.get("lo") is not None
              else "  (CI not estimable)")
        w(f"    {k:<10} {pc(d['mean'])}{ci}  n={d['n']}")
    w("")
    w("  gist pass rate, by arm / passage / L1")
    for k, d in a["gist"].items():
        w(f"    {k:<14} {pc(d['pass'])}  n={d['n']}")
    w("")
    w("SECONDARY — RZ minus Interlingua (EXPLORATORY, UNDERPOWERED)")
    p = a["paired"]
    if p.get("lo") is not None:
        w(f"  observed {100 * p['mean']:+.1f} points"
          f"   95% CI [{100 * p['lo']:+.1f}, {100 * p['hi']:+.1f}]  n={p['n']}")
    else:
        w(f"  observed {100 * p['mean']:+.1f} points   CI not estimable  n={p['n']}")
    if a["mde"] is not None:
        s = a["mde_assumptions"]
        w(f"  minimum detectable effect ~{100 * a['mde']:.0f} points, assuming a"
          f" paired-difference SD of {s['sd_paired_difference_assumed']}")
        w("  sensitivity: " + ", ".join(
            f"SD {k} -> {100 * v:.0f}pt" for k, v in s["sensitivity"].items()))
    w(f"  VERDICT: {a['verdict']}")
    w("")
    w("PER-ITEM, by arm — a design signal, not an outcome")
    w("  arm/item  correct   95% CI                n")
    for k, d in a["items"].items():
        if d["p"] is None:
            continue
        flag = "  <-- most miss this" if d["p"] < 0.34 and d["n"] >= 5 else ""
        w(f"  {k:>9}  {pc(d['p'])}   [{pc(d['lo'])}, {pc(d['hi'])}]   {d['n']:>3}{flag}")
    w("")
    w("An item most participants miss is a lexicon bug; an item one L1")
    w("misses is a weighting bug (compare the per-arm/L1 cells above).")
    return "\n".join(L)


# --------------------------------------------------------------------
# tests — adversarial, not self-consistent
# --------------------------------------------------------------------

def selftest():
    import io
    import os
    import tempfile
    fails = []

    def check(name, cond):
        print(("  ok   " if cond else "  FAIL ") + name)
        if not cond:
            fails.append(name)

    print("statistics")
    p, lo, hi = wilson(8, 10)
    check("wilson(8,10) centre in (.55,.95)", 0.55 < p < 0.95 and lo < p < hi)
    check("wilson(0,0) is None", wilson(0, 0) is None)
    check("bootstrap: no variance -> no interval",
          bootstrap_mean([0.5] * 20)[1] is None)
    check("bootstrap: tiny n -> no interval",
          bootstrap_mean([0.1, 0.9, 0.5])[1] is None)
    check("bootstrap: real sample -> interval",
          bootstrap_mean([i / 20 for i in range(20)])[1] is not None)
    m25 = mde_paired(25)
    check(f"mde(25)~14pt (got {100 * m25:.1f})", 13.0 < 100 * m25 < 15.0)
    check("mde honours power", mde_paired(25, power=0.95) > m25)
    check("mde(1) is None", mde_paired(1) is None)

    print("suggestions are exact-match only (the old prefix bug)")
    for item, bad in ((2, "mantener"), (32, "decree"), (35, "clarinet"),
                      (30, "investigate"), (33, "per capita")):
        check(f"item {item}: {bad!r} not suggested", suggest(bad, item) == "")
    check("item 3: 'retirar' IS suggested", suggest("retirar", 3) == "likely")
    check("accents ignored: 'astăzi'", suggest("astăzi", 26) == "likely")

    def make(rows_over=None, n=12):
        rows = []
        for k in range(n):
            rz_first = k % 2 == 0
            rows.append({
                COL_PID: f"p{k}", COL_L1: ["Spanish", "Portuguese", "Italian", "French"][k % 4],
                COL_CONLANG: "no", COL_DURATION: "240",
                COL_COND["A"]: "RZ" if rz_first else "IA",
                COL_COND["D"]: "IA" if rz_first else "RZ",
                COL_GIST["A"]: "1", COL_GIST["D"]: "1",
                **{item_col(n_): "x" for n_ in ALL_ITEMS}})
        for r in rows:
            r.update(rows_over or {})
        return rows

    def write(rows, path):
        with open(path, "w", newline="", encoding="utf-8") as f:
            wr = csv.DictWriter(f, fieldnames=REQUIRED)
            wr.writeheader()
            wr.writerows(rows)

    tmp = tempfile.mkdtemp()
    raw = os.path.join(tmp, "raw.csv")

    print("schema validation is fatal")
    write(make(), raw)
    check("valid file loads", len(read_raw(raw)) == 12)

    bad = make()
    bad[0][COL_COND["D"]] = "RZ"
    write(bad, raw)
    try:
        read_raw(raw); check("both-arms-RZ rejected", False)
    except DataError as e:
        check("both-arms-RZ rejected", "exactly one RZ and one IA" in str(e))

    bad = make()
    bad[0][COL_COND["A"]] = "Trial A"
    write(bad, raw)
    try:
        read_raw(raw); check("unknown condition rejected", False)
    except DataError:
        check("unknown condition rejected", True)

    bad = make()
    bad[1][COL_PID] = bad[0][COL_PID]
    write(bad, raw)
    try:
        read_raw(raw); check("duplicate participant rejected", False)
    except DataError:
        check("duplicate participant rejected", True)

    with open(raw, "w", encoding="utf-8") as f:
        f.write(",".join(REQUIRED[:-1]) + "\n")
    try:
        read_raw(raw); check("missing item column rejected", False)
    except DataError as e:
        check("missing item column rejected", "missing required columns" in str(e))

    print("exclusion metadata is fatal, never silently included")
    for field, value, label in ((COL_DURATION, "", "empty duration"),
                                (COL_DURATION, "n/a", "nonnumeric duration"),
                                (COL_CONLANG, "maybe", "unparseable conlang answer")):
        rows = make({field: value})
        write(rows, raw)
        blind = os.path.join(tmp, "b.csv")
        export_blind(read_raw(raw), blind)
        sc = {f"p{k}::{n}": True for k in range(12) for n in ALL_ITEMS}
        try:
            analyse(read_raw(raw), sc); check(f"{label} rejected", False)
        except DataError:
            check(f"{label} rejected", True)
    check("mm:ss duration parses", parse_duration("4:00", "p") == 240)

    print("blinded export leaks no condition")
    write(make(), raw)
    blind = os.path.join(tmp, "blind.csv")
    n = export_blind(read_raw(raw), blind)
    text = open(blind, encoding="utf-8").read()
    hdr = next(csv.reader(io.StringIO(text)))
    check("one row per participant-item", n == 12 * 20)
    check("no condition column", not any("condition" in h for h in hdr))
    check("no arm value anywhere", " RZ" not in text and ",RZ" not in text)
    check("correct column is empty for the human", all(
        r["correct"] == "" for r in csv.DictReader(io.StringIO(text))))

    print("unscored responses are fatal")
    try:
        read_scores(blind); check("blank scores rejected", False)
    except DataError as e:
        check("blank scores rejected", "unscored" in str(e))

    print("analysis")
    rows = read_raw(raw)
    sc = {}
    for k in range(12):
        for n_ in ALL_ITEMS:
            sc[f"p{k}::{n_}"] = (n_ + k) % 5 != 0        # ~80%, varied
    a = analyse(rows, sc)
    check("all 12 analysed", a["n_analysed"] == 12)
    check("both arms present", set(a["arms"]) == {"RZ", "IA"})
    check("paired n == participants", a["paired"]["n"] == 12)
    check("per-item split by arm", any(k.startswith("RZ/") for k in a["items"])
          and any(k.startswith("IA/") for k in a["items"]))
    check("L1 canonicalised", all(k.split("/")[1] in ("ES", "PT", "IT", "FR", "RO", "other")
                                  for k in a["by_arm_l1"]))
    check("verdict present in the analysis object", bool(a["verdict"]))
    check("json is strict (no NaN)", "NaN" not in json.dumps(a, allow_nan=False))

    sc_equal = {f"p{k}::{n_}": True for k in range(12) for n_ in ALL_ITEMS}
    a2 = analyse(rows, sc_equal)
    check("identical arms -> no zero-width CI", a2["paired"].get("lo") is None)
    check("identical arms -> inconclusive", a2["inconclusive"])

    print("\n" + ("SELFTEST FAILED: " + "; ".join(fails) if fails else "selftest OK"))
    return 1 if fails else 0


# --------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    e = sub.add_parser("export-blind", help="stage 1: responses for a human scorer")
    e.add_argument("raw")
    e.add_argument("-o", "--out", required=True)
    n = sub.add_parser("analyse", help="stage 3: join the human scores and report")
    n.add_argument("raw")
    n.add_argument("scored")
    n.add_argument("--json", action="store_true")
    sub.add_parser("selftest")
    args = ap.parse_args()

    try:
        if args.cmd == "selftest":
            return selftest()
        if args.cmd == "export-blind":
            k = export_blind(read_raw(args.raw), args.out)
            print(f"wrote {args.out}: {k} responses, shuffled, condition "
                  f"stripped.\nFill the `correct` column with 0/1 by hand, "
                  f"then run:\n  python3 {sys.argv[0]} analyse {args.raw} {args.out}")
            return 0
        a = analyse(read_raw(args.raw), read_scores(args.scored))
        print(json.dumps(a, indent=2, allow_nan=False) if args.json else report(a))
        return 0
    except DataError as ex:
        print(f"REFUSING TO REPORT — {ex}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
