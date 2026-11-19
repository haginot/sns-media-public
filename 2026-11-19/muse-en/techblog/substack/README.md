# Substack-ready English draft (Muse / Canly Tech Blog)

**Status: HOLD: fig24/5.5 pending — NOT PUBLISHED.** Nothing has been posted to Substack or X. This folder is a paste-ready package for Substack's editor, which does not render Markdown tables. Do not publish until fig24 and section 5.5 are confirmed.

Built from `../article_en.md` at commit `5cc4ee2` (image URLs already pinned to `60005e3`). The English title and subtitle were chosen by HAGINO at `702a962` (2026-11-19 13:37 JST, candidate 2). All 26 English figures (15 PNG and 11 GIF) are pinned to `60005e3`, which includes the redrawn Poppy figures (v1.0 since 11/13; 7 checked sites still serve 0.4, rechecked 11/19 13:27 JST) and the Canly, Inc. byline. Rendered table PNGs are in `images/`, with `raw.githubusercontent.com` URLs pinned to the commit that added those PNGs (see `manifest.json`). GIFs are kept as images; Substack supports GIF.

## Title and subtitle (Substack fields only — not in the body)

- **Title:** Secure VM, Sentinel, Poppy, UCP: Inside the Machinery of Meta's Muse
- **Subtitle:** An engineer's walk through Muse's alignment evals, sandboxing, approval gates, and the open protocols built for agents and businesses.

## HOLD: fig24 and section 5.5

fig24 and the wording in section 5.5 ("How Muse, UCP, and Poppy relate: what's known vs. what's guessed") may change pending HAGINO. Current fig24 URL, so it can be swapped later:

https://raw.githubusercontent.com/haginot/sns-media-public/60005e310347c83fd43fd0cc7bf0fa05aa9bb99d/2026-11-19/muse-en/techblog/figures/fig24.png

## Files

- `substack.md` — paste-ready Markdown
- `substack.html` — paste-ready HTML
- `manifest.json` — inventory of replaced tables, image SHA-256 and dimensions
- `images/` — 5 table PNGs (1600px wide)

Code blocks are left as code. Article wording, numbers, caveats, and code were not changed, except that markdown tables were replaced with images. Suggested cover / social image is fig01 (`60005e3`); it already appears in the body, so it is not repeated at the top. Samples of fig01, fig03, fig14, fig24, fig26, and fig09.gif were opened and checked (badge “Canly Tech Blog”; no Kanrii, no PIVOT, no xAI). Every figure and GIF URL returned HTTP 200.
