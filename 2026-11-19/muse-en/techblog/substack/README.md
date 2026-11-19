# Substack-ready English draft (Muse / Canly Tech Blog)

**Status: DRAFT — NOT PUBLISHED.** Nothing has been posted to Substack or X. This folder is a paste-ready package for Substack's editor, which does not render Markdown tables.

Built from `../article_en.md` at commit `1d72580` (5.5 closing sentence aligned with section 7 and fig24; image URLs already pinned to `0d474fd`). The English title and subtitle were chosen by HAGINO at `702a962` (2026-11-19 13:37 JST, candidate 2). All 26 English figures (15 PNG and 11 GIF) are pinned to `0d474fd`, which redraws fig24 and updates section 7 for the Poppy 1.0 ucp extension (formal Poppy-UCP link; Muse use unconfirmed; rechecked 11/19 13:43 JST). Rendered table PNGs are in `images/`, with `raw.githubusercontent.com` URLs pinned to the commit that added those PNGs (`f330f65`; see `manifest.json`). GIFs are kept as images; Substack supports GIF.

## Title and subtitle (Substack fields only — not in the body)

- **Title:** Secure VM, Sentinel, Poppy, UCP: Inside the Machinery of Meta's Muse
- **Subtitle:** An engineer's walk through Muse's alignment evals, sandboxing, approval gates, and the open protocols built for agents and businesses.

## Files

- `substack.md` — paste-ready Markdown
- `substack.html` — paste-ready HTML
- `manifest.json` — inventory of replaced tables, image SHA-256 and dimensions
- `images/` — 5 table PNGs (1600px wide)

Code blocks are left as code. Article wording, numbers, caveats, and code were not changed, except that markdown tables were replaced with images. Suggested cover / social image is fig01 (`0d474fd`); it already appears in the body, so it is not repeated at the top. fig24 was opened and checked against the previous version: the footer now states the formal v1.0 ucp-extension link and that Meta has not said Muse checks out via UCP. Samples of fig01, fig03, fig14, fig24, fig26, and fig09.gif were opened and checked (badge “Canly Tech Blog”; no Kanrii, no PIVOT, no xAI). Every figure and GIF URL returned HTTP 200.
