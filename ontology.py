"""Build the pilot knowledge dataset from version-controlled research."""
import argparse
import json
import unicodedata
from hashlib import sha256
from datetime import date
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, HttpUrl, model_validator

ROOT = Path(__file__).resolve().parent


class Record(BaseModel):
    model_config = ConfigDict(extra="forbid", str_min_length=1)


class EvidenceArchive(Record):
    path: str
    sha256: str
    reuse_basis: str

    def check_file(self, root: Path) -> None:
        path = (root / self.path).resolve()
        if not path.is_relative_to(root.resolve()) or not path.is_file():
            raise ValueError(f"Missing repository archive: {self.path}")
        content = path.read_bytes()
        if not content.strip() or sha256(content).hexdigest() != self.sha256:
            raise ValueError(f"Invalid archive content: {self.path}")


class Evidence(Record):
    url: HttpUrl
    provenance: Literal["reported", "verified"]
    locator: str | None = None
    observed_at: date | None = None
    archive: EvidenceArchive | None = None


class Treatment(Record):
    taxon_id: str
    name: str
    authority: str
    kind: Literal["scientific_name", "scientific_synonym", "alternative_treatment"]
    evidence_id: str
    research_basis: str | None = None


class Alias(Record):
    forms: list[str]
    resolution: Literal["preferred_candidate", "species_candidate", "trade_group", "ambiguous", "unresolved"]
    candidate_ids: list[str]
    report: str

    @model_validator(mode="after")
    def check_ambiguity(self):
        if not self.forms or not self.candidate_ids:
            raise ValueError("Alias needs forms and candidates")
        if self.resolution == "ambiguous" and len(set(self.candidate_ids)) < 2:
            raise ValueError("Ambiguous alias needs distinct candidates")
        return self


class LocaleReview(Record):
    reviewer: str
    reviewed_at: date
    decision: Literal["approved", "changes_requested"]
    wording_revision: str


class Claim(Record):
    id: str
    topic: str
    wording: dict[Literal["en", "fa"], str]
    evidence_ids: list[str]
    source_locators: dict[str, str] = {}
    research_record: str
    research_pointer: str
    editorial_status: Literal["draft"] = "draft"
    reviews: dict[Literal["en", "fa"], LocaleReview] = {}
    animal_species: list[Literal["cat", "dog"]] = []

    def wording_revision(self, locale: Literal["en", "fa"]) -> str:
        return sha256(self.wording[locale].encode("utf-8")).hexdigest()


class ImageCandidate(Record):
    source_page: HttpUrl
    creator: str
    license: str
    locator: str | None = None
    filename: str | None = None
    asset_url: HttpUrl | None = None
    asset_status: str
    publication_status: Literal["unpublished"] = "unpublished"


class Profile(Record):
    id: str
    taxon_id: str
    claims: list[Claim]
    image_candidates: dict[str, ImageCandidate]
    preferred_image_id: str
    listing_label: str
    listing_evidence_id: str


class Observation(Record):
    seller: str
    capture_id: str
    raw_label: str
    parent_path: list[str]
    ui_role: Literal["collection_link", "chooser_question"]
    mapped_concept_id: str


class PresentationField(Record):
    visibility: Literal["shown", "not_found_on_surface", "conditional", "unassessed"]
    evidence_status: Literal["verified", "reported", "unavailable"]
    locator: str | None = None
    detail: str | None = None

    @model_validator(mode="after")
    def check_evidence(self):
        if self.visibility == "unassessed":
            if self.evidence_status != "unavailable":
                raise ValueError("Unassessed field has no observation evidence")
        elif self.evidence_status == "unavailable" or not self.locator:
            raise ValueError("Assessed fields require evidence and a locator")
        return self


class PresentationObservation(Record):
    id: str
    market: Literal["IR", "US", "UK"]
    page_kind: Literal["product", "aggregator", "collection", "home"]
    product_kind: Literal["arrangement", "live_plant"] | None
    url: HttpUrl
    locator: str
    shown: str
    detail: str
    gaps: str
    status: Literal["verified", "unavailable"]
    visibility: Literal["shown", "not_found_on_surface", "conditional", "unassessed"]
    method: str
    date: date
    fields: dict[Literal["ingredients", "dimensions", "delivery", "care"], PresentationField]

    @model_validator(mode="after")
    def check_scope(self):
        if (self.page_kind in {"product", "aggregator"}) != bool(self.product_kind):
            raise ValueError("Product kind must match page scope")
        if self.status == "unavailable" and self.visibility != "unassessed":
            raise ValueError("Unavailable surfaces must be unassessed")
        if set(self.fields) != {"ingredients", "dimensions", "delivery", "care"}:
            raise ValueError("Missing presentation field states")
        if self.status == "unavailable" and any(field.visibility != "unassessed" for field in self.fields.values()):
            raise ValueError("Unavailable surface has assessed fields")
        return self


