"""Build the independently versioned, text-only public release."""
import argparse
import json
import re
import stat
import subprocess
from datetime import date
from hashlib import sha256
from io import BytesIO
from pathlib import Path, PureWindowsPath
from tempfile import TemporaryDirectory
from typing import Annotated, Literal
from zipfile import ZipFile

from pydantic import AfterValidator, Field

from ontology import ROOT, Evidence, Record, build

SCHEMA_VERSION = 1
ARTIFACT_NAME = "knowledge.json"
SPEC = "research/public-release.json"
ARCHIVES = "research/archives"


def nonblank(value: str) -> str:
    if not value.strip():
        raise ValueError("Expected nonblank text")
    return value


Text = Annotated[str, AfterValidator(nonblank)]
Digest = Annotated[str, Field(pattern=r"^[0-9a-f]{64}$")]


class Bilingual(Record):
    en: Text
    fa: Text


class Approval(Record):
    reviewer: Text
    reviewed_at: date
    decision: Literal["approved"]
    revision: Digest

    def check(self, revision, earliest, latest, subject):
        if self.revision != revision:
            raise ValueError(f"Stale approval for {subject}; expected {revision}")
        if not earliest <= self.reviewed_at <= latest:
            raise ValueError(f"Approval date outside verification and release window: {subject}")


class LocaleApprovals(Record):
    en: Approval
    fa: Approval


class Passage(Record):
    first_line: Annotated[int, Field(strict=True, ge=1)]
    last_line: Annotated[int, Field(strict=True, ge=1)]


class ClaimSelection(Record):
    conditions: Bilingual
    passages: dict[str, Passage]
    evidence_approval: Approval
    locale_approvals: LocaleApprovals


class ProfileSelection(Record):
    id: Text
    identity_passage: Passage
    identity_approval: Approval
    claims: dict[str, ClaimSelection]


class Release(Record):
    release_version: Literal["0.2.0"]
    release_date: date | None = None
    profile: ProfileSelection | None = None
    release_approval: Approval | None = None


def unique_pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def strict_json(path):
    data = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique_pairs)
    if path.name == "batch-02.json":
        ids = [record["ipni_id"] for record in data["taxa"]]
        if len(ids) != len(set(ids)):
            raise ValueError("Duplicate taxon ID")
    return data


def canonical(value) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
                       allow_nan=False) + "\n").encode("utf-8")


def revision(value) -> str:
    return sha256(canonical(value)).hexdigest()


def capture(root: Path, source: Evidence, source_id: str, passage: Passage) -> dict:
    archive = source.archive
    if (source.provenance != "verified" or not source.observed_at or not source.locator
            or not source.locator.strip() or not archive or not archive.reuse_basis.strip()):
        raise ValueError(f"Missing verified capture metadata: {source_id}")
    # Require a portable repository-relative path and prohibit linked components.
    parts = archive.path.split("/")
    if (not archive.path.startswith(ARCHIVES + "/")
            or any(not re.fullmatch(r"[A-Za-z0-9_-][A-Za-z0-9_.-]*", part)
                   or part.endswith(".") or PureWindowsPath(part).is_reserved() for part in parts)):
        raise ValueError(f"Invalid archive path: {archive.path}")
    path = root
    for part in parts:
        path /= part
        if path.is_symlink() or path.resolve() != path.absolute():
            raise ValueError(f"Linked archive path: {archive.path}")
    if not path.is_file():
        raise ValueError(f"Missing archive: {archive.path}")
    raw = path.read_bytes()
    if sha256(raw).hexdigest() != archive.sha256:
        raise ValueError(f"Archive checksum mismatch: {archive.path}")
    decoded = raw.decode("utf-8")
    if any(char in decoded for char in ("\r", "\x00", "\ufeff")):
        raise ValueError(f"Expected UTF-8 LF archive text: {archive.path}")
    lines = decoded.removesuffix("\n").split("\n")
    if not passage.first_line <= passage.last_line <= len(lines):
        raise ValueError(f"Invalid archive line range: {source_id}")
    excerpt = "\n".join(lines[passage.first_line - 1:passage.last_line])
    if not excerpt.strip():
        raise ValueError(f"Empty archive excerpt: {source_id}")
    return {
        "source_id": source_id,
        "url": str(source.url),
        "observed_at": source.observed_at.isoformat(),
        "source_locator": source.locator,
        "archive": {
            "sha256": archive.sha256,
            "first_line": passage.first_line,
            "last_line": passage.last_line,
            "excerpt": excerpt,
            "reuse_basis": archive.reuse_basis,
        },
    }


