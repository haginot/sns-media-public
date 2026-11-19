# English cover banner — Foundry Ontology Through a DDD Lens

Canly Tech Blog cover, English version of the Japanese `banner/final_v4` (commit `be6acc8`).

Layout, palette and isometric diagram match the Japanese final: Unbounded **DDD** in a gradient box, one rotated `skos:closeMatch` label on the top arrow (ObjectType → Entity), the other two arrows unlabeled, no legend. The Japanese show thumbnail and its source credit were removed so the English banner has no logos, no show name, and no Japanese characters.

## Text on the banner

- Kicker: I talked about ontology on a Japanese business TV show
- Title line 1: Foundry Ontology
- Title line 2: Through a DDD Lens
- Ruby under the DDD box: Domain-Driven Design
- Footer: Canly Tech Blog
- Diagram labels (unchanged English terms): OntologyConcept, ObjectType, LinkType, ActionType, Entity, Association, Command, DDDConcept, skos:closeMatch

Approved title (HAGINO): **Foundry Ontology Through a DDD Lens**.

## Files

- `banner_en_1600x900.png` / `banner_en_1200x675.png` — published images
- `banner_en.html` — source (with `zkit.css`, `zban.css`, `zban_head.js`, `iso.js`, `zlib.js`, `fonts/`)
- `render_banner_en.py` — Playwright render to both sizes

```bash
python3 render_banner_en.py
```

Fonts: Inter Tight (title, kicker, footer, ruby), Unbounded (DDD), IBM Plex Mono (diagram labels).
