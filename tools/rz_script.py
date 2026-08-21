#!/usr/bin/env python3
"""RZ featural display script — tape-out v0 (stdlib SVG).

The secondary-layer script for Romance Zonal (design:
docs/design/zonal/rz-script-adaptation.md; Latin stays primary).
Wide-model instantiation of the greenfield feature grammar:

- greenfield-shared phonemes keep their greenfield letterforms
  (p | , t X, k nested-angle, m slashed-O, n wide-||, s wide-//,
  l corner, ts ring — transfer learning is free);
- new letters fill free grid cells: f capped-ring, r capped-|,
  dZ crossed-| , J~ (ny) crossed-tick, L~ (ly) capped-tick;
- voicing = full-width GROUND BAR under the onset (b d g v z);
- onset clusters: main letter (mutually shrunk, Hangul-style) +
  scaled satellites above: s- top-left, liquid top-right — temporal
  reading order preserved, and the satellite band never collides
  with the voicing ground bar;
- nucleus: one carrier per vowel; diphthongs = two thin carriers,
  temporal order left-to-right;
- coda strip: n bar / s double bar / l down-hook / r up-tick;
- suffix logograms (the RZ grammar channel gets dedicated ink):
  -mente -cion -itate -abile rendered as half-width logogram blocks,
  plus TENSE logograms -va (left arrow: past) and -ria (fork:
  conditional), fired by a lexicon-derived verb-stem set (parlava
  segments, materia does not). Plural -s is just the coda strip.
- h letterform (tick doubled, greenfield transfer): [h] is silent in
  RZ words but PRONOUNCED in mode-frame particles (rz-number-mode.md)
  — `hu` renders with ink, `hotel` does not;
- R-scheme POS underlines (optional, pos=True): verb = full underbar,
  adjective = leading half-bar, noun/other = bare. Auto-fired from
  morphology (tense, known infinitives) or explicit `word:v` /
  `word:adj` tags. This is the GZ R-scheme prototype (script-only
  POS channel, gz-sketch.md).

No check channel. Layout: horizontal, headstroke-free (accompanies
Latin text). Usage:
  python3 tools/rz_script.py word WORD [WORD...]
  python3 tools/rz_script.py sentence "TEXT"
  python3 tools/rz_script.py specimen [--out PATH]
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

BLOCK = 100
STROKE = 5

CX, CY, CR = 33, 30, 17            # ring base (raised: ground bar below)
VX = 33
ZY0, ZY1 = 10, 50                  # base vertical extent (shortened)
GROUND_Y = 58                      # voicing ground bar
CARRIER_X, CARRIER_Y0, CARRIER_Y1 = 74, 10, 60
TICK_LEN = 12
HEIGHT_Y = {"high": 17, "mid": 34, "low": 52}
STRIP_Y0, STRIP_Y1 = 72, 94
STRIP_X0, STRIP_X1 = 12, 88

# phoneme -> (base, modifier, voiced)
RZ_ONSETS = {
    "p": ("vertical", "plain", False),  "b": ("vertical", "plain", True),
    "t": ("diagonal", "crossed", False), "d": ("diagonal", "crossed", True),
    "k": ("angle", "doubled", False),   "g": ("angle", "doubled", True),
    "f": ("circle", "capped", False),   "v": ("circle", "capped", True),
    "s": ("diagonal", "doubled", False), "z": ("diagonal", "doubled", True),
    "ts": ("circle", "plain", False),
    "dZ": ("vertical", "crossed", True),   # soft g; voiced by nature
    "m": ("circle", "crossed", False),
    "n": ("vertical", "doubled", False),
    "ny": ("tick", "crossed", False),
    "l": ("angle", "plain", False),
    "ly": ("tick", "capped", False),
    "r": ("vertical", "capped", False),
    "h": ("tick", "doubled", False),   # mode frames only (greenfield form)
}
VOWELS = {"a": ("low", "central"), "e": ("mid", "front"),
          "i": ("high", "front"), "o": ("mid", "back"),
          "u": ("high", "back")}
CODAS = ("l", "n", "r", "s")
LIQUIDS = ("l", "r")

SUFFIX_LOGOGRAMS = ("mente", "cion", "itate", "abile")
TENSE_LOGOGRAMS = ("va", "ria")        # past, conditional — verb-gated
MODE_PARTICLES = {"hu"}                # pronounced-h frame words
POS_Y = 101                            # R-scheme underline baseline

# suppletive verb forms (rz-grammar §4: the 3 irregulars) that carry
# POS but no strippable tense suffix
SUPPLETIVE_VERBS = {"es", "era", "seria", "va", "sta", "stava"}

# function-word logograms: quarter-width marks for the highest-
# frequency grammatical words (~40-50% of running tokens). Shapes are
# v0: simple, distinct, echoing related letters where natural.
FUNC_W = 42
FUNC_MARKS = {
    # word: list of (kind, args) with kind in {line, circle}
    "le":  [("line", (10, 34, 32, 34))],                      # single bar
    "les": [("line", (10, 28, 32, 28)), ("line", (10, 40, 32, 40))],
    "de":  [("line", (10, 44, 32, 22))],                      # rising diag
    "del": [("line", (10, 44, 32, 22)), ("line", (10, 52, 32, 52))],
    "a":   [("line", (21, 20, 21, 46)), ("line", (12, 46, 30, 46))],
    "al":  [("line", (21, 20, 21, 46)), ("line", (12, 46, 30, 46)),
            ("line", (12, 54, 30, 54))],
    "e":   [("line", (21, 22, 21, 46))],                      # single stroke
    "o":   [("circle", (21, 34, 9))],
    "que": [("circle", (21, 30, 9)), ("line", (21, 39, 21, 52))],
    "no":  [("line", (12, 24, 30, 44)), ("line", (12, 44, 30, 24))],
    "un":  [("line", (12, 34, 30, 34)), ("line", (21, 26, 21, 42))],
    "con": [("line", (30, 22, 14, 22)), ("line", (14, 22, 14, 46)),
            ("line", (14, 46, 30, 46))],
    "en":  [("line", (12, 26, 30, 26)), ("line", (12, 36, 26, 36)),
            ("line", (12, 46, 30, 46))],
    "se":  [("line", (10, 46, 26, 26)), ("line", (18, 50, 34, 30))],
    "su":  [("line", (10, 46, 26, 26)), ("line", (26, 26, 26, 44))],
    "por": [("line", (14, 22, 14, 48)), ("circle", (22, 29, 8))],
}


def _el(name, **attrs):
    a = " ".join(f'{k.replace("_", "-")}="{v}"' for k, v in attrs.items())
    return f"<{name} {a}/>"


def _line(x1, y1, x2, y2, w=STROKE):
    return _el("line", x1=x1, y1=y1, x2=x2, y2=y2,
               stroke="currentColor", stroke_width=w, stroke_linecap="round")


def _circle(cx, cy, r, w=STROKE):
    return _el("circle", cx=cx, cy=cy, r=r, stroke="currentColor",
               stroke_width=w, fill="none")


def letter(base, mod, scale=1.0, dx=0.0, dy=0.0):
    """One onset letterform (RZ grid cells only)."""
    s = scale
    w = STROKE * s

    def L(x1, y1, x2, y2):
        return _line(dx + x1 * s, dy + y1 * s, dx + x2 * s, dy + y2 * s, w=w)

    p = []
    if base == "circle":
        p.append(_circle(dx + CX * s, dy + CY * s, CR * s, w=w))
        if mod == "crossed":               # m: slash protrudes past the
            p.append(L(15, 48, 51, 12))    # ring (ts/m raster fix)
        elif mod == "capped":
            p.append(L(12, 9, 54, 9))
    elif base == "vertical":
        if mod == "doubled":
            p += [L(24, ZY0, 24, ZY1), L(44, ZY0, 44, ZY1)]
        else:
            p.append(L(VX, ZY0, VX, ZY1))
            if mod == "crossed":           # full-width cross (b/dZ fix)
                p.append(L(14, 30, 52, 30))
            elif mod == "capped":
                p.append(L(16, ZY0, 50, ZY0))
    elif base == "diagonal":
        if mod == "doubled":
            p += [L(8, ZY1, 44, ZY0), L(24, ZY1, 60, ZY0)]
        else:
            p.append(L(14, ZY1, 52, ZY0))
            if mod == "crossed":
                p.append(L(14, ZY0, 52, ZY1))
    elif base == "angle":
        p += [L(14, ZY0, 52, ZY0), L(14, ZY0, 14, ZY1)]
        if mod == "doubled":
            p += [L(30, 26, 52, 26), L(30, 26, 30, ZY1)]
    elif base == "tick":
        if mod == "doubled":               # h: two equal close bars
            p += [L(20, 28, 46, 28), L(20, 40, 46, 40)]
        else:
            p.append(L(20, 30, 46, 30))
            if mod == "crossed":
                p.append(L(33, 18, 33, 42))
            elif mod == "capped":          # ly: cap wider + higher than
                p.append(L(14, 12, 52, 12))  # the main bar (vs h's twins)
    return p


def onset_parts(phonemes, dx=0.0, dy=0.0):
    """Onset cluster split into (main_letter_parts, satellite_parts):
    (s-)? main (liquid)? with mutual sizing. Split exposed so the
    no-collision test measures exactly what the renderer draws."""
    sats_pre = [ph for ph in phonemes[:-1] if ph == "s"] \
        if len(phonemes) > 1 else []
    liquid = [phonemes[-1]] if len(phonemes) > 1 and \
        phonemes[-1] in LIQUIDS else []
    main = [ph for ph in phonemes if ph not in
            (sats_pre[:1] if sats_pre else []) or ph != "s"]
    # resolve main: the one phoneme that's neither the s-prefix nor
    # the trailing liquid
    core = list(phonemes)
    if sats_pre:
        core.remove("s")
    if liquid and core[-1] in LIQUIDS and len(core) > 1:
        core = core[:-1]
    if len(core) != 1:
        raise ValueError(f"unrenderable onset cluster {phonemes}")
    b, mod, voiced = RZ_ONSETS[core[0]]
    # Hangul-style mutual sizing: main letter yields room to satellites
    if sats_pre or liquid:
        main = letter(b, mod, scale=0.82, dx=dx + 5, dy=dy + 5)
    else:
        main = letter(b, mod, dx=dx, dy=dy)
    if voiced:
        main.append(_line(dx + 6, dy + GROUND_Y, dx + 60, dy + GROUND_Y,
                          w=8))
    sats = []
    if sats_pre:
        sb, sm, _ = RZ_ONSETS["s"]
        sats += letter(sb, sm, scale=0.40, dx=dx + 0, dy=dy - 8)
    if liquid:
        lb, lm, _ = RZ_ONSETS[liquid[0]]
        sats += letter(lb, lm, scale=0.40, dx=dx + 46, dy=dy - 10)
    return main, sats


def onset_glyph(phonemes, dx=0.0, dy=0.0):
    """Onset cluster: (s-)? main (liquid)? with scaled satellites."""
    main, sats = onset_parts(phonemes, dx=dx, dy=dy)
    return main + sats


def nucleus_glyph(vowels, dx=0.0, dy=0.0):
    """1 vowel = full carrier; diphthong = two thin carriers L->R."""
    parts = []
    n = len(vowels)
    xs = [CARRIER_X] if n == 1 else [CARRIER_X - 7, CARRIER_X + 7]
    w = STROKE if n == 1 else 3.4
    tick = TICK_LEN if n == 1 else 8
    for v, x in zip(vowels, xs):
        h, b = VOWELS[v]
        parts.append(_line(dx + x, dy + CARRIER_Y0, dx + x,
                           dy + CARRIER_Y1, w=w))
        ty = dy + HEIGHT_Y[h]
        if b in ("front", "central"):
            parts.append(_line(dx + x - tick, ty, dx + x, ty, w=w))
        if b in ("back", "central"):
            parts.append(_line(dx + x, ty, dx + x + tick, ty, w=w))
    return parts


def coda_glyph(coda, dx=0.0, dy=0.0):
    def L(x1, y1, x2, y2):
        return _line(dx + x1, dy + y1, dx + x2, dy + y2)
    if not coda:
        return []
    if coda == "n":
        return [L(STRIP_X0, 83, STRIP_X1, 83)]
    if coda == "s":
        return [L(STRIP_X0, 78, STRIP_X1, 78), L(STRIP_X0, 88, STRIP_X1, 88)]
    if coda == "l":
        return [L(STRIP_X0, 80, 80, 80), L(80, 80, 80, 88)]
    if coda == "r":
        return [L(STRIP_X0, 86, 80, 86), L(80, 86, 80, 78)]
    # marginal coda (x-words, learned borrowings): mini letterform
    b, m, voiced = RZ_ONSETS[coda]
    parts = letter(b, m, scale=0.32, dx=dx + 26, dy=dy + STRIP_Y0)
    if voiced:
        parts.append(_line(dx + 26 + 12 * 0.32, dy + STRIP_Y0 + GROUND_Y * 0.32,
                           dx + 26 + 54 * 0.32, dy + STRIP_Y0 + GROUND_Y * 0.32,
                           w=STROKE * 0.32))
    return parts


def logogram(suffix, dx=0.0, dy=0.0):
    """Half-width (50u) suffix logogram block. v0 shapes; style pass
    pending."""
    def L(x1, y1, x2, y2, w=STROKE):
        return _line(dx + x1, dy + y1, dx + x2, dy + y2, w=w)
    if suffix == "mente":                       # zigzag wave
        return [L(8, 40, 20, 24), L(20, 24, 32, 40), L(32, 40, 44, 24)]
    if suffix == "cion":                        # ring + descender
        return [_circle(dx + 25, dy + 24, 12), L(25, 36, 25, 60)]
    if suffix == "itate":                       # double-crossed descender
        return [L(25, 14, 25, 58), L(14, 26, 36, 26), L(14, 42, 36, 42)]
        # (v0 ring+descender+foot collapsed with -cion at 7px raster —
        #  0.000 phase-min; review finding, fixed 2026-08-22)
    if suffix == "abile":                       # peak + underbar
        return [L(10, 44, 25, 20), L(25, 20, 40, 44), L(10, 56, 40, 56)]
    if suffix == "va":                          # tense: past = left arrow
        return [L(42, 34, 10, 34), L(10, 34, 22, 22), L(10, 34, 22, 46)]
    if suffix == "ria":                         # tense: conditional = fork
        return [L(25, 58, 25, 32), L(25, 32, 11, 16), L(25, 32, 39, 16)]
    raise ValueError(suffix)


# --- orthography -> phonemes -> syllables --------------------------------

def to_phonemes(word, keep_h=None):
    """RZ spelling to phoneme list (rz-grammar.md §1 rules).

    keep_h: pronounce h (mode-frame particles). Default: True exactly
    for words in MODE_PARTICLES — RZ's own words have silent h; frame
    particles are the one pronounced-[h] class (rz-number-mode.md)."""
    w = word.lower()
    if keep_h is None:
        keep_h = w in MODE_PARTICLES
    out = []
    i = 0
    while i < len(w):
        c = w[i]
        nxt = w[i + 1] if i + 1 < len(w) else ""
        if c == "q" and nxt == "u":
            out.append("k"); i += 2; continue
        if c == "c":
            out.append("ts" if nxt and nxt in "ei" else "k"); i += 1; continue
        if c == "g":
            out.append("dZ" if nxt and nxt in "ei" else "g"); i += 1; continue
        if c == "z":
            out.append("ts"); i += 1; continue
        prev_v = i > 0 and w[i - 1] in "aeiou"
        if c == "n" and nxt == "i" and prev_v and i + 2 < len(w) \
                and w[i + 2] in "aeiou":
            out.append("ny"); i += 2; continue
        if c == "l" and nxt == "i" and prev_v and i + 2 < len(w) \
                and w[i + 2] in "aeiou":
            out.append("ly"); i += 2; continue
        if c == "h":
            if keep_h:
                out.append("h"); i += 1; continue
            i += 1; continue                    # silent: THE one spelling
            # exception (rz-grammar §1) — Romance keeps written h
        if c == "-":
            i += 1; continue                    # compound-number hyphen
        if c in "aeiou" or c in RZ_ONSETS or c in "bdgv":
            out.append(c); i += 1; continue
        if c == "j":
            out.append("dZ"); i += 1; continue
        if c == "x":
            out += ["k", "s"]; i += 1; continue
        raise ValueError(f"unspellable {c!r} in {word!r}")
    return out


LEGAL_ONSETS = set()
for _c in RZ_ONSETS:
    LEGAL_ONSETS.add((_c,))
    if _c not in ("s",):
        for _liq in LIQUIDS:
            if _c not in LIQUIDS + ("n", "m", "ny", "ly", "ts", "dZ",
                                    "z", "h"):
                LEGAL_ONSETS.add((_c, _liq))
for _c in ("p", "t", "k", "m", "n", "f"):
    LEGAL_ONSETS.add(("s", _c))
    for _liq in LIQUIDS:
        if _c in ("p", "t", "k"):
            LEGAL_ONSETS.add(("s", _c, _liq))


def syllabify(phonemes):
    """Onset-maximal; codas restricted to l n r s."""
    sylls = []
    i = 0
    n = len(phonemes)
    while i < n:
        onset = []
        j = i
        while j < n and phonemes[j] not in VOWELS:
            onset.append(phonemes[j]); j += 1
        if j == n:
            # word-final consonants: fold into previous coda if legal
            if sylls and len(onset) == 1 and onset[0] in CODAS:
                sylls[-1] = (sylls[-1][0], sylls[-1][1], onset[0])
                return sylls
            raise ValueError(f"cannot end word with {onset}")
        nucleus = [phonemes[j]]; j += 1
        if j < n and phonemes[j] in VOWELS:
            nucleus.append(phonemes[j]); j += 1
        # decide coda: take one consonant if the rest still starts legally
        coda = ""
        if j < n and phonemes[j] not in VOWELS:
            rest = []
            k = j
            while k < n and phonemes[k] not in VOWELS:
                rest.append(phonemes[k]); k += 1
            if k == n:                          # word-final cluster
                if len(rest) == 1:
                    coda = rest[0]; j += 1      # marginal codas allowed
            else:
                # leave the longest legal onset for the next syllable;
                # prefer canonical codas, allow marginal ones (x-words)
                if tuple(rest) in LEGAL_ONSETS:
                    pass                        # take = 0
                elif tuple(rest[1:]) in LEGAL_ONSETS:
                    coda = rest[0]; j += 1
                else:
                    raise ValueError(f"unsyllabifiable cluster {rest}")
        if tuple(onset) not in LEGAL_ONSETS and onset:
            raise ValueError(f"illegal onset {onset}")
        sylls.append((tuple(onset) if onset else (), nucleus, coda))
        i = j
    return sylls


# --- morphology (verb-stem set drives -va/-ria segmentation) -------------

_VERB_STEMS = None


def verb_stems():
    """Present-form verb stems, extracted from the lexicon docs
    (infinitives in -ar/-er/-ir inside backtick spans, minus final r).
    Lazy; falls back to a core set if the docs aren't reachable."""
    global _VERB_STEMS
    if _VERB_STEMS is not None:
        return _VERB_STEMS
    stems = {"parla", "vive", "veni", "parti", "dispute", "disputa",
             "compra", "vide", "comprende", "sabe", "lege", "crea"}
    base = Path(__file__).resolve().parent.parent / "docs" / "design"
    for rel in ("zonal/rz-lexicon.md", "zonal/core-conversational.md",
                "zonal/rz-grammar.md"):
        try:
            text = (base / rel).read_text()
        except OSError:
            continue
        for span in re.findall(r"`([^`]+)`", text):
            # spans mix RZ words with English glosses in parens and
            # FLAG notes — strip those before harvesting infinitives
            span = re.sub(r"\([^)]*\)", " ", span)
            span = re.split(r"FLAG|—|;", span)[0]
            for tok in re.findall(r"[a-z]+", span.lower()):
                if len(tok) > 3 and tok.endswith(("ar", "er", "ir")):
                    stems.add(tok[:-1])
    _VERB_STEMS = stems
    return stems