def build_release(root: Path, source_revision: str) -> tuple[bytes, bytes]:
    if not re.fullmatch(r"[0-9a-f]{40}", source_revision):
        raise ValueError("Expected a full Git commit SHA")
    release = Release.model_validate(strict_json(root / SPEC))
    selection = release.profile
    if not selection or not selection.claims or not release.release_date:
        raise ValueError("No bilingual profile authorized for public export")
    dataset = build(root, read_json=strict_json)
    profile = dataset.profile
    if selection.id != profile.id:
        raise ValueError(f"Unknown public profile: {selection.id}")
    treatment = next((item for item in dataset.treatments
                      if item.taxon_id == profile.taxon_id and item.kind == "scientific_name"
                      and item.authority == dataset.display_authority), None)
    if treatment is None:
        raise ValueError("Missing profile identity treatment")
    identity_source = dataset.evidence[treatment.evidence_id]
    identity = {
        "id": profile.id,
        "taxon_id": profile.taxon_id,
        "rank": dataset.taxa[profile.taxon_id],
        "scientific_name": treatment.name,
        "authority": treatment.authority,
        "evidence": capture(root, identity_source, treatment.evidence_id, selection.identity_passage),
    }
    identity_revision = revision({"kind": "identity-v1", "identity": identity,
                                  "archive_path": identity_source.archive.path})
    selection.identity_approval.check(identity_revision, identity_source.observed_at,
                                      release.release_date, profile.id)

    claims_by_id = {claim.id: claim for claim in profile.claims}
    claims = []
    approvals = {}
    for claim_id, selected in sorted(selection.claims.items()):
        if claim_id not in claims_by_id:
            raise ValueError(f"Unknown public claim: {claim_id}")
        claim = claims_by_id[claim_id]
        source_ids = set(claim.evidence_ids)
        if (len(source_ids) != len(claim.evidence_ids) or source_ids != selected.passages.keys()
                or any(not locator.strip() for locator in claim.source_locators.values())):
            raise ValueError(f"Invalid claim evidence references or locators: {claim_id}")
        if set(claim.wording) != {"en", "fa"} or any(not text.strip() for text in claim.wording.values()):
            raise ValueError(f"Missing bilingual wording: {claim_id}")
        evidence = [
            {**capture(root, dataset.evidence[key], key, selected.passages[key]),
             "claim_locator": claim.source_locators[key]}
            for key in sorted(source_ids)
        ]
        semantics = {
            "id": claim_id,
            "topic": nonblank(claim.topic),
            "animal_species": sorted(set(claim.animal_species)),
            "conditions": selected.conditions.model_dump(),
            "evidence": evidence,
        }
        wording = {locale: claim.wording[locale] for locale in ("en", "fa")}
        claim_revision = revision({
            "kind": "evidence-v1", "identity_revision": identity_revision, "semantics": semantics,
            "wording": wording, "archive_paths": {key: dataset.evidence[key].archive.path for key in source_ids},
        })
        observed = max(dataset.evidence[key].observed_at for key in source_ids)
        verified = max(observed, selection.identity_approval.reviewed_at)
        selected.evidence_approval.check(claim_revision, verified, release.release_date, claim_id)
        for locale, text in wording.items():
            review = getattr(selected.locale_approvals, locale)
            wording_revision = revision({"kind": "locale-v1", "evidence_revision": claim_revision,
                                         "locale": locale, "wording": text})
            review.check(wording_revision, selected.evidence_approval.reviewed_at,
                         release.release_date, f"{claim_id}/{locale}")
        claims.append({**semantics, "wording": wording})
        approvals[claim_id] = {
            "evidence": selected.evidence_approval.model_dump(mode="json"),
            "locales": selected.locale_approvals.model_dump(mode="json"),
        }
    artifact = canonical({"schema_version": SCHEMA_VERSION, "profile": {**identity, "claims": claims}})
    manifest = {
        "release_version": release.release_version,
        "release_date": release.release_date.isoformat(),
        "schema_version": SCHEMA_VERSION,
        "artifact": {"name": ARTIFACT_NAME, "sha256": sha256(artifact).hexdigest()},
        "identity_approval": selection.identity_approval.model_dump(mode="json"),
        "claim_approvals": approvals,
    }
    if not release.release_approval:
        raise ValueError("Missing final release approval")
    release_revision = revision({"kind": "release-v1", "manifest": manifest})
    last_review = max(review["reviewed_at"] for entry in approvals.values()
                      for review in entry["locales"].values())
    release.release_approval.check(release_revision, date.fromisoformat(last_review),
                                  release.release_date, "release")
    manifest["release_approval"] = release.release_approval.model_dump(mode="json")
    manifest["source_revision"] = source_revision
    return artifact, canonical(manifest)


def git_snapshot(root: Path, destination: Path) -> str:
    def git(*args):
        return subprocess.check_output(["git", "-C", str(root), *args])

    if git("status", "--porcelain", "--untracked-files=all"):
        raise ValueError("Public export requires a clean checkout")
    head = git("rev-parse", "HEAD").decode("ascii").strip()
    archive = git("-c", "core.autocrlf=false", "-c", "core.eol=lf", "archive", "--format=zip", head)
    with ZipFile(BytesIO(archive)) as snapshot:
        if any(stat.S_ISLNK(item.external_attr >> 16) for item in snapshot.infolist()):
            raise ValueError("Public export snapshot contains symbolic links")
        snapshot.extractall(destination)
    return head


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path, help="New directory for knowledge.json and manifest.json")
    parser.add_argument("--schema-version", choices=(1, 2), type=int, default=1,
                        help="Public schema version (default: 1)")
    args = parser.parse_args()
    build_selected_release = build_release
    if args.schema_version == 2:
        from public_export_v2 import build_release_v2
        build_selected_release = build_release_v2
    try:
        with TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            artifact, manifest = build_selected_release(root, git_snapshot(ROOT, root))
        args.output.mkdir()
        try:
            (args.output / ARTIFACT_NAME).write_bytes(artifact)
            (args.output / "manifest.json").write_bytes(manifest)
        except OSError:
            (args.output / "manifest.json").unlink(missing_ok=True)
            (args.output / ARTIFACT_NAME).unlink(missing_ok=True)
            args.output.rmdir()
            raise
    except (ValueError, OSError, subprocess.CalledProcessError) as error:
        parser.exit(1, f"Public export refused: {error}\n")


if __name__ == "__main__":
    main()
