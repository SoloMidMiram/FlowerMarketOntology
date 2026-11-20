import copy
import json
import shutil
import subprocess
import sys
import unittest
from hashlib import sha256
from pathlib import Path
from tempfile import TemporaryDirectory

from ontology import ROOT, build
from public_export import canonical, revision
from public_export_v2 import (
    SPEC, AuthorizedExcerpt, CitationOnly, ReleasePolicy, build_release_v2,
    evidence_digest, project_evidence, recheck_digest, rights_digest,
)

HEAD = "1" * 40
REVIEWER = "Synthetic reviewer"
OBSERVED = "2026-01-01"
REVIEWED = "2026-01-02"
RELEASE_DATE = "2026-01-03"
USE = "Synthetic unrestricted data distribution"
LIGHT = "care.pothos.light.001"
WATERING = "care.pothos.watering.001"
WITHHELD = "care.pothos.repotting.001"
SOURCE_ID = "rhs"
IDENTITY_ID = "powo-87014-1"


def approval(digest):
    return {"reviewer": REVIEWER, "reviewed_at": REVIEWED, "decision": "approved", "revision": digest}


class RightsAwareExportTests(unittest.TestCase):
    def setUp(self):
        directory = TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name).resolve()
        shutil.copytree(ROOT / "research", self.root / "research")
        for name in ("taxonomy.json", "observations.jsonl"):
            shutil.copyfile(ROOT / name, self.root / name)
        (self.root / "research/archives").mkdir(exist_ok=True)
        self.policy = ReleasePolicy(
            release_version="0.2.0", release_date=RELEASE_DATE, intended_use=USE,
            authorized_reviewers={REVIEWER},
        )
        self.dataset = build(self.root)
        self.claims = {claim.id: claim for claim in self.dataset.profile.claims}
        profile = self.dataset.profile
        self.selection = {
            "id": profile.id,
            "identity": self.archived(IDENTITY_ID, "Synthetic CC BY taxon data", "identity",
                                      ["Synthetic taxon record"]),
            "identity_approval": approval("0" * 64),
            "claims": {
                LIGHT: self.selected(self.archived(SOURCE_ID, "Synthetic external source", "light",
                                                   ["Synthetic light passage", "Synthetic second light passage"])),
                WATERING: self.selected(self.citation()),
                WITHHELD: {"mode": "withheld", "reason": "PRIVATE WITHHELD REASON"},
            },
        }
        self.spec = {**self.policy.model_dump(mode="json", exclude={"authorized_reviewers"}),
                     "authorized_reviewers": [REVIEWER], "profile": self.selection}
        self.approve_fixture()

    def source(self, distribution):
        return {"url": "https://example.invalid/evidence", "distribution": distribution, "version": "1",
                "observed_at": OBSERVED, "extraction_method": "PRIVATE EXTRACTION METHOD"}

    def part(self, passage_id, text, relation="supports"):
        return {"id": passage_id, "locator": f"Synthetic section {passage_id}", "relation": relation,
                "sha256": sha256(text.encode("utf-8")).hexdigest()}

    def rights(self, digest):
        return {**approval(digest), "basis": "PRIVATE PERMISSION RECORD", "permitted_use": USE}

    def authorize_evidence(self, source_id, record):
        model = (CitationOnly if record["mode"] == "citation_only" else AuthorizedExcerpt).model_validate(record)
        digest = evidence_digest(source_id, model.source, sorted(model.passages, key=lambda part: part.id))
        record["rights"]["citation"] = self.rights(rights_digest(self.policy, "citation", digest))
        if isinstance(model, CitationOnly):
            record["recheck"] = approval(recheck_digest(self.policy, digest))
        else:
            details = {"archive": record["archive"]}
            record["rights"]["retention"] = self.rights(rights_digest(self.policy, "retention", digest, **details))
            record["rights"]["redistribution"] = self.rights(rights_digest(
                self.policy, "redistribution", digest, **details,
                attribution=record["rights"]["attribution"], reuse_basis=record["rights"]["public_reuse_basis"],
            ))
        return record

    def archived(self, source_id, distribution, name, excerpts):
        path = f"research/archives/{name}.txt"
        content = "\nPRIVATE ARCHIVE GAP\n".join(excerpts).encode("utf-8") + b"\n"
        (self.root / path).write_bytes(content)
        parts = [
            {**self.part(f"p{index}", text), "lines": {"first_line": 2 * index + 1, "last_line": 2 * index + 1}}
            for index, text in enumerate(excerpts)
        ]
        return self.authorize_evidence(source_id, {
            "mode": "authorized_excerpt", "source": self.source(distribution), "passages": parts,
            "archive": {"path": path, "sha256": sha256(content).hexdigest()},
            "rights": {key: self.rights("0" * 64) for key in ("citation", "retention", "redistribution")} | {
                "attribution": "Synthetic publisher, CC BY 4.0", "public_reuse_basis": "Synthetic CC BY 4.0 scope",
            },
        })

    def citation(self):
        return self.authorize_evidence(SOURCE_ID, {
            "mode": "citation_only", "source": self.source("Synthetic external source"),
            "passages": [self.part("water-2", "PRIVATE IRRITATION TEXT", "qualifies"),
                         self.part("water-1", "PRIVATE WATERING TEXT")],
            "rights": {"citation": self.rights("0" * 64)}, "recheck": approval("0" * 64),
        })

    def selected(self, record):
        return {
            "mode": "selected", "conditions": {"en": "Synthetic indoor conditions", "fa": "شرایط آزمایشی"},
            "evidence": {SOURCE_ID: record}, "evidence_approval": approval("0" * 64),
            "locale_approvals": {locale: approval("0" * 64) for locale in ("en", "fa")},
        }

    def approve_fixture(self):
        def project(key, record):
            model = (CitationOnly if record["mode"] == "citation_only" else AuthorizedExcerpt).model_validate(record)
            public, digest, _ = project_evidence(self.root, key, model, self.policy)
            return public, digest

        profile = self.dataset.profile
        citation, disclosure = project(IDENTITY_ID, self.selection["identity"])
        identity = {"id": profile.id, "taxon_id": profile.taxon_id, "rank": "species",
                    "scientific_name": self.dataset.display_name(profile.taxon_id), "authority": "Kew POWO",
                    "evidence": citation}
        identity_revision = revision({"kind": "identity-v2", "identity": identity, "disclosure": disclosure})
        self.selection["identity_approval"] = approval(identity_revision)

        claims = []
        approvals = {}
        for claim_id in (LIGHT, WATERING):
            row = self.selection["claims"][claim_id]
            claim = self.claims[claim_id]
            citation, disclosure = project(SOURCE_ID, row["evidence"][SOURCE_ID])
            projection = {"id": claim_id, "topic": claim.topic, "animal_species": claim.animal_species,
                          "conditions": row["conditions"], "evidence": [citation], "wording": claim.wording}
            digest = revision({"kind": "evidence-v2", "identity_revision": identity_revision,
                               "claim": projection, "disclosures": {SOURCE_ID: disclosure}})
            row["evidence_approval"] = approval(digest)
            row["locale_approvals"] = {
                locale: approval(revision({"kind": "locale-v2", "evidence_revision": digest,
                                           "locale": locale, "wording": text}))
                for locale, text in claim.wording.items()
            }
            claims.append(projection)
            approvals[claim_id] = {"evidence": row["evidence_approval"], "locales": row["locale_approvals"]}
        artifact = {"schema_version": 2, "profile": {**identity, "claims": claims}}
        manifest = {"release_version": "0.2.0", "release_date": RELEASE_DATE, "schema_version": 2,
                    "intended_use": USE, "artifact": {"name": "knowledge.json", "sha256": revision(artifact)},
                    "identity_approval": self.selection["identity_approval"], "claim_approvals": approvals}
        self.spec["release_approval"] = approval(revision({"kind": "release-v2", "manifest": manifest}))
        self.save()

    def save(self):
        (self.root / SPEC).write_bytes(canonical(self.spec))

    def selected_evidence(self, claim):
        return self.selection["claims"][claim]["evidence"][SOURCE_ID]

    def test_mixed_release_keeps_only_cleared_public_fields(self):
        artifact, manifest = build_release_v2(self.root, HEAD)
        profile = json.loads(artifact)["profile"]
        self.assertEqual(json.loads(artifact)["schema_version"], 2)
        self.assertEqual(profile["evidence"]["passages"][0]["excerpt"], "Synthetic taxon record")
        claims = profile["claims"]
        self.assertEqual([item["id"] for item in claims], [LIGHT, WATERING])
        excerpt, citation = (item["evidence"][0] for item in claims)
        self.assertEqual(excerpt["mode"], "authorized_excerpt")
        self.assertEqual([part["first_line"] for part in excerpt["passages"]], [1, 3])
        self.assertEqual(citation["mode"], "citation_only")
        self.assertEqual(set(citation), {"source_id", "url", "distribution", "observed_at",
                                         "version", "mode", "passages"})
        self.assertEqual(citation["passages"], [
            {"id": "water-1", "locator": "Synthetic section water-1", "relation": "supports"},
            {"id": "water-2", "locator": "Synthetic section water-2", "relation": "qualifies"},
        ])
        self.assertEqual(json.loads(manifest)["artifact"]["sha256"], sha256(artifact).hexdigest())
        self.assertEqual(json.loads(manifest)["source_revision"], HEAD)
        for forbidden in ("PRIVATE", "research/archives", "recheck", WITHHELD, "kew-gallery",
                          "ncstate-dell-enecks", "care.pothos.toxicity.001"):
            self.assertNotIn(forbidden.encode(), artifact + manifest)

    def test_repeated_source_accepts_a_consistently_reviewed_replacement(self):
        replacement = {
            "url": "https://example.invalid/replacement",
            "distribution": "Synthetic replacement distribution",
            "version": "2",
        }
        for claim in (LIGHT, WATERING):
            record = self.selected_evidence(claim)
            record["source"].update(replacement)
            self.authorize_evidence(SOURCE_ID, record)
        self.approve_fixture()

        artifact, _ = build_release_v2(self.root, HEAD)
        for claim in json.loads(artifact)["profile"]["claims"]:
            reference = claim["evidence"][0]
            self.assertEqual(reference["source_id"], SOURCE_ID)
            self.assertEqual({key: reference[key] for key in replacement}, replacement)

    def test_repeated_source_rejects_conflicts_even_with_fresh_approvals(self):
        record = self.selected_evidence(WATERING)
        original = dict(record["source"])
        for field, value in (
            ("url", "https://example.invalid/different-source"),
            ("distribution", "Another distribution"),
            ("version", None),
        ):
            with self.subTest(field=field):
                record["source"] = {**original, field: value}
                self.authorize_evidence(SOURCE_ID, record)
                self.approve_fixture()

                with self.assertRaisesRegex(ValueError, "Conflicting source identity for rhs"):
                    build_release_v2(self.root, HEAD)

    def test_rights_review_after_release_is_rejected(self):
        self.selected_evidence(WATERING)["rights"]["citation"]["reviewed_at"] = "2026-01-04"
        self.save()
        with self.assertRaisesRegex(ValueError, "Unauthorized rights decision for rhs/citation"):
            build_release_v2(self.root, HEAD)

    def test_passage_and_claim_order_do_not_change_public_bytes(self):
        expected = build_release_v2(self.root, HEAD)
        for claim in (LIGHT, WATERING):
            self.selected_evidence(claim)["passages"].reverse()
        self.selection["claims"] = dict(reversed(list(self.selection["claims"].items())))
        self.save()
        self.assertEqual(build_release_v2(self.root, HEAD), expected)

    def test_unresolved_rights_and_invalid_citation_are_rejected(self):
        item = self.selected_evidence(WATERING)
        rights = item["rights"]["citation"]
        rights["permitted_use"] = "different distribution"
        self.save()
        with self.assertRaisesRegex(ValueError, "Rights scope mismatch"):
            build_release_v2(self.root, HEAD)
        rights["permitted_use"] = USE
        rights["decision"] = "pending"
        self.save()
        with self.assertRaisesRegex(ValueError, "approved"):
            build_release_v2(self.root, HEAD)
        rights["decision"] = "approved"
        item["source"]["url"] = "https://user:secret@example.invalid/invalid"
        self.save()
        with self.assertRaisesRegex(ValueError, "cannot contain credentials"):
            build_release_v2(self.root, HEAD)

    def test_recheck_is_required_authorized_and_specific_to_release_and_passage(self):
        item = self.selected_evidence(WATERING)
        good = copy.deepcopy(item)
        for failure, value, pattern in (
            ("missing", None, "Field required"),
            ("reviewer", "Unlisted reviewer", "Unauthorized reviewer"),
            ("reviewed_at", "2025-12-31", "Approval date outside"),
        ):
            with self.subTest(failure=failure):
                if failure == "missing":
                    item.pop("recheck")
                else:
                    item["recheck"][failure] = value
                self.save()
                with self.assertRaisesRegex(ValueError, pattern):
                    build_release_v2(self.root, HEAD)
                item.update(copy.deepcopy(good))
        self.spec["release_version"] = "0.2.1"
        self.save()
        with self.assertRaisesRegex(ValueError, "Stale approval for rhs/release recheck"):
            build_release_v2(self.root, HEAD)
        self.spec["release_version"] = "0.2.0"
        item["passages"][0]["sha256"] = "f" * 64
        self.save()
        with self.assertRaisesRegex(ValueError, "Stale rights decision"):
            build_release_v2(self.root, HEAD)
        item["rights"]["citation"] = self.authorize_evidence(SOURCE_ID, copy.deepcopy(item))["rights"]["citation"]
        self.save()
        with self.assertRaisesRegex(ValueError, "Stale approval for rhs/release recheck"):
            build_release_v2(self.root, HEAD)

    def test_fresh_recheck_for_changed_source_does_not_refresh_science_approval(self):
        selected = self.selected_evidence(WATERING)
        selected["source"]["version"] = "2"
        self.authorize_evidence(SOURCE_ID, selected)
        self.save()
        with self.assertRaisesRegex(ValueError, r"Stale approval for care\.pothos\.watering\.001;"):
            build_release_v2(self.root, HEAD)

    def test_citation_only_rejects_attempts_to_supply_excerpt_text(self):
        self.selected_evidence(WATERING)["passages"][0]["excerpt"] = "Publisher prose"
        self.save()
        with self.assertRaisesRegex(ValueError, "Extra inputs are not permitted"):
            build_release_v2(self.root, HEAD)

    def test_redistribution_record_cannot_be_reused_for_different_attribution(self):
        self.selected_evidence(LIGHT)["rights"]["attribution"] = "Different publisher attribution"
        self.save()
        with self.assertRaisesRegex(ValueError, "Stale rights decision for rhs/redistribution"):
            build_release_v2(self.root, HEAD)

    def test_selected_withheld_or_missing_evidence_blocks_entire_release(self):
        selected = self.selection["claims"][LIGHT]["evidence"]
        selected[SOURCE_ID] = {"mode": "withheld", "reason": "No permitted excerpt"}
        self.save()
        with self.assertRaisesRegex(ValueError, "Selected evidence is withheld"):
            build_release_v2(self.root, HEAD)
        selected.clear()
        self.save()
        with self.assertRaisesRegex(ValueError, "Invalid claim evidence references"):
            build_release_v2(self.root, HEAD)

    def test_mode_switch_invalidates_science_approval_even_with_new_disclosure_decisions(self):
        excerpt = self.selected_evidence(LIGHT)
        citation = self.authorize_evidence(SOURCE_ID, {
            "mode": "citation_only", "source": excerpt["source"],
            "passages": [{key: value for key, value in part.items() if key != "lines"}
                         for part in excerpt["passages"]],
            "rights": {"citation": self.rights("0" * 64)}, "recheck": approval("0" * 64),
        })
        self.selection["claims"][LIGHT]["evidence"][SOURCE_ID] = citation
        self.save()
        with self.assertRaisesRegex(ValueError, r"Stale approval for care\.pothos\.light\.001;"):
            build_release_v2(self.root, HEAD)

    def test_invalid_archived_ranges_or_fingerprints_are_rejected(self):
        item = self.selected_evidence(LIGHT)
        part = item["passages"][1]
        for change, pattern in (
            ({"lines": {"first_line": 1, "last_line": 1}}, "Overlapping archived passages"),
            ({"lines": {"first_line": 50, "last_line": 50}}, "Invalid archive line range"),
            ({"sha256": "f" * 64}, "Excerpt fingerprint mismatch"),
            ({"locator": item["passages"][0]["locator"]}, "Duplicate passage ID or locator"),
        ):
            with self.subTest(change=change):
                original = copy.deepcopy(part)
                part.update(change)
                self.authorize_evidence(SOURCE_ID, item)
                self.save()
                with self.assertRaisesRegex(ValueError, pattern):
                    build_release_v2(self.root, HEAD)
                part.update(original)

    def test_scope_and_wording_edits_invalidate_approval(self):
        selected = self.selection["claims"][WATERING]
        selected["conditions"]["en"] = "Different condition"
        self.save()
        with self.assertRaisesRegex(ValueError, r"Stale approval for care\.pothos\.watering\.001;"):
            build_release_v2(self.root, HEAD)
        selected["conditions"]["en"] = "Synthetic indoor conditions"
        self.save()
        batch = self.root / "research/batches/batch-04.json"
        data = json.loads(batch.read_bytes())
        next(claim for claim in data["claims"] if claim["id"] == WATERING)["fa"] += "."
        batch.write_bytes(canonical(data))
        with self.assertRaisesRegex(ValueError, r"Stale approval for care\.pothos\.watering\.001;"):
            build_release_v2(self.root, HEAD)

    def test_missing_locale_or_final_approval_blocks_release(self):
        locale_approvals = self.selection["claims"][WATERING]["locale_approvals"]
        fa = locale_approvals.pop("fa")
        self.save()
        with self.assertRaisesRegex(ValueError, "locale_approvals.fa"):
            build_release_v2(self.root, HEAD)
        locale_approvals["fa"] = fa
        self.spec.pop("release_approval")
        self.save()
        with self.assertRaisesRegex(ValueError, "Missing final release approval"):
            build_release_v2(self.root, HEAD)

    def test_cli_rebuilds_mixed_fixture_offline_from_pinned_checkout(self):
        for name in ("ontology.py", "public_export.py", "public_export_v2.py", ".gitignore"):
            shutil.copyfile(ROOT / name, self.root / name)

        def git(*args, cwd=self.root):
            return subprocess.check_output(["git", *args], cwd=cwd, stderr=subprocess.STDOUT)

        git("init", "-q")
        git("config", "core.autocrlf", "false")
        git("add", ".")
        git("-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
            "-c", "commit.gpgsign=false", "commit", "-qm", "Synthetic v2 release")
        head = git("rev-parse", "HEAD").decode().strip()
        with TemporaryDirectory() as directory:
            output = Path(directory)
            checkout = output / "checkout"
            git("clone", "-q", "--config", "core.autocrlf=true", str(self.root), str(checkout))
            for source, name in ((self.root, "first"), (checkout, "second")):
                result = subprocess.run(
                    [sys.executable, "public_export.py", "--schema-version", "2", str(output / name)],
                    cwd=source, capture_output=True,
                )
                self.assertEqual(result.returncode, 0, result.stderr.decode())
            for name, expected in zip(("knowledge.json", "manifest.json"), build_release_v2(self.root, head),
                                      strict=True):
                self.assertEqual((output / "first" / name).read_bytes(), expected)
                self.assertEqual((output / "second" / name).read_bytes(), expected)

    def test_real_spec_refuses_v2_release(self):
        with self.assertRaisesRegex(ValueError, "No bilingual profile"):
            build_release_v2(ROOT, HEAD)


if __name__ == "__main__":
    unittest.main()
