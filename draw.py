#!/usr/bin/env python3
"""One-page front page for Saturday 21 November 2026.

Eight stories from the day, laid out as a newspaper: a black masthead
naming the date, a wide lead panel for the missile strike on Kryvyi
Rih, then seven smaller panels for Mexico, the Strait of Hormuz, the
markets, COP31, the EU tech tax, Myanmar and AI weapons. Only Pillow
primitives are used; there are no photos or outside assets.

Run it from this directory and it writes entry.png next to itself.
"""
from math import cos, pi, sin
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

CANVAS = (1024, 1024)
BG = (247, 243, 232)
FG = (18, 18, 20)
GREY = (92, 88, 80)
CARD = (255, 254, 248)
CARD2 = (238, 233, 218)
CRIMSON = (178, 34, 40)
NAVY = (28, 74, 140)
TEAL = (14, 116, 110)
GOLD = (196, 138, 18)
LEAF = (38, 110, 52)
PLUM = (94, 52, 140)
EMBER = (214, 96, 20)

_DEJA = Path("/usr/share/fonts/truetype/dejavu")


def _font(name, size):
    return ImageFont.truetype(str(_DEJA / name), size)


def _serif(size):
    return _font("DejaVuSerif-Bold.ttf", size)


def _bold(size):
    return _font("DejaVuSans-Bold.ttf", size)


def _plain(size):
    return _font("DejaVuSans.ttf", size)


def _split(d, words, font, width):
    """Greedy word wrap: returns the lines that fit inside width."""
    out, current = [], ""
    for word in words.split():
        trial = word if not current else current + " " + word
        if d.textlength(trial, font=font) <= width:
            current = trial
        else:
            if current:
                out.append(current)
            current = word
    if current:
        out.append(current)
    return out


def _para(d, x, y, text, font, color, width, gap=4):
    for line in _split(d, text, font, width):
        d.text((x, y), line, font=font, fill=color)
        y += font.size + gap
    return y


class Sheet:
    """The drawing surface plus the small layout helpers."""

    def __init__(self):
        self.img = Image.new("RGB", CANVAS, BG)
        self.d = ImageDraw.Draw(self.img)

    def card(self, x0, y0, x1, y1, accent):
        self.d.rectangle([x0, y0, x1, y1], fill=CARD, outline=FG, width=2)
        self.d.rectangle([x0, y0, x1, y0 + 7], fill=accent)

    def tag(self, x, y, text, color):
        self.d.text((x, y), text, font=_bold(15), fill=color)
        return y + 21

    def head(self, x, y, text, size, width):
        return _para(self.d, x, y, text, _bold(size), FG, width, gap=2)

    def blurb(self, x, y, text, size, width):
        return _para(self.d, x, y, text, _plain(size), GREY, width, gap=3)

    def chip(self, x, y, text):
        self.d.rectangle([x, y, x + 178, y + 36], fill=CARD2, outline=FG,
                         width=2)
        self.d.text((x + 10, y + 10), text, font=_bold(15), fill=FG)


def _burst(d, cx, cy):
    """City blocks under an explosion star."""
    for left, wide in ((-44, 34), (-14, 40), (20, 36)):
        d.rectangle([cx + left, cy + 6, cx + left + wide, cy + 26], fill=FG)
    d.rectangle([cx - 52, cy + 26, cx + 52, cy + 30], fill=FG)
    star = [(cx + (34 if k % 2 == 0 else 16) * cos(pi * k / 6),
             cy - 6 + (34 if k % 2 == 0 else 16) * sin(pi * k / 6))
            for k in range(12)]
    d.polygon(star, fill=EMBER)
    d.ellipse([cx - 9, cy - 15, cx + 9, cy + 3], fill=CRIMSON)


def _cuffs(d, cx, cy):
    """Two linked rings and a WANTED tag."""
    d.ellipse([cx - 40, cy - 18, cx - 8, cy + 14], outline=FG, width=5)
    d.ellipse([cx + 8, cy - 18, cx + 40, cy + 14], outline=FG, width=5)
    d.line([cx - 8, cy - 2, cx + 8, cy - 2], fill=FG, width=4)
    d.rectangle([cx - 4, cy - 8, cx + 4, cy + 4], fill=GOLD)
    d.text((cx - 22, cy + 20), "WANTED", font=_bold(14), fill=CRIMSON)


