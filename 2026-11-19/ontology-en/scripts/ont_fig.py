# Ontology note figure engine (PIL only). Family = AIO Palantir PIL family (meo_build/ua_build): near-white (249,249,251) canvas + faint 30.4deg grid,
# procedural iso slabs (ont_lib.iso_slab: ratio .591, T 36, outline 3.6, greys 185/158/121), right-angle connectors with dots (no arrowheads),
# hairline rules, pills, violet #7B6CE0 / blue #3D8BFF only as thin accents. Rewritten as a primitive-based engine (no labels.json) for this note.
# Every drawn string is registered; QA asserts: >=40px, <=12 labels, each once, in margins, no text/text or text/line/plate overlap, lines clear of plates.
import sys,os,itertools; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); from ont_lib import *
W,H=2752,1536; OUT=BASE; MG=105
INK=(17,17,17); BODY=(48,48,54); MUTED=(66,66,70); PILL=(116,116,120); VIOLET=(123,108,224); BLUE=(61,139,255); HAIR=(154,154,154)
CONN_LINE=(86,86,90); CONN_DOT=(38,38,42); CONN_W=3; CONN_R=7; RATIO=0.591; T=36.0; MINPX=40; G=16
def F(s,bold=True): return ja(s,bold=bold)
def canvas():
    bg=np.full((H,W,3),(249,249,251),np.float32)
    g=np.zeros((H,W),np.float32); k=np.tan(np.deg2rad(30.4)); step=295
    for c in range(-4000,6000,step):
        cv2.line(g,(0,int(c)),(W,int(c-k*W)),1.0,2,cv2.LINE_AA); cv2.line(g,(0,int(c-k*W)),(W,int(c)),1.0,2,cv2.LINE_AA)
    return bg*(1-0.07*np.clip(g,0,1)[...,None])
def TOP(cy,A): return cy-A*RATIO
def BOT(cy,A): return cy+A*RATIO+T
def pts(cx,cy,A):
    B=A*RATIO; return dict(L=(cx-A,cy),T=(cx,cy-B),R=(cx+A,cy),Bt=(cx,cy+B),L2=(cx-A,cy+T),R2=(cx+A,cy+T),B2=(cx,cy+B+T))
def splitw(label,wrap):
    if wrap is None: return [label]
    parts=wrap.split('⏎')
    ok=[c for c in itertools.product(('',' '),repeat=len(parts)-1) if parts[0]+''.join(s+p for s,p in zip(c,parts[1:]))==label]
    assert ok,('wrap != label',wrap,label); return parts
