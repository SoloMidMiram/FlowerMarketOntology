import json
from datetime import date
from hashlib import sha256
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from pydantic import ValidationError

from ontology import Dataset, EvidenceArchive, LocaleReview, build


class PilotTests(unittest.TestCase):
    def test_review_requires_archive_and_current_locale_revision(self):
        dataset = self.dataset.model_copy(deep=True)
        claim = dataset.profile.claims[0]
        claim.reviews["en"] = LocaleReview(
            reviewer="fixture", reviewed_at=date(2026, 11, 13),
            decision="approved", wording_revision=claim.wording_revision("en"),
        )
        with TemporaryDirectory() as directory:
            root = Path(directory)
            self.assertEqual(dataset.reviewed_claims("en", root), [])
            content = b"Original test excerpt"
            (root / "excerpt.txt").write_bytes(content)
            for key in claim.evidence_ids:
                source = dataset.evidence[key]
                source.provenance = "verified"
                source.observed_at = date(2026, 11, 13)
                source.locator = claim.source_locators[key]
                source.archive = EvidenceArchive(path="excerpt.txt", sha256=sha256(content).hexdigest(),
                                                 reuse_basis="Original test fixture")
            self.assertEqual(dataset.reviewed_claims("en", root), [claim])
            self.assertEqual(dataset.reviewed_claims("fa", root), [])
            claim.wording["en"] += " Edited."
            self.assertEqual(dataset.reviewed_claims("en", root), [])

    def test_dimensions_delivery_and_care_have_independent_visibility(self):
        data = self.dataset.model_dump(mode="json")
        row = next(item for item in data["presentation_observations"] if item["id"] == "vip-k133")
        self.assertEqual(row["fields"]["dimensions"]["visibility"], "shown")
        row["fields"]["delivery"] = {"visibility": "conditional", "evidence_status": "verified",
                                     "locator": "Example city selector"}
        row["fields"]["care"] = {"visibility": "unassessed", "evidence_status": "unavailable"}
        Dataset.model_validate(data)
        row["fields"]["care"]["visibility"] = "not_found_on_surface"
        with self.assertRaises(ValidationError):
            Dataset.model_validate(data)
    def test_independent_search_cases_after_export(self):
        exported = Dataset.model_validate_json(self.dataset.model_dump_json())
        cases = json.loads(Path(__file__).with_name("golden-search.json").read_text(encoding="utf-8"))
        for case in cases:
            with self.subTest(query=case["query"]):
                self.assertEqual(exported.search(case["query"]).model_dump(), case["expected"])

    def test_presentation_records_are_validated(self):
        data = self.dataset.model_dump(mode="json")
        self.assertEqual(len(data["presentation_observations"]), 11)
        record = next(item for item in data["presentation_observations"] if item["status"] == "unavailable")
        record["visibility"] = "shown"
        with self.assertRaisesRegex(ValidationError, "Unavailable surfaces must be unassessed"):
            Dataset.model_validate(data)

    def test_preferred_image_remains_unpublished(self):
        profile = self.dataset.profile
        self.assertEqual(set(profile.image_candidates), {"kew-gallery", "ncstate-dell-enecks"})
        image = profile.image_candidates[profile.preferred_image_id]
        self.assertEqual(image.creator, "Dell Enecks")
        self.assertEqual(image.publication_status, "unpublished")
        self.assertIsNone(image.asset_url)
    @classmethod
    def setUpClass(cls):
        cls.dataset = build()

    def test_imported_search_fixtures(self):
        self.assertEqual(len(self.dataset.fixtures), 16)
        for fixture in self.dataset.fixtures:
            with self.subTest(query=fixture.raw_query):
                self.assertEqual(self.dataset.search(fixture.raw_query), fixture.expected)

    def test_trade_names_do_not_select_an_ambiguous_profile(self):
        result = self.dataset.search("برگ‌انجيري")
        self.assertEqual(result.route, "disambiguation")
        self.assertEqual(set(result.concept_ids), {"barg-anjiri", "87478-1", "77306988-1"})
        self.assertIsNone(result.profile_id)
        self.assertIsNone(self.dataset.search("بابا آدم").profile_id)

    def test_golden_pothos_loads_a_bilingual_draft(self):
        self.assertEqual(self.dataset.search("پتوس طلایی").profile_id, self.dataset.profile.id)
        light = next(claim for claim in self.dataset.profile.claims if claim.topic == "light")
        self.assertEqual(set(light.wording), {"en", "fa"})
        self.assertEqual(light.editorial_status, "draft")
        self.assertEqual(self.dataset.search("unknown plant").route, "no_match")

    def test_missing_claim_reference_is_rejected(self):
        data = self.dataset.model_dump(mode="json")
        del data["evidence"][data["profile"]["claims"][0]["evidence_ids"][0]]
        with self.assertRaisesRegex(ValidationError, "Missing claim evidence"):
            Dataset.model_validate(data)

    def test_round_trip(self):
        self.assertEqual(Dataset.model_validate_json(self.dataset.model_dump_json()), self.dataset)

    def test_authority_policy_preserves_alternative_treatment(self):
        result = self.dataset.search("Thaumatophyllum bipinnatifidum")
        self.assertEqual(result.route, "alternative_treatment")
        self.assertEqual(self.dataset.display_name(result.concept_ids[0]), "Philodendron bipinnatifidum")

    def test_invalid_fixture_reference_is_rejected(self):
        data = self.dataset.model_dump(mode="json")
        data["fixtures"][0]["expected"]["concept_ids"] = ["missing"]
        with self.assertRaisesRegex(ValidationError, "Unknown fixture concepts"):
            Dataset.model_validate(data)

    def test_tranche_preserves_bilingual_evidence_and_ambiguity(self):
        self.assertEqual(len(self.dataset.profile.claims), 6)
        for claim in self.dataset.profile.claims:
            self.assertEqual(set(claim.wording), {"fa", "en"})
            self.assertEqual(set(claim.source_locators), set(claim.evidence_ids))
            self.assertEqual(claim.editorial_status, "draft")
        self.assertEqual(self.dataset.search("باباآدم").route, "unresolved")
        self.assertEqual(self.dataset.search("پوتوس طلایی"), self.dataset.search("پتوس طلایی"))
        self.assertIsNone(self.dataset.search("برگ انجیری فر").profile_id)
