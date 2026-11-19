#!/usr/bin/env python3
"""Compose the 19 November 2026 world-news front page (1024x1024) — v1.

Dense newspaper front page in the v1 visual language (navy/cream, serif
masthead): 43 stories reported on Thursday 19 November 2026.
  - Top row: 3 big illustrated stories (Shenzhen summit, GTA VI, Anthropic IPO).
  - Grid: 10 more illustrated stories (4-13), each with a source credit.
  - Bottom: "WHERE IT HAPPENED" world map with numbered pins (1-13) plus
    "ALSO ON THURSDAY 19 NOVEMBER": 30 numbered briefs (14-43).
  - Footer: date-check note + full source list.
All typography is drawn with PIL so every word stays sharp and legible.
Illustration panels are original art generated for this entry (assets/raw/).
"""
import glob
from PIL import Image, ImageDraw, ImageFont

ROOT = "/home/hatch/workspace/makefun-entries/makefun-news-image-20261119"
RAW = f"{ROOT}/assets/raw"
OUT = f"{ROOT}/assets/entry.png"

W, H = 1024, 1024
NAVY = (14, 27, 46)
NAVY2 = (24, 42, 68)
GOLD = (232, 184, 75)
RED = (179, 39, 30)
PAPER = (247, 242, 231)
INK = (18, 18, 18)
GREY = (92, 92, 88)
WHITE = (255, 255, 255)
LIGHT = (235, 235, 228)
BORDER = (200, 196, 186)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def cover(img, w, h, cy=0.5):
    """Crop img to cover w x h, centred horizontally, cy vertical anchor."""
    sw, sh = img.size
    scale = max(w / sw, h / sh)
    nw, nh = int(sw * scale + 0.5), int(sh * scale + 0.5)
    img = img.resize((nw, nh), Image.LANCZOS)
    x = (nw - w) // 2
    y = int((nh - h) * cy)
    return img.crop((x, y, x + w, y + h))


def wrap(draw, text, fnt, max_w):
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


def raw(name):
    return Image.open(glob.glob(f"{RAW}/media-generation-{name}-*.png")[0]).convert("RGB")


