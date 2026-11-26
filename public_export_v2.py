"""Compile the rights-aware public projection from a pinned checkout."""
import re
from datetime import date
from hashlib import sha256
from pathlib import Path
from typing import Annotated, Literal

from pydantic import AfterValidator, Field, HttpUrl, StringConstraints

from ontology import Evidence, EvidenceArchive, Record, build
from public_export import (
    ARTIFACT_NAME, Approval, Bilingual, Digest, LocaleApprovals, Passage, Text,
    canonical, capture, revision, strict_json,
)

SPEC = "research/public-release-v2.json"
SCHEMA_VERSION = 2
Nonempty = Field(min_length=1)


def https_url(value: HttpUrl) -> HttpUrl:
    if value.scheme != "https" or value.username is not None or value.password is not None:
        raise ValueError("Evidence URLs require HTTPS and cannot contain credentials")
    return value


SourceURL = Annotated[HttpUrl, AfterValidator(https_url)]
ReleaseVersion = Annotated[str, StringConstraints(pattern=r"^[0-9]+\.[0-9]+\.[0-9]+$")]


class EvidencePassage(Record):
    id: Text
    locator: Text
    relation: Literal["supports", "qualifies", "conflicts"]
    sha256: Digest


class ArchivedPassage(EvidencePassage):
    lines: Passage


class EvidenceSource(Record):
    url: SourceURL
    distribution: Text
    version: Text | None = None
    observed_at: date
    extraction_method: Text


class RightsDecision(Record):
    reviewer: Text
    reviewed_at: date
    decision: Literal["approved"]
    basis: Text
    permitted_use: Text
    revision: Digest

    def check(self, policy, subject, scope, evidence_revision, **details):
        if self.reviewer not in policy.authorized_reviewers or self.reviewed_at > policy.release_date:
            raise ValueError(f"Unauthorized rights decision for {subject}")
        if self.permitted_use != policy.intended_use:
            raise ValueError(f"Rights scope mismatch for {subject}")
        expected = rights_digest(policy, scope, evidence_revision, **details)
        if self.revision != expected:
            raise ValueError(f"Stale rights decision for {subject}; expected {expected}")


class RightsCitation(Record):
    citation: RightsDecision


class RightsExcerpt(RightsCitation):
    retention: RightsDecision
    redistribution: RightsDecision
    attribution: Text
    public_reuse_basis: Text


class Archive(Record):
    path: Text
    sha256: Digest


class AuthorizedExcerpt(Record):
    mode: Literal["authorized_excerpt"]
    source: EvidenceSource
    passages: Annotated[list[ArchivedPassage], Nonempty]
    rights: RightsExcerpt
    archive: Archive


def doi_link(value: HttpUrl) -> HttpUrl:
    if (value.host != "doi.org" or value.query is not None or value.fragment is not None
            or not re.fullmatch(r"/10\.[0-9]{4,}/.+", value.path or "")):
        raise ValueError("DOI attribution requires a canonical https://doi.org/10.… link")
    return value


class CitationAttribution(Record):
    credit: Text
    doi_url: Annotated[SourceURL, AfterValidator(doi_link)] | None = None
    license_url: SourceURL
    modifications: Text


class CitationOnly(Record):
    mode: Literal["citation_only"]
    source: EvidenceSource
    passages: Annotated[list[EvidencePassage], Nonempty]
    rights: RightsCitation
    recheck: Approval
    public_attribution: CitationAttribution | None = None


class Withheld(Record):
    mode: Literal["withheld"]
    reason: Text


EvidenceInput = Annotated[AuthorizedExcerpt | CitationOnly | Withheld, Field(discriminator="mode")]


class ClaimSelection(Record):
    mode: Literal["selected"]
    conditions: Bilingual
    evidence: dict[str, EvidenceInput]
    evidence_approval: Approval
    locale_approvals: LocaleApprovals


ClaimInput = Annotated[ClaimSelection | Withheld, Field(discriminator="mode")]


class ProfileSelection(Record):
    id: Text
    identity: EvidenceInput
    identity_approval: Approval
    claims: dict[str, ClaimInput]


class Release(Record):
    release_version: ReleaseVersion
    release_date: date | None = None
    intended_use: Text | None = None
    authorized_reviewers: list[Text] = []
    profile: ProfileSelection | None = None
    release_approval: Approval | None = None


class ReleasePolicy(Record):
    release_version: ReleaseVersion
    release_date: date
    intended_use: Text
    authorized_reviewers: Annotated[set[Text], Nonempty]

    def check_approval(self, approval, digest, earliest, subject):
        if approval.reviewer not in self.authorized_reviewers:
            raise ValueError(f"Unauthorized reviewer for {subject}")
        approval.check(digest, earliest, self.release_date, subject)


