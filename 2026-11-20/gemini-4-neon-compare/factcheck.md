# Gemini 4 Neon ファクトチェック（2026-11-19 13:00 JST 確認）

判定: OK（一次ソース＝Google公式ページで確認）

| 項目 | 公式の記載 | 出典 |
|---|---|---|
| 発表日 | Nov 18, 2026（ブログ）。Vertexページ: Launch stage GA, Release date November 18, 2026 | blog.google / docs.cloud.google.com |
| モデルID | `gemini-4-neon` | docs.cloud.google.com, aistudio pricing |
| 価格 | 入力 $3.00/1M、出力（思考トークン含む）$15.00/1M、キャッシュ $0.15/1M。無料枠なし | aistudio.google.com/docs/pricing, blog |
| コンテキスト | 1,048,576 トークン（入力と出力で共有）。1セグメントの出力は最大65,536トークン、long decode で最大 1,048,576−入力 | docs.cloud.google.com |
| 思考レベル | LOW / MEDIUM / HIGH（既定）/ XHIGH。thinking_budget や MINIMAL は400エラー | docs.cloud.google.com |
| サンプリング | temperature/top_p/top_k の指定は無視（temperature 1.0固定） | docs.cloud.google.com |
| 知識カットオフ | March 2026 | docs.cloud.google.com |
| AA Intelligence Index | xhigh で 61、総合3位 | blog |
| Vals Index | 70.9%、2位 | blog, deepmind |
| AA Coding Agent Index | 58.6、1位 | blog, antigravity |
| Terminal-Bench 4.1 | 65.2%（Claude Opus 5.5 65.8%、GPT-6.2 Sol 61.5%） | blog, deepmind |
| FrontierCode 2.0 | 46.2%（high）（Opus 5.5 47.3%、GPT-6.2 Sol 43.8%） | blog, deepmind |
| SWE-sweep | Antigravity 39.0% / mini-SWE 12.8%（Opus 5.5 10.1%/3.6%、GPT-6.2 Sol 8.3%/11.6%） | blog, deepmind |
| AutomationBench | 56.3%（Opus 42.5%、GPT 41.3%） | blog, deepmind |
| Agents' Last Exam v1.1 | 75.8%（Opus 71.6%、GPT 73.0%） | blog, deepmind |
| RiemannBench | 84.0%（Opus 80.0%、GPT 80.0%） | blog, deepmind |
| Terminal-Bench Science | 70.5%（Opus 63.3%、GPT 68.0%） | blog, deepmind |
| HLE-Diamond | 71.3%（Opus 67.9%、GPT 64.0%） | blog, deepmind |
| Chartography | 73.5%（Opus 66.3%、GPT-6.2 Sol 75.1% ← GPTが上） | blog, deepmind |
| GraphWalks 256k–1M BFS F1 | 95.2%（Opus 66.8%、GPT 80.1%） | deepmind |
| CursorBench 4.1 | 65.4%（Opus 58.1%） | deepmind |
| Agent Arena Index | 1336、2位 | blog |
| Vending-Bench 2 | $16,843、1位 | blog |
| コスト | high で Carbon より1タスクあたり32%安い | blog, antigravity |

注意: 上記ベンチマークは Google 自身の発表値。比較相手の数値も Google 掲載のもの（第三者の再現ではない）。

出典URL
- https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-4-neon/
- https://aistudio.google.com/docs/pricing
- https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/4-neon
- https://deepmind.google/models/gemini/
- https://antigravity.google/blog/gemini-4-neon-in-google-antigravity/
