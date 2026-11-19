# PIVOT ontology note: English edition (for Substack)

**Status: DRAFT, NOT PUBLISHED.** Nothing has been posted to Substack or X. This GitHub copy is a working draft.

- Prepared: **2026-11-19 (JST)**
- Author / voice: **Takahiro Hagino (萩野貴拓)**, first person
- Original (Japanese, note): 「PIVOTで話した「オントロジー」と、話しきれなかったこと」 https://note.com/haginota/n/nbf04863132cf
- Original published: **2026-11-16 17:28 JST** (note API `publish_at`). Live body fetched **2026-11-19 (JST)** via `https://note.com/api/v3/notes/nbf04863132cf`. The live text is the source of truth (local drafts differ slightly and were not used).
- Companion piece: Canly Tech Blog article, English draft in [`../../2026-11-16/zenn-ontology/en/article_en.md`](../../2026-11-16/zenn-ontology/en/article_en.md). Terminology is shared with it.

## Title options

| # | Title | Note |
|---|---|---|
| 1 | **What I Said About Ontology on Japanese TV, and What I Didn't Get To** | **Working title** (used as H1). Closest to the original's "what I said / what I couldn't finish saying." |
| 2 | Ontology on Japanese TV: The Parts I Didn't Get To | Shorter |
| 3 | A Blueprint of Meaning: Following Up on My TV Segment About Ontology | Leads with the key-visual phrase |

Suggested Substack subtitle: *Ontology in general vs. Palantir's Foundry Ontology, and answers to viewers' questions.*

## Files

| File | Purpose |
|---|---|
| [`note_en.md`](note_en.md) | English Substack-ready Markdown. Inline links plus an unnumbered source list, no `[n]` markers. English figures embedded at pinned commit URLs. |
| [`note_ja.md`](note_ja.md) | Japanese source converted from the live note HTML (with figure placeholder comments listing the original note image URLs). |
| `figs/` | English figures (already committed in c1065d5 / 4a47e52; not modified here). |

## Process

1. Live HTML converted to Markdown (`note_ja.md`). The two table images were transcribed into Markdown tables.
2. First-pass translation: `claude -p` (Opus), 6 chunks in parallel, with a fixed glossary shared with the Tech Blog article.
3. Native-English edit pass: `claude -p` acting as an experienced English tech editor (short sentences, natural headings, no Japanese-isms; all facts, numbers, hedges kept).
4. Line-by-line review by Grok Bot against the Japanese. Mechanical checks: every non-image URL kept; numbers compared (differences are only formatting such as 3-1 → 3.1, 20万 → 200,000); hedges compared paragraph by paragraph between pass 2 and pass 3. One strengthened hedge was reverted ("control over actions, **more than** avoiding mix-ups in meaning").

Word count: **~9,060 words** (whole file, link targets excluded).

## Figure mapping (live note order → English figure)

| # in live note | English figure | Original note image | Notes |
|---|---|---|---|
| 1 | F1 | `1794814510-rRdEwAGjbyWFkHcz1S73OsQ9.jpg` | Pinned to **4a47e52** (the "PIVOT" pill became "My third time on a Japanese TV show"). All other figures pinned to **c1065d5**. |
| 2 | F2 | `…5hg4FD2MXa801qYcGIxOCSBK.jpg` | |
| 3 | F3 | `…AwIRMbJPHfEad2hySGkOin5q.jpg` | See mismatch 1 |
| 4 | F7 | `…dkJgAxLiVKBtqQwnj2P80D5R.jpg` | |
| 5 | F8 | `…takp7BQdOPFbsC5hueYyJSAI.jpg` | |
| 6 | F9 | `…CgbSrhiezUROGYo0DWuTw28J.jpg` | |
| 7 | F10 | `…I1j2JBYhnCOwQGFDo4bAWyZk.jpg` | |
| 8 | F11 | `…hFmjTkRoJclOpU6MZQB7Nxeu.jpg` | |
| 9 | (table) | `1794816298-4LkmFAplGCc985NDR6bQTjKP.png` | No English figure. Rendered as a Markdown table ("general ontology vs. Foundry Ontology"). |
| 10 | F12 | `…OJoKBY0ys8cHuU2j3eR6NTIa.jpg` | |
| 11 | F4 | `…PnwHBWQvVAXliUu0adpF9hz6.jpg` | |
| 12 | F5 | `…7hJkxKZvHa1g6jcwSCnVmozD.jpg` | |
| 13 | (table) | `1794816347-lAkIHr17aZM0i6mxUKLnSPdF.png` | No English figure. Rendered as a Markdown table ("what I said on the show → closest Palantir term"). |

F6 does not appear in the note (and has no English file). Alt text is taken from `figs/index.md`; italic *Figure:* captions translate the note's own captions.

## Mismatches to flag (figures not changed)

1. **F3 wording.** The English F3 image and its alt in `figs/index.md` say *"Not the same 'graph' as in Functions."* The Japanese means "not the graph of a (mathematical) function" (関数のグラフ), not Palantir Functions. I corrected the **alt text and caption** in `note_en.md` only; the image still carries the misleading wording. Needs a figure fix if HAGINO agrees.
2. **`figs/index.md` title.** It names the note as オントロジーは「意味の設計図」, which is not the live title (「PIVOTで話した「オントロジー」と、話しきれなかったこと」).
3. **Tables as Markdown.** Substack doesn't render Markdown tables natively, so the two tables need images or manual layout when pasting.

## Judgment calls

- **PIVOT naming (HAGINO's steering):** English readers don't know PIVOT, so the body says "a Japanese business TV show" / "the show". "PIVOT" survives only in the top note's quoted Japanese title and in the source list ("PIVOT (a Japanese business video show)"), where it's needed to identify the link.
- **Top note** says this is an English version, links the original, and gives its date.
- **Commenters' words stay inside blockquotes**, including continuation lines and the "(name, comment on the show's website, excerpt)" attributions, so they are not read as my own words.
- **Commenter handle** とんでもない子 romanized as "Tondemonaiko".
- **Palantir `/docs/jp/` links kept unchanged**, as in the original. English equivalents exist at the same paths under `/docs/` (several are already in the source list); swap them if preferred for an English audience.
- **Japanese-titled sources** are marked "(Japanese, title translated)" or "(Japanese)". Note embed URLs on their own line are kept so Substack can auto-embed them.
- **Glossary (shared with the Tech Blog article):** 意味の設計図 = "blueprint of meaning"; 実行条件 = "submission criteria"; 動かす部品 = "components that make things happen" (short form "moving parts"); 提案はAI、承認は人 = "AI proposes, humans approve"; 未公開・未査読 = "unpublished and not peer-reviewed"; 書き戻し = "writeback".
- HTML comments (source comment, figure placeholders) were removed from `note_en.md` for clean pasting; the mapping lives in this README and in `note_ja.md`.

## Before publishing

- HAGINO picks the title and decides on the F3 figure fix.
- Turn the two tables into images (or lay them out manually) in Substack.
- Publish only when separately authorized.
