#!/usr/bin/env python3
"""VELMARA: a travel poster for a town that does not exist.

Deterministic flat travel poster drawn with PIL at 2x supersampling,
then downscaled to 896 x 1024 and finished with seeded paper grain
and a soft vignette. The only text in the picture is the name VELMARA.
"""
import random

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

SS = 2                      # supersample factor
W, H = 896, 1024            # final size
W2, H2 = W * SS, H * SS
FONT = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
OUT = "poster.png"

rng = random.Random(20261121)

# Palette
CORAL_DEEP = (201, 62, 38)
CORAL = (224, 84, 48)
APRICOT = (238, 118, 54)
APRICOT_LT = (246, 152, 66)
GOLD = (250, 184, 84)
GOLD_LT = (252, 210, 120)
CREAM = (253, 240, 208)
CREAM_PURE = (255, 246, 220)
SUN = (255, 243, 205)
TEAL_BACK = (74, 148, 140)
TEAL_MID = (38, 106, 106)
TEAL_DARK = (20, 72, 76)
TEAL_FACET = (29, 90, 94)
WATER = (43, 176, 160)
WATER_LT = (94, 205, 188)
WATER_DK = (32, 150, 142)
WHITE = (252, 248, 238)
TERRA = (196, 84, 50)
TERRA_DK = (168, 66, 40)
RED = (206, 52, 44)
ROCK = (146, 74, 52)


def s(v):
    return int(round(v * SS))


def pts(seq):
    return [(s(x), s(y)) for x, y in seq]


img = Image.new("RGB", (W2, H2), CREAM)
d = ImageDraw.Draw(img, "RGBA")

# --- Sky: flat horizontal dawn bands -------------------------------------
bands = [
    (0, 120, CORAL_DEEP),
    (120, 235, CORAL),
    (235, 345, APRICOT),
    (345, 450, APRICOT_LT),
    (450, 545, GOLD),
    (545, 640, GOLD_LT),
    (640, 700, CREAM),
]
for y0, y1, col in bands:
    d.rectangle([0, s(y0), W2, s(y1)], fill=col)

# --- Sun: one large low disc ---------------------------------------------
sun_cx, sun_cy, sun_r = 585, 505, 148
d.ellipse([s(sun_cx - sun_r), s(sun_cy - sun_r),
           s(sun_cx + sun_r), s(sun_cy + sun_r)], fill=SUN)

# --- Lighthouse beam (soft, under the hills so it stays subtle) ----------
beam = [(s(408), s(468)), (s(760), s(392)), (s(760), s(470)), (s(408), s(492))]
d.polygon(beam, fill=(255, 244, 200, 46))

# --- Water base ------------------------------------------------------------
d.rectangle([0, s(615), W2, H2], fill=WATER)
d.rectangle([0, s(615), W2, s(660)], fill=WATER_LT)
# sun glitter: broken cream dashes under the sun
for i, (gw, gy) in enumerate([(190, 700), (150, 736), (205, 776), (120, 818),
                              (165, 862), (95, 908)]):
    gx = sun_cx - gw // 2 + rng.randint(-16, 16)
    d.rounded_rectangle([s(gx), s(gy), s(gx + gw), s(gy + 9)],
                        radius=s(5), fill=(255, 244, 205, 150 - i * 14))
# a darker flat sweep in the lower bay
d.polygon(pts([(0, 940), (420, 880), (896, 960), (896, 1024), (0, 1024)]),
          fill=WATER_DK)

# --- Layered headlands -----------------------------------------------------
# back left hill
d.polygon(pts([(0, 400), (150, 452), (300, 560), (360, 640), (0, 660)]),
          fill=TEAL_BACK)
# back right headland
d.polygon(pts([(896, 330), (730, 420), (600, 545), (560, 640),
               (640, 660), (896, 640)]), fill=TEAL_BACK)
# mid right headland
d.polygon(pts([(896, 455), (770, 530), (690, 625), (700, 690), (896, 700)]),
          fill=TEAL_MID)
# main headland, left, carrying the village and the point
main_head = [(0, 445), (120, 478), (235, 540), (330, 600), (415, 652),
             (448, 676), (420, 700), (300, 712), (120, 724), (0, 730)]
d.polygon(pts(main_head), fill=TEAL_DARK)
# cliff facet and a warm rock face near the point
d.polygon(pts([(235, 540), (330, 600), (415, 652), (448, 676), (420, 700),
               (300, 690), (250, 620)]), fill=TEAL_FACET)
d.polygon(pts([(360, 622), (415, 652), (448, 676), (420, 700), (372, 678)]),
          fill=ROCK)

