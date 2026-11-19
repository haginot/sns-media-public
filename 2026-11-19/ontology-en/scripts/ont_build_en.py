# English figures for HAGINO's note on PIVOT appearance #3 (ontology).
# Same engine, layout, palette and size as the Japanese originals in
# /workspace/note-pivot-ontology-20261116/figures/ (F1–F5, F7–F12).
# F7 follows the published note: short pill "An analogy from the show"
# (the on-disk F7.jpg matches raw/F7_tatoe_only.jpg).
# Run: python3 ont_build_en.py [F1 F3 ...]
import sys,os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); from ont_fig import *
FIG={}
def fig(fn): FIG[fn.__name__]=fn; return fn

@fig
def F1():   # key visual: one base plate (ontology) carries semantics (dots & lines) and kinetics (approval & write-back)
    f=Fig('F1')
    f.pill('Third appearance on PIVOT',200,470,44,left=True)
    f.text('A blueprint of meaning',200,650,120,anchor='lm',kind='h',wrap='A blueprint⏎of meaning',pitch=1.25)
    f.text("It's more than just data",206,880,60,anchor='lm',kind='t')
    b=f.slab(1900,1060,540,accent='violet'); f.face(b,[('Ontology','h',None)],fs=76)
    s1=f.slab(1560,400,310); f.face(s1,[('Semantic elements','h',None)],fs=47); f.text('Dots and lines',1560,160,46)
    s2=f.slab(2240,400,310,accent='blue'); f.face(s2,[('Kinetic elements','h',None)],fs=47); f.text('Approval and write-back',2240,160,46)
    for x in (1560,2240):
        top=1060-540*RATIO*(1-abs(x-1900)/540); f.conn([(x,int(BOT(400,310))+G),(x,int(top)-26)])
    return f

@fig
def F3():   # v3: blueprint layer vs instance graph layer stay separate; Foundry's name covers both + the moving parts (one outline)
    f=Fig('F3')
    f.text('What Foundry collectively calls the “Ontology”',190,215,46,anchor='lm',kind='t')
    f.box(150,280,2600,1180)
    L=f.slab(540,700,360,accent='violet'); f.face(L,[('Blueprint of meaning','h','Blueprint of⏎meaning'),('Types, relations, constraints','t','Types, relations,⏎constraints')],fs=56)
    n1,n2,A=1360,1800,110
    f.conn([(540+360+G,700),(n1-A-G,700)]); f.text('Built from the blueprint',1070,610,44)
    f.text('The graph (also called a knowledge graph)',1580,400,48,kind='h')
    for x in (n1,n2): f.slab(x,700,A)
    f.conn([(n1+A+G,700),(n2-A-G,700)]); f.text('appears on',1580,645,44)
    f.text('Takahiro Hagino',n1,900,44); f.text('OpenClaw Demo Explained',n2,900,44,wrap='OpenClaw Demo⏎Explained')
    f.pill('Not the same “graph” as in Functions',1580,1010,42)
    K=f.slab(2310,700,230,accent='blue'); f.face(K,[('Moving parts','h',None)],fs=56)
    f.conn([(n2+A+G,700),(2310-230-G,700)])
    f.rule([(2310,int(BOT(700,230))+G),(2310,940)]); f.text('Actions, Functions, and dynamic security',2310,1010,44,wrap='Actions, Functions,⏎and dynamic security')
    f.text('The blueprint and the graph are different layers',1376,1320,60,kind='h')
    return f

