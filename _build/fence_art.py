# -*- coding: utf-8 -*-
"""
Drawings for the fence template, all generated as inline SVG (no images, nothing to download):

  defs_svg()            shared gradients and patterns, placed once per page that uses the drawings
  fence_card(t, ...)    one fence type on a cut-away of the ground (holes, gravel, concrete, frost line).
                        Every part carries a start (--s) and a duration (--d) on a 0-1 build timeline; the page
                        sets --b (build progress) on the card and CSS works out each part's own progress (--q).
                        Used by the pinned scroll sequence on the home page and the estimate preview.
  hero_fence_svg()      a perspective fence line receding to the horizon behind the home hero
  yard_plan_svg()       top-down yard with a fence line being measured (home estimate teaser)
  locate_plan_svg()     top-down lot with the property line and utility locate marks (home "know the line" band)

Build timeline (fraction of a fence type's slot in the scroll sequence):
  0.02-0.20 dig holes · 0.12-0.30 posts drop in · 0.26-0.40 concrete · 0.36-0.52 rails
  0.48-0.82 pickets / panels / mesh / boards · 0.82-0.90 caps and trim · 0.88 "built" stamp
"""
import math, html

# ---------------------------------------------------------------- the five fence types in the scroll sequence
# "service" links each drawing to a service slug, so a type disappears if the client doesn't offer it.
TYPES = [
    {"id": "wood", "service": "wood-fences", "name": "Wood", "word": "Cedar", "height_ft": 6,
     "infill": "Pickets", "title": "Cedar privacy"},
    {"id": "vinyl", "service": "vinyl-fences", "name": "Vinyl", "word": "Vinyl", "height_ft": 6,
     "infill": "Panels", "title": "Vinyl lattice-top"},
    {"id": "ornamental", "service": "ornamental-fences", "name": "Ornamental", "word": "Aluminum", "height_ft": 5,
     "infill": "Pickets", "title": "Ornamental aluminum"},
    {"id": "chain-link", "service": "chain-link-fences", "name": "Chain link", "word": "Chain link", "height_ft": 5,
     "infill": "Mesh", "title": "Galvanized chain link"},
    {"id": "composite", "service": "composite-fences", "name": "Composite", "word": "Composite", "height_ft": 6,
     "infill": "Boards", "title": "Horizontal composite"},
]

G = 400                       # ground line
FT = 35                       # pixels per foot
POSTS = [62, 332, 602, 872]   # post centres (8 ft sections, drawn slightly short so the scene fits)
HOLE_BOTTOM = 522             # 3.5 ft below grade
FROST = 505
VB = "0 96 900 464"


def _r(v):
    return f"{v:.1f}".rstrip("0").rstrip(".")


def _q(s, d):
    """style for a timed part: starts at s, takes d of the build timeline"""
    return f'style="--s:{s:.3f};--d:{d:.3f}"'


