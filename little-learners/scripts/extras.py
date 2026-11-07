# Adds 3 new pages (name page, star chart, certificate) to the A4 workbook, reusing the
# book's own frame image, Agbalumo font and illustrations (by xref, so no duplicated data).
import sys, math, pymupdf as fitz
S, src, out = sys.argv[1], sys.argv[2], sys.argv[3]
font = fitz.Font(fontfile=S + "/fonts/Agbalumo.ttf")
TRACK = -0.054
BLACK = (0, 0, 0); GRAY = (0.35, 0.35, 0.35); LINE = (0.55, 0.55, 0.55)
PINK = (240/255, 143/255, 161/255); PINK_D = (238/255, 144/255, 154/255)
YEL = (1, 0.84, 0.35)
FRAME, KIDS, RABBIT, CHICK, BUTTERFLY = 13, 65, 611, 245, 16
TULIP, SUNFLOWER, BEE, MUSHROOM, CLOUD = 541, 543, 539, 545, 537
doc = fitz.open(src)
CX = doc[1].rect.width / 2

def width(s, sz, tr): return font.text_length(s, sz) + tr * sz * (len(s) - 1)
def text(p, s, base, sz, color=BLACK, track=0.0, cx=CX):
    tw = fitz.TextWriter(p.rect); x = cx - width(s, sz, track) / 2
    for ch in s:
        tw.append((x, base), ch, font=font, fontsize=sz); x += font.text_length(ch, sz) + track * sz
    tw.write_text(p, color=color)
def title(p, s, base=106.44, sz=45): text(p, s, base, sz, BLACK, TRACK)
def new_page(at):
    p = doc.new_page(at, width=595.5, height=842.25)
    p.insert_image(fitz.Rect(-9, -9, 605, 852), xref=FRAME)
    return p
def img(p, xref, x0, y0, x1, y1): p.insert_image(fitz.Rect(x0, y0, x1, y1), xref=xref)
def star_pts(cx, cy, R, r=None, rot=-90):
    r = r or R * 0.48
    return [fitz.Point(cx + (R if i % 2 == 0 else r) * math.cos(math.radians(rot + i * 36)),
                       cy + (R if i % 2 == 0 else r) * math.sin(math.radians(rot + i * 36))) for i in range(10)]
def star(p, cx, cy, R, fill=(1, 1, 1), width=2.6):
    pts = star_pts(cx, cy, R); pts.append(pts[0])
    p.draw_polyline(pts, color=BLACK, fill=fill, width=width, lineJoin=1, closePath=True)
def writing_line(p, x0, x1, y): p.draw_line((x0, y), (x1, y), color=LINE, width=1.4)

# ---------- 1. This Book Belongs To (after cover) ----------
p = new_page(1)
title(p, "This Book Belongs To")
box = fitz.Rect(150, 140, 445.5, 400)
p.draw_rect(box, color=PINK, width=3, radius=0.08, dashes="[9 6] 0")
text(p, "Draw yourself", 262, 18, LINE)
text(p, "or paste your photo here", 286, 18, LINE)
rows = [("My name is", 452), ("I am", 510), ("I started this book on", 568)]
for lab, y in rows:
    lw = font.text_length(lab, 24)
    tw = fitz.TextWriter(p.rect); tw.append((70, y), lab, font=font, fontsize=24); tw.write_text(p, color=BLACK)
    if lab == "I am":
        writing_line(p, 70 + lw + 10, 70 + lw + 90, y + 2)
        tw = fitz.TextWriter(p.rect); tw.append((70 + lw + 100, y), "years old", font=font, fontsize=24); tw.write_text(p, color=BLACK)
    else:
        writing_line(p, 70 + lw + 10, 525, y + 2)
img(p, KIDS, 50, 615, 240, 805)
img(p, BUTTERFLY, 300, 660, 400, 760)
img(p, RABBIT, 420, 650, 530, 790)

# ---------- 2. My Star Chart ----------
p = new_page(2)
title(p, "My Star Chart")
text(p, "Color a star each time you finish a page!", 140, 17, GRAY)
cols, rows_n = 5, 6
gx0, gx1, gy0, gy1 = 72, 523.5, 160, 712
cw, rh = (gx1 - gx0) / cols, (gy1 - gy0) / rows_n
labels = list(range(2, 31))          # matches printed page numbers 2-30
for i in range(cols * rows_n):
    cx = gx0 + cw * (i % cols + 0.5); cy = gy0 + rh * (i // cols + 0.5)
    if i < len(labels):
        star(p, cx, cy + 2, 40)
        s = str(labels[i]); text(p, s, cy + 11, 20, PINK_D, cx=cx)
    else:
        img(p, CHICK, cx - 34, cy - 44, cx + 34, cy + 24)
        text(p, "I did it!", cy + 42, 17, BLACK, cx=cx)
for k, x in enumerate([TULIP, SUNFLOWER, BEE, MUSHROOM, CLOUD]):
    cx = 120 + k * 89; img(p, x, cx - 30, 722, cx + 30, 782)

# ---------- 3. Certificate (last page) ----------
p = new_page(-1)
title(p, "Certificate", base=112, sz=54)
text(p, "of Completion", 152, 30, BLACK, TRACK)
# rosette badge
bx, by = CX, 252
p.draw_polyline([(bx - 30, by + 30), (bx - 46, by + 104), (bx - 28, by + 92), (bx - 14, by + 108), (bx - 2, by + 40)],
                color=BLACK, fill=PINK, width=2, lineJoin=1, closePath=True)
p.draw_polyline([(bx + 30, by + 30), (bx + 46, by + 104), (bx + 28, by + 92), (bx + 14, by + 108), (bx + 2, by + 40)],
                color=BLACK, fill=PINK, width=2, lineJoin=1, closePath=True)
sc = [fitz.Point(bx + (60 if j % 2 == 0 else 52) * math.cos(math.radians(j * 7.5)),
                 by + (60 if j % 2 == 0 else 52) * math.sin(math.radians(j * 7.5))) for j in range(48)]
sc.append(sc[0]); p.draw_polyline(sc, color=BLACK, fill=PINK, width=2, lineJoin=1, closePath=True)
p.draw_circle((bx, by), 42, color=BLACK, fill=YEL, width=2)
star(p, bx, by + 3, 28, fill=(1, 1, 1), width=2)
text(p, "This certificate is proudly presented to", 392, 18, GRAY)
writing_line(p, 110, 485.5, 448)
text(p, "for completing the", 490, 18, GRAY)
text(p, "Little Learners", 530, 30, BLACK, TRACK)
text(p, "Preschool Activity Workbook", 566, 30, BLACK, TRACK)
text(p, "Great job! Keep learning and growing!", 612, 18, PINK_D)
for x0, x1, lab in [(85, 265, "Date"), (330, 510, "Signature")]:
    writing_line(p, x0, x1, 655); text(p, lab, 676, 16, GRAY, cx=(x0 + x1) / 2)
img(p, CHICK, 70, 705, 150, 785)
img(p, BUTTERFLY, 257, 708, 338, 789)
img(p, RABBIT, 437, 680, 537, 790)

for n in (2, 3, len(doc)):
    print("new page", n)
doc.save(out, garbage=4, deflate=True)
print("pages", len(doc))