@fig
def F4():   # Palantir: every decision = data + logic + action
    f=Fig('F4'); f.uniform=True
    f.text('The three building blocks of a decision',1376,230,64,kind='h')
    xs=(500,1376,2252); y=640; A=380
    rows=[[('Data','h',None),('Objects and links','t',None)],[('Logic','h',None),('Rules and models','t',None)],[('Action','h',None),('Verbs, permissions, and write-back','t','Verbs, permissions,⏎and write-back')]]
    qs=[('What facts form the context of the decision?','What facts form the context⏎of the decision?'),('What rules act as guardrails?',None),('How does the decision take effect in the real world?','How does the decision⏎take effect in the real world?')]
    for i,x in enumerate(xs):
        s=f.slab(x,y,A,accent='violet' if i==2 else None); f.face(s,rows[i],fs=60)
        f.rule([(x,int(BOT(y,A))+G),(x,1000)]); f.text(qs[i][0],x,1080,46,wrap=qs[i][1])
    for a,b in ((xs[0],xs[1]),(xs[1],xs[2])): f.conn([(a+A+G,y),(b-A-G,y)])
    f.text('The premise is collaboration among operators, analysts, specialists, and AI',1376,1310,44,kind='note',wrap='The premise is collaboration among⏎operators, analysts, specialists, and AI')
    f.pill('The architecture write-up adds security, as a fourth',1376,325,40)
    return f