def credit(d, x, y, w, text):
    """Small source-credit chip at the bottom-left of an illustration."""
    fnt = font(SANS_B, 10)
    tw = int(d.textlength(text, font=fnt))
    chip_w, chip_h = tw + 12, 16
    d.rectangle([x + 4, y - chip_h - 4, x + 4 + chip_w, y - 4], fill=(10, 16, 28))
    d.text((x + 10, y - chip_h - 1), text, font=fnt, fill=WHITE)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---------- Masthead ----------
    d.rectangle([0, 0, W, 84], fill=NAVY)
    d.rectangle([0, 84, W, 88], fill=GOLD)
    d.text((16, 8), "THE WORLD TODAY", font=font(SERIF_B, 46), fill=WHITE)
    d.text((16, 58), "THURSDAY, 19 NOVEMBER 2026", font=font(SANS_B, 17), fill=GOLD)
    d.text((W - 16, 12), "THE DAY IN WORLD NEWS", font=font(SANS_B, 17),
           fill=WHITE, anchor="ra")
    d.text((W - 16, 40), "43 STORIES \u00b7 6 CONTINENTS \u00b7 ONE DAY",
           font=font(SANS_B, 15), fill=GOLD, anchor="ra")

    # ---------- Top row: 3 big illustrated stories ----------
    top_y, top_h, top_img = 96, 200, 92
    top_w = 330
    top_x = [8, 347, 686]
    top = [
        ("summit", "SUMMIT", "Three leaders, one table in Shenzhen",
         "Trump, Xi and Putin meet for the first time; nuclear arms top the agenda.",
         "AFP", 0.45),
        ("gta-vi", "GTA VI", "GTA VI launches after a 13-year wait",
         "Midnight launch on PS5 and Xbox; 99/100 on Metacritic, 2.3m watch on Twitch.",
         "LE MONDE", 0.5),
        ("anthropic-ipo", "RECORD IPO", "Anthropic's $81.3B debut, the biggest ever",
         "$83 a share on Nasdaq; a $1.5T value as AI's first big lab goes public.",
         "REUTERS", 0.45),
    ]
    for i, (name, kicker, head, deck, src, cy) in enumerate(top):
        x0 = top_x[i]
        d.rectangle([x0, top_y, x0 + top_w, top_y + top_h], fill=WHITE,
                    outline=BORDER, width=2)
        pic = cover(raw(name), top_w - 4, top_img, cy=cy)
        img.paste(pic, (x0 + 2, top_y + 2))
        credit(d, x0 + 2, top_y + 2 + top_img, top_w - 4, src)
        ty = top_y + top_img + 10
        d.text((x0 + 14, ty), kicker, font=font(SANS_B, 13), fill=RED)
        hf = font(SANS_B, 18)
        lines = wrap(d, head, hf, top_w - 28)
        yy = ty + 18
        for ln in lines[:2]:
            d.text((x0 + 14, yy), ln, font=hf, fill=INK)
            yy += 21
        bf = font(SANS, 13)
        lines = wrap(d, deck, bf, top_w - 28)
        for ln in lines[:2]:
            d.text((x0 + 14, yy), ln, font=bf, fill=(52, 52, 50))
            yy += 16

    # ---------- Grid: 10 illustrated stories (4-13) ----------
    grid = [
        ("crimea-bridge", "BRIDGE HIT AGAIN", "Crimea link shut after a third strike this week.",
         "BBC"),
        ("icj", "WORLD COURT RULES TODAY", "Myanmar genocide verdict due in The Hague.",
         "ICJ"),
        ("vangogh", "VAN GOGH: A RECORD $190.4M", "Blossoming Chestnut Trees tops the artist's record.",
         "BBC"),
        ("cyclone", "CYCLONE AKVAN NEARS INDIA", "Storm set to cross between Machilipatnam and Puri.",
         "AFP"),
        ("gaza", "ISRAELI TANKS CROSS INTO GAZA", "Rare ground move beyond the ceasefire line.",
         "BBC"),
        ("eisenkot", "EISENKOT TO FORM GOVERNMENT", "Herzog picks ex-army chief over Netanyahu.",
         "AP"),
        ("venezuela", "U.S., VENEZUELA RESTORE TIES", "Military cooperation resumes, Hegseth says.",
         "AP"),
        ("tokyo-talks", "INDIA, JAPAN IN 2+2 TALKS", "Defence dialogue opens in Tokyo.",
         "ANI"),
        ("manila", "U.S. PURSUES $2B FOR MANILA", "Loan package for the Philippines in the works.",
         "AP"),
        ("cop31", "25 NATIONS BACK WILDLIFE PACT", "COP31 first: animals join the climate deal.",
         "REUTERS"),
    ]
    grid_y = [304, 436]
    grid_h, grid_img = 124, 56
    grid_w = 195
    grid_x = [8, 211, 414, 617, 820]
    for idx, (name, head, body, src) in enumerate(grid):
        row, col = divmod(idx, 5)
        x0, y0 = grid_x[col], grid_y[row]
        d.rectangle([x0, y0, x0 + grid_w, y0 + grid_h], fill=WHITE,
                    outline=BORDER, width=2)
        pic = cover(raw(name), grid_w - 4, grid_img, cy=0.45)
        img.paste(pic, (x0 + 2, y0 + 2))
        credit(d, x0 + 2, y0 + 2 + grid_img, grid_w - 4, src)
        ty = y0 + grid_img + 8
        hf = font(SANS_B, 12)
        lines = wrap(d, head, hf, grid_w - 16)
        yy = ty
        for ln in lines[:2]:
            d.text((x0 + 8, yy), ln, font=hf, fill=INK)
            yy += 14
        bf = font(SANS, 10)
        lines = wrap(d, body, bf, grid_w - 16)
        for ln in lines[:2]:
            d.text((x0 + 8, yy), ln, font=bf, fill=(52, 52, 50))
            yy += 12

    # ---------- Bottom: map + numbered briefs ----------
    bot_y = 568
    # --- Map panel ---
    map_x, map_w = 8, 352
    d.text((map_x + 4, bot_y + 2), "WHERE IT HAPPENED", font=font(SANS_B, 15), fill=NAVY)
    d.line([(map_x + 4, bot_y + 24), (map_x + map_w - 4, bot_y + 24)], fill=GOLD, width=2)
    mmap = raw("world-map")
    map_img = cover(mmap, map_w - 8, 176, cy=0.5)
    img.paste(map_img, (map_x + 4, bot_y + 30))
    d = ImageDraw.Draw(img)
    # numbered pins: (story, fx, fy, label dx, label dy)
    pins = [
        (1, 0.805, 0.375, 0, 0),
        (2, 0.205, 0.355, 0, 0),
        (3, 0.155, 0.300, 0, 0),
        (4, 0.575, 0.325, 0, -20),
        (5, 0.475, 0.220, 0, 0),
        (6, 0.235, 0.270, 0, 0),
        (7, 0.785, 0.475, 0, 0),
        (8, 0.595, 0.405, 0, 0),
        (9, 0.588, 0.388, 24, -10),
        (10, 0.245, 0.470, 0, 0),
        (11, 0.855, 0.295, 0, 0),
        (12, 0.815, 0.455, 20, 6),
        (13, 0.565, 0.355, -24, 12),
    ]
    mx0, my0 = map_x + 4, bot_y + 30
    for num, fx, fy, ldx, ldy in pins:
        px, py = mx0 + int(fx * (map_w - 8)), my0 + int(fy * 176)
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=RED, outline=WHITE, width=1)
        lx, ly = px + ldx, py + ldy
        if ldx or ldy:
            d.line([(px, py), (lx, ly)], fill=RED, width=1)
        d.ellipse([lx - 7, ly - 7, lx + 7, ly + 7], fill=RED, outline=WHITE, width=1)
        nf = font(SANS_B, 8)
        tw = d.textlength(str(num), font=nf)
        d.text((lx - tw / 2, ly - 5), str(num), font=nf, fill=WHITE)
    # stat strip
    sy = bot_y + 214
    d.rectangle([map_x, sy, map_x + map_w, sy + 34], fill=NAVY)
    sf = font(SANS_B, 12)
    stat = "43 STORIES \u00b7 13 ILLUSTRATED \u00b7 30 IN BRIEF"
    tw = d.textlength(stat, font=sf)
    d.text((map_x + (map_w - tw) / 2, sy + 10), stat, font=sf, fill=GOLD)
    # legend + numbers box
    ly = sy + 42
    d.text((map_x + 4, ly), "Pins mark the 13 illustrated stories, 1-13.",
           font=font(SANS, 11), fill=GREY)
    ny = ly + 22
    d.rectangle([map_x, ny, map_x + map_w, ny + 104], outline=BORDER, width=2)
    d.text((map_x + 12, ny + 8), "THE DAY IN NUMBERS", font=font(SANS_B, 12), fill=RED)
    nf2 = font(SANS, 11)
    nums = [
        "$81.3B \u2014 Anthropic's record IPO",
        "99/100 \u2014 GTA VI's Metacritic score",
        "$190.4m \u2014 record Van Gogh sale",
    ]
    yy = ny + 30
    for ln in nums:
        d.text((map_x + 12, yy), ln, font=nf2, fill=(52, 52, 50))
        yy += 18
    d.text((map_x + 12, yy + 4), "2.3m \u2014 Twitch viewers watch GTA VI launch",
           font=nf2, fill=(52, 52, 50))

    # --- Briefs ---
    br_x, br_w = 368, 648
    d.text((br_x, bot_y + 2), "ALSO ON THURSDAY 19 NOVEMBER",
           font=font(SANS_B, 15), fill=NAVY)
    d.line([(br_x, bot_y + 24), (br_x + br_w - 4, bot_y + 24)], fill=GOLD, width=2)
    briefs = [
        (14, "Hormuz tanker hit; crew safe."),
        (15, "Coalition warns of missile threat to Riyadh."),
        (16, "Riyadh: Civil Defence says danger passed."),
        (17, "U.S. sanctions Hezbollah-linked entities."),
        (18, "Panama: second arrest in journalist attack."),
        (19, "Paraguay: Ueno Bank guarantee extended."),
        (20, "IAEA: North Korea expanding uranium work."),
        (21, "Bangladesh garment unrest, third week."),
        (22, "Fed minutes: more hikes; Dow falls 1.3%."),
        (23, "APEC: Xi pledges $20m for cooperation."),
        (24, "APEC: Trump hails U.S. economy, hits AI rules."),
        (25, "APEC: Putin calls Asia-Pacific a growth engine."),
        (26, "Albanese meets Xi; Darwin port spat flares."),
        (27, "Albanese snapped with Putin; backs Ukraine."),
        (28, "Trump praises 'friend' Albanese at Quad."),
        (29, "Canada, Australia sanction Israeli settlers."),
        (30, "Four nations: let aid reach flooded Gaza."),
        (31, "U.S. details $12bn Venezuelan oil revenue."),
        (32, "Five EU states advance Rwanda return hub."),
        (33, "Iraq jails six French citizens for life over IS."),
        (34, "UK 'Scattered Spider' hacker jailed 6 years."),
        (35, "Indonesia raises key rate as rupiah sinks."),
        (36, "Seoul backs possible Trump-Kim dialogue."),
        (37, "Bumrah strikes; NZ 60/4 in Wellington Test."),
        (38, "Sindhu back in badminton's world top five."),
        (39, "Delhi schools resume as smog curbs lifted."),
        (40, "Dutch far right used 'remigration' 96 times."),
        (41, "Data breach hits 40 Irish credit unions."),
        (42, "France braces for fourth protest weekend."),
        (43, "Jessica L. Nelson wins Prix Interallie."),
    ]
    col_w = 316
    col_x = [br_x, br_x + 332]
    bf = font(SANS, 11)
    nbf = font(SANS_B, 11)
    for i, (num, text) in enumerate(briefs):
        col, row = (0, i) if i < 15 else (1, i - 15)
        x0 = col_x[col]
        # y position: stack by measured lines of previous briefs in this column
        yy = bot_y + 34
        for j in range(row):
            pnum, ptext = briefs[j + (0 if col == 0 else 15)]
            plines = wrap(d, ptext, bf, col_w - 26)
            yy += len(plines) * 14 + 5
        d.text((x0, yy), f"{num}.", font=nbf, fill=RED)
        lines = wrap(d, text, bf, col_w - 26)
        ly2 = yy
        for ln in lines:
            d.text((x0 + 26, ly2), ln, font=bf, fill=INK)
            ly2 += 14

    # ---------- Footer ----------
    fy = 980
    d.rectangle([0, fy - 6, W, fy - 2], fill=GOLD)
    d.rectangle([0, fy - 2, W, H], fill=NAVY)
    ff = font(SANS, 11)
    d.text((16, fy + 8),
           "Every story was reported on Thursday 19 November 2026; disputed claims are attributed.",
           font=ff, fill=LIGHT)
    d.text((16, fy + 24),
           "Sources: Reuters, AP, AFP, BBC, Al Jazeera and others. Original drawings.",
           font=ff, fill=GOLD)

    # ---------- Outer border ----------
    d.rectangle([0, 0, W - 1, H - 1], outline=(10, 14, 22), width=4)

    img.save(OUT, "PNG", optimize=True)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
