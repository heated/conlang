#!/usr/bin/env python3
"""How far is RZ from its baseline, measured in running tokens?

paper §9b says the rule-level overlap with Interlingua is roughly
80-85% but that the TOKEN-level overlap is unmeasured — and that the
missing deltas concentrate in the closed class, which carries about
half of running text, so the token distance is probably larger than
the rule figure suggests.

This measures it on the only matched material that exists: the two
passages rendered in both languages for the cloze study
(docs/design/zonal/cloze-micro-study-packet.md §2), whose Interlingua
side has every visible word attested in running Interlingua prose.

What this is: a real token-level number on 2 passages of matched
content, ~120 aligned tokens.
What this is NOT: a corpus estimate. Both renderings are the project's
own, the sample is tiny, and the passages were chosen to EXERCISE the
deltas, which biases the distance upward. It replaces "unmeasured"
with "measured on this, with these limits" — no more.

Usage: python3 tools/profile_distance.py [--verbose]
"""

import re
import sys
import unicodedata
from collections import Counter

# The blanked slots are removed from both renderings, so alignment is
# over the visible words only -- which is also what a reader sees.
PASSAGES = {
    "A (fable)": (
        # RZ
        """Le vento del norte e le sol disputava sobre qui era le plus
        quando un viajator passava, coprite de un calde. Les dos accordava
        que le prime a facer le viajator su manto seria considerate le plus
        forte. Le vento del norte comenzava a con tote su forza, ma quanto
        plus el soplava, tanto plus le viajator se con su manto; e al le
        vento abandonava le tentativa. Alora le sol comenzava a caldemente
        e immediatamente le viajator su manto. E asi le vento del norte
        deveva que le sol era le plus de les dos.""",
        # Interlingua
        """Le vento del nord e le sol disputava super qui esseva le plus
        quando un viagiator passava, coperite de un calide. Illes accordava
        que le prime a facer le viagiator su mantello esserea considerate le
        plus forte. Le vento del nord comenciava a con tote su fortia, ma
        quanto plus ille sufflava, tanto plus le viagiator se con su mantello
        e al le vento abandonava le tentativa. Alora le sol comenciava a
        calidemente e immediatemente le viagiator su mantello. E assi le
        vento del nord debeva que le sol esseva le plus del duo."""),
    "D (news)": (
        """Le governo anunciava un nove programa de energia Le plan preve la
        construccion de centrales en le sud del durante les proximes cinco
        annos con un total de dos miliardes de euros. Segun le ministra de
        energia le programa va plus de cuatro mil postos de labor e va les
        emisiones de carbon en vinte per Les organizaciones ambientales
        reciveva le con optimismo prudente ma demandava plus sobre le
        calendario de construccion.""",
        """Le governamento annunciava un nove programma de energia Le plano
        previde le construction de centrales in le sud del durante le proxime
        cinque annos con un total de duo milliardos de euros. Secundo le
        ministro de energia le programma plus de quatro mille postos de
        travalio e le emissiones de carbon de vinti pro Le organisationes
        ambiental recipeva le con optimismo prudente ma demandava plus super
        le calendario de construction."""),
}


def toks(s):
    return re.findall(r"[a-zA-Zàáâãéêíóôõúüñç]+", s.lower())


def strip_accents(w):
    return "".join(c for c in unicodedata.normalize("NFD", w)
                   if unicodedata.category(c) != "Mn")


def lev(a, b):
    if a == b:
        return 0
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1,
                           prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


def sim(a, b):
    """0..1 word similarity, used to decide whether two tokens are a
    substitution of each other or genuinely unrelated."""
    if a == b:
        return 1.0
    d = lev(strip_accents(a), strip_accents(b))
    return max(0.0, 1.0 - d / max(len(a), len(b)))


