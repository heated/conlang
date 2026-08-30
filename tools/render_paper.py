#!/usr/bin/env python3
"""Render paper/paper.md to a self-contained docs/paper.html.

No dependencies: a small, deliberately limited Markdown subset that
covers exactly what the paper uses (headings, paragraphs, emphasis,
inline code, block quotes, bullet and numbered lists, pipe tables,
footnote-free pandoc citations), plus the two things a paper needs
that generic renderers get wrong here:

  * [@key] and [@a; @b] citations become numbered links into a
    reference list built from paper/references.bib, in citation
    order, so the published page has real references rather than
    raw @keys.
  * [H] / [D] / [M] / [TODO-verify...] evidence markers are styled,
    because they are load-bearing in this project and must not read
    as typos.

Usage:  python3 tools/render_paper.py [--check]
        --check exits non-zero if any citation has no bib entry.
"""

import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "paper" / "paper.md"
BIB = ROOT / "paper" / "references.bib"
OUT = ROOT / "docs" / "paper.html"


# ---------------------------------------------------------------- bib

def parse_bib(text):
    """Very small BibTeX reader: key -> {field: value}."""
    entries = {}
    for m in re.finditer(r"@(\w+)\s*\{\s*([^,]+),", text):
        kind, key = m.group(1).lower(), m.group(2).strip()
        start = m.end()
        depth, i = 1, start
        while i < len(text) and depth:
            if text[i] == "{":
                depth += 1
            elif text[i] == "}":
                depth -= 1
            i += 1
        body = text[start:i - 1]
        fields = {}
        for fm in re.finditer(r"(\w+)\s*=\s*", body):
            j = fm.end()
            if j >= len(body):
                continue
            if body[j] == "{":
                d, k = 1, j + 1
                while k < len(body) and d:
                    if body[k] == "{":
                        d += 1
                    elif body[k] == "}":
                        d -= 1
                    k += 1
                fields[fm.group(1).lower()] = body[j + 1:k - 1].strip()
            elif body[j] == '"':
                k = body.index('"', j + 1)
                fields[fm.group(1).lower()] = body[j + 1:k].strip()
        fields["_type"] = kind
        entries[key] = fields
    return entries


# Minimal LaTeX accent decoding, so names render as names.
ACCENTS = {
    ("'", "e"): "é", ("'", "a"): "á", ("'", "o"): "ó", ("'", "i"): "í",
    ("'", "u"): "ú", ("`", "e"): "è", ("`", "a"): "à", ('"', "o"): "ö",
    ('"', "u"): "ü", ('"', "a"): "ä", ("^", "e"): "ê", ("^", "o"): "ô",
    ("~", "n"): "ñ", ("c", "c"): "ç", ("v", "s"): "š", ("v", "c"): "č",
}


def delatex(x):
    # \'e  \'{e}  \c c  \c{c}
    def sub(m):
        return ACCENTS.get((m.group(1), m.group(2)), m.group(2))
    x = re.sub(r"\\([\'`\"^~])\{?(\w)\}?", sub, x)
    x = re.sub(r"\\([cv])\s*\{?(\w)\}?", sub, x)
    return x.replace("\\&", "&").replace("\\_", "_")


def format_ref(f):
    def clean(x):
        return delatex(re.sub(r"[{}]", "", x or "").replace("\\emph", "")).strip()
    head = ""
    if f.get("author"):
        head = html.escape(clean(f["author"]))
    if f.get("year"):
        head = f"{head} ({clean(f['year'])})" if head else f"({clean(f['year'])})"
    tail = []
    if f.get("title"):
        tail.append(f"<em>{html.escape(clean(f['title']))}</em>")
    for k in ("journal", "booktitle", "publisher", "institution", "howpublished"):
        if f.get(k):
            tail.append(html.escape(clean(f[k])))
            break
    if f.get("volume"):
        tail.append(f"vol. {clean(f['volume'])}")
    if f.get("pages"):
        tail.append(f"pp. {clean(f['pages'])}")
    out = ". ".join(x for x in ([head] if head else []) + [", ".join(tail)] if x)
    if out and not out.endswith("."):
        out += "."
    if f.get("note"):
        out += f'<br><span class="note">{html.escape(clean(f["note"]))}</span>'
    return out


# ------------------------------------------------------------- inline

MARKER = re.compile(r"\[(H|D|M|TODO-verify[^\]]*)\]")


def inline(text, cite):
    """Escape, then apply inline markup. Order matters."""
    t = html.escape(text)

    # citations first: [@a] or [@a; @b]
    def cite_sub(m):
        keys = [k.strip().lstrip("@") for k in m.group(1).split(";")]
        return "[" + ", ".join(cite(k) for k in keys) + "]"

    t = re.sub(r"\[@([^\]]+)\]", cite_sub, t)
    t = MARKER.sub(lambda m: f'<span class="marker">[{m.group(1)}]</span>', t)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    t = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<![*\w])\*([^*]+)\*(?!\*)", r"<em>\1</em>", t)
    t = re.sub(r"(?<!\w)_([^_]+)_(?!\w)", r"<em>\1</em>", t)
    return t


