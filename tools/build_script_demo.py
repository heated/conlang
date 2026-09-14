"""Build docs/script-demo.html: RZ text beside the featural display script.

Usage: python3 tools/build_script_demo.py
Renders the SVGs first, then writes the page. Safe to re-run.
"""
import json, os, html, subprocess, sys
from pathlib import Path
os.chdir(Path(__file__).resolve().parent.parent)
subprocess.run([sys.executable, "tools/build_script_demo_render.py"], check=True)
parts = json.load(open(".rz_parts.json"))

lines = [p for p in parts if p[0] == 'line']
dlg = [p for p in parts if p[0] == 'dlg']
words = [p for p in parts if p[0] == 'word']
letters = [p for p in parts if p[0] == 'letter']

CSS = """
:root{
  --paper:#F7F7F5; --ink:#1B1D20; --soft:#585E66; --faint:#8A9098;
  --rule:#E2E4E0; --accent:#2244AA; --accent-soft:#EAEEF9; --panel:#FFFFFF;
  --ochre:#8A5F28; --ochre-soft:#F5EEE2;
}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){
  --paper:#15171B; --ink:#E9EAE6; --soft:#A4ABB4; --faint:#767D86;
  --rule:#2A2F35; --accent:#8AA6F2; --accent-soft:#1D2540; --panel:#1C1F25;
  --ochre:#C79A55; --ochre-soft:#292317;
}}
:root[data-theme="dark"]{
  --paper:#15171B; --ink:#E9EAE6; --soft:#A4ABB4; --faint:#767D86;
  --rule:#2A2F35; --accent:#8AA6F2; --accent-soft:#1D2540; --panel:#1C1F25;
  --ochre:#C79A55; --ochre-soft:#292317;
}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);
  font-family:"IBM Plex Sans",system-ui,-apple-system,sans-serif;
  font-size:17px;line-height:1.6;-webkit-font-smoothing:antialiased}
.wrap{max-width:760px;margin:0 auto;padding:0 24px 90px}
header.t{padding:64px 0 28px;border-bottom:1px solid var(--rule);margin-bottom:8px}
.eyebrow{font-family:"IBM Plex Mono",ui-monospace,monospace;font-size:11.5px;
  letter-spacing:.14em;text-transform:uppercase;color:var(--faint);margin-bottom:14px}
h1{font-family:Spectral,Georgia,serif;font-size:clamp(28px,4vw,38px);
  line-height:1.15;margin:0 0 16px;font-weight:600;letter-spacing:-.01em}
.sub{font-size:17px;color:var(--soft);line-height:1.55;max-width:62ch}
h2{font-size:19px;font-weight:600;margin:52px 0 6px;letter-spacing:-.005em}
.h2note{color:var(--soft);font-size:15.5px;margin:0 0 24px;max-width:62ch}
p{margin:0 0 16px}
a{color:var(--accent)}

/* the script itself */
svg.rz{width:100%;height:auto;display:block;color:var(--ink)}
svg.rz.sm{max-width:190px}

.line{border-bottom:1px solid var(--rule);padding:26px 0}
.line:last-child{border-bottom:none}
.latin{font-family:Spectral,Georgia,serif;font-size:20px;line-height:1.5;
  margin:0 0 4px}
.gloss{color:var(--faint);font-size:15px;margin:0 0 16px}
.script-box{background:var(--panel);border:1px solid var(--rule);border-radius:3px;
  padding:16px 20px;overflow-x:auto}

.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));
  gap:18px;margin-bottom:10px}
.card{background:var(--panel);border:1px solid var(--rule);border-radius:3px;
  padding:16px 16px 14px;display:flex;flex-direction:column;gap:10px}
.card .glyphs{height:70px;display:flex;align-items:center;justify-content:center}
.card .w{font-family:Spectral,Georgia,serif;font-size:18px;font-weight:600}
.card .g{color:var(--faint);font-size:14px;margin-top:-6px}
.card .n{color:var(--soft);font-size:14px;line-height:1.45}
.card .n b{color:var(--ink);font-weight:600}
.tag{font-family:"IBM Plex Mono",ui-monospace,monospace;font-size:12px;
  background:var(--ochre-soft);color:var(--ochre);padding:2px 7px;border-radius:2px;
  align-self:flex-start}

.note{border-left:2px solid var(--accent);padding-left:16px;color:var(--soft);
  font-size:15.5px;margin:28px 0}
.note b{color:var(--ink);font-weight:600}
footer{border-top:1px solid var(--rule);margin-top:60px;padding-top:26px;
  font-size:15px;color:var(--soft)}
footer a{margin-right:20px}
"""


