# PIVOTで話した「オントロジー」と、話しきれなかったこと

<!-- Source: https://note.com/haginota/n/nbf04863132cf (live published text, fetched via note API v3 on 2026-11-19 JST; publish_at 2026-11-16T17:28:10.000+09:00) -->

萩野貴拓です。2026年11月14日、[ビジネス動画メディアのPIVOT](https://pivotmedia.co.jp/movie/15261)に[3回目の出演](https://www.youtube.com/watch?v=_V7IF1XdNLQ)が公開されました。テーマは、企業はAIでどこまで自動化できるのか、そしてそのときに出てくる「オントロジー」とは何か、です。

前回の出演では、MetaのパーソナルAIエージェント「Muse」についてお話しし、[番組で話しきれなかったこと](https://note.com/haginota/n/nba922eb92cd9)をnoteにまとめました。今回も、同じように書きたいと思います。

[https://note.com/haginota/n/nba922eb92cd9](https://note.com/haginota/n/nba922eb92cd9)
<!-- embed: note -->

公開後のコメントは、水準が高く、正直なところ、私自身もすぐには答えきれない指摘がありました。たとえ話のままにしてしまったところや、言葉を簡単にしすぎたところもあります。この記事では、番組で話したことをまず整理します。そのうえで、一般的な意味のオントロジーと、[Palantir の Foundry Ontology](https://www.palantir.com/docs/jp/foundry/platform-overview/overview) が何を指すかを分けて書き、コメントで多かった問いを、事実と私の考えを分けて補います。

先にお断りしておきます。

- この記事は私個人の見解です。PIVOT、Palantir、所属組織の公式な見解ではなく、提携やタイアップの記事でもありません。
- 番組内の私の発言は、要約して書いています。正確な言い回しは本編でご確認ください（時刻は目安です）。
- 事実と数字には出典を付けています。私の推測や意見は、「と考えています」「見立てです」と書き分けています。資料は2026年11月16日（日本時間）に確認しました。
- 書き起こしには自動字幕を使っています。固有名詞の誤りは直していますが、音声での最終確認が残っている箇所には、草稿用の印を付けています。

本編はこちらです。

[https://www.youtube.com/watch?v=_V7IF1XdNLQ](https://www.youtube.com/watch?v=_V7IF1XdNLQ)
<!-- embed: youtube -->

[https://pivotmedia.co.jp/movie/15261](https://pivotmedia.co.jp/movie/15261)

![](https://assets.st-note.com/img/1794814510-rRdEwAGjbyWFkHcz1S73OsQ9.jpg)
<!-- figure: F1 -->

▲ キービジュアル。「意味の設計図」「単なるデータではない」。土台のオ  
ントロジーの上に、セマンティック要素（点と線）とキネティック要素（承認と書き戻し）

---

## 1. 番組で話したこと

番組では、おおよそ次のことをお話ししました。いずれも要約です。

### オントロジーは新語ではない

オントロジーは、ここ数ヶ月で突然出てきた言葉ではありません。AIが扱う言葉の意味を、人間と同じように伝える方法として、以前から注目されてきた技術です。いま再び取り上げられているのは、AIエージェントを、企業が正確かつ安全に動かそうとする流れがあるからだ、とお話ししました（03:00ごろ、04:07ごろ）。

その背景にある大きな変化として、確認できている事実だけを書いておきます。[GPT-3 の論文](https://arxiv.org/abs/2005.14165)は2020年です。[ChatGPT の公開](https://openai.com/index/chatgpt/)は2022年11月30日、[GPT-4 の発表](https://openai.com/index/gpt-4-research/)は2023年3月14日です。番組の16:10ごろに私が触れた大きな変化は、ChatGPT が公開された時期のことです。

私自身の背景としても、ビズリーチで約10年、職務経歴書と求人票のテキストを扱ってきました。キーワードの照合だけでは、言葉の裏側にある意図までは読めません。自然文のままでは、コンピューターに意味を渡しきれない、という問題は以前からありました。

### 個人のエージェントと、企業のエージェントは条件が違う

[1回目の出演](https://www.youtube.com/watch?v=PeZHAztFgqc)（OpenClaw回、2026年5月19日）でもお話しし、[今回の番組](https://www.youtube.com/watch?v=_V7IF1XdNLQ)（06:00ごろ）でも触れましたとおり、私は消費者として、個人向けのエージェント（OpenClaw）に、買い物や予約、日々の生活の一部を任せています。個人なら、誤った購入や意図しない予約があっても、「後で取り消す」「連絡する」で済ませられる場合もあります。

企業では、それが許されません。申し込んでいない発注や、個人情報の漏えいは、信用の問題になります。関係者もシステムも多いので、仕組みはより複雑になります。そこにオントロジーが必要になる、というのが番組での整理です。

導入の進み具合について、番組では「昨年末時点で3%」という話が出ました（05:00ごろ）。後から一次資料を当たると、この数字に近い調査はあります。[矢野経済研究所](https://www.yano.co.jp/press-release/show/press_id/3991)が2025年12月19日に発表したプレスリリースでは、生成AIを活用していると答えた215社のうち、AIエージェントを「利用中」と答えたのは3.3%でした。**全企業の3%ではありません。** 母数は、すでに生成AIを使っている企業です。番組では「増えても1割に満たない」という見立てにも話が及んでいますが、その部分の出典は確認できていません。ここでは、出典のある3.3%の範囲だけを書いておきます。

### オントロジーは「意味の設計図」

番組でお伝えした核は、次の定義です（07:12ごろ）。

人間とAIが、同じ現実世界の情報を意味として共有するための設計図。意味の設計図。

具体的には、現実の概念をオブジェクト（点）として定義し、概念同士を関係（線）で結びます。1回目の出演（OpenClaw回）を例にすると、「萩野貴拓」という人物が、「OpenClawのデモ解説」という番組に「出演する」で結ばれると、出演者という位置づけが見えてきます。番組が「AI」というテーマを「扱う」で結ばれると、番組テーマになります。

この「主語・述語・目的語」に近い3つの組を、トリプレットと呼ぶこともあります。情報技術の標準では、[RDFの「トリプル」](https://www.w3.org/TR/rdf11-concepts/)がこれに相当します。一方、後述する [Palantir の公式用語](https://www.palantir.com/docs/jp/foundry/ontology/core-concepts)は、トリプルではなく、オブジェクト、リンク、プロパティです。

オブジェクトには属性があります。番組なら、放映日や視聴者数などです。属性まで定義していくと、私たちが見ている現実が、データ構造の側にも写っていきます。その意味で、オントロジーはデジタルツインと呼ばれることもある、とお話ししました。[Palantir のドキュメント](https://www.palantir.com/docs/jp/foundry/ontology/core-concepts)にも、[「組織のデジタルツイン」](https://www.palantir.com/docs/jp/foundry/ontology/overview)という説明があります。

![](https://assets.st-note.com/img/1794814510-5hg4FD2MXa801qYcGIxOCSBK.jpg)
<!-- figure: F2 -->

▲ トリプレットの例。人物「萩野貴拓」—出演する→ 番組「OpenClawのデモ解説」—扱う→ テーマ「AI」。プロパティは放映日・視聴者数

多義語の例として、「Python」を挙げました。プログラミングの話なら言語、爬虫類の話なら蛇です。その場で言葉がどの意味を持ち、概念同士がどう関係するかを書いておくことが、オントロジーの役割です。ただ、この例だけで「いまもオントロジーが要る」とは言い切れない、というコメントをいただいています。その点は、3-3節で補います。

### 設計図と、実データのグラフは、層が違う

点（概念）と線（関係）を結んでできたものを、グラフと呼びます。場合によって、ナレッジグラフ（知識グラフ）とも呼ばれます。

ここで、番組で私が強く言いたかった切り分けがあります。**設計図の層と、実データのグラフの層は違います。** 設計図（何の種類があり、どんな関係がありうるか）に沿って、実際の人物や番組のグラフを作っていきます。

番組では「オントロジー自体はグラフではない」とも言いました（15:02ごろ）。方向は同じですが、この記事では少し正確に言い直します。[W3C の OWL](https://www.w3.org/TR/owl2-mapping-to-rdf/) では、オントロジーそのものを RDF グラフとして書き表すこともできます。ですから、「グラフではない」と断定するより、「型の定義と、それに沿って作る実データのグラフは、層が違う」とした方がよい、と考えています。

ひとつ、番組では言いそびれたことがあります。Palantir の Foundry では、「オントロジー」という語が、この設計図に加えて、実データのグラフと、それを動かす部品までをまとめて指します。層が違うことと、どこまでを一つの名前で呼ぶかは、別の話です。この違いは、2章で書き分けます。

![](https://assets.st-note.com/img/1794814510-AwIRMbJPHfEad2hySGkOin5q.jpg)
<!-- figure: F3 -->

▲ 左はオントロジー（タイプ・関係・制約＝意味の設計図）。右はそれに基づくインスタンスのグラフ（ナレッジグラフとも呼ぶ）。両方と「動かす部品」（アクション・関数・セキュリティ）を外側の囲み線で「Foundry がまとめて『オントロジー』と呼ぶ範囲」と示す。結論は「設計図とグラフは層が違う」。注記「関数のグラフとは別の意味」

14:47ごろの「グラフ」という言葉の使い方については、視聴者の指摘を受けて、3-1節で書き分けます。

### Excelでも表せる。ただし、行動の制御までは保証できない

極論すれば、グラフの形をわざわざ作らなくても、Excel でオントロジーを表すことはできます。Palantir 自身も、オブジェクトタイプをデータセット、オブジェクトを行、[プロパティを列に対応づけて説明](https://www.palantir.com/docs/jp/foundry/ontology/core-concepts)しています。

ただし、意味付けだけを表にしても、経費精算のように、社内規定や決裁のルールを踏まえた判断を、AIが毎回「確認する」のではなく、仕組みとして制御できる保証はありません。番組ではこれをバリデーションと呼びました。Palantir の公式用語では、[アクション](https://www.palantir.com/docs/jp/foundry/action-types/overview)を実行してよいかを決める[「実行条件」](https://www.palantir.com/docs/jp/foundry/action-types/submission-criteria)（英語では Submission criteria。旧称は検証、validations）に当たります。

ひとつ注釈があります。Excel にも[「データの入力規則」](https://support.microsoft.com/en-us/office/apply-data-validation-to-cells-29fecbcc-d1b9-42c1-9d76-eff3ce5f7249)があり、セルに入る値の検証はできます。保証しにくいのは、**誰が、どの条件で、外部のシステムに何をしてよいか**（権限、トランザクション、副作用の制御）の側です。「Excelでは検証が一切できない」とは言いません。

この比喩として、番組では「AIの記憶」より「契約書」に近い、ともお話ししました。記憶は曖昧になりやすく、契約書は、書かれたことが正として進む、という対比です。これは私自身のたとえです。Palantir の製品ドキュメントは、「契約」という語では説明していません。ただ、[Palantir の公式ブログ](https://blog.palantir.com/ontology-finding-meaning-in-data-palantir-rfx-blog-series-1-399bd1a5971b)には、オントロジーが表す「一元化された契約（the centralized contract the ontology represents）」という表現があります。オブジェクトに結びついたロジックも変更できる形にしておけば、アプリケーションがその契約を使いやすくなる、という文脈です。製品ドキュメントの言葉に寄せるなら、権限と実行条件、そして変更の監査、に近いと考えています。

![](https://assets.st-note.com/img/1794814510-dkJgAxLiVKBtqQwnj2P80D5R.jpg)
<!-- figure: F7 -->

▲ 「記憶」より「契約書」に近い、という番組でのたとえ。記憶は曖昧になりやすい。契約書・内部規定は書かれたことが正。一定額以上は部長決裁、さらに上は取締役会決議

### 業務を構造化する専門職と、予期せぬ問題

どこまで概念を分け、どこまで分けないかの線引きは、人間が決める必要があります。そうした仕事を担う専門職として、番組では FDE を紹介しました。いまの FDE の仕事の中核のひとつに、現場の業務を構造化してオントロジーの形に直すことがある、という整理です。

一方、「Palantir はオントロジーが競争力になると分かっていたから FDE という職種を作った」という因果までは、公式資料では確認できていません。これは、番組での私の解釈です。[Palantir の2019年のブログ](https://blog.palantir.com/dev-versus-delta-demystifying-engineering-roles-at-palantir-ad44c2a6e87)では、FDE（社内では Delta とも呼ばれた役割）は、顧客のところでプラットフォームを導入し、課題を解く職種として説明されています。事実として書くなら、「オントロジーづくりは、いまの FDE の仕事の中核の一つ」までに留めます。

本領としてお話ししたのは、あらかじめ全部の分岐をワークフローに書いておけない、予期せぬ問題への判断です。すでに出荷された注文は「キャンセル」できず、「返品」として扱う、といった切り分けは、操作の名前を分けるだけでなく、ルールごと定義しておく必要があります。優秀な担当者は、頭の中の「世界地図」を使って臨機応変に動きます。その地図を共有できていれば、AIも、どの情報にアクセスし、どこに連絡すべきかが見えてくる、というのが番組での見立てです。

![](https://assets.st-note.com/img/1794814510-takp7BQdOPFbsC5hueYyJSAI.jpg)
<!-- figure: F8 -->

▲ キャンセルと返品は別のアクション。注文オブジェクトの出荷状況（プロパティ）により、出荷前はキャンセル、出荷後は返品

### デモ（架空データのシミュレーションです）

番組の後半では、PIVOT の番組づくりをモデルにした想定で、出演者のキャンセルから代打を探し、人間が承認したあと、関連するシステムへ連携する流れを見てもらいました。これは架空のデータで動かしたシミュレーションです。裏側のグラフは機械が読める構造になっていて、過去の出演やテーマ、条件を辿って候補を出す、という説明です。

使った固有名や金額はダミーです。実在の方の出演条件ではありません。承認を外して自律的に進めることも原理的にはできますが、その場合も、参照している情報が新しい出演者に更新されていなければ、後続の作業（番組では、宣伝まわりの連携としてお話ししました）を誤ります。

![](https://assets.st-note.com/img/1794814510-CgbSrhiezUROGYo0DWuTw28J.jpg)
<!-- figure: F9 -->

▲ 想定・ダミーデータ。キャンセルを検知 → グラフを辿り候補を探す → 人が承認 → 関連システムへ連携（企画データ、概要欄、宣材の利用確認、演者との連絡）。点線「承認を外す自律運転でも、責任は残る」

### 導入は、足元の小さな地図から

最初から全社の地図を描く必要はありません。負担の大きい業務、判断に時間がかかる業務、多くの人とシステムを巻き込む業務から、ルール、データ、データの所在、操作に必要な権限を一つずつ言語化します。小さな地図がいくつかできると、つながり始めて、世界地図に近づいていきます。

個人や小さな組織なら、正式なオントロジー基盤でなくとも、エージェントがみな参照するファイルを共有するだけで足りる場合もある、とお話ししました。大きな会社では、そうはいきません。オントロジーを中心にした基盤を、各社がどう位置づけるかは、いま企業の側でも判断が求められている、というのが私の見立てです。

番組では、Microsoft、Palantir、Databricks の名前を挙げました。確認できた範囲だけを書くと、Microsoft は 2025年11月18日に [Fabric IQ をプレビューとして発表](https://blog.fabric.microsoft.com/en-us/blog/from-data-platform-to-intelligence-platform-introducing-microsoft-fabric-iq)し、[2026年6月の Build](https://azure.microsoft.com/en-us/blog/microsoft-build-2026-building-agentic-apps-with-microsoft-fabric-and-microsoft-databases/) で一般提供を発表しています。ただし、中核の「オントロジー」の機能は、2026年11月16日時点の [Microsoft Learn](https://learn.microsoft.com/en-us/fabric/iq/ontology/overview) でもプレビューと書かれています。Databricks は 2026年6月16日に [Genie Ontology を発表](https://www.databricks.com/blog/introducing-genie-one-genie-ontology-and-genie-agents)し、[同年11月11日に一般提供](https://www.databricks.com/blog/announcing-ga-genie-ontology)としています。Palantir は、自社ドキュメントで、オントロジーを中心としたソフトウェアアーキテクチャを[最大の差別化要因](https://www.palantir.com/docs/jp/foundry/platform-overview/overview)だと書いています。各社が「オントロジー」と呼ぶ範囲の違いは、2-4節で触れます。

「奪い合い」や優劣は、私の評価ではありませんし、比較するつもりもありません。番組で「最も早く提供した」とお話しした箇所は、基準によって変わるので、この記事では「早くから取り組んだ企業のひとつ」に言い換えます。価格の高低も、公開の価格表では確認できていないため、ここでは扱いません。

社内でツールが分かれていると、全社の地図は作りにくくなります。番組では、Dify や Claude、Gemini など、部署ごとに違う道具を使っている例が話題になりました。

ロックインのリスクは、番組でも認めました。それでも、世界地図があることが、エージェントを業務で使ううえでの重要なピースになる、というのが私の考えです。

![](https://assets.st-note.com/img/1794814510-I1j2JBYhnCOwQGFDo4bAWyZk.jpg)
<!-- figure: F10 -->

▲ 経費精算・注文と返品・出演の調整の小さな地図が、世界地図につながる。ルール・データ・システム・権限を書き出す。個人・小規模は、全エージェントが参照するファイルで足りる場合も。大企業では、基盤の選定が判断になる（見立て）

---

## 2. 『意味の設計図』は、どこまでを指すか

番組では、「オントロジー」という一つの言葉で、二つのものを続けて話していました。一つは、哲学や情報工学で使われてきた、一般的な意味のオントロジーです。もう一つは、Palantir が自社の製品の中心に置く Foundry Ontology です。コメントで「層が混ざっている」と指摘されたのは、ここを分けずに話したことも一因だと思います。この章では、二つを分けて書きます。

### 2-1. 一般的なオントロジー：意味の設計図

情報工学でよく引かれる定義は、[Gruber の「概念化の明示的な仕様」](https://tomgruber.org/writing/ontolingua-kaj-1993.pdf)です。[Studer ら](https://doi.org/10.1016/S0169-023X(97)00056-6)は、これを「共有された概念化の、形式的で明示的な仕様」と言い直しています。[Guarino ら](https://link.springer.com/chapter/10.1007/978-3-540-92673-3_0)は、オントロジーという成果物と、それが表そうとする概念化そのものを区別しています。

書き表すための標準もあります。RDF は[トリプルでグラフを表すデータモデル](https://www.w3.org/TR/rdf11-concepts/)で、OWL はクラスやプロパティ、個体と、その意味を定める言語で、[OWL のオントロジー](https://www.w3.org/TR/owl2-mapping-to-rdf/)は RDF グラフとしても書けます。[SHACL](https://www.w3.org/TR/shacl/) は、RDF グラフが満たすべき制約を書き、検証するための標準です。設計図に沿って、実体と関係をグラフとして集めたものは[ナレッジグラフ](https://arxiv.org/abs/2003.02320)と呼ばれ、その研究は、データモデル、問い合わせ（SPARQL など）、検証、推論まで幅広く扱っています。

ここで押さえておきたいのは、これらの標準が定めるのが、意味、推論、制約、問い合わせだという点です。[SPARQL 1.1 Update](https://www.w3.org/TR/sparql11-update/) のようにグラフ自体を更新する仕様はありますが、業務システムへの書き込み（トランザクション、権限、副作用の制御）の仕組みまでは、規定していません。一般的な意味で「オントロジー」と言うとき、中心にあるのは設計図、つまり型と関係と制約です。

私の調査では、この議論を歪める誤りが、対称的に二つあると整理しています。一つは**グラフの誤謬**で、データがつながっていればオントロジーだ、とみなすことです。もう一つは**形式主義の誤謬**で、特定の形式言語（たとえば OWL）で書いていなければオントロジーではない、とみなすことです。番組の「点と線」の説明は、前者に寄って聞こえた面があったと思います。

### 2-2. Foundry Ontology：設計図に、中身と動かす部品まで

[Palantir の英語版ドキュメント](https://www.palantir.com/docs/foundry/ontology/core-concepts)は、オントロジーをまず「世界の分類」と書き、Foundry では「組織のデジタルツイン」だと説明します。データセットやモデルを、オブジェクトタイプ、プロパティ、リンクタイプ、アクションタイプに写して、一つにまとめたもの、という位置づけです。

ここで大事なのは、Foundry でも**型とインスタンスは区別されている**ことです。オブジェクトはオブジェクトタイプの一つのインスタンスで、データセットの1行に当たります。リンクも、[リンクタイプの一つのインスタンス](https://www.palantir.com/docs/foundry/ontology/core-concepts)です。1章で書いた「設計図と実データのグラフは層が違う」は、Foundry でもそのまま成り立ちます。

違うのは、「オントロジー」という語の範囲です。一般的には、設計図（型と関係と制約）を指すことが多い。Foundry は、設計図と、その中身（オブジェクトとリンク）と、動かす部品（アクション、関数、動的セキュリティ）を、まとめて「オントロジー」と呼びます。

私の見方では、Foundry Ontology は、グラフ（オブジェクトとリンクのデータの層）と、実行基盤までを含む呼び名です。そう読む根拠として、公式の記述を挙げておきます。

- 意味の要素（オブジェクト、プロパティ、リンク）と、[動きの要素](https://www.palantir.com/docs/foundry/ontology/overview)（アクション、関数、動的セキュリティ）の両方を含む
- オントロジーは[「セマンティックレイヤー」ではない](https://www.palantir.com/docs/foundry/architecture-center/ontology-system)、と明記している。意味は動き（kinetics）と組で扱う必要があり、アクションは業務やエッジのシステムへ書き戻される
- アクションは、ユーザーが定義したロジックに基づく[単一のトランザクション](https://www.palantir.com/docs/foundry/action-types/overview)で、編集を反映した最新の状態は書き戻し用のデータセット（writeback dataset）に残る
- アクションを実行してよいかは、[実行条件](https://www.palantir.com/docs/foundry/action-types/submission-criteria)（submission criteria、旧称 validations）で決める
- オントロジーのデータは、[オブジェクトとプロパティのポリシー](https://www.palantir.com/docs/foundry/object-permissioning/managing-object-security)、またはデータソースのポリシーで保護する
- 関数は、[TypeScript や Python で書くロジック](https://www.palantir.com/docs/foundry/functions/overview)

グラフという言い方についても書いておきます。Palantir 自身も、一部の資料ではグラフとして説明しています。2023年7月の[半導体業界向けホワイトペーパー](https://www.palantir.com/assets/xrfr7uokpv1b/2T3BgBpe3drnqBaSTCXl6O/bdc9445d10053eb84b3f9487e63fc2d7/Whitepaper_-_Accelerating_Research_and_Development_in_the_Semiconductor_Industry.pdf)には、オントロジーによって「knowledge graph」を作れる、という書き方があります。[公式ブログ](https://blog.palantir.com/ontology-finding-meaning-in-data-palantir-rfx-blog-series-1-399bd1a5971b)にも、オントロジーが定める「object graph」という表現があります。一方で、[製品ドキュメント](https://www.palantir.com/docs/foundry/ontology/core-concepts)の中心にある言い方は、グラフではなく[「組織のデジタルツイン」](https://www.palantir.com/docs/foundry/ontology/overview)です。どちらも Palantir の言葉で、強調している面が違う、と私は読んでいます。

なぜここまで「動かす部品」を一体で持つのか。私は、使われてきた現場の厳しさと関係していると見ています。Palantir は国防の分野でも使われていて、たとえば米陸軍は2025年7月31日、Palantir との[エンタープライズ契約を発表](https://www.army.mil/article/287506/u_s_army_awards_enterprise_service_agreement_to_enhance_military_readiness_and_drive_operational_efficiency)しました。75件の契約（元請け15件と関連60件）を1本にまとめ、期間は最長10年、金額は最大100億ドルの上限つきです。発表は、この額は上限であって、支払いが確定した額ではないとも書いています。国防のように誤った操作が許されない現場では、AIやシステムに何を見せ、何をさせてよいかを、権限、実行条件、監査の記録で縛っておく必要があります。国防レベルの現場で求められるこの縛りを、私は「ハーネス」と呼んでいます。これは Palantir の用語ではなく、私自身の見方です。

![](https://assets.st-note.com/img/1794814510-hFmjTkRoJclOpU6MZQB7Nxeu.jpg)
<!-- figure: F11 -->

▲ 左に「一般的なオントロジー」＝設計図の層（クラス・関係・制約。標準は RDF / OWL / SHACL）を1枚の板で描く。右に「Foundry Ontology」を3枚の板で描く。下から、設計図（オブジェクトタイプ・リンクタイプ・プロパティ）、中身（オブジェクトとリンク）、動かす部品（アクション・関数・実行条件・セキュリティ・書き戻し）。3枚は層を分けたまま、外側の囲み線に「Foundry がまとめて『オントロジー』と呼ぶ範囲」。左右の設計図の板どうしを点線で結び「ここは同じ層」

### 2-3. 並べてみると

二つを、同じ項目で並べると、おおよそ次のようになります。左の列は一般的な整理、右の列は Palantir の英語版ドキュメントの言葉です。

![](https://assets.st-note.com/img/1794816298-4LkmFAplGCc985NDR6bQTjKP.png)
<!-- figure: TABLE1 -->

  
▲ 一般的なオントロジーと、Palantir の Foundry Ontology の比較

表の「対象外」は、標準が規定していない、という意味です。OWL や RDF を使う基盤が、書き込みや権限の仕組みを別に持つことは、もちろんあります。

### 2-4. Microsoft Fabric IQ は、切り方が違う

対照として、Microsoft Fabric IQ のオントロジーも短く見ておきます。[Microsoft Learn のページ](https://learn.microsoft.com/en-us/fabric/iq/ontology/overview)の見出しは「What is ontology (preview)?」で、2026年11月16日時点でプレビューです。

そこでは、オントロジーは、エンティティ、プロパティ、関係、ルール、メトリクスなどの定義を、既存の企業データにバインドするものだと書かれています。オントロジーが別のデータストアになる必要はない、とも書かれています。グラフ（Graph in Microsoft Fabric）は、関係の経路そのものが大事な場面のための「任意の実行層」で、オントロジーから作るスキーマのグラフは、既定ではインスタンスのデータを読み込みません。必要なときに、[関係するデータを実体化する](https://learn.microsoft.com/en-us/fabric/iq/ontology/overview)、という説明です。

つまり、Fabric IQ は「オントロジー」を定義の側に寄せて切り、グラフの実行は別の層として選べるようにしています。Foundry は、定義と中身と動かす部品をまとめて「オントロジー」と呼びます。これは、どちらが優れているかという話ではなく、どこまでを「オントロジー」と呼ぶかの切り方の違いです。

私の整理では、製品をまたいで比べるときは、製品上の名詞（オブジェクト、エンティティ、グラフ）どうしを並べるのではなく、「定義」「実データとのつながり」「問い合わせ」「書き込みと実行」「権限」といった中立的な役割に写してから比べる方が、取り違えが少なくなります。また、公式ドキュメントで確かめられるのは「その機能がある」という事実までで、「精度や生産性が上がる」という便益の主張とは分けて読むべきだと考えています。

![](https://assets.st-note.com/img/1794814510-OJoKBY0ys8cHuU2j3eR6NTIa.jpg)
<!-- figure: F12 -->

▲ 「どこまでを『オントロジー』と呼ぶか」の比較。左「[Palantir の Foundry Ontology](https://www.palantir.com/docs/foundry/ontology/core-concepts)」：定義（オブジェクトタイプ等）・中身（オブジェクトとリンク）・動かす部品（アクション・[関数](https://www.palantir.com/docs/foundry/functions/overview)・動的セキュリティ）を一つの実線の囲みに入れる。右「[Fabric IQのオントロジー](https://learn.microsoft.com/en-us/fabric/iq/ontology/overview)（プレビュー）」：定義（エンティティ・プロパティ・関係・ルール・メトリクス）を実線で囲み、既存データへ「バインド（別のデータストアにしない）」の矢印。グラフは囲みの外に点線で「任意の実行層。既定ではインスタンスを読み込まない」

### 2-5. 番組の言い方と、Palantir の用語

番組の言葉を、Palantir の用語に対応づけておきます。起点は、[日本語のプラットフォーム概要](https://www.palantir.com/docs/jp/foundry/platform-overview/overview)です。日本語ドキュメントの多くには、英語版からの機械翻訳で、正確性は検証されていない、という注があります。用語は英語版と突き合わせたうえで使っています。

公式の一言は、こうです。オントロジーは、[単なるデータではなく](https://www.palantir.com/docs/jp/foundry/platform-overview/overview)、企業の**意思決定**を表現するために設計されている。意思決定は、[次の3つに分解](https://www.palantir.com/docs/jp/foundry/platform-overview/overview)できます。

- **データ**: 意思決定の文脈を作る、現実や業務の事実。オブジェクトとリンクとして統合される。
- **ロジック**: ガードレールになる組織・業務のルール、モデル、分析。
- **アクション**: 意思決定の「動き」。判断が現実世界に伝わる方法を制御する。公式の言い方では、企業の「動詞」です。

[アーキテクチャの解説](https://www.palantir.com/docs/jp/foundry/architecture-center/ontology-system)では、ここに**セキュリティ**を加えた4要素として書かれています。権限は後から足すオプションではなく、最初からある部品だ、と私は考えています。

![](https://assets.st-note.com/img/1794814510-PnwHBWQvVAXliUu0adpF9hz6.jpg)
<!-- figure: F4 -->

▲ 意思決定の3つの構成要素。データ（オブジェクトとリンク）、ロジック（ルールとモデル）、アクション（動詞・権限・書き戻し）。下に公式の問いの要約。協働が前提である旨の注記あり

![](https://assets.st-note.com/img/1794814510-7hJkxKZvHa1g6jcwSCnVmozD.jpg)
<!-- figure: F5 -->

▲ Excel（意味付けはできるが、権限・トランザクション・副作用の制御は保証できない）と、オントロジー＝セマンティック要素＋キネティック要素。「実行条件（バリデーション）」。結び「意味付けだけでは、エージェントの行動を制御しきれない」

![](https://assets.st-note.com/img/1794816347-lAkIHr17aZM0i6mxUKLnSPdF.png)
<!-- figure: TABLE2 -->

  
▲ 番組での言い方と、Palantir 公式に近い語

データをモデル化すると、[API やオントロジー SDK](https://www.palantir.com/docs/jp/foundry/platform-overview/overview) を通じて、社内のつながり（公式は「業務バス」と呼びます）としても使える、とされています。アクションは、通知などの[副次的効果](https://www.palantir.com/docs/jp/foundry/action-types/overview)も含みます。

---

## 3. 番組では話しきれなかったこと

ここからは、番組で簡略化したところと、コメントで指摘されたところを補います。指摘は批判としてではなく、説明を正確にするための材料として受け取りました。コメントの引用は原文に沿い、抜粋する場合はその旨を書いています。

### 3-1. 14:47の「グラフ」を、書き分けます

番組の14:47ごろ、進行が「グラフ」をXY軸の関数の図として受け取ったのに対し、私は「点と点を線で結んだものがグラフ」と説明しました。導入のたとえのつもりでしたが、概念を混ぜてしまいました。コメント欄の @thara6890 さんの指摘どおりです。

> 14:47 座標平面のグラフ（関数を満たす順序対の集合の可視化表現）と、グラフ理論のグラフ（ノードとエッジの集合）とは全く異なる概念だと思います

（後者の一部を座標平面図上で表現することはできるとは思いますが）

この説明は正しい、と考えています。中学で習う「y=2x+1 のグラフ」は、関数を満たす順序対 (x, f(x)) の集まりで、座標平面上の曲線として見えます。一方、ナレッジグラフの「グラフ」は、[グラフ理論のグラフ](https://diestel-graph-theory.com/)、つまり頂点の集合と辺の集合の組 G=(V,E) です。座標も、連続性も、前提ではありません。

「点と線で結ぶ」という導入は、後者（ネットワークとしてのグラフ）には使えます。ただ、関数のグラフと同一視はできません。関数のグラフは「点を線で結んだもの」ではなく、点そのものの集まりです。番組の説明は、ここが粗かったです。

設計図とグラフの層の話は、1章と2章に書いたとおりです。同一視しないことと、「グラフという表現を使ってはいけない」ことは、別の話です。

### 3-2. オントロジー、セマンティクス、因果は、層が違います

@猛-c4w さんから、次の指摘をいただきました。

> オントロジーとセマンティックス、因果などとごっちゃにしてませんか？レイヤの違うことを全部オントロジーになっていますよね！！

ご指摘には、一理あります。学術的には、おおよそ次のように層を分けられます。

- **オントロジー**: [何が存在し、どう関係するか](https://link.springer.com/chapter/10.1007/978-3-540-92673-3_0)を書いた、[形式的な仕様](https://tomgruber.org/writing/ontolingua-kaj-1993.pdf)
- **セマンティクス**: 言葉や指標が何を意味するか。BI では「売上」などの定義を一元化するセマンティックレイヤー、という使い方もあります
- **因果**: 介入したときに、結果がどう変わるかを扱う理論

私の調査では、オントロジーの隣には、似ていて別の成果物がいくつも並んでいます。統制語彙、分類体系、データスキーマ、ナレッジグラフ、セマンティック層、デジタルツインなどです。これらは「単純なものから高度なものへ」の一列の階段ではなく、それぞれ答える問いが違う、と整理しています。たとえば、セマンティック層は「指標をどう計算するか」に、デジタルツインは「対象の状態がいまどうか」に答えます。オントロジーは「どんな種類のものと関係を、共通の前提として認めるか」に答えます。

番組で「在庫が半分になったら取引先に連絡する」とお話しした部分は、厳密には「何が存在するか」だけではなく、手続きや因果の知識です。Palantir の用語に当てはめると、型の定義だけではなく、ロジック（関数）とアクションに入ります。

Palantir の言うオントロジーが、意味の層に加えて、中身と動きと権限まで含む[広い呼び名](https://www.palantir.com/docs/foundry/architecture-center/ontology-system)であることは、2章に書いたとおりです。番組では、一般的な意味と、この広い意味を分けずに話していました。この記事では、一般的な意味のときは「一般的なオントロジー」、Palantir の製品を指すときは「Foundry Ontology」と書き分けます。

哲学の「存在論」との関係についても、@ksngyz さんが触れてくださいました。情報工学のオントロジーは、哲学用語を借りた別物です。同コメントの後半は、私の問題意識にとても近いものでした。

> というのは冗談で、LLMの登場によって、従来の人工知能研究におけるオントロジーの問題はある種迂回できたと思っていましたが、いざ企業の実業務に展開しようとすると、再びオントロジーの問題が立ちはだかるというのは興味深いですね。ある意味、イタチごっこのようでもあります。

迂回できたように見えたのは、言葉の理解の側だと、私は考えています。迂回しきれないのは、責任と権限の側です。

あわせて、@bghk-g9r さんの「誰かによる近似でしかないことに注意しなければなりません。」も、そのとおりです。オントロジーは現実そのものではなく、ある視点からの模型です。誰の近似かを明示し、ずれたら直せる運用（版の管理や承認）が要る、と私は見ています。

### 3-3. LLMがあっても、オントロジーが残る理由

@nikko8x さんから、次の反論をいただきました。

> 昔、LLMがない時代はPCが物事を理解するにはオントロジーが必要ですが、現在のLLMはpythonが文脈から蛇かプログラム種類か理解しているはず。現在オントロジーがまだ必要の例は思いつきにくい

この指摘は、番組の Python の例に対して、正当だと思います。いまの LLM は、文脈から多義語をかなり解けます。あの例だけで「いまもオントロジーが要る」と説得するのは、弱いです。

私が番組で本当に言いたかった核は、意味の取り違えよりも、**行動の制御**です。誰が、どの条件で、どのシステムに、何をしてよいかを、LLM のその場の判断だけに任せず、仕組みで保証する。権限、実行条件、監査が、その中身です。

言葉の理解が進んでも、企業データへの質問では、データをナレッジグラフ（オントロジー付き）の形で渡した方が正答率が上がった、という報告もあります。GPT-4 を使った[著者らのベンチマーク](https://arxiv.org/abs/2311.07509)では、zero-shot（例を与えない条件）で SQL に直接聞いた場合は16%、ナレッジグラフ経由では54%だった、とされています。これは一つの実験であり、すべての業務に同じ数字が出る、という意味ではありません。ただ、「意味が分かれば、あとは自然文だけで足りる」とは言い切れない、という材料にはなると思います。

「いままで普通に考えていたことを、専門用語で言っているだけでは」という疑問もあるでしょう。半分は、そのとおりです。大事なのは用語ではなく、意味の定義と、行動の条件を、人が後から検証できる形で残すことです。

私の手元の実験でも、近い傾向が出ています（未公開・未査読です）。架空の業務を題材に、AIエージェントを使って組んだ検証で、同じ業務知識を「平文の文書」「用語集」「形式的なオントロジー」の形で渡す条件と、何も渡さない条件を比べました。解析した2,117回の実行では、業務知識をそもそも渡すかどうかで、点数に25.7〜49.3ポイントの差が出ました。一方、同じ知識を、平文の文書ではなくオントロジーの形式で書くことの上乗せは、難しい定義や判定ルールのタスクに限って約2.3ポイントで、手順を追う型の業務では差が見えませんでした。主な集計では統計的に有意でしたが、より慎重な条件で集計し直すと約2.0ポイントに縮み、有意とまでは言えなくなります。一つの架空の業務での、査読を経ていない結果です。それでも私は、「オントロジーにすれば性能が飛躍的に上がる」というより、まず知識を渡すことが効き、形式化は境界の判定のような細部と、実行前の検査に効く、と受け取っています。

### 3-4. ブレーキは注意書きではなく、アクションと権限です

Excel でも意味付けはできます。保証しにくいのは、先に書いたとおり、権限とトランザクション、副作用の制御です。

[Palantir の公式な基本パターン](https://www.palantir.com/docs/jp/foundry/platform-overview/overview)では、AI エージェントが直接変更するのではなく、提案を作り、人が判断してからオントロジーにコミットします。番組のデモで、候補を出したあと人間が承認し、その後に関連システムへ連携した流れは、このパターンに近い、と私は考えています。承認を外して自律運転にすることも、原理的にはできます。その場合に残る責任は、仕組みを外した側の判断です。

@BullGo-s8c さんは、Human in the Loop の限界を、こう書いてくださいました。

> Human In the Loopなんて言うけど結局、AIエージェントだけでは自己完結しない。任せられるタスクの幅が広がるだけだろうね。ただその分、アウトプットに対する人間のレビュー負担も相当なものになる。しかも途中の推論がブラックボックスだったりいちいち遡及できない状況があるから、実は分からないものに対して真に責任をとれるか？という話にもなる。

さながら、身体に人工の異物を混入するようなもので、いつか社会活動がスタックするような巨大な事故が起きる気がする。

途中の推論が全部見えるわけではない、という点は、認めます。そのうえで、オントロジー側で残せるのは、「何を、どの権限で、どの条件で実行したか」を、アクション単位で記録し、監査できるようにすることだ、と私は考えています。レビューの負担そのものが消えるわけではありません。ここは、解決済みだとは言いません。

自動化が進むと、人は監視役になり、いざというときに介入しにくくなる。この逆説は、1983年に Bainbridge が[「自動化の皮肉」](https://doi.org/10.1016/0005-1098(83)90046-8)として論じています。PIVOT のコメント欄でも、とんでもない子さんが、同じ構造を指摘してくださいました。

> 「オントロジー」の精度が上がったにしても、やはり『ＡＩは間違うことがある』という大前提の課題はどこまでも残り続ける。よって、政府、地方自治体や企業では、最終チェックを行える人材が特に重要になると思われますが、いかがでしょうか？

そして、最大の懸念は、ＡＩやＡＩエージェントを使い続けることにより、「最終チェックを行える人材」が育ちにくい社会になってしまう、ことであると思われます。

（とんでもない子さん、PIVOTコメント、抜粋）

私の考えでは、最終チェックができる人は、これからも必要です。だからこそ、提案を人が判断する運用を残し、判断の練習量をゼロにしないことが大切だと思います。オントロジーは、間違いをゼロにする装置ではありません。間違ったときの影響範囲と、後から辿れる記録を、あらかじめ決めておく装置に近い、と見ています。

[前回の Muse の記事](https://note.com/haginota/n/nba922eb92cd9)では、「隔離と権限の管理は別の話です」と書きました。企業のオントロジーでも、同じように考えられます。ファイルに書いたお願い（注意書き）だけでは権限は縛れず、ブレーキになるのは実行条件と権限の設定だ、と私は見ています。

### 3-5. 小さな地図を、どうつなぎ、誰が維持するか

地図作りそのものが大変ではないか、自動化できないか、という問いも多くいただきました。

> オントロジーの地図を作るの自体が大変すぎませんか？オントロジー作りを自動化できないのでしょうか？（@雅-f2c、2026-11-15ごろ、抜粋）

> オントロジーの構築を人間がやるのかAIがやるのかという話が出ていましたがAIにやらせて重要なところは人間がチェックしていくのでしょうかね（@hiroyukik2588、2026-11-15ごろ、抜粋）

番組でも、人間の監査のもとで作るのか、AIに描かせるのかは、方針次第だとお話ししました。後者にするなら、企業は責任を取れるのか、が残ります。@hiroyukik2588 さんの読み、つまり「AIが作り、重要なところを人が確認する」は、いまの業界の動きにも近いと思います。たとえば Databricks は、Genie Ontology について、[エージェントが組み立て、人が統治する](https://www.databricks.com/blog/announcing-ga-genie-ontology)、と説明しています。研究の側でも、[LLM でオントロジーを学習する試み](https://arxiv.org/abs/2307.16648)があります。自動化の可否を、ここでは言い切りません。

PIVOT の Wonderwall さんは、「オントロジー≒業務仕様書」と整理したうえで、粒度の違いを問うてくださいました。

> オントロジー≒業務仕様書なんですね。

（中略）

ただ、業務ごとに仕様の細かさと粗さがまちまちです。そこをどう平準化していくかがまだよく分からなかったです。

（Wonderwallさん、PIVOTコメント、抜粋）

部署ごとに定義の細かさが違うとき、共通の上位概念にそろえる、共通のプロパティやインターフェースを持つ、必要なら共有のオントロジーを使う、といった方法があります。Palantir では、[異なるオントロジーをまたぐリンク](https://www.palantir.com/docs/foundry/object-link-types/link-types-overview)はできず、その場合は共有オントロジーを検討する、と書かれています。番組で「地域の地図をつないで世界地図にする」とお話ししたことの、具体的なやり方の一つです。

特定の製品に定義を閉じ込めると抜け出せなくなる、という懸念も、もっともです。@大江戸太郎-s5o さんが指摘したロックインは、番組でも認めました。設計図を、標準形式でも書き出せる形で持つ、というのは、一つの選択肢だと思います。定義そのものは、[W3C の RDF](https://www.w3.org/TR/rdf11-concepts/) や [OWL](https://www.w3.org/TR/owl2-mapping-to-rdf/) といった標準でも書けます。

ただし、2章で見たとおり、標準が受け持つのは意味と制約と問い合わせ（とグラフの更新）の側です。クラス名と関係名を書き出せても、データとの対応づけ、権限、操作の意味までは一緒に移りません。私の整理では、可搬性は「標準形式で書き出せるか」で判断するのではなく、テストするものです。小さな範囲を書き出し、別の環境で同じ問いと操作をやり直し、何が失われたかを書き出す。そこで初めて、持ち出せる範囲が分かると考えています。

（一点だけ、数字の範囲を補います。同コメントの「GDPの何割にもなる巨額のデジタル赤字」について、[総務省の白書](https://www.soumu.go.jp/johotsusintokei/whitepaper/ja/r08/html/nd211400.html)では、2025年のデジタル関連収支の支払超（いわゆるデジタル赤字）は約6.6兆円とされています。白書自身が、この区分にはデジタル分野以外のサービスに係る収支も含まれる、と注記しています。名目GDPとの比較は概算ですが、私の見立てでは「何割」ではなく、1%程度の規模です。）

### 3-6. FDEと、「事務の話では」という感想

FDE について、事実として確認できたのは先に書いた範囲です。[顧客の現場でプラットフォームを導入し](https://blog.palantir.com/dev-versus-delta-demystifying-engineering-roles-at-palantir-ad44c2a6e87)、課題を解く職種である。オントロジーづくりは、いまのその仕事の中核の一つになりうる。職種の起源をオントロジーに直接結ぶのは、私の解釈に留めます。

@4500-b3b さんからは、次の感想をいただきました。

> 事務屋の仕事だなー。　エンジニア領域でのオントロジーを示してほしい。どこもやっていない

番組の例が、経費精算や番組づくりなど、事務寄りに見えた、という感想は妥当だと思います。一方、「工学の領域ではどこもやっていない」は、当たりません。プラントのライフサイクルデータを扱う [ISO 15926](https://www.iso.org/standard/29557.html)、上位オントロジーの [ISO/IEC 21838-2](https://www.iso.org/standard/74572.html)（BFO）、製造業向けの [Industrial Ontologies Foundry](https://www.industrialontologies.org/)、設備のデジタルツインに関する [Asset Administration Shell](https://webstore.iec.ch/en/publication/65628)（IEC 63278-1）など、工学側の蓄積は以前からあります。[Palantir の公式の例](https://www.palantir.com/docs/jp/foundry/architecture-center/ontology-system)も、航空機やフライト、[製造工場](https://www.palantir.com/docs/foundry/object-link-types/link-types-overview)、作業指示など、工学寄りが多いです。

次に書くときは、製造業の例を一つは足したい、と思っています。

---

## 4. コメントで多かった問い

公開から2日ほど（2026年11月16日11時ごろ、日本時間）の時点で、[YouTube のコメント](https://www.youtube.com/watch?v=_V7IF1XdNLQ)は29件（公式の固定コメント1件、返信1件を含む）、[PIVOT サイトのコメント](https://pivotmedia.co.jp/movie/15261)は2件でした。ここでは、多かった問いと、この記事の受け先だけを示します。個別の解釈の詳細は、これ以上は重ねません。

- **地図は誰が、どうやって作るのか。自動化できるのか。** 3-5節、3-6節。
- **LLMがあれば、オントロジーは不要ではないか。** 3-3節。Python の例だけでは弱い、という指摘は受け入れます。
- **用語の層が混ざっている。グラフの意味も混ざっている。** 2章、3-1節、3-2節。
- **人間がループに入っても、責任とレビュー負担はどうなるのか。最終確認ができる人は育つのか。** 3-4節。
- **日本の現場や組織の文化と、相性はどうなのか。** 番組では深く扱えませんでした。雑談や現場の空気で決まる判断を、そのまま否定するつもりはありません。ただ、「AIが使えない」で終わるのではなく、判断の根拠を後から辿れる形に近づけられるかどうかが、私は論点だと考えています。答えを急がないでおきたい問いです。
- **基盤に閉じ込められないか。自分たちで持てるか。** 2-4節、3-5節。

次回や続きで取り上げたい、とコメントで要望のあったテーマ（実際の構築プロセス、部門をまたぐ統合、FDE の実務、具体的な事例）は、まだこの記事では書ききれていません。宿題として受け取ります。

---

## 5. まとめ

持ち帰っていただきたいのは、次の3点です。

1. **オントロジーは意味の設計図であり、実データのグラフとは層が違う。** Palantir の Foundry Ontology は、層を分けたまま、設計図と中身と動かす部品までをまとめて「オントロジー」と呼びます。どこまでをその名前で呼ぶかは、製品によって違います。「点と線」は導入として使えますが、関数のグラフと、ネットワークとしてのグラフは別物です。
2. **ブレーキは、記憶や注意書きではなく、実行条件と権限である。** Excel でも意味は書けます。保証しにくいのは、誰が、どの条件で、何をしてよいかです。AIの間違いをゼロにはできません。間違ったときの範囲と、記録を決めておくことが、企業では先に来ます。
3. **全社の世界地図から始めない。** 負担の大きい業務の、小さな地図からでよい。個人や小さな組織なら、共有ファイルでも足りる場合があります。大きな組織では、基盤の選び方が判断になりますが、優劣をここで付けるつもりはありません。

コメントをくださったみなさま、ありがとうございました。指摘のおかげで、番組では雑になっていた層を、書き分けることができました。また続きが書けたら、ここで補います。

---

## 出典

資料の確認は、2026年11月16日（日本時間）です。

PIVOT「オントロジーとは?」本編（YouTube、2026年11月14日公開） [https://www.youtube.com/watch?v=_V7IF1XdNLQ](https://www.youtube.com/watch?v=_V7IF1XdNLQ)

PIVOT「オントロジーとは?」 [https://pivotmedia.co.jp/movie/15261](https://pivotmedia.co.jp/movie/15261)

萩野 貴拓「YouTube20万回再生、PIVOT週間1位。嬉しい声と、まだ残る不安。PIVOTのコメントに答えます」 [https://note.com/haginota/n/nba922eb92cd9](https://note.com/haginota/n/nba922eb92cd9)

Palantir「プラットフォームの概要」（日本語版） [https://www.palantir.com/docs/jp/foundry/platform-overview/overview](https://www.palantir.com/docs/jp/foundry/platform-overview/overview)

Tom Brown et al., “Language Models are Few-Shot Learners,” 2020 [https://arxiv.org/abs/2005.14165](https://arxiv.org/abs/2005.14165)

OpenAI「Introducing ChatGPT」（2022年11月30日） [https://openai.com/index/chatgpt/](https://openai.com/index/chatgpt/)

OpenAI「GPT-4」（2023年3月14日） [https://openai.com/index/gpt-4-research/](https://openai.com/index/gpt-4-research/)

PIVOT「OpenClaw どこまで自動化できる？」（2026年5月19日公開） [https://www.youtube.com/watch?v=PeZHAztFgqc](https://www.youtube.com/watch?v=PeZHAztFgqc) ／ [https://pivotmedia.co.jp/movie/14402](https://pivotmedia.co.jp/movie/14402)

矢野経済研究所「生成AI活用に関する企業アンケート調査」（プレスリリース、2025年12月19日） [https://www.yano.co.jp/press-release/show/press_id/3991](https://www.yano.co.jp/press-release/show/press_id/3991)

W3C「RDF 1.1 Concepts and Abstract Syntax」 [https://www.w3.org/TR/rdf11-concepts/](https://www.w3.org/TR/rdf11-concepts/)

Palantir「Ontology core concepts」（日本語版） [https://www.palantir.com/docs/jp/foundry/ontology/core-concepts](https://www.palantir.com/docs/jp/foundry/ontology/core-concepts)

Palantir「オントロジーを構築する」（日本語版） [https://www.palantir.com/docs/jp/foundry/ontology/overview](https://www.palantir.com/docs/jp/foundry/ontology/overview)

W3C「OWL 2 Web Ontology Language Mapping to RDF Graphs」 [https://www.w3.org/TR/owl2-mapping-to-rdf/](https://www.w3.org/TR/owl2-mapping-to-rdf/)

Palantir「アクションタイプ」（日本語版） [https://www.palantir.com/docs/jp/foundry/action-types/overview](https://www.palantir.com/docs/jp/foundry/action-types/overview)

Palantir「実行条件（Submission criteria）」（日本語版） [https://www.palantir.com/docs/jp/foundry/action-types/submission-criteria](https://www.palantir.com/docs/jp/foundry/action-types/submission-criteria)

Microsoft「Apply data validation to cells」 [https://support.microsoft.com/en-us/office/apply-data-validation-to-cells-29fecbcc-d1b9-42c1-9d76-eff3ce5f7249](https://support.microsoft.com/en-us/office/apply-data-validation-to-cells-29fecbcc-d1b9-42c1-9d76-eff3ce5f7249)

Palantir Blog「Ontology: Finding meaning in data (Palantir RFx Blog Series #1)」 [https://blog.palantir.com/ontology-finding-meaning-in-data-palantir-rfx-blog-series-1-399bd1a5971b](https://blog.palantir.com/ontology-finding-meaning-in-data-palantir-rfx-blog-series-1-399bd1a5971b)

Palantir Blog「Dev versus Delta: Demystifying engineering roles at Palantir」（2019年4月8日） [https://blog.palantir.com/dev-versus-delta-demystifying-engineering-roles-at-palantir-ad44c2a6e87](https://blog.palantir.com/dev-versus-delta-demystifying-engineering-roles-at-palantir-ad44c2a6e87)

Microsoft Fabric Blog「From data platform to intelligence platform: Introducing Microsoft Fabric IQ」（2025年11月18日） [https://blog.fabric.microsoft.com/en-us/blog/from-data-platform-to-intelligence-platform-introducing-microsoft-fabric-iq](https://blog.fabric.microsoft.com/en-us/blog/from-data-platform-to-intelligence-platform-introducing-microsoft-fabric-iq)

Microsoft Azure Blog「Microsoft Build 2026: Building agentic apps with Microsoft Fabric and Microsoft databases」 [https://azure.microsoft.com/en-us/blog/microsoft-build-2026-building-agentic-apps-with-microsoft-fabric-and-microsoft-databases/](https://azure.microsoft.com/en-us/blog/microsoft-build-2026-building-agentic-apps-with-microsoft-fabric-and-microsoft-databases/)

Microsoft Learn「What is ontology (preview)?（Fabric IQ）」（2026年11月16日時点でプレビューと記載） [https://learn.microsoft.com/en-us/fabric/iq/ontology/overview](https://learn.microsoft.com/en-us/fabric/iq/ontology/overview)

Databricks「Introducing Genie, Genie Ontology, and Genie Agents」（2026年6月16日） [https://www.databricks.com/blog/introducing-genie-one-genie-ontology-and-genie-agents](https://www.databricks.com/blog/introducing-genie-one-genie-ontology-and-genie-agents)

Databricks「Announcing the GA of Genie Ontology」（2026年11月11日） [https://www.databricks.com/blog/announcing-ga-genie-ontology](https://www.databricks.com/blog/announcing-ga-genie-ontology)

Thomas R. Gruber, “A Translation Approach to Portable Ontology Specifications,” 1993 [https://tomgruber.org/writing/ontolingua-kaj-1993.pdf](https://tomgruber.org/writing/ontolingua-kaj-1993.pdf)

Rudi Studer, V. Richard Benjamins, Dieter Fensel, “Knowledge engineering: Principles and methods,” Data & Knowledge Engineering 25(1–2): 161–197, 1998, DOI: 10.1016/S0169-023X(97)00056-6 [https://doi.org/10.1016/S0169-023X(97)00056-6](https://doi.org/10.1016/S0169-023X(97)00056-6)

Nicola Guarino, Daniel Oberle, Steffen Staab, “What Is an Ontology?,” 2009, DOI: 10.1007/978-3-540-92673-3_0 [https://link.springer.com/chapter/10.1007/978-3-540-92673-3_0](https://link.springer.com/chapter/10.1007/978-3-540-92673-3_0)

W3C「Shapes Constraint Language (SHACL)」 [https://www.w3.org/TR/shacl/](https://www.w3.org/TR/shacl/)

Aidan Hogan et al., “Knowledge Graphs,” ACM Computing Surveys, 2021 [https://arxiv.org/abs/2003.02320](https://arxiv.org/abs/2003.02320)

W3C「SPARQL 1.1 Update」（W3C勧告、2013年3月21日） [https://www.w3.org/TR/sparql11-update/](https://www.w3.org/TR/sparql11-update/)

Palantir「Core concepts」（Ontology、英語版） [https://www.palantir.com/docs/foundry/ontology/core-concepts](https://www.palantir.com/docs/foundry/ontology/core-concepts)

Palantir「Ontology building: Overview」（英語版） [https://www.palantir.com/docs/foundry/ontology/overview](https://www.palantir.com/docs/foundry/ontology/overview)

Palantir「Ontology system」（Architecture center、英語版） [https://www.palantir.com/docs/foundry/architecture-center/ontology-system](https://www.palantir.com/docs/foundry/architecture-center/ontology-system)

Palantir「Action types: Overview」（英語版） [https://www.palantir.com/docs/foundry/action-types/overview](https://www.palantir.com/docs/foundry/action-types/overview)

Palantir「Submission criteria」（英語版） [https://www.palantir.com/docs/foundry/action-types/submission-criteria](https://www.palantir.com/docs/foundry/action-types/submission-criteria)

Palantir「Manage object security」（英語版） [https://www.palantir.com/docs/foundry/object-permissioning/managing-object-security](https://www.palantir.com/docs/foundry/object-permissioning/managing-object-security)

Palantir「Functions: Overview」（英語版） [https://www.palantir.com/docs/foundry/functions/overview](https://www.palantir.com/docs/foundry/functions/overview)

Palantir「Accelerating Research and Development in the Semiconductor Industry」（ホワイトペーパー、2023年7月） [https://www.palantir.com/assets/xrfr7uokpv1b/2T3BgBpe3drnqBaSTCXl6O/bdc9445d10053eb84b3f9487e63fc2d7/Whitepaper_-_Accelerating_Research_and_Development_in_the_Semiconductor_Industry.pdf](https://www.palantir.com/assets/xrfr7uokpv1b/2T3BgBpe3drnqBaSTCXl6O/bdc9445d10053eb84b3f9487e63fc2d7/Whitepaper_-_Accelerating_Research_and_Development_in_the_Semiconductor_Industry.pdf)

U.S. Army「U.S. Army Awards Enterprise Service Agreement to Enhance Military Readiness and Drive Operational Efficiency」（2025年7月31日） [https://www.army.mil/article/287506/u_s_army_awards_enterprise_service_agreement_to_enhance_military_readiness_and_drive_operational_efficiency](https://www.army.mil/article/287506/u_s_army_awards_enterprise_service_agreement_to_enhance_military_readiness_and_drive_operational_efficiency)

Palantir「Ontology system」（アーキテクチャセンター、日本語版） [https://www.palantir.com/docs/jp/foundry/architecture-center/ontology-system](https://www.palantir.com/docs/jp/foundry/architecture-center/ontology-system)

Reinhard Diestel『Graph Theory』（定義 G=(V,E)） [https://diestel-graph-theory.com/](https://diestel-graph-theory.com/)

Juan Sequeda, Dean Allemang, Bryon Jacob, “A Benchmark to Understand the Role of Knowledge Graphs on Large Language Model’s Accuracy for Question Answering on Enterprise SQL Databases,” 2023 [https://arxiv.org/abs/2311.07509](https://arxiv.org/abs/2311.07509)

Lisanne Bainbridge, “Ironies of Automation,” Automatica, 1983 [https://doi.org/10.1016/0005-1098(83)90046-8](https://doi.org/10.1016/0005-1098(83)90046-8)

Hamed Babaei Giglou, Jennifer D’Souza, Sören Auer, “LLMs4OL: Large Language Models for Ontology Learning,” 2023 [https://arxiv.org/abs/2307.16648](https://arxiv.org/abs/2307.16648)

Palantir「Link types overview」 [https://www.palantir.com/docs/foundry/object-link-types/link-types-overview](https://www.palantir.com/docs/foundry/object-link-types/link-types-overview)

総務省『情報通信白書』令和8年版（デジタル収支） [https://www.soumu.go.jp/johotsusintokei/whitepaper/ja/r08/html/nd211400.html](https://www.soumu.go.jp/johotsusintokei/whitepaper/ja/r08/html/nd211400.html)

ISO/IEC 21838-2:2021（Basic Formal Ontology） [https://www.iso.org/standard/74572.html](https://www.iso.org/standard/74572.html)

Industrial Ontologies Foundry [https://www.industrialontologies.org/](https://www.industrialontologies.org/)

IEC 63278-1（Asset Administration Shell） [https://webstore.iec.ch/en/publication/65628](https://webstore.iec.ch/en/publication/65628)

ISO 15926-2:2003（プロセスプラントのライフサイクルデータモデル） [https://www.iso.org/standard/29557.html](https://www.iso.org/standard/29557.html)
