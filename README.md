# FlowerMarketOntology

Research snapshot: 11 November 2026. Initial audience: Persian-speaking apartment growers in Iran, with an English edition and room for later country-specific shops. “Apartment flowers” includes foliage plants sold as گل آپارتمانی as well as flowering plants.

Start with [Market research](market-research.md), then read the [Knowledge and website blueprint](blueprint.md). [taxonomy.json](taxonomy.json) is the proposed content vocabulary and data contract. [observations.jsonl](observations.jsonl) contains source-linked labels for follow-up comparisons.

The first public knowledge-data release contains one bilingual golden-pothos profile with inspectable evidence. The [project roadmap](research-roadmap.md) links the delivery issues, acceptance gates, and research backlog.

## Intended outcome

See the [project knowledge map](knowledge-map.md) for the site categories, research coverage, and evidence boundaries.

The [live product presentation audit](research/product-presentation-audit.md) compares seller grouping, product details and gaps across sampled Iranian, U.S. and U.K. pages.

Original reports live in [research/sources](research/sources/). Their structured imports live in [research/batches](research/batches/). [Direct observations](observations.jsonl) and the [taxonomy](taxonomy.json) remain at the project root.

The [Tehran execution intake](research/batches/batch-02.json) extends the first batch with page-level evidence, reported authority IDs, and online wholesale unit examples. The [third tranche](research/batches/batch-03.json) adds bilingual pilot wording, an image candidate, scoped seller policies, and search fixtures. The roadmap tracks remaining validation and release work.

Build a maintained Persian and English reference that connects plant names, botanical identities, and cited care advice. The same records should support a plant directory, condition-based discovery, and troubleshooting. A later shop can attach local offers and arrangements while keeping plant profiles and care links stable.

## Run the knowledge pilot

```sh
python -m pip install -r requirements.txt
python ontology.py validate
python ontology.py search "برگ انجیری"
python ontology.py search "پتوس طلایی"
python ontology.py export
python ontology.py schema
python -m unittest discover -s tests
```

The Python models define the executable pilot contract. Taxonomy v6 remains the broader design vocabulary. The importer reads the four research batches and the observation log, then emits canonical schema v5. Keep the input files as evidence. For a breaking export change, add a version and an explicit migration. Taxon IDs are distinct from display names, which come from an identified treatment. The internal pilot export includes draft care and candidate image metadata. Editorial review, exact evidence locators, image selection and attribution, and mobile user testing remain release work.

The separate public exporter reads an explicit release authorization from the committed checkout. See the [public export contract](publication-contract.md) for the build command, approval requirements, and current release blockers.

## Release plan

| Milestone | Scope | Completion criteria |
|---|---|---|
| v0.1 · Research foundation | Architecture, proposed vocabulary, market notes, and evidence format | Taxonomy parses and the existing seller observations resolve to defined concepts. |
| v0.2 · Public knowledge-data release | Publish a reproducible, versioned public artifact and manifest with canonical serialization and one stable profile ID, approved Persian and English claims, and inspectable evidence. | Exact-head validation of reconciled main and editorial sign-off are recorded. The internal export remains separate. Regression tests verify exclusion of drafts and unapproved images. |
| v0.3 · Knowledge library | Verify deterministic multi-profile migration and stable IDs and references across renamed treatments. Then build the Persian-first RTL mobile interface and prepare three to five additional reviewed profiles beyond pothos in parallel. | The integrated batch and interface pass joint export, search, authorization, and usability checks. The five-reader pilot aims for four unassisted completions per task, reports by task, device, and failure category, and reruns affected checks after blocking corrections. |
| v0.4 · Plant finder and troubleshooting | Use deterministic light and space selection and a separate yellow-leaf flow with reviewed symptom-to-cause evidence. | Tests cover missing, unsupported, and conflicting evidence. Troubleshooting communicates uncertainty and offers safe next observations. |
| v1.0 · Maintained reference | Maintain stable profile links, editorial correction workflows, documented schema migrations, and reproducible publication. | A maintainer can add or correct a sourced claim, correct a name, migrate the catalog, and regenerate the public release while preserving existing links and references. |

Commerce research proceeds independently of botanical releases. The roadmap starts Tehran offer testing with one comparable product family and defines the evidence required before ranking offers.
