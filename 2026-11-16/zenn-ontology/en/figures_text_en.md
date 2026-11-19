# English text for the ontology article figures (fig1–fig7)

For the illustrator making English versions of the figures in the Canly Tech Blog ontology article.

- Article (Japanese): https://zenn.dev/canly/articles/121db874319244
- English article draft: `article_en.md` in this folder
- How the text was collected: I opened each published PNG (2000×1125) and read off every visible Japanese string. I then checked them against the figure source HTML (`figkit/zfig1.html`–`zfig7.html` in the working folder). The published PNGs are byte-identical to the working copies in `images/fig1.png`–`fig7.png`.
- Strings that are already English or code (e.g. `RDF`, `features rdfs:range Person`, `propose_rebooking`, `schema.yaml`) are listed only where they sit next to Japanese text. Keep them unchanged.
- Colored or emphasized words in titles are marked **bold**. Keep the same kind of emphasis in English.
- English strings run longer than Japanese. The suggested wording is the full meaning; shorter alternatives are given where space is tight.
- ⚠ marks a point to check.

---

## Figure 1: what each side calls "ontology"

Current image: https://raw.githubusercontent.com/haginot/sns-media-public/4d36a02ce4b2679f8f54415b8f9b4e7468e68f2c/2026-11-16/zenn-ontology/v1/fig1.png
Caption in article (EN): Figure 1: The difference in scope between what general ontology and Foundry Ontology call "ontology"

| Japanese (as shown) | English |
|---|---|
| 「オントロジー」と呼ぶ範囲 (title; 「オントロジー」 highlighted) | What counts as **"ontology"** |
| 一般的なオントロジー（W3C の標準） | Ontology in general (W3C standards) |
| `RDF` `OWL` `SHACL` `SPARQL` (tags) | (unchanged) |
| 型の層：<br>クラス・プロパティ・制約 | Type layer:<br>classes, properties, constraints |
| 実データ（ナレッジグラフ） | Actual data (knowledge graph) |
| 含むことも、型と制約だけのこともある | May be included, or it may be types and constraints only |
| 権限・業務システムへの書き込みは、標準の対象外 | Permissions and writes to business systems are outside the standards' scope |
| ここは同じ層 (label on the dotted line between the two type layers) | Same layer |
| Foundry Ontology（Palantir） | Foundry Ontology (Palantir) (already English; change only the full-width parentheses) |
| 動かす部品：<br>アクション・関数・権限 | Components that make things happen:<br>actions, functions, permissions |
| 中身：<br>オブジェクトとリンク | Contents:<br>objects and links |
| 型：<br>オブジェクトタイプ・<br>リンクタイプ・プロパティ | Types:<br>object types,<br>link types, properties |
| Foundry が「オントロジー」と呼ぶ範囲 (label under the purple box) | What Foundry calls "ontology" |
| 優劣ではなく、どこまでを同じ名前で呼ぶかの違い (footer) | Not better or worse: a difference in how much gets called by the same name |

Notes: "動かす部品" is rendered as "components that make things happen", the same wording the English article uses. If space is tight, use "Moving parts:" or "Kinetic layer:".

---

## Figure 2: inference and validation do different jobs

Current image: https://raw.githubusercontent.com/haginot/sns-media-public/4d36a02ce4b2679f8f54415b8f9b4e7468e68f2c/2026-11-16/zenn-ontology/v1/fig2.png
Caption in article (EN): Figure 2: The same range declaration works as inference in OWL / RDFS and as validation in SHACL

| Japanese (as shown) | English |
|---|---|
| 推論と検証は、別の働き (title; 推論 and 検証 highlighted) | **Inference** and **validation** do different jobs |
| （番組） (under each `ep001` / `ep002` node; appears 6×) | (episode) |
| `ep001` `ep002` `guest001` `features` | (unchanged) |
| `features rdfs:range Person` / `sh:class Person / sh:minCount 1` (code boxes) | (unchanged) |
| 推論なし (left panel heading) | Without inference |
| RDFS 推論あり (right panel heading) | With RDFS inference |
| Person と書かれていない →<br>クラスの検査で違反 | Not stated as a Person →<br>fails the class check |
| 出演者が0人 →<br>minCount で違反 (appears in both panels) | Zero guests →<br>fails minCount |
| Person と推論 (highlighted, right panel) | Inferred as a Person |
| range から Person と推論 →<br>違反が消える | Person inferred from range →<br>the violation goes away |
| OWL は「書かれていない事実」を偽とは扱わない（開世界仮定）。必須の検査は SHACL で書く (footer) | OWL doesn't treat "facts that aren't stated" as false (open-world assumption). Write required checks in SHACL |
| 説明用の例（pySHACL 0.40.2 で実行） (bottom-right note) | Illustrative example (run with pySHACL 0.40.2) |

