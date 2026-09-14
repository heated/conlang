#!/usr/bin/env python3
"""Build docs/script-demo.html: RZ text paired word by word with the script.

Usage: python3 tools/build_script_demo.py

Two things this has to get right, both learned the hard way:

  * Every glyph renders at the SAME scale. rz_script.py emits a constant
    viewBox height (142), so sizing the SVG by HEIGHT gives a uniform
    scale everywhere. Sizing by width does not: it scales each SVG to
    its container, so a long sentence comes out small and a short word
    comes out huge, and a fixed-height box then clips it.
  * Vertical alignment is shared. Each word keeps its own horizontal
    extent but takes the union vertical extent of every word on the
    page, so baselines line up across words instead of each word being
    cropped to itself.
"""

import html
import os
import re
import subprocess
import sys
from pathlib import Path

os.chdir(Path(__file__).resolve().parent.parent)

GLYPH_H = 32          # px. A little larger than the Latin beside it, because
                      # the marks that tell script letters apart are small next
                      # to the letter. Not much larger: the point is to compare
                      # them, and an oversized script wins on nothing.
PAD = 4               # viewBox padding in source units


def render(word):
    out = subprocess.run([sys.executable, "tools/rz_script.py", "word", word],
                         capture_output=True, text=True)
    if out.returncode != 0:
        raise SystemExit(f"render failed for {word!r}:\n{out.stderr}")
    return out.stdout.strip()


def bbox(svg):
    """Ink bounds of an SVG made of <line> and <circle>, stroke included."""
    xs, ys = [], []
    for m in re.finditer(r'<line x1="([\d.-]+)" y1="([\d.-]+)" '
                         r'x2="([\d.-]+)" y2="([\d.-]+)"[^>]*?'
                         r'stroke-width="([\d.]+)"', svg):
        x1, y1, x2, y2, w = (float(g) for g in m.groups())
        xs += [min(x1, x2) - w / 2, max(x1, x2) + w / 2]
        ys += [min(y1, y2) - w / 2, max(y1, y2) + w / 2]
    for m in re.finditer(r'<circle cx="([\d.-]+)" cy="([\d.-]+)" r="([\d.]+)"'
                         r'[^>]*?stroke-width="([\d.]+)"', svg):
        cx, cy, r, w = (float(g) for g in m.groups())
        xs += [cx - r - w / 2, cx + r + w / 2]
        ys += [cy - r - w / 2, cy + r + w / 2]
    if not xs:
        return None
    return min(xs), min(ys), max(xs), max(ys)


def recrop(svg, y0, y1):
    """Tight horizontal crop, shared vertical extent, sized by height."""
    b = bbox(svg)
    if b is None:
        return svg
    x0, _, x1, _ = b
    w = (x1 - x0) + 2 * PAD
    h = (y1 - y0) + 2 * PAD
    svg = re.sub(r'viewBox="[^"]*"',
                 f'viewBox="{x0-PAD:.1f} {y0-PAD:.1f} {w:.1f} {h:.1f}"', svg, 1)
    svg = re.sub(r'\swidth="[\d.]+"\s*height="[\d.]+"',
                 f' height="{GLYPH_H}" width="{GLYPH_H*w/h:.1f}"', svg, 1)
    return svg.replace(' style="color:#1a1a1a"', '').replace('<svg ', '<svg class="rz" ')


WORD_RE = re.compile(r"[A-Za-zÀ-ÿ]+")


def pairs(text):
    """[(display token, svg or None)] preserving punctuation for display."""
    out = []
    for tok in text.split():
        m = WORD_RE.search(tok)
        out.append((tok, render(m.group(0)) if m else None))
    return out


# ------------------------------------------------------------------ content

LINES = [
    ("Le vento del norte e le sol disputava sobre qui era le plus forte.",
     "The north wind and the sun were arguing about which of them was stronger."),
    ("Un viajator passava, coprite de un manto calde.",
     "A traveller came by, wrapped in a warm cloak."),
]

DIALOGUE = [
    ("Bon dia! Cuante costa istes pomos?", "Good morning. How much are these apples?"),
    ("Dos euros le kilo.", "Two euros a kilo."),
    ("Alora io prende tres kilos.", "Then I will take three kilos."),
]

LETTERS = [("pa", "p"), ("ba", "b"), ("ta", "t"), ("da", "d")]
CODAS = [("pan", "n"), ("pas", "s"), ("pal", "l"), ("par", "r")]
GRAMMAR = [
    ("parla", "speaks", "plain verb, no suffix mark"),
    ("parlava", "was speaking", "past. The <b>-va</b> suffix is the arrow at the end."),
    ("parlaria", "would speak", "conditional. Same verb, fork instead of arrow."),
    ("rapidemente", "quickly", "<b>-mente</b> makes an adverb. It gets its own block."),
    ("construccion", "construction", "<b>-cion</b> makes a noun."),
]