def defs_svg():
    return '''<svg class="fx-defs" width="0" height="0" aria-hidden="true" focusable="false"><defs>
<linearGradient id="fx-cedar-1" x1="0" x2="1"><stop offset="0" stop-color="#b8743f"/><stop offset=".5" stop-color="#c98a52"/><stop offset="1" stop-color="#a5652f"/></linearGradient>
<linearGradient id="fx-cedar-2" x1="0" x2="1"><stop offset="0" stop-color="#a9673a"/><stop offset=".55" stop-color="#bd7d48"/><stop offset="1" stop-color="#985a2c"/></linearGradient>
<linearGradient id="fx-cedar-3" x1="0" x2="1"><stop offset="0" stop-color="#c4834b"/><stop offset=".45" stop-color="#d3955b"/><stop offset="1" stop-color="#b0703b"/></linearGradient>
<linearGradient id="fx-wpost" x1="0" x2="1"><stop offset="0" stop-color="#7a4a26"/><stop offset=".5" stop-color="#94592d"/><stop offset="1" stop-color="#6a3f1f"/></linearGradient>
<linearGradient id="fx-vinyl" x1="0" x2="1"><stop offset="0" stop-color="#dfe3e4"/><stop offset=".5" stop-color="#f6f7f6"/><stop offset="1" stop-color="#cfd4d6"/></linearGradient>
<linearGradient id="fx-iron" x1="0" x2="1"><stop offset="0" stop-color="#1c2026"/><stop offset=".45" stop-color="#6b7580"/><stop offset="1" stop-color="#1c2026"/></linearGradient>
<linearGradient id="fx-galv" x1="0" x2="1"><stop offset="0" stop-color="#7d8790"/><stop offset=".45" stop-color="#dde3e8"/><stop offset="1" stop-color="#6f7881"/></linearGradient>
<linearGradient id="fx-alu" x1="0" x2="1"><stop offset="0" stop-color="#2a2f35"/><stop offset=".5" stop-color="#4a525b"/><stop offset="1" stop-color="#23272c"/></linearGradient>
<linearGradient id="fx-comp-1" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8a7766"/><stop offset="1" stop-color="#6d5c4e"/></linearGradient>
<linearGradient id="fx-comp-2" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7d6b5b"/><stop offset="1" stop-color="#5f5044"/></linearGradient>
<linearGradient id="fx-comp-3" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#94816f"/><stop offset="1" stop-color="#776554"/></linearGradient>
<linearGradient id="fx-conc" x1="0" x2="1"><stop offset="0" stop-color="#8b8f93"/><stop offset=".5" stop-color="#a9adb1"/><stop offset="1" stop-color="#83878b"/></linearGradient>
<linearGradient id="fx-soil" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2a2119"/><stop offset="1" stop-color="#15110d"/></linearGradient>
<pattern id="fx-clay" width="14" height="14" patternUnits="userSpaceOnUse" patternTransform="rotate(35)"><path d="M0 7h14" stroke="#3a2e23" stroke-width="1.2"/></pattern>
<pattern id="fx-grav" width="9" height="7" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.5" fill="#6b6e72"/><circle cx="6.5" cy="5" r="1.3" fill="#55585c"/></pattern>
<pattern id="fx-lattice" width="12" height="12" patternUnits="userSpaceOnUse"><path d="M0 0L12 12M12 0L0 12" stroke="#e9ecec" stroke-width="2.4"/></pattern>
<linearGradient id="fx-sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="var(--bg)" stop-opacity="0"/><stop offset="1" stop-color="var(--accent)" stop-opacity=".22"/></linearGradient>
<linearGradient id="fx-tape" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffe08a"/><stop offset="1" stop-color="var(--accent)"/></linearGradient>
</defs></svg>'''


# ---------------------------------------------------------------- ground cut-away shared by every card
def _ground(t):
    h = t["height_ft"] * FT
    top = G - h
    x0, x1 = POSTS[0], POSTS[1]
    return f'''<g class="fg">
<rect class="fg-soil" x="0" y="{G}" width="900" height="164"/><rect x="0" y="{G}" width="900" height="164" fill="url(#fx-clay)" opacity=".55"/>
<path class="fg-line" d="M0 {G}H900"/>
<path class="fg-grass" d="{" ".join(f"M{x} {G}l3 -7l2 7l4 -9l2 9" for x in range(8, 900, 37))}"/>
<path class="fg-frost" d="M0 {FROST}H900"/><text class="fg-note" x="467" y="{FROST - 6}" text-anchor="middle">FROST LINE</text>
<g class="fg-dim"><path d="M{x0} 126V138M{x1} 126V138M{x0} 132H{x1}"/><text x="{(x0 + x1) / 2}" y="122" text-anchor="middle">8 FT</text></g>
<g class="fg-dim"><path d="M18 {G}V{top}M12 {G}H24M12 {top}H24"/><text x="30" y="{(G + top) / 2 + 5}">{t["height_ft"]} FT</text></g>
</g>'''


