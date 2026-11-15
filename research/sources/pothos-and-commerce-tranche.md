# FlowerMarketOntology Research Tranche: Pothos, Ambiguous Trade Names, Search Readiness, and Commerce Evidence

This tranche follows the uploaded **Deep Research prompt for FlowerMarketOntology** as the governing scope and the latest roadmap as the release gate: reproducible pothos evidence first; diagnostic examples for «بابا آدم» and «برگ‌انجیری»; genuine mobile/user testing rather than simulated claims; and separation of seller, vendor, and wholesale evidence. fileciteturn0file0 fileciteturn0file1 The repository files named in the governing prompt—such as `README.md`, `knowledge-map.md`, `taxonomy.json`, `ontology.py`, and the earlier research batches—were not accessible in full in this research environment, so “new/confirm/conflict” judgments below are relative to the uploaded prompt and roadmaps rather than a fresh line-by-line audit of the repository.

iturn506144image0

## Executive delta

The strongest publication-ready result is the **golden pothos care layer**. Kew currently accepts *Epipremnum aureum* (Linden & André) G.S.Bunting and preserves older names including *Pothos aureus*, *Rhaphidophora aurea*, *Scindapsus aureus*, and *Epipremnum mooreense*. Kew also records historical treatment around *E. pinnatum* ‘aureum’, which makes those names useful search aliases but not suitable as the preferred display name. citeturn670481view3 NC State independently uses *Epipremnum aureum* and notes that it was formerly treated as *E. pinnatum* ‘Aureum’. citeturn670481view1

The care evidence now supports a more precise ontology distinction between **preference** and **tolerance**. Golden pothos prefers bright indirect light but tolerates some shade or prolonged lower-light conditions; insufficient light can reduce variegation or growth quality. citeturn940555view0turn670481view1 Watering is better represented as a substrate-state trigger—water as the compost approaches dryness—rather than a fixed calendar interval, while prolonged saturation or standing water raises root-rot risk. citeturn940555view2 Humidity should no longer be encoded as a categorical “high humidity required” claim: RHS explicitly says these plants do not require high humidity, whereas NC State suggests a humidifier or wet pebble tray as an optional cultural measure. The safest ontology representation is therefore **ordinary indoor humidity usually sufficient; supplemental humidity is conditional rather than mandatory**. citeturn670481view0turn670481view1

The toxicity wording can also be tightened substantially. ASPCA identifies golden pothos as toxic specifically to **cats and dogs**, attributes the effect to insoluble calcium oxalates, and lists oral irritation, burning of the mouth/tongue/lips, drooling, vomiting, and difficulty swallowing. The publication layer should not silently generalize this particular citation to “all pets.” citeturn670481view2

For the ambiguous Persian names, the evidence confirms that the project was right not to force one-to-one mappings. Iranian commerce commonly uses «برگ انجیری» for *Monstera deliciosa*, but sellers also apply related wording such as «برگ انجیری فر» and «برگ انجیری مینیاتوری» to split-leaf philodendron-like plants. citeturn579861search5turn579861search12turn579861search13 «بابا آدم» likewise behaves as a retail group label rather than a species-level identifier: seller pages associate it broadly with *Alocasia*, while individual modifiers may point toward *A. macrorrhizos*, *A. zebrina*, *A. baginda* ‘Dragon Scale’, *A. cuprea* ‘Red Secret’, or other horticultural entities. citeturn579861search0turn579861search8

A second important ontology delta concerns the split-leaf philodendron. Current Kew POWO accepts *Philodendron bipinnatifidum* Schott ex Endl. and places *Thaumatophyllum bipinnatifidum* in synonymy, while Kew also records that the latter name was accepted under an alternative World Checklist treatment; IPNI independently records both nomenclatural names and their relationship. citeturn577908search1turn577908search3turn577908search0turn577908search4 The data model therefore needs **versioned taxonomic treatments**, not a destructive rename from one scientific string to another.

The commerce work closed two concrete gaps. The requested Mashhad Telegram post is recoverable as `https://t.me/floristshopmashhad/648`, and the requested VIPShop basket is `https://vipshop.flowers/product/flower-basket-no-133/`. The Mashhad post markets a «بابا آدم» specimen by container/height rather than a scientific identity; the VIPShop K133 page exposes ingredient counts, dimensions, price, and product-level substitution language. citeturn314694view0turn123165view2

The main unresolved release blockers remain exactly where the roadmap expects them: no genuine two-device mobile test or human pilot could be performed with the available research tools; no permissioned seller-photo acquisition was conducted; no physical Mahallati or Imam Reza/Khavaran market visit occurred; and no dated in-person vendor measurements should therefore be represented as completed. The latest roadmap explicitly makes those live observations part of the exit criteria rather than desk-research substitutes. fileciteturn0file1

## Golden pothos bilingual pilot

The proposed publication record should separate identity, environment preference, tolerated conditions, action trigger, hazard, and editorial synthesis. That prevents phrases such as “low-light plant” or “likes humidity” from becoming decontextualized truths.