# render everything, then compute one shared vertical extent
work = {}
for txt, _ in LINES + DIALOGUE:
    work[txt] = pairs(txt)
singles = {w: render(w) for w, *_ in LETTERS + CODAS + GRAMMAR}

allsvg = [s for ps in work.values() for _, s in ps if s] + list(singles.values())
boxes = [bbox(s) for s in allsvg]
Y0 = min(b[1] for b in boxes if b)
Y1 = max(b[3] for b in boxes if b)

work = {t: [(tok, recrop(s, Y0, Y1) if s else None) for tok, s in ps]
        for t, ps in work.items()}
singles = {w: recrop(s, Y0, Y1) for w, s in singles.items()}

# ------------------------------------------------------------------ page

CSS = f"""
:root{{
  --paper:#F7F7F5; --ink:#1B1D20; --soft:#585E66; --faint:#8A9098;
  --rule:#E2E4E0; --accent:#2244AA; --panel:#FFFFFF;
  --ochre:#8A5F28; --ochre-soft:#F5EEE2;
}}
@media (prefers-color-scheme: dark){{:root:not([data-theme="light"]){{
  --paper:#15171B; --ink:#E9EAE6; --soft:#A4ABB4; --faint:#767D86;
  --rule:#2A2F35; --accent:#8AA6F2; --panel:#1C1F25;
  --ochre:#C79A55; --ochre-soft:#292317;
}}}}
:root[data-theme="dark"]{{
  --paper:#15171B; --ink:#E9EAE6; --soft:#A4ABB4; --faint:#767D86;
  --rule:#2A2F35; --accent:#8AA6F2; --panel:#1C1F25;
  --ochre:#C79A55; --ochre-soft:#292317;
}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--paper);color:var(--ink);
  font-family:"IBM Plex Sans",system-ui,-apple-system,sans-serif;
  font-size:17px;line-height:1.6;-webkit-font-smoothing:antialiased}}
.wrap{{max-width:780px;margin:0 auto;padding:0 24px 90px}}
header.t{{padding:64px 0 30px;border-bottom:1px solid var(--rule)}}
.eyebrow{{font-family:"IBM Plex Mono",ui-monospace,monospace;font-size:11.5px;
  letter-spacing:.14em;text-transform:uppercase;color:var(--faint);margin-bottom:14px}}
h1{{font-family:Spectral,Georgia,serif;font-size:clamp(28px,4vw,38px);
  line-height:1.15;margin:0 0 16px;font-weight:600;letter-spacing:-.01em}}
.sub{{font-size:17px;color:var(--soft);line-height:1.55;max-width:62ch}}
h2{{font-size:19px;font-weight:600;margin:54px 0 6px;letter-spacing:-.005em}}
.h2note{{color:var(--soft);font-size:15.5px;margin:0 0 22px;max-width:62ch}}
p{{margin:0 0 16px}}
a{{color:var(--accent)}}

/* every glyph at one scale: height is fixed, width follows */
svg.rz{{display:block;color:var(--ink);overflow:visible}}

.sent{{border-bottom:1px solid var(--rule);padding:26px 0}}
.sent:last-of-type{{border-bottom:none}}
.words{{display:flex;flex-wrap:wrap;align-items:flex-end;
  gap:14px 18px;margin-bottom:16px}}
.wd{{display:flex;flex-direction:column;align-items:center;gap:3px}}
.wd .lat{{font-family:Spectral,Georgia,serif;font-size:20px;line-height:1.25;
  color:var(--ink);white-space:nowrap}}
.wd .sc{{height:{GLYPH_H}px;display:flex;align-items:flex-end}}
.gloss{{color:var(--faint);font-size:15px;margin:0}}
.sizenote{{font-size:14.5px;color:var(--faint);margin:0 0 22px;max-width:64ch}}

.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(190px,1fr));
  gap:16px;margin-bottom:8px}}
.card{{background:var(--panel);border:1px solid var(--rule);border-radius:3px;
  padding:16px;display:flex;flex-direction:column;gap:12px}}
.card .sc{{min-height:{GLYPH_H}px;display:flex;align-items:flex-end}}
.card .w{{font-family:Spectral,Georgia,serif;font-size:18px;font-weight:600}}
.card .g{{color:var(--faint);font-size:14px;margin-top:-8px}}
.card .n{{color:var(--soft);font-size:14px;line-height:1.45}}
.card .n b{{color:var(--ink);font-weight:600}}

.note{{border-left:2px solid var(--accent);padding-left:16px;color:var(--soft);
  font-size:15.5px;margin:26px 0}}
.note b{{color:var(--ink);font-weight:600}}
.status{{background:var(--ochre-soft);border-radius:3px;padding:18px 20px;
  font-size:15px;color:var(--soft);margin:34px 0 0}}
.status b{{color:var(--ochre)}}
.status ul{{margin:8px 0 0;padding-left:20px}}
.status li{{margin-bottom:5px}}
footer{{border-top:1px solid var(--rule);margin-top:54px;padding-top:24px;
  font-size:15px;color:var(--soft)}}
footer a{{margin-right:20px}}
"""