def _holes(post_w):
    """dig holes (with dirt piles), gravel, concrete footings. Each post index k gets its own timing."""
    out = []
    for k, cx in enumerate(POSTS):
        hw = 22
        s_dig = 0.02 + 0.035 * k
        s_conc = 0.26 + 0.025 * k
        mound_x = cx + (30 if k < 3 else -30)
        out.append(
            f'<g class="fh">'
            f'<rect class="q f-hole" {_q(s_dig, 0.07)} x="{cx - hw}" y="{G}" width="{hw * 2}" height="{HOLE_BOTTOM - G}" rx="3"/>'
            f'<rect class="q f-grav" {_q(s_dig + 0.04, 0.05)} x="{cx - hw + 2}" y="{HOLE_BOTTOM - 12}" width="{hw * 2 - 4}" height="11" fill="url(#fx-grav)"/>'
            f'<g class="q f-mound-in" {_q(s_dig, 0.07)}><g class="q f-mound-out" {_q(s_conc, 0.08)}>'
            f'<path class="f-mound" d="M{mound_x - 20} {G}q20 -22 40 0z"/></g></g>'
            f'<path class="q f-conc" {_q(s_conc, 0.09)} d="M{cx - 17} {G + 3}L{cx + 17} {G + 3}L{cx + hw - 2} {HOLE_BOTTOM - 13}L{cx - hw + 2} {HOLE_BOTTOM - 13}Z"/>'
            f'</g>')
    return "".join(out)


def _post(k, cx, w, top, fill, extra=""):
    s = 0.12 + 0.04 * k
    return (f'<g class="q f-post" {_q(s, 0.08)}><rect x="{_r(cx - w / 2)}" y="{top}" width="{w}" height="{HOLE_BOTTOM - 12 - top}" fill="{fill}"/>{extra}</g>'
            f'<g class="q f-dust" {_q(s + 0.075, 0.06)}><circle cx="{cx - 16}" cy="{G - 4}" r="6"/><circle cx="{cx + 15}" cy="{G - 6}" r="5"/><circle cx="{cx}" cy="{G - 10}" r="4"/></g>')


def _stamp(label):
    return (f'<g class="q f-stamp" {_q(0.88, 0.05)}><rect x="676" y="134" width="190" height="44" rx="4"/>'
            f'<path class="f-stamp-tick" d="M694 157l7 7 14 -15"/><text x="726" y="164">{html.escape(label.upper())}</text></g>')


def _rail(m, j, y, h, fill, post_w, cls="f-rail"):
    a, b = POSTS[m] + post_w / 2, POSTS[m + 1] - post_w / 2
    s = 0.36 + 0.03 * m + 0.022 * j
    return f'<rect class="q {cls}" {_q(s, 0.07)} x="{_r(a)}" y="{y}" width="{_r(b - a)}" height="{h}" fill="{fill}"/>'


def _infill_start(i, n, span=0.3, start=0.48):
    return start + span * (i / max(1, n - 1)) * 0.86


# ---------------------------------------------------------------- fence types
def _wood():
    t = TYPES[0]
    top = G - t["height_ft"] * FT          # 190
    pw = 14
    out = [_holes(pw)]
    for k, cx in enumerate(POSTS):
        out.append(_post(k, cx, pw, top - 10, "url(#fx-wpost)"))
    for m in range(3):
        for j, y in enumerate((top + 16, top + 102, G - 22)):
            out.append(_rail(m, j, y, 9, "#6f4423", pw))
    pickets, n = [], 0
    for m in range(3):
        a = POSTS[m] + pw / 2 + 1
        width = POSTS[m + 1] - pw / 2 - 1 - a
        cnt = 14
        w = width / cnt
        for i in range(cnt):
            pickets.append((a + i * w, w - 1.2, (m * cnt + i) % 3 + 1))
    n = len(pickets)
    for i, (x, w, tone) in enumerate(pickets):
        y0, y1 = top + 2, G - 5
        d = f"M{_r(x)} {y0 + 5}L{_r(x + 4.5)} {y0}H{_r(x + w - 4.5)}L{_r(x + w)} {y0 + 5}V{y1}H{_r(x)}Z"
        out.append(f'<path class="q f-drop" {_q(_infill_start(i, n), 0.06)} d="{d}" fill="url(#fx-cedar-{tone})"/>')
    for m in range(3):
        a, b = POSTS[m] + pw / 2, POSTS[m + 1] - pw / 2
        out.append(f'<rect class="q f-trim" {_q(0.82 + 0.015 * m, 0.05)} x="{_r(a)}" y="{top - 5}" width="{_r(b - a)}" height="7" fill="#8a5630"/>')
    for k, cx in enumerate(POSTS):
        out.append(f'<path class="q f-cap" {_q(0.84 + 0.012 * k, 0.05)} d="M{cx - 10} {top - 10}L{cx} {top - 20}L{cx + 10} {top - 10}Z" fill="#9b6236"/>')
    return out


