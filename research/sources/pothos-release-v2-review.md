# Golden-pothos v2 release-candidate review

**Disposition: REVISE.** This is a review record for issue #7. The committed v2 release input selects no profile.

## Candidate and distribution

| Field | Review target |
| --- | --- |
| Reference revision | `0679eac9302c96d9fccd6522b9556ac92322c851` |
| Candidate release version | `0.2.0`, as declared in the committed v2 input |
| Schema and profile | Public schema v2, `plant-fa-pothos-001` |
| Display identity | Golden pothos · پتوس طلایی · *Epipremnum aureum* |
| Candidate distribution | Text-only bilingual public JSON knowledge artifact and manifest for Persian-speaking apartment growers in Iran and English readers. Final distribution terms, approved URLs and release date require maintainer confirmation. |
| Candidate claims | The six canonical Batch 04 claim IDs below. Initial review set consists of light, watering and repotting. |
| Assets | Both image candidates are withheld from this text-only candidate. |

[Issue #7](https://github.com/SoloMidMiram/FlowerMarketOntology/issues/7) · [Batch 04 canonical drafts](../batches/batch-04.json) · [Committed v2 input](../public-release-v2.json) · [Publication policy v2](../../publication-policy-v2.md)

## Identity check

IPNI displayed *Epipremnum aureum* under ID `87014-1` with authorship `(Linden ex André) G.S.Bunting`. The historical tranche used `(Linden & André) G.S.Bunting`. IPNI corroborates the nomenclatural identifier. The selected POWO accepted-treatment page returned a browser challenge, so its treatment and author string could not be rechecked. The GBIF website search also showed a challenge and World Flora Online search timed out. The separate GBIF public API served Kew’s World Checklist of Vascular Plants (WCVP) record. It lists taxon `70476` as accepted, binds that record to `ipni:87014-1` and the selected POWO URL, and gives the historical tranche’s author string. This directly verifies an accepted treatment in the GBIF-distributed WCVP, with a nomenclatural authorship variation visible in IPNI. NC State independently uses the binomial and explains the historical treatment of golden pothos as *E. pinnatum* ‘Aureum’. The reviewer can assess the GBIF-distributed WCVP as a replacement for the historical POWO evidence identifier. Confirm selection and terms for this exact distribution before recording identity approval. [WCVP verbatim record](https://api.gbif.org/v1/species/206541383/verbatim) · [Dataset metadata](https://api.gbif.org/v1/dataset/f382f0ce-323a-4091-bb9f-add557f3a9a2) [Selected POWO record](https://powo.science.kew.org/taxon/urn:lsid:ipni.org:names:87014-1) · [IPNI record](https://www.ipni.org/n/87014-1) · [IPNI terms](https://www.ipni.org/terms-and-conditions) · [NC State profile](https://plants.ces.ncsu.edu/plants/epipremnum-aureum/)

## Claim review matrix

Each row refers to the exact English and Persian drafts in Batch 04. All six scientific decisions and all twelve independent locale approvals remain pending. The observed source dispositions below are review findings.

| Claim | Evidence relation and applicability | Scientific and bilingual review action | Rights and release status |
| --- | --- | --- | --- |
| `care.pothos.light.001` | `rhs-overview` and `rhs-light` support bright indirect light, some shade tolerance and the variegation effect. `rhs-naming` and `nc-naming` help establish the scope of the genus guide, whose golden-pothos link resolves to the RHS species profile. The species profile’s cultivation paragraph separately supports bright filtered light under glass. The inspected sections did not establish reduced growth under lower light. `nc-culture` and `nc-light` provide species-level corroboration of preference, survival and variegation. | Narrow both drafts to light preference, some shade tolerance and possible loss of variegation, or provide direct evidence for reduced growth. Confirm the indoor scope and avoid translating tolerance as a preference. | RHS citation clearance and release-specific recheck pending. NC State is corroboration in this review. Adding it to the release evidence requires a separate source decision. |
| `care.pothos.watering.001` | `rhs-watering` supports checking the potting mix as it approaches dryness and avoiding extended wetness and standing water. `nc-culture` uses a stronger dry-out phrase. Its text does not define a depth or moisture threshold. | Keep the trigger as a potting-mix condition. Verify the Persian conveys approaching dryness, with no fixed interval or instruction to dry the entire root ball. Review the warning within the scope of a drained indoor container. | RHS citation clearance and release-specific recheck pending. Initial review set. |
| `care.pothos.humidity.001` | `rhs-overview` supports lack of a high-humidity requirement in typical home conditions. `nc-culture` describes ways to add humidity. It does not specify an unusually dry-room threshold or show the size of a benefit. | Review the synthesis as a single bilingual recommendation. Consider phrasing supplemental humidity as an option without claiming a measured threshold or benefit. | Both source clearances and release-specific rechecks pending. Hold for synthesis review. |
| `care.pothos.substrate.001` | `rhs-planting` supports an open, moisture-retentive, well-drained and slightly acidic container medium. Its general houseplant compost option qualifies how strongly to state acidity. The RHS species profile spans acidic, neutral, and alkaline soil categories and gives separate outdoor and under-glass guidance. That broader setting does not establish a requirement for acidity in an indoor container. | Check each property and whether the acidity wording should be framed as a preference. Preserve the distinction between retaining some moisture and poor drainage. | RHS citation clearance and release-specific recheck pending. Hold for scope review. |
| `care.pothos.repotting.001` | `rhs-planting` supports crowding or roots appearing at the drainage openings, spring repotting, and a small size increase. It separately describes a one-size increase. The guide covers the genus and includes golden pothos under its historical treatment. | Confirm species applicability and spring context. Review whether the Persian wording can distinguish crowded roots from ordinary root occupancy and convey a modest size increase. | RHS citation clearance and release-specific recheck pending. Initial review set. |
| `care.pothos.toxicity.001` | `asp-name`, `asp-animals`, `asp-principle` and `asp-signs` support the species, dog and cat scope, toxic principle and oral irritation. Those fields do not explicitly define the chewing or ingestion route. | Review a species-specific exposure reference for chewing or ingestion, or narrow both drafts to the directly supported statement. Keep animal scope to cats and dogs. | ASPCA’s legal page refers linking to its linking policy. The species-page URL remains unresolved, and reproduction is handled separately. Withhold until clearance or a separately reviewed alternative. |

[RHS growing guide](https://www.rhs.org.uk/plants/epipremnum/growing-guide) · [RHS species profile](https://www.rhs.org.uk/plants/91403/epipremnum-aureum/details) · [NC State plant profile](https://plants.ces.ncsu.edu/plants/epipremnum-aureum/) · [ASPCA golden-pothos record](https://www.aspca.org/pet-care/aspca-poison-control/toxic-and-non-toxic-plants/golden-pothos)

## Wording for the initial review

These are proposed revisions for scientific and independent locale review. The canonical Batch 04 claims are the comparison baseline.

| Claim | English proposal | Persian proposal |
| --- | --- | --- |
| `care.pothos.light.001` | Give golden pothos bright, indirect light. It tolerates some shade, but too little light can reduce leaf variegation. | پتوس طلایی را در نور روشن و غیرمستقیم بگذارید. گیاه کمی سایه را تحمل می‌کند، اما نور خیلی کم ممکن است ابلقی برگ‌ها را کاهش دهد. |
| `care.pothos.watering.001` | Check the potting mix and water when it is starting to dry. Avoid keeping the mix wet for long periods or leaving the pot standing in water. | بستر گلدان را بررسی کنید و وقتی رو به خشکی می‌رود آبیاری کنید. نگذارید بستر برای مدت طولانی خیس بماند یا گلدان در آب بماند. |
| `care.pothos.repotting.001` | When roots crowd the pot or emerge from the drainage holes, repot in spring into a pot one size larger. | اگر ریشه‌ها در گلدان جا کم آورده‌اند یا از سوراخ‌های زهکش بیرون زده‌اند، در بهار گیاه را به گلدانی یک اندازه بزرگ‌تر منتقل کنید. |

## Source-rights review

| Source and distribution | Proposed disposition | Evidence for the decision still needed |
| --- | --- | --- |
| RHS public growing guide | Investigate citation-only | The reviewed terms URL covered ChatBotanist and did not establish the rule for this growing-guide URL. Confirm the applicable linking and citation terms for the actual distribution. Retention and redistribution rights would require separate decisions. [RHS terms page inspected](https://www.rhs.org.uk/terms-and-conditions) |
| NC State Extension Gardener Plant Toolbox web profile | Investigate citation-only | The profile displays individual asset licenses. The university copyright information does not establish a reuse grant for the profile prose. Confirm applicable citation and linking terms for the selected URL. [NC State copyright information](https://www.ncsu.edu/copyright/) |
| ASPCA public species record | Withhold | Obtain clearance for the actual species-page link or review a replacement evidence source. ASPCA treats reproduction requests case by case. [Legal information](https://www.aspca.org/about-us/legal-information) · [Copyright and reprint policy](https://www.aspca.org/about-us/copyright-and-reprint-policy) |
| Kew POWO web record | Withhold pending recheck and rights review | Direct inspection was challenged. Review POWO terms if selecting this web distribution. [POWO record](https://powo.science.kew.org/taxon/urn:lsid:ipni.org:names:87014-1) |
| Kew WCVP via GBIF, dataset `f382f0ce-323a-4091-bb9f-add557f3a9a2` | Candidate identity replacement, citation-only first | GBIF metadata lists CC BY 4.0, DOI `10.15468/6h8ucr`, and publication date 2026-06-04. It identifies Govaerts R and Royal Botanic Gardens, Kew in the citation. The selected record is the verbatim GBIF API URL for `206541383`. The maintainer must record the replacement correspondence, intended-use and exact-URL decision, and recheck approval. [Metadata and attribution](https://api.gbif.org/v1/dataset/f382f0ce-323a-4091-bb9f-add557f3a9a2) · [CC BY 4.0 license](https://creativecommons.org/licenses/by/4.0/legalcode) |

## Passage locators and fingerprints

Observed **25 November 2026, Asia/Tehran** by reading the rendered browser DOM. Each digest covers the browser's `innerText` from the indicated paragraph, heading individual labelled field, or full JSON response from the rendered `pre` element, with CRLF and CR normalized to LF before SHA-256 over UTF-8. The passage prose was omitted from this record. Reopen the exact source for the release-specific recheck under policy v2. The failed POWO retrieval has no fingerprint.

| Passage ID | Locator | DOM scope | Evidence finding | SHA-256 |
| --- | --- | --- | --- | --- |
| `rhs-overview` | Before you get started → What are epipremnums? | P | Genus-level indoor culture, bright indirect light, and humidity. | `47e581e6e5a5d582a5616246ece1919fd5c5cf99f535185c3ae69a518e18c7fd` |
| `rhs-naming` | Before you get started → Choosing epipremnums | P | Historical name for the golden-pothos example. | `6b47ad771c52a609767beae666d5bcb7709e1aa9058cc6f5d60c57d222fc249a` |
| `rhs-planting` | Planting | P | Crowding and drainage-hole triggers, spring timing, container size, and compost properties. | `5c495eb1f8cad65ead66a3e2abd02733b54247d0e207895720e0691c534fe52b` |
| `rhs-light` | Ongoing Care → Location | P | Light preference and loss of variegation in too little light. | `8cfe7f06f169e2606b0c54ccb66b2ff768368ec89b3e79a71620822818b2ac23` |
| `rhs-watering` | Ongoing Care → Watering | P | Test the compost and avoid extended wetness or standing water. | `7fb14cbdbff2fc83c2fb94c0fbfefe60eac735f95b4ea4eccd6b7bdacdc9afa1` |
| `nc-culture` | Description → culture paragraph | P | Species-level light tolerance and supplemental humidity method. Watering wording differs. | `3f46d50348ad1d80cc8ce7124011cb5d6581345397e007bf20ad3b4afc2db6e2` |
| `nc-naming` | Description → paragraph about former treatment | P | Connects the historical cultivar treatment to the current species name. | `10a3cee0a173601b8e987fd4bb5825eefe07540c1fb0003a2d3f2429216d26f3` |
| `nc-light` | Description → Insects, Diseases, and Other Plant Problems | P | Low light can reduce variegation. Overwatering can cause root rot. | `69e0715de8a8efecc8bbea6ff2d078f510f7fb189d4405bf1ca858fa9d7b72ee` |
| `asp-name` | Golden Pothos → Scientific Name | field | Species identity. | `1c49610b68bbfb5e1aed15f4adee6d0cad84607cebe38c99a5c0080b63e9dba5` |
| `asp-animals` | Golden Pothos → Toxicity | field | Cat and dog scope. | `3fbde7a26d7552e66ea9bbe8910538e623261b5657c47a4506d5499b787f8dc9` |
| `asp-principle` | Golden Pothos → Toxic Principles | field | Insoluble calcium oxalates. | `71c6a1a8be929cfd7fbba959b4a653b66af6b222dae249cfe602abb476fa7204` |
| `asp-signs` | Golden Pothos → Clinical Signs | field | Oral irritation. | `cc1e6763f82f525097e5d91653eb411bc36f90a8af2a5fb7dabc4e8becb4c78e` |
| `ipni-name` | Taxon record → name heading, ID 87014-1 | heading | Nomenclatural name and author citation. | `5b44865369eb657bb34ee763b03596db4a42a9707bb2493f0cb49723e0a69219` |
| `rhs-species-culture` | RHS species profile → How to grow → Cultivation | P | Bright filtered light under glass and differentiated growing settings. | `b7dec9c7e8fcaa141087cefe0af7de5be7c9492a88be6122d899087b3fad630b` |
| `wcvp-accepted-verbatim` | WCVP verbatim record `206541383` → full JSON body | PRE | Accepted species, accepted-name linkage and IPNI identifier. | `6745be98513d1379568f7a938245ddf3001880adc34673747784e97ec608f4a0` |

## Same-source fingerprint recheck

All 15 passages were retrieved again on 26 November 2026 (Asia/Tehran). Fourteen digests matched the original review. The WCVP capture was identical across visits. Python and PowerShell agreed on the corrected SHA-256 now recorded in the passage table. The ASPCA fields reproduced after a retry following a navigation timeout.

To repeat the check, open the exact URL and hash the selected node's rendered `innerText` under the normalization rule above. CSS paths can change when a publisher rearranges a page. If a path changes, use the named section or field and compare the exact selected passage. The technical check supplies evidence for an authorized reviewer's release-specific decision.

| Passage ID | Observed source URL | Observed CSS path |
| --- | --- | --- |
| `asp-animals` | [Source](https://www.aspca.org/pet-care/aspca-poison-control/toxic-and-non-toxic-plants/golden-pothos) | `#content > div:nth-child(3) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(6)` |
| `asp-name` | [Source](https://www.aspca.org/pet-care/aspca-poison-control/toxic-and-non-toxic-plants/golden-pothos) | `#content > div:nth-child(3) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(4)` |
| `asp-principle` | [Source](https://www.aspca.org/pet-care/aspca-poison-control/toxic-and-non-toxic-plants/golden-pothos) | `#content > div:nth-child(3) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(8)` |
| `asp-signs` | [Source](https://www.aspca.org/pet-care/aspca-poison-control/toxic-and-non-toxic-plants/golden-pothos) | `#content > div:nth-child(3) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(9)` |
| `ipni-name` | [Source](https://www.ipni.org/n/87014-1) | `#c-page-body > div:nth-child(1) > div:nth-child(1) > h2:nth-child(1)` |
| `nc-culture` | [Source](https://plants.ces.ncsu.edu/plants/epipremnum-aureum/) | `#plant_detail > div:nth-child(5) > dl:nth-child(1) > dd:nth-child(6) > p:nth-child(2)` |
| `nc-light` | [Source](https://plants.ces.ncsu.edu/plants/epipremnum-aureum/) | `#plant_detail > div:nth-child(5) > dl:nth-child(1) > dd:nth-child(6) > p:nth-child(7)` |
| `nc-naming` | [Source](https://plants.ces.ncsu.edu/plants/epipremnum-aureum/) | `#plant_detail > div:nth-child(5) > dl:nth-child(1) > dd:nth-child(6) > p:nth-child(3)` |
| `rhs-light` | [Source](https://www.rhs.org.uk/plants/epipremnum/growing-guide) | `body > div:nth-child(6) > div:nth-child(2) > div:nth-child(2) > main:nth-child(2) > div:nth-child(5) > section:nth-child(1) > div:nth-child(2) > p:nth-child(2)` |
| `rhs-naming` | [Source](https://www.rhs.org.uk/plants/epipremnum/growing-guide) | `body > div:nth-child(6) > div:nth-child(2) > div:nth-child(2) > main:nth-child(2) > div:nth-child(3) > section:nth-child(1) > div:nth-child(2) > p:nth-child(4)` |
| `rhs-overview` | [Source](https://www.rhs.org.uk/plants/epipremnum/growing-guide) | `body > div:nth-child(6) > div:nth-child(2) > div:nth-child(2) > main:nth-child(2) > div:nth-child(3) > section:nth-child(1) > div:nth-child(2) > p:nth-child(2)` |
| `rhs-planting` | [Source](https://www.rhs.org.uk/plants/epipremnum/growing-guide) | `body > div:nth-child(6) > div:nth-child(2) > div:nth-child(2) > main:nth-child(2) > div:nth-child(4) > section:nth-child(1) > div:nth-child(2) > p:nth-child(1)` |
| `rhs-species-culture` | [Source](https://www.rhs.org.uk/plants/91403/epipremnum-aureum/details) | `body > div:nth-child(10) > div:nth-child(2) > div:nth-child(3) > div:nth-child(6) > div:nth-child(2) > div:nth-child(1) > p:nth-child(2)` |
| `rhs-watering` | [Source](https://www.rhs.org.uk/plants/epipremnum/growing-guide) | `body > div:nth-child(6) > div:nth-child(2) > div:nth-child(2) > main:nth-child(2) > div:nth-child(5) > section:nth-child(1) > div:nth-child(2) > p:nth-child(7)` |
| `wcvp-accepted-verbatim` | [Source](https://api.gbif.org/v1/species/206541383/verbatim) | `body > pre:nth-child(1)` |

## Approval and build status

1. Confirm the distribution and release date, then record the exact accepted taxonomic treatment and citation or excerpt decisions for the selected sources.
2. Record scientific approval on the reviewed identity and exact claim wording, evidence, growing conditions and disclosure revision. Obtain separate English and Persian approvals on that revision. Renew bound approvals after an applicable wording, evidence, or disclosure change.
3. Record final release approval and build twice from independent clean checkouts pinned to the authorized input commit. Compare exact bytes and SHA-256 for `knowledge.json` and `manifest.json`, and verify the source revision, selected claims, disclosure modes and absence of withheld images.
4. Keep issue #7 open while release decisions are pending. The initial set may be smaller than six claims if the maintainer approves the actual selected scope.

A clean checkout of the reference revision passed ontology validation, 16 search fixtures, and all 47 tests. The real schema-v2 command returned status 1 because no bilingual profile was authorized and created no output directory. Reproducibility of the real release remains pending an approved input revision.

The source inspection used `mcp__playwright_global.browser_navigate` and `mcp__playwright_global.browser_evaluate`.
