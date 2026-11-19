# Ontology note (PIVOT 3rd) PIL helpers. COPIED 2026-11-16 from aio-research/articles/2026-11-15-chatgpt-meo/images/qa/meo_lib.py (BASE changed only).
import numpy as np, cv2
from scipy.ndimage import binary_fill_holes
from PIL import Image, ImageDraw, ImageFont
BASE='/workspace/ontology-note-en-20261119/figures/'
JA='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
JAB='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
INTER='/usr/share/fonts/truetype/sand-box/google/Inter/Inter-VariableFont_opsz,wght.ttf'
def load(p): return np.array(Image.open(BASE+p).convert('RGB'))
def lum(a): return a.astype(np.float32).mean(2)
def sat(a): return a.max(2).astype(int)-a.min(2).astype(int)
def flood(a,seed,tol=6):
    g=cv2.GaussianBlur(lum(a),(5,5),0).astype(np.uint8)
    h,w=g.shape; m=np.zeros((h+2,w+2),np.uint8)
    cv2.floodFill(g.copy(),m,seed,0,tol,tol,cv2.FLOODFILL_FIXED_RANGE|cv2.FLOODFILL_MASK_ONLY|(255<<8))
    return binary_fill_holes(m[1:-1,1:-1]>0)
def inter(size,wght=600,opsz=None):
    f=ImageFont.truetype(INTER,size)
    try:
        axes=f.get_variation_axes(); vals=[]
        for ax in axes:
            n=ax.get('name',b'');n=n.decode() if isinstance(n,bytes) else n
            if 'eight' in n or n=='wght': vals.append(wght)
            elif 'ptical' in n or n=='opsz': vals.append(opsz or min(32,ax['maximum']))
            else: vals.append(ax['default'])
        f.set_variation_by_axes(vals)
    except Exception as e: print('axes',e)
    return f
def ja(size,bold=False): return ImageFont.truetype(JAB if bold else JA,size,index=0)  # index0 = JP
def planefit_fill(out,mask,ring_px=14,deg=2,within=None):
    """fill mask on a flat-ish face by fitting a low-order polynomial to a ring around it"""
    m=mask.astype(np.uint8)
    ring=(cv2.dilate(m,np.ones((ring_px*2+1,)*2,np.uint8))>0)&~(cv2.dilate(m,np.ones((5,5),np.uint8))>0)
    if within is not None: ring&=within
    ys,xs=np.where(ring); yy,xx=np.where(mask)
    def feats(y,x):
        y=y/1000.;x=x/1000.
        f=[np.ones_like(x),x,y]
        if deg>=2: f+= [x*x,x*y,y*y]
        return np.stack(f,1)
    A=feats(ys,xs)
    for c in range(3):
        v=out[ys,xs,c].astype(np.float64)
        # robust: drop outliers once
        co,*_=np.linalg.lstsq(A,v,rcond=None); r=v-A@co; keep=np.abs(r)<3*r.std()+1
        co,*_=np.linalg.lstsq(A[keep],v[keep],rcond=None)
        out[yy,xx,c]=np.clip(feats(yy,xx)@co,0,255)
    return out

def plates(a,lo=180,hi=205,minar=50000,smax=6):
    l=lum(a); s=sat(a); face=(l>lo)&(l<hi)&(s<smax)
    n,lab,st,cen=cv2.connectedComponentsWithStats(face.astype(np.uint8))
    out=[]
    for i in range(1,n):
        if st[i,4]>minar:
            m0=(lab==i).astype(np.uint8); cs,_=cv2.findContours(m0,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE); hull=cv2.convexHull(np.vstack(cs)); m=np.zeros_like(m0); cv2.fillPoly(m,[hull],1); m=m>0; x,y,w,h,_=st[i]; out.append(dict(mask=m,box=(x,y,w,h),c=(x+w/2,y+h/2)))
    out.sort(key=lambda p:(round(p['c'][1]/300),p['c'][0]))
    return out
