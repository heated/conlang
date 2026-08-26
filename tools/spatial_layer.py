"""The spatial sentence layer — round 1 (conlang-4j7).

The designated sequel, pulled forward as an experiment: render a
discourse's relational skeleton SPATIALLY instead of serially, so
reference and role binding are done by parallel vision rather than by
the ~39 bits/s serial channel.

Pipeline: marked-up linear source -> deterministic parse -> clause
graph -> N layout engines -> geometry-derived metrics.

The parse is deterministic because the grammar is: `-n` = predicate,
`-s` = modifier, h-particles carry oblique roles, SVO fixes agent and
patient.  That is the conlang's actual contribution here — extraction
is lossless by construction, not AI-approximate.

Specimens render ENGLISH lexemes inside the GF grammar so the layout
is the only variable under test (Edward can read English; he cannot
read GZ, which would confound the judgment).

CLI:
    python3 tools/spatial_layer.py pages [outdir]
    python3 tools/spatial_layer.py sheet [outpath]
    python3 tools/spatial_layer.py metrics
"""

from __future__ import annotations

import math
import os
import sys
from dataclasses import dataclass, field

# ---------------------------------------------------------------- source

SOURCE = [
    "engineer build-n bridge stone-s hol valley",
    "bridge cross-n river",
    "river hoon flood-n valley hol spring",
    "flood haan damage-n bridge",
    "engineer say-n hel stone hold-n",
    "stone come-n hees mountain",
    "village praise-n engineer",
]

# Plain English of the same discourse, for orientation only — so the judge
# always knows what content he is looking at while judging the layout.
PROSE = ("The engineer built a stone bridge in the valley.  The bridge "
         "crosses the river.  The river flooded the valley in spring.  The "
         "flood did not damage the bridge.  The engineer says the stone "
         "held.  The stone came from the mountain.  The village praised "
         "the engineer.")

# particle -> (kind, role/marker).  Subset of gf-grammar.md §3 that this
# specimen exercises.
PARTICLES = {
    "hol": ("oblique", "LOC"),
    "hees": ("oblique", "SRC"),
    "his": ("oblique", "INSTR"),
    "hal": ("oblique", "GOAL"),
    "haan": ("marker", "NEG"),
    "hoon": ("marker", "PAST"),
    "huul": ("marker", "IRR"),
    "hus": ("marker", "Q"),
    "hel": ("comp", "COMP"),
}

TIME_WORDS = {"spring"}  # lexicon type: temporal noun (hol + time = when)

ROLE_ORDER = ["AG", "PAT", "LOC", "SRC", "INSTR", "GOAL", "TIME"]
ROLE_LABEL = {
    "AG": "", "PAT": "", "LOC": "at", "SRC": "from",
    "INSTR": "with", "GOAL": "to", "TIME": "when",
}
# role -> compass angle (degrees, math convention; SVG y is flipped)
ROLE_ANGLE = {
    "AG": 180.0, "PAT": 0.0, "TIME": 90.0, "LOC": 270.0,
    "SRC": 135.0, "GOAL": 45.0, "INSTR": 225.0, "COMP": 315.0,
}


@dataclass
class Arg:
    ent: str
    role: str
    mods: list = field(default_factory=list)


@dataclass
class Clause:
    idx: int
    pred: str
    args: list = field(default_factory=list)
    marks: list = field(default_factory=list)   # NEG, PAST, ...
    parent: int | None = None                   # matrix clause index
    tokens: int = 0                             # source token count

    def arg(self, role):
        for a in self.args:
            if a.role == role:
                return a
        return None

    def ents(self):
        out = []
        for a in self.args:
            out.append(a.ent)
            out.extend(a.mods)
        return out


def parse(lines=SOURCE):
    """Marked-up GF linear form -> clause list.  Deterministic."""
    clauses = []
    for line in lines:
        toks = line.split()
        cur = Clause(idx=len(clauses), pred="", tokens=len(toks))
        clauses.append(cur)
        pending_role = None     # oblique particle just seen
        seen_pred = False
        last_arg = None
        for tok in toks:
            if tok in PARTICLES:
                kind, val = PARTICLES[tok]
                if kind == "oblique":
                    pending_role = val
                elif kind == "marker":
                    cur.marks.append(val)
                else:  # complementizer: everything after is a sub-clause
                    sub = Clause(idx=len(clauses), pred="",
                                 parent=cur.idx, tokens=0)
                    clauses.append(sub)
                    cur = sub
                    seen_pred = False
                    last_arg = None
                continue
            if tok.endswith("-n"):
                cur.pred = tok[:-2]
                seen_pred = True
                last_arg = None
                continue
            if tok.endswith("-s"):
                if last_arg is not None:
                    last_arg.mods.append(tok[:-2])
                continue
            # bare noun
            if pending_role:
                role = pending_role
                pending_role = None
                if role == "LOC" and tok in TIME_WORDS:
                    role = "TIME"
            elif not seen_pred:
                role = "AG"
            else:
                role = "PAT"
            last_arg = Arg(ent=tok, role=role)
            cur.args.append(last_arg)
        # source token count for a matrix clause includes its complement
        if cur.parent is not None:
            clauses[cur.parent].tokens += len(
                [t for t in toks[toks.index("hel") + 1:]])
            clauses[cur.parent].tokens -= 0
    return clauses


def entity_order(clauses):
    order, seen = [], set()
    for c in clauses:
        for e in c.ents():
            if e not in seen:
                seen.add(e)
                order.append(e)
    return order


# ---------------------------------------------------------------- palette