def _tanker(d, cx, cy):
    """Oil tanker taking a hit: flame, smoke, sea line."""
    d.polygon([(cx - 46, cy - 2), (cx + 46, cy - 2), (cx + 38, cy + 22),
               (cx - 38, cy + 22)], fill=FG)
    for off in (-30, -8, 14):
        d.rectangle([cx + off, cy - 18, cx + off + 18, cy - 2], fill=NAVY)
    d.rectangle([cx + 30, cy - 26, cx + 42, cy - 2], fill=CRIMSON)
    flame = [(cx - 22 + (20 if k % 2 == 0 else 10) * cos(pi * k / 5),
              cy - 30 + (20 if k % 2 == 0 else 10) * sin(pi * k / 5))
             for k in range(10)]
    d.polygon(flame, fill=EMBER)
    d.ellipse([cx - 46, cy - 52, cx - 30, cy - 36], fill=GREY)
    d.ellipse([cx + 18, cy - 56, cx + 34, cy - 40], fill=GREY)
    d.line([cx - 52, cy + 28, cx + 52, cy + 28], fill=TEAL, width=3)


def _plunge(d, cx, cy):
    """Axes and a falling line with a red arrowhead."""
    d.line([cx - 38, cy + 28, cx + 40, cy + 28], fill=FG, width=3)
    d.line([cx - 38, cy + 28, cx - 38, cy - 28], fill=FG, width=3)
    pts = [(cx - 32, cy - 18), (cx - 12, cy - 4), (cx + 6, cy - 10),
           (cx + 30, cy + 18)]
    d.line(pts, fill=CRIMSON, width=5)
    d.polygon([(cx + 30, cy + 18), (cx + 18, cy + 14), (cx + 26, cy + 4)],
              fill=CRIMSON)
    d.text((cx - 34, cy - 34), "-5.1%", font=_bold(15), fill=CRIMSON)


def _draft(d, cx, cy):
    """A document page with its green leaf crossed out."""
    d.rectangle([cx - 26, cy - 30, cx + 26, cy + 30], fill=(255, 255, 255),
                outline=FG, width=3)
    for yy in (-16, -4, 8):
        d.line([cx - 18, cy + yy, cx + 18, cy + yy], fill=GREY, width=2)
    d.ellipse([cx - 8, cy + 14, cx + 8, cy + 26], fill=LEAF)
    d.line([cx - 12, cy + 10, cx + 12, cy + 30], fill=CRIMSON, width=4)
    d.line([cx + 12, cy + 10, cx - 12, cy + 30], fill=CRIMSON, width=4)


def _euro(d, cx, cy):
    """Gold coin stamped with a euro sign."""
    d.ellipse([cx - 32, cy - 32, cx + 32, cy + 32], fill=GOLD, outline=FG,
              width=3)
    d.ellipse([cx - 24, cy - 24, cx + 24, cy + 24], outline=FG, width=2)
    d.text((cx - 13, cy - 20), "€", font=_bold(40), fill=FG)


def _scales(d, cx, cy):
    """A balance: post, beam, two pans, base."""
    d.line([cx, cy - 30, cx, cy + 28], fill=FG, width=4)
    d.line([cx - 34, cy - 30, cx + 34, cy - 30], fill=FG, width=4)
    for sign in (-1, 1):
        px = cx + sign * 34
        d.line([px, cy - 30, px, cy - 8], fill=FG, width=3)
        d.polygon([(px - 14, cy - 8), (px + 14, cy - 8), (px, cy + 8)],
                  fill=NAVY)
    d.rectangle([cx - 24, cy + 28, cx + 24, cy + 34], fill=FG)


def _robot(d, cx, cy):
    """Robot head: antenna, red eyes, vent mouth."""
    d.line([cx, cy - 40, cx, cy - 26], fill=FG, width=3)
    d.ellipse([cx - 5, cy - 46, cx + 5, cy - 36], fill=CRIMSON)
    d.rectangle([cx - 30, cy - 26, cx + 30, cy + 26], fill=GREY, outline=FG,
                width=3)
    d.rectangle([cx - 22, cy - 14, cx - 4, cy + 2], fill=CRIMSON)
    d.rectangle([cx + 4, cy - 14, cx + 22, cy + 2], fill=CRIMSON)
    d.line([cx - 18, cy + 14, cx + 18, cy + 14], fill=FG, width=3)
    for off in (-12, 0, 12):
        d.line([cx + off, cy + 14, cx + off, cy + 18], fill=FG, width=2)


ICONS = {"burst": _burst, "cuffs": _cuffs, "tanker": _tanker,
         "plunge": _plunge, "draft": _draft, "euro": _euro,
         "scales": _scales, "robot": _robot}

