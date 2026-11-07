# Etsy listing images (3000x2250, 4:3) built from the real rendered workbook pages.
import sys, math, random
from PIL import Image, ImageDraw, ImageFilter, ImageFont

S = sys.argv[1]
P = S + "/etsy/pages/a-%02d.png"        # A4 render, 33 pages (1-based index of final book)
OUT = S + "/etsy/out/"
W, H = 3000, 2250
BG = (253, 236, 240); PINK = (240, 143, 161); PINK_D = (226, 96, 124)
NAVY = (31, 52, 98); INK = (40, 40, 48); WHITE = (255, 255, 255); YEL = (255, 214, 90)
AGB = S + "/fonts/Agbalumo.ttf"; FRE = S + "/fonts/Fredoka-Bold.ttf"; FRS = S + "/fonts/Fredoka-SemiBold.ttf"
ICON = S + "/icons/"

def F(path, size): return ImageFont.truetype(path, size)
def page(n): return Image.open(P % n).convert("RGB")
def icon(name): return Image.open(ICON + name).convert("RGBA")

def canvas(bg=BG):
    im = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(im)
    rnd = random.Random(7)                       # soft confetti dots, deterministic
    for _ in range(70):
        x, y, r = rnd.randint(0, W), rnd.randint(0, H), rnd.randint(6, 16)
        c = rnd.choice([(250, 205, 214), (255, 228, 160), (200, 226, 250), (210, 240, 210)])
        d.ellipse((x - r, y - r, x + r, y + r), fill=c)
    return im

def tracked(d, xy, text, font, fill, track=0.0, anchor_center=False):
    size = font.size; widths = [font.getlength(ch) + track * size for ch in text]
    total = sum(widths) - track * size
    x, y = xy
    if anchor_center: x -= total / 2
    for ch, w in zip(text, widths):
        d.text((x, y), ch, font=font, fill=fill); x += w
    return total

def title(d, text, y, size=150, fill=INK, cx=W / 2):
    tracked(d, (cx, y), text, F(AGB, size), fill, -0.04, True)

def ctext(d, text, y, font, fill=INK, cx=W / 2):
    w = d.textlength(text, font=font); d.text((cx - w / 2, y), text, font=font, fill=fill)