def evidence_digest(source_id, source, passages) -> str:
    return revision({
        "kind": "passages-v2", "source_id": source_id, "source": source.model_dump(mode="json"),
        "passages": [part.model_dump(mode="json") for part in passages],
    })


def recheck_digest(policy, evidence_revision) -> str:
    return revision({
        "kind": "release-recheck-v2", "release_version": policy.release_version,
        "release_date": policy.release_date.isoformat(), "intended_use": policy.intended_use,
        "evidence_revision": evidence_revision,
    })


def rights_digest(policy, scope, evidence_revision, **details) -> str:
    return revision({
        "kind": "rights-v2", "scope": scope, "intended_use": policy.intended_use,
        "evidence_revision": evidence_revision, "details": details,
    })


def project_evidence(root, source_id, selection, policy):
    """Return the public reference, its review binding, and latest verification date."""
    if isinstance(selection, Withheld):
        raise ValueError(f"Selected evidence is withheld: {source_id}")
    source = selection.source
    passages = sorted(selection.passages, key=lambda part: part.id)
    if (len({part.id for part in passages}) != len(passages)
            or len({part.locator for part in passages}) != len(passages)):
        raise ValueError(f"Duplicate passage ID or locator: {source_id}")
    if source.observed_at > policy.release_date:
        raise ValueError(f"Evidence date after release: {source_id}")
    evidence_revision = evidence_digest(source_id, source, passages)
    citation_details = {}
    if isinstance(selection, CitationOnly) and selection.public_attribution is not None:
        citation_details["public_attribution"] = selection.public_attribution.model_dump(
            mode="json", exclude_none=True)
    selection.rights.citation.check(
        policy, f"{source_id}/citation", "citation", evidence_revision, **citation_details)
    public_passages = [
        {"id": part.id, "locator": part.locator, "relation": part.relation} for part in passages
    ]
    reference = {
        "source_id": source_id, "url": str(source.url), "distribution": source.distribution,
        "observed_at": source.observed_at.isoformat(), "version": source.version,
        "mode": selection.mode, "passages": public_passages, **citation_details,
    }
    reviewed_at = max(source.observed_at, selection.rights.citation.reviewed_at)
    if isinstance(selection, CitationOnly):
        policy.check_approval(selection.recheck, recheck_digest(policy, evidence_revision),
                              source.observed_at, f"{source_id}/release recheck")
        reviewed_at = max(reviewed_at, selection.recheck.reviewed_at)
    else:
        archive = selection.archive.model_dump(mode="json")
        selection.rights.retention.check(policy, f"{source_id}/retention", "retention", evidence_revision,
                                         archive=archive)
        selection.rights.redistribution.check(
            policy, f"{source_id}/redistribution", "redistribution", evidence_revision,
            archive=archive, attribution=selection.rights.attribution,
            reuse_basis=selection.rights.public_reuse_basis,
        )
        reviewed_at = max(reviewed_at, selection.rights.retention.reviewed_at,
                          selection.rights.redistribution.reviewed_at)
        ranges = sorted((part.lines.first_line, part.lines.last_line) for part in passages)
        if any(last >= next_first for (_, last), (next_first, _) in zip(ranges, ranges[1:])):
            raise ValueError(f"Overlapping archived passages: {source_id}")
        source_capture = Evidence(
            url=source.url, provenance="verified", observed_at=source.observed_at,
            locator=passages[0].locator,
            archive=EvidenceArchive(path=selection.archive.path, sha256=selection.archive.sha256,
                                    reuse_basis=selection.rights.public_reuse_basis),
        )
        for part, public in zip(passages, public_passages, strict=True):
            entry = capture(root, source_capture, source_id, part.lines)["archive"]
            excerpt = entry["excerpt"]
            if sha256(excerpt.encode("utf-8")).hexdigest() != part.sha256:
                raise ValueError(f"Excerpt fingerprint mismatch: {source_id}/{part.id}")
            public.update(first_line=part.lines.first_line, last_line=part.lines.last_line, excerpt=excerpt)
        reference.update(archive_sha256=selection.archive.sha256, attribution=selection.rights.attribution,
                         reuse_basis=selection.rights.public_reuse_basis)
    binding = selection.model_dump(mode="json", exclude={"passages", "public_attribution"})
    binding.update(citation_details)
    binding["evidence_revision"] = evidence_revision
    return reference, revision({"kind": "disclosure-v2", "binding": binding}), reviewed_at


