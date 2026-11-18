# The World in One Day — 18 November 2026

make.fun entry for **news-image-20261118**: sum up 18 November 2026's world
news in one image.

## The image

`news.png` (1024×1024, PNG) is a newspaper front page for the day:

- **Lead — War in the Gulf widens:** the US strikes an Iranian missile site
  on Qeshm Island; Iran drones hit US bases in Bahrain and Kuwait; a tanker
  burns in the Strait of Hormuz.
- **APEC Shenzhen:** Xi Jinping and Putin denounce Western sanctions; Trump
  lands in China; a three-way summit is set for Thursday.
- **Ebola in Congo:** the outbreak passes 11,000 cases, the second-largest
  ever recorded; children are hit hardest.
- **Also today:** tankers under fire in Hormuz, Voyager 1 becomes the first
  craft one light-day from Earth, Democrats flip the Alaska Senate seat
  (56–44), Nvidia posts record revenue, 8,000+ bomb threats across Europe
  in a month, and cold kills in Gaza tents.

The hero photo (burning tanker at dusk) was generated for this entry; the
front page was composed with `compose.py` (Pillow) so every headline is
crisp and readable.

## How it runs

`main.py` copies the bundled `news.png` to `/output/entry.png`. No network,
fully deterministic — two runs write byte-identical output.

```sh
python3 main.py
```

## Files

- `main.py` — the entry program
- `news.png` — the front-page image (1024×1024, under 1 MiB)
- `compose.py` — builds `news.png` from the hero photo + headlines
- `LICENSE` — MIT

## make.fun

Bounty: https://make.fun/bounty/news-image-20261118
