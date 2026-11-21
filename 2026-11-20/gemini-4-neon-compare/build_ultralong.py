import json,re
def body(f):
    t=open(f,encoding='utf-8-sig').read()
    s=t.find('*** START OF'); s=t.find('\n',s)+1 if s>=0 else 0
    e=t.find('*** END OF'); e=e if e>0 else len(t)
    return t[s:e].strip()
FACTS=[(0.06,"The ledger of the Thornbury Lending Society records that its strongbox could be opened only with the code word heliotrope."),
(0.21,"The Pelham Lending Society, a rival club, kept its own strongbox, and its code word was primrose."),
(0.37,"Mr. Ashcombe, the steward, noted that anyone who gives the Thornbury Lending Society's current code word may collect the sealed parcel kept behind the counter of the Harrowgate post office."),
(0.52,"When the sealed parcel from the Harrowgate post office was finally opened, it held exactly forty-two silver buttons and a folded map."),
(0.68,"Captain Ashcombe later removed eleven of the silver buttons from that parcel to have them reset by a jeweller."),
(0.81,"A later entry in the Thornbury Lending Society's ledger records that at Michaelmas the code word was changed from heliotrope to larkspur."),
(0.93,"The jeweller returned four of the reset silver buttons to the parcel a fortnight afterwards.")]
HERONS=[(0.03,"A blue heron was seen standing in the shallows near the copper kettle bridge."),
(0.15,"Someone remarked that the blue heron had come back to the copper kettle bridge."),
(0.29,"At dawn the blue heron stood again beneath the copper kettle bridge."),
(0.44,"The children counted ripples while a blue heron waited by the copper kettle bridge."),
(0.59,"A blue heron rose slowly from the reeds by the copper kettle bridge."),
(0.73,"Once more a blue heron was noticed at the copper kettle bridge, quite still."),
(0.97,"Late in the autumn a blue heron was still to be found at the copper kettle bridge.")]
Q="""Below are the full texts of several novels, joined one after another, into which some extra sentences have been inserted. Answer using ONLY the text provided. Do not rely on memory of the novels, and do not use tools, code, or search.

Questions:
1. What is the Thornbury Lending Society's code word at the latest point described in the text, and what was it before?
2. To collect the sealed parcel, which code word would you have to give, and where exactly is the parcel kept?
3. How many silver buttons are in the parcel at the end of all the events described? Show the arithmetic step by step.
4. What was the Pelham Lending Society's code word?
5. What was drawn on the folded map? If the text does not say, answer "not stated".
6. Exactly how many separate sentences mention a blue heron? Give the number.
7. In the order of the text, which comes first: the opening of the sealed parcel, or the change of the Thornbury code word?

Answer in English, numbered 1-7, concisely.

=== TEXT START ===
"""
TRUTH={"1":"larkspur (before: heliotrope)","2":"larkspur; behind the counter of the Harrowgate post office","3":"42-11+4=35","4":"primrose","5":"not stated","6":"7","7":"the opening of the parcel comes first"}
def build(files,tag):
    paras=[]
    for f in files: paras+=body(f).split('\n\n')+["\n\n* * * * *\n\n"]
    ins={}
    for p,s in FACTS+HERONS: ins.setdefault(int(len(paras)*p),[]).append(s)
    out=[]
    for i,p in enumerate(paras):
        out.append(p); out+=ins.get(i,[])
    doc='\n\n'.join(out)
    assert doc.lower().count("blue heron")==7
    open(f"prompts/{tag}.txt","w").write(Q+doc+"\n=== TEXT END ===\n")
    json.dump({"files":files,"truth":TRUTH,"facts":FACTS,"herons":HERONS,"chars":len(doc)},open(f"data/{tag}_truth.json","w"),indent=1)
    print(tag,len(doc))
build(["data/pp.txt","data/g158.txt"],"ultralong_a")
build(["data/pp.txt","data/g158.txt","data/g161.txt","data/g105.txt"],"ultralong_b")