# -------------------------------------------------------------- block

def render(md, bib):
    order, seen = [], {}

    def cite(key):
        if key not in seen:
            order.append(key)
            seen[key] = len(order)
        n = seen[key]
        label = key if key not in bib else f"{n}"
        return f'<a class="cite" href="#ref-{html.escape(key)}">{label}</a>'

    lines = md.split("\n")
    out, i = [], 0
    # strip YAML front matter
    if lines and lines[0].strip() == "---":
        j = 1
        while j < len(lines) and lines[j].strip() != "---":
            j += 1
        i = j + 1

    para = []

    def flush():
        if para:
            out.append("<p>" + inline(" ".join(para), cite) + "</p>")
            para.clear()

    while i < len(lines):
        line = lines[i]
        st = line.strip()

        if not st:
            flush()
            i += 1
            continue

        m = re.match(r"^(#{2,4})\s+(.*)$", st)
        if m:
            flush()
            lvl = len(m.group(1))
            txt = inline(m.group(2), cite)
            anchor = re.sub(r"[^a-z0-9]+", "-",
                            re.sub(r"<[^>]+>", "", m.group(2)).lower()).strip("-")
            out.append(f'<h{lvl} id="{anchor}">{txt}</h{lvl}>')
            i += 1
            continue

        if st.startswith("|") and i + 1 < len(lines) and re.match(r"^\s*\|[\s:|-]+\|\s*$", lines[i + 1]):
            flush()
            head = [c.strip() for c in st.strip("|").split("|")]
            i += 2
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            out.append('<div class="tw"><table><thead><tr>'
                       + "".join(f"<th>{inline(h, cite)}</th>" for h in head)
                       + "</tr></thead><tbody>"
                       + "".join("<tr>" + "".join(f"<td>{inline(c, cite)}</td>" for c in r) + "</tr>"
                                 for r in rows)
                       + "</tbody></table></div>")
            continue

        if st.startswith(">"):
            flush()
            buf = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                buf.append(lines[i].strip().lstrip(">").strip())
                i += 1
            out.append("<blockquote>" + inline(" ".join(buf), cite) + "</blockquote>")
            continue

        if re.match(r"^[-*]\s+", st):
            flush()
            items = []
            while i < len(lines) and re.match(r"^[-*]\s+", lines[i].strip()):
                buf = [re.sub(r"^[-*]\s+", "", lines[i].strip())]
                i += 1
                while (i < len(lines) and lines[i].strip()
                       and not re.match(r"^[-*]\s+|^\d+\.\s+|^#{2,4}\s|^\|", lines[i].strip())):
                    buf.append(lines[i].strip())
                    i += 1
                items.append(" ".join(buf))
            out.append("<ul>" + "".join(f"<li>{inline(x, cite)}</li>" for x in items) + "</ul>")
            continue

        if re.match(r"^\d+\.\s+", st):
            flush()
            items = []
            while i < len(lines) and re.match(r"^\d+\.\s+", lines[i].strip()):
                buf = [re.sub(r"^\d+\.\s+", "", lines[i].strip())]
                i += 1
                while (i < len(lines) and lines[i].strip()
                       and not re.match(r"^[-*]\s+|^\d+\.\s+|^#{2,4}\s|^\|", lines[i].strip())):
                    buf.append(lines[i].strip())
                    i += 1
                items.append(" ".join(buf))
            out.append("<ol>" + "".join(f"<li>{inline(x, cite)}</li>" for x in items) + "</ol>")
            continue

        para.append(st)
        i += 1

    flush()
    return "\n".join(out), order