Notes: 番組 here means a show episode. In the article's example the class is `ex:Episode`, so "(episode)" matches the code. 出演者 = the person featured; the article uses "guest".

---

## Figure 3: types and instances are different layers

Current image: https://raw.githubusercontent.com/haginot/sns-media-public/4d36a02ce4b2679f8f54415b8f9b4e7468e68f2c/2026-11-16/zenn-ontology/v1/fig3.png
Caption in article (EN): Figure 3: Object types, link types, and properties (the type layer), and objects and links (the instance layer)

| Japanese (as shown) | English |
|---|---|
| 型とインスタンスは、層が違う (title; 層が違う highlighted) | Types and instances are **different layers** |
| 型の層<br>（オブジェクトタイプ・<br>リンクタイプ・プロパティ） | Type layer<br>(object types,<br>link types, properties) |
| `Theme` / テーマ | Theme (drop the Japanese second line) |
| `Episode` / 番組 | Episode (drop the Japanese second line) |
| `Person` / 人物 | Person (drop the Japanese second line) |
| `ABOUT` / 扱う (link label) | ABOUT / covers |
| `FEATURES` / 出演している (link label) | FEATURES / features |
| `publishedAt` 公開日 | publishedAt (publish date) |
| `durationSeconds` 尺 | durationSeconds (length) |
| 一般的なオントロジーの<br>「クラスとプロパティ」に近い (right note, upper) | Close to "classes and properties"<br>in ontology in general |
| インスタンス (label on vertical dotted lines) | instances |
| インスタンスの層<br>（オブジェクトとリンク） | Instance layer<br>(objects and links) |
| テーマ：AI | Theme: AI |
| 番組A / 番組B | Episode A / Episode B |
| 人物X / 人物Y | Person X / Person Y |
| 知識グラフ／オブジェクトグラフと<br>呼ばれるのは、主にこの層 (right note, lower) | What's called a knowledge graph / object graph<br>is mainly this layer |
| 番組・人物は架空データ (bottom-right note) | Episodes and people are fictional data |

Notes: In the type layer, each node has an English identifier above its Japanese name, so the English version only needs the identifier. ⚠ The source HTML lists 「テーマ：AI」 twice, but only one instance-layer node is labeled テーマ：AI in the rendered PNG. Follow the PNG.

---

## Figure 4: an action defines how things are changed

Current image: https://raw.githubusercontent.com/haginot/sns-media-public/4d36a02ce4b2679f8f54415b8f9b4e7468e68f2c/2026-11-16/zenn-ontology/v1/fig4.png
Caption in article (EN): Figure 4: The flow of an action: parameters → submission criteria → rules → writeback and side effects → action log

