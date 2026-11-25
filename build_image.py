#!/usr/bin/env python3
"""Draw the front page of THE WORLD TODAY for Wednesday 25 November 2026.

One 1024x1024 PNG: a masthead, one lead story (Shenzhou-24 / first
Pakistani in orbit, with an AI-generated launch illustration), three
news panels and an "Also today" strip. Headlines and panels are drawn
with plain PIL shapes and DejaVu type; the hero art is a committed
asset (hero.png) pasted in. Fully deterministic: no network, no clock,
no randomness.
Run:  python3 build_image.py   -> writes entry.png next to this file.
"""

import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
HERE = os.path.dirname(os.path.abspath(__file__))

PAPER = (247, 243, 232)
INK = (22, 22, 22)
RED = (178, 34, 34)
BLUE = (28, 68, 128)
STEEL = (70, 90, 120)
NIGHT = (18, 30, 58)
GOLD = (198, 148, 52)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)   # noqa: E731
SERIF = lambda s: font("DejaVuSerif.ttf", s)         # noqa: E731
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)     # noqa: E731
SANS = lambda s: font("DejaVuSans.ttf", s)            # noqa: E731


def wrap(draw, text, fnt, width):
    """Greedy word wrap; returns a list of lines that fit `width` px."""
    lines, cur = [], ""
    for word in text.split():
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, text, fnt, width, fill=INK, leading=None):
    """Draw wrapped text; returns the y just below the last line."""
    lh = leading if leading is not None else int(fnt.size * 1.28)
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += lh
    return y


