import sys, pymupdf as fitz
S=sys.argv[1]; src, out = sys.argv[2], sys.argv[3]
FONT=S+"/fonts/Agbalumo.ttf"
font=fitz.Font(fontfile=FONT)
TRACK=-0.054   # Canva letter-spacing measured from original titles
MAXW=455
# page: (lines, mode) mode 'orig' = reuse original baselines; ('top',y) explicit first baseline
CFG={
 3:(["Match the Same Animals"],'orig'),
 4:(["Trace the Ladder to Help","the Child Reach the Apple"],('base',None)),
 6:(["Match Each Fruit","to Its Shadow"],'orig'),
 13:(["Trace the Zigzag Lines to","Help the Chick Hatch"],'orig'),
 17:(["Trace the Curved Lines"],'single'),
 22:(["Trace the Curved and","Zigzag Lines"],'orig'),
 23:(["Color the Apples to","Match the Pattern"],'shiftup'),
 25:(["Trace the Horizontal","Curves and Zigzags"],'orig'),
 26:(["Trace and Color the Cloud"],'orig'),
 29:(["Trace and Color the Apple"],'orig'),
}
def width(s,sz): return font.text_length(s,sz)+TRACK*sz*(len(s)-1)
def draw(tw,s,cx,base,sz):
    x=cx-width(s,sz)/2
    for ch in s:
        tw.append((x,base),ch,font=font,fontsize=sz)
        x+=font.text_length(ch,sz)+TRACK*sz
doc=fitz.open(src)
single_base=None
for n,(lines,mode) in CFG.items():
    p=doc[n-1]
    spans=[s for b in p.get_text("dict")["blocks"] for l in b.get("lines",[]) for s in l["spans"] if "Agbalumo" in s["font"]]
    bases=[s["origin"][1] for s in spans]; sz0=spans[0]["size"]
    for s in spans: p.add_redact_annot(fitz.Rect(s["bbox"]),fill=False)
    p.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE,graphics=fitz.PDF_REDACT_LINE_ART_NONE,text=fitz.PDF_REDACT_TEXT_REMOVE)
    sz=sz0
    while max(width(l,sz) for l in lines)>MAXW: sz-=0.5
    lead=42.0
    if mode=='orig' and len(bases)==len(lines): bl=bases
    elif mode=='single': bl=[106.44]
    elif mode=='shiftup': bl=[bases[0]-14, bases[0]-14+lead]
    else: bl=[bases[0]-21+i*lead for i in range(len(lines))] if mode!='orig' else bases
    if n==4: bl=[bases[0]-24, bases[0]-24+lead]
    tw=fitz.TextWriter(p.rect)
    for l,b in zip(lines,bl): draw(tw,l,p.rect.width/2,b,sz)
    tw.write_text(p,color=(0,0,0))
    if n==23:
        tw2=fitz.TextWriter(p.rect); s="Use the color pattern below."; f2=17
        x=p.rect.width/2-font.text_length(s,f2)/2
        tw2.append((x,bl[1]+24),s,font=font,fontsize=f2); tw2.write_text(p,color=(0.25,0.25,0.25))
    print(n,"size",sz,"baselines",[round(b,1) for b in bl],"orig",[round(b,1) for b in bases])
doc.save(out,garbage=3,deflate=True)
