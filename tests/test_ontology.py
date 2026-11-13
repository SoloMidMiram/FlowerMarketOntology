import unittest

from pydantic import ValidationError

from ontology import Dataset, build


class PilotTests(unittest.TestCase):
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
