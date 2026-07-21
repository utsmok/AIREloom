"""Tests for V3-added fields on the Organization model."""

from aireloom.models.organization import Organization


def test_v3_original_ids():
    """originalIds (list[str]) is accepted and accessible."""
    d = {
        "id": "org::__test__",
        "legalName": "Test Org",
        "originalIds": ["pending_org_::abc123"],
    }
    org = Organization.model_validate(d)
    assert org.originalIds == ["pending_org_::abc123"]


def test_v3_collected_from():
    """collectedFrom (list[CfHbKeyValue]) round-trips correctly."""
    d = {
        "id": "org::__test__",
        "legalName": "Test Org",
        "collectedFrom": [
            {
                "key": "openaire____::0362fcdb3076765d9c0041ad331553e8",
                "value": "OpenOrgs Database",
            }
        ],
    }
    org = Organization.model_validate(d)
    assert len(org.collectedFrom) == 1
    cf = org.collectedFrom[0]
    assert cf.key == "openaire____::0362fcdb3076765d9c0041ad331553e8"
    assert cf.value == "OpenOrgs Database"


def test_v3_fundings():
    """fundings uses the Organization-specific Funding shape (not project.Funding)."""
    d = {
        "id": "org::__test__",
        "legalName": "Test Org",
        "fundings": [
            {
                "funder": {
                    "id": "funder1",
                    "shortname": "EC",
                    "name": "European Commission",
                    "jurisdiction": {"code": "EU", "label": "European Union"},
                    "pid": [],
                },
                "level0": {
                    "id": "H2020",
                    "description": "Horizon 2020",
                    "name": "H2020",
                },
                "level1": {
                    "id": "ERC",
                    "description": "European Research Council",
                    "name": "ERC",
                },
                "level2": None,
            }
        ],
    }
    org = Organization.model_validate(d)
    assert len(org.fundings) == 1
    f = org.fundings[0]
    assert f.funder.name == "European Commission"
    assert f.funder.jurisdiction.code == "EU"
    assert f.level0.name == "H2020"
    assert f.level1.name == "ERC"
    assert f.level2 is None


def test_v3_all_fields_together():
    """A realistic V3-shaped Organization dict validates completely."""
    d = {
        "id": "openaire____::harvard",
        "legalShortName": "Harvard",
        "legalName": "Harvard University",
        "alternativeNames": ["Harvard College"],
        "websiteUrl": "https://www.harvard.edu",
        "country": {"code": "US", "label": "United States"},
        "pids": [{"scheme": "ROR", "value": "03ax2r23"}],
        "originalIds": ["pending_org_::abde8d72214cd15facc2fb7cab6e50b9"],
        "collectedFrom": [
            {
                "key": "openaire____::0362fcdb3076765d9c0041ad331553e8",
                "value": "OpenOrgs Database",
            }
        ],
        "fundings": [],
    }
    org = Organization.model_validate(d)
    assert org.legalName == "Harvard University"
    assert org.originalIds == ["pending_org_::abde8d72214cd15facc2fb7cab6e50b9"]
    assert len(org.collectedFrom) == 1
    assert org.fundings == []
    # Existing fields still work
    assert org.ror_id == "03ax2r23"
    assert org.country_code == "US"