def align(rz, ia):
    """Needleman-Wunsch with SUBSTITUTION allowed.

    A pure LCS alignment scores every changed word as a deletion plus
    an insertion, which reports `norte`/`nord` as two unaligned tokens
    rather than one substitution — and then claims 0% 'different word'
    while 53% is 'present in only one'. That is an artifact, not a
    finding, so substitution is a first-class operation here and is
    charged by dissimilarity.
    """
    n, m = len(rz), len(ia)
    GAP = -1.0
    dp = [[0.0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        dp[i][0] = dp[i - 1][0] + GAP
    for j in range(1, m + 1):
        dp[0][j] = dp[0][j - 1] + GAP
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            # substitution scores 2*sim-1, so identical=+1, unrelated=-1
            dp[i][j] = max(dp[i - 1][j - 1] + (2 * sim(rz[i - 1], ia[j - 1]) - 1),
                           dp[i - 1][j] + GAP,
                           dp[i][j - 1] + GAP)
    pairs, i, j = [], n, m
    while i > 0 and j > 0:
        if dp[i][j] == dp[i - 1][j - 1] + (2 * sim(rz[i - 1], ia[j - 1]) - 1):
            pairs.append((rz[i - 1], ia[j - 1])); i -= 1; j -= 1
        elif dp[i][j] == dp[i - 1][j] + GAP:
            pairs.append((rz[i - 1], None)); i -= 1
        else:
            pairs.append((None, ia[j - 1])); j -= 1
    while i > 0:
        pairs.append((rz[i - 1], None)); i -= 1
    while j > 0:
        pairs.append((None, ia[j - 1])); j -= 1
    return pairs[::-1]


def main():
    verbose = "--verbose" in sys.argv
    tot = Counter()
    diffs = []
    for name, (rz_s, ia_s) in PASSAGES.items():
        rz, ia = toks(rz_s), toks(ia_s)
        pairs = align(rz, ia)
        c = Counter()
        for a, b in pairs:
            if a is None or b is None:
                c["unaligned"] += 1
                diffs.append((name, a or "-", b or "-", "insert/delete"))
                continue
            c["aligned"] += 1
            if a == b:
                c["identical"] += 1
            elif strip_accents(a) == strip_accents(b):
                c["accent only"] += 1
            elif lev(a, b) == 1:
                c["one edit"] += 1
                diffs.append((name, a, b, "1 edit"))
            elif lev(a, b) <= 2:
                c["two edits"] += 1
                diffs.append((name, a, b, "2 edits"))
            else:
                c["different word"] += 1
                diffs.append((name, a, b, "different"))
        tot.update(c)
        n = c["aligned"] + c["unaligned"]
        print(f"{name}: {n} visible tokens, "
              f"{100*c['identical']/n:.0f}% identical, "
              f"{100*(c['identical']+c['accent only']+c['one edit'])/n:.0f}% "
              f"within one edit")

    n = tot["aligned"] + tot["unaligned"]
    ident = tot["identical"]
    near = tot["identical"] + tot["accent only"] + tot["one edit"]
    print("\n" + "=" * 62)
    print(f"{n} visible tokens of matched content, both renderings ours")
    print(f"  identical                  {ident:>4}  {100*ident/n:5.1f}%")
    print(f"  within one edit            {near:>4}  {100*near/n:5.1f}%")
    print(f"  different word entirely    {tot['different word']:>4}  "
          f"{100*tot['different word']/n:5.1f}%")
    print(f"  present in only one        {tot['unaligned']:>4}  "
          f"{100*tot['unaligned']/n:5.1f}%")
    print("=" * 62)
    print("Limits, which are severe: two passages, ~120 tokens, both")
    print("renderings written by this project, and the passages were")
    print("chosen to EXERCISE the deltas — so this is an upper bound on")
    print("distance, not a corpus estimate. It replaces 'unmeasured'")
    print("with 'measured on this', and nothing more.")
    if verbose:
        print("\nevery non-identical aligned pair:")
        for name, a, b, kind in diffs:
            print(f"  {name:<10} {a:<16} {b:<16} {kind}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
