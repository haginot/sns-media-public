# Fact-check: muse-techblog English version (Canly Tech Blog)

- Rechecked: 2026-11-19 (JST). Original sources checked by the article: 2026-11-09 (JST).
- Rule: the English article keeps facts **as of 2026-11-09**. Nothing silently updated. Decide per item below. Items 1–3 (Poppy) were applied on 2026-11-19 at HAGINO's request (see "Update applied" at the end).
- JA -> EN machine checks: all numbers, all URLs, all 4 code/JSON blocks identical, 26 figure slots preserved. Footnote markers removed and replaced by inline links + unnumbered Sources list.

## A. Outdated or now inaccurate (decision needed)

1. **[Applied 11/19, see end] Poppy is "draft 0.4" (section 4.1, section 7, fig14 "Draft 0.4", fig26 "Poppy is at draft 0.4").** Poppy **v1.0 was released on 2026-11-13** (Sierra, https://sierra.ai/blog/releasing-poppy). https://personalagentprotocol.org/docs/spec now serves v1.0 ("It's 0.4 with the fixes implementers needed"). The 0.4 text is still at https://personalagentprotocol.org/docs/0.4/spec . Suggest: add an update note and point "draft 0.4" links to /docs/0.4/spec.
2. **[Applied 11/19, see end] "The only primary source for Muse and Poppy working together is a demo at a Sierra event; not available to the general public" (section 5.5; fig01 "Availability in Muse unconfirmed (only demoed at a Sierra event)").** Outdated since 11/13: Sierra says "Poppy is now on for everyone who uses Muse, Meta's AI agent, which automatically looks for Poppy first on every site it visits", and Shopify enabled Poppy for every merchant. (Source is Sierra, not Meta.)
3. **[Partly applied 11/19: update note in 5.5; fig24 unchanged] "No formal link between Poppy and UCP is defined" (section 5.5, section 7, fig24/fig26).** Partly outdated: v1.0 is "largely built with existing standards like MCP, OpenAPI, and UCP", adds extensions incl. "the commerce extension co-authored by Shopify", every Shopify store "automatically publishes a Poppy file", and Sierra says "UCP and Poppy complement each other" (same Sierra post). The v1.0 spec also lists UCP endpoints among entry points. Whether a Poppy session formally calls UCP checkout was not confirmed in this recheck.
4. **Model inside Muse (sections 1 and 2.1).** The article says the core is a Muse Spark 1.3 variant (true per the 10/23 evaluation report) and that "as of 2026-11-09, none of the sources I checked say the model inside Muse has switched to Wonder". But on **2026-11-06** (before publication) Meta announced "specialized versions of our existing models, trained using Muse Wonder", rolled out to Muse and Meta AI users (index 47% vs 38%; Active Memory 90% vs 76%) — https://research.meta.ai/blog/specialized-models-for-muse-and-metaai . Literally the "switched to Wonder" statement still holds (these are not Wonder itself), but readers may take "Muse runs Spark 1.3" as current. Suggest an update note.

## B. Still correct (rechecked)

5. Confidential VM: still "planned"/"in the future"; not launched as of 11/19 (https://muse.ai/privacy effective 2026-11-16; no Meta launch post).
6. Ads / training / PII removal / opt-out: consistent with the revised privacy policy (2026-11-16) and the safety blog.
7. Japan launch 2026-10-23, first market outside North America: correct. (For context: US 9/8, Canada 9/18, Singapore 10/28 SGT.)
8. US announcement still mentions WhatsApp (post updated 2026-11-10); Japanese announcement still doesn't.
9. Shopify "Selling on Meta": direct checkout shown in 11 countries incl. Japan; still correct (Australia, Brazil, Canada, India, Japan, Mexico, New Zealand, Singapore, South Korea, UK, US).
10. UCP: latest dated version is still 2026-08-25 (ucp.dev). MAINTAINERS.md still lists Meta and Amazon members.
11. Safety blog figures ($300,000 max bounty, $130,000 prompt injection etc.) unchanged on https://research.meta.ai/blog/security-and-safety-for-ai-agents-our-approach-with-muse .

## C. New since 11/9, not in the article (optional context)

- Voice + expressive avatars: US 2026-11-05, Canada 2026-11-18; Japan TBA.
- Phone calls to US businesses for paid US subscribers: 2026-11-12 (TechCrunch).
- Amazon: Muse's shopping skill now says "Do not search Amazon" (GeekWire 11/17).

## D. Could not re-verify today

- ppc.land analysis (403 to bots), IETF Web Bot Auth draft status beyond -01 (not rechecked for -02), evaluation-report numbers (static PDF; not re-extracted line by line — the English text was compared number-by-number against the Japanese article instead).

## E. Editorial choices to confirm

- No "PIVOT"; "Zenn" never used alone (publication = "Canly Tech Blog").
- Byline "HAGINO, CAIO at Canly, Inc." (fig03 byline pill: "Canly Tech Blog | HAGINO (CAIO, Canly, Inc.)"). HAGINO 2026-11-19 13:26 JST: formal company name "Canly, Inc."; "Canly" alone on later mentions; blog stays "Canly Tech Blog". English company name confirmed as "Canly" and the blog as "Canly Tech Blog" by HAGINO (2026-11-19 12:44 JST); consistent with the official site biz.can-ly.com and zenn.dev/canly.
- "(lol)" in the original intro dropped for English tone.

## Addendum (2026-11-19 12:25 JST, from AIO総合研究所)
- Poppy: the spec reached v1.0 on 11/13, but as of 11/19 12:00 JST the merchant-side `poppy.json` on the 7 domains AIO tracks (including Shopify and Mercury) still declares 0.4. If the figures/text are updated, write it as "the spec is 1.0, but most merchant implementations are still on 0.4", not "Poppy is now 1.0 everywhere".

## Update applied (2026-11-19 13:30 JST, per HAGINO 13:26 JST: "redraw the outdated figures to current facts")

### Primary sources rechecked just before drawing
- Poppy spec page https://personalagentprotocol.org/docs/spec : HTTP 200, "Personal Agent Protocol specification (version 1.0)"; "This is version 1.0. It's 0.4 with the fixes implementers needed." 0.4 text still at https://personalagentprotocol.org/docs/0.4/spec (200). Checked 2026-11-19 13:27 JST.
- Sierra "Releasing Personal Agent Protocol 1.0" (2026-11-13) https://sierra.ai/blog/releasing-poppy : "v1.0 of the protocol is now available"; "Shopify has enabled Poppy for every merchant"; "Poppy is now on for everyone who uses Muse ... automatically looks for Poppy first on every site it visits"; the Shopify-co-authored commerce extension "links the two protocols" (Poppy and UCP). Reread 2026-11-19 13:28 JST.
- `https://{domain}/.well-known/poppy.json`, fetched 2026-11-19 13:27 JST: allbirds.com, kith.com, colourpop.com, gymshark.com (Shopify US), jp.kith.com, mini-mal.tokyo (Shopify JP), app.mercury.com: all HTTP 200, `protocol_version` "0.4". Same result as AIO's 12:00 JST run (aio-research `research/2026-11-19-light-collection-1200/observations/poppy-json-1200.tsv`). Nothing has changed since then. These 7 sites are a non-random sample.
- v1.0 still has the points the figures use: pairwise User IDs per Company (5.1); Session JWT `htm`/`htu` = method and URL without query or fragment; "A Personal Agent SHOULD also sign requests ... using Web Bot Auth".

### Figures
- fig01 (`s00b`), Poppy row: "Availability in Muse unconfirmed (only demoed at a Sierra event)" -> "v1.0 since Nov 13; on for all Muse users, per Sierra". (UCP row "adoption in Muse unconfirmed" kept: Meta still hasn't said Muse checks out via UCP.)
- fig14 (`s14`): chip "Draft 0.4" -> "v1.0 (Nov 13) · most sites still on 0.4"; source "[poppy] draft 0.4" -> "[poppy] v1.0 (this section reads 0.4/0.3) / [sierra] / poppy.json on 7 sites, Nov 19".
- fig26 (`s26`), item 4: "Poppy is at draft 0.4" [Draft] -> "Poppy spec is v1.0, but most sites still serve 0.4" [Migrating]. Item 6 "Meta has not stated that Muse uses UCP" kept (still true).
- fig03 (`s03`) byline pill -> "Canly Tech Blog | HAGINO (CAIO, Canly, Inc.)" (company-name decision, not Poppy).

### Text near the figures
- 4.1: added "Update (November 19, 2026)" note after the "current working draft is 0.4" paragraph (v1.0 released 11/13, spec page now serves it, this section still describes 0.4/0.3, the 7 sites checked still publish 0.4). The original sentence is kept, since it was true as of 11/9.
- 5.5: added an "Update (November 19, 2026)" note after "only ... a demo at a Sierra event" (Sierra: on for everyone who uses Muse; Muse looks for Poppy first; Shopify publishes Poppy for every store; commerce extension links Poppy and UCP; Meta itself still hasn't said Muse checks out via UCP).
- 7 (Limits): "Poppy is at draft 0.4" -> "Poppy's spec reached v1.0 on November 13, but the business sites I checked on November 19 still published version 0.4 in their poppy.json files" (links: Sierra v1.0 post, /docs/0.4/spec).
- Closing note: "Poppy is a draft" -> "Poppy reached v1.0 on November 13 (Poppy points updated November 19)".
- Sources: draft 0.4 entry now points to /docs/0.4/spec; added "specification (version 1.0)" and Sierra "Releasing Personal Agent Protocol 1.0".
- Not changed: fig24 and the 5.5 sentence "none of the sources I checked define a formal link between the specs". The new 5.5 note covers this. A redraw of fig24 was not requested.

