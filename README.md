# FlowerMarketOntology

Research snapshot: 11 November 2026. Initial audience: Persian-speaking apartment growers in Iran, with an English edition and room for later country-specific shops. “Apartment flowers” includes foliage plants sold as گل آپارتمانی as well as flowering plants.

Start with [Market research](market-research.md), then read the [Knowledge and website blueprint](blueprint.md). [taxonomy.json](taxonomy.json) is the proposed content vocabulary and data contract. [observations.jsonl](observations.jsonl) contains source-linked labels for follow-up comparisons.

The first release should answer **What plant do I have? Will it suit my home? What should I do when something looks wrong?** Start with Persian search and a bilingual indoor plant library. The [research roadmap](research-roadmap.md) orders the evidence audit, name mapping, care literature, and usability work. Commerce and wholesale research follow their own tracks.

## Intended outcome

Build a maintained Persian and English reference that connects plant names, botanical identities, and cited care advice. The same records should support a plant directory, condition-based discovery, and troubleshooting. A later shop can attach local offers and arrangements while keeping plant profiles and care links stable.

## Release plan

| Milestone | Scope | Completion criteria |
|---|---|---|
| v0.1 · Research foundation | Architecture, proposed vocabulary, market notes, and evidence format | Taxonomy parses and the existing seller observations resolve to defined concepts. |
| v0.2 · Next release | Audit Tarhegol, Nargil, and VIPShop. Review five Persian name records and publish one pilot profile in both languages with source-linked care claims. | Each seller has a dated capture or documented access failure. Each name has an explicit resolution status. A reviewer can trace the pilot profile's care advice to its sources. |
| v0.3 · Knowledge library | 15–20 reviewed profiles, five care guides, and a mobile directory with Persian, English, and scientific name search | Editorial review and mobile search checks pass, including ambiguous names and Persian spelling variants. |
| v0.4 · Plant finder and troubleshooting | Match light and space needs to reviewed profiles and show plausible causes for common symptoms | Example scenarios cover conflicting or missing information and produce understandable results. |
| v1.0 · Maintained reference | Stable profile URLs, documented data exports, and an editorial correction and review workflow | Someone new to the project can add a sourced claim, correct a name, and regenerate the directory without breaking existing links. |

Treat cut-flower guides, seller offers, and florist delivery as extensions. The research roadmap defines the evidence to collect before adding them.