# --- Village: small white cubic houses, terracotta roofs -------------------
houses = [
    (52, 470, 46, 36), (108, 486, 40, 32), (160, 500, 48, 38),
    (70, 512, 38, 30), (128, 528, 44, 34), (196, 540, 40, 32),
    (238, 566, 44, 34), (168, 566, 36, 28), (104, 556, 40, 30),
    (282, 596, 38, 30), (222, 600, 34, 26),
]
for hx, hy, hw, hh in houses:
    d.rectangle([s(hx), s(hy), s(hx + hw), s(hy + hh)], fill=WHITE)
    roof_h = 13
    d.polygon(pts([(hx - 4, hy), (hx + hw + 4, hy),
                   (hx + hw - 6, hy - roof_h), (hx + 6, hy - roof_h)]),
              fill=TERRA)
    # one small dark window
    wx = hx + hw // 2 - 4
    d.rectangle([s(wx), s(hy + hh // 2), s(wx + 8), s(hy + hh // 2 + 10)],
                fill=TEAL_DARK)

# --- The landmark: striped lighthouse on the point -------------------------
lx = 408            # centre x of the tower
base_y = 668
top_y = 486
base_w, top_w = 46, 32
stripe_h = (base_y - top_y) // 5
for i in range(5):
    yb = base_y - i * stripe_h
    yt = yb - stripe_h
    wb = base_w - (base_w - top_w) * (base_y - yb) / (base_y - top_y)
    wt = base_w - (base_w - top_w) * (base_y - yt) / (base_y - top_y)
    col = WHITE if i % 2 == 0 else RED
    d.polygon(pts([(lx - wb / 2, yb), (lx + wb / 2, yb),
                   (lx + wt / 2, yt), (lx - wt / 2, yt)]), fill=col)
# gallery, lamp room and cap
d.rectangle([s(lx - 26), s(top_y - 12), s(lx + 26), s(top_y)], fill=TEAL_DARK)
d.rectangle([s(lx - 13), s(top_y - 34), s(lx + 13), s(top_y - 12)],
            fill=(255, 226, 140))
d.polygon(pts([(lx - 18, top_y - 34), (lx + 18, top_y - 34), (lx, top_y - 56)]),
          fill=TERRA_DK)
d.ellipse([s(lx - 7), s(top_y - 30), s(lx + 7), s(top_y - 16)],
          fill=(255, 250, 220))

# --- Boats: two small white sails on the bay --------------------------------
def boat(cx, cy, scale, flip=False):
    f = -1 if flip else 1
    d.polygon(pts([(cx - 34 * scale, cy), (cx + 34 * scale, cy),
                   (cx + 22 * scale, cy + 13 * scale),
                   (cx - 22 * scale, cy + 13 * scale)]), fill=TEAL_DARK)
    d.polygon(pts([(cx, cy - 52 * scale), (cx, cy - 2),
                   (cx + 30 * f * scale, cy - 2)]), fill=WHITE)
    d.polygon(pts([(cx - 4 * f * scale, cy - 40 * scale),
                   (cx - 4 * f * scale, cy - 2),
                   (cx - 24 * f * scale, cy - 2)]), fill=CREAM_PURE)

boat(618, 792, 1.0)
boat(742, 898, 0.72, flip=True)

# --- Birds: a few tiny silhouettes ------------------------------------------
def bird(cx, cy, w):
    d.arc([s(cx - w), s(cy - w * 0.55), s(cx), s(cy + w * 0.55)],
          start=300, end=35, fill=TEAL_DARK, width=s(3))
    d.arc([s(cx), s(cy - w * 0.55), s(cx + w), s(cy + w * 0.55)],
          start=145, end=240, fill=TEAL_DARK, width=s(3))

bird(196, 268, 15)
bird(238, 292, 11)
bird(716, 214, 13)
bird(758, 240, 10)

# --- The name: VELMARA, the only text ---------------------------------------
text = "VELMARA"
size = 116
font = ImageFont.truetype(FONT, s(size))
spacing = s(16)
widths = []
for ch in text:
    bb = d.textbbox((0, 0), ch, font=font)
    widths.append(bb[2] - bb[0])
total = sum(widths) + spacing * (len(text) - 1)
x = (W2 - total) // 2
ty = s(74)
# flat offset shadow in deep coral, then cream on top
for dx, dy, col in [(s(4), s(5), (168, 52, 30)), (0, 0, CREAM_PURE)]:
    cx = x + dx
    for ch, chw in zip(text, widths):
        bb = d.textbbox((0, 0), ch, font=font)
        d.text((cx - bb[0], ty + dy - bb[1]), ch, font=font, fill=col)
        cx += chw + spacing

# --- Cream border frame with a thin coral inner line -------------------------
d.rectangle([0, 0, W2 - 1, H2 - 1], outline=CREAM_PURE, width=s(20))
d.rectangle([s(30), s(30), W2 - s(30), H2 - s(30)], outline=CORAL, width=s(3))

# --- Downscale, grain, vignette ----------------------------------------------
img = img.resize((W, H), Image.LANCZOS)

arr = np.asarray(img).astype(np.float32)
noise = np.random.default_rng(20261121).normal(0, 5.5, arr.shape[:2])[..., None]
arr = np.clip(arr + noise, 0, 255)

yy, xx = np.mgrid[0:H, 0:W]
dist = np.sqrt(((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2)
vig = 1.0 - 0.16 * np.clip(dist - 0.55, 0, None) ** 2
arr = np.clip(arr * vig[..., None], 0, 255).astype(np.uint8)

out = Image.fromarray(arr, "RGB")
# A flat poster lives happily in a 256 colour palette, and the palette
# keeps the file well under the 1 MiB cap despite the paper grain.
out = out.quantize(colors=256, method=Image.MEDIANCUT,
                   dither=Image.FLOYDSTEINBERG)
out.save(OUT, optimize=True)
print("wrote", OUT, out.size)
