# pstack 実践ガイド 記事バナー

1つの HTML テンプレートから、note（1280×670）とカンリー Techブログ（1600×900 / 1200×675）を書き出します。記事タイトルがまだ仮なので、見出しは変数で差し替えられます。

## タイトルの差し替え

`src/render_banner.py` の先頭にある `TITLE` と `SUBTITLE` を書き換えてから、このフォルダで次を実行します。

```bash
python3 src/render_banner.py
```

ファイルを触らずに差し替えるなら:

```bash
python3 src/render_banner.py \
  --title '人の手なしで、古いリンク27件→0件' \
  --subtitle 'pstack 10分で読める入門'
```

`、` か改行で見出しを2行に分けます。2行目に `27件→0件` のような数字があると、27件はオレンジ、0件はティールになります。数字が無いタイトルは、そのまま紺で描きます。

Techブログ用には、右下に「カンリー Techブログ」が入ります。note 用には入りません。

## 出力

- `banner_note_1280x670.png`
- `banner_techblog_1600x900.png`
- `banner_techblog_1200x675.png`
