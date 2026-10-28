#!/usr/bin/env python3
"""Generates logo, favicons and the default social-share image from the brand config.
Needs Pillow, fontTools and brotli:  pip install pillow fonttools brotli
Run after changing the business name or colours:  python3 _build/make_images.py"""
import json, os, io, math
from PIL import Image, ImageDraw, ImageFont
from fontTools.ttLib import TTFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CFG = json.load(open(os.path.join(HERE, "site.config.json")))
IMG = os.path.join(ROOT, "assets", "img")
os.makedirs(IMG, exist_ok=True)
ACCENT_HEX = (CFG.get("accent") or "#f5a524").strip()
HEAT_HEX = (CFG.get("accent_alt") or "#9fb4c7").strip()
BG, TEXT, MUTED = (10, 10, 11), (242, 239, 233), (160, 156, 148)
hexrgb = lambda h: tuple(int(h.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4))
ACCENT, HEAT = hexrgb(ACCENT_HEX), hexrgb(HEAT_HEX)
LOGO_FILE = (CFG.get("logo") or "").strip()

def font(name, size):
    f = TTFont(os.path.join(ROOT, "assets", "fonts", name))
    f.flavor = None
    buf = io.BytesIO(); f.save(buf); buf.seek(0)
    return ImageFont.truetype(buf, size)

def mark(draw, x, y, s, w=None):
    """Fence mark: three pointed pickets (the middle one in the accent colour) crossed by two rails."""
    k = s / 40
    P = lambda pts: [(x + px * k, y + py * k) for px, py in pts]
    draw.polygon(P([(5, 37), (5, 12), (9.5, 7), (14, 12), (14, 37)]), fill=TEXT)
    draw.polygon(P([(15.5, 37), (15.5, 8), (20, 3), (24.5, 8), (24.5, 37)]), fill=ACCENT)
    draw.polygon(P([(26, 37), (26, 12), (30.5, 7), (35, 12), (35, 37)]), fill=TEXT)
    draw.rectangle(P([(2, 16), (38, 19.4)]), fill=HEAT)
    draw.rectangle(P([(2, 28), (38, 31.4)]), fill=HEAT)

name = CFG["business_name"]
first, rest = name.split(" ")[0].upper(), " ".join(name.split(" ")[1:]).upper()

# favicon.svg
open(os.path.join(IMG, "favicon.svg"), "w").write(
 '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 40 40"><rect width="40" height="40" rx="7" fill="#0a0a0b"/>'
 '<g transform="translate(4 4) scale(.8)"><path d="M5 37V12l4.5-5 4.5 5v25z" fill="#f2efe9"/><path d="M15.5 37V8l4.5-5 4.5 5v29z" fill="' + ACCENT_HEX + '"/>'
 '<path d="M26 37V12l4.5-5 4.5 5v25z" fill="#f2efe9"/><rect x="2" y="16" width="36" height="3.4" fill="' + HEAT_HEX + '"/><rect x="2" y="28" width="36" height="3.4" fill="' + HEAT_HEX + '"/></g></svg>')

for size, fname in [(32, "favicon-32.png"), (180, "apple-touch-icon.png"), (512, "icon-512.png")]:
    S = size * 4
    im = Image.new("RGB", (S, S), BG); d = ImageDraw.Draw(im)
    pad = S * 0.14
    mark(d, pad, pad, S - 2 * pad)
    im.resize((size, size), Image.LANCZOS).save(os.path.join(IMG, fname))

# logo.png (for schema): the client's logo when supplied, otherwise mark + wordmark on dark
W, H = 1200, 300
im = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(im)
mark(d, 40, 40, 220)
d.text((300, 52), first, font=font("anton-latin-400-normal.woff2", 140), fill=TEXT)
d.text((306, 218), rest or CFG["short_tagline"].upper(), font=font("barlow-condensed-latin-600-normal.woff2", 44), fill=MUTED)
bbox = d.textbbox((300, 52), first, font=font("anton-latin-400-normal.woff2", 140))
sub = d.textbbox((306, 218), rest or CFG["short_tagline"].upper(), font=font("barlow-condensed-latin-600-normal.woff2", 44))
im = im.crop((0, 0, min(W, max(bbox[2], sub[2], 700) + 50), H))
if LOGO_FILE:
    src = Image.open(os.path.join(ROOT, LOGO_FILE.lstrip("/"))).convert("RGBA")
    src = src.crop(src.getchannel("A").getbbox() or (0, 0, src.width, src.height))
    if src.width > 1200:
        src = src.resize((1200, round(src.height * 1200 / src.width)), Image.LANCZOS)
    im = src
im.save(os.path.join(IMG, "logo.png"))

# og-default.png 1200x630: a fence line running to a glowing horizon, with the headline
W, H = 1200, 630
im = Image.new("RGB", (W, H), BG)
glow = Image.new("RGB", (W, H), BG); g = ImageDraw.Draw(glow)
vx, vy = 900, 440
for i in range(80):
    t = i / 80
    g.ellipse([vx - 760 * (1 - t), vy - 260 * (1 - t), vx + 760 * (1 - t), vy + 160 * (1 - t)], fill=tuple(int(BG[k] + (ACCENT[k] - BG[k]) * 0.34 * t) for k in range(3)))
im = Image.blend(im, glow, 1.0); d = ImageDraw.Draw(im)
d.rectangle([0, vy, W, H], fill=(9, 9, 10))
def proj(dd):
    sc = 1 / (1 + dd / 7)
    return vx + (1280 - vx) * sc, vy + (760 - vy) * sc, 520 * sc
dd = 0.0
pk = []
while dd < 160:
    x0, y0, h0 = proj(dd); x1, y1, h1 = proj(dd + 0.38)
    pk.append((x0, y0, h0, x1, y1, h1, dd))
    dd += 0.5
for x0, y0, h0, x1, y1, h1, dd in reversed(pk):
    d.polygon([(x0, y0), (x0, y0 - h0 * .93), ((x0 + x1) / 2, y0 - h0), (x1, y1 - h1 * .93), (x1, y1)], fill=(14, 13, 12))
    a = max(0.15, 1 - dd / 60)
    d.line([(x0, y0 - h0 * .93), ((x0 + x1) / 2, y0 - h0), (x1, y1 - h1 * .93)], fill=tuple(int(14 + (ACCENT[k] - 14) * 0.85 * a) for k in range(3)), width=2 if dd < 20 else 1)
d.rectangle([0, H - 12, W // 2, H], fill=ACCENT); d.rectangle([W // 2, H - 12, W, H], fill=HEAT)
mark(d, 70, 60, 90)
d.text((182, 70), first, font=font("anton-latin-400-normal.woff2", 64), fill=TEXT)
big = font("anton-latin-400-normal.woff2", 120)
d.text((70, 200), "SET DEEP.", font=big, fill=TEXT)
d.text((70, 330), "BUILT", font=big, fill=TEXT)
w2 = d.textlength("BUILT ", font=big)
d.text((70 + w2, 330), "STRAIGHT.", font=big, fill=ACCENT)
d.text((74, 540), f"FENCES & GATES  ·  INSTANT FENCE ESTIMATE  ·  {CFG['region_label'].upper()}", font=font("barlow-condensed-latin-600-normal.woff2", 32), fill=MUTED)
im.save(os.path.join(IMG, "og-default.png"), optimize=True)
print("Images written to assets/img/")