def erase_text_on_face(out,face,textmask,grow=5,shrink=1,ringmask=None,protect=None):
    inner=cv2.erode(face.astype(np.uint8),np.ones((shrink*2+1,)*2,np.uint8))>0
    ringok=cv2.erode(face.astype(np.uint8),np.ones((13,13),np.uint8))>0
    if ringmask is not None: ringok&=ringmask
    tm=(cv2.dilate(textmask.astype(np.uint8),np.ones((grow*2+1,)*2,np.uint8))>0)&inner
    if protect is not None: tm&=~protect
    # fill per connected blob region for local fit
    n,lab,st,_=cv2.connectedComponentsWithStats(cv2.dilate(tm.astype(np.uint8),np.ones((41,41),np.uint8)))
    for i in range(1,n):
        reg=(lab==i)&tm
        if reg.any(): planefit_fill(out,reg,ring_px=16,deg=1,within=ringok&~tm)
    return out
def text_lines(img,lines,center,font,fill,pitch,anchor='mm'):
    d=ImageDraw.Draw(img); cx,cy=center; n=len(lines)
    for i,t in enumerate(lines):
        y=cy+(i-(n-1)/2)*pitch
        d.text((cx,y),t,font=font,fill=tuple(int(v) for v in fill),anchor=anchor)
# ---------------- H2 addition: procedural isometric slab ("reconstructed sheet") in the body-plate language.
# Geometry/colours calibrated on the AEO body sprite (qa/assets/body_plate.npz, 799x511; replica at A=397.5 mean |diff| 4.3/255): face half-height/half-width
# ratio 0.591, slab thickness 36 px, ~3.6 px charcoal outline, flat face 185, left side 158, right side 121 (sprite medians).
# Used only where one 799x511 plate cannot hold the rows (05 two log sheets, 06 one log sheet). Same projection, same edge, same
# thickness; larger face. Rendered at 4x and box-downsampled (anti-aliased like the sprite).
def iso_slab(A,ratio=0.591,T=36.0,lw=3.6,face=185.0,left=158.0,right=121.0,line=50.0,ss=4):
    B=A*ratio; pad=lw/2+1
    Wd=int(np.ceil(2*A+2*pad)); Hd=int(np.ceil(2*B+T+2*pad))
    cx,cy=Wd/2.0,pad+B
    def P(x,y): return (x*ss,y*ss)
    L,Tp,R,Bt=P(cx-A,cy),P(cx,cy-B),P(cx+A,cy),P(cx,cy+B)
    L2,R2,B2=P(cx-A,cy+T),P(cx+A,cy+T),P(cx,cy+B+T)
    def poly(pts):
        im=Image.new('L',(Wd*ss,Hd*ss),0); ImageDraw.Draw(im).polygon(pts,fill=255); return im
    def strokes(segs):
        im=Image.new('L',(Wd*ss,Hd*ss),0); d=ImageDraw.Draw(im); w=int(round(lw*ss))
        for a,b in segs:
            d.line([a,b],fill=255,width=w)
            for q in (a,b): r=w/2; d.ellipse([q[0]-r,q[1]-r,q[0]+r,q[1]+r],fill=255)
        return im
    def down(im): return np.array(im.resize((Wd,Hd),Image.BOX)).astype(np.float32)/255.
    fpoly=poly([L,Tp,R,Bt]); lpoly=poly([L,Bt,B2,L2]); rpoly=poly([Bt,R,R2,B2])
    sil=poly([L,Tp,R,R2,B2,L2])
    st=strokes([(L,Tp),(Tp,R),(R,R2),(R2,B2),(B2,L2),(L2,L),(L,Bt),(Bt,R),(Bt,B2)])
    st_np=np.array(st)>0; sil_np=(np.array(sil)>0)|st_np
    col=np.zeros((Hd*ss,Wd*ss),np.float32)
    col[np.array(lpoly)>0]=left; col[np.array(rpoly)>0]=right; col[np.array(fpoly)>0]=face; col[st_np]=line
    a_hi=sil_np.astype(np.float32)
    alpha=down(Image.fromarray((a_hi*255).astype(np.uint8)))
    prem=np.array(Image.fromarray(col*a_hi).resize((Wd,Hd),Image.BOX),np.float32) if False else \
        cv2.resize(col*a_hi,(Wd,Hd),interpolation=cv2.INTER_AREA)
    spr=np.where(alpha[...,None]>1e-6,(prem/np.maximum(alpha,1e-6))[...,None],0).repeat(3,2).astype(np.float32)
    fm_hi=(np.array(fpoly)>0)&~st_np
    fm=cv2.resize(fm_hi.astype(np.float32),(Wd,Hd),interpolation=cv2.INTER_AREA)>0.999
    return spr,alpha,fm