def analyze(word):
    """(stem, tense_suffix_or_None, pos_or_None) for a plain word.

    Tense fires only when stripping the suffix leaves a known verb
    stem — `parlava` segments (parla is a verb), `materia` does not
    (mate isn't). Suppletives (era, seria, …) tag verb, render plain.
    POS: 'v' when verbal morphology is certain, else None (explicit
    `word:pos` input tags cover the rest — R-scheme prototype)."""
    wl = word.lower()
    if wl in SUPPLETIVE_VERBS:
        return wl, None, "v"
    stems = verb_stems()
    for suf in TENSE_LOGOGRAMS:
        stem = wl[: -len(suf)]
        if wl.endswith(suf) and stem in stems:
            return stem, suf, "v"
    if wl.endswith(("ar", "er", "ir")) and wl[:-1] in stems:
        return wl, None, "v"                   # infinitive
    return wl, None, None


# --- assembly ------------------------------------------------------------

def syllable_block(syl, dx=0.0, dy=0.0):
    onset, nucleus, coda = syl
    parts = []
    if onset:
        parts += onset_glyph(list(onset), dx=dx, dy=dy)
    parts += nucleus_glyph(nucleus, dx=dx, dy=dy)
    parts += coda_glyph(coda, dx=dx, dy=dy)
    return parts


