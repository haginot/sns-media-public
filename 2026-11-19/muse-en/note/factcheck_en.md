# Fact-check: muse-note English version

- Rechecked: 2026-11-19 (JST) against primary sources reopened that day. Raw page captures are not committed (copyright); URLs below.
- Rule followed: the English article keeps the facts **as of the original's dates** (sources checked 11/9, 11/10, 11/13, 11/16 JST). Nothing was silently updated. Items below are for HAGINO to decide (add an "Update, Nov 19" note, change, or leave). Items 1–2 were applied on 2026-11-19 at HAGINO's request (see "Update applied" at the end).
- Numbers, dates, URLs and figure facts were machine-compared JA -> EN (all numbers and all 50+ URLs preserved; 19 figure slots preserved).

## A. Outdated or now inaccurate (decision needed)

1. **[Applied 11/19, see end] Figures still say Poppy is "a draft" and "general use in Muse unconfirmed" (fig03, fig13).** The body text was already updated on 11/16 for Poppy v1.0, but the two figures were not. Sierra, 2026-11-13: v1.0 released; "Poppy is now on for everyone who uses Muse ... automatically looks for Poppy first". https://sierra.ai/blog/releasing-poppy
   - English figures were translated as-is (draft wording kept). Suggest: redraw fig03/fig13 badges to "v1.0 (Nov 13)" / "On for all Muse users (per Sierra)", and drop "does not indicate Muse adopts it" on fig13.
