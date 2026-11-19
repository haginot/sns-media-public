# Fact-check: muse-techblog English version (Canly Tech Blog)

- Rechecked: 2026-11-19 (JST). Original sources checked by the article: 2026-11-09 (JST).
- Rule: the English article keeps facts **as of 2026-11-09**. Nothing silently updated. Decide per item below.
- JA -> EN machine checks: all numbers, all URLs, all 4 code/JSON blocks identical, 26 figure slots preserved. Footnote markers removed and replaced by inline links + unnumbered Sources list.

## A. Outdated or now inaccurate (decision needed)

1. **Poppy is "draft 0.4" (section 4.1, section 7, fig14 "Draft 0.4", fig26 "Poppy is at draft 0.4").** Poppy **v1.0 was released on 2026-11-13** (Sierra, https://sierra.ai/blog/releasing-poppy). https://personalagentprotocol.org/docs/spec now serves v1.0 ("It's 0.4 with the fixes implementers needed"). The 0.4 text is still at https://personalagentprotocol.org/docs/0.4/spec . Suggest: add an update note and point "draft 0.4" links to /docs/0.4/spec.
2. **"The only primary source for Muse and Poppy working together is a demo at a Sierra event; not available to the general public" (section 5.5; fig01 "Availability in Muse unconfirmed (only demoed at a Sierra event)").** Outdated since 11/13: Sierra says "Poppy is now on for everyone who uses Muse, Meta's AI agent, which automatically looks for Poppy first on every site it visits", and Shopify enabled Poppy for every merchant. (Source is Sierra, not Meta.)
3. **"No formal link between Poppy and UCP is defined" (section 5.5, section 7, fig24/fig26).** Partly outdated: v1.0 is "largely built with existing standards like MCP, OpenAPI, and UCP", adds extensions incl. "the commerce extension co-authored by Shopify", every Shopify store "automatically publishes a Poppy file", and Sierra says "UCP and Poppy complement each other" (same Sierra post). The v1.0 spec also lists UCP endpoints among entry points. Whether a Poppy session formally calls UCP checkout was not confirmed in this recheck.
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
- Byline "HAGINO, CAIO at Canly" (fig03 byline pill: "Canly Tech Blog | HAGINO (CAIO, Canly)"). English company name confirmed as "Canly" and the blog as "Canly Tech Blog" by HAGINO (2026-11-19 12:44 JST); consistent with the official site biz.can-ly.com and zenn.dev/canly.
- "(lol)" in the original intro dropped for English tone.

## Addendum (2026-11-19 12:25 JST, from AIO総合研究所)
- Poppy: the spec reached v1.0 on 11/13, but as of 11/19 12:00 JST the merchant-side `poppy.json` on the 7 domains AIO tracks (including Shopify and Mercury) still declares 0.4. If the figures/text are updated, write it as "the spec is 1.0, but most merchant implementations are still on 0.4", not "Poppy is now 1.0 everywhere".