class SearchResult(Record):
    route: Literal["alias", "disambiguation", "unresolved", "scientific_name",
                   "scientific_synonym", "alternative_treatment", "light_collection",
                   "symptom", "no_match"]
    concept_ids: list[str]
    profile_id: str | None = None


class Fixture(Record):
    raw_query: str
    locale: Literal["fa-IR", "en"]
    expected: SearchResult


class Dataset(Record):
    schema_version: Literal[5] = 5
    taxa: dict[str, Literal["species", "genus"]]
    evidence: dict[str, Evidence]
    treatments: list[Treatment]
    aliases: dict[str, Alias]
    profile: Profile
    facets: list[str]
    symptoms: dict[str, str]
    observations: dict[str, Observation]
    presentation_observations: list[PresentationObservation]
    fixtures: list[Fixture]
    display_authority: Literal["Kew POWO"] = "Kew POWO"

    def reviewed_claims(self, locale: Literal["en", "fa"], root: Path = ROOT) -> list[Claim]:
        result = []
        for claim in self.profile.claims:
            review = claim.reviews.get(locale)
            if locale not in claim.wording or not review or review.decision != "approved":
                continue
            if review.wording_revision != claim.wording_revision(locale):
                continue
            sources = [self.evidence[key] for key in claim.evidence_ids]
            if not sources or not all(s.provenance == "verified" and s.observed_at and s.locator and s.archive for s in sources):
                continue
            for source in sources:
                source.archive.check_file(root)
            result.append(claim)
        return result

    def display_name(self, taxon_id: str) -> str | None:
        return next((record.name for record in self.treatments
                     if record.taxon_id == taxon_id and record.authority == self.display_authority
                     and record.kind == "scientific_name"), None)

    @model_validator(mode="after")
    def references(self):
        claim_ids = [claim.id for claim in self.profile.claims]
        if len(claim_ids) != len(set(claim_ids)):
            raise ValueError("Duplicate claim ID")
        if self.profile.preferred_image_id not in self.profile.image_candidates:
            raise ValueError("Unknown preferred image")
        ids = [record.id for record in self.presentation_observations]
        if len(ids) != len(set(ids)):
            raise ValueError("Duplicate presentation observation")
        display_taxa = [record.taxon_id for record in self.treatments
                        if record.authority == self.display_authority and record.kind == "scientific_name"]
        if len(display_taxa) != len(set(display_taxa)):
            raise ValueError("Multiple display names under the selected authority")
        for treatment in self.treatments:
            if treatment.taxon_id not in self.taxa or treatment.evidence_id not in self.evidence:
                raise ValueError(f"Broken treatment references: {treatment.name}")
        for alias in self.aliases.values():
            if set(alias.candidate_ids) - self.taxa.keys():
                raise ValueError(f"Unknown alias candidates: {alias.forms}")
        if self.profile.taxon_id not in self.taxa or self.profile.listing_evidence_id not in self.evidence:
            raise ValueError("Broken profile identity references")
        for claim in self.profile.claims:
            if not claim.evidence_ids or set(claim.evidence_ids) - self.evidence.keys():
                raise ValueError(f"Missing claim evidence: {claim.topic}")
            if set(claim.source_locators) != set(claim.evidence_ids):
                raise ValueError(f"Missing or extra source locators: {claim.topic}")
        for obs in self.observations.values():
            if obs.capture_id not in self.evidence or obs.mapped_concept_id not in self.facets:
                raise ValueError(f"Broken observation references: {obs.raw_label}")
        concepts = set(self.taxa) | self.aliases.keys() | set(self.facets) | self.symptoms.keys()
        for fixture in self.fixtures:
            if set(fixture.expected.concept_ids) - concepts:
                raise ValueError(f"Unknown fixture concepts: {fixture.raw_query}")
            if fixture.expected.profile_id not in (None, self.profile.id):
                raise ValueError(f"Unknown fixture profile: {fixture.raw_query}")
        return self

    def search(self, query: str) -> SearchResult:
        key = normalize(query)
        if key in {normalize(self.profile.listing_label), "پوتوس طلایی"}:
            return SearchResult(route="alias", concept_ids=["pothos", self.profile.taxon_id],
                                profile_id=self.profile.id)
        for alias_id, alias in self.aliases.items():
            if key in {normalize(form) for form in alias.forms}:
                route = {"ambiguous": "disambiguation", "unresolved": "unresolved"}.get(
                    alias.resolution, "alias"
                )
                ids = [alias_id, *alias.candidate_ids] if route != "alias" else [alias_id]
                return SearchResult(route=route, concept_ids=ids)
        for treatment in self.treatments:
            if key == normalize(treatment.name):
                return SearchResult(route=treatment.kind, concept_ids=[treatment.taxon_id],
                                    profile_id=self.profile.id if treatment.taxon_id == self.profile.taxon_id else None)
        if key == "نور کم":
            return SearchResult(route="light_collection", concept_ids=["light"])
        for symptom_id, label in self.symptoms.items():
            if key == normalize(label):
                return SearchResult(route="symptom", concept_ids=[symptom_id])
        return SearchResult(route="no_match", concept_ids=[])