PALETTE = [
    "#cfe3f7", "#f7dfcf", "#d7f0d5", "#eed7f2", "#f9eec6",
    "#d3eeee", "#f5d5d5", "#e2e2f4", "#e8efd0", "#f0e0ee",
]
EDGE = "#4a5568"
INK = "#1a202c"
MUTED = "#8a94a6"


def tint(ents, e):
    return PALETTE[ents.index(e) % len(PALETTE)] if e in ents else "#eeeeee"


# ---------------------------------------------------------------- svg prims

def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def rect(x, y, w, h, fill="none", stroke=EDGE, sw=1.4, rx=3, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}"'
            f' rx="{rx}" fill="{fill}" stroke="{stroke}"'
            f' stroke-width="{sw}"{d}/>')


def line(x1, y1, x2, y2, stroke=EDGE, sw=1.4, dash=None, cap="round"):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}"'
            f' stroke="{stroke}" stroke-width="{sw}"'
            f' stroke-linecap="{cap}"{d}/>')


def circ(cx, cy, r, fill="none", stroke=EDGE, sw=1.4, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{fill}"'
            f' stroke="{stroke}" stroke-width="{sw}"{d}/>')


def text(x, y, s, size=15, anchor="middle", fill=INK, weight="normal",
         style="normal", family="Helvetica, Arial, sans-serif"):
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}"'
            f' font-family="{family}" font-weight="{weight}"'
            f' font-style="{style}" fill="{fill}"'
            f' text-anchor="{anchor}">{esc(s)}</text>')


def tw(s, size=15):
    """Advance width for Helvetica-ish text.  Deliberately generous: an
    under-estimate silently overflows the canvas and clips the render."""
    return 0.62 * size * len(s)


_NUM = r"([-\d.]+)"


def content_bbox(parts):
    """(minx, miny, maxx, maxy) of everything actually drawn.

    Used two ways: to fit the canvas (a layout that under-estimates its own
    size silently clips the render), and to normalize metrics against the
    INK box rather than the canvas — otherwise a layout improves every
    normalized score just by padding itself with blank margin.
    """
    import re
    mx = my = 0.0
    nx = ny = 1e9
    blob = "".join(parts)

    def see(x, y):
        nonlocal mx, my, nx, ny
        mx, my, nx, ny = max(mx, x), max(my, y), min(nx, x), min(ny, y)

    for m in re.finditer(r'<rect x="%s" y="%s" width="%s" height="%s"'
                         % (_NUM, _NUM, _NUM, _NUM), blob):
        x, y, w, h = (float(v) for v in m.groups())
        see(x, y)
        see(x + w, y + h)
    for m in re.finditer(r'<line x1="%s" y1="%s" x2="%s" y2="%s"'
                         % (_NUM, _NUM, _NUM, _NUM), blob):
        x1, y1, x2, y2 = (float(v) for v in m.groups())
        see(x1, y1)
        see(x2, y2)
    for m in re.finditer(r'<circle cx="%s" cy="%s" r="%s"'
                         % (_NUM, _NUM, _NUM), blob):
        cx, cy, r = (float(v) for v in m.groups())
        see(cx - r, cy - r)
        see(cx + r, cy + r)
    for m in re.finditer(
            r'<text x="%s" y="%s" font-size="%s".*?text-anchor="(\w+)">'
            r'(.*?)</text>' % (_NUM, _NUM, _NUM), blob):
        x, y, fs, anchor, body = m.groups()
        x, y, fs = float(x), float(y), float(fs)
        w = tw(body, fs)
        left = x if anchor == "start" else (x - w / 2 if
                                            anchor == "middle" else x - w)
        see(left, y - fs)
        see(left + w, y + fs * 0.3)
    for m in re.finditer(r'<polygon points="([^"]+)"', blob):
        for pair in m.group(1).split():
            px, py = (float(v) for v in pair.split(","))
            see(px, py)
    if nx > mx:
        nx = ny = 0.0
    return nx, ny, mx, my


def content_extent(parts):
    _, _, mx, my = content_bbox(parts)
    return mx, my


def svg(parts, w, h, bg="#ffffff", fit=False):
    # `fit` is only safe when parts carry no transform (page bodies are
    # translated, sheets are scaled — those pass their own measured size).
    if fit:
        ex, ey = content_extent(parts)
        w, h = max(w, ex + 24), max(h, ey + 24)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w:.0f}"'
            f' height="{h:.0f}" viewBox="0 0 {w:.0f} {h:.0f}">'
            f'<rect width="{w:.0f}" height="{h:.0f}" fill="{bg}"'
            f' stroke="#dde3ec" stroke-width="2"/>'
            + "".join(parts) + "</svg>")


# ---------------------------------------------------------------- layout API

@dataclass
class Layout:
    key: str
    name: str
    parts: list
    w: float
    h: float
    mentions: list       # (ent, cx, cy)
    labels: int          # rendered text labels (repetition cost)
    crossings: int = 0
    note: str = ""


def _box(x, y, s, ents, size=15, pad=7, h=26, bold=False):
    """Tinted entity box; returns (parts, w, h, cx, cy)."""
    w = tw(s, size) + 2 * pad
    parts = [rect(x, y, w, h, fill=tint(ents, s)),
             text(x + w / 2, y + h / 2 + size * 0.36, s, size=size,
                  weight="bold" if bold else "normal")]
    return parts, w, h, x + w / 2, y + h / 2


