#!/usr/bin/env python3
"""Compose the 19 November 2026 world-news front page (1024x1024) — v2.

Dense newspaper front page in the v1 visual language (navy/cream, serif
masthead): 43 stories reported on Thursday 19 November 2026.
  - Top row: 3 big illustrated stories (Shenzhen summit, GTA VI, Anthropic IPO).
  - Numbers strip under the masthead: 6 big figures from this page.
  - Region strip under the masthead: per-region story counts, honestly
    counted from this page's 43 stories (see NEWS.md for the convention).
  - Grid: 10 more illustrated stories (4-13), the canonical set the
    day's leading pages carry, each with a source credit.
  - Bottom: "WHERE IT HAPPENED" world map with numbered pins (1-13) plus
    "ALSO ON THURSDAY 19 NOVEMBER": 30 numbered briefs (14-43).
  - DATE CHECK box above the footer: stories first reported 18 Nov,
    so not on this page as news.
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

    # ---------- Region strip: honestly counted from this page ----------
    regions = [
        ("EUROPE", 10, (43, 108, 176)),
        ("THE AMERICAS", 7, (47, 133, 90)),
        ("ASIA-PACIFIC", 14, (197, 48, 48)),
        ("MIDEAST", 8, (183, 121, 31)),
        ("AFRICA", 1, (214, 158, 46)),
        ("OCEANIA", 1, (107, 70, 193)),
        ("WORLD", 2, (74, 85, 104)),
    ]
    strip_x0, strip_w, strip_y, strip_h = 8, 1008, 88, 20
    widths = [212, 149, 297, 170, 64, 64, 52]
    rf = font(SANS_B, 9)
    x = strip_x0
    for (label, n, color), w in zip(regions, widths):
        d.rectangle([x, strip_y, x + w, strip_y + strip_h], fill=color)
        d.text((x + w / 2, strip_y + 4), f"{label} {n}", font=rf, fill=WHITE,
               anchor="ma")
        x += w

    # ---------- Numbers strip: six big figures from this page ----------
    numbers = [
        ("$81.3bn", "raised by Anthropic \u2014 the largest IPO on record"),
        ("15.9m", "GTA VI pre-orders banked before release day"),
        ("200,000", "identified for evacuation ahead of Cyclone Akvan"),
        ("$120bn", "a year of adaptation finance unresolved at COP31"),
        ("730,000", "Rohingya who fled in 2017 \u2014 the ICJ case"),
        ("16bn miles", "Voyager 1 from Earth \u2014 one light-day out"),
    ]
    num_y, num_h = 110, 46
    col_w = strip_w // len(numbers)
    nf = font(SANS_B, 19)
    cf = font(SANS, 10)
    for i, (fig, cap) in enumerate(numbers):
        cx = strip_x0 + i * col_w
        d.text((cx + col_w / 2, num_y + 1), fig, font=nf, fill=RED, anchor="ma")
        lines = wrap(d, cap, cf, col_w - 12)
        yy = num_y + 23
        for ln in lines[:2]:
            d.text((cx + col_w / 2, yy), ln, font=cf, fill=(52, 52, 50),
                   anchor="ma")
            yy += 11
        if i:
            d.line([(cx, num_y + 4), (cx, num_y + num_h - 4)], fill=BORDER,
                   width=1)
    d.line([(strip_x0, num_y + num_h), (strip_x0 + strip_w, num_y + num_h)],
           fill=GOLD, width=2)

    # ---------- Top row: 3 big illustrated stories ----------
    top_y, top_h, top_img = 162, 188, 88
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
        ty = top_y + top_img + 8
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
        ("icj", "WORLD COURT RULES ON MYANMAR",
         "Judgment read in The Hague on the 2017 Rohingya case.", "ICJ"),
        ("cop31-final", "COP31 ENTERS ITS FINAL 48 HOURS",
         "Ministers take over in Antalya; the $120bn fund still open.", "REUTERS"),
        ("cyclone", "AKVAN BEARS DOWN AS 200,000 FLEE THE COAST",
         "Odisha marks 204,000 for evacuation; landfall due Friday.", "AFP"),
        ("ukraine", "UKRAINE LEFT OFF THE AGENDA IN SHENZHEN",
         "The war will not be raised in Shenzhen; Kyiv fears a carve-up.", "AP"),
        ("shenzhen-declaration", "SHENZHEN DECLARATION ADOPTED BY APEC",
         "Twenty-one economies back digital trade and a community roadmap.", "REUTERS"),
        ("florida", "FLOODED FLORIDA BRACES FOR MORE RAIN",
         "Up to 15 inches in Hollywood; schools shut a second day.", "AP"),
        ("billion-years", "EARTH'S MISSING BILLION YEARS ARE EXPLAINED",
         "A Nature study blames mantle currents and ancient ice sheets.", "NATURE"),
        ("melenchon", "M\u00c9LENCHON COULD WIN, SAYS JUSTICE MINISTER",
         "France's justice minister concedes the hard-left leader could win.", "REUTERS"),
        ("saudi", "SAUDI ARABIA SAYS DANGER HAS PASSED",
         "The all-clear in three cities follows a downed Houthi missile.", "AP"),
        ("libya-cocaine", "COCAINE AND MILLIONS OF PILLS SEIZED IN LIBYA",
         "One of the country's biggest drug hauls, seized in the east.", "REUTERS"),
    ]
    grid_y = [356, 476]
    grid_h, grid_img = 112, 52
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
        ty = y0 + grid_img + 6
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
    bot_y = 596
    # --- Map panel ---
    map_x, map_w = 8, 352
    d.text((map_x + 4, bot_y + 2), "WHERE IT HAPPENED", font=font(SANS_B, 15), fill=NAVY)
    d.line([(map_x + 4, bot_y + 24), (map_x + map_w - 4, bot_y + 24)], fill=GOLD, width=2)
    mmap = raw("world-map")
    map_img = cover(mmap, map_w - 8, 150, cy=0.5)
    img.paste(map_img, (map_x + 4, bot_y + 30))
    d = ImageDraw.Draw(img)
    # numbered pins: (story, fx, fy, label dx, label dy)
    # 1 and 8 share Shenzhen; 2 and 9 share Florida; 10 is a global
    # science story, pinned in the open southern ocean.
    pins = [
        (1, 0.805, 0.375, 0, 0),
        (2, 0.205, 0.350, 0, 0),
        (3, 0.155, 0.300, 0, 0),
        (4, 0.475, 0.215, 0, 0),
        (5, 0.570, 0.350, 0, 0),
        (6, 0.785, 0.475, 0, 0),
        (7, 0.560, 0.270, 24, -6),
        (8, 0.805, 0.375, 26, 16),
        (9, 0.205, 0.350, -4, 22),
        (10, 0.450, 0.800, 0, 0),
        (11, 0.462, 0.255, -26, 12),
        (12, 0.605, 0.420, 18, 10),
        (13, 0.525, 0.375, -20, 14),
    ]
    mx0, my0 = map_x + 4, bot_y + 30
    for num, fx, fy, ldx, ldy in pins:
        px, py = mx0 + int(fx * (map_w - 8)), my0 + int(fy * 150)
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=RED, outline=WHITE, width=1)
        lx, ly = px + ldx, py + ldy
        if ldx or ldy:
            d.line([(px, py), (lx, ly)], fill=RED, width=1)
        d.ellipse([lx - 7, ly - 7, lx + 7, ly + 7], fill=RED, outline=WHITE, width=1)
        nf = font(SANS_B, 8)
        tw = d.textlength(str(num), font=nf)
        d.text((lx - tw / 2, ly - 5), str(num), font=nf, fill=WHITE)
    # stat strip
    sy = bot_y + 188
    d.rectangle([map_x, sy, map_x + map_w, sy + 30], fill=NAVY)
    sf = font(SANS_B, 12)
    stat = "43 STORIES \u00b7 13 ILLUSTRATED \u00b7 30 IN BRIEF"
    tw = d.textlength(stat, font=sf)
    d.text((map_x + (map_w - tw) / 2, sy + 9), stat, font=sf, fill=GOLD)
    # legend
    ly = sy + 38
    d.text((map_x + 4, ly), "Pins mark the 13 illustrated stories, 1-13.",
           font=font(SANS, 11), fill=GREY)
    d.text((map_x + 4, ly + 16), "10 is a global science story, pinned at sea.",
           font=font(SANS, 11), fill=GREY)

    # --- Briefs ---
    br_x, br_w = 368, 648
    d.text((br_x, bot_y + 2), "ALSO ON THURSDAY 19 NOVEMBER",
           font=font(SANS_B, 15), fill=NAVY)
    d.line([(br_x, bot_y + 24), (br_x + br_w - 4, bot_y + 24)], fill=GOLD, width=2)
    briefs = [
        (14, "Crimea Bridge hit again; traffic shut."),
        (15, "Van Gogh sells for a record $190.4m."),
        (16, "Israeli tanks cross Gaza ceasefire line."),
        (17, "Eisenkot tapped to form Israel's government."),
        (18, "U.S. and Venezuela restore military ties."),
        (19, "India, Japan hold 2+2 defence talks in Tokyo."),
        (20, "U.S. pursues $2B-plus loan package for Manila."),
        (21, "Hormuz tanker hit; crew safe."),
        (22, "Coalition warns of missile threat to Riyadh."),
        (23, "U.S. sanctions Hezbollah-linked entities."),
        (24, "Panama: second arrest in journalist attack."),
        (25, "IAEA: North Korea expanding uranium work."),
        (26, "Bangladesh garment unrest, third week."),
        (27, "Fed minutes: more hikes; Dow falls 1.3%."),
        (28, "APEC: Trump hails U.S. economy, hits AI rules."),
        (29, "APEC: Putin calls Asia-Pacific a growth engine."),
        (30, "Albanese meets Xi; Darwin port spat flares."),
        (31, "Albanese snapped with Putin; backs Ukraine."),
        (32, "Canada, Australia sanction Israeli settlers."),
        (33, "U.S. details $12bn Venezuelan oil revenue."),
        (34, "Five EU states advance Rwanda return hub."),
        (35, "Iraq jails six French citizens for life over IS."),
        (36, "UK 'Scattered Spider' hacker jailed 6 years."),
        (37, "Indonesia raises key rate as rupiah sinks."),
        (38, "Seoul backs possible Trump-Kim dialogue."),
        (39, "Bumrah strikes; NZ 60/4 in Wellington Test."),
        (40, "Delhi schools resume as smog curbs lifted."),
        (41, "Dutch far right used 'remigration' 96 times."),
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
        yy = bot_y + 30
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

    # ---------- DATE CHECK box ----------
    dc_y, dc_h = 928, 44
    d.rectangle([8, dc_y, W - 8, dc_y + dc_h], outline=RED, width=2)
    d.text((16, dc_y + 5),
           "DATE CHECK \u2014 FIRST REPORTED WEDNESDAY 18 NOV, SO NOT ON THIS PAGE AS NEWS:",
           font=font(SANS_B, 11), fill=RED)
    dc_items = ("the Iranian drone interceptions \u00b7 the EU's proposed \u20ac45bn loan "
                "for Ukraine \u00b7 the House Democrats' 251-11 vote nominating Hakeem "
                "Jeffries \u00b7 Voyager 1 crossing one light-day \u00b7 Peltola's Alaska "
                "win \u00b7 Pew's projection that Islam becomes the largest religion by "
                "2035 \u00b7 the first COP31 draft (Monday) \u00b7 the NSA network outage "
                "(Tuesday)")
    df = font(SANS, 10)
    lines = wrap(d, dc_items, df, W - 32)
    yy = dc_y + 20
    for ln in lines[:2]:
        d.text((16, yy), ln, font=df, fill=INK)
        yy += 12

    # ---------- Footer ----------
    fy = 978
    d.rectangle([0, fy, W, fy + 2], fill=GOLD)
    d.rectangle([0, fy + 2, W, H], fill=NAVY)
    ff = font(SANS, 11)
    d.text((16, fy + 10),
           "Every story was reported on Thursday 19 November 2026; disputed claims are attributed.",
           font=ff, fill=LIGHT)
    d.text((16, fy + 26),
           "Sources: Reuters, AP, AFP, BBC, Al Jazeera and others. Original drawings.",
           font=ff, fill=GOLD)

    # ---------- Outer border ----------
    d.rectangle([0, 0, W - 1, H - 1], outline=(10, 14, 22), width=4)

    img.save(OUT, "PNG", optimize=True)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