def block_width(syl):
    """Proportional widths: open CV blocks with simple onsets narrow."""
    onset, nucleus, coda = syl
    if not coda and len(nucleus) == 1 and len(onset) <= 1:
        return 80
    return BLOCK


def word_glyph(word, dx=0.0, dy=0.0, dense=True, pos=False):
    """Horizontal block row. With dense=True (default): function-word
    logograms, derivation- and tense-suffix logograms, proportional
    widths. With pos=True (R-scheme prototype): POS underlines — verb
    full underbar, adjective leading half-bar. POS comes from verbal
    morphology (analyze) or an explicit `word:v` / `word:adj` tag."""
    tag = None
    if ":" in word:
        word, tag = word.split(":", 1)
    wl = word.lower()
    parts = []
    if dense and wl in FUNC_MARKS:
        for kind, args in FUNC_MARKS[wl]:
            if kind == "line":
                x1, y1, x2, y2 = args
                parts.append(_line(dx + x1, dy + y1, dx + x2, dy + y2))
            else:
                cx, cy, r = args
                parts.append(_circle(dx + cx, dy + cy, r))
        return parts, FUNC_W
    stem, tense, auto_pos = analyze(word)
    suffix = None
    if not dense:
        stem, tense = wl, None
    elif tense is None:
        stem = wl
        for suf in SUFFIX_LOGOGRAMS:
            if wl.endswith(suf) and len(word) > len(suf) + 1:
                stem, suffix = wl[: -len(suf)], suf
                break
    sylls = syllabify(to_phonemes(stem))
    x = dx
    for syl in sylls:
        parts += syllable_block(syl, dx=x, dy=dy)
        x += block_width(syl) if dense else BLOCK
    if dense and tense:
        parts += logogram(tense, dx=x + 4, dy=dy + 14)
        x += 54
    elif suffix:
        parts += logogram(suffix, dx=x + 4, dy=dy + 14)
        x += 54
    width = x - dx
    if pos:
        p = (tag or auto_pos or "").lower()
        if p == "v":
            parts.append(_line(dx + 4, dy + POS_Y, dx + width - 4,
                               dy + POS_Y, w=3.5))
        elif p in ("adj", "a"):
            parts.append(_line(dx + 4, dy + POS_Y,
                               dx + 4 + 0.4 * width, dy + POS_Y, w=3.5))
    return parts, width