def _pred_box(x, y, s, size=15, pad=9, h=26, neg=False, past=False):
    label = s
    w = tw(label, size) + 2 * pad + (14 if past else 0)
    parts = [rect(x, y, w, h, fill="#ffffff", stroke=INK, sw=2.0,
                  dash="5 3" if neg else None)]
    tx = x + w / 2 + (7 if past else 0)
    if past:
        parts.append(text(x + pad, y + h / 2 + size * 0.36, "«",
                          size=size, anchor="start", fill=MUTED))
    parts.append(text(tx, y + h / 2 + size * 0.36, label, size=size,
                      weight="bold"))
    if neg:
        parts.append(line(x + 4, y + h - 3, x + w - 4, y + 3,
                          stroke="#c53030", sw=2.0))
    return parts, w, h, x + w / 2, y + h / 2


# ---------------------------------------------------------------- S0 linear

def layout_S0(clauses, ents, width=1180):
    """Control: ordinary running text, one string, wrapped."""
    parts, mentions = [], []
    x, y = 40.0, 60.0
    size, gap = 17, 7
    labels = 0
    for c in clauses:
        toks = []
        if c.parent is not None:
            toks.append(("p", "‹that›"))
        for a in c.args:
            if a.role == "AG":
                toks.append(("e", a.ent))
                for m in a.mods:
                    toks.append(("e", m))
        if "PAST" in c.marks:
            toks.append(("p", "did"))
        if "NEG" in c.marks:
            toks.append(("p", "not"))
        toks.append(("v", c.pred))
        for a in c.args:
            if a.role == "AG":
                continue
            if ROLE_LABEL[a.role]:
                toks.append(("p", ROLE_LABEL[a.role]))
            toks.append(("e", a.ent))
            for m in a.mods:
                toks.append(("e", m))
        if c.parent is None and not any(
                d.parent == c.idx for d in clauses):
            toks.append(("punct", "."))
        for kind, t in toks:
            if kind == "punct":
                parts.append(text(x - gap + 2, y, ".", size=size,
                                  anchor="start"))
                continue
            w = tw(t, size)
            if x + w > width - 40:
                x, y = 40.0, y + 36
            if kind == "e":
                parts.append(rect(x - 4, y - size + 3, w + 8, size + 9,
                                  fill=tint(ents, t), stroke="none", rx=3))
                mentions.append((t, x + w / 2, y - size * 0.35,
                                 w + 8, size + 9))
            parts.append(text(
                x, y, t, size=size, anchor="start",
                fill=MUTED if kind == "p" else INK,
                weight="bold" if kind == "v" else "normal"))
            labels += 1
            x += w + gap
    return Layout("S0", "linear control", parts, width, y + 60,
                  mentions, labels,
                  note="ordinary string; reference and role both serial")


# ------------------------------------------------------- S1 referent lanes

def layout_S1(clauses, ents):
    """Entities are vertical lanes; a clause is a bar joining lanes.

    ASL's 'same entity, same column' + the subway-map/storyline move.
    Each entity is NAMED ONCE at its lane head; participation is a cap
    on the lane, so token repetition collapses.
    """
    lane_ents = [e for e in ents if e not in TIME_WORDS]
    LANE = 118.0
    x0, y0 = 90.0, 108.0
    row_h = 62.0
    lane_x = {e: x0 + i * LANE for i, e in enumerate(lane_ents)}
    n_rows = len(clauses)
    last_lane = x0 + (len(lane_ents) - 1) * LANE
    gutter_x = last_lane + 96          # clear of the rightmost lane's caps
    width = gutter_x + 300
    height = y0 + n_rows * row_h + 70
    parts, mentions = [], []
    labels = 0
    pred_pos = {}

    # lane lines + heads
    for e in lane_ents:
        x = lane_x[e]
        parts.append(line(x, y0 - 26, x, y0 + n_rows * row_h - 16,
                          stroke="#c9d2e0", sw=1.2))
        bp, bw, bh, cx, cy = _box(x - (tw(e, 15) + 14) / 2, y0 - 62, e, ents)
        parts.extend(bp)
        labels += 1

    # rows
    row_y = {}
    for j, c in enumerate(clauses):
        y = y0 + j * row_h
        row_y[c.idx] = y
        parts.append(line(40, y + 26, width - 30, y + 26,
                          stroke="#eef1f6", sw=1.0))
        xs = [lane_x[a.ent] for a in c.args if a.ent in lane_x]
        for a in c.args:
            for m in a.mods:
                if m in lane_x:
                    xs.append(lane_x[m])
        if not xs:
            xs = [x0]
        lo, hi = min(xs), max(xs)
        if hi - lo < 96:      # one-participant clause still needs a bar to
            hi = lo + 96      # hang the predicate on
        neg = "NEG" in c.marks
        indent = 22 if c.parent is not None else 0
        parts.append(line(lo, y + indent, hi, y + indent,
                          stroke="#c53030" if neg else EDGE, sw=2.2,
                          dash="6 4" if neg else None))
        # caps: role is carried by cap SHAPE (the third channel)
        for a in c.args:
            if a.ent not in lane_x:
                continue
            x = lane_x[a.ent]
            yy = y + indent
            mentions.append((a.ent, x, yy, 16, 16))
            if a.role == "AG":
                parts.append(rect(x - 6, yy - 6, 12, 12,
                                  fill=tint(ents, a.ent), sw=1.8, rx=1))
            elif a.role == "PAT":
                parts.append(
                    f'<polygon points="{x-9:.1f},{yy-7:.1f} {x+7:.1f},{yy:.1f}'
                    f' {x-9:.1f},{yy+7:.1f}" fill="{tint(ents, a.ent)}"'
                    f' stroke="{EDGE}" stroke-width="1.6"/>')
            else:
                parts.append(circ(x, yy, 7, fill=tint(ents, a.ent), sw=1.6))
                parts.append(text(x, yy + 3.5, ROLE_LABEL[a.role][0].upper(),
                                  size=9, fill=EDGE))
                labels += 1
            for m in a.mods:
                if m in lane_x:
                    mx = lane_x[m]
                    mentions.append((m, mx, yy + 12, 10, 10))
                    parts.append(circ(mx, yy, 5, fill=tint(ents, m),
                                      sw=1.2, dash="2 2"))
        # predicate rides the bar
        px = (lo + hi) / 2 - tw(c.pred, 15) / 2 - 9
        pp, pw, ph, pcx, pcy = _pred_box(px, y + indent - 13, c.pred,
                                         neg=neg, past="PAST" in c.marks)
        parts.extend(pp)
        labels += 1
        pred_pos[c.idx] = (pcx, pcy + ph / 2)
        # temporal / non-lane obliques go to the right gutter
        for a in c.args:
            if a.ent in lane_x:
                continue
            parts.append(text(gutter_x, y + indent + 5,
                              f"{ROLE_LABEL[a.role]} {a.ent}", size=13,
                              anchor="start", fill=MUTED, style="italic"))
            mentions.append((a.ent, gutter_x + 30, y + indent,
                             tw(a.ent, 13) + 30, 18))
            labels += 1
        if c.parent is not None and c.parent in pred_pos:
            mx, my = pred_pos[c.parent]
            parts.append(line(mx, my, mx, y + indent, stroke=MUTED, sw=1.4,
                              dash="3 3"))
            parts.append(line(mx, y + indent, lo - 8, y + indent,
                              stroke=MUTED, sw=1.4, dash="3 3"))
    return Layout("S1", "referent lanes", parts, width, height,
                  mentions, labels,
                  note="x = entity (reference pinned), y = clause, "
                       "role = cap shape")