@fig
def F5():   # semantics vs kinetics; Excel can carry meaning but not guaranteed control
    f=Fig('F5'); f.uniform=True
    xs=(500,1376,2252); y=640; A=380
    e=f.slab(xs[0],y,A,dashed=True); f.face(e,[('Excel','h',None),('You can attach meaning','t',None)],fs=58)
    s1=f.slab(xs[1],y,A); f.face(s1,[('Semantic elements','h',None),('Objects, properties, and links','t','Objects, properties,⏎and links')],fs=58)
    s2=f.slab(xs[2],y,A,accent='blue'); f.face(s2,[('Kinetic elements','h',None),('Actions, Functions, dynamic security','t','Actions, Functions,⏎dynamic security')],fs=58)
    f.conn([(xs[1]+A+G,y),(xs[2]-A-G,y)])
    f.rule([(xs[1]-A,350),(xs[1]-A,310),(xs[2]+A,310),(xs[2]+A,350)],dots=False); f.text('Ontology',(xs[1]+xs[2])//2,240,56,kind='h')
    f.rule([(xs[0],int(BOT(y,A))+G),(xs[0],990)]); f.text('Permissions, transactions, and side effects are not guaranteed to be controlled',xs[0],1080,46,wrap='Permissions, transactions,⏎and side effects are not⏎guaranteed to be controlled')
    f.rule([(xs[2],int(BOT(y,A))+G),(xs[2],990)]); f.pill('Submission criteria (validation)',xs[2],1050,46,col=BLUE)
    f.text('Meaning alone is not enough to control what an agent does',1376,1300,56,kind='h')
    return f

@fig
def F8():   # one order object, two different actions depending on shipment state
    f=Fig('F8')
    f.text('Cancel and return are different actions',200,200,60,anchor='lm',kind='h')
    o=f.slab(620,760,400); f.face(o,[('Order','h',None),('Object','t',None)],fs=64)
    f.rule([(620,int(BOT(760,400))+G),(620,1085)]); f.pill('Shipment status (property)',620,1140,44)
    A=330; xa=2000; yu,yl=430,1090
    u=f.slab(xa,yu,A,accent='violet'); f.face(u,[('Cancel','h',None),('Cancel the order','t',None)],fs=56)
    l=f.slab(xa,yl,A,accent='violet'); f.face(l,[('Return','h',None),('Process a return','t',None)],fs=56)
    f.conn([(620+400+G,760),(1300,760)]); f.conn([(1300,yu),(1300,yl)])
    f.conn([(1300,yu),(xa-A-G,yu)]); f.conn([(1300,yl),(xa-A-G,yl)])
    f.text('Before shipment',1480,yu-55,46); f.text('After shipment',1480,yl-55,46)
    f.text("A shipped order can't be canceled, so it's handled as a return",200,1330,44,anchor='lm',kind='note')
    return f

@fig
def F9():   # demo flow (dummy data): detect -> traverse -> human approval -> sync to related systems; bypass = autonomous, responsibility stays
    f=Fig('F9')
    f.pill('Hypothetical, dummy data',200,200,42,left=True)
    xs=(390,1040,1690,2340); y=620; A=270
    rows=[('Detect a cancellation','Detect a⏎cancellation'),('Walk the graph for candidates','Walk the graph⏎for candidates'),('A person approves','A person⏎approves'),('Sync to related systems','Sync to related⏎systems')]
    for i,x in enumerate(xs):
        s=f.slab(x,y,A,accent='violet' if i==2 else None); f.face(s,[(rows[i][0],'h',rows[i][1])],fs=50)
    f.uniform=True
    for a,b in zip(xs,xs[1:]): f.conn([(a+A+G,y),(b-A-G,y)])
    top=int(TOP(y,A))-G; f.conn([(xs[1],top),(xs[1],270),(xs[3],270),(xs[3],top)],dashed=True)
    f.text('Even in autonomous mode, responsibility remains',(xs[1]+xs[3])//2,212,44,kind='note')
    px=(500,1110,1720,2340); by=1060
    f.conn([(xs[3],int(BOT(y,A))+G),(xs[3],by)]); f.rule([(px[0],by),(xs[3],by)],dots=False)
    for i,(x,lab) in enumerate(zip(px,('Show planning data','Description field','Promo clearance','Contacting the talent'))):
        f.rule([(x,by),(x,1148)]); f.pill(lab,x,1200,44)
    return f

@fig
def F10():  # small maps per business, linked into a world map; individuals vs enterprises note
    f=Fig('F10'); f.uniform=True
    xs=480; ys=(300,650,1000); A=230
    for yy,lab,wr in zip(ys,('Expense reports','Orders and returns','Appearance booking'),('Expense⏎reports','Orders and⏎returns','Appearance⏎booking')):
        s=f.slab(xs,yy,A); f.face(s,[(lab,'h',wr)],fs=52)
    r=xs+A+G; f.conn([(r,ys[0]),(900,ys[0]),(900,ys[2]),(r,ys[2])]); f.conn([(r,ys[1]),(1130-G,ys[1])])
    w=f.slab(1650,650,520,accent='violet'); f.face(w,[('A world map','h',None),('Small maps joined by links','t','Small maps joined⏎by links')],fs=60)
    f.text('Start with the work at hand, and draw a small map',1650,180,56,kind='h')
    f.pill('Write down the rules, data, systems, and permissions',1650,270,42)
    f.text('Individuals and small teams: a shared file every agent can read may be enough',1650,1120,44,kind='note',wrap='Individuals and small teams:⏎a shared file every agent can read may be enough')
    f.text('Large enterprises: choosing a platform becomes a decision',1650,1220,44,kind='note')
    return f

@fig
def F2():   # the show's triplet example (HAGINO's previous appearance) + properties
    f=Fig('F2'); f.uniform=True
    f.text('A triplet example: object—link—object',1376,220,60,kind='h')
    xs=(500,1376,2252); y=640; A=380
    rows=[[('Person','h',None),('Takahiro Hagino','t',None)],[('Show','h',None),('OpenClaw Demo Explained','t','OpenClaw Demo⏎Explained')],[('Theme','h',None),('AI','t',None)]]
    for i,x in enumerate(xs):
        sl=f.slab(x,y,A,accent='violet' if i==1 else None); f.face(sl,rows[i],fs=58)
    for (a,b),lab in zip(((xs[0],xs[1]),(xs[1],xs[2])),('appears on','covers')):
        f.conn([(a+A+G,y),(b-A-G,y)]); f.text(lab,(a+b)//2,y-100,46)
    f.rule([(xs[1],int(BOT(y,A))+G),(xs[1],1010)]); f.pill('Properties: air date, viewership',xs[1],1070,46)
    f.text('It maps reality in a form close to subject–verb–object (SVO)',1376,1300,44,kind='note')
    return f

@fig
def F7():   # HAGINO's analogy: closer to a contract than to memory (published note uses the short pill)
    f=Fig('F7'); f.uniform=True
    f.pill('An analogy from the show',200,200,42,left=True)
    f.text('Closer to a “contract” than to “memory”',1376,330,64,kind='h')
    m=f.slab(760,760,440,dashed=True); f.face(m,[('Memory','h',None),('Easily becomes fuzzy','t',None)],fs=60)
    c=f.slab(1992,760,440,accent='violet'); f.face(c,[('Contracts and internal rules','h','Contracts and⏎internal rules'),("What's written is what counts",'t',"What's written⏎is what counts")],fs=60)
    f.rule([(1992,int(BOT(760,440))+G),(1992,1170)]); f.text('Above a set amount, a general manager must approve; higher still requires a board resolution',1992,1240,44,kind='note',wrap='Above a set amount, a general manager must approve;⏎higher still requires a board resolution')
    return f

@fig
def F11():  # v3 §2-2: general ontology = the blueprint layer; Foundry = three separate layers inside one named outline
    f=Fig('F11')
    f.text('What “ontology” refers to',200,300,64,anchor='lm',kind='h')
    f.text('Ontology in the general sense',560,840,52,kind='h')
    g=f.slab(560,1140,380,accent='violet'); f.face(g,[('Classes, relations, constraints','h','Classes, relations,⏎constraints'),('RDF, OWL, SHACL','t',None)],fs=54)
    X0=1180; cx=1500; A=200
    f.box(X0,250,2620,1400); f.text('What Foundry collectively calls the “Ontology”',X0+40,310,46,anchor='lm')
    rows=[(500,'Moving parts','Moving⏎parts','Actions, Functions, submission criteria, security, and write-back','Actions, Functions,⏎submission criteria,⏎security, and write-back','blue'),
          (820,'Contents',None,'Objects and links',None,None),
          (1140,'Blueprint',None,'Object types, link types, and properties','Object types, link types,⏎and properties','violet')]
    for cy,h,hwr,t,wr,ac in rows:
        sl=f.slab(cx,cy,A,accent=ac); f.face(sl,[(h,'h',hwr)],fs=54)
        f.rule([(cx+A+G,cy),(cx+A+70,cy)]); f.text(t,cx+A+100,cy,44,anchor='lm',wrap=wr)
    f.conn([(560+380+G,1140),(cx-A-G,1140)],dashed=True); f.text('Same layer',1040,1220,42)
    return f

@fig
def F12():  # v3 §2-4: where each product draws the line called "ontology" — two equal columns, no ranking
    f=Fig('F12'); f.uniform=True
    f.text('Where each product draws the line called “ontology”',1376,160,60,kind='h')
    f.rule([(1376,340),(1376,1400)],dots=False)
    # left: Foundry
    f.text('Foundry Ontology',725,265,52,kind='h')
    f.box(490,322,960,1232)
    for cy,h,wr,ac in ((462,'Moving parts','Moving⏎parts','blue'),(760,'Contents',None,None),(1058,'Definitions',None,'violet')):
        sl=f.slab(725,cy,185,accent=ac); f.face(sl,[(h,'h',wr)],fs=50)
    f.text('Definitions, contents, and moving parts in one box',725,1305,48,wrap='Definitions, contents,⏎and moving parts in one box')
    # right: Fabric IQ
    f.text('The Fabric IQ ontology (preview)',2027,265,52,kind='h')
    f.box(1470,322,2130,792)
    d=f.slab(1800,545,290,accent='violet'); f.face(d,[('Entities, relationships, and rules','h','Entities,⏎relationships,⏎and rules')],fs=52)
    e=f.slab(1800,1050,190); f.face(e,[('Existing data','h','Existing⏎data')],fs=50)
    f.conn([(1800,int(BOT(545,290))+G),(1800,int(TOP(1050,190))-G)])
    f.text('It binds to existing data and has no separate store',1840,862,44,anchor='lm',wrap='It binds to existing data⏎and has no separate store')
    gr=f.slab(2370,1050,170,dashed=True); f.face(gr,[('Graph','h',None)],fs=50)
    f.conn([(1800+190+G,1050),(2370-170-G,1050)],dashed=True)
    f.text('The graph is an optional outer runtime. By default it does not load instances',1990,1300,44,wrap='The graph is an optional outer runtime.⏎By default it does not load instances')
    return f

if __name__=='__main__':
    for n in (sys.argv[1:] or list(FIG)): FIG[n]().save()