CSS = """
:root{
  --paper:#F7F7F5; --ink:#1B1D20; --soft:#585E66; --faint:#8A9098;
  --rule:#E2E4E0; --accent:#2244AA; --accent-soft:#EAEEF9;
  --marker:#8A5F28; --marker-bg:#F5EEE2;
}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){
  --paper:#15171B; --ink:#E9EAE6; --soft:#A4ABB4; --faint:#767D86;
  --rule:#2A2F35; --accent:#8AA6F2; --accent-soft:#1D2540;
  --marker:#C79A55; --marker-bg:#292317;
}}
:root[data-theme="dark"]{
  --paper:#15171B; --ink:#E9EAE6; --soft:#A4ABB4; --faint:#767D86;
  --rule:#2A2F35; --accent:#8AA6F2; --accent-soft:#1D2540;
  --marker:#C79A55; --marker-bg:#292317;
}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);
  font-family:Spectral,Georgia,"Times New Roman",serif;
  font-size:18px;line-height:1.68;-webkit-font-smoothing:antialiased}
.wrap{max-width:720px;margin:0 auto;padding:0 24px 96px}
header.t{border-bottom:1px solid var(--rule);padding:72px 0 32px;margin-bottom:40px}
h1{font-size:clamp(28px,4vw,38px);line-height:1.18;margin:0 0 18px;
  text-wrap:balance;font-weight:600;letter-spacing:-.01em}
.by{font-family:"IBM Plex Sans",system-ui,sans-serif;font-size:14px;color:var(--soft)}
.status{font-family:"IBM Plex Mono",ui-monospace,monospace;font-size:12px;
  color:var(--faint);margin-top:10px;line-height:1.5}
h2{font-family:"IBM Plex Sans",system-ui,sans-serif;font-size:20px;font-weight:600;
  margin:56px 0 16px;padding-top:20px;border-top:1px solid var(--rule);
  text-wrap:balance;letter-spacing:-.005em}
h3{font-family:"IBM Plex Sans",system-ui,sans-serif;font-size:16px;font-weight:600;
  margin:34px 0 12px;text-wrap:balance}
h4{font-family:"IBM Plex Sans",system-ui,sans-serif;font-size:15px;font-weight:600;margin:26px 0 10px}
p{margin:0 0 18px}
ul,ol{margin:0 0 18px;padding-left:24px}li{margin-bottom:9px}
blockquote{margin:0 0 20px;padding:2px 0 2px 20px;border-left:2px solid var(--accent);
  color:var(--soft)}
code{font-family:"IBM Plex Mono",ui-monospace,monospace;font-size:.86em;
  background:var(--accent-soft);padding:1px 5px;border-radius:2px}
a{color:var(--accent)}
a.cite{font-family:"IBM Plex Sans",system-ui,sans-serif;font-size:.8em;
  text-decoration:none;padding:0 1px}
a.cite:hover{text-decoration:underline}
.marker{font-family:"IBM Plex Mono",ui-monospace,monospace;font-size:.72em;
  color:var(--marker);background:var(--marker-bg);padding:1px 5px;
  border-radius:2px;white-space:nowrap;letter-spacing:.02em}
.tw{overflow-x:auto;margin:0 0 22px}
table{border-collapse:collapse;width:100%;font-size:14px;
  font-family:"IBM Plex Sans",system-ui,sans-serif}
th,td{text-align:left;padding:8px 14px 8px 0;border-bottom:1px solid var(--rule);
  vertical-align:top}
th{font-family:"IBM Plex Mono",ui-monospace,monospace;font-size:11px;
  text-transform:uppercase;letter-spacing:.08em;color:var(--faint);font-weight:500}
#references ol{padding-left:22px}
#references li{font-size:15px;color:var(--soft);margin-bottom:12px}
#references .note{font-size:13px;color:var(--faint)}
.toc{font-family:"IBM Plex Sans",system-ui,sans-serif;font-size:14px;
  border:1px solid var(--rule);border-radius:2px;padding:20px 24px;margin-bottom:44px}
.toc div{font-family:"IBM Plex Mono",ui-monospace,monospace;font-size:11px;
  letter-spacing:.1em;text-transform:uppercase;color:var(--faint);margin-bottom:10px}
.toc a{display:block;padding:3px 0;text-decoration:none;color:var(--ink)}
.toc a:hover{color:var(--accent)}
@media (prefers-reduced-motion:reduce){*{transition:none!important}}
"""


def main():
    md = SRC.read_text(encoding="utf-8")
    bib = parse_bib(BIB.read_text(encoding="utf-8"))
    body, order = render(md, bib)

    missing = [k for k in order if k not in bib]
    if "--check" in sys.argv:
        if missing:
            print("citations with no bib entry:", ", ".join(missing), file=sys.stderr)
            return 1
        print(f"ok — {len(order)} citations, all resolved")
        return 0

    refs = "".join(
        f'<li id="ref-{html.escape(k)}">{format_ref(bib[k])}</li>' if k in bib
        else f'<li id="ref-{html.escape(k)}"><em>missing bib entry: {html.escape(k)}</em></li>'
        for k in order)

    toc = "".join(f'<a href="#{a}">{t}</a>'
                  for a, t in re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', body))

    title = ("Engineering Languages for Learning Speed: Interlingua as the "
             "Baseline, a Ledger-Priced Toolkit of Add-Ons, and the "
             "Channel-Coded Laboratory Behind Them")
    page = f"""<title>Engineering Languages for Learning Speed</title>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Spectral:ital,wght@0,300;0,400;0,600;1,400&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>{CSS}</style>
<div class="wrap">
<header class="t">
<h1>{html.escape(title)}</h1>
<div class="by">Edward Swernofsky, with Claude</div>
<div class="status">Complete draft. Every learner-facing number is a labelled
hypothesis; the project has zero external human subjects.<br>
<span class="marker">[H]</span> hypothesis &nbsp;
<span class="marker">[D]</span> derived &nbsp;
<span class="marker">[M]</span> measured &nbsp;
<span class="marker">[TODO-verify]</span> sourced secondarily, unchecked</div>
</header>
<nav class="toc"><div>Contents</div>{toc}</nav>
{body}
<h2 id="references">References</h2>
<div id="references"><ol>{refs}</ol></div>
</div>
"""
    OUT.write_text(page, encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)} — {len(order)} citations, "
          f"{len(missing)} unresolved{': ' + ', '.join(missing) if missing else ''}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