# --------------------------------------------------- S2 role geometry (tree)

def layout_S2(clauses, ents):
    """Role = compass position around the predicate.  Case is geometry."""
    CELL_W, CELL_H = 430.0, 250.0
    per_row = 3
    R = 92.0
    parts, mentions = [], []
    labels = 0
    n = len(clauses)
    rows = (n + per_row - 1) // per_row
    width = 60 + per_row * CELL_W
    height = 90 + rows * CELL_H
    centers = {}
    for j, c in enumerate(clauses):
        cx = 60 + (j % per_row) * CELL_W + CELL_W / 2 - 60
        cy = 90 + (j // per_row) * CELL_H + CELL_H / 2 - 30
        centers[c.idx] = (cx, cy)
        neg = "NEG" in c.marks
        for a in c.args:
            ang = math.radians(ROLE_ANGLE[a.role])
            ax = cx + R * math.cos(ang)
            ay = cy - R * math.sin(ang)
            parts.append(line(cx, cy, ax, ay, stroke="#b9c2d0", sw=1.3))
            s = a.ent
            bw = tw(s, 15) + 14
            bp, bw, bh, bcx, bcy = _box(ax - bw / 2, ay - 13, s, ents)
            parts.extend(bp)
            labels += 1
            mentions.append((s, bcx, bcy, bw, bh))
            for k, m in enumerate(a.mods):
                mp, mw, mh, mcx, mcy = _box(ax - tw(m, 12) / 2 - 6,
                                            ay + 15 + k * 20, m, ents,
                                            size=12, h=19)
                parts.extend(mp)
                labels += 1
                mentions.append((m, mcx, mcy, mw, mh))
        pp, pw, ph, pcx, pcy = _pred_box(cx - tw(c.pred, 15) / 2 - 9,
                                         cy - 13, c.pred, neg=neg,
                                         past="PAST" in c.marks)
        parts.extend(pp)
        labels += 1
        if c.parent is not None and c.parent in centers:
            px, py = centers[c.parent]
            ang = math.radians(ROLE_ANGLE["COMP"])
            parts.append(line(px + R * 0.6 * math.cos(ang),
                              py - R * 0.6 * math.sin(ang), cx, cy,
                              stroke=MUTED, sw=1.6, dash="4 3"))
    return Layout("S2", "role compass", parts, width, height,
                  mentions, labels,
                  note="role = angle around predicate; reference only "
                       "by tint (repeated boxes)")


# ------------------------------------------------------- S3 proposition rings

def _ring_dir(role):
    ang = math.radians(ROLE_ANGLE[role])
    return math.cos(ang), -math.sin(ang)


def layout_S3(clauses, ents):
    """Heptapod, taken seriously.

    Role lives on the ANGULAR channel, which frees both plane axes for
    topology — so a shared entity can be written ONCE and read as agent
    by one ring and patient by another, if the rings are placed so the
    shared box lands at the right angle for both.  We solve that
    constraint greedily and report how many shares it satisfies.
    """
    R = 84.0
    placed = {}          # clause idx -> (cx, cy)
    ent_slot = {}        # ent -> (x, y) once fixed
    satisfied, total_shares = 0, 0
    order = list(clauses)
    placed[order[0].idx] = (0.0, 0.0)
    for a in order[0].args:
        dx, dy = _ring_dir(a.role)
        ent_slot[a.ent] = (R * dx, R * dy)

    # Two rings that share a boundary entity sit EXACTLY 2R apart (the shared
    # box straddles the tangency), so tangency must be legal; only closer
    # than tangent is a real collision.
    def collides(cx, cy, exclude=None):
        for k, (px, py) in placed.items():
            if k == exclude:
                continue
            if math.hypot(cx - px, cy - py) < 2 * R - 4:
                return True
        return False

    for c in order[1:]:
        best = None
        for a in c.args:
            if a.ent in ent_slot:
                total_shares += 1
                ex, ey = ent_slot[a.ent]
                dx, dy = _ring_dir(a.role)
                cx, cy = ex - R * dx, ey - R * dy
                if best is None and not collides(cx, cy):
                    best = (cx, cy, a.ent)
        if best is None:
            # fall back: park it clear of everything, to the right
            cx = max((p[0] for p in placed.values()), default=0.0) + 2 * R + 60
            cy = 0.0
            k = 0
            while collides(cx, cy):
                k += 1
                cy = (k // 2 + 1) * (2 * R + 50) * (1 if k % 2 else -1)
            placed[c.idx] = (cx, cy)
        else:
            cx, cy, _ = best
            placed[c.idx] = (cx, cy)
            satisfied += 1
        for a in c.args:
            if a.ent not in ent_slot:
                dx, dy = _ring_dir(a.role)
                ent_slot[a.ent] = (cx + R * dx, cy + R * dy)

    # ---- draw
    parts, mentions = [], []
    labels = 0
    drawn = set()
    xs = [p[0] for p in placed.values()] + [p[0] for p in ent_slot.values()]
    ys = [p[1] for p in placed.values()] + [p[1] for p in ent_slot.values()]
    ox = 150 - min(xs)
    oy = 170 - min(ys)
    width = max(xs) - min(xs) + 300
    height = max(ys) - min(ys) + 320

    for c in clauses:
        cx, cy = placed[c.idx]
        cx, cy = cx + ox, cy + oy
        neg = "NEG" in c.marks
        parts.append(circ(cx, cy, R, fill="none", stroke="#aab4c4", sw=1.6,
                          dash="6 4" if neg else None))
        for a in c.args:
            dx, dy = _ring_dir(a.role)
            ax, ay = cx + R * dx, cy + R * dy
            slot = ent_slot.get(a.ent)
            shared = (slot is not None
                      and math.hypot(slot[0] + ox - ax, slot[1] + oy - ay) < 2)
            parts.append(line(cx + 0.45 * R * dx, cy + 0.45 * R * dy,
                              ax - 6 * dx, ay - 6 * dy,
                              stroke="#8f9bad", sw=1.3))
            if shared and a.ent in drawn:
                mentions.append((a.ent, ax, ay, tw(a.ent, 14) + 14, 26))
                continue
            bw = tw(a.ent, 14) + 14
            bp, bw, bh, bcx, bcy = _box(ax - bw / 2, ay - 13, a.ent, ents,
                                        size=14)
            parts.extend(bp)
            labels += 1
            drawn.add(a.ent)
            mentions.append((a.ent, bcx, bcy, bw, bh))
            for k, m in enumerate(a.mods):
                mp, mw, mh, mcx, mcy = _box(ax - tw(m, 11) / 2 - 6,
                                            ay + 14 + k * 18, m, ents,
                                            size=11, h=17)
                parts.extend(mp)
                labels += 1
                mentions.append((m, mcx, mcy, mw, mh))
        pp, pw, ph, pcx, pcy = _pred_box(cx - tw(c.pred, 15) / 2 - 9,
                                         cy - 13, c.pred, neg=neg,
                                         past="PAST" in c.marks)
        parts.extend(pp)
        labels += 1
    note = (f"role = ring angle; shared entity written once "
            f"({satisfied}/{total_shares} shares geometrically satisfied)")
    lay = Layout("S3", "proposition rings", parts, width, height,
                 mentions, labels, note=note)
    lay.shares = (satisfied, total_shares)
    return lay


# ----------------------------------------------------------- S4 schema grid

def layout_S4(clauses, ents):
    """Ablation: just make it a table.  Role = column, clause = row."""
    cols = ["AG", "pred", "PAT", "oblique", "when"]
    widths = [170.0, 165.0, 170.0, 200.0, 130.0]
    x0, y0 = 46.0, 96.0
    row_h = 44.0
    width = x0 + sum(widths) + 46
    height = y0 + len(clauses) * row_h + 60
    parts, mentions = [], []
    labels = 0
    cx = x0
    for name, w in zip(cols, widths):
        parts.append(text(cx + 10, y0 - 14, name, size=13, anchor="start",
                          fill=MUTED, weight="bold"))
        cx += w
    parts.append(line(x0, y0 - 6, x0 + sum(widths), y0 - 6,
                      stroke="#c9d2e0", sw=1.4))
    for j, c in enumerate(clauses):
        y = y0 + j * row_h
        parts.append(line(x0, y + row_h - 4, x0 + sum(widths), y + row_h - 4,
                          stroke="#eef1f6", sw=1.0))
        ind = 18 if c.parent is not None else 0
        cx = x0 + ind
        # AG
        a = c.arg("AG")
        if a:
            bp, bw, bh, bx, by = _box(cx + 6, y + 4, a.ent, ents)
            parts.extend(bp)
            labels += 1
            mentions.append((a.ent, bx, by, bw, bh))
            for m in a.mods:
                mp, mw, mh, mx, my = _box(cx + 12 + bw, y + 7, m, ents,
                                          size=12, h=19)
                parts.extend(mp)
                labels += 1
                mentions.append((m, mx, my, mw, mh))
        cx = x0 + widths[0] + ind
        pp, pw, ph, pcx, pcy = _pred_box(cx + 6, y + 4, c.pred,
                                         neg="NEG" in c.marks,
                                         past="PAST" in c.marks)
        parts.extend(pp)
        labels += 1
        cx = x0 + widths[0] + widths[1]
        a = c.arg("PAT")
        if a:
            bp, bw, bh, bx, by = _box(cx + 6, y + 4, a.ent, ents)
            parts.extend(bp)
            labels += 1
            mentions.append((a.ent, bx, by, bw, bh))
            for m in a.mods:
                mp, mw, mh, mx, my = _box(cx + 12 + bw, y + 7, m, ents,
                                          size=12, h=19)
                parts.extend(mp)
                labels += 1
                mentions.append((m, mx, my, mw, mh))
        cx = x0 + sum(widths[:3])
        for a in c.args:
            if a.role in ("AG", "PAT", "TIME"):
                continue
            parts.append(text(cx + 6, y + 22, ROLE_LABEL[a.role], size=12,
                              anchor="start", fill=MUTED))
            bp, bw, bh, bx, by = _box(cx + 12 + tw(ROLE_LABEL[a.role], 12),
                                      y + 4, a.ent, ents)
            parts.extend(bp)
            labels += 2
            mentions.append((a.ent, bx, by, bw, bh))
            cx += 30 + bw
        cx = x0 + sum(widths[:4])
        a = c.arg("TIME")
        if a:
            bp, bw, bh, bx, by = _box(cx + 6, y + 4, a.ent, ents)
            parts.extend(bp)
            labels += 1
            mentions.append((a.ent, bx, by, bw, bh))
        if c.parent is not None:
            parts.append(text(x0 + 4, y + 24, "↳", size=15,
                              anchor="start", fill=MUTED))
    return Layout("S4", "schema grid", parts, width, height,
                  mentions, labels,
                  note="role = column (pinned), reference = tint only")


LAYOUTS = [("S0", layout_S0), ("S1", layout_S1), ("S2", layout_S2),
           ("S3", layout_S3), ("S4", layout_S4)]


# ---------------------------------------------------------------- metrics

def _clusters(pts, radius):
    """Single-linkage cluster count — 'how many places must the eye go'."""
    if not pts:
        return 0
    unassigned = list(range(len(pts)))
    n = 0
    while unassigned:
        seed = unassigned.pop(0)
        frontier = [seed]
        group = {seed}
        while frontier:
            i = frontier.pop()
            for j in list(unassigned):
                if math.hypot(pts[i][0] - pts[j][0],
                              pts[i][1] - pts[j][1]) <= radius:
                    unassigned.remove(j)
                    group.add(j)
                    frontier.append(j)
        n += 1
    return n


# Guide colours carry no proposition content (lane rules, row separators);
# every other stroke/box/label is an information-bearing mark.
GUIDE_COLOURS = ("#c9d2e0", "#eef1f6", "#dde3ec")


def count_marks(parts):
    """Every information-bearing mark, not just text.

    Counting labels alone flatters layouts that replace a word with a cap,
    an angle or a connector — those are marks the reader must still decode.
    """
    import re
    blob = "".join(parts)
    n = 0
    for tag in ("rect", "line", "circle", "polygon", "text"):
        for m in re.finditer(r"<%s\b[^>]*>" % tag, blob):
            frag = m.group(0)
            if any(c in frag for c in GUIDE_COLOURS):
                continue
            if tag == "rect" and 'x="' not in frag:
                continue            # page background
            n += 1
    return n


def _segments(parts):
    import re
    segs = []
    for m in re.finditer(
            r'<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="([^"]+)"'
            % (_NUM, _NUM, _NUM, _NUM), "".join(parts)):
        x1, y1, x2, y2 = (float(v) for v in m.groups()[:4])
        if m.group(5) in GUIDE_COLOURS:
            continue
        segs.append((x1, y1, x2, y2))
    return segs


def count_crossings(parts):
    """Proper intersections between content edges — the standard
    graph-drawing readability predictor."""
    def cross(o, a, b):
        return ((a[0] - o[0]) * (b[1] - o[1])
                - (a[1] - o[1]) * (b[0] - o[0]))

    segs = _segments(parts)
    n = 0
    for i in range(len(segs)):
        p1, p2 = segs[i][:2], segs[i][2:]
        for j in range(i + 1, len(segs)):
            q1, q2 = segs[j][:2], segs[j][2:]
            d1, d2 = cross(p1, p2, q1), cross(p1, p2, q2)
            d3, d4 = cross(q1, q2, p1), cross(q1, q2, p2)
            if ((d1 > 0) != (d2 > 0)) and ((d3 > 0) != (d4 > 0)):
                n += 1
    return n


def metrics(lay, clauses, ents):
    """Geometry-derived structural DIAGNOSTICS.  All [M] on the render.

    These are not evidence of parallel binding (Codex plan review, blocker
    1): they measure clustering, repetition and compactness only.  Every
    normalization is against the INK bounding box, never the canvas, so a
    layout cannot improve its score by padding itself with margin.
    """
    x0, y0, x1, y1 = content_bbox(lay.parts)
    iw, ih = max(x1 - x0, 1.0), max(y1 - y0, 1.0)
    diag = math.hypot(iw, ih)
    ink_area = iw * ih
    per_ent = {}
    for e, cx, cy, w, h in lay.mentions:
        per_ent.setdefault(e, []).append((cx, cy, w, h))
    scatter, search = [], []
    for e, ms in per_ent.items():
        if len(ms) < 2:
            continue        # singletons: no scatter, and a bbox that would
                            # flatter every layout equally.  Excluded.
        ds = [math.hypot(ms[i][0] - ms[j][0], ms[i][1] - ms[j][1])
              for i in range(len(ms)) for j in range(i + 1, len(ms))]
        scatter.append(sum(ds) / len(ds) / diag)
        # union box over full GLYPH extents, not anchor points
        bx0 = min(m[0] - m[2] / 2 for m in ms)
        bx1 = max(m[0] + m[2] / 2 for m in ms)
        by0 = min(m[1] - m[3] / 2 for m in ms)
        by1 = max(m[1] + m[3] / 2 for m in ms)
        search.append((bx1 - bx0) * (by1 - by0) / ink_area)
    n_prop = len(clauses)
    return {
        "ink_area_per_prop": ink_area / n_prop,
        "marks_per_prop": count_marks(lay.parts) / n_prop,
        "labels_per_prop": lay.labels / n_prop,
        "scatter": sum(scatter) / len(scatter) if scatter else 0.0,
        "search": sum(search) / len(search) if search else 0.0,
        "crossings": count_crossings(lay.parts),
    }


# --------------------------------------------------- oracle coverage [A]

# The information a rendering must preserve to be an equivalent encoding of
# the discourse (Codex plan review, blocker 3).  Coverage below is ASSERTED
# by inspection of each renderer, not proved by a decoder — a layout->oracle
# decoder is the named next piece of work.
ORACLE_FIELDS = ["clause order", "predicate", "arg roles", "entity id",
                 "coreference", "TAM", "polarity", "modifier attachment",
                 "complement edge"]

COVERAGE = {
    #        order pred role  id    coref TAM   pol   modattach comp
    "S0": ["yes", "yes", "yes", "yes", "no", "yes", "yes", "yes", "yes"],
    "S1": ["yes", "yes", "yes", "yes", "yes", "yes", "yes", "NO", "yes"],
    "S2": ["yes", "yes", "yes", "yes", "tint", "yes", "yes", "yes", "yes"],
    "S3": ["NO", "yes", "yes", "yes", "part", "yes", "yes", "yes", "NO"],
    "S4": ["yes", "yes", "yes", "yes", "tint", "yes", "yes", "yes", "yes"],
}

COVERAGE_NOTES = {
    "S0": "coreference is left to the reader — the string repeats a name "
          "and never says the two mentions are the same referent.",
    "S1": "coreference is ARCHITECTURAL (same lane = same referent), but a "
          "modifier's cap sits on its own lane with nothing saying which "
          "argument it attaches to.",
    "S2": "complete, but reference is carried only by tint, i.e. by a "
          "non-positional channel that does not scale past ~10 entities.",
    "S3": "rings have no reading order, so DISCOURSE ORDER is lost, and "
          "the complement edge has no place to attach; shared entities are "
          "written once only when the geometry permits.",
    "S4": "complete; reference by tint only.  The ablation to beat.",
}


def serial_binding_span(clauses):
    """Working-memory span the SOURCE string forces: mean number of
    intervening tokens between successive mentions of one entity."""
    seq = []
    pos = 0
    for c in clauses:
        for a in c.args:
            seq.append((a.ent, pos))
            pos += 1
            for m in a.mods:
                seq.append((m, pos))
                pos += 1
        pos += 1 + len(c.marks)  # predicate + markers
    per = {}
    for e, p in seq:
        per.setdefault(e, []).append(p)
    gaps = [b - a - 1 for ps in per.values() for a, b in zip(ps, ps[1:])]
    return (sum(gaps) / len(gaps) if gaps else 0.0), max(gaps) if gaps else 0


# ---------------------------------------------------------------- rendering

TITLE = {
    "S0": "S0 · linear control",
    "S1": "S1 · referent lanes",
    "S2": "S2 · role compass",
    "S3": "S3 · proposition rings",
    "S4": "S4 · schema grid",
}


def build(key):
    clauses = parse()
    ents = entity_order(clauses)
    fn = dict(LAYOUTS)[key]
    return fn(clauses, ents), clauses, ents


def prose_parts(x, y, width, size=14):
    """Wrap PROSE into gray lines; returns (parts, height)."""
    parts, cx, cy = [], x, y
    line_h = size + 7
    words, cur = PROSE.split(), []
    for wd in words:
        trial = " ".join(cur + [wd])
        if tw(trial, size) > width and cur:
            parts.append(text(x, cy, " ".join(cur), size=size, anchor="start",
                              fill=MUTED, style="italic"))
            cy += line_h
            cur = [wd]
        else:
            cur.append(wd)
    if cur:
        parts.append(text(x, cy, " ".join(cur), size=size, anchor="start",
                          fill=MUTED, style="italic"))
        cy += line_h
    return parts, cy - y


def page(key):
    lay, clauses, ents = build(key)
    bx, by = content_extent(lay.parts)
    pw = max(lay.w, bx + 40, 900.0)
    head = [text(40, 44, TITLE[key], size=24, anchor="start", weight="bold"),
            text(40, 68, lay.note, size=14, anchor="start", fill=MUTED)]
    pp, ph = prose_parts(40, 96, pw - 120)
    head.extend(pp)
    top = 96 + ph + 18
    body = [f'<g transform="translate(0,{top:.0f})">'
            + "".join(lay.parts) + "</g>"]
    return svg(head + body, pw, max(lay.h, by) + top + 30)


def sheet():
    """All five layouts scaled onto one comparison sheet + metric table."""
    clauses = parse()
    ents = entity_order(clauses)
    W = 2000.0
    parts = [text(46, 52, "The spatial sentence layer — structural "
                          "bake-off, round 1",
                  size=30, anchor="start", weight="bold"),
             text(46, 80,
                  "same discourse, five spatial grammars.  english lexemes "
                  "inside the GF grammar so LAYOUT is the only variable.  "
                  "this selects a prototype; it does NOT test reading.",
                  size=15, anchor="start", fill=MUTED)]
    pp, ph = prose_parts(46, 108, W - 700, size=15)
    parts.extend(pp)
    y = 108.0 + ph + 16
    rows = []
    for key, fn in LAYOUTS:
        lay = fn(clauses, ents)
        m = metrics(lay, clauses, ents)
        rows.append((key, lay, m))
        s = min(1.0, (W - 92) / lay.w, 430 / lay.h)
        parts.append(text(46, y + 20, TITLE[key], size=19, anchor="start",
                          weight="bold"))
        parts.append(text(46 + tw(TITLE[key], 19) + 24, y + 20, lay.note,
                          size=13, anchor="start", fill=MUTED))
        parts.append(f'<g transform="translate(46,{y + 34:.1f}) '
                     f'scale({s:.4f})">' + "".join(lay.parts) + "</g>")
        y += 34 + lay.h * s + 34
        parts.append(line(46, y - 14, W - 46, y - 14, stroke="#e6eaf1",
                          sw=1.2))
    # metric table
    y += 16
    parts.append(text(46, y, "measured [M] on these renders", size=19,
                      anchor="start", weight="bold"))
    y += 30
    cols = ["layout", "ink area/prop", "marks/prop", "referent scatter",
            "area to search per referent", "edge crossings"]
    cw = [220, 210, 190, 250, 320, 220]
    x = 46.0
    for c, w in zip(cols, cw):
        parts.append(text(x, y, c, size=14, anchor="start", fill=MUTED,
                          weight="bold"))
        x += w
    y += 8
    parts.append(line(46, y, 46 + sum(cw), y, stroke="#c9d2e0", sw=1.3))
    y += 24
    for key, lay, m in rows:
        x = 46.0
        vals = [TITLE[key], f"{m['ink_area_per_prop']:.0f} px²",
                f"{m['marks_per_prop']:.1f}", f"{m['scatter']:.3f}",
                f"{100 * m['search']:.1f}%", f"{m['crossings']}"]
        for v, w in zip(vals, cw):
            parts.append(text(x, y, v, size=15, anchor="start"))
            x += w
        y += 28
    y += 14
    mean_gap, max_gap = serial_binding_span(clauses)
    parts.append(text(
        46, y,
        f"the STIMULUS (not any layout) forces a serial binding span of "
        f"{mean_gap:.1f} tokens mean / {max_gap} worst: the working-memory "
        f"reach a linear reader holds to bind a referent to its last "
        f"mention.",
        size=15, anchor="start"))
    y += 46

    # oracle coverage — the kill gate that runs before any geometry counts
    parts.append(text(46, y, "oracle coverage [A] — can the layout encode "
                             "the field at all?", size=19, anchor="start",
                      weight="bold"))
    y += 30
    cx = 46.0
    parts.append(text(cx, y, "field", size=14, anchor="start", fill=MUTED,
                      weight="bold"))
    for i, (key, _) in enumerate(LAYOUTS):
        parts.append(text(300 + i * 120, y, key, size=14, anchor="middle",
                          fill=MUTED, weight="bold"))
    y += 8
    parts.append(line(46, y, 300 + len(LAYOUTS) * 120, y, stroke="#c9d2e0",
                      sw=1.3))
    y += 24
    for i, f in enumerate(ORACLE_FIELDS):
        parts.append(text(46, y, f, size=15, anchor="start"))
        for j, (key, _) in enumerate(LAYOUTS):
            v = COVERAGE[key][i]
            parts.append(text(300 + j * 120, y, v, size=15, anchor="middle",
                              fill="#c53030" if v == "NO" else
                              (MUTED if v in ("tint", "part", "no")
                               else INK),
                              weight="bold" if v == "NO" else "normal"))
        y += 26
    y += 16
    for key, _ in LAYOUTS:
        parts.append(text(46, y, f"{key}: {COVERAGE_NOTES[key]}", size=14,
                          anchor="start", fill=MUTED))
        y += 24
    return svg(parts, W, y + 50)


def main(argv=None):
    argv = argv or sys.argv[1:]
    cmd = argv[0] if argv else "sheet"
    if cmd == "pages":
        out = argv[1] if len(argv) > 1 else "."
        os.makedirs(out, exist_ok=True)
        for key, _ in LAYOUTS:
            p = os.path.join(out, f"page_{key}.svg")
            with open(p, "w") as f:
                f.write(page(key))
            print(p)
    elif cmd == "sheet":
        p = argv[1] if len(argv) > 1 else "sheet.svg"
        with open(p, "w") as f:
            f.write(sheet())
        print(p)
    elif cmd == "metrics":
        clauses = parse()
        ents = entity_order(clauses)
        print(f"{len(clauses)} clauses, {len(ents)} entities: "
              f"{', '.join(ents)}")
        mean_gap, max_gap = serial_binding_span(clauses)
        print(f"serial binding span (source): mean {mean_gap:.1f} tokens, "
              f"max {max_gap}")
        hdr = (f"{'layout':<22}{'ink/prop':>12}{'marks/prop':>12}"
               f"{'scatter':>10}{'search%':>10}{'cross':>8}")
        print(hdr)
        print("-" * len(hdr))
        for key, fn in LAYOUTS:
            lay = fn(clauses, ents)
            m = metrics(lay, clauses, ents)
            print(f"{TITLE[key]:<22}{m['ink_area_per_prop']:>12.0f}"
                  f"{m['marks_per_prop']:>12.1f}{m['scatter']:>10.3f}"
                  f"{100 * m['search']:>10.1f}{m['crossings']:>8}")
            if hasattr(lay, "shares"):
                print(f"    shared-entity constraints satisfied: "
                      f"{lay.shares[0]}/{lay.shares[1]}")
        print()
        print("oracle coverage [A] — can the layout encode the field at all?")
        print(f"{'field':<22}" + "".join(f"{k:>8}" for k, _ in LAYOUTS))
        for i, f in enumerate(ORACLE_FIELDS):
            print(f"{f:<22}"
                  + "".join(f"{COVERAGE[k][i]:>8}" for k, _ in LAYOUTS))
    else:
        print(__doc__)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