def rule(draw, x0, y, x1, width=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def kicker(draw, x, y, text, color=RED, size=16):
    f = SANS_B(size)
    draw.text((x, y), text.upper(), font=f, fill=color)
    return y + size + 6


def draw_chip_art(draw, box):
    """A microchip with circuit traces (Huawei verdict panel)."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(26, 34, 46))
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    for gx in range(x0 + 16, x1 - 16, 28):
        draw.line([(gx, y0 + 6), (gx, y1 - 6)], fill=(60, 120, 90), width=2)
    for gy in range(y0 + 12, y1 - 12, 28):
        draw.line([(x0 + 6, gy), (x1 - 6, gy)], fill=(60, 120, 90), width=2)
    draw.rectangle([cx - 62, cy - 22, cx + 62, cy + 22], fill=(16, 22, 32),
                   outline=(120, 200, 160), width=2)
    draw.rectangle([cx - 40, cy - 13, cx + 40, cy + 13], fill=(52, 120, 84))
    draw.text((cx - 32, cy - 12), "AI", font=SANS_B(22), fill=(255, 255, 255))
    for i in range(6):
        px = cx - 48 + i * 20
        draw.rectangle([px, cy - 30, px + 8, cy - 22], fill=(180, 190, 200))
        draw.rectangle([px, cy + 22, px + 8, cy + 30], fill=(180, 190, 200))


def draw_shield_art(draw, box):
    """A cracked shield over a dark server wall (CIA breach panel)."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(20, 28, 44))
    # server racks
    for i in range(9):
        sx = x0 + 8 + i * 30
        draw.rectangle([sx, y0 + 6, sx + 22, y1 - 6], fill=(38, 52, 74),
                       outline=(90, 110, 140), width=1)
        for j in range(3):
            draw.rectangle([sx + 4, y0 + 10 + j * 14, sx + 10, y0 + 16 + j * 14],
                           fill=(90, 200, 120) if (i + j) % 3 else (220, 80, 60))
    # shield in the middle
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    shield = [(cx, cy - 24), (cx + 22, cy - 14), (cx + 22, cy + 4),
              (cx, cy + 24), (cx - 22, cy + 4), (cx - 22, cy - 14)]
    draw.polygon(shield, fill=(198, 148, 52), outline=(240, 220, 160), width=2)
    draw.line([(cx, cy - 14), (cx + 12, cy + 6)], fill=RED, width=3)
    draw.line([(cx - 10, cy - 2), (cx + 2, cy + 14)], fill=RED, width=3)


def draw_tower_art(draw, box):
    """A tall tower at dusk with a small drone above it (Riyadh panel)."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(232, 190, 130))
    # dusk sky gradient bands
    draw.rectangle([x0, y0, x1, y0 + 18], fill=(214, 140, 90))
    # city blocks
    for bx, bh in ((8, 18), (52, 26), (96, 14)):
        draw.rectangle([x0 + bx, y1 - bh, x0 + bx + 36, y1], fill=(90, 70, 80))
    # the tower
    tx = x0 + 190
    draw.polygon([(tx - 16, y1), (tx - 8, y0 + 6), (tx + 8, y0 + 6),
                  (tx + 16, y1)], fill=(70, 80, 110), outline=INK, width=2)
    for wy in range(y0 + 16, y1 - 6, 12):
        draw.rectangle([tx - 5, wy, tx + 5, wy + 6], fill=GOLD)
    # drone + warning flash
    dx, dy = x0 + 250, y0 + 12
    draw.ellipse([dx - 8, dy - 4, dx + 8, dy + 4], fill=INK)
    draw.line([(dx - 16, dy - 8), (dx + 16, dy - 8)], fill=INK, width=2)
    draw.line([(dx - 16, dy + 8), (dx + 16, dy + 8)], fill=INK, width=2)
    draw.polygon([(dx + 26, dy + 2), (dx + 34, dy + 8), (dx + 26, dy + 12)],
                 fill=RED)


def panel(draw, x, y, w, h, kicker_text, headline, body, art_fn):
    draw.rectangle([x, y, x + w, y + h], outline=INK, width=2)
    aw, ah = w - 20, 54
    art_fn(draw, (x + 10, y + 10, x + 10 + aw, y + 10 + ah))
    ty = kicker(draw, x + 10, y + 10 + ah + 6, kicker_text, size=15)
    ty = text_block(draw, x + 10, ty + 2, headline, SERIF_B(22), w - 20,
                    leading=26)
    text_block(draw, x + 10, ty + 4, body, SANS(15), w - 20, leading=20)


def hero_image():
    """Load the committed hero art, cropped to the 964x270 band."""
    src = Image.open(os.path.join(HERE, "hero.png")).convert("RGB")
    return src


def render():
    """Draw the front page and return the PIL Image (no file written)."""
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    m = 30  # margin
    # ---- masthead ----
    rule(d, m, 22, W - m, 3)
    d.text((m, 32), "THE WORLD TODAY", font=SERIF_B(84), fill=INK)
    rule(d, m, 126, W - m, 2)
    d.text((m, 136), "WEDNESDAY 25 NOVEMBER 2026", font=SANS_B(22), fill=RED)
    d.text((W - m - d.textlength("WORLD NEWS IN ONE PAGE", font=SANS_B(19)),
            138), "WORLD NEWS IN ONE PAGE", font=SANS_B(19), fill=INK)
    rule(d, m, 168, W - m, 3)

    # ---- lead story ----
    ly = 178
    kicker(d, m, ly, "Lead — Space · China / Pakistan", size=16)
    y = text_block(d, m, ly + 26, "FIRST PAKISTANI IN ORBIT",
                   SERIF_B(52), W - 2 * m, leading=58)
    deck = ("Shenzhou-24 blasts off from Jiuquan at 08:18 Beijing time with "
            "Tang Hongbo, Wu Yi and Muhammad Zeeshan Ali — the first foreign "
            "astronaut ever to visit Tiangong.")
    y = text_block(d, m, y + 6, deck, SERIF(20), W - 2 * m, leading=26)

    # ---- hero art (full width) ----
    hy = 330
    img.paste(hero_image(), (m, hy))
    d.text((m, hy + 276),
           "Shenzhou-24 lifts off from Jiuquan, 25 November 2026. (Illustration)",
           font=SANS(14), fill=STEEL)
    rule(d, m, 630, W - m, 2)

    # ---- three panels, one row ----
    pw, ph = 305, 240
    gy = 644
    panel(d, m, gy, pw, ph, "United States · Courts",
          "HUAWEI FOUND GUILTY",
          "A New York jury convicts Huawei on 10 of 12 counts, including "
          "trade-secret theft and bank fraud, after a three-month trial. "
          "— Reuters",
          draw_chip_art)
    panel(d, m + pw + 24, gy, pw, ph, "United States · Security",
          "CIA AND ODNI BREACHED",
          "The CIA and the director of national intelligence\u2019s office "
          "are hit by a cyberattack affecting classified systems, "
          "sources say. — CNN",
          draw_shield_art)
    panel(d, m + 2 * (pw + 24), gy, pw, ph, "Middle East · Saudi Arabia",
          "DRONE HITS RIYADH TOWER",
          "A Houthi drone strikes Riyadh\u2019s tallest tower, wounding 11, "
          "as fighting closes in on Aden. — Reuters",
          draw_tower_art)

    # ---- also today strip ----
    ay = 898
    rule(d, m, ay, W - m, 3)
    d.text((m, ay + 10), "ALSO TODAY", font=SANS_B(18), fill=RED)
    items = ("Gaza strike kills a Hamas security chief  \u2022  Nepal quake "
             "5.6  \u2022  Zelenskiy confirms Ukraine hit a Russian ship in "
             "the Gulf of Finland  \u2022  Malaysia to send 6,500 Rohingya "
             "back  \u2022  AIDS deaths lowest in 20+ years")
    text_block(d, m, ay + 36, items, SANS(17), W - 2 * m, leading=23)
    d.text((m, H - 26),
           "Sources: Reuters, AP, Xinhua. Hero art: AI-generated illustration.",
           font=SANS(14), fill=STEEL)
    return img


def build():
    """Render the front page and save it as entry.png next to this file."""
    img = render()
    out = os.path.join(HERE, "entry.png")
    img.save(out, "PNG")
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    build()
