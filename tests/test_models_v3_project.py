"""Tests for V3-added fields on the Project model: ``funding`` (hierarchical) and ``links``."""

from aireloom.models.project import (
    Project,
    ProjectFunding,
    ProjectLink,
)


def _v3_funding_dict() -> dict:
    """Return a minimal V3-shaped ``funding`` object matching doc-03 section 4.4."""
    return {
        "funder": {
            "id": "ec__________::EC",
            "shortname": "EC",
            "name": "European Commission",
            "jurisdiction": {"code": "EU", "label": "European Union"},
            "pid": None,
        },
        "level0": {
            "id": "ec__________::EC::FP7",
            "description": "SEVENTH FRAMEWORK PROGRAMME",
            "name": "FP7",
        },
        "level1": {
            "id": "ec__________::EC::FP7::SP2",
            "description": "SP2-Ideas",
            "name": "SP2",
        },
        "level2": {
            "id": "ec__________::EC::FP7::SP2::ERC",
            "description": "ERC",
            "name": "ERC",
        },
    }


def _v3_links_list() -> list[dict]:
    """Return a minimal V3-shaped ``links`` array matching doc-03 section 4.5."""
    return [
        {
            "header": {
                "relationType": "projectOrganization",
                "relationClass": "hasParticipant",
                "relatedIdentifier": "openorgs____::testorg",
                "relatedRecordType": "organization",
                "trust": "0.900",
            },
            "legalname": "UNIVERSITY OF STRATHCLYDE",
            "pid": ["doi123"],
            "country": {"code": "UNKNOWN", "label": "Unknown"},
        }
    ]


def _v3_project_dict(**overrides: object) -> dict:
    """Build a minimal V3 Project dict including both ``funding`` and ``fundings``."""
    base: dict = {
        "id": "openaire____::testproj",
        "code": "123456",
        "acronym": "TESTPROJ",
        "title": "Test Project for V3 Validation",
        "fundings": [
            {
                "fundingStream": {
                    "id": "FP7",
                    "description": "SEVENTH FRAMEWORK PROGRAMME",
                    "shortName": "FP7",
                },
                "fundingLevel_0": "EC",
                "fundingLevel_1": "SP2",
                "fundingLevel_2": "ERC",
                "jurisdiction": "EU",
                "name": "European Commission",
                "shortName": "EC",
            }
        ],
        "granted": {"currency": "EUR", "fundedAmount": 1500000, "totalAmount": 2000000},
        "funding": _v3_funding_dict(),
        "links": _v3_links_list(),
    }
    base.update(overrides)
    return base


class TestV3FundingField:
    """Tests for the hierarchical ``Project.funding`` field (doc-03 s4.4)."""

    def test_validate_succeeds(self) -> None:
        p = Project.model_validate(_v3_project_dict())
        assert isinstance(p.funding, ProjectFunding)

    def test_funder_accessible(self) -> None:
        p = Project.model_validate(_v3_project_dict())
        assert p.funding.funder.name == "European Commission"
        assert p.funding.funder.shortname == "EC"
        assert p.funding.funder.jurisdiction.code == "EU"

    def test_levels_accessible(self) -> None:
        p = Project.model_validate(_v3_project_dict())
        assert p.funding.level0.name == "FP7"
        assert p.funding.level1.name == "SP2"
        assert p.funding.level2.name == "ERC"

    def test_none_becomes_default_instance(self) -> None:
        d = _v3_project_dict()
        d["funding"] = None
        p = Project.model_validate(d)
        # Safe alias should produce an empty instance, not None
        assert p.funding is not None
        assert p.funding.funder.name == ""


class TestV3LinksField:
    """Tests for the ``Project.links`` field (doc-03 s4.5)."""

    def test_validate_succeeds(self) -> None:
        p = Project.model_validate(_v3_project_dict())
        assert isinstance(p.links, list)
        assert len(p.links) == 1
        assert isinstance(p.links[0], ProjectLink)

    def test_link_header_accessible(self) -> None:
        p = Project.model_validate(_v3_project_dict())
        link = p.links[0]
        assert link.header.relationType == "projectOrganization"
        assert link.header.relationClass == "hasParticipant"
        assert link.header.trust == "0.900"

    def test_link_entity_fields_accessible(self) -> None:
        p = Project.model_validate(_v3_project_dict())
        link = p.links[0]
        assert link.legalname == "UNIVERSITY OF STRATHCLYDE"
        assert link.country.code == "UNKNOWN"
        assert link.pid == ["doi123"]

    def test_empty_links_default(self) -> None:
        d = _v3_project_dict()
        del d["links"]
        p = Project.model_validate(d)
        assert p.links == []


class TestExistingFundingsUntouched:
    """Ensure the existing plural ``fundings`` field still works alongside new fields."""

    def test_both_present(self) -> None:
        p = Project.model_validate(_v3_project_dict())
        # Existing fundings should still be populated
        assert len(p.fundings) == 1
        assert p.fundings[0].shortName == "EC"

    def test_fundings_without_new_fields(self) -> None:
        d = _v3_project_dict()
        del d["funding"]
        del d["links"]
        p = Project.model_validate(d)
        assert len(p.fundings) == 1
        assert p.fundings[0].shortName == "EC"


class TestRoundTrip:
    """Model round-trip: validate → access → dump."""

    def test_full_dump_includes_new_fields(self) -> None:
        p = Project.model_validate(_v3_project_dict())
        data = p.model_dump()
        assert "funding" in data
        assert "links" in data
        assert "fundings" in data

    def test_funding_hierarchy_preserved(self) -> None:
        p = Project.model_validate(_v3_project_dict())
        fd = p.model_dump()["funding"]
        assert fd["funder"]["name"] == "European Commission"
        assert fd["level2"]["name"] == "ERC"
