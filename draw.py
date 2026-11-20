#!/usr/bin/env python3
"""Draw the 20 November 2026 world-news front page (1024x1024 PNG).

The image is a newspaper front page, drawn entirely with PIL shapes and
text -- no photos, no downloaded assets, no web content.  Every headline
and summary below was verified against real reporting published on
19-20 November 2026 (see the STORIES table).

Run:  python3 draw.py            (writes entry.png next to this file)
"""

import os

from PIL import Image, ImageDraw, ImageFont

# --------------------------------------------------------------------------
# Canvas and palette
# --------------------------------------------------------------------------
W, H = 1024, 1024
PAPER = (248, 244, 233)      # warm newsprint
INK = (20, 20, 20)          # near-black text
NAVY = (12, 35, 64)         # masthead band
RED = (166, 25, 46)         # kickers and rules
GOLD = (185, 138, 31)       # masthead rule and globe
GREY = (90, 90, 90)         # secondary text
RULE = (201, 194, 176)      # hairline dividers
WHITE = (255, 255, 255)

MARGIN = 40                 # side margin
TEXT_W = W - 2 * MARGIN     # 944 px of text width

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    """Load a DejaVu font by file name."""
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


# Type scale (all DejaVu; serif headlines, sans for labels and summaries).
# Kept tight on purpose: six stories must fit one 1024 px page.
F_MASTHEAD = font("DejaVuSerif-Bold.ttf", 80)
F_DATE = font("DejaVuSans-Bold.ttf", 27)
F_HERO_KICKER = font("DejaVuSans-Bold.ttf", 22)
F_HERO_HEAD = font("DejaVuSerif-Bold.ttf", 42)
F_HERO_SUM = font("DejaVuSans.ttf", 24)
F_HERO_FACT = font("DejaVuSans.ttf", 20)
F_KICKER = font("DejaVuSans-Bold.ttf", 19)
F_HEAD = font("DejaVuSerif-Bold.ttf", 29)
F_SUM = font("DejaVuSans.ttf", 22)
F_FOOT = font("DejaVuSans.ttf", 19)

# --------------------------------------------------------------------------
# The news: six verified stories of Friday 20 November 2026.
# Each entry: (kicker, headline, summary).  Sources checked 20 Nov 2026:
# ICJ ruling (CNN/Reuters/Le Monde, 19 Nov), Shenzhen trilateral
# (USA Today/NY Post/The Times, 19 Nov), Cyclone Akvan (IMD via
# Hindu BusinessLine/Jagran Josh, landfall 20 Nov), Hormuz/IEA
# (Bloomberg via Insurance Journal, 19 Nov), COP31 draft (Reuters/
# UN News, 19 Nov; closing day 20 Nov), Crimean Bridge (Reuters,
# third strike 19 Nov).
# --------------------------------------------------------------------------
HERO = (
    "TOP STORY  \u2022  THE HAGUE",
    "UN COURT FINDS MYANMAR GUILTY OF ROHINGYA GENOCIDE",
    "The International Court of Justice rules 9\u20136 that Myanmar committed "
    "genocide against the Rohingya \u2014 the first time a state has been "
    "found guilty.",
    "9\u20136 majority  \u2022  Reparations ordered  \u2022  Case brought by The Gambia in 2019",
)

STORIES = [
    (
        "2  \u2022  SHENZHEN \u2014 DIPLOMACY",
        "TRUMP, XI AND PUTIN MEET IN SHENZHEN",
        "First-ever three-way summit of the US, China and Russia ends with a "
        "pledge on nuclear risks and UN reform \u2014 but no breakthrough on "
        "Ukraine or Iran.",
    ),
    (
        "3  \u2022  ODISHA \u2014 WEATHER",
        "CYCLONE AKVAN SLAMS INTO ODISHA",
        "Storm hits Gopalpur at noon, 100 km/h winds; 80,000+ evacuated.",
    ),
    (
        "4  \u2022  STRAIT OF HORMUZ \u2014 ENERGY",
        "HORMUZ TANKER ATTACKS DEEPEN OIL CRISIS",
        "Iran\u2019s campaign reaches 14 attacks in November; the IEA calls it "
        "the largest disruption to world oil and gas trade on record.",
    ),
    (
        "5  \u2022  ANTALYA \u2014 CLIMATE",
        "COP31 CLOSES WITH FOSSIL FUELS ERASED",
        "Antalya draft erases all fossil-fuel mentions; final text due tonight.",
    ),
    (
        "6  \u2022  KERCH STRAIT \u2014 WAR IN UKRAINE",
        "CRIMEAN BRIDGE HIT FOR A THIRD TIME",
        "Ukraine\u2019s strikes halt Kerch Bridge rail traffic before Putin\u2019s summit.",
    ),
]

