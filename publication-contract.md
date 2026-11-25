# Public knowledge export

This document covers public schema 1. The separate [rights-aware schema v2 contract](publication-policy-v2.md) describes the explicit v2 export option.

## Baseline and boundary

GitHub `main`, the local remote-tracking ref and the clean baseline worktree all resolved to `32eac01cce3b956a8d3035bda0d445153b807df8`. The original local checkout had staged and unstaged work on an older branch. Validation ran in the isolated worktree with Python 3.11.4 and installed Pydantic 2.14.1.

| Baseline command | Result |
|---|---|
| `python ontology.py validate` | 5 seller observations, 11 presentation records, 16 imported search fixtures |
| `python -m unittest discover -s tests` | 13 passed, including independent golden search cases after export and reload |
| GitHub Actions | [Successful hosted main run](https://github.com/SoloMidMiram/FlowerMarketOntology/actions/runs/43740346679), recorded in [issue #6](https://github.com/SoloMidMiram/FlowerMarketOntology/issues/6) |

The importer builds an internal singleton profile from research batches and patch records, alongside taxonomy, aliases, seller observations, presentation audit rows and search fixtures. The proposed taxonomy vocabulary is v6. The executable internal dataset is schema v5. Its `export`, `schema`, `search`, and `validate` commands keep their existing behavior. Local search and the golden cases use that internal dataset. No public web or API consumer exists in this checkout.

Batch 04 preserves six canonical bilingual care IDs and reported source locators. `research/publication.json` overlays verified captures and legacy review metadata, and currently contains no entries. The internal `reviewed_claims` helper checks a locale wording digest and archive readiness. It can select an independently approved locale and exports no standalone artifact. Its digest does not bind scientific scope or capture revisions. The public exporter uses its own approval record and projection. All research data, legacy review fields, and canonical claim IDs remain intact.

## Build and file contract

Run from the source checkout with Git, Python 3.11 and Pydantic. Reproducibility was tested with Pydantic 2.14.1. Use the same interpreter and dependency versions for repeat builds.

```sh
python -m pip install -r requirements.txt
python ontology.py validate
python -m unittest discover -s tests
python public_export.py ../pothos-release
```

The public command reads the committed checkout, including `research/public-release.json`. The output path must be a new directory. The checked-in allowlist has no authorized profile, so the command exits with status 1 before creating the directory. The test suite builds a synthetic authorized fixture from two clean Git checkouts with different line-ending settings and compares both files byte for byte. The synthetic decisions and archives exist only inside test workspaces. A separate regression selects light, humidity with two passages from different sources, and cat/dog toxicity. It checks deterministic ordering, excludes all other claims and images, and rejects the entire release if any selected claim has unusable evidence or stale locale approval.

Successful builds write `knowledge.json` followed by `manifest.json`. A consumer should accept the pair only after checking the manifest's artifact name, schema version and SHA-256 against the actual bytes. Both files use UTF-8 without BOM, compact JSON, Unicode code-point order for object keys, and exactly one trailing LF. Claim arrays sort by canonical claim ID, references sort by source ID, and animal species are sorted and deduplicated. There is no build timestamp or network access. Fixed release metadata comes from the authorization file and the manifest records the Git source SHA. Do not interpret a manifest as a cryptographic identity signature. Trusted repository access and the maintainer's recorded decision establish authorization.

Public schema 1 explicitly emits one profile with its stable ID, taxon ID, rank, accepted scientific name, authority, identity citation and selected bilingual claims. Each claim includes its canonical ID, topic, indexed animal species where applicable, bilingual growing conditions, exact wording, and source references. Citations expose the source URL, capture date, source locator, claim locator where applicable, archive SHA-256, inclusive 1-based line range, approved plain-text excerpt and reuse basis. Whole captures and local paths stay internal. Consumers should render text as text and handle citation URLs as links. The schema has no media data or image resolution feature. Supporting images requires a reviewed extension with pinned asset bytes, rights, permitted use and attribution.

## Authorization input

The release file specifies `release_version` (`0.2.0`), a fixed `release_date`, one `profile`, and `release_approval`. The profile specifies its `id`, `identity_passage`, `identity_approval`, and a `claims` map keyed by canonical claim ID. Each selected claim specifies `conditions` keyed by `en` and `fa`, `passages` keyed by the exact original source IDs, `evidence_approval`, and `locale_approvals` keyed by `en` and `fa`. Passages specify `first_line` and `last_line`.

Verified sources are entered under `evidence` in `research/publication.json` with provenance, observation date, source locator and an archive record containing the relative path, SHA-256 and reuse basis. Archive paths must be canonical files within `research/archives/`. Captures must be present in the committed snapshot and contain UTF-8 LF text. Both the original claim locator and the exact nonblank archived passage are required. Duplicate JSON keys, duplicate claim IDs, unknown selected claims, extra passage references, unsupported nested fields and any invalid selected record stop the build. Capture checks verify the recorded file and excerpt. Scientific support, locator accuracy against the original source, and permission to reproduce the excerpt are maintainer decisions.

An approval contains `reviewer`, `reviewed_at`, `decision: "approved"` and a SHA-256 `revision`. Revisions hash the same canonical JSON used for output. The public exporter and synthetic test spell out the hash inputs:

| Decision | Bound content |
|---|---|
| Identity | `identity-v1`, the projected identity, capture and internal archive path |
| Claim evidence | `evidence-v1`, identity revision, claim semantics, both wordings and archive paths |
| Editorial per locale | `locale-v1`, the claim evidence revision, locale code and exact locale wording |
| Release | `release-v1` and the manifest before adding the release approval and source SHA |

Identity review follows its capture. Scientific approval follows identity approval and all claim captures. Locale approvals follow scientific approval. Release approval follows all locale approvals and is dated on or before the fixed release date. Any approval may occur on the same date as its prerequisite. The final digest covers the exact artifact checksum and decision records. The source SHA is added after approval to avoid a self-referential commit hash. The repository policy separately requires explicit maintainer acceptance of the exact PR head before merge. A digest reported by a failed build helps identify the revision for review and carries no decision authority.

## Issue 7 acceptance matrix

| Requirement | Technical evidence | Remaining release gate |
|---|---|---|
| Reproduce a stable bilingual profile with inspectable evidence and conditions | Synthetic successful clean-checkout CLI builds and exact-shape assertions | Verify accepted identity, sources, scope and conditions for actual golden pothos |
| Canonical artifact and release metadata | Byte equality across clean checkouts and record reorder checks | Fix the actual release date before signing |
| Manifest, source revision, checksum and approvals | Manifest digest, full source SHA, ordered decisions and stale approval tests | Record real bilingual editorial decisions and final release authorization |
| Asset-specific rights and nested image exclusion | Text-only projection, strict rejection of nested image injection, and projection equality excluding both candidates | Both candidates remain unpublished. Any image support needs verified exact file, permission, attribution and intended use |
| Reject drafts, corrupt archives, wording changes, missing approvals and leakage | No real artifact, invalid path/range/checksum tests, duplicate and reference tests, stale scientific and locale tests, separate internal export | Capture and verify the relevant RHS, NC State and ASPCA passages, including applicability of genus-level RHS guidance. Review all six claim wordings and capture reuse rights |

[Issue #7](https://github.com/SoloMidMiram/FlowerMarketOntology/issues/7) tracks the actual release. [Issue #8](https://github.com/SoloMidMiram/FlowerMarketOntology/issues/8) owns multi-profile migration. [Issue #14](https://github.com/SoloMidMiram/FlowerMarketOntology/issues/14) owns presentation visibility semantics. PR #4 remains outside this slice. Automated validation is technical evidence. Maintainer acceptance and publication decisions are pending.


## Hosted CI gate

The push and pull request checks for the initial PR #15 head reported an account-level Actions billing block. GitHub's annotations state that the jobs never started because recent account payments failed or the spending limit needs to be increased. The annotations leave the specific billing condition unresolved. The configured hosted runner never reached checkout or workflow steps. [Push check](https://github.com/SoloMidMiram/FlowerMarketOntology/actions/runs/44708668842/job/136194511392) and [pull request check](https://github.com/SoloMidMiram/FlowerMarketOntology/actions/runs/44708790979/job/136195599294).

Keep the merge on hold until the account can start hosted jobs and the applicable checks pass for the exact PR head. Local clean-checkout results and Git tree comparisons provide technical evidence while hosted CI is blocked.
