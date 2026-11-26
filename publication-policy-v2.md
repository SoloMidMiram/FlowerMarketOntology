# Publication policy v2

## Decision and release boundary

The v2 exporter separates scientific verification, rights review, and public disclosure. Both disclosure modes require the same identity, scientific, bilingual editorial, and final release approvals. The implementation is prepared on a separate branch from the frozen PR #15 head `12925f926631cd35a1766580a981b81dffbf6ef9`. Merge acceptance and the real golden-pothos release remain separate maintainer decisions.

Use `python public_export.py --schema-version 2 OUTPUT_DIRECTORY` from a clean Git checkout. The exporter reads `research/public-release-v2.json` from the committed snapshot. It writes `knowledge.json` and `manifest.json` to a new directory only after all checks pass. The checked-in v2 input has no selected profile. Public schema 1 remains the default with its existing input and approval rules. Internal schema v5 retains its existing commands and behavior.

## Authoring input

The v2 release input specifies `release_version`, `release_date`, `intended_use`, a maintainer-managed `authorized_reviewers` roster, `profile` and `release_approval`. Use a unique release version for each distribution and describe the precise intended distribution in `intended_use`. A new release or a different declared use requires new release-specific rechecks. Review dates use ISO calendar dates. The roster and review records are trusted under the repository's access and review policy. The exporter checks the records and their binding digests. It does not authenticate human identity or confirm that an external review actually took place.

- A profile specifies its existing `id`, `identity` evidence, `identity_approval`, and a `claims` map keyed by canonical claim ID. Each `selected` claim specifies bilingual `conditions`, an `evidence` map, `evidence_approval` and both `locale_approvals`. Every required source ID must be present. A `withheld` claim contains a private `reason` and stays out of the release. A selected claim that depends on a `withheld` source causes the entire release to fail.
- Each source identifies the reviewed HTTPS `url`, `distribution`, optional publisher `version`, `observed_at` and `extraction_method`. Each passage has a unique `id` and `locator` within the evidence entry, a `relation` of `supports`, `qualifies` or `conflicts`, and the `sha256` of its exact UTF-8 text after normalizing line endings to LF. Preserve other whitespace and Unicode. For archived passages, hash the selected lines joined by LF with no extra terminal separator.
- `authorized_excerpt` requires an `archive` with a repository-relative `path` under `research/archives/` and its `sha256`. Each passage also specifies inclusive 1-based `lines` through `first_line` and `last_line`. Rights include separate `citation`, `retention`, and `redistribution` decisions, along with public `attribution` and `public_reuse_basis`. Retention clearance must cover the full committed file and repository clone access. Redistribution clearance must cover each emitted passage and the intended distribution.
- `citation_only` requires cleared citation rights for the exact URL, and a `recheck` approval. It accepts no archive or excerpt fields. The exporter validates the recorded recheck for the candidate release offline. Before approval, an authorized reviewer must reopen the lawful source, locate each exact passage, and confirm the recorded fingerprints still match. The recheck is required for each release, even when a reviewer can consult a lawfully retained restricted copy outside the checkout. If the evidence cannot be rechecked, withhold the claim. A citation-only build evaluates the attestation. It cannot independently reconstruct or hash publisher text that was not supplied.

For a citation-only source with attribution conditions, supply `public_attribution` with `credit`, `license_url`, and `modifications`. Supply `doi_url` as a canonical HTTPS DOI link when the source has a DOI. The exporter copies these fields into the public citation and binds them to the citation rights decision and disclosure revision. Adding, editing, or removing attribution requires a new citation rights decision and renews the dependent identity or scientific, locale, and release approvals. The release passage recheck continues to bind the observed passages. Sources without public attribution fields keep their existing output and approval digests.

The public identity's `authority` is the ontology's display treatment label. The identity evidence's `distribution` and `url` identify the actual approved dataset distribution and record, including when a GBIF-distributed WCVP record replaces the POWO page. Use `public_attribution` to credit that distribution.

Approval records contain `reviewer`, `reviewed_at`, `decision` and `revision`. Rights decisions add a private `basis` and `permitted_use` matching the release's `intended_use`. The reviewer must belong to the maintainer-managed roster. Citation clearance applies to the stated public link as well as the intended use. For a different URL, record the reviewed source and locators that actually apply to that URL. Keep excerpts, confidential notes, and credentials out of public metadata fields.

A source ID identifies one URL, distribution and optional publisher version
throughout a release, including profile identity and selected claims.
Passages, observation dates and disclosure modes may differ. For a reviewed
replacement distribution, record the original source ID and the replacement
URL, distribution and version in the review record. Apply that identity
consistently to every use of the source ID in the release and renew the
applicable approvals against the replacement and its locators. For example,
record the correspondence from the historical POWO evidence ID to the actual
WCVP distribution when reviewers approve that substitution.

