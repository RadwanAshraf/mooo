import sys, pymupdf as fitz
S=sys.argv[1]
orig=fitz.open(S+'/src/orig.pdf'); meta=orig.metadata
meta.update(title="Little Learners - Preschool Activity Workbook", subject="Printable preschool activity workbook (30 pages)")
inter=fitz.open(S+'/work/interior.pdf')
a4=fitz.open(); p=a4.new_page(width=595.5,height=842.25)
p.insert_image(fitz.Rect(0,-26.25,595.5,868.5),filename=S+'/cov/cover_a4.jpg')
a4.insert_pdf(inter,from_page=1,to_page=29); a4.set_metadata(meta)
a4.save(S+'/out/Little-Learners-Full-A4.pdf',garbage=4,deflate=True,deflate_images=True,deflate_fonts=True)
W,H=612,792; src=fitz.open(S+'/out/Little-Learners-Full-A4.pdf'); lt=fitz.open()
p=lt.new_page(width=W,height=H); ch=W*3504/2616
p.insert_image(fitz.Rect(0,(H-ch)/2,W,(H+ch)/2),filename=S+'/cov/cover_letter.jpg')
pink=(240/255,143/255,161/255)
for i in range(1,30):
    sp=src[i].rect; s=H/sp.height; w=sp.width*s; x0=(W-w)/2
    p=lt.new_page(width=W,height=H)
    p.draw_rect(fitz.Rect(0,0,W,H),color=None,fill=pink,overlay=False)
    p.show_pdf_page(fitz.Rect(x0,0,x0+w,H),src,i)
lt.set_metadata(meta); lt.save(S+'/out/Little-Learners-Full-US-Letter.pdf',garbage=4,deflate=True)