def _vinyl():
    t = TYPES[1]
    top = G - t["height_ft"] * FT
    pw = 18
    out = [_holes(pw)]
    for k, cx in enumerate(POSTS):
        out.append(_post(k, cx, pw, top - 8, "url(#fx-vinyl)"))
    lat_top, lat_bot = top + 2, top + 46
    for m in range(3):
        for j, (y, h) in enumerate(((G - 16, 10), (lat_bot, 9), (lat_top - 2, 8))):
            out.append(_rail(m, j, y, h, "#e3e6e6", pw))
    items = []
    for m in range(3):
        a, b = POSTS[m] + pw / 2, POSTS[m + 1] - pw / 2
        boards = "".join(f'<path d="M{_r(a + (b - a) * i / 9)} {lat_bot + 9}V{G - 16}"/>' for i in range(1, 9))
        items.append(f'<g class="q f-panel" {{q}}><rect x="{_r(a)}" y="{lat_bot + 9}" width="{_r(b - a)}" height="{G - 16 - lat_bot - 9}" fill="url(#fx-vinyl)"/><g class="f-vgroove">{boards}</g></g>')
    for m in range(3):
        a, b = POSTS[m] + pw / 2, POSTS[m + 1] - pw / 2
        items.append(f'<g class="q f-panel" {{q}}><rect x="{_r(a)}" y="{lat_top + 6}" width="{_r(b - a)}" height="{lat_bot - lat_top - 6}" fill="url(#fx-lattice)"/></g>')
    for i, it in enumerate(items):
        s = 0.48 + 0.055 * i
        out.append(it.replace("{q}", _q(s, 0.08)))
    for k, cx in enumerate(POSTS):
        out.append(f'<path class="q f-cap" {_q(0.84 + 0.012 * k, 0.05)} d="M{cx - 12} {top - 8}H{cx + 12}L{cx + 9} {top - 13}L{cx} {top - 20}L{cx - 9} {top - 13}Z" fill="#f3f4f3"/>')
    return out


def _ornamental():
    t = TYPES[2]
    top = G - t["height_ft"] * FT        # 225
    pw = 11
    out = [_holes(pw)]
    for k, cx in enumerate(POSTS):
        out.append(_post(k, cx, pw, top - 6, "url(#fx-iron)"))
    for m in range(3):
        for j, (y, h) in enumerate(((G - 20, 6), (top + 30, 6), (top + 6, 6))):
            out.append(_rail(m, j, y, h, "url(#fx-iron)", pw))
    pickets = []
    for m in range(3):
        a, b = POSTS[m] + pw / 2, POSTS[m + 1] - pw / 2
        cnt = 18
        step = (b - a) / cnt
        for i in range(cnt):
            pickets.append(a + step * (i + 0.5))
    n = len(pickets)
    for i, x in enumerate(pickets):
        d = f"M{_r(x - 2)} {G - 8}V{top - 6}H{_r(x - 4.5)}L{_r(x)} {top - 18}L{_r(x + 4.5)} {top - 6}H{_r(x + 2)}V{G - 8}Z"
        out.append(f'<path class="q f-drop f-drop--iron" {_q(_infill_start(i, n), 0.06)} d="{d}" fill="url(#fx-iron)"/>')
    rings = []
    for i in range(n - 1):
        if pickets[i + 1] - pickets[i] > 20 or i % 2:
            continue
        rings.append((pickets[i] + pickets[i + 1]) / 2)
    for i, x in enumerate(rings):
        out.append(f'<circle class="q f-ring" {_q(0.82 + 0.06 * i / max(1, len(rings) - 1), 0.04)} cx="{_r(x)}" cy="{top + 21}" r="5.2"/>')
    for k, cx in enumerate(POSTS):
        out.append(f'<circle class="q f-cap" {_q(0.84 + 0.012 * k, 0.05)} cx="{cx}" cy="{top - 12}" r="7" fill="url(#fx-iron)"/>')
    return out


