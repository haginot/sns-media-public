import sys,subprocess,json,time,os,shutil
BASE=os.path.dirname(os.path.abspath(__file__))
tag,which=sys.argv[1],sys.argv[2]
prompt=open(f"{BASE}/prompts/{tag}.txt").read()
wd=f"/tmp/cmp_{which}_{tag}"; shutil.rmtree(wd,ignore_errors=True); os.makedirs(wd)
img=None
if tag=="chart":
    shutil.copy(f"{BASE}/data/chart.png",wd+"/chart.png"); img=wd+"/chart.png"
t=time.time()
if which=="claude":
    tools="Read" if img else ""
    p=prompt+(f"\n\nThe chart image is at: {img}" if img else "")
    cmd=[os.environ.get("CLAUDE_BIN", "claude"),"-p","--model","claude-opus-5-5","--effort","high","--output-format","json","--tools",tools]
    r=subprocess.run(cmd,input=p,capture_output=True,text=True,cwd=wd,timeout=3000)
    dt=time.time()-t
    try:
        d=json.loads(r.stdout); text=d.get("result",""); meta={"models":list(d.get("modelUsage",{}).keys()),"modelUsage":d.get("modelUsage"),"usage":d.get("usage"),"total_cost_usd_equiv":d.get("total_cost_usd"),"num_turns":d.get("num_turns"),"is_error":d.get("is_error")}
    except Exception as e:
        text=r.stdout; meta={"parse_error":str(e),"stderr":r.stderr[-2000:]}
else:
    cmd=["codex","exec","--skip-git-repo-check","-m","gpt-6.2-sol","-c",'model_reasoning_effort="high"',"-s","read-only","--json"]
    if img: cmd+=["-i",img]
    cmd+=["-"]
    r=subprocess.run(cmd,input=prompt,capture_output=True,text=True,cwd=wd,timeout=3000)
    dt=time.time()-t
    open(f"{BASE}/raw/{tag}_codex_events.jsonl","w").write(r.stdout)
    msgs=[];usage=None;cmds=[]
    for line in r.stdout.splitlines():
        try: e=json.loads(line)
        except: continue
        it=e.get("item",{})
        if e.get("type")=="item.completed" and it.get("type")=="agent_message": msgs.append(it["text"])
        if it.get("type")=="command_execution": cmds.append(it.get("command"))
        if e.get("type")=="turn.completed": usage=e.get("usage")
    text=msgs[-1] if msgs else r.stdout[-3000:]
    meta={"models":["gpt-6.2-sol (reasoning high)"],"usage":usage,"tool_commands":sorted(set(map(str,cmds))),"stderr_tail":r.stderr[-800:] if r.returncode else ""}
meta["latency_s"]=round(dt,1); meta["returncode"]=r.returncode
open(f"{BASE}/raw/{tag}_{which}.md","w").write(text)
json.dump(meta,open(f"{BASE}/raw/{tag}_{which}_meta.json","w"),indent=1,ensure_ascii=False)
print(tag,which,meta.get("latency_s"),meta.get("models"),r.returncode)