def build_release_v2(root: Path, source_revision: str) -> tuple[bytes, bytes]:
    if not re.fullmatch(r"[0-9a-f]{40}", source_revision):
        raise ValueError("Expected a full Git commit SHA")
    release = Release.model_validate(strict_json(root / SPEC))
    selection = release.profile
    if not selection or not any(isinstance(item, ClaimSelection) for item in selection.claims.values()):
        raise ValueError("No bilingual profile authorized for public export")
    policy = ReleasePolicy(
        release_version=release.release_version, release_date=release.release_date,
        intended_use=release.intended_use, authorized_reviewers=set(release.authorized_reviewers),
    )
    dataset = build(root, read_json=strict_json)
    profile = dataset.profile
    if selection.id != profile.id:
        raise ValueError(f"Unknown public profile: {selection.id}")
    treatment = next((item for item in dataset.treatments
                      if item.taxon_id == profile.taxon_id and item.kind == "scientific_name"
                      and item.authority == dataset.display_authority), None)
    if treatment is None:
        raise ValueError("Missing profile identity treatment")
    identity_citation, identity_binding, identity_date = project_evidence(
        root, treatment.evidence_id, selection.identity, policy)
    identity = {
        "id": profile.id, "taxon_id": profile.taxon_id, "rank": dataset.taxa[profile.taxon_id],
        "scientific_name": treatment.name, "authority": treatment.authority, "evidence": identity_citation,
    }
    identity_revision = revision({"kind": "identity-v2", "identity": identity, "disclosure": identity_binding})
    policy.check_approval(selection.identity_approval, identity_revision, identity_date, profile.id)

    claims_by_id = {claim.id: claim for claim in profile.claims}
    if selection.claims.keys() - claims_by_id.keys():
        raise ValueError("Unknown v2 claim selection")
    claims = []
    approvals = {}
    for claim_id, selected in sorted(selection.claims.items()):
        if isinstance(selected, Withheld):
            continue
        claim = claims_by_id[claim_id]
        source_ids = set(claim.evidence_ids)
        if len(source_ids) != len(claim.evidence_ids) or source_ids != selected.evidence.keys():
            raise ValueError(f"Invalid claim evidence references: {claim_id}")
        if set(claim.wording) != {"en", "fa"} or any(not text.strip() for text in claim.wording.values()):
            raise ValueError(f"Missing bilingual wording: {claim_id}")
        evidence, bindings, review_dates = zip(*(
            project_evidence(root, key, selected.evidence[key], policy) for key in sorted(source_ids)
        ), strict=True)
        projection = {
            "id": claim_id, "topic": claim.topic, "animal_species": sorted(set(claim.animal_species)),
            "conditions": selected.conditions.model_dump(), "evidence": evidence, "wording": claim.wording,
        }
        claim_revision = revision({
            "kind": "evidence-v2", "identity_revision": identity_revision, "claim": projection,
            "disclosures": dict(zip(sorted(source_ids), bindings, strict=True)),
        })
        verified = max(selection.identity_approval.reviewed_at, *review_dates)
        policy.check_approval(selected.evidence_approval, claim_revision, verified, claim_id)
        for locale, text in sorted(claim.wording.items()):
            digest = revision({"kind": "locale-v2", "evidence_revision": claim_revision,
                               "locale": locale, "wording": text})
            policy.check_approval(getattr(selected.locale_approvals, locale), digest,
                                  selected.evidence_approval.reviewed_at, f"{claim_id}/{locale}")
        claims.append(projection)
        approvals[claim_id] = {
            "evidence": selected.evidence_approval.model_dump(mode="json"),
            "locales": selected.locale_approvals.model_dump(mode="json"),
        }
    source_identities = {}
    citation_attributions = {}
    references = [identity_citation, *(ref for claim in claims for ref in claim["evidence"])]
    for reference in references:
        source_id = reference["source_id"]
        source_identity = (reference["url"], reference["distribution"], reference["version"])
        if source_identities.setdefault(source_id, source_identity) != source_identity:
            raise ValueError(f"Conflicting source identity for {source_id}")
        if reference["mode"] == "citation_only":
            attribution = reference.get("public_attribution")
            if citation_attributions.setdefault(source_id, attribution) != attribution:
                raise ValueError(f"Conflicting citation attribution for {source_id}")

    artifact = canonical({"schema_version": SCHEMA_VERSION, "profile": {**identity, "claims": claims}})
    manifest = {
        "release_version": policy.release_version, "release_date": policy.release_date.isoformat(),
        "intended_use": policy.intended_use, "schema_version": SCHEMA_VERSION,
        "artifact": {"name": ARTIFACT_NAME, "sha256": sha256(artifact).hexdigest()},
        "identity_approval": selection.identity_approval.model_dump(mode="json"), "claim_approvals": approvals,
    }
    if not release.release_approval:
        raise ValueError("Missing final release approval")
    last_review = max(review["reviewed_at"] for entry in approvals.values() for review in entry["locales"].values())
    policy.check_approval(release.release_approval, revision({"kind": "release-v2", "manifest": manifest}),
                          date.fromisoformat(last_review), "release")
    manifest["release_approval"] = release.release_approval.model_dump(mode="json")
    manifest["source_revision"] = source_revision
    return artifact, canonical(manifest)