| Japanese (as shown) | English |
|---|---|
| アクションは「動かし方」の定義 (title; 「動かし方」 highlighted) | An action defines **how things get changed** |
| 筆者の見方：この縛り全体を「ハーネス」と呼んでいます<br>（Palantir の用語ではありません） (top-left, inside dashed frame) | The author's view: I call this whole set of constraints a "harness"<br>(not a Palantir term) |
| ① パラメータ<br>入力の型 | ① Parameters<br>Input types |
| ② 実行条件（submission criteria）<br>誰が・どの状態なら。すべて満たすときだけ送信できる | ② Submission criteria<br>Who, and in what state. Can be submitted only when all are met |
| ③ ルール<br>オブジェクトとリンクの作成・変更・削除／関数ルール | ③ Rules<br>Create, modify, delete objects and links / function rules |
| ④ 単一のトランザクションで反映 | ④ Applied in a single transaction |
| ⑤ 書き戻しと副作用<br>writeback dataset・業務システム／通知・Webhook | ⑤ Writeback and side effects<br>Writeback dataset, business systems / notifications, webhooks |
| ⑥ アクションログ<br>成功した送信だけを記録 | ⑥ Action log<br>Records successful submissions only |
| 権限：ロール／オブジェクトとプロパティのポリシー（セル単位） (slanted text along the base) | Permissions: roles / object and property policies (cell-level) |
| 満たさない → 送信できない<br>（失敗はアクションメトリクスで追う） | Not met → cannot submit<br>(failures are tracked in action metrics) |
| 例：便の機材を変える — 運航管理者のグループに属し、かつ機材が運用中のときだけ (bottom bar) | Example: change a flight's aircraft — only if the user is in the flight controllers group and the aircraft is in service |

Notes: ⚠ The figure has six steps, including "④ Applied in a single transaction", but the article caption lists five (no transaction step). This is the same in the Japanese original. I left the caption as it is rather than change content. In ②, drop the Japanese 実行条件 and keep the official English term "Submission criteria".

---

## Figure 5: what's in the research repository pivot-ontology

Current image: https://raw.githubusercontent.com/haginot/sns-media-public/013e400fbce7fc68d54ea361eccbdefd3549db4d/2026-11-16/zenn-ontology/figures_fix/fig5.png
Caption in article (EN): Figure 5: Structure of the research repository: collecting public data → schema → graph and aggregation → demos (fictional data) → verification

| Japanese (as shown) | English |
|---|---|
| 調査リポジトリ pivot-ontology の中身 (title; `pivot-ontology` highlighted) | Inside the research repository **pivot-ontology** |
| ① 収集<br>PIVOT 公式 YouTube の<br>公開データ | ① Collect<br>Public data from PIVOT's<br>official YouTube channel |
| ② 正規化<br>Episode／MetricsSnapshot | ② Normalize<br>Episode / MetricsSnapshot |
| ③ 抽出<br>規則／LLM | ③ Extract<br>Rules / LLM |
| ④ スキーマ<br>schema.yaml<br>（来歴：public・owner・<br>derived・computed・external） | ④ Schema<br>schema.yaml<br>(provenance: public, owner,<br>derived, computed, external) |
| ⑤ グラフと集計<br>集計の対象は「全数取得<br>かつ 公開30日以上」の212本 | ⑤ Graph and aggregates<br>Aggregates cover the 212 episodes that are<br>"fully collected AND public for 30+ days" |
| 架空データのシミュレーション (label above the demo area) | Simulation on fictional data |
| デモ1 / デモ2 / デモ3 | Demo 1 / Demo 2 / Demo 3 |
| `operational-ontology-demo`<br>4つの業務をまたぐ操作。<br>取消と返品を別のアクションに | `operational-ontology-demo`<br>Operations spanning four business systems.<br>Cancel and return as separate actions |
| `pivot-live-studio`<br>実際の Codex エージェント＋人の承認 | `pivot-live-studio`<br>A real Codex agent + human approval |
| `pivot-team-agent-demo`<br>番組で使ったデモ。台本どおりに動く | `pivot-team-agent-demo`<br>The demo used on the show. Runs to a script |
| `pivot-ontology-basis`<br>検証用。A プレーンテキスト／<br>B 用語集／C オントロジー／<br>Z 知識なし<br>（未公開・未査読） | `pivot-ontology-basis`<br>For verification. A plain text /<br>B glossary / C ontology /<br>Z no knowledge<br>(unpublished, not peer-reviewed) |
| Legend: 公開データ / 合成データ / 評価データ | Legend: Public data / Synthetic data / Evaluation data |

Notes: 4つの業務 is the four business systems (sales, warehouse, accounting, support), matching "four mock systems" in the article.

---

## Figure 6: AI proposes, humans approve

Current image: https://raw.githubusercontent.com/haginot/sns-media-public/56a3a54f85dd5340aa193851a480407be4f75a8b/2026-11-16/zenn-ontology/figures_fix/fig6.png
Caption in article (EN): Figure 6: Where the LLM agent sits: it reads the ontology, proposes changes, and nothing is finalized until those changes pass human approval and the submission criteria