# box, accent, kicker, headline, subline, icon, head size, sub size,
# text width, icon centre
SMALL = [
    ((652, 168, 1000, 306), NAVY, "JUSTICE  ·  SINALOA, MEXICO",
     "MEXICO CAPTURES FBI MOST-WANTED CARTEL BOSS",
     "'El Chapo Isidro' seized in Guasave; 11 killed in the violence "
     "that followed.", "cuffs", 19, 14, 205, (940, 248)),
    ((652, 318, 1000, 452), EMBER, "MIDDLE EAST  ·  STRAIT OF HORMUZ",
     "TWO TANKERS HIT AS HAWKS PRESS TRUMP ON IRAN",
     "Projectiles strike ships in the oil corridor; Israel urges "
     "renewed strikes.", "tanker", 19, 14, 205, (940, 398)),
    ((24, 464, 336, 686), LEAF, "MARKETS  ·  NEW YORK & TOKYO",
     "AI SELL-OFF: S&P -3.7%, NIKKEI -5.1%",
     "S&P 500 enters correction; Nasdaq falls 5.3% in the worst week "
     "in 18 months.", "plunge", 22, 16, 272, (180, 640)),
    ((348, 464, 660, 686), TEAL, "CLIMATE  ·  COP31, ANTALYA",
     "COP31 TALKS RUN PAST DEADLINE ON FOSSIL FUELS",
     "Nations quarrel over fuels as the summit overruns its Friday "
     "deadline.", "draft", 22, 16, 190, (592, 606)),
    ((672, 464, 1000, 686), GOLD, "EUROPE  ·  BRUSSELS",
     "EU PROPOSES TAX ON BIG TECH TO FUND BUDGET",
     "A levy on the world's biggest digital firms would pay for the "
     "next EU budget.", "euro", 22, 16, 272, (836, 650)),
    ((24, 698, 500, 918), PLUM, "JUSTICE  ·  THE HAGUE",
     "MYANMAR REJECTS WORLD COURT GENOCIDE RULING",
     "Rights groups urge sanctions after the ICJ's first-ever verdict "
     "that a state committed genocide.", "scales", 22, 16, 330, (424, 838)),
    ((512, 698, 1000, 918), CRIMSON, "TECH  ·  GENEVA",
     "UN TALKS PLEDGE 'KILLER ROBOT' RULES BY 2028",
     "States agree to draft rules for AI weapons after Russian "
     "pushback.", "robot", 24, 16, 330, (918, 838)),
]


def render():
    s = Sheet()
    d = s.d

    # Masthead: black band, paper title, red date, right-hand motto.
    d.rectangle([0, 0, 1024, 148], fill=FG)
    d.text((36, 14), "THE WORLD IN ONE IMAGE  ·  GLOBAL FRONT PAGE",
           font=_bold(19), fill=(240, 220, 150))
    d.text((34, 40), "SATURDAY", font=_serif(54), fill=(255, 255, 255))
    d.text((34, 98), "21 NOVEMBER 2026", font=_serif(40), fill=(255, 96, 96))
    d.text((700, 52), "ONE DAY.", font=_serif(30), fill=(255, 255, 255))
    d.text((700, 88), "EIGHT STORIES.", font=_serif(30),
           fill=(255, 255, 255))
    d.rectangle([0, 148, 1024, 156], fill=CRIMSON)

    # Lead: the Kryvyi Rih strike, with toll chips under the story.
    s.card(24, 168, 636, 452, CRIMSON)
    y = s.tag(44, 182, "LEAD  ·  KRYVYI RIH, UKRAINE  ·  WAR", CRIMSON)
    y = s.head(44, y, "RUSSIAN MISSILE HITS ZELENSKY'S HOMETOWN", 31, 470)
    y = s.blurb(44, y + 4,
                "A ballistic missile strikes central Kryvyi Rih; "
                "2 killed, 60 wounded, as 148 drones fill the night sky.",
                17, 470)
    _burst(d, 556, 250)
    for i, chip in enumerate(("2 KILLED", "60 WOUNDED", "148 DRONES")):
        s.chip(44 + i * 190, 352, chip)
    d.text((44, 408), "UKRAINE SAYS 117 DRONES SHOT DOWN",
           font=_bold(14), fill=GREY)

    # The seven smaller stories, each drawn from the table above.
    for box, accent, kick, head, sub, icon, hs, ss, w, (ix, iy) in SMALL:
        s.card(*box, accent)
        y = s.tag(box[0] + 18, box[1] + 12, kick, accent)
        y = s.head(box[0] + 18, y, head, hs, w)
        s.blurb(box[0] + 18, y + 2, sub, ss, w)
        ICONS[icon](d, ix, iy)

    # Footer: black band repeating the date and the story list.
    d.rectangle([0, 932, 1024, 1024], fill=FG)
    d.text((36, 946), "SATURDAY 21 NOVEMBER 2026 -- THE DAY IN ONE IMAGE",
           font=_bold(20), fill=(255, 255, 255))
    d.text((36, 976),
           "Kryvyi Rih  ·  Cartel boss held  ·  Tankers hit  ·  "
           "AI sell-off  ·  COP31  ·  Big Tech tax  ·  Myanmar  ·  "
           "Killer robots",
           font=_plain(16), fill=(220, 214, 195))
    return s.img


if __name__ == "__main__":
    target = Path(__file__).with_name("entry.png")
    render().save(target, format="PNG", optimize=True)
    print(target, target.stat().st_size)
