import itertools
names=["Aoi","Ben","Chika","Daiki","Emi"]; langs=["Python","Rust","Go","Java","Swift"]
sols=[]
for ps in itertools.permutations(names):
  slot={n:i+1 for i,n in enumerate(ps)}
  for ls in itertools.permutations(langs):
    L={ps[i]:ls[i] for i in range(5)}; who={ls[i]:ps[i] for i in range(5)}
    s=lambda lang: slot[who[lang]]
    if slot["Aoi"]+1!=s("Python"): continue
    if slot["Ben"] in (1,5) or L["Ben"] in ("Python","Go"): continue
    if not (s("Go")<s("Swift") and s("Go")<s("Java")): continue
    if not slot["Chika"]>slot["Ben"]: continue
    if abs(slot["Emi"]-slot["Chika"])!=2: continue
    if slot["Daiki"]%2==0: continue
    if abs(s("Rust")-s("Swift"))==1: continue
    if s("Swift")%2==1: continue
    if s("Java")!=s("Python")+1: continue
    sols.append((ps,ls))
print(len(sols)); [print(x) for x in sols]
