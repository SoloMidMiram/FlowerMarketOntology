# Deep Research prompt for FlowerMarketOntology

Research and propose an evidence-backed upgrade to FlowerMarketOntology, a Persian-first plant knowledge base with an English edition and a future flower shop. Study the plants and cut flowers themselves, the language sellers use to describe them, and the way flower sites present them to buyers. Return an import-ready research package and design recommendations.

## Start from the project baseline

Read `README.md`, `knowledge-map.md`, `blueprint.md`, `research-roadmap.md`, `taxonomy.json`, `ontology.py`, and the three batches under `research/batches/` if supplied. Identify which findings are new, which confirm earlier work, which conflict with it, and which gaps remain. If files are unavailable, state the limits of the comparison. Preserve stable IDs where they exist. Treat the existing pothos profile as a draft, «برگ‌انجیری» as ambiguous, and «بابا آدم» as unresolved at species level.

## 1. Upgrade the plant and flower knowledge

- Complete the evidence package for golden pothos / «پتوس طلایی» first. Verify the identity, link each care claim to an exact passage, and propose reviewed wording in Persian and English. Cover light preference versus tolerance, watering triggers, humidity, substrate and repotting, and animal-specific toxicity. Record where sources disagree and how the conditions affect applicability. If suggesting an image, identify the exact asset and its credit, license, and reuse scope.
- Add a focused comparison set of four to six houseplants, prioritizing «سانسوریا»، «زاموفیلیا»، «برگ‌انجیری» and «بابا آدم». Document scientific names and synonyms under named authorities, Persian and English trade names, diagnostic traits, lookalikes, and identification precision. Distinguish documented cultivar names from appearance terms such as «ابلق». Record unresolved candidates with the evidence needed to tell them apart.
- Add three to five cut-flower types such as rose, gerbera, tuberose and lily. For each, record commercial and botanical identity at the supported rank, common selling forms, vase care, and condition-dependent vase-life evidence where available. Keep vase care distinct from care for the living plant. Treat missing data as unknown.
- Prefer botanical authorities for identity, horticultural institutions and primary studies for care and postharvest claims, and specialist references for toxicity. Cite the specific page or passage for each proposed claim. Keep seller care and marketing language as retail evidence.

## 2. Compare market descriptions

- Prioritize Tehran and include at least one seller elsewhere in Iran. Start with Tarhegol, Nargil, VIPShop and Sarinaland where accessible. Use U.S. and U.K. benchmarks for both houseplants and florist gifting, and include one Canadian or Australian comparison if it adds a distinct pattern. Report seller counts by market and segment. Treat the sample as qualitative.
- Compare how sellers title and describe similar plants or flowers. Capture original Persian or English labels, qualifiers, variants, height and pot dimensions, stem count and selling unit, appearance, care badges, photo type, gift occasion, arrangement format, ingredients and substitution terms. Where present, record displayed price and currency unit, delivery coverage and timing with the date and applicable product or channel. Distinguish sellers from aggregators.
- Pick at least two matched examples, such as golden pothos across plant shops and a rose bouquet across florists. Compare equivalent page roles and record the evidence of equivalence. Explain which fields transfer across markets and which need local wording or a different commercial meaning.

## 3. Audit how sites present the information

- Inspect actual navigation, search results, collection pages, product cards, product details and any linked care guides. Sample mobile and desktop layouts where available. Use Playwright Global MCP when working in the Codex project. If a surface is inaccessible, record the failure and keep any indexed text labeled by its retrieval method.
- For each surface record visible labels and order, navigation path, filters, image role, care disclosure, delivery and substitution placement, and the main action. Distinguish what appears on the page from your design interpretation. Note where Persian RTL, scientific names, units or mixed scripts affect readability. Treat viewport inspection and user testing as different evidence.
- Propose a bilingual navigation tree and field order for four screens: plant directory, care profile, live-plant product detail and bouquet detail. For each, identify what belongs in the menu, a filter, a card, the first screen, or a detail section. Tie each recommendation to a buyer task and a captured example. Include expected search behavior for «پتوس طلایی»، «برگ انجیری»، «بابا آدم»، «نور کم» and «دسته گل رز».

## Return these deliverables

1. **Executive delta.** Summarize the most consequential additions, contradictions and remaining gaps. Identify what changes in the ontology, the site hierarchy and the next release.
2. **Evidence tables.** Provide a plant and care table, a bilingual retail vocabulary table, a seller and page audit, and a screen-level UI comparison. Keep original terms alongside proposed Persian and English display labels.
3. **Structured records.** Return JSON or JSONL grouped as evidence, identity treatments, aliases and candidate links, care claims and translations, seller observations, presentation observations, media candidates and search fixtures. Include a stable record ID, source URL, precise page or passage locator, date, capture method, market and locale where relevant, evidence status, editorial status where relevant, and scope. Propose a mapping to existing fields and flag schema changes. Leave absent values null and explain material gaps. Distinguish direct observations, reported findings and inferences. A citation token alone is insufficient.
4. **Prioritized next tranche.** Rank remaining research by release impact. For each item give the decision it unlocks, the evidence required, and a completion criterion. Call out work that needs field visits, permissioned photos, editorial approval or real mobile users.

Before delivery, check that each proposed care claim can be traced to a specific source, each seller term is scoped to its observed surface, and each UI recommendation is labeled as a proposal. Report what can inform the project immediately, what remains draft, and what evidence would justify publication.