FOOTER = "FRIDAY, 20 NOVEMBER 2026  \u2022  SIX STORIES THAT DEFINED THE DAY"


# --------------------------------------------------------------------------
# Drawing helpers
# --------------------------------------------------------------------------
def wrap(draw, text, fnt, max_width):
    """Greedy word wrap; returns a list of lines that fit max_width."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, lines, fnt, x, y, fill, leading):
    """Draw lines top to bottom; return the y below the last line."""
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def centred(draw, text, fnt, y, fill, cx=W // 2):
    """Draw one line centred on cx; return its width."""
    w = draw.textlength(text, font=fnt)
    draw.text((cx - w / 2, y), text, font=fnt, fill=fill)
    return w


def draw_globe(draw, cx, cy, r):
    """Small line-art globe: circle, meridians and parallels (gold)."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=GOLD, width=3)
    # Vertical meridian ellipses.
    for rx in (r // 3, 2 * r // 3):
        draw.ellipse([cx - rx, cy - r, cx + rx, cy + r], outline=GOLD, width=2)
    # Horizontal parallels.
    for dy in (-r // 2, 0, r // 2):
        half = int((r * r - dy * dy) ** 0.5)
        draw.line([cx - half, cy + dy, cx + half, cy + dy], fill=GOLD, width=2)
    # Equator, slightly heavier.
    draw.line([cx - r, cy, cx + r, cy], fill=GOLD, width=3)


def rule(draw, y, fill=RULE, width=2, x0=MARGIN, x1=W - MARGIN):
    """Horizontal rule; return the y below it."""
    draw.line([x0, y, x1, y], fill=fill, width=width)
    return y + width


# --------------------------------------------------------------------------
# Page layout
# --------------------------------------------------------------------------
def draw_page():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # --- Masthead: navy band, gold globe, white serif title. ---
    d.rectangle([0, 0, W, 124], fill=NAVY)
    draw_globe(d, 62, 62, 34)
    centred(d, "WORLD NEWS", F_MASTHEAD, 16, WHITE)
    d.rectangle([0, 124, W, 129], fill=GOLD)

    # --- Date strip. ---
    y = 129
    y = rule(d, y + 8, fill=RED, width=3)
    centred(d, "FRIDAY, 20 NOVEMBER 2026", F_DATE, y + 6, INK)
    y = y + 6 + 36
    y = rule(d, y, fill=RED, width=3)

    # --- Hero story: the ICJ genocide ruling. ---
    y += 14
    d.text((MARGIN, y), HERO[0], font=F_HERO_KICKER, fill=RED)
    y += 28
    y = draw_lines(d, wrap(d, HERO[1], F_HERO_HEAD, TEXT_W),
                   F_HERO_HEAD, MARGIN, y, INK, 48)
    y += 6
    y = draw_lines(d, wrap(d, HERO[2], F_HERO_SUM, TEXT_W),
                   F_HERO_SUM, MARGIN, y, INK, 30)
    y += 8
    # Fact strip: red bar + grey facts.
    d.rectangle([MARGIN, y + 2, MARGIN + 6, y + 24], fill=RED)
    d.text((MARGIN + 16, y), HERO[3], font=F_HERO_FACT, fill=GREY)
    y += 30

    # --- Double rule into the story list. ---
    y = rule(d, y + 6, fill=INK, width=3)
    y = rule(d, y + 3, fill=INK, width=1)

    # --- Stories 2-6. ---
    for kicker, head, summ in STORIES:
        y += 4
        d.text((MARGIN, y), kicker, font=F_KICKER, fill=RED)
        y += 24
        y = draw_lines(d, wrap(d, head, F_HEAD, TEXT_W),
                       F_HEAD, MARGIN, y, INK, 34)
        y += 3
        y = draw_lines(d, wrap(d, summ, F_SUM, TEXT_W),
                       F_SUM, MARGIN, y, (40, 40, 40), 25)
        y += 4
        y = rule(d, y + 2, fill=RULE, width=1)

    print("content ends at y =", y, "(footer rule at", H - 44, ")")

    # --- Footer. ---
    y = H - 44
    y = rule(d, y, fill=INK, width=2)
    centred(d, FOOTER, F_FOOT, y + 8, GREY)
    return img


def main():
    img = draw_page()
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, format="PNG", optimize=True)
    print("wrote", out, img.size, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