def pill(d, cx, y, text, font, fill=PINK, color=WHITE, padx=44, h=None):
    w = d.textlength(text, font=font); h = h or int(font.size * 1.75)
    d.rounded_rectangle((cx - w / 2 - padx, y, cx + w / 2 + padx, y + h), radius=h // 2, fill=fill)
    d.text((cx - w / 2, y + (h - font.size) / 2 - font.size * 0.12), text, font=font, fill=color)
    return w + 2 * padx

def paste_page(im, pg, cx, cy, height, angle=0.0, shadow=True, border=0):
    pg = pg.resize((round(pg.width * height / pg.height), height), Image.LANCZOS)
    if border:
        b = Image.new("RGB", (pg.width + 2 * border, pg.height + 2 * border), WHITE); b.paste(pg, (border, border)); pg = b
    pg = pg.convert("RGBA")
    if angle: pg = pg.rotate(angle, resample=Image.BICUBIC, expand=True)
    x, y = int(cx - pg.width / 2), int(cy - pg.height / 2)
    if shadow:
        a = pg.split()[3]
        sh = Image.new("RGBA", (pg.width + 120, pg.height + 120), (0, 0, 0, 0))
        blk = Image.new("RGBA", pg.size, (60, 30, 40, 95)); sh.paste(blk, (60, 60), a)
        sh = sh.filter(ImageFilter.GaussianBlur(26))
        im.paste(sh, (x - 60 + 18, y - 60 + 30), sh)
    im.paste(pg, (x, y), pg)
    return (x, y, x + pg.width, y + pg.height)

def star(d, cx, cy, R, fill=YEL, outline=None, width=0):
    pts = [(cx + (R if i % 2 == 0 else R * 0.48) * math.cos(math.radians(-90 + i * 36)),
            cy + (R if i % 2 == 0 else R * 0.48) * math.sin(math.radians(-90 + i * 36))) for i in range(10)]
    d.polygon(pts, fill=fill, outline=outline, width=width)

def put_icon(im, name, cx, cy, h):
    ic = icon(name); ic = ic.resize((round(ic.width * h / ic.height), h), Image.LANCZOS)
    bbox = ic.getbbox(); ic = ic.crop(bbox)
    im.paste(ic, (int(cx - ic.width / 2), int(cy - ic.height / 2)), ic)

def save(im, name): im.save(OUT + name, quality=95, subsampling=0, dpi=(300, 300)); print(name)

# ---------------------------------------------------------------- 1. HERO
im = canvas(); d = ImageDraw.Draw(im)
paste_page(im, page(32), 1700, 1200, 1650, angle=-12)
paste_page(im, page(15), 2560, 1170, 1650, angle=10)
paste_page(im, page(1), 2190, 1120, 1920, angle=0, border=0)
title(d, "Preschool", 250, 210, NAVY, cx=760)
title(d, "Activity", 470, 210, PINK_D, cx=760)
title(d, "Workbook", 690, 210, NAVY, cx=760)
f = F(FRS, 70)
ctext(d, "Fun printable activities", 990, f, INK, cx=760)
ctext(d, "for little learners", 1080, f, INK, cx=760)
fb = F(FRE, 64)
for i, t in enumerate(["33 PAGES", "AGES 3 - 5", "INSTANT DOWNLOAD", "A4 + US LETTER"]):
    pill(d, 760, 1270 + i * 165, t, fb, fill=[PINK_D, NAVY, PINK_D, NAVY][i])
save(im, "01-hero.jpg")

# ---------------------------------------------------------------- 2. WHAT'S INSIDE (all pages)
im = canvas(); d = ImageDraw.Draw(im)
title(d, "What's Inside", 70, 170, NAVY)
ctext(d, "33 printable pages  -  tracing, matching, coloring & puzzles", 300, F(FRS, 68), INK)
cols, rows = 9, 4; pw = 285; ph = round(pw * 1.4142); gx = 24; gy = 36
x0 = (W - (cols * pw + (cols - 1) * gx)) / 2; y0 = 440
for i in range(33):
    r = i // cols; inrow = min(cols, 33 - r * cols)
    rx0 = (W - (inrow * pw + (inrow - 1) * gx)) / 2
    cx = rx0 + (i % cols) * (pw + gx) + pw / 2; cy = y0 + (i // cols) * (ph + gy) + ph / 2
    paste_page(im, page(i + 1), cx, cy, ph)
save(im, "02-whats-inside.jpg")

# ---------------------------------------------------------------- 3. SKILLS
im = canvas(); d = ImageDraw.Draw(im)
title(d, "Skills Your Child Will Build", 70, 150, NAVY)
cats = [("Tracing", 9, PINK_D), ("Matching", 5, NAVY), ("Coloring", 4, PINK_D), ("Puzzles & Mazes", 32, NAVY)]
for i, (lab, n, col) in enumerate(cats):
    cx = 420 + i * 720
    paste_page(im, page(n), cx, 1060, 1000)
    pill(d, cx, 1620, lab, F(FRE, 66), fill=col)
fs = F(FRS, 58)
chips = ["Fine motor skills", "Pencil control", "Shapes & colors", "Focus & attention", "Visual matching"]
ws = [d.textlength(c, font=fs) + 80 for c in chips]; gap = 30
x = (W - sum(ws) - gap * (len(chips) - 1)) / 2
for c, w in zip(chips, ws):
    pill(d, x + w / 2, 1880, c, fs, fill=WHITE, color=INK, padx=40); x += w + gap
save(im, "03-skills.jpg")

# ---------------------------------------------------------------- 4. CLOSE-UP
im = canvas(); d = ImageDraw.Draw(im)
title(d, "Big, Clear Pages for Little Hands", 70, 140, NAVY)
for cx, n in [(830, 6), (2170, 15)]:
    paste_page(im, page(n), cx, 1270, 1800)
save(im, "04-close-up.jpg")

# ---------------------------------------------------------------- 5. BONUS PAGES
im = canvas(); d = ImageDraw.Draw(im)
title(d, "Bonus Pages Included!", 70, 160, PINK_D)
for i, (n, lab) in enumerate([(2, "Name Page"), (3, "Star Reward Chart"), (33, "Certificate")]):
    cx = 540 + i * 960
    paste_page(im, page(n), cx, 1110, 1300)
    pill(d, cx, 1940, lab, F(FRE, 66), fill=[NAVY, PINK_D, NAVY][i])
save(im, "05-bonus-pages.jpg")

# ---------------------------------------------------------------- 6. SIZES & FORMAT
im = canvas(); d = ImageDraw.Draw(im)
title(d, "Two Paper Sizes Included", 70, 150, NAVY)
a4 = page(4); lt = Image.open(S + "/etsy/pages/l-02.png").convert("RGB")
paste_page(im, a4, 600, 1100, 1300)
paste_page(im, lt, 1650, 1139, round(1300 * 792 / 842.25))
fb = F(FRE, 62); fs = F(FRS, 52)
pill(d, 600, 1830, "A4", fb, fill=PINK_D); ctext(d, "21 x 29.7 cm", 1960, fs, INK, cx=600)
pill(d, 1650, 1830, "US LETTER", fb, fill=NAVY); ctext(d, "8.5 x 11 in", 1960, fs, INK, cx=1650)
lines = ["High-quality PDF files", "Crisp lines for tracing", "Print at home or at a", "print shop", "Print as many times as", "you like (personal use)"]
y = 640
for j in range(0, len(lines), 2):
    star(d, 2250, y + 40, 34, fill=YEL, outline=INK, width=3)
    d.text((2315, y), lines[j], font=F(FRS, 60), fill=INK)
    d.text((2315, y + 76), lines[j + 1], font=F(FRS, 60), fill=INK)
    y += 330
save(im, "06-sizes.jpg")

# ---------------------------------------------------------------- 7. HOW IT WORKS
im = canvas(); d = ImageDraw.Draw(im)
title(d, "How It Works", 70, 170, NAVY)
steps = [("1", "Purchase", "p27_x543.png"), ("2", "Download", "p30_x611.png"),
         ("3", "Print", "p2_x16.png"), ("4", "Learn & Play!", "p13_x245.png")]
for i, (num, lab, ic) in enumerate(steps):
    cx = 480 + i * 680
    d.ellipse((cx - 260, 560, cx + 260, 1080), fill=WHITE, outline=PINK, width=10)
    put_icon(im, ic, cx, 820, 300)
    d.ellipse((cx - 85, 470, cx + 85, 640), fill=PINK_D)
    ctext(d, num, 497, F(FRE, 100), WHITE, cx=cx)
    ctext(d, lab, 1140, F(FRE, 78), INK, cx=cx)
d.rounded_rectangle((330, 1420, 2670, 1900), radius=60, fill=WHITE, outline=PINK, width=6)
ctext(d, "This is a DIGITAL product", 1490, F(FRE, 78), PINK_D)
ctext(d, "No physical item will be shipped.", 1620, F(FRS, 64), INK)
ctext(d, "Your PDF files are ready to download right after purchase.", 1730, F(FRS, 58), INK)
save(im, "07-how-it-works.jpg")