All citation-only references with the same source ID must carry identical
public attribution or all omit it. Their passage locators may differ.
Excerpt references retain their own attribution and redistribution decisions.

A standing license can predate observation. For source-specific clearance,
reviewers must record a review dated on or after observation of the material
being cleared. The offline exporter enforces the release-date upper bound and
the approval bindings. Reviewers are responsible for the source-specific lower
bound.

## Revision and output rules

All revision inputs use the same canonical JSON as the output. The v2 module defines the exact typed input and hash preimages.

| Domain | Bound fields |
|---|---|
| `passages-v2` | Source ID, exact distribution metadata and method, passage IDs, locators, relations, fingerprints, and archive ranges where applicable |
| `rights-v2` | Evidence revision, rights scope, intended use, and any public citation attribution. Retention also binds the archive path and checksum. Redistribution additionally binds the public attribution and reuse basis. |
| `release-recheck-v2` | Evidence revision, release version, fixed release date, and intended use |
| `disclosure-v2` | Evidence revision and the complete disclosure inputs, including rights decisions, mode, and archive or recheck |
| `identity-v2` and `evidence-v2` | Projected identity and evidence bindings, plus exact bilingual wording and scope for claim approval |
| `locale-v2` | Claim evidence revision, locale code, and exact wording |
| `release-v2` | Manifest with artifact checksum and the decision records, before adding the final approval and source SHA |

Rights and rechecks must precede the applicable identity or claim approval. Identity and all required source checks precede scientific approval. Locale approvals follow scientific approval. The final approval must follow both locale approvals for each selected claim and be dated no later than the fixed release date. Decisions may share a calendar date.

Both modes emit source ID, URL, distribution, observation date, available version, mode, and each selected passage's ID, locator, and relation. Excerpt mode additionally emits the verified text and line range per passage, archive checksum, attribution, and public reuse basis. Citation-only passage fingerprints remain in the verification input. Neither the artifact nor manifest contains restricted source prose, archive paths, confidential rights bases, or external recheck notes. The public manifest retains the artifact checksum, release and schema metadata, source SHA, and identity, scientific, locale and final approval records.

Claims, source references, and passages sort by canonical ID, source ID, and passage ID respectively. The output uses sorted JSON keys, compact UTF-8 encoding, and one trailing LF. Rebuilding the same committed release produces identical artifact and manifest bytes without network requests or build timestamps.

## Source-rights disposition

- Record the actual GBIF WCVP distribution and its CC BY 4.0 terms if that is the material used. Keep the separately distributed Kew v16 terms separate and verify the licence on that distribution before reuse.
- Treat the ASPCA species-page link as unresolved under its stated linking policy. Its excerpt permission is a separate question. Seek a cleared link or retain an independently supportable alternative if either route cannot be established.
- Check the Virginia Cooperative Extension handbook's noncommercial and ShareAlike terms against the actual distribution. Keep the stronger species-specific evidence where broader horticulture evidence does not establish the claim.
- Published schema 2 describes the disclosure and its approvals. It does not grant source rights or authorize botanical publication. All six real claims remain unpublished.

## Acceptance matrix

| Gate | Verification |
|---|---|
| V2-G1 Source identity | Repeated source IDs share one URL, distribution and optional version throughout each release. Conflicting identities fail even with fresh approvals. Evidence and rights still bind the observation date and specific distribution. |
| V2-G2 Scientific verification | The mixed synthetic release exercises archived checks and per-release external rechecks. Missing, stale, unauthorized and predating rechecks fail. |
| V2-G3 Passage selection | A source can supply two noncontiguous passages. Duplicate IDs or locators, overlaps and invalid ranges fail. |
| V2-G4 Rights decision | Intended-use mismatch, unresolved clearance, stale excerpt attribution clearance and invalid citation URLs fail. |
| V2-G5 Restricted content | Exact mixed-output assertions cover omitted restricted prose, private records, archive gaps, withheld IDs and images. Citation-only rejects an input excerpt. |
| V2-G6 Approval binding | Mode-only change with refreshed disclosure decisions still invalidates scientific approval. Evidence, condition and wording changes invalidate it. Missing locale or final approvals block release. |
| V2-G7 Determinism | Independent clean checkouts with different Git line-ending configuration produce identical synthetic artifact and manifest; input map and passage reorderings preserve bytes. |
| V2-G8 Internal compatibility | Compare internal schema and export bytes against the frozen revision and run its existing regressions. |
| V2-G9 Public v1 compatibility | Keep the existing default, contract and v1 regressions. Explicit v2 selection cannot consume a v1 input. |
| V2-G10 Fail closed | Invalid selected evidence stops the entire export before output. A withheld claim stays absent from a successful release when explicitly excluded. |