| Stable claim ID | Topic | Evidence-backed English wording | Reviewed Persian wording | Status and locator |
|---|---|---|---|---|
| `care.pothos.identity.001` | Identity | **Golden pothos — *Epipremnum aureum* (Linden & André) G.S.Bunting.** | **پتوس طلایی — *Epipremnum aureum* (Linden & André) G.S.Bunting** | `verified`; Kew accepted-name block and synonym section. citeturn670481view3 |
| `care.pothos.light.001` | Light | **Best in bright, indirect light. It tolerates lower light, but growth may slow and variegation may become less distinct. Avoid strong direct sun.** | **بهترین رشد را در نور زیادِ غیرمستقیم دارد. نور کمتر را تحمل می‌کند، اما ممکن است رشد کندتر شود و ابلقی برگ‌ها کاهش پیدا کند. از آفتاب مستقیمِ شدید دور نگه دارید.** | `verified`; RHS light section, lines represented in retrieved passage 104–110; NC State description/ID notes. citeturn940555view0turn670481view1 |
| `care.pothos.water.001` | Water | **Water when the potting mix is approaching dryness; check the mix rather than relying on a fixed schedule. Do not leave the roots continuously wet or the pot standing in water.** | **وقتی بستر به سمت خشک‌شدن می‌رود آبیاری کنید؛ به‌جای برنامهٔ ثابت، رطوبت بستر را بررسی کنید. ریشه‌ها را دائماً خیس نگه ندارید و اجازه ندهید گلدان در آب بماند.** | `verified`; RHS watering passage 116–124. citeturn940555view2 |
| `care.pothos.humidity.001` | Humidity | **Average indoor humidity is usually sufficient. Extra humidity may be useful in an unusually dry room, but high humidity is not a requirement.** | **رطوبت معمول فضای خانه معمولاً کافی است. در محیط بسیار خشک می‌توان رطوبت را کمی افزایش داد، اما رطوبت بالا الزام نگهداری نیست.** | `verified` evidence + `editorial_synthesis`; RHS says high humidity is not required; NC State suggests supplemental humidity. citeturn670481view0turn670481view1 |
| `care.pothos.substrate.001` | Substrate | **Use an airy, moisture-retentive but well-drained, slightly acidic potting mix.** | **از بستری سبک و هواخور، با توان نگهداری مقداری رطوبت اما زهکشی خوب و واکنش کمی اسیدی استفاده کنید.** | `verified`; RHS compost/repotting section 80–97. citeturn670481view0 |
| `care.pothos.repot.001` | Repotting | **Repot when roots crowd the container or emerge from drainage holes; normally increase only one pot size at a time. Oversized pots can keep the mix wet for too long.** | **وقتی ریشه‌ها گلدان را پر کرده‌اند یا از سوراخ‌های زهکش بیرون می‌آیند تعویض گلدان انجام دهید؛ معمولاً فقط یک سایز بزرگ‌تر انتخاب کنید. گلدان بیش‌ازحد بزرگ می‌تواند بستر را مدت زیادی خیس نگه دارد.** | `verified`; RHS repotting section 80–97. citeturn670481view0 |
| `care.pothos.tox.catdog.001` | Toxicity | **Toxic to cats and dogs if chewed or eaten. Insoluble calcium oxalates can cause oral irritation, drooling, vomiting and difficulty swallowing. This citation does not establish the same risk statement for every animal species.** | **در صورت جویدن یا خوردن، برای گربه و سگ سمی است. بلورهای نامحلول اگزالات کلسیم می‌توانند باعث تحریک و سوزش دهان، آبریزش دهان، استفراغ و دشواری در بلع شوند. این منبع به‌تنهایی مبنای تعمیم حکم به همهٔ جانوران نیست.** | `verified`; ASPCA species/toxin/clinical-sign fields. citeturn670481view2 |

The stable identity URL is:

`https://powo.science.kew.org/taxon/urn:lsid:ipni.org:names:87014-1`

The principal care URL is:

`https://www.rhs.org.uk/plants/epipremnum/growing-guide`

The NC State horticultural profile is:

`https://plants.ces.ncsu.edu/plants/epipremnum-aureum/`

The animal-toxicity record is:

`https://www.aspca.org/pet-care/aspca-poison-control/toxic-and-non-toxic-plants/golden-pothos`

These four sources have different evidentiary roles: Kew for taxonomic identity, RHS and NC State for horticultural culture, and ASPCA for species-specific companion-animal toxicity. citeturn670481view3turn670481view0turn670481view1turn670481view2

The image-rights audit yields one usable candidate but not yet a fully pinned production asset. NC State's profile labels a Dell Enecks pothos photograph as **CC BY 4.0** and separately lists another Matt Stevens photograph under CC BY 4.0; it also labels a Sergei image CC0. citeturn670481view1 Under the official CC BY 4.0 deed, reuse and adaptation, including commercial reuse, are permitted provided the license conditions such as attribution are followed. citeturn286338search1turn286338search15 The direct signed download endpoint encountered during this capture returned an access failure, so the asset itself is not yet safely pinned into the project archive. The correct status is therefore **license label verified; separate permission not requested; publication asset retrieval/archival pending**, not “photo permission obtained.”

