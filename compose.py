"""Build the 18 Nov 2026 front page (1024x1024 PNG) from the hero photo.

Layout: masthead, hero photo with caption, lead story, 2x2 story grid,
ticker strip, footer. All text is drawn with PIL so the page is readable
at a glance; the hero is the only photographic element.
"""
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
W, H = 1024, 1024
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, fnt, width, fill="black", leading=4):
    lines = wrap(draw, text, fnt, width)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += fnt.size + leading
    return y


def main():
    img = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W - 1, H - 1], outline="black", width=4)

    # Masthead
    d.text((512, 18), "THE WORLD IN ONE DAY", font=font(SERIF_B, 58),
           fill="black", anchor="ma")
    d.text((512, 92), "WEDNESDAY 18 NOVEMBER 2026  •  TEN STORIES, ONE PAGE",
           font=font(SANS_B, 20), fill="black", anchor="ma")
    d.line([(24, 128), (1000, 128)], fill="black", width=3)

    # Hero photo
    hero = Image.open(HERE / "media-generation-hero-tanker-18nov-0-399a38bf-7e39-4670-a39c-22fce1a0ad09.png").convert("RGB")
    tw, th = 976, 300
    ratio = max(tw / hero.width, th / hero.height)
    hero = hero.resize((int(hero.width * ratio) + 1, int(hero.height * ratio) + 1))
    x0 = (hero.width - tw) // 2
    y0 = (hero.height - th) // 2
    hero = hero.crop((x0, y0, x0 + tw, y0 + th))
    img.paste(hero, (24, 140))
    d.rectangle([24, 140, 1000, 440], outline="black", width=2)
    d.text((24, 448), "A tanker burns in the Strait of Hormuz after a night of strikes.",
           font=font(SANS, 17), fill="#333333")

    # Lead story
    y = draw_wrapped(d, 24, 478, "WAR IN THE GULF WIDENS: US HITS QESHM, IRAN HITS BACK",
                     font(SERIF_B, 34), 976, leading=2)
    y = draw_wrapped(d, 24, y + 2,
                     "US jets strike an Iranian missile site on Qeshm Island; Iran drones hit "
                     "US bases in Bahrain and Kuwait as tankers come under fire in Hormuz.",
                     font(SERIF, 21), 976, leading=2)

    d.line([(24, y + 10), (1000, y + 10)], fill="black", width=2)
    gy = y + 22

    # 2x2 grid of stories
    stories = [
        ("APEC SHENZHEN",
         "Xi and Putin denounce Western sanctions; Trump lands in China and a "
         "three-way summit is set for Thursday."),
        ("EBOLA PASSES 11,000",
         "Congo's outbreak becomes the second-largest ever recorded; children "
         "are hit hardest as clinics run out of beds."),
        ("TANKERS UNDER FIRE",
         "An ADNOC vessel is attacked, 11 crew hurt and one missing; the Tara Gas "
         "burns and 24 crew are evacuated off Oman."),
        ("VOYAGER 1, ONE LIGHT-DAY",
         "Voyager 1 becomes the first craft one light-day from Earth, still "
         "sending data home after 49 years in space."),
    ]
    col_w, row_h = 478, 132
    for i, (head, body) in enumerate(stories):
        cx = 24 + (i % 2) * 498
        cy = gy + (i // 2) * row_h
        if i % 2 == 1:
            d.line([(512, cy), (512, cy + row_h - 14)], fill="#999999", width=1)
        draw_wrapped(d, cx, cy, head, font(SANS_B, 21), col_w, leading=1)
        draw_wrapped(d, cx, cy + 30, body, font(SANS, 17), col_w, leading=1)

    ty = gy + 2 * row_h + 6
    d.line([(24, ty), (1000, ty)], fill="black", width=2)
    ticker = ("ALSO TODAY:  Democrats flip the Alaska Senate seat 56-44  •  Nvidia posts record revenue  •  "
              "8,000+ bomb threats across Europe in a month  •  Cold kills in Gaza tents  •  "
              "Kerch bridge still closed after Tuesday's strike")
    ty = draw_wrapped(d, 24, ty + 10, ticker, font(SANS_B, 17), 976, leading=3)
    d.text((512, 992), "THE WORLD IN ONE DAY — 18 NOVEMBER 2026",
           font=font(SANS, 15), fill="#555555", anchor="ma")
    img.save(HERE / "news.png", optimize=True)
    print("wrote", HERE / "news.png", (HERE / "news.png").stat().st_size)


if __name__ == "__main__":
    main()
