"""Tests for V3 response-model fields on the DataSource entity.

Additive fields only — every assertion covers a field that did not exist in the
V2-era model.
"""

from aireloom.models.data_source import DataSource

# Minimal V3-shaped payload derived from the live-verified sample in
# docs/v3-migration/04-data-sources.md (lines 175–211).
V3_DATASOURCE_DICT = {
    "id": "infrastruct_::f66f1bd369679b5b077dcdf006089556",
    "originalIds": ["infrastruct_::openaire"],
    "pids": None,
    "type": {"scheme": "scholarcomminfra", "value": "Scholarly Comm. Infrastructure"},
    "openaireCompatibility": "OpenAIRE 2.0 (EC funding)",
    "officialName": "OpenAIRE",
    "englishName": "OpenAIRE",
    "websiteUrl": "http://www.openaire.eu/",
    "logoUrl": "http://www.openaire.eu/images/openaire/logos/logo_openaire.png",
    "dateOfValidation": None,
    "description": None,
    "subjects": [],
    "languages": None,
    "contentTypes": None,
    "releaseStartDate": None,
    "releaseEndDate": None,
    "missionStatementUrl": None,
    "accessRights": None,
    "uploadRights": None,
    "databaseAccessRestriction": None,
    "dataUploadRestriction": None,
    "versioning": False,
    "citationGuidelineUrl": None,
    "pidSystems": None,
    "certificates": None,
    "policies": None,
    "journal": None,
    # --- V3 additive fields ---
    "collectedFrom": [{"key": "ds::123", "value": "Example Repository"}],
    "thematic": False,
    "eoscdatasourcetype": {"code": "Aggregator", "label": "Aggregator"},
    "jurisdiction": {"code": "Global", "label": "Global"},
    "odlanguages": ["en", "fr"],
    "openaireCompatibilityId": "openaire2.0",
    "links": [
        {
            "header": {"id": "result::abc", "type": "publication"},
            "title": "Related Paper",
        }
    ],
}


class TestDataSourceV3Fields:
    def test_model_validate_succeeds(self):
        ds = DataSource.model_validate(V3_DATASOURCE_DICT)
        assert ds.id == "infrastruct_::f66f1bd369679b5b077dcdf006089556"

    def test_collected_from(self):
        ds = DataSource.model_validate(V3_DATASOURCE_DICT)
        assert len(ds.collectedFrom) == 1
        assert ds.collectedFrom[0].key == "ds::123"
        assert ds.collectedFrom[0].value == "Example Repository"

    def test_thematic(self):
        ds = DataSource.model_validate(V3_DATASOURCE_DICT)
        assert ds.thematic is False

    def test_eoscdatasourcetype(self):
        ds = DataSource.model_validate(V3_DATASOURCE_DICT)
        assert ds.eoscdatasourcetype.code == "Aggregator"
        assert ds.eoscdatasourcetype.label == "Aggregator"

    def test_jurisdiction(self):
        ds = DataSource.model_validate(V3_DATASOURCE_DICT)
        assert ds.jurisdiction.code == "Global"
        assert ds.jurisdiction.label == "Global"

    def test_odlanguages(self):
        ds = DataSource.model_validate(V3_DATASOURCE_DICT)
        assert ds.odlanguages == ["en", "fr"]

    def test_openaire_compatibility_id(self):
        ds = DataSource.model_validate(V3_DATASOURCE_DICT)
        assert ds.openaireCompatibilityId == "openaire2.0"

    def test_links(self):
        ds = DataSource.model_validate(V3_DATASOURCE_DICT)
        assert ds.links is not None
        assert len(ds.links) == 1
        assert ds.links[0]["title"] == "Related Paper"

    def test_null_v3_fields_default_safely(self):
        """V3 fields that are null in the live response should produce safe defaults."""
        payload = dict(V3_DATASOURCE_DICT)
        payload["collectedFrom"] = None
        payload["thematic"] = None
        payload["eoscdatasourcetype"] = None
        payload["jurisdiction"] = None
        payload["odlanguages"] = None
        payload["openaireCompatibilityId"] = None
        payload["links"] = None
        ds = DataSource.model_validate(payload)
        # SafeCodeLabel defaults to empty CodeLabel (code="", label="")
        assert ds.eoscdatasourcetype.code == ""
        assert ds.jurisdiction.label == ""
        # Lists default to []
        assert ds.collectedFrom == []
        assert ds.odlanguages == []

    def test_relaxed_literal_fields_accept_any_string(self):
        """accessRights / uploadRights / databaseAccessRestriction now accept any string."""
        payload = dict(V3_DATASOURCE_DICT)
        payload["accessRights"] = "embargoed"
        payload["uploadRights"] = "creativeCommons"
        payload["databaseAccessRestriction"] = "loginRequired"
        ds = DataSource.model_validate(payload)
        assert ds.accessRights == "embargoed"
        assert ds.uploadRights == "creativeCommons"
        assert ds.databaseAccessRestriction == "loginRequired"