def card(w, label, note, svg, tag=None):
    t = f'<div class="tag">{html.escape(tag)}</div>' if tag else ''
    return f"""<div class="card">
      <div class="glyphs">{svg.replace('class="rz"','class="rz sm"')}</div>
      <div><div class="w">{html.escape(w)}</div><div class="g">{label}</div></div>
      <div class="n">{note}</div>{t}</div>"""


body = []
B = body.append

B('<header class="t"><div class="eyebrow">RZ &middot; Romance zonal &middot; display script</div>')
B('<h1>A language, and the script it is written in</h1>')
B('<p class="sub">RZ is a constructed language built so that people who already read '
  'Spanish, Portuguese, Italian or French can read it <em>without studying it first</em>. '
  'Its everyday spelling is the Latin alphabet. This page also shows the optional '
  'display script — a featural one, where the shape of each letter tells you how '
  'to say it.</p></header>')

B('<h2>Read this first, before any explanation</h2>')
B('<p class="h2note">If you read any Romance language, try the line before you read the '
  'grey translation under it. The script underneath is the same sentence again.</p>')
for _, latin, gloss, s in lines:
    B(f'<div class="line"><p class="latin">{html.escape(latin)}</p>'
      f'<p class="gloss">{html.escape(gloss)}</p>'
      f'<div class="script-box">{s}</div></div>')

B('<div class="note"><b>That’s Aesop’s north wind and sun</b> — the passage '
  'phoneticians use as a standard text. If you guessed most of it cold, that’s the '
  'entire point of the language; if you didn’t, that’s the measurement we '
  'haven’t run yet.</div>')

B('<h2>At the market</h2>')
B('<p class="h2note">Ordinary conversational register, with numbers.</p>')
for _, latin, gloss, s in dlg:
    B(f'<div class="line"><p class="latin">{html.escape(latin)}</p>'
      f'<p class="gloss">{html.escape(gloss)}</p>'
      f'<div class="script-box">{s}</div></div>')

B('<h2>How a letter works</h2>')
B('<p class="h2note">The script is <em>featural</em>: related sounds get related shapes, '
  'so the writing system doubles as a pronunciation guide. Voicing isn’t a new '
  'letter — it’s a bar underneath.</p>')
B('<div class="grid">')
for _, w, label, note, s in letters[:6]:
    B(card(w, f'the <b>{html.escape(label)}</b> onset', note, s))
B('</div>')

B('<h2>How a syllable ends</h2>')
B('<p class="h2note">Every coda is one mark in a strip after the vowel. RZ only needs a '
  'handful — which is exactly why a chorded keyboard for it is easy.</p>')
B('<div class="grid">')
for _, w, label, note, s in letters[6:]:
    B(card(w, f'coda <b>{html.escape(label)}</b>', note, s))
B('</div>')

B('<h2>Grammar gets its own ink</h2>')
B('<p class="h2note">Suffixes that carry grammar — tense, adverbs, nominalisation — '
  'are drawn as dedicated blocks rather than spelled out. You can see the tense of a '
  'verb without reading the word.</p>')
B('<div class="grid">')
for _, w, gloss, note, s in words:
    B(card(w, html.escape(gloss), note, s))
B('</div>')

B('<div class="note"><b>Honest labelling, since this is a research project.</b> '
  'The language is real and complete enough to read. The script is a working prototype, '
  'not a finished typeface. And nobody outside the project has been tested yet — '
  'every claim about how learnable this is remains a hypothesis until that happens.</div>')

B('<footer><a href="./">Read more, and score yourself</a>'
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
{chr(10).join(body)}
</div>
"""
open('docs/script-demo.html', 'w', encoding='utf-8').write(page)
print("wrote docs/script-demo.html", len(page), "bytes")