def _chain_link():
    t = TYPES[3]
    top = G - t["height_ft"] * FT        # 225
    out = [_holes(12)]
    widths = [13, 9, 9, 13]
    for k, cx in enumerate(POSTS):
        out.append(_post(k, cx, widths[k], top - 4, "url(#fx-galv)"))
    x0, x1 = POSTS[0] + 6, POSTS[-1] - 6
    out.append(f'<rect class="q f-rail" {_q(0.36, 0.14)} x="{x0 - 2}" y="{top + 2}" width="{x1 - x0 + 4}" height="7" rx="3.5" fill="url(#fx-galv)"/>')
    out.append(f'<path class="q f-rail f-wire" {_q(0.45, 0.06)} d="M{x0} {G - 8}H{x1}"/>')
    # mesh: two sets of diagonal wires, woven in from left to right, clipped to the fence frame
    mesh_top, mesh_bot = top + 9, G - 8
    h = mesh_bot - mesh_top
    span = x1 - x0
    step = 14
    wires = []
    xs = list(range(int(x0 - h), int(x1), step))
    n = len(xs)
    for i, x in enumerate(xs):
        # each wire is timed by where it crosses the middle of the fence, so the mesh "unrolls" left to right
        mid = x + h / 2
        s = 0.48 + 0.3 * max(0, min(1, (mid - x0) / span))
        wires.append(f'<path class="q f-wire-d" {_q(s, 0.05)} pathLength="1" d="M{x} {mesh_top}L{x + h} {mesh_bot}"/>')
        wires.append(f'<path class="q f-wire-d" {_q(s, 0.05)} pathLength="1" d="M{x + h} {mesh_top}L{x} {mesh_bot}"/>')
    out.append(f'<clipPath id="fx-mesh-clip"><rect x="{x0}" y="{mesh_top - 2}" width="{span}" height="{h + 4}"/></clipPath>'
               f'<g class="f-mesh" clip-path="url(#fx-mesh-clip)">{"".join(wires)}</g>')
    out.append(f'<g class="q f-roll" style="--s:.48;--d:.3;--w:{span}"><rect x="{x0 - 9}" y="{mesh_top - 6}" width="18" height="{h + 10}" rx="9" fill="url(#fx-galv)"/>'
               f'<path d="M{x0 - 4} {mesh_top}V{mesh_bot}M{x0 + 4} {mesh_top}V{mesh_bot}" stroke="#5c656e" stroke-width="1"/></g>')
    for k, cx in enumerate((POSTS[0], POSTS[-1])):
        sx = cx + (9 if k == 0 else -9)
        out.append(f'<path class="q f-trim f-tbar" {_q(0.82 + 0.02 * k, 0.05)} d="M{sx} {mesh_top}V{mesh_bot}"/>')
    for i, x in enumerate(range(int(x0 + 30), int(x1), 60)):
        out.append(f'<path class="q f-tie" {_q(0.83 + 0.05 * i / 13, 0.03)} d="M{x} {top + 1}v10"/>')
    for k, cx in enumerate(POSTS):
        if k in (0, 3):
            out.append(f'<path class="q f-cap" {_q(0.84 + 0.012 * k, 0.05)} d="M{cx - 9} {top - 3}a9 7 0 0 1 18 0z" fill="#c9cfd4"/>')
        else:
            out.append(f'<ellipse class="q f-cap" {_q(0.84 + 0.012 * k, 0.05)} cx="{cx}" cy="{top + 4}" rx="9" ry="7" fill="none" stroke="#c9cfd4" stroke-width="3"/>')
    return out


