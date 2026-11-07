import sys, pymupdf as fitz
S, a4path, out = sys.argv[1], sys.argv[2], sys.argv[3]
src = fitz.open(a4path); lt = fitz.open(); W, H = 612, 792
p = lt.new_page(width=W, height=H); ch = W * 3504 / 2616
p.insert_image(fitz.Rect(0, (H - ch) / 2, W, (H + ch) / 2), filename=S + '/cov/cover_letter.jpg')
pink = (240/255, 143/255, 161/255)
for i in range(1, len(src)):
    sp = src[i].rect; s = H / sp.height; w = sp.width * s; x0 = (W - w) / 2
    p = lt.new_page(width=W, height=H)
    p.draw_rect(fitz.Rect(0, 0, W, H), color=None, fill=pink, overlay=False)
    p.show_pdf_page(fitz.Rect(x0, 0, x0 + w, H), src, i)
lt.set_metadata(src.metadata); lt.save(out, garbage=4, deflate=True)
