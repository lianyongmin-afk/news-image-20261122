#!/usr/bin/env python3
"""Render the 22 November 2026 world-news infographic (1024x1024 PNG).

Draws everything from Pillow primitives: masthead, one lead story,
a 2x2 grid of stories, one closing strip and a source footer.
Deterministic: no randomness, no timestamps, fixed fonts and geometry,
so re-running writes byte-identical PNG bytes.
"""

import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
M = 28
CW = W - 2 * M  # 968 content width

PAPER = (246, 241, 231)
INK = (20, 33, 61)
NAVY = (18, 38, 63)
MUTED = (90, 96, 110)
CARD = (255, 255, 255)
LINE = (205, 198, 184)
WHITE = (255, 255, 255)
RED = (169, 50, 38)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_TITLE = font("DejaVuSans-Bold.ttf", 46)
F_KICK = font("DejaVuSans-Bold.ttf", 19)
F_HERO_HEAD = font("DejaVuSans-Bold.ttf", 33)
F_HERO_BODY = font("DejaVuSans.ttf", 20)
F_HEAD = font("DejaVuSans-Bold.ttf", 25)
F_BODY = font("DejaVuSans.ttf", 18)
F_TAG = font("DejaVuSans-Bold.ttf", 16)
F_NUM = font("DejaVuSans-Bold.ttf", 22)
F_FOOT = font("DejaVuSans.ttf", 14)
F_STRIP_HEAD = font("DejaVuSans-Bold.ttf", 26)
F_STRIP_BODY = font("DejaVuSans.ttf", 19)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, xy, lines, fnt, fill, leading):
    x, y = xy
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def chip(draw, box, accent, kind):
    """Draw a small pictogram for a story inside box (x0,y0,x1,y1)."""
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    draw.rounded_rectangle(box, radius=14, outline=accent, width=3)
    if kind == "globe":
        r = 34
        draw.ellipse((cx - r, cy - r, cx + r, cy + r), outline=accent, width=4)
        draw.ellipse((cx - 14, cy - r, cx + 14, cy + r), outline=accent, width=3)
        draw.line((cx - r, cy, cx + r, cy), fill=accent, width=3)
        draw.arc((cx - r, cy - 18, cx + r, cy + 18), 200, 340, fill=accent, width=3)
        draw.line((cx - 26, cy + 26, cx + 26, cy - 26), fill=RED, width=5)
    elif kind == "building":
        draw.rectangle((cx - 34, cy - 6, cx - 6, cy + 34), outline=accent, width=3)
        draw.rectangle((cx + 2, cy - 22, cx + 34, cy + 34), outline=accent, width=3)
        draw.line((cx + 2, cy - 22, cx + 18, cy - 34, cx + 34, cy - 22),
                  fill=accent, width=3)
        for bx, by in ((cx - 26, cy + 4), (cx - 14, cy + 4), (cx + 12, cy - 8),
                       (cx + 24, cy - 8), (cx + 12, cy + 8), (cx + 24, cy + 8)):
            draw.rectangle((bx, by, bx + 7, by + 7), fill=accent)
        for sx, sy, sr in ((cx - 20, cy - 26, 6), (cx - 6, cy - 36, 8),
                           (cx + 12, cy - 30, 5)):
            draw.ellipse((sx - sr, sy - sr, sx + sr, sy + sr),
                         outline=MUTED, width=2)
    elif kind == "badge":
        pts = [(cx, cy - 36), (cx + 30, cy - 24), (cx + 30, cy + 6),
               (cx, cy + 36), (cx - 30, cy + 6), (cx - 30, cy - 24)]
        draw.polygon(pts, outline=accent, width=4)
        draw.regular_polygon((cx, cy - 2, 16), 5, outline=accent, width=3)
    elif kind == "drop":
        draw.polygon([(cx, cy - 38), (cx - 20, cy - 8), (cx + 20, cy - 8)],
                     fill=accent)
        draw.ellipse((cx - 20, cy - 14, cx + 20, cy + 26), fill=accent)
        for wy in (cy + 38,):
            draw.arc((cx - 30, wy - 8, cx - 2, wy + 8), 0, 180, fill=accent, width=3)
            draw.arc((cx + 2, wy - 8, cx + 30, wy + 8), 0, 180, fill=accent, width=3)
    elif kind == "planet":
        r = 30
        draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(168, 160, 148))
        for dx, dy, cr in ((-12, -8, 7), (10, 4, 9), (-4, 14, 5), (14, -14, 4)):
            draw.ellipse((cx + dx - cr, cy + dy - cr, cx + dx + cr, cy + dy + cr),
                         fill=(128, 120, 108))
        draw.ellipse((cx - 44, cy - 44, cx + 44, cy + 44), outline=accent, width=2)
        draw.rectangle((cx + 34, cy - 40, cx + 46, cy - 28), fill=accent)
    elif kind == "factory":
        draw.rectangle((cx - 36, cy + 2, cx + 36, cy + 34), outline=accent, width=3)
        draw.rectangle((cx + 20, cy - 30, cx + 30, cy + 2), outline=accent, width=3)
        draw.polygon([(cx - 14, cy - 2), (cx - 4, cy - 26), (cx + 4, cy - 2)],
                     fill=(200, 90, 23))
        draw.polygon([(cx + 8, cy - 2), (cx + 16, cy - 20), (cx + 24, cy - 2)],
                     fill=(226, 122, 31))