def _composite():
    t = TYPES[4]
    top = G - t["height_ft"] * FT        # 190
    pw = 16
    out = [_holes(pw)]
    for k, cx in enumerate(POSTS):
        out.append(_post(k, cx, pw, top - 6, "url(#fx-alu)"))
    for m in range(3):
        out.append(_rail(m, 0, G - 8, 6, "url(#fx-alu)", pw))
        out.append(_rail(m, 1, top + 2, 5, "url(#fx-alu)", pw))
    rows = 11
    bh = (G - 8 - (top + 4)) / rows
    items = []
    for r in range(rows):
        y = G - 8 - (r + 1) * bh
        for m in range(3):
            a, b = POSTS[m] + pw / 2, POSTS[m + 1] - pw / 2
            items.append((r, m, a, y, b - a, (r * 3 + m * 2) % 3 + 1))
    for r, m, a, y, w, tone in items:
        s = 0.48 + 0.3 * (r / (rows - 1)) * 0.9 + 0.012 * m
        out.append(f'<rect class="q f-board" {_q(s, 0.06)} x="{_r(a)}" y="{_r(y + 0.8)}" width="{_r(w)}" height="{_r(bh - 1.6)}" fill="url(#fx-comp-{tone})"/>')
    for m in range(3):
        a, b = POSTS[m] + pw / 2, POSTS[m + 1] - pw / 2
        out.append(f'<rect class="q f-trim" {_q(0.82 + 0.015 * m, 0.05)} x="{_r(a - 2)}" y="{top - 2}" width="{_r(b - a + 4)}" height="8" fill="#2c3137"/>')
        out.append(f'<rect class="q f-trim" {_q(0.83 + 0.015 * m, 0.05)} x="{_r(a)}" y="{_r(top + 4 + bh * 4)}" width="{_r(b - a)}" height="3" fill="var(--accent)"/>')
    for k, cx in enumerate(POSTS):
        out.append(f'<rect class="q f-cap" {_q(0.84 + 0.012 * k, 0.05)} x="{cx - 11}" y="{top - 11}" width="22" height="6" rx="1" fill="#3a4047"/>')
    return out


_DRAW = {"wood": _wood, "vinyl": _vinyl, "ornamental": _ornamental, "chain-link": _chain_link, "composite": _composite}


def fence_svg(t, label):
    parts = _DRAW[t["id"]]()
    return (f'<svg class="fence-svg fence-svg--{t["id"]}" viewBox="{VB}" role="img" aria-label="{html.escape(label)}">'
            f'{_ground(t)}<g class="fence">{"".join(parts)}{_stamp("Built")}</g></svg>')


def fence_card(t, label, caption=""):
    cap = f'<figcaption class="fence-card__cap"><b>{html.escape(t["title"])}</b>{caption}</figcaption>' if caption is not None else ""
    return (f'<figure class="fence-card" data-fence="{t["id"]}" data-infill="{html.escape(t["infill"])}" data-height="{t["height_ft"]}"><span class="fence-card__word" aria-hidden="true">{html.escape(t["word"])}</span>'
            f'{fence_svg(t, label)}{cap}</figure>')