def normalize(text: str) -> str:
    text = unicodedata.normalize("NFKC", text).translate(str.maketrans("يك\u200c", "یک "))
    text = "".join(char for char in text if unicodedata.category(char) != "Mn")
    return " ".join(text.casefold().split())


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def build(root=ROOT) -> Dataset:
    directory = root / "research" / "batches"
    first, second, third, fourth = (load_json(directory / f"batch-{number:02}.json") for number in (1, 2, 3, 4))
    reports = []
    for batch in (first, second, third, fourth):
        report = (directory / batch["report"]).resolve()
        if not report.is_file():
            raise ValueError(f"Missing report: {report}")
        reports.append(report.relative_to(root).as_posix())
    evidence = {key: Evidence(url=url, provenance="reported") for key, url in first["sources"].items()}
    taxa = {entry["ipni_id"]: "species" for entry in second["taxa"]}
    taxa.update({"77306988-1": "species", "genus-alocasia": "genus"})
    names = {entry["name"]: entry["ipni_id"] for entry in second["taxa"]}
    names.update({"Philodendron bipinnatifidum": "77306988-1", "Alocasia": "genus-alocasia"})
    treatments = []
    for name, taxon_id in names.items():
        if taxon_id == "genus-alocasia":
            continue
        evidence_id = f"powo-{taxon_id}"
        evidence[evidence_id] = Evidence(
            url=f"https://powo.science.kew.org/taxon/urn:lsid:ipni.org:names:{taxon_id}",
            provenance="reported",
        )
        treatments.append(Treatment(taxon_id=taxon_id, name=name, authority="Kew POWO",
                                    kind="scientific_name", evidence_id=evidence_id))
    for name, taxon_id, kind in (
        ("Sansevieria trifasciata", "77164235-1", "scientific_synonym"),
        ("Scindapsus aureus", "87014-1", "scientific_synonym"),
        ("Pothos aureus", "87014-1", "scientific_synonym"),
        ("Thaumatophyllum bipinnatifidum", "77306988-1", "alternative_treatment"),
    ):
        treatments.append(Treatment(taxon_id=taxon_id, name=name,
                                    authority="2018 treatment (reported)" if kind == "alternative_treatment" else "Kew POWO",
                                    kind=kind, evidence_id=f"powo-{taxon_id}",
                                    research_basis=reports[1] if kind == "alternative_treatment" else None))
    aliases = {
        entry["id"]: Alias(forms=entry["forms"], resolution=entry["resolution"],
                           candidate_ids=[names[item["name"]] for item in entry["candidates"]],
                           report=reports[0])
        for entry in first["aliases"]
    }
    aliases["zz"].forms.append("زامفولیا")
    aliases["baba-adam"].forms.append("باباآدم")
    pilot = third["pilot"]
    listing = next(capture for capture in first["seller_captures"] if "پتوس طلایی" in capture["raw_labels"])
    evidence["nargil-golden-pothos"] = Evidence(
        url=listing["url"], provenance="reported", locator="پتوس طلایی"
    )
    publication = load_json(root / "research" / "publication.json")
    for key, source in publication["evidence"].items():
        if key not in evidence:
            raise ValueError(f"Unknown publication evidence ID: {key}")
        record = Evidence.model_validate({**evidence[key].model_dump(), **source})
        if record.archive:
            record.archive.check_file(root)
        evidence[key] = record
    claims = [Claim(id=item["id"], topic=item["topic"], wording={"en": item["en"], "fa": item["fa"]},
                    evidence_ids=list(item["evidence"]), source_locators=item["evidence"],
                    animal_species=item.get("animal_species", []),
                    reviews=publication["reviews"].get(item["id"], {}),
                    research_record="research/batches/batch-04.json", research_pointer=f"/claims/{index}")
              for index, item in enumerate(fourth["claims"])]
    if publication["reviews"].keys() - {claim.id for claim in claims}:
        raise ValueError("Review references unknown claim ID")
    observations = {}
    for line in (root / "observations.jsonl").read_text(encoding="utf-8").splitlines():
        item = json.loads(line)
        capture_id = f"capture-{item['id']}"
        evidence[capture_id] = Evidence(url=item["url"], provenance=item["status"],
                                        observed_at=item["observed_at"], locator=item["raw_label"])
        observations[item["id"]] = Observation(
            seller=item["seller"], capture_id=capture_id, raw_label=item["raw_label"],
            parent_path=[item["parent_label"]], ui_role=item["ui_role"],
            mapped_concept_id=item["proposed_concept_id"],
        )
    fixtures = []
    defaults = {"scientific_synonym": "77164235-1", "light_collection": "light", "symptom": "yellow-leaves"}
    for batch in (first, third):
        for item in batch["search_fixtures"]:
            query, route = item["query"], item["expected_route"]
            ref = item.get("alias_id") or item.get("candidate_ref") or defaults.get(route)
            ids = [ref]
            if route == "disambiguation":
                ids.extend(["87478-1", "77306988-1"])
            elif route == "unresolved":
                ids.append("genus-alocasia")
            fixtures.append(Fixture(raw_query=query, locale="en" if query.isascii() else "fa-IR",
                                    expected=SearchResult(route=route, concept_ids=ids,
                                                          profile_id=pilot["profile_id"] if ref == "87014-1" else None)))
    kew = pilot["asset_candidate"]
    ncstate = fourth["media_candidate"]
    images = {
        "kew-gallery": ImageCandidate(source_page=kew["page_url"], creator=kew["reported_credit"],
                                     license=kew["reported_license"], asset_url=kew["asset_url"],
                                     asset_status=kew["publication_status"]),
        "ncstate-dell-enecks": ImageCandidate(
            source_page=first["sources"][ncstate["source_id"]], creator=ncstate["creator"],
            license=ncstate["license_url"], locator=ncstate["locator"], filename=ncstate["filename"],
            asset_status=ncstate["asset_status"],
        ),
    }
    presentations = [PresentationObservation.model_validate(item)
                     for item in load_json(directory / "product-presentation-audit.json")]
    return Dataset(taxa=taxa, evidence=evidence, treatments=treatments, aliases=aliases,
                   profile=Profile(id=pilot["profile_id"], taxon_id="87014-1", claims=claims,
                                   image_candidates=images, preferred_image_id="ncstate-dell-enecks",
                                   listing_label="پتوس طلایی", listing_evidence_id="nargil-golden-pothos"),
                   facets=list(load_json(root / "taxonomy.json")["facets"]),
                   symptoms={"yellow-leaves": "زرد شدن برگ"}, observations=observations, fixtures=fixtures,
                   presentation_observations=presentations)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["validate", "export", "schema", "search"])
    parser.add_argument("query", nargs="?")
    args = parser.parse_args()
    if args.command == "schema":
        print(json.dumps(Dataset.model_json_schema(), indent=2))
        return
    dataset = build()
    if args.command == "export":
        print(dataset.model_dump_json(indent=2))
    elif args.command == "search":
        if not args.query:
            parser.error("search requires a query")
        print(dataset.search(args.query).model_dump_json(indent=2))
    else:
        for fixture in dataset.fixtures:
            actual = dataset.search(fixture.raw_query)
            if actual != fixture.expected:
                raise SystemExit(f"{fixture.raw_query!r}: expected {fixture.expected}, got {actual}")
        print(f"Validated {len(dataset.observations)} observations and "
              f"{len(dataset.presentation_observations)} presentation records. "
              f"Ran {len(dataset.fixtures)} search fixtures.")


if __name__ == "__main__":
    main()
