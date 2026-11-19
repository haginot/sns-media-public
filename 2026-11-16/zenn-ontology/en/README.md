# Canly Tech Blog ontology article — English edition

**Status: DRAFT — NOT PUBLISHED.** Prepared for Substack; do not treat this GitHub copy as a Substack publication. No Substack or X post has been made as part of this translation task.

Prepared: **2026-11-19 (JST)**
Author: **Takahiro Hagino (萩野貴拓), CAIO / Chief AI Officer at Canly (カンリー)**

## Source of truth

- Original Japanese article: [【PIVOTでオントロジーを解説しました】PalantirのFoundry OntologyはDDDのドメインモデリングとして読めるという話](https://zenn.dev/canly/articles/121db874319244)
- Published Japanese article date: **2026-11-17 (JST)** (Zenn's public article metadata). The Japanese article says its sources and local test results were checked on **2026-11-16 (JST)**. These are different dates; the English version keeps the original source-check date.
- Canonical source file supplied for translation: `/workspace/zenn-ontology-20261116/zenn_body_v8.md`
- Reference copy in this folder: [`zenn_body_v8.md`](zenn_body_v8.md)
- SHA-256 of that Japanese source copy: `aa722c419ff424238499819b55422e9b3f8ced8cdaf5410fb6c60b52c2053bf5`
- Earlier `v5`–`v7` and `article.md` were **not used** as translation sources.

## Files

| File | Purpose |
|---|---|
| [`article_en.md`](article_en.md) | English Substack-ready Markdown draft. Author's first-person voice; original inline links and unnumbered reference list. Image URLs still point to the current Japanese figures. |
| [`figures_text_en.md`](figures_text_en.md) | Full visible Japanese text and English renderings for figures 1–7, with each current image URL, layout notes, and uncertainties. |
| [`zenn_body_v8.md`](zenn_body_v8.md) | Unmodified canonical Japanese source, for reference and comparison. |
| [`README.md`](README.md) | Source, dates, status, review notes, and publication handoff. |

## Translation and review

- Primary translation: Claude Code (`claude -p`, Opus), using the authenticated box session, section by section.
- Review: Grok Bot (コーディングの使い手) compared all 12 translated chunks against the canonical Japanese, paragraph by paragraph / line by line, then corrected terminology, a few over-specific phrasings, and formatting.
- Mechanical checks: all **31 code blocks** present. Executable code and Japanese string literals inside them are unchanged; only Japanese comments and Mermaid diagram labels were translated. All original URLs are present. All seven figure image URLs match the Japanese source. Source copy verified by SHA-256.
- Figure review: all seven published PNGs were downloaded and opened. Visible text was read directly, then cross-checked with the working figure HTML. The PNGs are byte-identical to the local image copies.
- Word count: **12,418 whitespace-delimited words/tokens** for all of `article_en.md` (includes code and references); **11,297** excluding fenced code blocks; **10,880** for body prose before References, excluding code and URL targets. The count is approximate for English prose because code, identifiers, and Japanese string literals are present.

## Translation judgment calls / things for final editorial review

1. **"Can be read as" DDD domain modeling**, not "is the same as." The distinction is explicit in the title and Section 3.
2. **実行条件 → "submission criteria"** throughout, matching Palantir's official English term that the original pairs it with in §4.2. A parenthetical in §4.2 notes that the Japanese original says 実行条件 (literally "execution conditions"). This does not imply the local demos are Foundry implementations.
3. **"Harness" and "defense-grade" (国防レベル) are Hagino's own terms**, not Palantir terminology. Both disclaimers stay explicit.
4. **Code is quoted, not localized.** Zenn-style fence titles (e.g. `js:path（7〜12行目）`) became italic lines above plain fences, for Substack. Japanese UI labels, error messages, and data values inside code stay as written; a note at the top says so. Japanese code comments and the Mermaid labels are translated. Substack does not render Mermaid or Markdown tables natively, so these need manual handling (image or reformat) when pasting.
5. **マスター → "master"** (authoritative source of a value), kept consistently instead of "system of record".
6. **番組 → "show" / "episode"** depending on context; 出演者 → "guest" / "cast member"; 予約 → "booking".
7. **Translated titles in the reference list** are marked "(Japanese; title translated)". The English H1 title is a translation of the Zenn title and should be confirmed by Hagino before posting.
8. **Experiment caveats are retained**: unpublished, not peer-reviewed; 2,117 runs; a single fictional business; 25.7–49.3 points is the effect of providing knowledge, not ontology form; +2.3 points and p=0.0027 in the main analysis; ≈2.0 points and not significant after correction in the conservative analysis; all 137 invalid plans blocked only on the newly prepared tasks; gates are not substitutes for knowledge. None is generalized to PIVOT operations.
9. **Original figure inconsistencies left unchanged** (see `figures_text_en.md`): figure 4 has six steps while its caption lists five; figure 6 simplifies the timing of `check_plan` relative to approval; figure 7 has −0.5 for Experiment II only in the image, not in the article body. These are not translation changes. Do not change them without editorial approval.
10. **This is a long technical piece** (~10.9k body-prose words plus code and references). It has not been shortened, split, or editorially rewritten, because that would risk losing caveats. Substack formatting and email length may merit a later editorial pass.

## Figure inventory

1. **fig1** — scope of "ontology" (W3C vs. Foundry)
2. **fig2** — inference vs. validation
3. **fig3** — type layer vs. instance layer
4. **fig4** — action flow and permissions / "harness"
5. **fig5** — research repository architecture and data provenance
6. **fig6** — AI proposes, humans approve
7. **fig7** — knowledge provision vs. ontology-form effects

The English figure artwork has **not** yet been created; `figures_text_en.md` is the illustrator handoff. The images embedded in `article_en.md` are still the existing Japanese PNGs at immutable raw.githubusercontent.com commit URLs.

## Before publishing

- Final author/editor review of English wording.
- Produce English figures from `figures_text_en.md`, verify every number/caveat, and update image links.
- Paste/import into Substack and check code fences, tables, inline citations, and the Mermaid block. Some Markdown elements may need manual layout adjustment in Substack's editor.
- Publish only when separately authorized in the actual Substack workflow. No publish action was requested of this executor task.
