# meta: muse-note (English)

- Status: DRAFT, not published anywhere. Publishing on Substack needs HAGINO's OK and his Substack sign-in.
- Original (Japanese, note, published 2026-11-13 09:39 JST): https://note.com/haginota/n/nba922eb92cd9
  - Original title: 「YouTube20万回再生、PIVOT週間1位。嬉しい声と、まだ残る不安。PIVOTのコメントに答えます」
- Policy applied (HAGINO, 2026-11-19): no "PIVOT" anywhere (called "a Japanese business TV show" on first mention, team wording / "the show"); native fluency first, facts/numbers/URLs unchanged.
- The ranking link still points to pivotmedia.co.jp (URL only, not named).

## Title (proposed)
200,000 Views and a No. 1 Week: Your Questions About Meta's Muse, Answered

Alternatives:
- What You Asked Me About Meta's Muse After My TV Appearance
- "Just Because It's Meta, I Don't Trust It": Answering 40 Comments About Muse

## Subtitle (proposed)
The praise, the worries that remain, and what Meta's public documents actually say about Muse's ads, data, security, and shopping.

## Cover image (Substack social preview)
The Japanese note eyecatch has Japanese text and a show thumbnail, so it is NOT reused. Suggested cover: fig01
https://raw.githubusercontent.com/haginot/sns-media-public/fca3d9cbdb1c8eec54deb0ea83144b5ed8bd17df/2026-11-19/muse-en/note/figures/fig01.png

## Video
The article embeds the episode on YouTube: https://www.youtube.com/watch?v=NvNLJjozcJo (paste the bare URL on its own line in Substack to embed).

## Figures and alt text (images are public, pinned to sns-media-public commit fca3d9cbdb1c8eec54deb0ea83144b5ed8bd17df)
Base: https://raw.githubusercontent.com/haginot/sns-media-public/fca3d9cbdb1c8eec54deb0ea83144b5ed8bd17df/2026-11-19/muse-en/

| # | file | alt text |
|---|---|---|
| fig01 | `note/figures/fig01.png` | Diagram contrasting the current absence of ads with guarantees about the future |
| fig02 | `note/figures/fig02.png` | Diagram sorting out revenue, ads, and training, reading "no ads now" separately from any guarantee about the future |
| fig03 | `note/figures/fig03.png` | Diagram showing the three analogies (dedicated cloud PC, permit, watchdog) aren't safety guarantees; only purchases are stated to need confirmation every time |
| fig04 | `note/figures/fig04.png` | Diagram of isolation vs. permission management: your PC and the dedicated cloud VM are separate, but operating permissions on connected services remain |
| fig05 | `note/figures/fig05.png` | Diagram: isolation differs from permission management, Sentinel judges connector actions and outbound traffic, and only purchases are confirmed every time |
| fig06 | `note/figures/fig06.png` | Diagram: instructions on external pages are untrusted input handled with layered defenses; page instructions aren't the user's permission; defense isn't complete |
| fig07 | `note/figures/fig07.png` | A 10-item checklist for users, based on developer guidelines; Muse may not behave this way in every situation |
| fig08 | `note/figures/fig08.png` | Diagram: sending a request differs from confirming a booking; distinguish quote, pending, and confirmed. A developer requirement, not a guarantee on every path |
| fig09 | `note/figures/fig09.png` | Diagram: single-use card numbers apply to Muse Wallet on first-time sites; why Amazon blocks; UCP listing ≠ Muse acceptance; Meta hasn't said Muse uses UCP |
| fig10 | `note/figures/fig10.png` | Diagram of overlap between Muse and existing agents, and experience differences that don't show up in feature tables (author's analysis) |
| fig11 | `note/figures/fig11.png` | Venn diagram of Muse, OpenClaw, and Hermes overlap, with experience absent from feature tables shown below an iceberg's waterline |
| fig12 | `note/figures/fig12.png` | Diagram of how personal information is handed over at the end of a purchase |
| fig13 | `note/figures/fig13.png` | Sharing passwords vs. Poppy's proposed scoped permissions. Web Bot Auth only proves the key holder's signature. A proposed spec, not evidence Muse adopts it |
| fig14 | `note/figures/fig14.png` | Diagram mapping person → app → service on smartphones to Muse → connector → service for agents (author's analysis) |
| fig15 | `note/figures/fig15.png` | Diagram mapping people, apps, and services to Muse, connectors, and services |
| fig16 | `note/figures/fig16.png` | Diagram explaining the chasm and network effects (author's analysis) |
| fig17 | `note/figures/fig17.png` | Diagram of the chasm and network effects |
| fig18 | `note/figures/fig18.png` | Diagram: Model API prompt caching makes tokens cheaper and faster without removing them; whether the Muse app caches or counts it toward limits is unconfirmed |
| fig19 | `note/figures/fig19.png` | Diagram: users check what they connect, permit, and what got done; hypothesis that AI-friendly entry points may set services apart (author's analysis) |

Source slides (HTML/CSS) and renderer: sns-media-public `2026-11-19/muse-en/{note,techblog}/figures/src/` (earlier copy: `2026-11-19/substack-en/_src/`, commit d4c0ed3).
Mapping to original Japanese sources: fig01=sT21, fig02=s06, fig03=09-three-analogies, fig04=sO2, fig05=s02, fig06=sT38, fig07=s08, fig08=sT40, fig09=s07, fig10=s01, fig11=sT02, fig12=sT31, fig13=03-poppy-identity-v5_1, fig14=s04, fig15=sT18, fig16=s05, fig17=sT19, fig18=10-cache-boundary, fig19=11-service-entry
