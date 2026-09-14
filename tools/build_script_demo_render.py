"""Render the RZ script SVGs used by tools/build_script_demo.py.

Run build_script_demo.py instead; it calls this.
"""
import os, re, subprocess, sys, html
from pathlib import Path
os.chdir(Path(__file__).resolve().parent.parent)

def svg(mode, arg):
    out = subprocess.run([sys.executable, 'tools/rz_script.py', mode] +
                         ([arg] if isinstance(arg, str) else arg),
                         capture_output=True, text=True)
    if out.returncode != 0:
        raise SystemExit(f"render failed for {arg!r}:\n{out.stderr}")
    s = out.stdout.strip()
    # strip the hardcoded colour so the page's theme drives it, and let it scale
    s = s.replace(' style="color:#1a1a1a"', '')
    s = re.sub(r'\swidth="\d+"\s*height="\d+"', ' class="rz"', s, count=1)
    return s

# ---- content: (latin RZ, english gloss) ----
LINES = [
    ("Le vento del norte e le sol disputava",
     "The north wind and the sun were arguing"),
    ("sobre qui era le plus forte.",
     "about which of them was the stronger."),
    ("Un viajator passava, coprite de un manto calde.",
     "A traveller came by, wrapped in a warm cloak."),
]

DIALOGUE = [
    ("Bon dia! Cuante costa istes pomos?", "Good morning! How much are these apples?"),
    ("Dos euros le kilo.", "Two euros a kilo."),
    ("Alora io prende tres kilos.", "Then I'll take three kilos."),
]

WORDS = [
    ("parlava", "was speaking", "the <b>-va</b> past tense fires a logogram — a left arrow, meaning 'past'"),
    ("parlaria", "would speak", "<b>-ria</b> conditional: a fork instead of an arrow"),
    ("rapidemente", "quickly", "<b>-mente</b> adverb suffix gets its own half-width block"),
    ("construccion", "construction", "<b>-cion</b> likewise — the grammar channel gets dedicated ink"),
    ("nove", "new / nine", "a plain two-syllable word, no logogram"),
]

LETTERS = [
    ("pa", "p", "the greenfield letterform, kept verbatim"),
    ("ba", "b", "same letter, plus a full-width <b>ground bar</b> = voiced"),
    ("ta", "t", "t is an X"),
    ("da", "d", "and d is t with the ground bar"),
    ("pra", "pr", "cluster: the liquid rides <b>top-right</b> as a satellite"),
    ("spa", "sp", "s- rides <b>top-left</b> — reading order is preserved"),
]

CODAS = [
    ("pan", "-n", "coda strip: a bar"),
    ("pas", "-s", "double bar"),
    ("pal", "-l", "down-hook"),
    ("par", "-r", "up-tick"),
]

parts = []
A = parts.append

for latin, gloss in LINES:
    A(('line', latin, gloss, svg('sentence', latin)))
for latin, gloss in DIALOGUE:
    A(('dlg', latin, gloss, svg('sentence', latin)))
for w, gloss, note in WORDS:
    A(('word', w, gloss, note, svg('word', w)))
for w, label, note in LETTERS:
    A(('letter', w, label, note, svg('word', w)))
for w, label, note in CODAS:
    A(('letter', w, label, note, svg('word', w)))

import json
json.dump([list(p) for p in parts], open('.rz_parts.json', 'w'))
print(f"rendered {len(parts)} items")