# ---------------------------------------------------------------- hero: a fence line running to the horizon
def hero_fence_svg():
    W, H = 1600, 900
    vx, vy = 1520, 560          # vanishing point
    nx, gy, hn = -30, 930, 600   # near end: x, ground y, fence height
    def proj(d):
        s = 1 / (1 + d / 11)
        return vx + (nx - vx) * s, vy + (gy - vy) * s, hn * s, s
    pickets, posts, k = [], [], 0
    d = 0.0
    while d < 150:
        x0, y0, h0, s0 = proj(d)
        x1, y1, h1, s1 = proj(d + 0.47)
        op = max(0.12, min(1, s0 * 3.2))
        pickets.append(f'<path class="hp" style="--k:{k};opacity:{op:.2f}" d="M{x0:.1f} {y0:.1f}V{y0 - h0 * .93:.1f}L{(x0 + x1) / 2:.1f} {y0 - h0:.1f}L{x1:.1f} {y1 - h1 * .93:.1f}V{y1:.1f}Z"/>')
        k += 1
        d += 0.5
    for i in range(0, 19):
        x0, y0, h0, s0 = proj(i * 8)
        posts.append(f'<path class="hp hp--post" style="--k:{i * 16}" d="M{x0 - 7 * s0:.1f} {y0:.1f}V{y0 - h0 * 1.04:.1f}H{x0 + 7 * s0:.1f}V{y0:.1f}Z"/>')
    # perspective grid on the ground and the light
    grid = "".join(f'<path d="M{vx} {vy}L{x} {H}"/>' for x in range(-1600, 1700, 160))
    rows = "".join(f'<path d="M0 {vy + (H - vy) * (1 - 1 / (1 + i * .35)):.1f}H{W}"/>' for i in range(1, 16))
    ra, rb = proj(0), proj(150)
    rail = lambda f: f'<path class="hr" d="M{ra[0]:.1f} {ra[1] - ra[2] * f:.1f}L{rb[0]:.1f} {rb[1] - rb[2] * f:.1f}"/>'
    return f'''<svg class="hero-fence" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMax slice" aria-hidden="true" focusable="false">
<defs><radialGradient id="hf-sun" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="var(--accent)" stop-opacity=".55"/><stop offset=".4" stop-color="var(--accent)" stop-opacity=".16"/><stop offset="1" stop-color="var(--accent)" stop-opacity="0"/></radialGradient>
<linearGradient id="hf-pk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2b2219"/><stop offset=".1" stop-color="#120f0c"/><stop offset="1" stop-color="#080706"/></linearGradient>
<linearGradient id="hf-sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="var(--accent)" stop-opacity="0"/><stop offset=".55" stop-color="var(--accent)" stop-opacity=".05"/><stop offset="1" stop-color="var(--accent)" stop-opacity=".30"/></linearGradient>
<linearGradient id="hf-ground" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0d0f12" stop-opacity="0"/><stop offset=".25" stop-color="#0b0c0e"/><stop offset="1" stop-color="var(--bg)"/></linearGradient></defs>
<rect x="0" y="{vy - 340}" width="{W}" height="340" fill="url(#hf-sky)"/>
<g class="hero-fence__sun"><ellipse cx="{vx - 60}" cy="{vy - 20}" rx="760" ry="420" fill="url(#hf-sun)"/></g>
<path class="hero-fence__horizon" d="M0 {vy}H{W}"/>
<rect x="0" y="{vy}" width="{W}" height="{H - vy}" fill="url(#hf-ground)"/>
<g class="hero-fence__grid">{grid}{rows}</g>
<g class="hero-fence__rails">{rail(0.2)}{rail(0.78)}</g>
<g class="hero-fence__pk">{"".join(pickets)}{"".join(posts)}</g>
<path class="hero-fence__edge" d="M{proj(0)[0]:.1f} {proj(0)[1] - proj(0)[2]:.1f}{"".join(f"L{proj(i)[0]:.1f} {proj(i)[1] - proj(i)[2]:.1f}" for i in range(2, 151, 2))}"/>
</svg>'''