class Fig:
    def __init__(s,ID): s.ID=ID; s.slabs=[]; s.lines=[]; s.items=[]; s.labels=[]
    def slab(s,cx,cy,A,accent=None,dashed=False):
        s.slabs.append(dict(c=(cx,cy),A=A,accent=accent,dashed=dashed)); return len(s.slabs)-1
    def face(s,i,rows,fs=56,minfs=MINPX):
        """rows: list of (label,kind,wrap) kind h|t ; auto-shrinks to fit the diamond (margin), never below 40"""
        s.items.append(dict(type='face',slab=i,rows=rows,fs=fs,minfs=minfs))
        for l,_,_ in rows: s.labels.append(l)
    def text(s,label,x,y,size=48,anchor='mm',kind='t',wrap=None,color=None,pitch=1.3):
        s.items.append(dict(type='text',label=label,xy=(x,y),size=size,anchor=anchor,kind=kind,wrap=wrap,color=color,pitch=pitch)); s.labels.append(label)
    def pill(s,label,x,y,size=44,col=PILL,fill=(249,249,251),left=False):
        s.items.append(dict(type='pill',label=label,xy=(x,y),size=size,col=col,fill=fill,left=left)); s.labels.append(label)
    def conn(s,path,dashed=False): s.lines.append(dict(kind='conn',path=path,dashed=dashed))
    def rule(s,path,dots=True): s.lines.append(dict(kind='rule',path=path,dots=dots))
    def box(s,x0,y0,x1,y1,col=VIOLET,dashed=False,w=3):   # v3: thin enclosing outline (scope of a name); QA'd like a line
        s.lines.append(dict(kind='box',rect=(x0,y0,x1,y1),col=col,dashed=dashed,w=w))
    # ---------- rendering
    def _faceplan(s,d,it):
        p=s.slabs[it['slab']]; cx,cy=p['c']; A=p['A']; B=A*RATIO; M=26 if A>=400 else 16
        def plan(fs):
            fh=int(round(fs*1.15)); ops=[]; y=0
            for n,(lab,kind,wrap) in enumerate(it['rows']):
                if n>0: y+=fs*0.45
                sz=fh if kind=='h' else fs; f=F(sz); pch=sz*1.3; ls=splitw(lab,wrap)
                for k,t in enumerate(ls): ops.append((y+pch/2+k*pch,t,f,INK if kind=='h' else BODY,sz))
                y+=pch*len(ls)
            res=[]; ok=True
            for yy,t,f,col,sz in ops:
                Y=cy-y/2+yy; bb=d.textbbox((cx,Y),t,font=f,anchor='mm'); res.append(((cx,Y),t,f,col,bb,sz))
                for X in (bb[0],bb[2]):
                    for YY in (bb[1],bb[3]):
                        if abs(X-cx)/(A-M)+abs(YY-cy)/(B-M*RATIO)>1: ok=False
            return ok,res
        for fs in range(it['fs'],it['minfs']-1,-1):
            ok,res=plan(fs)
            if ok: return fs,res
        raise AssertionError(('face text does not fit at >=40px',s.ID,it['rows'],max((f for f in range(120,20,-1) if plan(f)[0]),default=None)))
    def render(s):
        out=canvas(); sils=[]
        for p in s.slabs:
            cx,cy=p['c']; A=p['A']
            if p['dashed']:
                q=pts(cx,cy,A); im=Image.new('L',(W,H),0); ImageDraw.Draw(im).polygon([q['L'],q['T'],q['R'],q['R2'],q['B2'],q['L2']],fill=255)
                m=cv2.dilate((np.array(im)>0).astype(np.uint8),np.ones((5,5),np.uint8))>0
                x0,x1=cx-A,cx+A; y0,y1=TOP(cy,A),BOT(cy,A); assert x0>=100 and x1<=W-100 and y0>=100 and y1<=H-100,('margin',s.ID,p)
            else:
                spr,al,fm=iso_slab(float(A)); Hd,Wd=al.shape; pad=3.6/2+1; B=A*RATIO
                x0=int(round(cx-Wd/2)); y0=int(round(cy-(pad+B)))
                assert x0>=100 and y0>=100 and x0+Wd<=W-100 and y0+Hd<=H-100,('margin',s.ID,cx,cy,A)
                reg=out[y0:y0+Hd,x0:x0+Wd]; reg[:]=reg*(1-al[...,None])+spr*al[...,None]
                m=np.zeros((H,W),bool); m[y0:y0+Hd,x0:x0+Wd]=al>0.5
            sils.append(m)
        for i in range(len(sils)):
            dist=cv2.distanceTransform((~sils[i]).astype(np.uint8),cv2.DIST_L2,5)
            for j in range(i+1,len(sils)): md=dist[sils[j]].min(); assert md>=40,('plates too close',s.ID,i,j,md)
        foot=np.any(sils,0) if sils else np.zeros((H,W),bool); fd=cv2.dilate(foot.astype(np.uint8),np.ones((9,9),np.uint8))>0
        # lines (4x supersampled)
        ss=4; Lc=Image.new('L',(W*ss,H*ss),0); Dc=Image.new('L',(W*ss,H*ss),0); Lr=Image.new('L',(W*ss,H*ss),0); Dr=Image.new('L',(W*ss,H*ss),0)
        boxes_l=[]
        for ln in s.lines:
            if ln['kind']=='box':
                x0,y0,x1,y1=ln['rect']; im=Image.new('L',(W*ss,H*ss),0); dl=ImageDraw.Draw(im); w=ln['w']*ss
                segs=[((x0,y0),(x1,y0)),((x1,y0),(x1,y1)),((x1,y1),(x0,y1)),((x0,y1),(x0,y0))]
                for (a0,b0),(a1,b1) in segs:
                    if ln['dashed']:
                        Lg=abs(a1-a0)+abs(b1-b0); t=0
                        while t<Lg:
                            t1=min(Lg,t+20); f0,f1=t/Lg,t1/Lg
                            dl.line([((a0+(a1-a0)*f0)*ss,(b0+(b1-b0)*f0)*ss),((a0+(a1-a0)*f1)*ss,(b0+(b1-b0)*f1)*ss)],fill=255,width=w); t=t1+14
                    else: dl.line([(a0*ss,b0*ss),(a1*ss,b1*ss)],fill=255,width=w)
                for q in ((x0,y0),(x1,y0),(x1,y1),(x0,y1)): r=w/2; dl.rectangle([q[0]*ss-r,q[1]*ss-r,q[0]*ss+r,q[1]*ss+r],fill=255)
                boxes_l.append((im,ln['col'])); continue
            path=ln['path']
            for (x0,y0),(x1,y1) in zip(path,path[1:]): assert x0==x1 or y0==y1,('segment not orthogonal',s.ID,path)
            if ln['kind']=='conn':
                dl=ImageDraw.Draw(Lc); dd=ImageDraw.Draw(Dc)
                for (x0,y0),(x1,y1) in zip(path,path[1:]):
                    if ln['dashed']:
                        Lg=abs(x1-x0)+abs(y1-y0); t=0
                        while t<Lg:
                            t1=min(Lg,t+20); f0,f1=t/Lg,t1/Lg
                            dl.line([((x0+(x1-x0)*f0)*ss,(y0+(y1-y0)*f0)*ss),((x0+(x1-x0)*f1)*ss,(y0+(y1-y0)*f1)*ss)],fill=255,width=CONN_W*ss); t=t1+14
                    else: dl.line([(x0*ss,y0*ss),(x1*ss,y1*ss)],fill=255,width=CONN_W*ss)
                for x,y in path: dd.ellipse([(x-CONN_R)*ss,(y-CONN_R)*ss,(x+CONN_R)*ss,(y+CONN_R)*ss],fill=255)
            else:
                dl=ImageDraw.Draw(Lr); dd=ImageDraw.Draw(Dr)
                for (x0,y0),(x1,y1) in zip(path,path[1:]): dl.line([(x0*ss,y0*ss),(x1*ss,y1*ss)],fill=255,width=2*ss)
                if ln['dots']:
                    for x,y in (path[0],path[-1]): r=5; dd.ellipse([(x-r)*ss,(y-r)*ss,(x+r)*ss,(y+r)*ss],fill=255)
        linemask=np.zeros((H,W),bool)
        for im,col in boxes_l:
            la=np.array(im.resize((W,H),Image.BOX),np.float32)/255; out=out*(1-la[...,None])+np.array(col,np.float32)*la[...,None]; linemask|=la>0.05
        for Lm,Dm,lc,dc in ((Lr,Dr,HAIR,(90,90,94)),(Lc,Dc,CONN_LINE,CONN_DOT)):
            la=np.array(Lm.resize((W,H),Image.BOX),np.float32)/255; da=np.array(Dm.resize((W,H),Image.BOX),np.float32)/255
            out=out*(1-la[...,None])+np.array(lc,np.float32)*la[...,None]; out=out*(1-da[...,None])+np.array(dc,np.float32)*da[...,None]
            linemask|=(la>0.05)|(da>0.05)
        if (linemask&fd).any(): ys,xs=np.where(linemask&fd); raise AssertionError(('a line touches a plate',s.ID,int(xs.min()),int(ys.min()),int(xs.max()),int(ys.max())))
        img=Image.fromarray(np.clip(out+0.5,0,255).astype(np.uint8)); d=ImageDraw.Draw(img)
        for p in s.slabs:
            cx,cy=p['c']; A=p['A']; q=pts(cx,cy,A)
            if p['dashed']:
                d.polygon([q['L'],q['Bt'],q['B2'],q['L2']],fill=(226,226,229)); d.polygon([q['Bt'],q['R'],q['R2'],q['B2']],fill=(214,214,218)); d.polygon([q['L'],q['T'],q['R'],q['Bt']],fill=(238,238,241))
                for a,b in [('L','T'),('T','R'),('R','R2'),('R2','B2'),('B2','L2'),('L2','L'),('L','Bt'),('Bt','R'),('Bt','B2')]:
                    (x0,y0),(x1,y1)=q[a],q[b]; Lg=((x1-x0)**2+(y1-y0)**2)**.5; t=0
                    while t<Lg:
                        t1=min(Lg,t+22); d.line([(x0+(x1-x0)*t/Lg,y0+(y1-y0)*t/Lg),(x0+(x1-x0)*t1/Lg,y0+(y1-y0)*t1/Lg)],fill=(120,120,124),width=3); t=t1+14
            if p['accent']:
                B=A*RATIO; col=BLUE if p['accent']=='blue' else VIOLET
                d.line([(cx-A+12,cy),(cx,cy-B+6),(cx+A-12,cy)],fill=col,width=5,joint='curve')
        if getattr(s,'uniform',False):   # all face stacks at the same (smallest fitting) size
            m=min(s._faceplan(d,it)[0] for it in s.items if it['type']=='face')
            for it in s.items:
                if it['type']=='face': it['fs']=m
        boxes=[]; drawn=[]; sizes=[]
        for it in s.items:
            if it['type']=='face':
                fs,res=s._faceplan(d,it); sizes.append(fs)
                for xy,t,f,col,bb,sz in res: d.text(xy,t,font=f,fill=col,anchor='mm'); boxes.append(('face',bb))
                drawn+=[r[0] for r in it['rows']]
            elif it['type']=='text':
                sz=it['size']; f=F(sz); ls=splitw(it['label'],it['wrap']); x,y=it['xy']; pch=sz*it['pitch']; n=len(ls); a=it['anchor']
                col=it['color'] or (INK if it['kind']=='h' else (MUTED if it['kind']=='note' else BODY))
                for k,t in enumerate(ls):
                    yy=y+(k-(n-1)/2)*pch; bb=d.textbbox((x,yy),t,font=f,anchor=a); d.text((x,yy),t,font=f,fill=col,anchor=a); boxes.append(('canvas',bb))
                sizes.append(sz); drawn.append(it['label'])
            elif it['type']=='pill':
                sz=it['size']; f=F(sz); x,y=it['xy']; px,py=0.6*sz,0.36*sz
                if it['left']: w0=d.textlength(it['label'],font=f); x=x+px+w0/2
                bb=d.textbbox((x,y),it['label'],font=f,anchor='mm')
                r=(bb[0]-px,y-0.5*sz-py,bb[2]+px,y+0.5*sz+py); d.rounded_rectangle(r,radius=(r[3]-r[1])/2,outline=it['col'],width=3,fill=it['fill'])
                d.text((x,y),it['label'],font=f,fill=MUTED,anchor='mm'); boxes.append(('canvas',r)); sizes.append(sz); drawn.append(it['label'])
        # ---- QA
        assert min(sizes)>=MINPX,('text <40px',s.ID,min(sizes))
        assert len(s.labels)==len(set(s.labels)),('label repeated',s.ID,[l for l in s.labels if s.labels.count(l)>1])
        assert len(s.labels)<=12,('>12 labels',s.ID,len(s.labels)); assert sorted(drawn)==sorted(s.labels)
        for kind,b in boxes:
            if kind=='canvas':
                assert b[0]>=MG and b[1]>=MG and b[2]<=W-MG and b[3]<=H-MG,('text outside margin',s.ID,b)
                bm=np.zeros((H,W),bool); bm[int(b[1])-4:int(b[3])+5,int(b[0])-4:int(b[2])+5]=True
                assert not (bm&foot).any(),('canvas text overlaps a plate',s.ID,b)
            bm=np.zeros((H,W),bool); bm[int(b[1])-6:int(b[3])+7,int(b[0])-6:int(b[2])+7]=True
            assert not (bm&linemask).any(),('text overlaps a line',s.ID,b)
        for i in range(len(boxes)):
            for j in range(i+1,len(boxes)):
                a,b=boxes[i][1],boxes[j][1]; assert a[2]+8<b[0] or b[2]+8<a[0] or a[3]+4<b[1] or b[3]+4<a[1],('texts overlap',s.ID,a,b)
        print(f'{s.ID}: OK {len(s.labels)} labels each once; min text {min(sizes)}px; face sizes {[x for x,it in zip(sizes,s.items) if it["type"]=="face"]}; plates {len(s.slabs)}')
        return img
    def save(s):
        img=s.render(); img.save(OUT+f'raw/{s.ID}.png'); dst=OUT+f'{s.ID}.jpg'
        img.convert('RGB').save(dst,'JPEG',quality=95,subsampling=0,optimize=True)
        chk=Image.open(dst); assert chk.size==(W,H) and chk.mode=='RGB'
        return img