2. **[Applied 11/19, see end] "Poppy spec draft" links now open v1.0.** https://personalagentprotocol.org/docs/spec now shows Version 1.0 ("0.4 with the fixes implementers needed"). The draft the article describes is at https://personalagentprotocol.org/docs/0.4/spec . Suggest switching the link to /docs/0.4/spec where the text says "draft".
3. **Voice ("real-time voice isn't available" section).** The article says the author has no document to state the status. Since then: Meta rolled out voice + avatars in the Muse app **in the US** on 2026-11-05 (https://about.fb.com/news/2026/11/introducing-muse-ai-voice-expressive-avatars/) and in **Canada** on 2026-11-18 (https://about.fb.com/news/2026/11/meta-welcomes-loblaw-as-first-canadian-retail-partner-to-muse/). For Japan, Meta's 10/23 Japanese release says availability "will be announced separately" (https://about.fb.com/ja/news/2026/10/muse-personal-ai-agent-launches-in-japan/). No Japan date found.

## B. Still correct, with useful new context (optional update)

4. **Amazon block (section 3).** Still blocked. New: Muse's shopping skill now tells it "Do not search Amazon" / "leave out Amazon unless the user asks for it" (GeekWire, 2026-11-17, https://www.geekwire.com/2026/do-not-search-amazon-metas-muse-now-shops-elsewhere-by-default/). Amazon CEO Andy Jassy (11/17, Semafor event): "I don't think that we've said we're not going to open it up" if it's a good experience and "a fair exchange of value" (Business Insider, https://www.businessinsider.com/amazon-ai-shopping-agents-muse-instinct-dots-2026-11). The article's "no public commitment on when the block might be lifted" remains true.
5. **Muse privacy policy was revised (effective 2026-11-16).** Re-read https://muse.ai/privacy : the claims used (no sharing of conversations/VM data with Meta ad systems; training setting on by default and can be turned off; removes "names, email addresses, phone numbers and Social Security Numbers" and disassociates from account; Confidential VM "in the future") are all still consistent.
6. **Muse Confidential VM** still not launched as of 11/19 (privacy policy: "In the future..."; no Meta launch post found). Article's statement stands.
7. **Phone calls (not in article).** Muse can now call US businesses for **paid subscribers in the US** from 2026-11-12 (TechCrunch, https://techcrunch.com/2026/11/12/muse-can-now-place-calls-to-u-s-businesses-if-you-pay/ ; Alexandr Wang's post). Not available in Japan per reports. Pricing quoted there: Power $20/month (500M Muse tokens/week), Maximum $100/month (3B tokens).
8. **Availability (not in article beyond Japan).** US 2026-09-08, Canada 2026-09-18 (Muse on X), Japan 2026-10-23, Singapore 2026-10-28 SGT (Meta newsroom post dated 10/27). Japan = first market outside North America: still correct.
9. **Grok Bot plans (dots/Grok Bot comparison).** docs.x.ai now also lists linking **SuperGrok Plus, SuperGrok Heavy** and a self-serve **Grok Business** seat, besides SuperGrok and X Premium+ (https://docs.x.ai/grok-bot/get-started). Article is not wrong, just less complete.
10. **Model behind Muse (not claimed in the note).** FYI for consistency with the tech blog: on 2026-11-06 Meta rolled out "specialized versions of our existing models, trained using Muse Wonder" to Muse users (https://research.meta.ai/blog/specialized-models-for-muse-and-metaai).

## C. Could not re-verify today (page blocks bots or is JS-rendered)

- Axios 2026-09-08 ("no ads"), GeekWire Amazon block (Sep), OpenAI dots pages, Meta Q3 earnings transcript (medianama PDF fetched OK; investor page 403), Stripe Shared Payment Tokens country list (JS-rendered; Japan support status as of 11/8 not rechecked), Meta help page on Muse tokens (JS-rendered). Claims kept as written.
- YouTube view count (205,746 as of 11/12 14:00 JST) and the weekly ranking are dated snapshots; not updated.

## D. Translation/editorial choices to confirm

- "PIVOT" removed everywhere per HAGINO's policy. The ranking source link still points to pivotmedia.co.jp (URL only). The comment links still go to the YouTube episode.
- Author shown as "HAGINO (CAIO, Canly, Inc.)" (HAGINO 2026-11-19 13:26 JST: formal company name "Canly, Inc."; "Canly" alone on later mentions; blog stays "Canly Tech Blog"). No first-name romanization was used (I didn't confirm the official spelling). English company name confirmed as "Canly" and the blog as "Canly Tech Blog" by HAGINO (2026-11-19 12:44 JST); consistent with the official site biz.can-ly.com and zenn.dev/canly.
- Japanese-only services are glossed briefly (e.g. "note (a Japanese blogging platform)").

## Addendum (2026-11-19 12:25 JST, from AIO総合研究所)
- Poppy: the spec reached v1.0 on 11/13, but as of 11/19 12:00 JST the merchant-side `poppy.json` on the 7 domains AIO tracks (including Shopify and Mercury) still declares 0.4. If the figures/text are updated, write it as "the spec is 1.0, but most merchant implementations are still on 0.4", not "Poppy is now 1.0 everywhere".

## Update applied (2026-11-19 13:30 JST, per HAGINO 13:26 JST: "redraw the outdated figures to current facts")

### Primary sources rechecked just before drawing
- Poppy spec page https://personalagentprotocol.org/docs/spec : HTTP 200, "Personal Agent Protocol specification (version 1.0)"; "This is version 1.0. It's 0.4 with the fixes implementers needed." 0.4 text still at https://personalagentprotocol.org/docs/0.4/spec (200). Checked 2026-11-19 13:27 JST.
- Sierra "Releasing Personal Agent Protocol 1.0" (2026-11-13) https://sierra.ai/blog/releasing-poppy : "v1.0 of the protocol is now available"; "Shopify has enabled Poppy for every merchant"; "Poppy is now on for everyone who uses Muse ... automatically looks for Poppy first on every site it visits"; the Shopify-co-authored commerce extension "links the two protocols" (Poppy and UCP). Reread 2026-11-19 13:28 JST.
- `https://{domain}/.well-known/poppy.json`, fetched 2026-11-19 13:27 JST: allbirds.com, kith.com, colourpop.com, gymshark.com (Shopify US), jp.kith.com, mini-mal.tokyo (Shopify JP), app.mercury.com: all HTTP 200, `protocol_version` "0.4". Same result as AIO's 12:00 JST run (aio-research `research/2026-11-19-light-collection-1200/observations/poppy-json-1200.tsv`). Nothing has changed since then. These 7 sites are a non-random sample.
- v1.0 still has the points the figures use: pairwise User IDs per Company (5.1); Session JWT `htm`/`htu` = method and URL without query or fragment; "A Personal Agent SHOULD also sign requests ... using Web Bot Auth".

### Figures
- fig03 (`09-three-analogies`), Permit slip card: stamp "DRAFT" -> "v1.0"; "Poppy is still a draft / General use in Muse unconfirmed" -> "Poppy spec v1.0 since Nov 13 / Most sites still serve 0.4"; source line "Personal Agent Protocol draft spec" -> "Personal Agent Protocol spec v1.0 / poppy.json on 7 sites (checked Nov 19, 2026)".
- fig13 (`03-poppy-identity-v5_1`): headline "Proposal: scoped permission, not passwords" -> "Poppy: scoped permission, not passwords"; "Poppy proposal" -> "Poppy v1.0"; stamp "Draft" -> "v1.0"; "General use in Muse: unconfirmed" -> "Most sites still serve 0.4"; "Web Bot Auth (signature the Poppy draft recommends)" -> "(signature Poppy 1.0 recommends)"; key point "A proposed standard; it does not indicate Muse adopts it" -> "On for all Muse users (Sierra); 7 sites checked still serve 0.4"; source line updated (Sierra Oct 6 intro + Nov 13 v1.0 release, spec v1.0, poppy.json on 7 sites).

### Text near the figures
- Section 6 (Poppy): "The explanation and figure below are based on the spec as I read it at the draft stage. I haven't checked here whether anything changed in v1.0." -> "I first wrote the explanation below from the draft spec. I've since rechecked these points against v1.0 (November 19, 2026), and they still hold. One caveat: ... still publish version 0.4 in their poppy.json files." / "The draft gives you" -> "The spec gives you" / "Poppy spec draft" link label -> "Poppy spec v1.0" / "The Poppy draft also recommends" -> "Poppy 1.0 also recommends". fig13 alt text updated to match.
- Sources list: spec entry relabelled "version 1.0" and a "draft 0.4" entry added (/docs/0.4/spec).
- fig03's surrounding text already said v1.0 (HAGINO's 11/16 update); unchanged.

