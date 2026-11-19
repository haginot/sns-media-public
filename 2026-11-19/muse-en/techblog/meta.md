# meta: muse-techblog (English)

- Status: DRAFT, not published anywhere. Publishing on Substack needs HAGINO's OK and his Substack sign-in.
- Original (Japanese, Kanrii Tech Blog / カンリー Techブログ, published 2026-11-09 21:24 JST, body updated 22:39 JST): https://zenn.dev/canly/articles/d108f4bc26ceb7
  - Original title: 「【PIVOTでMuseを解説しました】番組では話しきれない、Museの本当はすごい技術解剖」
- Policy applied: no "PIVOT" (=> "a Japanese business TV show" on first mention, team wording), never "Zenn" alone (=> "Kanrii Tech Blog"), native fluency first.

## Title (proposed)
What I Couldn't Say on TV: A Technical Teardown of Meta's Muse

Alternatives:
- Inside Meta's Muse: Alignment, Sandboxing, and the Protocols Behind a Personal AI Agent
- Muse Under the Hood: An Engineer's Read of Meta's Primary Sources

## Subtitle (proposed)
Alignment evals, the Secure VM and Sentinel, the Poppy agent protocol, and UCP, read straight from Meta's and the specs' primary sources.

## Cover image
Suggested: fig01 (summary) https://raw.githubusercontent.com/haginot/sns-media-public/fca3d9cbdb1c8eec54deb0ea83144b5ed8bd17df/2026-11-19/muse-en/techblog/figures/fig01.png

## Figures and alt text
11 figures are animated GIFs (fig09, 10, 12, 15-22; 1200x675). Each also has a static final-frame PNG with the same name (.png) if Substack's GIF handling is a problem.

| # | file | alt text |
|---|---|---|
| fig01 | `techblog/figures/fig01.png` | Summary contrasting what was said on the TV show with this article: checking its analogies against primary sources on Secure VM, Poppy, and Sentinel. UCP is extra |
| fig02 | `techblog/figures/fig02.png` | Muse overview: client, per-user Secure VM, connectors and browser, limited inference and telemetry |
| fig03 | `techblog/figures/fig03.png` | What's public about training: five official sources and the areas they don't cover |
| fig04 | `techblog/figures/fig04.png` | The five pillars of the behavior principles and instruction priority (Meta → developer → user → environment) |
| fig05 | `techblog/figures/fig05.png` | Four evaluation configurations (Helpful / Muse Model / Muse / API), with a note on internal-interface evaluations |
| fig06 | `techblog/figures/fig06.png` | Key figures: MASK, Agentic Misalignment 0.0–0.60%, hallucination, principle-violation rates, and SHADE-Arena, with notes |
| fig07 | `techblog/figures/fig07.png` | Monitor scale mapped to the behavior taxonomy, with a note on evaluation limits |
| fig08 | `techblog/figures/fig08.png` | Secure VM's two zones: the runtime cell and host-side protection services |
| fig09 | `techblog/figures/fig09.gif` | Flow where Sentinel judges action requests and outbound traffic and swaps in proxy tokens; tainted context falls back to standard review |
| fig10 | `techblog/figures/fig10.gif` | Approvals happen in UI outside the chat. Grant scopes: once, session, task, time-limited, permanent; low-risk actions proceed without interruption |
| fig11 | `techblog/figures/fig11.png` | Layered defenses against the lethal trifecta, with deterministic boundaries |
| fig12 | `techblog/figures/fig12.gif` | Browser restrictions, approval for every purchase, and single-use cards |
| fig13 | `techblog/figures/fig13.png` | Data policy: no sharing for ads, training opt-out, Confidential VM planned |
| fig14 | `techblog/figures/fig14.png` | Spectrum of agent-access options, showing the middle ground Poppy fills |
| fig15 | `techblog/figures/fig15.gif` | poppy.json discovery and two-way domain/issuer verification |
| fig16 | `techblog/figures/fig16.gif` | Poppy sign-in (Direct/Device) and scope hints |
| fig17 | `techblog/figures/fig17.gif` | Delegated keys and Poppy-Session JWT. One-identity limit is operational; limits of §10.7 and Web Bot Auth |
| fig18 | `techblog/figures/fig18.gif` | Browser participation flow; access tokens never pass through the browser |
| fig19 | `techblog/figures/fig19.gif` | Conversation author.type, handoff to humans, excluded_tasks, and business content treated as data |
| fig20 | `techblog/figures/fig20.gif` | Overview of UCP consolidating N×N integrations into a common language |
| fig21 | `techblog/figures/fig21.gif` | UCP profile negotiation: only shared capabilities are used; signatures prove origin only |
| fig22 | `techblog/figures/fig22.gif` | Checkout state transitions: at ready_for_complete the platform calls Complete Checkout; requires_escalation hands off to the buyer via continue_url |
| fig23 | `techblog/figures/fig23.png` | UCP payment trust triangle: the platform never touches raw card data |
| fig24 | `techblog/figures/fig24.png` | Three layers (Muse internals, Poppy, UCP), distinguished by level of certainty |
| fig25 | `techblog/figures/fig25.png` | Implications for brick-and-mortar businesses: machine-readable entry points, labeled as analysis |
| fig26 | `techblog/figures/fig26.png` | Checklist of limitations and open questions |

Source slides (HTML/CSS) and renderer: sns-media-public `2026-11-19/muse-en/{note,techblog}/figures/src/` (earlier copy: `2026-11-19/substack-en/_src/`, commit d4c0ed3).