def sentence_glyphs(words, dy=0.0, dense=True, headstroke=False,
                    pos=False):
    """A sentence row. headstroke=True: words cohere under a top rule
    and abut with a minimal gap — no spaces needed (boundary = rule
    break); otherwise words are separated by spacing."""
    parts = []
    x = 0
    gap = 6 if headstroke else 24
    for w in words:
        pw, wid = word_glyph(w, dx=x, dy=dy, dense=dense, pos=pos)
        parts += pw
        if headstroke:
            parts.append(_line(x + 2, dy + 2, x + wid - 2, dy + 2, w=3.5))
        x += wid + gap
    return parts, x - gap


def svg(parts, w, h):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
            f'width="{w}" height="{h}" style="color:#1a1a1a">'
            + "".join(parts) + "</svg>")


def specimen():
    parts = []
    pad, y = 10, 10

    def label(x, ytxt, text):
        parts.append(f'<text x="{x}" y="{ytxt}" font-size="12" '
                     f'fill="currentColor" font-family="monospace">'
                     f'{text}</text>')

    # consonant letters
    x = pad
    for ph in RZ_ONSETS:
        parts += onset_glyph([ph], dx=x, dy=y)
        label(x + 20, y + 112, ph)
        x += 72
    y += 135
    # vowels + two diphthongs
    x = pad
    for v in VOWELS:
        parts += nucleus_glyph([v], dx=x - 40, dy=y)
        label(x + 28, y + 76, v)
        x += 72
    for dv in ("ai", "ue"):
        parts += nucleus_glyph(list(dv), dx=x - 40, dy=y)
        label(x + 24, y + 76, dv)
        x += 72
    y += 100
    # codas
    x = pad
    for c in CODAS:
        parts += coda_glyph(c, dx=x, dy=y - 60)
        label(x + 40, y + 40, f"-{c}")
        x += 110
    # logograms (derivational + tense)
    x += 30
    for suf in SUFFIX_LOGOGRAMS + TENSE_LOGOGRAMS:
        parts += logogram(suf, dx=x, dy=y - 55)
        label(x + 6, y + 40, f"-{suf}")
        x += 80
    y += 70
    # sample words
    for w in ("parlar", "nacion", "rapidemente", "stacion", "proxime",
              "fromage", "veritate", "governo"):
        parts_w, wid = word_glyph(w, dx=pad, dy=y)
        parts += parts_w
        label(pad + wid + 14, y + 60, w)
        y += 118
    # first fable clause (with the tense logogram now firing on
    # disputava)
    x = pad
    for w in "le vento del norte e le sol disputava".split():
        pw, wid = word_glyph(w, dx=x, dy=y)
        parts += pw
        x += wid + 22
    label(pad, y + 122, "le vento del norte e le sol disputava")
    y += 145
    # R-scheme POS underlines (verb auto, adjective tagged)
    x = pad
    for w in "le viajator parlava de un manto:adj calde:adj".split():
        pw, wid = word_glyph(w, dx=x, dy=y, pos=True)
        parts += pw
        x += wid + 22
    label(pad, y + 126, "R-scheme: le viajator parlava de un "
          "manto[adj] calde[adj]")
    y += 150
    # number mode: hu opens, digit syllables follow (42 = hu ki)
    x = pad
    for w in "hu ki".split():
        pw, wid = word_glyph(w, dx=x, dy=y)
        parts += pw
        x += wid + 22
    label(pad, y + 122, "number mode: hu ki = 42 (pronounced h)")
    return svg(parts, 1450, y + 140)