def sentence_block(txt, gloss):
    ws = "".join(
        f'<div class="wd"><div class="lat">{html.escape(tok)}</div>'
        f'<div class="sc">{s or ""}</div></div>'
        for tok, s in work[txt])
    return (f'<div class="sent"><div class="words">{ws}</div>'
            f'<p class="gloss">{html.escape(gloss)}</p></div>')


def card(w, title, note):
    return (f'<div class="card"><div class="sc">{singles[w]}</div>'
            f'<div><div class="w">{html.escape(w)}</div>'
            f'<div class="g">{title}</div></div>'
            f'<div class="n">{note}</div></div>')


B = []
a = B.append

a('<header class="t"><div class="eyebrow">RZ, a Romance zonal language</div>')
a('<h1>RZ and its script</h1>')
a('<p class="sub">RZ is built so that people who already read Spanish, Portuguese, '
  'Italian or French can read it without studying it first. Normally it is written '
  'in the Latin alphabet. It also has a second, optional script, shown here under '
  'each word. In that script the shape of a letter tells you how to say it.</p>'
  '</header>')

a('<h2>Try reading these</h2>')
a('<p class="h2note">Every word is set twice, the Latin spelling above and the '
  'script below it. The translation is under each sentence, so have a go at the RZ '
  'before you look at it.</p>')
for t, g in LINES:
    a(sentence_block(t, g))

a('<div class="note"><b>That is Aesop, the north wind and the sun.</b> '
  'Phoneticians use it as a standard passage, so versions of it exist in most '
  'languages.</div>')

a('<h2>At the market</h2>')
a('<p class="h2note">Everyday speech, with numbers.</p>')
for t, g in DIALOGUE:
    a(sentence_block(t, g))

a('<h2>How a letter works</h2>')
a('<p class="h2note">Sounds that are related get shapes that are related. '
  'Voicing is the clearest case. To turn p into b you do not learn a new letter, '
  'you add a bar underneath.</p>')
a('<div class="grid">')
for w, lab in LETTERS:
    a(card(w, f'the <b>{lab}</b> sound',
           'bar underneath means voiced' if lab in ('b', 'd')
           else 'no bar, so unvoiced'))
a('</div>')

a('<h2>How a syllable ends</h2>')
a('<p class="h2note">A syllable can end in one of four consonants, and each is a '
  'single mark after the vowel. Four is a small number, which is part of why a '
  'chorded keyboard for RZ is easy to build.</p>')
a('<div class="grid">')
for w, lab in CODAS:
    a(card(w, f'ending in <b>{lab}</b>', {
        'n': 'one bar', 's': 'two bars', 'l': 'a hook downward',
        'r': 'a tick upward'}[lab]))
a('</div>')

a('<h2>Grammar suffixes</h2>')
a('<p class="h2note">Endings that carry grammar get their own mark instead of being '
  'spelled out. The useful part is that you can see what a verb is doing without '
  'reading the whole word.</p>')
a('<div class="grid">')
for w, g, n in GRAMMAR:
    a(card(w, html.escape(g), n))
a('</div>')

a('<div class="status"><b>Where this actually stands.</b>'
  '<ul><li>The language works. There is a grammar, a lexicon and enough text to '
  'read.</li>'
  '<li>The script is a working prototype, not a finished typeface. '
  'Single letters are in decent shape. Consonant clusters are not: they are '
  'drawn by shrinking one letter and tucking another above it, and the result '
  'is cramped. That is the next thing to redraw.</li>'
  '<li>Two stroke weights is deliberate, not a rendering fault. Structural '
  'strokes are heavy, marks are light, which is what keeps a mark from reading '
  'as a letter.</li>'
  '<li>Nobody outside the project has been tested on any of it, so how easy it is '
  'to read is still a guess.</li></ul></div>')

a('<footer><a href="./">Read more, and score yourself</a>'
  '<a href="faster-language.html">Why not just make it faster?</a>'
  '<a href="paper.html">The paper</a></footer>')

page = f"""<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>RZ and Its Script</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Spectral:ital,wght@0,400;0,600;1,400&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>{CSS}</style>
<div class="wrap">
{chr(10).join(B)}
</div>
"""
Path("docs/script-demo.html").write_text(page, encoding="utf-8")
print(f"wrote docs/script-demo.html ({len(page)} bytes), "
      f"shared vertical extent {Y0:.1f}..{Y1:.1f}, glyph height {GLYPH_H}px")
