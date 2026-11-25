import json
import shutil
import subprocess
import sys
import unittest
from hashlib import sha256
from pathlib import Path
from tempfile import TemporaryDirectory

from ontology import ROOT, build
from public_export import ARCHIVES, SPEC, build_release, canonical, git_snapshot, revision


HEAD = "1" * 40


class PublicExportTests(unittest.TestCase):
    def setUp(self):
        directory = TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name).resolve()
        shutil.copytree(ROOT / "research", self.root / "research")
        for name in ("taxonomy.json", "observations.jsonl"):
            shutil.copyfile(ROOT / name, self.root / name)
        self.batch = "research/batches/batch-04.json"
        self.claim = self.read(self.batch)["claims"][0]
        self.claim_id = self.claim["id"]
        archive = self.root / ARCHIVES
        archive.mkdir(exist_ok=True)
        self.excerpt = "Synthetic verification passage"
        content = (self.excerpt + "\nInternal-only second line\n").encode()
        (archive / "synthetic.txt").write_bytes(content)
        self.archive = {
            "path": f"{ARCHIVES}/synthetic.txt",
            "sha256": sha256(content).hexdigest(),
            "reuse_basis": "Original test fixture",
        }
        self.source = {"provenance": "verified", "observed_at": "2026-01-01",
                       "locator": "Synthetic section", "archive": self.archive}
        self.identity_id = "powo-87014-1"
        self.write("research/publication.json",
                   {"evidence": {key: self.source for key in (self.identity_id, "rhs")}, "reviews": {}})
        self.sign_fixture()

    def read(self, path):
        return json.loads((self.root / path).read_text(encoding="utf-8"))

    def write(self, path, data):
        (self.root / path).write_bytes(canonical(data))

    def sign_fixture(self, claims=None, excerpts=None):
        dataset = build(self.root)
        passage = {"first_line": 1, "last_line": 1}
        sources = self.read("research/publication.json")["evidence"]
        excerpts = excerpts or {}

        def reference(key):
            source = sources[key]
            return {
                "source_id": key, "url": str(dataset.evidence[key].url),
                "observed_at": source["observed_at"], "source_locator": source["locator"],
                "archive": {
                    "sha256": source["archive"]["sha256"], "reuse_basis": source["archive"]["reuse_basis"],
                    **passage, "excerpt": excerpts.get(key, self.excerpt),
                },
            }

        def approval(value):
            return {"reviewer": "Synthetic fixture", "reviewed_at": "2026-01-02",
                    "decision": "approved", "revision": revision(value)}

        profile = dataset.profile
        identity = {"id": profile.id, "taxon_id": profile.taxon_id, "rank": "species",
                    "scientific_name": dataset.display_name(profile.taxon_id), "authority": "Kew POWO",
                    "evidence": reference(self.identity_id)}
        identity_approval = approval({"kind": "identity-v1", "identity": identity,
                                      "archive_path": self.archive["path"]})
        conditions = {"en": "Synthetic indoor conditions", "fa": "شرایط آزمایشی"}
        projected = []
        selections = {}
        approvals = {}
        for claim in sorted(claims or [self.claim], key=lambda record: record["id"]):
            claim_id = claim["id"]
            evidence_ids = sorted(claim["evidence"])
            semantics = {
                "id": claim_id, "topic": claim["topic"], "conditions": conditions,
                "animal_species": sorted(claim.get("animal_species", [])),
                "evidence": [{**reference(key), "claim_locator": claim["evidence"][key]}
                             for key in evidence_ids],
            }
            wording = {locale: claim[locale] for locale in ("en", "fa")}
            evidence_approval = approval({
                "kind": "evidence-v1", "identity_revision": identity_approval["revision"], "semantics": semantics,
                "wording": wording, "archive_paths": {key: sources[key]["archive"]["path"] for key in evidence_ids},
            })
            locale_approvals = {
                locale: approval({"kind": "locale-v1", "evidence_revision": evidence_approval["revision"],
                                  "locale": locale, "wording": text})
                for locale, text in wording.items()
            }
            projected.append({**semantics, "wording": wording})
            selections[claim_id] = {
                "conditions": conditions, "passages": {key: dict(passage) for key in evidence_ids},
                "evidence_approval": evidence_approval, "locale_approvals": locale_approvals,
            }
            approvals[claim_id] = {"evidence": evidence_approval, "locales": locale_approvals}
        self.expected = {"schema_version": 1, "profile": {**identity, "claims": projected}}
        manifest = {
            "schema_version": 1, "release_version": "0.2.0", "release_date": "2026-01-03",
            "artifact": {"name": "knowledge.json", "sha256": revision(self.expected)},
            "identity_approval": identity_approval,
            "claim_approvals": approvals,
        }
        self.spec = {
            "release_version": manifest["release_version"], "release_date": manifest["release_date"],
            "profile": {
                "id": profile.id, "identity_passage": dict(passage), "identity_approval": identity_approval,
                "claims": selections,
            },
            "release_approval": approval({"kind": "release-v1", "manifest": manifest}),
        }
        self.write(SPEC, self.spec)

    def test_real_inputs_refuse_release_and_keep_internal_records(self):
        dataset = build()
        self.assertEqual(dataset.schema_version, 5)
        self.assertEqual(len(dataset.profile.claims), 6)
        self.assertEqual(len(dataset.profile.image_candidates), 2)
        with self.assertRaisesRegex(ValueError, "No bilingual profile"):
            build_release(ROOT, HEAD)

    def test_synthetic_release_exposes_only_selected_fields_and_passages(self):
        artifact, manifest = build_release(self.root, HEAD)
        self.assertEqual(json.loads(artifact), self.expected)
        self.assertNotIn(b"Internal-only second line", artifact)
        parsed = json.loads(manifest)
        self.assertEqual(parsed["artifact"]["sha256"], sha256(artifact).hexdigest())
        self.assertEqual(parsed["source_revision"], HEAD)
        self.assertEqual(parsed["release_approval"], self.spec["release_approval"])
        self.assertEqual(artifact, canonical(json.loads(artifact)))
        self.assertEqual(manifest, canonical(parsed))

    def test_multi_claim_release_is_ordered_and_rejects_any_invalid_selected_claim(self):
        batch = self.read(self.batch)
        publication_path = "research/publication.json"
        metadata = self.read(publication_path)
        excerpts = {"ncstate": "Synthetic secondary humidity passage", "aspca": "Synthetic toxicity passage"}
        for key, excerpt in excerpts.items():
            path = f"{ARCHIVES}/{key}.txt"
            content = (excerpt + "\n").encode("utf-8")
            (self.root / path).write_bytes(content)
            metadata["evidence"][key] = {
                **self.source, "archive": {**self.archive, "path": path, "sha256": sha256(content).hexdigest()},
            }
        self.write(publication_path, metadata)
        topics = {"light", "humidity", "toxicity"}
        self.sign_fixture([claim for claim in batch["claims"] if claim["topic"] in topics], excerpts)

        artifact, manifest = build_release(self.root, HEAD)
        self.assertEqual(json.loads(artifact), self.expected)
        claims = json.loads(artifact)["profile"]["claims"]
        self.assertEqual([claim["topic"] for claim in claims], ["humidity", "light", "toxicity"])
        self.assertEqual([item["source_id"] for item in claims[0]["evidence"]], ["ncstate", "rhs"])
        self.assertEqual([item["archive"]["excerpt"] for item in claims[0]["evidence"]],
                         [excerpts["ncstate"], self.excerpt])
        self.assertEqual(claims[2]["animal_species"], ["cat", "dog"])
        approval_ids = list(json.loads(manifest)["claim_approvals"])
        self.assertEqual(approval_ids, [claim["id"] for claim in claims])
        for claim in batch["claims"]:
            if claim["topic"] not in topics:
                self.assertNotIn(claim["id"].encode(), artifact + manifest)
        for image in ("kew-gallery", "ncstate-dell-enecks"):
            self.assertNotIn(image.encode(), artifact + manifest)

        batch["claims"].reverse()
        humidity = next(claim for claim in batch["claims"] if claim["topic"] == "humidity")
        humidity["evidence"] = dict(reversed(list(humidity["evidence"].items())))
        selections = self.spec["profile"]["claims"]
        self.spec["profile"]["claims"] = dict(reversed(list(selections.items())))
        selections[humidity["id"]]["passages"] = dict(
            reversed(list(selections[humidity["id"]]["passages"].items()))
        )
        (self.root / self.batch).write_text(json.dumps(batch), encoding="utf-8")
        (self.root / SPEC).write_text(json.dumps(self.spec), encoding="utf-8")
        self.assertEqual(build_release(self.root, HEAD), (artifact, manifest))

        metadata["evidence"]["ncstate"]["provenance"] = "reported"
        self.write(publication_path, metadata)
        with self.assertRaisesRegex(ValueError, "Missing verified capture metadata: ncstate"):
            build_release(self.root, HEAD)
        metadata["evidence"]["ncstate"]["provenance"] = "verified"
        self.write(publication_path, metadata)

        toxicity = selections[claims[2]["id"]]
        toxicity["locale_approvals"]["fa"]["revision"] = "0" * 64
        self.write(SPEC, self.spec)
        with self.assertRaisesRegex(ValueError, r"Stale approval for care\.pothos\.toxicity\.001/fa"):
            build_release(self.root, HEAD)

    def test_reordering_inputs_preserves_bytes(self):
        before = build_release(self.root, HEAD)
        batch = self.read(self.batch)
        batch["claims"].reverse()
        self.write(self.batch, batch)
        (self.root / SPEC).write_text(json.dumps(self.spec, indent=4), encoding="utf-8")
        self.assertEqual(build_release(self.root, HEAD), before)

    def test_locale_wording_edit_requires_new_scientific_approval(self):
        batch = self.read(self.batch)
        batch["claims"][0]["fa"] += "!"
        self.write(self.batch, batch)
        with self.assertRaisesRegex(ValueError, f"Stale approval for {self.claim_id};"):
            build_release(self.root, HEAD)

    def test_locale_approval_cannot_authorize_the_other_locale(self):
        selected = self.spec["profile"]["claims"][self.claim_id]
        selected["locale_approvals"]["fa"] = selected["locale_approvals"]["en"]
        self.write(SPEC, self.spec)
        with self.assertRaisesRegex(ValueError, f"Stale approval for {self.claim_id}/fa"):
            build_release(self.root, HEAD)

    def test_semantic_and_locator_changes_invalidate_evidence_binding(self):
        batch = self.read(self.batch)
        for key, value in (("topic", "changed"), ("animal_species", ["cat"]), ("evidence", {"rhs": "New locator"})):
            with self.subTest(key=key):
                self.write(self.batch, {**batch, "claims": [{**self.claim, key: value}, *batch["claims"][1:]]})
                with self.assertRaisesRegex(ValueError, f"Stale approval for {self.claim_id}"):
                    build_release(self.root, HEAD)

    def test_reported_source_cannot_enter_public_evidence(self):
        metadata = self.read("research/publication.json")
        metadata["evidence"]["rhs"]["provenance"] = "reported"
        self.write("research/publication.json", metadata)
        with self.assertRaisesRegex(ValueError, "Missing verified capture metadata: rhs"):
            build_release(self.root, HEAD)

    def test_new_capture_checksum_does_not_refresh_approval(self):
        path = self.root / self.archive["path"]
        path.write_bytes(path.read_bytes() + b"Changed archive\n")
        metadata = self.read("research/publication.json")
        metadata["evidence"]["rhs"]["archive"]["sha256"] = sha256(path.read_bytes()).hexdigest()
        metadata["evidence"][self.identity_id]["archive"]["sha256"] = sha256(path.read_bytes()).hexdigest()
        self.write("research/publication.json", metadata)
        with self.assertRaisesRegex(ValueError, "Stale approval"):
            build_release(self.root, HEAD)

    def test_missing_and_corrupt_archive(self):
        path = self.root / self.archive["path"]
        path.write_bytes(b"Corrupt archive\n")
        with self.assertRaisesRegex(ValueError, "Invalid archive content"):
            build_release(self.root, HEAD)
        path.unlink()
        with self.assertRaisesRegex(ValueError, "Missing repository archive"):
            build_release(self.root, HEAD)

    def test_archive_path_must_be_canonical_and_inside_dedicated_directory(self):
        metadata = self.read("research/publication.json")
        metadata["evidence"]["rhs"]["archive"]["path"] = f"{ARCHIVES}/../archives/synthetic.txt"
        self.write("research/publication.json", metadata)
        with self.assertRaisesRegex(ValueError, "Invalid archive path"):
            build_release(self.root, HEAD)

    def test_invalid_passage_and_unselected_reference(self):
        selected = self.spec["profile"]["claims"][self.claim_id]
        selected["passages"]["rhs"]["last_line"] = 80
        self.write(SPEC, self.spec)
        with self.assertRaisesRegex(ValueError, "Invalid archive line range"):
            build_release(self.root, HEAD)
        selected["passages"]["unrelated"] = {"first_line": 1, "last_line": 1}
        self.write(SPEC, self.spec)
        with self.assertRaisesRegex(ValueError, "Invalid claim evidence references"):
            build_release(self.root, HEAD)

    def test_duplicate_claim_ids_and_json_keys(self):
        batch = self.read(self.batch)
        batch["claims"].append(self.claim)
        self.write(self.batch, batch)
        with self.assertRaisesRegex(ValueError, "Duplicate claim ID"):
            build_release(self.root, HEAD)
        (self.root / SPEC).write_text('{"release_version":"0.2.0","release_version":"0.2.0"}', encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Duplicate JSON key"):
            build_release(self.root, HEAD)

    def test_partial_locale_approval_and_nested_image_injection(self):
        selected = self.spec["profile"]["claims"][self.claim_id]
        selected["passages"]["rhs"]["image"] = "ncstate-dell-enecks"
        self.write(SPEC, self.spec)
        with self.assertRaisesRegex(ValueError, "Extra inputs are not permitted"):
            build_release(self.root, HEAD)
        del selected["passages"]["rhs"]["image"]
        del selected["locale_approvals"]["fa"]
        self.write(SPEC, self.spec)
        with self.assertRaisesRegex(ValueError, "locale_approvals.fa"):
            build_release(self.root, HEAD)

    def test_valid_locale_approvals_do_not_replace_release_approval(self):
        self.spec.pop("release_approval")
        self.write(SPEC, self.spec)
        with self.assertRaisesRegex(ValueError, "Missing final release approval"):
            build_release(self.root, HEAD)

    def test_release_digest_binds_the_manifest_approval_records(self):
        entry = self.spec["profile"]["claims"][self.claim_id]
        entry["locale_approvals"]["en"]["reviewer"] = "Different test reviewer"
        self.write(SPEC, self.spec)
        with self.assertRaisesRegex(ValueError, "Stale approval for release;"):
            build_release(self.root, HEAD)

    def test_cli_reproduces_committed_fixture_from_clean_checkouts(self):
        for file in ("public_export.py", "ontology.py", ".gitignore"):
            shutil.copyfile(ROOT / file, self.root / file)

        def git(*args, cwd=self.root):
            return subprocess.check_output(["git", *args], cwd=cwd, stderr=subprocess.STDOUT)

        git("init", "-q")
        git("config", "core.autocrlf", "false")
        git("add", ".")
        git("-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
            "-c", "commit.gpgsign=false", "commit", "-qm", "Synthetic release fixture")
        head = git("rev-parse", "HEAD").decode().strip()
        with TemporaryDirectory() as another:
            output = Path(another)
            checkout = output / "checkout"
            git("clone", "-q", "--config", "core.autocrlf=true", str(self.root), str(checkout))
            for source, label in ((self.root, "first"), (checkout, "second")):
                result = subprocess.run([sys.executable, "public_export.py", str(output / label)], cwd=source,
                                        capture_output=True)
                self.assertEqual(result.returncode, 0, f"{label}: {result.stderr.decode()}")
            for file in ("knowledge.json", "manifest.json"):
                self.assertEqual((output / "first" / file).read_bytes(), (output / "second" / file).read_bytes())
            self.assertEqual(json.loads((output / "first/manifest.json").read_bytes())["source_revision"], head)
            (self.root / "untracked.txt").touch()
            with self.assertRaisesRegex(ValueError, "clean checkout"):
                git_snapshot(self.root, output / "unused")


if __name__ == "__main__":
    unittest.main()