def page(text, width=2200, dense=True, headstroke=False, pos=False,
         title=None):
    """Wrapped multi-line page of running text. Words that exceed the
    line width wrap; line pitch leaves room for POS underlines."""
    words = re.findall(r"[a-zA-Z-]+(?::[a-z]+)?", text)
    pitch = 128
    parts, x, y = [], 10, 10
    gap = 6 if headstroke else 24
    for w in words:
        pw, wid = word_glyph(w.strip("-"), dx=x, dy=y, dense=dense,
                             pos=pos)
        if x + wid > width - 10 and x > 10:
            x, y = 10, y + pitch
            pw, wid = word_glyph(w.strip("-"), dx=x, dy=y, dense=dense,
                                 pos=pos)
        parts += pw
        if headstroke:
            parts.append(_line(x + 2, y + 2, x + wid - 2, y + 2, w=3.5))
        x += wid + gap
    h = y + pitch + 10
    if title:
        parts.append(f'<text x="10" y="{h - 8}" font-size="13" '
                     f'fill="currentColor" font-family="monospace">'
                     f'{title}</text>')
        h += 16
    return svg(parts, width, h)


def main(argv=None):
    args = sys.argv[1:] if argv is None else argv
    if not args:
        print(__doc__, file=sys.stderr)
        return 2
    if args[0] == "word":
        all_parts, x = [], 0
        for w in args[1:]:
            pw, wid = word_glyph(w, dx=x)
            all_parts += pw
            x += wid + 22
        print(svg(all_parts, x, 130))
    elif args[0] == "sentence":
        all_parts, x = [], 0
        for w in re.findall(r"[a-zA-Z]+", args[1]):
            pw, wid = word_glyph(w, dx=x)
            all_parts += pw
            x += wid + 22
        print(svg(all_parts, x, 130))
    elif args[0] == "page":
        opts = {a.split("=")[0][2:]: a.split("=", 1)[1] if "=" in a
                else True for a in args[2:] if a.startswith("--")}
        text = Path(args[1]).read_text() if Path(args[1]).exists() \
            else args[1]
        s = page(text, headstroke=bool(opts.get("headstroke")),
                 pos=bool(opts.get("pos")),
                 title=opts.get("title"))
        out = opts.get("out")
        if out:
            Path(out).write_text(s)
            print(f"written: {out}")
        else:
            print(s)
    elif args[0] == "specimen":
        out = args[args.index("--out") + 1] if "--out" in args else None
        s = specimen()
        if out:
            Path(out).write_text(s)
            print(f"written: {out}")
        else:
            print(s)
    else:
        print(__doc__, file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