A candidate media record is:

```json
{
  "id": "media.pothos.ncstate.dell-enecks.001",
  "type": "media_candidate",
  "taxon_id": "taxon.epipremnum-aureum",
  "source_url": "https://plants.ces.ncsu.edu/plants/epipremnum-aureum/",
  "source_locator": "image gallery; Dell Enecks entry; retrieved profile lines 47-50",
  "creator": "Dell Enecks",
  "observed_asset_name": "Pothos_Dell_Enecks_m7ECuAQTwlEH.jpeg",
  "license_label": "CC BY 4.0",
  "license_url": "https://creativecommons.org/licenses/by/4.0/",
  "reuse_scope": "commercial and noncommercial reuse/adaptation subject to CC BY 4.0 conditions",
  "separate_permission": "not_requested",
  "asset_archive_status": "pending",
  "direct_asset_fetch": "unavailable_in_capture",
  "evidence_status": "verified",
  "editorial_status": "candidate_not_published"
}
```

Retail pothos text should not be elevated into the care layer merely because it resembles authoritative guidance. Nargil's golden-pothos page contains care and promotional statements, but those are useful as **retail-language evidence**, not as the authority for publication care claims. citeturn123165view3 In particular, broad marketing statements about pest resistance or air-related benefits should remain seller observations unless independently supported for the exact claim and conditions.

## Identity, Persian vocabulary, and diagnostic examples

The identity layer needs to distinguish **trade label**, **candidate taxon**, **taxonomic treatment**, **cultivar**, and **appearance modifier**. That distinction is especially important in Persian because a visually evocative name can act like a category rather than a botanical identifier.

For «برگ‌انجیری», Kew accepts *Monstera deliciosa*, and Kew's synonymy includes historical names such as *Monstera borsigiana* and *M. deliciosa* var. *borsigiana*. citeturn101580search0 Nargil supplies a strong Iranian retail example because an offer explicitly couples «گل برگ انجیری» with “Monstera Deliciosa.” citeturn579861search5 That supports a **high-confidence candidate link** from the unmodified retail term to *M. deliciosa* when the morphology/product context agrees, but it does not justify making «برگ انجیری» a globally exact synonym.

The reason is visible in other Iranian commerce. Anguor uses wording equivalent to “split-leaf philodendron / برگ انجیری فر” and also associates «برگ انجیری مینیاتوری» with a Xanadu-type philodendron. citeturn579861search12turn579861search13 Mahak likewise sells «برگ انجیری غول پیکر (مونسترا)» and «برگ انجیری فر», showing that modifiers can partition visibly different commercial forms without necessarily encoding a formally registered cultivar. citeturn579861search4turn579861search9turn579861search10

The split-leaf philodendron taxonomic history is itself version-sensitive. Current Kew treatment accepts *Philodendron bipinnatifidum*, while Kew records *Thaumatophyllum bipinnatifidum* as a synonym and notes that the latter was accepted in an alternative checklist treatment. citeturn577908search1turn577908search3 IPNI provides a stable nomenclatural record for *Thaumatophyllum bipinnatifidum* at `urn:lsid:ipni.org:names:77178497-1` and for *Philodendron bipinnatifidum* at `urn:lsid:ipni.org:names:77306988-1`. citeturn577908search0turn577908search4 An ontology entry should therefore preserve both strings, the authority/version that considers each accepted or synonymous, and the dates of those treatments.

For «بابا آدم», seller evidence strongly favors a **genus/group interpretation** until additional morphology is available. Nargil labels a page «آلوکازیا - بابا آدم», while another Iranian seller presents a family of “بابا آدم” products attached to several *Alocasia* names. citeturn579861search0turn579861search8 Kew separately accepts *Alocasia macrorrhizos* and *Colocasia esculenta*, two taxa relevant to the broader elephant-ear trade-name problem, which is why the Persian common name should not be hard-wired to one species without an identified specimen. citeturn101580search4turn101580search3

The Mashhad seller post provides a useful provenance-controlled retail example rather than a botanical identification: post `648` advertises «بابا آدم» with a stated container/height and delivery by Snapp, but does not supply a scientific determination. citeturn314694view0 That record should be classified **trade-name observation, candidate taxon unresolved**, not expert identification.