| Japanese (as shown) | English |
|---|---|
| 提案はAI、承認は人 (title; 承認は人 highlighted) | AI proposes, **humans approve** |
| LLM エージェント<br>（Codex） | LLM agent<br>(Codex) |
| `ontology_schema` `search_objects` `traverse_graph` `get_object` (vertical tool labels) | (unchanged) |
| オントロジー<br>（型・関係・アクションの定義） | Ontology<br>(definitions of types, relationships, actions) |
| 前提が変わった →<br>確定できない →<br>案を作り直す (label on the dotted loop) | Premises changed →<br>can't commit →<br>redo the plan |
| 変更案（提案） — `propose_rebooking` | Change plan (proposal) — `propose_rebooking` |
| 人の承認 — `approve_plan`<br>制作責任者だけ。エージェントのツールにはない | Human approval — `approve_plan`<br>Production lead only. Not among the agent's tools |
| 実行前の検査 — `check_plan`<br>承認時の前提（バージョン）が変わっていないか | Pre-execution check — `check_plan`<br>Have the premises (versions) changed since approval? |
| 確定 — `commit_rebooking`<br>1つのトランザクションで反映 | Commit — `commit_rebooking`<br>Applied in one transaction |
| 監査の記録<br>成功も拒否も残す | Audit record<br>Keeps both successes and refusals |
| 実行してよい条件と承認の主体は、プロンプトではなくサーバー側の定義で縛る (footer) | Conditions for execution and who approves are bound by server-side definitions, not by the prompt |
| 架空データ。Palantir の製品は使っていません (bottom-right note) | Fictional data. No Palantir products are used |

Notes: ⚠ The figure's step order (proposal → human approval → pre-execution check `check_plan` → commit) is a simplification. In the article's sequence diagram, `check_plan` is called by the AI *before* approval, and the re-check happens inside `commit_rebooking`. This is the same in the Japanese original and is not a translation issue, but the illustrator may want to keep the order exactly as drawn rather than "fixing" it without HAGINO's OK.

---

## Figure 7: what helps first is providing knowledge

Current image: https://raw.githubusercontent.com/haginot/sns-media-public/a1e890a7fc7c08c3cea31dba184b4f173a2d1bf2/2026-11-16/zenn-ontology/figures_fix/fig7.png
Caption in article (EN): Figure 7: The difference in size between the effect of providing knowledge and the effect of writing that knowledge in ontology form

| Japanese (as shown) | English |
|---|---|
| 効くのは、まず知識を渡すこと (title; 知識を渡すこと highlighted) | What helps first is **providing knowledge** |
| 知識を渡すかどうか (bar 1 label) | Whether knowledge is provided |
| +25.7〜+49.3 (bar 1 value) | +25.7 to +49.3 |
| 同じ知識をオントロジー形式で<br>（高難度・主な集計） (bar 2 label) | Same knowledge in ontology form<br>(high difficulty, main analysis) |
| +2.3（有意） (bar 2 value) | +2.3 (significant) |
| 同（慎重な再集計） (bar 3 label) | Same (conservative re-analysis) |
| 約+2.0（補正後は有意でない） (bar 3 value) | ≈ +2.0 (not significant after correction) |
| 手順を扱う業務（実験II） (bar 4 label) | Procedural work (Experiment II) |
| −0.5（有意差なし） (bar 4 value) | −0.5 (no significant difference) |
| ポイント（知識なし、またはプレーンテキストとの差） (x-axis title) | Points (difference vs. no knowledge, or vs. plain text) |
| 未公開・未査読。一つの架空の業務での結果。解析対象 2,117 回の実行 (footer) | Unpublished, not peer-reviewed. Results from a single fictional business. Analysis covers 2,117 runs |

Notes: ⚠ The −0.5 for Experiment II appears only in the figure. The article text says only that the form made no difference, with no number. Keep −0.5 as drawn. Bar 2's "(significant)" refers to the main analysis (p=0.0027). The English article keeps that qualifier in the text. Keep "(significant)" short in the figure, as in the original.
