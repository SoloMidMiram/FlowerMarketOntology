# Project roadmap

The first release serves Persian-first apartment growers in Iran and includes an English edition. v0.2 is a versioned public knowledge-data release with one bilingual golden-pothos profile. Tehran is the first commerce research sample.

## Delivery order

| Order | Issue | Acceptance gate |
|---|---|---|
| 1 | [#6 Reconcile the pilot PR stack](https://github.com/SoloMidMiram/FlowerMarketOntology/issues/6) | Review #5 and #1 against main, then reconcile #2 and #3. Record the final disposition of PRs #1–#5 and maintainer decisions. Capture clean-checkout validation, unit tests, and CI evidence for the exact reconciled main HEAD. Give #4 an independent commerce research base so it cannot block the botanical release. |
| 2 | [#7 Release the bilingual pothos data](https://github.com/SoloMidMiram/FlowerMarketOntology/issues/7) | Reproduce a versioned public artifact with a stable profile ID, approved Persian and English claims, and inspectable evidence references with exact locators and scope. Include a manifest with release and schema versions, source revision, checksum, and publication approvals. Serialize both the artifact and manifest canonically using stable record and key order, UTF-8, and LF line endings. Use fixed release metadata so build timestamps cannot change checksums. Keep the internal export separate. Test missing approvals, wording edits, invalid archives, nested references, and exclusion of all unapproved images. |
| 3 | [#8 Support multiple plants](https://github.com/SoloMidMiram/FlowerMarketOntology/issues/8) | Migrate and round-trip the pilot and a second plant. Keep project-owned concept IDs and profile links stable when botanical treatments are renamed. Preserve aliases, claim and evidence references, and sourced authority mappings. Require deterministic migration, import, and export. Reject duplicate IDs and broken references. |
| 4a | [#9 Validate Persian search and read access](https://github.com/SoloMidMiram/FlowerMarketOntology/issues/9) | Provide versioned read-only routes and a minimal Persian-first, RTL, mobile-capable interface. Use independent fixtures and report separate results for normalization, identity resolution, ranking, ambiguity, and public-data authorization. Require zero false exact identifications on ambiguous cases and zero unauthorized data on public routes. |
| 4b | [#10 Expand the reviewed library](https://github.com/SoloMidMiram/FlowerMarketOntology/issues/10) | Import three to five additional publishable profiles beyond pothos without application changes. Preserve unresolved labels and unknown fields. Reproduce the public artifact and manifest under #7. Use review throughput and reader findings to size later batches. The 15–20 profiles, 80–120 names and five guides are planning targets. |
| 5 | [#11 Pilot selection and troubleshooting](https://github.com/SoloMidMiram/FlowerMarketOntology/issues/11) | Implement deterministic light and space selection using reviewed traits. Before enabling the separate yellow-leaf flow, approve symptom-to-cause relations with source locators, applicable species and conditions, and competing causes. For conflicting or unsupported evidence, communicate uncertainty and offer safe observations or questions. Withhold definitive diagnoses and unsupported interventions. Test both flows with readers. |
| Parallel | [#12 Test Tehran offer comparability](https://github.com/SoloMidMiram/FlowerMarketOntology/issues/12) | Select one comparable product family and define required fields before collecting from a target of three sellers. Define the maximum observation age for the market and product family before comparison. Capture dated, source-linked units, counts, grades, currencies, delivery terms, and substitution disclosures where applicable. Reject rankings for missing required fields, incompatible offers, or stale observations. |

After #8 and the publication contract in #7, implement and review #9 and #10 in parallel. Close v0.3 only after export and search tests pass with the reviewed batch and mobile interface together, and the reader pilot passes joint acceptance recorded in both issues. #11 follows that gate. #12 proceeds independently of botanical delivery.

For v1.0, verify that a maintainer can correct names or claims, apply documented schema migrations, and reproduce the public release while preserving stable profile links and evidence references.

Decide on graph exports or evidence-grounded Q&A after the catalog and read interface have demonstrated a concrete interoperability or reader need.

## Baseline verified on November 15, 2026

- Main at `4ae56a3` contains the research foundation. The five PRs are open. #1 and #5 target main. #2, #3, and #4 target #1’s branch.
- Local Python 3.11 validation passed at #1 `b1c88a1` and #2 `5887cf0`. Each validated five direct observations, 11 presentation records, and 16 search fixtures. The unit suites passed 11 and 13 tests respectively.
- The #2 revision provides reviewed-claim filtering, and its ordinary export still serializes the full dataset. Public consumers need the boundary specified in #7.

## Test, review, and iterate

1. Each issue records the revision, test commands, results, and open failures. Technical review and CI support the maintainer’s merge decision. The evidence and locale decisions govern publication.
2. For joint v0.3 acceptance, ask five Persian-first readers to find a named plant, locate a sourced care instruction, and explain an ambiguous search result using the integrated build. Aim for four of five unassisted completions on **each** task as a small-sample pilot target. Report results by task, device, and failure category.
3. Fix blocking findings, including false identifications, draft exposure, and failures that prevent task completion. Rerun affected automated tests and reader tasks after each blocking correction. Record the disposition and next scope before advancing.

## Research backlog

Use the investigations below to supply the delivery issues. Validate the audience and seller-sample assumptions during discovery. Treat the supplied market report as a source of leads and design proposals.

| Order | Investigation and collection | Output and exit criteria |
|---|---|---|
| 1. Persian discovery | Inspect Tarhegol and Nargil for indoor plants, VIPShop for florist language, and a seller outside Tehran for regional comparison. Capture navigation, one listing, one product, and delivery terms per seller. Compare with the existing Sill capture and sample Patch and Bloom & Wild. | Dated observations with exact labels, parent paths, role, market, URL and capture status. Candidate Persian labels have a traceable example or an explicit hypothesis status. |
| 2. Names and identity | Seed names from listings and queries. Begin with پتوس، سانسوریا، زاموفیلیا، برگ‌انجیری and بابا آدم. Check taxon records in Kew and horticultural profiles in NC State. Check cultivar references where the listing claims a cultivar. | A ranked list of 40–60 candidates and a working lexicon of up to 80–120 names as coverage warrants. The first 15–20 profiles have stable IDs and evidenced identities. Ambiguous labels retain multiple candidates or remain unresolved. |
| 3. Care literature | Use RHS and extension sources for light, watering, humidity, substrate and repotting. Then review species profiles and toxicity references for each candidate. Read primary studies for disputed claims where available. Extract the conditions, population or species, applicability to apartments, and conflicts. | Five guides and 15–20 profiles with claim-level references, review status, and asset rights. A reviewer can reproduce each care summary from its records. |
| 4. Search and navigation | Draft search fixtures during Phase 2. Test Persian spelling variants, English names, scientific synonyms, ambiguous trade names, and condition-based discovery on mobile. Ask a small pilot group to find a plant and locate a watering instruction. | Record query, expected results, actual behavior, and corrections. Test «سانسوريا», «برگ انجیری», «نور کم», and «زرد شدن برگ». Publish the directory and guides after editorial and search review. |
| 5. Decision support | Collect symptom, environment and cause evidence for yellow leaves, wilt and leaf spots. Test finder rules against scenarios with known light and space conditions. | Reviewed symptom-to-cause links and a fixture set that covers ambiguous cases and missing data. Launch guided selection and troubleshooting when these results are usable. |
| 6. Floristry and commerce | Sample cut-stem units, bouquet ingredients, substitutions, occasions, price units and delivery zones. Check merchant data and image permissions. Study Mahallati and Imam Reza/Khavaran separately for wholesale units and seasonality. | Dated offer and arrangement examples, source permissions, and a city/date delivery test. Expand English-market sampling and regionalize labels when there is a market decision to support. |

Phases 1 and 2 can overlap once sample names are captured. Phase 3 can start with general guides while species mappings are under review. Use Playwright Global MCP for live retailer inspection according to the repository browser instructions.

## First collection batch status

The [first intake](research/batches/batch-01.json) contains five name records, five draft pothos claim topics, and eight search fixtures. The [execution intake](research/batches/batch-02.json) adds exact URLs where supplied, a Mahallat seller, authority IDs, one product substitution example and repeated online wholesale units. The second review identified these remaining topics.

| Priority | Next investigation | Evidence needed |
|---|---|---|
| P0 | Close the pilot publication review | The tranche supplies revised light, humidity and cat/dog toxicity wording. Resolve exact claim locators and review both languages. Select the individual Kew image and record its attribution, asset-specific license and any crop. Review the watering and substrate claims retained from the first batch if they appear in the pilot. |
| P0 | Research diagnostic features and naming scope | Build a permissioned comparison set for «بابا آدم» and «برگ‌انجیری» with expert-confirmed identity and visible distinguishing traits. Test whether modifiers narrow candidate rank across vendors. Consult cultivar references for links proposed by sellers. |
| P1 | Test Persian search with users | The third tranche adds scientific names, synonyms and spelling variants. Run the fixtures on Android/Chrome and iOS/Safari with a small user pilot. Record keyboard autocorrection, ranking, correction paths and ambiguity handling. |
| P1 | Collect condition-rich symptom cases | Gather examples of yellowing, wilt and leaf spots with timing, moisture, drainage, exposure and root or pest evidence. Record competing causes and where the evidence ends. |
| P2 | Resolve seller policy and archive gaps | VIPShop's B133 and K133 URLs and differing terms are supplied. Capture product-specific snapshots and distinguish flower substitutions from foliage/decor changes. Recover the target Mashhad post ID and date. Check Nargil household terms at checkout or through seller-provided documentation separately from project delivery and linked vendors. |
| P2 | Sample both wholesale markets | Collect vendor-attributed observations on separate dates in each market, with permission, grade, count, price and original currency. Compare seasonal samples only within comparable units. Keep Imam Reza online examples as a separate series. |
| P2 | Compare English and regional markets where useful | Use Sarinaland and Mashhad as different channel examples. Find matched historical Sill surfaces before trend work. Fill the Bloom & Wild product gap if it affects a design decision. |

## Evidence to retain

- **Seller observation.** URL, market, city when applicable, capture date, raw text, parent label, UI role, mapped concept, and evidence reference. Use `reported` for findings from the supplied report, `verified` for direct observations, and `unavailable` for failed captures.
- **Identity and alias.** Stable profile or taxon ID, original name, normalized name, locale, candidate IDs, authority reference, precision, and review decision.
- **Care claim.** Profile ID, topic, conditions, recommendation, source and location within the source, conflicting guidance, review status, reviewer, and review date.
- **Commerce evidence.** Seller, product, market, time observed, currency and display unit, delivery coverage, stock and substitution terms when stated. Keep asset rights and attribution with the source record.

Keep page captures or precise excerpts with the source notes. Store conclusions as structured records and summarize them in the project Markdown. Treat a retailer menu as evidence of wording and navigation. Use separate data to measure demand, stock coverage, and market share.