def card(draw, box, num, tag, accent, headline, body, pic, head_fnt, body_fnt,
         head_lead, body_lead):
    x0, y0, x1, y1 = box
    draw.rounded_rectangle(box, radius=12, fill=CARD, outline=LINE, width=1)
    draw.rounded_rectangle((x0, y0, x0 + 8, y1), radius=4, fill=accent)
    tx = x0 + 24
    ty = y0 + 16
    draw.ellipse((tx, ty, tx + 34, ty + 34), fill=accent)
    tw = draw.textlength(str(num), font=F_NUM)
    draw.text((tx + (34 - tw) / 2, ty + 4), str(num), font=F_NUM, fill=WHITE)
    draw.text((tx + 46, ty + 7), tag, font=F_TAG, fill=accent)
    pic_w = 118
    text_w = (x1 - 24) - pic_w - tx
    lines = wrap(draw, headline, head_fnt, text_w)
    y = text_block(draw, (tx, ty + 46), lines, head_fnt, INK, head_lead)
    blines = wrap(draw, body, body_fnt, text_w)
    text_block(draw, (tx, y + 6), blines, body_fnt, MUTED, body_lead)
    chip(draw, (x1 - 24 - 104, y0 + 52, x1 - 24, y0 + 52 + 104), accent, pic)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Masthead
    d.rounded_rectangle((M, M, W - M, 132), radius=12, fill=NAVY)
    d.text((M + 24, M + 14), "THE WORLD IN ONE IMAGE", font=F_KICK,
           fill=(150, 200, 220))
    d.text((M + 24, M + 42), "SUNDAY 22 NOVEMBER 2026", font=F_TITLE, fill=WHITE)
    gx, gy = W - M - 96, M + 26
    d.ellipse((gx, gy, gx + 56, gy + 56), outline=(150, 200, 220), width=3)
    d.ellipse((gx + 12, gy, gx + 44, gy + 56), outline=(150, 200, 220), width=2)
    d.line((gx, gy + 28, gx + 56, gy + 28), fill=(150, 200, 220), width=2)

    teal = (14, 124, 107)
    blue = (46, 90, 136)
    ochre = (183, 121, 31)
    crimson = (169, 50, 38)
    plum = (108, 74, 138)
    orange = (200, 90, 23)

    # Lead story: COP31 collapse
    card(d, (M, 148, W - M, 322), 1, "CLIMATE  ·  ANTALYA, TURKEY", teal,
         "COP31 climate talks collapse with no deal",
         "EU rejects a draft with no mention of fossil fuels; the summit ends "
         "two days past its deadline.",
         "globe", F_HERO_HEAD, F_HERO_BODY, 40, 26)

    # Grid row 1
    card(d, (M, 338, 504, 556), 2, "UKRAINE  ·  KYIV REGION", blue,
         "Russian drone hits Kyiv flats; 14 missing",
         "A five-storey block in Dymer is struck overnight; 2 killed, 4 hurt.",
         "building", F_HEAD, F_BODY, 30, 23)
    card(d, (520, 338, W - M, 556), 3, "MEXICO  ·  SINALOA", ochre,
         "Cartel boss \u201cEl Chapo Isidro\u201d captured",
         "Special forces seize Fausto Isidro Meza Flores; 11 killed in the raid.",
         "badge", F_HEAD, F_BODY, 30, 23)

    # Grid row 2
    card(d, (M, 572, 504, 790), 4, "GULF  ·  BAHRAIN", crimson,
         "Iran hits Bahrain site as Gulf tensions rise",
         "Projectiles hit an industrial site; two people injured, Bahrain says.",
         "drop", F_HEAD, F_BODY, 30, 23)
    card(d, (520, 572, W - M, 790), 5, "SPACE  ·  MERCURY", plum,
         "BepiColombo reaches Mercury after 8 years",
         "ESA confirms orbit entry; a thruster glitch is under study, craft safe.",
         "planet", F_HEAD, F_BODY, 30, 23)

    # Closing strip: Indonesia factory fire
    card(d, (M, 806, W - M, 936), 6, "DISASTER  ·  CIKANDE, INDONESIA", orange,
         "Candy factory fire kills 3; dozens missing",
         "Blaze sweeps a plant in Banten; rescuers search the ruins for 36 workers.",
         "factory", F_STRIP_HEAD, F_STRIP_BODY, 32, 24)

    # Footer
    d.text((M, 952),
           "Sources: AP  ·  Reuters  ·  AFP  ·  ESA  ·  SCMP  —  all six stories first reported 22 Nov 2026",
           font=F_FOOT, fill=MUTED)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, format="PNG")
    print(f"wrote {out} ({os.path.getsize(out)} bytes)")


if __name__ == "__main__":
    main()