| Persian term as observed | Recommended ontology treatment | Candidate identity | Modifier interpretation | Confidence |
|---|---|---|---|---|
| «برگ انجیری» | Ambiguous trade label with ranked candidate links | *Monstera deliciosa* usually first candidate when matching fenestrated Monstera morphology | none | High for candidate, not exact synonym. citeturn579861search5turn101580search0 |
| «برگ انجیری فر» | Separate retail alias requiring disambiguation | split-leaf philodendron/*Philodendron bipinnatifidum* treatment possible | «فر» = appearance/trade modifier unless seller supplies a cultivar | Medium. citeturn579861search12turn577908search1 |
| «برگ انجیری غول پیکر» | Product/appearance label | frequently Monstera in observed seller context | «غول پیکر» = size/appearance unless backed by a cultivar source | Medium-high for the cited product only. citeturn579861search10 |
| «برگ انجیری مینیاتوری» | Ambiguous retail alias | Xanadu-type philodendron in observed seller context | «مینیاتوری» = size/trade descriptor | Medium; seller-scoped only. citeturn579861search13 |
| «بابا آدم» | Trade-group label; do not resolve to species automatically | *Alocasia* spp.; potentially other elephant-ear taxa depending specimen | none | High at group level, low at species level. citeturn579861search0turn579861search8 |
| «بابا آدم غول‌پیکر» | Seller-scoped candidate link | *Alocasia macrorrhizos* in the cited seller's taxonomy | modifier functions as seller's label but also describes scale | Medium. citeturn579861search8turn101580search4 |
| «بابا آدم گورخری» | Seller-scoped candidate link | *Alocasia zebrina* in cited catalog | modifier is a strong species cue on that seller, but still verify specimen | Medium-high on that surface. citeturn579861search8 |
| «ابلق» | Appearance attribute by default | no cultivar implication by itself | variegated appearance | High as editorial rule; Tarhegol uses it in names such as «پتوس ابلق». citeturn199253search0 |
| «مرمری» | Trade/appearance modifier pending cultivar evidence | may evoke a named marble-type pothos in commerce, but seller wording alone is insufficient | appearance/trade | Medium-low for cultivar identity. citeturn199253search0 |

The required next identification evidence is therefore not “more seller names” alone. A publication-quality example should carry at least one of: a botanical-garden/herbarium or horticultural-authority determination; an expert determination tied to a particular photographed specimen; or a permissioned seller photograph with diagnostic features and a documented reviewer decision. None of the seller photographs gathered in this tranche should be represented as permissioned simply because they are publicly viewable.

A useful schema change is:

```json
{
  "trade_name_observation": {
    "raw_label": "string",
    "locale": "fa-IR",
    "seller_id": "string|null",
    "surface_url": "string",
    "candidate_taxa": [
      {
        "taxon_id": "string",
        "confidence": 0.0,
        "basis": "seller_text|morphology|expert_determination|authority_crosswalk"
      }
    ],
    "modifier_tokens": [
      {
        "text": "string",
        "role": "cultivar|appearance|size|marketing|uncertain",
        "evidence_ref": "string"
      }
    ],
    "identification_precision": "species|genus|trade_group|unresolved",
    "provenance": "string",
    "evidence_status": "verified|reported|unavailable"
  }
}
```

## Search, symptom evidence, and diagnostic readiness

No genuine two-configuration mobile test or human pilot was completed in this environment. Web retrieval is not an acceptable substitute for viewport interaction, Persian-keyboard behavior, ranking inspection, correction behavior, or human task performance. Accordingly, the status for this roadmap gate is **`unavailable` for completed live testing / `pending` for execution**, consistent with the governing requirement not to fabricate tests. fileciteturn0file0 fileciteturn0file1

The reproducible mobile protocol should use two genuinely different stacks rather than two resized desktop windows: one current iPhone-class device using Safari and a Persian keyboard, and one current Android device using Chrome and a Persian keyboard. For every query, record device model, OS/browser version, viewport, locale, keyboard, exact Unicode query string, top ten results, zero-result state, spelling correction, ambiguity prompt, clicked result, time to find the intended plant, and time to locate one watering instruction. A small pilot should assign the same discovery tasks to multiple users and retain failures rather than reporting only successful paths.

The minimum fixture set should include the roadmap strings plus historical and ambiguity-sensitive aliases:

```json
[
  {"q": "پتوس طلایی", "intent": "exact_trade_name"},
  {"q": "پوتوس طلایی", "intent": "spelling_variant"},
  {"q": "پتوس", "intent": "broad_trade_name"},
  {"q": "Epipremnum aureum", "intent": "accepted_scientific_name"},
  {"q": "Scindapsus aureus", "intent": "legacy_scientific_name"},
  {"q": "Epipremnum pinnatum Aureum", "intent": "legacy_treatment"},
  {"q": "برگ انجیری", "intent": "ambiguous_trade_name"},
  {"q": "برگ‌انجیری", "intent": "zwnj_variant"},
  {"q": "برگ انجیری فر", "intent": "split_leaf_ambiguity"},
  {"q": "مونسترا", "intent": "transliterated_genus"},
  {"q": "مانسترا", "intent": "spelling_variant"},
  {"q": "Monstera deliciosa", "intent": "accepted_scientific_name"},
  {"q": "Philodendron selloum", "intent": "legacy_trade_scientific_name"},
  {"q": "Philodendron bipinnatifidum", "intent": "current_kew_treatment"},
  {"q": "Thaumatophyllum bipinnatifidum", "intent": "alternative_taxonomic_treatment"},
  {"q": "بابا آدم", "intent": "ambiguous_trade_group"},
  {"q": "باباآدم", "intent": "spacing_variant"},
  {"q": "آلوکازیا", "intent": "genus_trade_name"},
  {"q": "نور کم", "intent": "condition_discovery"},
  {"q": "زرد شدن برگ", "intent": "symptom_discovery"}
]
```

The scientific-name fixtures are justified by the documented Kew/IPNI synonym and treatment history rather than arbitrary keyword expansion. citeturn670481view3turn577908search1turn577908search3 Search normalization should fold spacing and ZWNJ variants where doing so preserves meaning, but it should **not** collapse ambiguous Persian common names onto a single taxon.

The symptom research likewise argues against premature one-symptom/one-cause rules. In a University of Florida/IFAS pothos disease guide, Phytophthora root rot, ethylene injury, bacterial wilt, Rhizoctonia disease, chemical injury, and manganese toxicity produce overlapping visible signs such as yellowing, wilting, browning, spotting, or necrosis under different environmental histories. The publication is oriented to commercial/greenhouse production rather than apartment diagnosis, so these are mechanistic reference cases, not direct household diagnoses. citeturn875547view0turn875547view1turn875547view2

For example, the UF/IFAS material describes apparent wilt from ethylene even when soil moisture is adequate, with ventilation/heater/shipping context helping distinguish it from drought; it describes bacterial wilt together with vascular discoloration; and it links manganese toxicity to yellow flecking/spotting under conditions including excessive micronutrients, very acidic substrate, or manganese-containing treatments. citeturn875547view0turn875547view1turn875547view2 Penn State's houseplant guidance similarly treats root rot and foliar spotting as condition-dependent problems rather than diagnoses inferred from one visible symptom. citeturn899739search2

The future troubleshooting record should therefore require contextual fields before any diagnostic ranking is emitted:

```json
{
  "symptom_case_id": "symptom.case.<stable-id>",
  "plant_identity": {
    "profile_id": null,
    "confidence": null
  },
  "symptoms": ["yellowing", "wilt", "leaf_spot"],
  "onset": null,
  "progression": null,
  "substrate_moisture": null,
  "watering_history": null,
  "drainage": null,
  "light_exposure": null,
  "recent_light_change": null,
  "root_condition": null,
  "pest_evidence": null,
  "temperature_or_transport_event": null,
  "fertilizer_or_chemical_event": null,
  "affected_leaf_age": null,
  "competing_causes": [],
  "diagnostic_status": "insufficient_evidence",
  "evidence_refs": []
}
```

No real user symptom cases satisfying those fields were collected here; that roadmap item remains pending. The immediate design implication is to build a **question sequence and uncertainty model**, not a deterministic “yellow leaf = overwatering” rule.

## Seller, delivery, and wholesale audit

The exact VIPShop product requested in the roadmap is now recovered as:

`https://vipshop.flowers/product/flower-basket-no-133/`

The live product page identifies “سبد گل K133”, displays a price of 10,700,000 toman in the retrieved capture, and specifies an ingredient composition of 6 Strelitzia, 4 Alstroemeria, 15 carnations, and 20 chrysanthemums, along with dimensions. citeturn123165view2 Its product-level wording also says decorative leaves may change with stock and that unavailable seasonal flowers may be replaced with equal-value flowers compatible with the arrangement's color, quality, and style. citeturn123165view2 That is materially better ontology evidence than a generic florist FAQ because the substitution rule is tied to a concrete product surface.

VIPShop's own general surfaces additionally advertise date/time selection, same-day service for many products, and free Tehran delivery subject to stated range conditions. citeturn199253search3turn199253search4 These should be stored separately from K133's product-specific substitution terms.

The Mashhad «بابا آدم» post permalink is:

`https://t.me/floristshopmashhad/648`

The post is a direct seller-channel observation with an offered plant, size/container language, price context, and Snapp delivery wording; it is not an expert botanical identification. citeturn314694view0 A related seller care post is available at `https://t.me/floristshopmashhad/774`, but its care advice remains retailer-originated content. citeturn314694view2

Nargil needs two commerce entities in the ontology. Its golden-pothos page combines its own content with seller offers, including linked vendor cards; the existence of those cards does not make each vendor's delivery promise a Nargil promise. citeturn199253search1turn123165view3 Nargil's shop surface states online purchasing and a seven-day money-back proposition, but the retrieved official consumer surfaces did not expose a sufficiently precise retail delivery coverage/timing policy to record as a verified nationwide delivery rule. citeturn127712search0turn127712search3 Separately, Nargil's wholesale/project material describes delivery conditions as dependent on order factors such as species, quantity, size, season and destination; that statement belongs to the wholesale/project channel, not the consumer retail policy. citeturn127712search2turn583018search2

The resulting seller audit is:

| Record | Surface | Direct observation | Evidence status | Ontology implication |
|---|---|---|---|---|
| `seller.tarhegol.home.001` | Tarhegol homepage/catalog | «پتوس ابلق», «پتوس مرمری» and apartment-plant/light grouping observed | `verified` | Retain raw modifiers; do not promote them to cultivars without cultivar evidence. citeturn199253search0 |
| `seller.nargil.pothos.001` | Nargil golden-pothos page | Retail care text plus vendor offers | `verified` direct page observation; content itself is retailer-authored | Separate editorial content from offer/vendor entity. citeturn123165view3turn199253search1 |
| `seller.nargil.delivery.retail.001` | Nargil own retail policy | No precise consumer delivery rule recovered from inspected official pages | `unavailable` | Keep null rather than inheriting vendor terms. citeturn127712search0turn127712search3 |
| `seller.nargil.delivery.project.001` | Nargil wholesale/project channel | Delivery conditions vary with order characteristics | `verified`, project/wholesale scope only | Model channel scope explicitly. citeturn127712search2turn583018search2 |
| `seller.vipshop.k133.001` | Product detail | ingredient counts, dimensions, displayed price, substitution conditions | `verified` | Product-level substitution belongs on bouquet product record. citeturn123165view2 |
| `seller.mashhad.telegram.648` | Telegram seller post | «بابا آدم» product offer and Snapp delivery | `verified` retail observation | Trade-name evidence; identity unresolved. citeturn314694view0 |

No physical wholesale visit was made. The desk research did recover two useful but differently scoped series. Rezvan Flower identifies a presence at Tehran's Mahallati market and has published a market price table with named selling units for flowers such as gladiolus, narcissus, anthurium, lilies, roses, chrysanthemums, carnations, gerbera, and Alstroemeria. citeturn912327search1turn912327search0 Because that material is seller-published and not an observation made on November 13, 2026, it must be stored as an **indexed vendor-attributed historical lead**, not as a current field price.

For Imam Reza/Khavaran, the searchable “بازار گل امام رضا” channel contains dated Solar Hijri price lists and explicitly uses commercial units such as 50 stems for gladiolus, 5 stems for Oriental lily, 20 for Dutch roses, 10 for spray roses, 25 for tuberose, and 20 for sunflower; the channel also advertises shipment around the country. citeturn912327search2turn912327search3 Again, this is an online vendor/channel series rather than an in-person market observation.

The field protocol required to close the roadmap gate should sample both markets independently on at least two dates and preserve vendor attribution, permission, timestamp, exact original currency expression, flower/type, cultivar or grade if stated, stem length where relevant, bundle/stem count, origin, quality grade, availability, and selling unit. Price comparisons should be made only between equivalent units and grades; a 20-stem rose pack must not be compared numerically with a per-stem quote without an explicit normalized calculation. This requirement follows the roadmap's emphasis on dated, vendor-attributed, comparable observations rather than anonymous market anecdotes. fileciteturn0file1

The four requested screen roles can now be tightened as **design proposals**, not observed facts. The plant directory should surface the Persian trade name first, scientific identity second, and an ambiguity badge when multiple candidates exist. A care profile should show preference versus tolerance, watering trigger, conditional warnings, and claim provenance. A live-plant product detail should keep seller identity, actual pot/height/unit, stock and delivery separate from botanical truth. A bouquet detail should elevate ingredient counts, dimensions, substitutions and delivery because VIPShop demonstrates that those terms can alter what the buyer actually receives. citeturn123165view2

## Structured evidence package, unresolved questions, and release gates

The following records are JSONL-ready and preserve the requested distinction among direct observation, reported content, inference, and unavailable evidence. URLs are explicit rather than hidden behind citation tokens so the package can be imported or archived independently.

```json
{"id":"evidence.pothos.kew.identity.001","record_type":"evidence","subject_id":"taxon.epipremnum-aureum","source_url":"https://powo.science.kew.org/taxon/urn:lsid:ipni.org:names:87014-1","locator":"accepted-name block; synonym section","capture_method":"direct_web_observation","locale":"en","scope":"taxonomy","evidence_status":"verified","editorial_status":"approved_candidate","claim":"Epipremnum aureum (Linden & André) G.S.Bunting is the accepted name; historical synonyms are retained."}
{"id":"identity.pothos.001","record_type":"identity_treatment","profile_id":"plant.epipremnum-aureum","preferred_scientific_name":"Epipremnum aureum","authority":"(Linden & André) G.S.Bunting","authority_id":"urn:lsid:ipni.org:names:87014-1","preferred_fa":"پتوس طلایی","preferred_en":"golden pothos","precision":"species","evidence_status":"verified"}
{"id":"alias.pothos.scindapsus-aureus.001","record_type":"alias","profile_id":"plant.epipremnum-aureum","alias":"Scindapsus aureus","alias_role":"historical_scientific_synonym","searchable":true,"display_as_preferred":false,"source_url":"https://powo.science.kew.org/taxon/urn:lsid:ipni.org:names:87014-1","evidence_status":"verified"}
{"id":"care.pothos.light.001","record_type":"care_claim","profile_id":"plant.epipremnum-aureum","topic":"light","preference":"bright indirect light","tolerance":"some lower light","condition":"lower light may reduce growth quality or variegation; strong direct sun should be avoided","source_url":"https://www.rhs.org.uk/plants/epipremnum/growing-guide","locator":"light section; retrieved passage 104-110","evidence_status":"verified","editorial_status":"reviewed_wording"}
{"id":"care.pothos.water.001","record_type":"care_claim","profile_id":"plant.epipremnum-aureum","topic":"watering","trigger":"potting mix approaching dryness","avoid":"continuous saturation or standing water","source_url":"https://www.rhs.org.uk/plants/epipremnum/growing-guide","locator":"watering section; retrieved passage 116-124","evidence_status":"verified","editorial_status":"reviewed_wording"}
{"id":"care.pothos.humidity.001","record_type":"care_claim","profile_id":"plant.epipremnum-aureum","topic":"humidity","recommendation":"average indoor humidity usually sufficient; supplemental humidity conditional in unusually dry rooms","source_urls":["https://www.rhs.org.uk/plants/epipremnum/growing-guide","https://plants.ces.ncsu.edu/plants/epipremnum-aureum/"],"locator":"RHS overview/humidity passage; NC State description","claim_type":"editorial_synthesis_from_verified_sources","evidence_status":"verified","editorial_status":"reviewed_wording"}
{"id":"care.pothos.toxicity.catdog.001","record_type":"care_claim","profile_id":"plant.epipremnum-aureum","topic":"toxicity","animals":["cat","dog"],"toxic":true,"toxic_principle":"insoluble calcium oxalates","signs":["oral irritation","burning of mouth/tongue/lips","drooling","vomiting","difficulty swallowing"],"source_url":"https://www.aspca.org/pet-care/aspca-poison-control/toxic-and-non-toxic-plants/golden-pothos","locator":"scientific name, toxicity and clinical-sign fields","evidence_status":"verified","editorial_status":"reviewed_wording"}
{"id":"identity.fa.barg-anjiri.001","record_type":"candidate_link","raw_label":"برگ انجیری","locale":"fa-IR","candidate_taxon":"Monstera deliciosa","precision":"trade_name_to_candidate_species","confidence":"high_candidate_not_exact_synonym","basis":"Iranian seller explicitly pairs trade label with Monstera deliciosa; authority confirms accepted taxon","evidence_status":"verified"}
{"id":"identity.fa.barg-anjiri-far.001","record_type":"candidate_link","raw_label":"برگ انجیری فر","locale":"fa-IR","candidate_taxon":"Philodendron bipinnatifidum","alternative_name":"Thaumatophyllum bipinnatifidum","precision":"ambiguous_trade_name","confidence":"medium","modifier":{"text":"فر","role":"appearance_or_trade"},"evidence_status":"verified","editorial_status":"needs_specimen_review"}
{"id":"identity.fa.baba-adam.001","record_type":"candidate_link","raw_label":"بابا آدم","locale":"fa-IR","candidate_taxa":["Alocasia spp.","Alocasia macrorrhizos"],"precision":"trade_group","confidence":"high_at_group_low_at_species","evidence_status":"verified","editorial_status":"unresolved_species"}
{"id":"taxonomy.split-leaf.001","record_type":"identity_treatment","concept_id":"plant.split-leaf-philodendron","kew_current_accepted":"Philodendron bipinnatifidum","ipni_id_current_kew_name":"urn:lsid:ipni.org:names:77306988-1","alternative_name":"Thaumatophyllum bipinnatifidum","ipni_id_alternative":"urn:lsid:ipni.org:names:77178497-1","treatment_rule":"retain versioned authority treatments; never silently rewrite historical records","evidence_status":"verified"}
{"id":"seller.vipshop.k133.001","record_type":"seller_observation","seller":"VIPShop","market":"Iran","locale":"fa-IR","source_url":"https://vipshop.flowers/product/flower-basket-no-133/","locator":"product title/price/ingredients/dimensions and shipping-substitution sections","capture_method":"direct_web_observation","evidence_status":"verified","product_label":"سبد گل K133","substitution_scope":"seasonally unavailable flowers may be replaced with equal-value flowers compatible with color, quality and style"}
{"id":"seller.mashhad.telegram.648","record_type":"seller_observation","seller":"floristshopmashhad","market":"Mashhad","locale":"fa-IR","source_url":"https://t.me/floristshopmashhad/648","locator":"Telegram post 648","capture_method":"direct_web_observation","raw_label":"بابا آدم","identity_precision":"unresolved_trade_name","evidence_status":"verified"}
{"id":"seller.nargil.delivery.retail.001","record_type":"commerce_evidence","seller":"Nargil","channel":"consumer_retail","claim":"precise delivery coverage/timing","source_url":"https://nargil.ir/","capture_method":"official-site search and page inspection","evidence_status":"unavailable","value":null,"note":"Do not inherit linked-vendor delivery terms."}
{"id":"seller.nargil.delivery.project.001","record_type":"commerce_evidence","seller":"Nargil","channel":"wholesale_project","claim":"delivery terms depend on species, quantity, size, season and destination","capture_method":"direct_web_observation","evidence_status":"verified","scope":"wholesale_project_only"}
{"id":"wholesale.mahallati.rezvan.lead.001","record_type":"commerce_evidence","market":"Mahallati","vendor":"Rezvan Flower","capture_method":"indexed_vendor_published_page","observation_type":"historical_online_lead","field_visit":false,"evidence_status":"verified","current_price_status":"not_verified_for_2026-11-13"}
{"id":"wholesale.imamreza.channel.series.001","record_type":"commerce_evidence","market":"Imam Reza/Khavaran","vendor_or_channel":"بازار گل امام رضا","capture_method":"direct_web_observation_of_vendor_channel","observation_type":"dated_online_price_series","field_visit":false,"evidence_status":"verified","units_observed":["gladiolus: 50 stems","Oriental lily: 5 stems","Dutch rose: 20 stems","spray rose: 10 stems","tuberose: 25 stems","sunflower: 20 stems"]}
{"id":"test.mobile.search.001","record_type":"test_run","test_type":"two_mobile_configurations","actual_devices_used":false,"human_users_used":false,"result":null,"evidence_status":"unavailable","editorial_status":"pending","note":"Protocol supplied; no simulated run is represented as user testing."}
{"id":"field.wholesale.tehran.001","record_type":"field_observation","markets":["Mahallati","Imam Reza/Khavaran"],"visits_completed":0,"result":null,"evidence_status":"unavailable","editorial_status":"pending"}
```

The principal unresolved questions are now narrow enough to manage as release gates rather than open-ended research themes. The exact identity behind any individual «بابا آدم» listing remains unresolved unless the specimen is independently determined. The exact meaning of «برگ انجیری فر» remains seller- and specimen-dependent. The project still lacks permissioned diagnostic photographs for both ambiguous labels. The pothos image candidate has a verified open-license label but still needs a stable archived asset and final attribution string. Consumer-level Nargil delivery coverage remains unverified. No true mobile/user pilot, contextualized household symptom cohort, or physical Tehran wholesale sampling has been completed. Those absences should remain `null`/`unavailable`, not be backfilled from retailer prose or search snippets.

The prioritized next actions, mapped to the roadmap exits, are:

| Priority | Action | Decision unlocked | Evidence required | Completion criterion |
|---|---|---|---|---|
| **P0** | Pin one pothos media asset and attribution | Publish bilingual golden-pothos profile with lawful image reuse | Stable archived original; creator; exact license; attribution text; any required source link | Asset can be retrieved from project archive and license/attribution reproduced without relying on a transient signed URL. The current CC BY candidate is not yet at this gate. citeturn670481view1turn286338search1 |
| **P0** | Expert-review two to four «بابا آدم» and «برگ‌انجیری» specimen examples | Enable safe disambiguation cards and image-led identification | Permissioned photos or authority/expert-determined listings with diagnostic features and reviewer identity | Each example has a taxon or explicit unresolved rank, provenance, permission/license, confidence, and distinguishing features. |
| **P1** | Execute the two-device Persian search pilot | Approve search normalization, aliases and ambiguity UX | Actual iOS/Safari and Android/Chrome sessions plus small human pilot | Every fixture has query string, rank/results, correction behavior, task completion and failure notes on both configurations; ambiguous labels do not silently resolve to one taxon. fileciteturn0file1 |
| **P1** | Collect real contextualized symptom cases | Decide whether troubleshooting can move beyond educational prompts | Yellowing, wilt and spot examples with moisture, drainage, exposure, timing, roots/pests and intervention history | Reviewed cases cover competing causes and missing-data scenarios; rules express uncertainty rather than one-to-one symptom mappings. UF/IFAS reference cases can guide field structure but do not fulfill this gate. citeturn875547view0turn875547view1turn875547view2 |
| **P2** | Resolve Nargil consumer delivery directly | Publish reliable seller-delivery comparison | Official consumer shipping/coverage page or documented checkout test | Coverage, timing, exceptions, channel and observation date captured from Nargil itself; linked-vendor policy remains separate. |
| **P2** | Run dated field collection at both Tehran wholesale markets | Support local selling-unit and seasonality ontology | Separate visits, vendor attribution/permission, exact units, grade, stem count, price and currency | At least two comparable dated rounds per market with equivalent units; online Imam Reza and Rezvan records remain a separate series. fileciteturn0file1 |

The immediate release can therefore safely incorporate the golden-pothos identity, bilingual conditional care wording, cat/dog toxicity record, scientific synonym/search aliases, the product-level VIPShop substitution model, the recovered Mashhad permalink, and an ambiguity-preserving identity structure for «بابا آدم» and «برگ‌انجیری». citeturn670481view3turn670481view0turn670481view2turn123165view2turn314694view0 The next release should **not** yet claim validated Persian mobile search behavior, symptom diagnosis, permissioned identification photography, Nargil consumer-delivery coverage, or current in-person Tehran wholesale prices; the governing roadmap explicitly requires evidence of those activities before they cross their respective exit criteria. fileciteturn0file0 fileciteturn0file1