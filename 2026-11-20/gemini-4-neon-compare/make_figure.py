import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
import json
for p in ["/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc","/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"]:
    fm.fontManager.addfont(p)
plt.rcParams["font.family"]="Noto Sans CJK JP"
C={"gemini":"#E8730C","claude":"#2B6CB0","codex":"#7A7A7A"}
N={"gemini":"Gemini 4 Neon","claude":"Claude Opus 5.5","codex":"GPT-6.2 Sol"}
tasks=[("html_app","① 1枚のHTMLでゲームを作る"),("reasoning","② 答えが決まる数学・論理パズル"),("chart","③ グラフ画像の読み取り"),
       ("japanese","④ 日本語の説明文（500字）"),("longctx","⑤ 小説1冊（17万トークン）から探す"),("graphwalk","⑥ 8万トークンの経路たどり"),
       ("ultralong_a","⑦ 小説2冊（39万トークン）から探す"),("ultralong_b","⑧ 小説4冊（65万トークン）から探す")]
# result text per task/model (verified by hand; see results.md)
res={"html_app":{"gemini":"動く","claude":"動く","codex":"動く"},
     "reasoning":{"gemini":"3/3","claude":"3/3","codex":"3/3"},
     "chart":{"gemini":"5/5","claude":"5/5","codex":"5/5"},
     "japanese":{"gemini":"3位","claude":"2位","codex":"1位"},
     "longctx":{"gemini":"6/6","claude":"6/6","codex":"6/6"},
     "graphwalk":{"gemini":"18/18","claude":"18/18","codex":"18/18"},
     "ultralong_a":{"gemini":"7/7","claude":"7/7","codex":"入力不可"},
     "ultralong_b":{"gemini":"7/7","claude":"7/7","codex":"入力不可"}}
rows=json.load(open("data/run_table.json"))
lat={(r[0],r[1]):(r[2] if r[2]!="n/a" else None) for r in rows}
fig=plt.figure(figsize=(20,11.25),dpi=100); fig.patch.set_facecolor("white")
fig.text(0.04,0.925,"同じ8つの課題を、3つのAIに解かせた結果",fontsize=50,weight="bold",color="#1a1a1a")
fig.text(0.04,0.872,"正解数は同じ。差が出たのは時間、日本語の書き方、読める長さ",fontsize=27,color="#333")
# left: result table
ax=fig.add_axes([0.04,0.12,0.47,0.70]); ax.axis("off"); ax.set_xlim(0,10); ax.set_ylim(0,9.2)
for j,m in enumerate(["gemini","claude","codex"]):
    ax.text(6.3+j*1.35,8.8,N[m].replace(" ","\n",1),ha="center",va="center",fontsize=17,weight="bold",color=C[m],linespacing=1.1)
for i,(t,label) in enumerate(tasks):
    y=8.0-i*1.0
    ax.text(0,y,label,va="center",fontsize=20,color="#1a1a1a")
    for j,m in enumerate(["gemini","claude","codex"]):
        v=res[t][m]; x=6.3+j*1.35
        col="#BBBBBB" if v in ("未実施","入力不可") else C[m]
        ax.add_patch(plt.Rectangle((x-0.6,y-0.36),1.2,0.72,color=col,alpha=0.14 if v not in ("未実施","入力不可") else 0.25,lw=0))
        ax.text(x,y,v,ha="center",va="center",fontsize=20,weight="bold",color="#666" if v in ("未実施","入力不可") else C[m])
    ax.plot([0,10],[y-0.5,y-0.5],color="#E3E3E3",lw=1)
fig.text(0.04,0.085,"②③⑤〜⑧は筆者が用意した正解と照合。④は書き手を伏せて3つのAIが採点した平均順位（3者とも GPT を1位にした）。⑦⑧の GPT は Codex CLI が100万文字を超える入力を受け付けず実行できず。",fontsize=14,color="#555")
# right: latency
ax2=fig.add_axes([0.58,0.17,0.39,0.59])
import numpy as np
y=np.arange(len(tasks))[::-1]; h=0.26
for j,m in enumerate(["gemini","claude","codex"]):
    vals=[lat.get((t,m)) for t,_ in tasks]
    for k,v in enumerate(vals):
        yy=y[k]+(1-j)*h
        if v is None:
            ax2.text(5,yy,"入力不可",va="center",fontsize=14,color="#888"); continue
        ax2.barh(yy,v,height=h*0.92,color=C[m])
        ax2.text(v+5,yy,f"{v:.0f}秒",va="center",fontsize=14,color=C[m])
ax2.set_yticks(y); ax2.set_yticklabels([l.split(" ")[0] for _,l in tasks],fontsize=22)
ax2.set_xlim(0,480); ax2.tick_params(axis="x",labelsize=14)
for s in ["top","right"]: ax2.spines[s].set_visible(False)
ax2.set_xlabel("秒",fontsize=16)
fig.text(0.58,0.825,"答えが返るまでの時間",fontsize=27,weight="bold",color="#1a1a1a")
for j,m in enumerate(["gemini","claude","codex"]):
    fig.text(0.60+j*0.11,0.785,"■ "+N[m].split(" ")[0] if m!="codex" else "■ GPT",fontsize=17,color=C[m])
fig.text(0.04,0.04,"各1回だけの実測（2026年11月19日）。トークン数は Gemini の数え方。Gemini は API を直接、Claude は Claude Code、GPT は Codex CLI から実行（どれも思考の深さは「高」）。CLI の起動時間を含む。",fontsize=14,color="#555")
fig.savefig("figure_compare.png"); print("ok")
