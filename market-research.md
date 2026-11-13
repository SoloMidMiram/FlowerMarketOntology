# How flower sellers organize their catalogs

Research date: 11 November 2026. This is a qualitative benchmark. A seller's menu shows the language and paths it chose; it does not establish national demand, popularity, or market share.

## Findings from the supplied report

The supplied report, `flower_knowledge_market_taxonomy_ia_research_2026-11-11.md`, expands the seller sample. These findings carry the status **reported** until the project captures page-level evidence. Use this list to prioritize checks and retain the earlier browser results below as a separate record.

| Market | Reported evidence | Design implication to test |
|---|---|---|
| Iran | [Tarhegol](https://tarhegol.com/shop/) groups plants by light. [Nargil](https://nargil.ir/ProductType/1/2/گیاهان-آپارتمانی/) spans plants and supplies. [VIPShop](https://vipshop.flowers/) combines arrangements and occasions. | Test «نور کم», «گل آپارتمانی», «باکس گل» and «ترحیم» as distinct entry points. |
| US | [Bloomscape](https://bloomscape.com/shop/shop-all-plants/) supports suitability discovery and [FTD](https://www.ftd.com/flowers/all) provides a florist comparison. | Test condition-based plant browsing and occasion-based gifting separately. |
| UK | [Patch](https://www.patchplants.com/collections/plants-all/) emphasizes space and care. [Bloom & Wild](https://www.bloomandwild.com/send-flowers/tagonly/occasions) introduces letterbox delivery. | Track delivery form independently from bouquet format. |
| Canada | [Foli](https://foli.ca/collections/) and [Plant Collective](https://plantcollective.co/) add living plant and seasonal shipping examples. | Date shipping restrictions and attach them to the seller or offer. |
| Australia | [The Jungle Collective](https://thejunglecollective.com.au/collections/indoor-plants) includes rooms, exposure and balcony cues. | Validate exposure when using room labels. |
| Netherlands | [Intratuin](https://www.intratuin.nl/kamerplanten) offers deeper group and size filtering. | Preserve Dutch labels as benchmark data. |
| India | [Ugaoo](https://www.ugaoo.com/collections/indoor-plants) includes growth forms and watering labels. | Capture watering labels as merchant observations and review care guidance separately. |
| UAE and Kuwait | [Plantshop.me](https://www.plantshop.me/ae-en/categories/indoor-plants) and [Floward Kuwait](https://floward.com/en-kw/categories.html) cover hot-climate plant merchandising and gifting respectively. | Audit market-specific conditions and delivery terms when regionalizing. |

The report also identifies Tehran’s Mahallati and Imam Reza/Khavaran markets. Treat them as leads for wholesale fieldwork on channels, selling units, and seasonality. Keep exact operating hours and stall counts out of stable reference data.

## First collection batch

The [12 November research report](research/sources/first-collection-batch.md) supplies newer research on Tarhegol, Nargil, VIPShop, a Mashhad seller channel, The Sill, Patch and Bloom & Wild. The [structured intake](research/batches/batch-01.json) records selected labels, supplied URLs, name candidates, draft care and search cases. It uses `reported` for this import because it relies on the report’s citations. The earlier direct Sill records in [observations.jsonl](observations.jsonl) cover the collection page and chooser. The new report discusses a product and shipping, so these surfaces support a comparison of coverage. A historical change audit needs matched pages and the original capture.

## Tehran execution update

The [execution intake](research/batches/batch-02.json) adds product, category, aggregator, policy, and social surfaces from the [execution report](research/sources/tehran-execution-update.md). The report records live retrieval on 12 November. The intake uses `reported` for those imports and records archive status separately. Sarinaland adds a Mahallat regional seller. Mahallati is a separate Tehran wholesale market. Imam Reza has repeated dated online unit examples, while Mahallati still has secondary unit evidence. The Sill trend remains unavailable pending a matched historical surface.

The [next tranche](research/batches/batch-03.json) recovers separate VIPShop product URLs for B133 and K133 and reports different substitution terms for each. Nargil's wholesale/project delivery wording has a separate scope from its household retail terms. The recovered Mashhad post 778 is a different message. The target pothos permalink remains missing. Mahallati seller leads advance recruitment for fieldwork, while Imam Reza's online lists remain a separate collection.

## Earlier direct browser audit

| Market | Indoor-plant seller | Florist benchmark | Evidence status |
|---|---|---|---|
| United States | [The Sill live plants](https://www.thesill.com/collections/live-plants) | [1-800-Flowers](https://www.1800flowers.com/) | The Sill catalog verified in a rendered snapshot; florist navigation returned `net::ERR_CONNECTION_CLOSED`. |
| United Kingdom | [Patch Plants](https://www.patchplants.com/) | [Interflora UK](https://www.interflora.co.uk/) | Patch navigation timed out; Interflora returned `net::ERR_CONNECTION_CLOSED`. |
| Canada | [JOMO Studio](https://jomostudio.com/) | Sample a Canadian national florist and an independent city florist | JOMO tab title recovered after navigation timed out; category evidence and florist sample pending. |
| Australia | [The Jungle Collective](https://www.thejunglecollective.com.au/) | Sample a national florist and a city florist | Jungle Collective returned `net::ERR_CONNECTION_CLOSED`; florist sample pending. |
| Iran, Persian (fa-IR) | [Golsetan](https://golsetan.com/) | [VIP Shop](https://vipshop.flowers/) | Golsetan returned `net::ERR_TIMED_OUT`. VIPShop’s tab title recovered and advertised free delivery in Tehran; service terms and categories were not verified. |

The Sill placed “Large & Giant Houseplants,” “Easy-Care Plants,” “Pet-Friendly Plants” and “Low-Light Tolerant Plants” under “Shop by category.” The collection also offered a chooser whose first step asks where the plant will live, and described filters for growing zone, light, growth rate and category. This supports using living conditions and buyer priorities as discovery routes while keeping a single plant library. It does not establish that other sellers use the same labels, or that growing zone belongs on an indoor-only site.

Verification limits: browser navigation reported `TimeoutError: browserBackend.callTool: Timeout 60000ms exceeded.` on several sites. Follow-up tab selection returned `TimeoutError: browserBackend.callTool: Timeout 30000ms exceeded.` A recovered tab title establishes only that the title was visible. Kew returned a browser challenge during the audit. The literature list is a reading queue; it is not a completed review.

## Cross-market vocabulary to test

The terms below are editorial candidates for the bilingual site and prompts for the next audit. They are not claims about what appeared on sites that failed to load.

| Buyer intent | English label | Persian label | What to model |
|---|---|---|---|
| Find a plant for an apartment | Houseplants / indoor plants | گیاهان آپارتمانی؛ گل آپارتمانی as search alias | Growing context, not a botanical rank |
| Find something that flowers indoors | Flowering houseplants | گیاهان آپارتمانی گل‌دار | Flowering behavior under indoor conditions |
| Find a plant for a small or dim space | Small plants; low-light-tolerant plants | گیاهان کوچک؛ گیاهان مناسب نور کم | Separate sold size, mature size and light tolerance |
| Choose familiar groups | Cacti and succulents; orchids; foliage plants | کاکتوس و ساکولنت؛ ارکیده؛ گیاهان برگ‌زینتی | Groups may overlap; keep formal taxonomy separate |
| Buy flowers by the stem | Cut flowers / cut stems | گل شاخه‌بریده؛ گل شاخه‌ای | Stem type, color, unit and offer |
| Send a gift | Bouquet; flower box; basket; vase arrangement | دسته‌گل؛ باکس گل؛ سبد گل؛ گل‌آرایی در گلدان | Arrangement format separate from flowers used |
| Shop for a ceremony | Sympathy; congratulations | ترحیم؛ تبریک | Occasion facet; «تاج گل» is a format and can serve multiple occasions |
| Buy lasting décor | Dried; preserved | گل خشک؛ گل ماندگار | Separate treatments from fresh flowers |
| Buy supplies | Planters; potting mix; accessories | گلدان؛ خاک و بستر کشت؛ لوازم نگهداری | Separate catalog family |

For Iran, start with independent audits for Tehran, a second major city and a seller that claims nationwide shipping. Tehran delivery coverage should never stand in for Iranian coverage. Record Persian labels exactly as shown before normalizing. Check for هدیه, تولد, سالگرد, ترحیم and تبریک as occasion terms; separate these from format and from delivery promises. Check for seasonal collections such as نوروز and شب یلدا before adding them to local merchandising. Other Persian-speaking markets are separate research scopes, with different delivery networks and local conventions.

For English, audit labels at the country level and keep the interface adaptable: test indoor plants versus houseplants, sympathy versus funeral flowers, city versus postcode eligibility, and seller-specific units and currency. Keep florist occasions and houseplant traits as parallel classification systems. Include independent florists in addition to national sites so the sample shows city-specific delivery constraints and merchandising vocabulary.

## How to close the gaps

For each market, capture two houseplant catalogs and two florists where feasible, including a local shop and a national or broad-coverage seller. Record the rendered homepage menu, one listing page, one product detail, and the delivery terms. For Iran, add a wholesale or physical-market evidence stream before drawing conclusions about the general flower trade; the online florist sample alone will not show wholesale selling units or seasonality. Record wholesale units separately from retail formats.

Use one observation per row: `id, market, city, seller, seller_type, page_type, url, observed_at, status, raw_label, parent_label, ui_role, proposed_concept_id, evidence_note`. Distinguish top-level menu, collection, filter, editorial heading, product attribute and service promise. Count sellers rather than the number of links when comparing how often a label occurs, and give the denominator for each market. Preserve failed and incomplete captures in the evidence log. Prioritize a confirmed Persian catalog and florist before freezing the Persian navigation.
