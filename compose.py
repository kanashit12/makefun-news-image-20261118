#!/usr/bin/env python3
"""Compose the 18 Nov 2026 front-page image for make.fun news-image-20261118.

Layout: 1024x1024 newspaper front page. Masthead, AI-generated hero photo
(burning tanker, Strait of Hormuz), lead headline US-Iran strikes, two
second-story panels (APEC Shenzhen, Ebola Congo), bottom strip of six more
stories. Deterministic: same input -> same output bytes (PNG, fixed metadata
via Pillow default; no timestamps embedded by Pillow PNG encoder).
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
HERO = os.path.join(HERE, "assets",
                    "media-generation-hero-tanker-0-d78d3fae-d7ec-4a74-933d-4a881e07bda7.png")
OUT = os.path.join(HERE, "news.png")

W, H = 1024, 1024
NAVY = (16, 28, 51)
RED = (193, 18, 31)
DARKRED = (140, 20, 28)
INK = (20, 20, 20)
GREY = (70, 70, 70)
PANEL = (244, 244, 244)
RULE = (210, 210, 210)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def main():
    img = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(img)

    # --- masthead ---
    d.rectangle([0, 0, W, 78], fill=NAVY)
    d.text((28, 14), "THE WORLD IN ONE PAGE", font=font(SERIF_B, 44), fill="white")
    d.text((996, 20), "TUESDAY", font=font(SANS_B, 20), fill=(180, 190, 205),
           anchor="ra")
    d.text((996, 44), "18 NOV 2026", font=font(SANS_B, 24), fill="white", anchor="ra")
    d.rectangle([0, 78, W, 84], fill=RED)

    # --- hero photo: center-crop 1920x1280 -> 1024x386 ---
    hero = Image.open(HERO).convert("RGB")
    ch = int(1920 * 386 / 1024)
    y0 = (1280 - ch) // 2
    hero = hero.crop((0, y0, 1920, y0 + ch)).resize((1024, 386), Image.LANCZOS)
    img.paste(hero, (0, 84))

    # --- kicker + lead headline ---
    d.rectangle([0, 470, W, 506], fill=RED)
    d.text((28, 477), "WAR IN THE GULF  —  STRAIT OF HORMUZ",
           font=font(SANS_B, 24), fill="white")
    d.text((28, 516), "US STRIKES IRAN MISSILE SITE", font=font(SERIF_B, 38), fill=INK)
    d.text((28, 562), "ON QESHM ISLAND — TEHRAN HITS BACK",
           font=font(SERIF_B, 38), fill=INK)
    sub = ("Iran retaliates on US bases in Bahrain and Kuwait; a tanker burns in "
           "the Strait of Hormuz as shipping braces for closure.")
    y = 616
    for line in wrap(d, sub, font(SANS, 21), 968):
        d.text((28, y), line, font=font(SANS, 21), fill=GREY)
        y += 27

    d.line([(28, 684), (996, 684)], fill=RULE, width=2)

    # --- middle row: two panels ---
    def panel(x, w, bar, bar_text, head, body):
        d.rectangle([x, 700, x + w, 734], fill=bar)
        d.text((x + 14, 706), bar_text, font=font(SANS_B, 21), fill="white")
        d.rectangle([x, 734, x + w, 880], fill=PANEL)
        yy = 746
        for line in wrap(d, head, font(SERIF_B, 29), w - 28):
            d.text((x + 14, yy), line, font=font(SERIF_B, 29), fill=INK)
            yy += 34
        yy += 6
        for line in wrap(d, body, font(SANS, 19), w - 28):
            d.text((x + 14, yy), line, font=font(SANS, 19), fill=GREY)
            yy += 23

    panel(28, 472, NAVY, "APEC  •  SHENZHEN",
          "XI AND PUTIN DENOUNCE SANCTIONS",
          "Trump lands in China; three-way summit Thursday.")
    panel(524, 472, DARKRED, "EBOLA  •  CONGO",
          "EBOLA PASSES 11,000 CASES",
          "Second-largest ever; children hit hardest.")

    d.line([(28, 896), (996, 896)], fill=RULE, width=2)
    d.text((28, 906), "ALSO TODAY", font=font(SANS_B, 20), fill=RED)

    items = [
        ("VOYAGER 1 — ", "First craft one light-day out."),
        ("ALASKA — ", "Democrats flip Senate seat, 56–44."),
        ("MEASLES — ", "US loses elimination status, 26 yrs."),
        ("NVIDIA — ", "Record revenue; board blocks Huang."),
        ("EUROPE — ", "8,000+ bomb threats in a month."),
        ("GAZA — ", "Cold kills in tents as truce frays."),
    ]
    col_x = [28, 524]
    y = 936
    for i, (lead, body) in enumerate(items):
        x = col_x[i % 2]
        if i % 2 == 0 and i > 0:
            y += 26
        line = lead + body
        assert d.textlength(line, font=font(SANS, 18)) <= 448, line
        lead_w = d.textlength(lead, font=font(SANS_B, 18))
        d.text((x, y), lead, font=font(SANS_B, 18), fill=INK)
        d.text((x + lead_w, y), body, font=font(SANS, 18), fill=INK)

    img.save(OUT, optimize=True)
    print("saved", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
