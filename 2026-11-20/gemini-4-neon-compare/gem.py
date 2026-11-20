import os,sys,json,time,base64,urllib.request,urllib.error
# Gemini 4 Neon runner (streaming SSE). The API key is read from file and never printed.
KEY=os.environ["GEMINI_API_KEY"]
URL="https://generativelanguage.googleapis.com/v1beta/models/gemini-4-neon:streamGenerateContent?alt=sse"
def call(prompt, level="HIGH", image=None, tag="test"):
    parts=[]
    if image:
        parts.append({"inline_data":{"mime_type":"image/png","data":base64.b64encode(open(image,'rb').read()).decode()}})
    parts.append({"text":prompt})
    body={"contents":[{"role":"user","parts":parts}],
          "generationConfig":{"thinkingConfig":{"thinkingLevel":level}}}
    req=urllib.request.Request(URL,data=json.dumps(body).encode(),
        headers={"Content-Type":"application/json","x-goog-api-key":KEY})
    t=time.time(); ttft=None; text=[]; usage={}; model=None; finish=None
    try:
        with urllib.request.urlopen(req,timeout=1200) as resp:
            for raw in resp:
                line=raw.decode().strip()
                if not line.startswith("data:"): continue
                ev=json.loads(line[5:])
                usage=ev.get("usageMetadata",usage); model=ev.get("modelVersion",model)
                for c in ev.get("candidates",[]):
                    finish=c.get("finishReason",finish)
                    for p in c.get("content",{}).get("parts",[]):
                        if p.get("text") and not p.get("thought"):
                            if ttft is None: ttft=time.time()-t
                            text.append(p["text"])
    except urllib.error.HTTPError as e:
        msg=e.read().decode()[:2000]
        json.dump({"status":e.code,"error":msg},open(f"raw/{tag}_gemini_error.json","w"),indent=1)
        print("HTTP",e.code,msg[:500]); sys.exit(2)
    dt=time.time()-t
    inp=usage.get("promptTokenCount",0); cached=usage.get("cachedContentTokenCount",0)
    out=usage.get("candidatesTokenCount",0)+usage.get("thoughtsTokenCount",0)
    cost=(inp-cached)*3e-6+cached*0.15e-6+out*15e-6   # $3 / $0.15 cached / $15 per 1M
    meta={"model":model,"level":level,"latency_s":round(dt,1),"time_to_first_text_s":round(ttft or 0,1),
          "finishReason":finish,"usage":usage,"cost_usd":round(cost,4),"transport":"streamGenerateContent SSE"}
    open(f"raw/{tag}_gemini.md","w").write("".join(text))
    json.dump(meta,open(f"raw/{tag}_gemini_meta.json","w"),indent=1)
    print(json.dumps(meta)); return text
if __name__=="__main__":
    tag=sys.argv[1]; level=sys.argv[2] if len(sys.argv)>2 else "HIGH"
    img=sys.argv[3] if len(sys.argv)>3 else None
    call(open(f"prompts/{tag}.txt").read(),level,img,tag)