# ---------------------------------------------------------------- home: estimate teaser yard plan
def yard_plan_svg(total_label="186 FT", price_label="$9,850 – $12,600", material="Cedar privacy · 6 ft"):
    return f'''<svg class="yard" viewBox="0 0 420 380" role="img" aria-label="Illustration of a backyard plan with a fence line being measured, showing an example length and price range">
<rect x="1" y="1" width="418" height="378" rx="14" class="yard__bg"/>
<g class="yard__grid">{"".join(f'<path d="M{x} 20V360"/>' for x in range(40, 400, 20))}{"".join(f'<path d="M20 {y}H400"/>' for y in range(40, 360, 20))}</g>
<rect class="yard__lot" x="40" y="40" width="340" height="250"/>
<rect class="yard__house" x="110" y="214" width="200" height="76"/><text class="yard__lbl" x="210" y="258" text-anchor="middle">HOUSE</text>
<rect class="yard__pool" x="214" y="80" width="110" height="64" rx="10"/>
<path class="yard__tree" d="M88 104a22 22 0 1 0 0.1 0z"/>
<path class="yard__fence" pathLength="1" d="M110 214V40H380V214H310"/>
<g class="yard__gate"><path d="M110 214H80"/><circle cx="110" cy="214" r="4"/></g>
<g class="yard__posts">{"".join(f'<circle cx="{x}" cy="{y}" r="3.6" style="--k:{i}"/>' for i, (x, y) in enumerate([(110, 214), (110, 170), (110, 126), (110, 84), (110, 40), (154, 40), (200, 40), (245, 40), (290, 40), (335, 40), (380, 40), (380, 84), (380, 128), (380, 172), (380, 214), (345, 214), (310, 214)]))}</g>
<g class="yard__dim"><path d="M110 28H380M110 22V34M380 22V34"/><text x="245" y="22" text-anchor="middle">90 FT</text><path d="M394 40V214M388 40H400M388 214H400"/><text x="404" y="132" transform="rotate(90 404 132)" text-anchor="middle">58 FT</text></g>
<rect x="20" y="304" width="380" height="58" rx="8" class="yard__readout"/>
<text class="yard__k" x="38" y="327">{html.escape(material.upper())}</text><text class="yard__total" x="382" y="327" text-anchor="end">{html.escape(total_label)}</text>
<text class="yard__v" x="38" y="352">{html.escape(price_label)}</text><text class="yard__chip" x="382" y="352" text-anchor="end">EXAMPLE · NOT A QUOTE</text>
</svg>'''


# ---------------------------------------------------------------- home: "know the line" lot plan with locate marks
def locate_plan_svg(label):
    # utility colour code used for locate paint and flags: yellow gas, red electric, orange communications, blue water
    flags = [("gas", 120, 160), ("gas", 190, 175), ("gas", 260, 190), ("hydro", 330, 120), ("hydro", 330, 190), ("hydro", 330, 260),
             ("comm", 90, 250), ("comm", 160, 262), ("comm", 230, 274), ("water", 60, 120), ("water", 60, 190)]
    f = "".join(f'<g class="lp-flag lp-flag--{c}" style="--k:{i}"><path d="M{x} {y}v-22"/><path class="lp-flag__f" d="M{x} {y - 22}l14 5 -14 5z"/></g>' for i, (c, x, y) in enumerate(flags))
    return f'''<svg class="lot" viewBox="0 0 420 360" role="img" aria-label="{html.escape(label)}">
<rect x="1" y="1" width="418" height="358" rx="14" class="lot__bg"/>
<path class="lot__street" d="M0 330H420"/><text class="lot__lbl" x="210" y="350" text-anchor="middle">STREET</text>
<rect class="lot__house" x="120" y="210" width="170" height="80"/><text class="lot__lbl" x="205" y="255" text-anchor="middle">HOUSE</text>
<path class="lot__u lot__u--gas" d="M120 150L270 200V210"/><path class="lot__u lot__u--hydro" d="M330 60V300H290"/><path class="lot__u lot__u--comm" d="M40 240L260 280H290"/><path class="lot__u lot__u--water" d="M60 60V300H120"/>
<path class="lot__line" pathLength="1" d="M30 310V30H390V310"/>
<g class="lot__stakes">{"".join(f'<rect x="{x - 4}" y="{y - 4}" width="8" height="8" style="--k:{i}"/>' for i, (x, y) in enumerate([(30, 310), (30, 30), (390, 30), (390, 310)]))}</g>
{f}
<g class="lot__legend"><circle cx="34" cy="20" r="0"/></g>
</svg>'''
