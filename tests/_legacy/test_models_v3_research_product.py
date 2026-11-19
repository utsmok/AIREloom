"""Tests for V3 response-model fields on ResearchProduct entity models."""

from __future__ import annotations

from aireloom.models.research_product import (
    AccessRight,
    Author,
    Container,
    EoscIfGuideline,
    ResearchProduct,
    Subject,
)


class TestAuthorV3Id:
    """Author.id field (V3)."""

    def test_author_with_id(self) -> None:
        raw = {
            "id": "0000-0001-2345-6789",
            "fullName": "Jane Doe",
            "name": "Jane",
            "surname": "Doe",
            "rank": 1,
            "pid": None,
        }
        a = Author.model_validate(raw)
        assert a.id == "0000-0001-2345-6789"
        assert a.fullName == "Jane Doe"

    def test_author_without_id(self) -> None:
        raw = {"fullName": "John Smith", "pid": None}
        a = Author.model_validate(raw)
        assert a.id is None


class TestAccessRightOpenAccessRoute:
    """AccessRight.openAccessRoute already existed; confirm it still works."""

    def test_access_right_with_route(self) -> None:
        raw = {
            "code": "c_abf2",
            "label": "OPEN",
            "openAccessRoute": "gold",
            "scheme": "http://...",
        }
        ar = AccessRight.model_validate(raw)
        assert ar.openAccessRoute == "gold"

    def test_access_right_null_route(self) -> None:
        raw = {
            "code": "c_abf2",
            "label": "OPEN",
            "openAccessRoute": None,
            "scheme": "http://...",
        }
        ar = AccessRight.model_validate(raw)
        assert ar.openAccessRoute is None


class TestContainerConferenceFields:
    """Container.conferencePlace / conferenceDate (V3)."""

    def test_container_with_conference_fields(self) -> None:
        raw = {
            "name": "Test Conf Proc",
            "conferencePlace": "Vienna",
            "conferenceDate": "2024-06-15",
        }
        c = Container.model_validate(raw)
        assert c.conferencePlace == "Vienna"
        assert c.conferenceDate == "2024-06-15"

    def test_container_without_conference_fields(self) -> None:
        raw = {"name": "Journal of Tests"}
        c = Container.model_validate(raw)
        assert c.conferencePlace is None
        assert c.conferenceDate is None


class TestSubjectProvenance:
    """Subject.provenance field (V3 shape: {subject: {scheme,value}, provenance})."""

    def test_subject_v3_shape(self) -> None:
        raw = {
            "subject": {"scheme": "FOS", "value": "03 medical and health sciences"},
            "provenance": None,
        }
        s = Subject.model_validate(raw)
        assert s.subject == {"scheme": "FOS", "value": "03 medical and health sciences"}
        assert s.provenance is None

    def test_subject_v3_with_provenance(self) -> None:
        raw = {
            "subject": {"scheme": "ddc", "value": "610"},
            "provenance": {"harvested": True},
        }
        s = Subject.model_validate(raw)
        assert s.provenance == {"harvested": True}

    def test_subject_backward_compat(self) -> None:
        """Old V2 flat shape still works via extra='allow'."""
        raw = {"subject": {"fos": "Computer Science"}}
        s = Subject.model_validate(raw)
        assert s.provenance is None


class TestEoscIfGuideline:
    """EoscIfGuideline model (V3)."""

    def test_guideline(self) -> None:
        g = EoscIfGuideline.model_validate({"code": "eoscfu"})
        assert g.code == "eoscfu"

    def test_guideline_empty(self) -> None:
        g = EoscIfGuideline.model_validate({})
        assert g.code == ""


class TestResearchProductV3Fields:
    """Top-level ResearchProduct V3 fields."""

    @staticmethod
    def _minimal_v3_rp() -> dict:
        return {
            "id": "doi::10.1234/test.v3",
            "type": "publication",
            "mainTitle": "A V3 Test Paper",
            "authors": [
                {
                    "id": "0000-0001-9999-8888",
                    "fullName": "Alice V3",
                    "name": "Alice",
                    "surname": "V3",
                    "rank": 1,
                    "pid": None,
                }
            ],
            "subjects": [
                {
                    "subject": {
                        "scheme": "FOS",
                        "value": "03 medical and health sciences",
                    },
                    "provenance": None,
                }
            ],
            "container": {
                "name": "Journal of V3 Tests",
                "conferencePlace": "Berlin",
                "conferenceDate": "2024-09-01",
            },
            "bestAccessRight": {
                "code": "c_abf2",
                "label": "OPEN",
                "openAccessRoute": "gold",
                "scheme": "http://vocabularies.coar-repositories.org/documentation/access_rights/",
            },
            # New V3 boolean flags
            "isGreen": True,
            "isInDiamondJournal": False,
            "publiclyFunded": True,
            # New V3 eoscIfGuidelines
            "eoscIfGuidelines": [
                {"code": "eoscfu"},
                {"code": "osr"},
            ],
        }

    def test_model_validate_succeeds(self) -> None:
        rp = ResearchProduct.model_validate(self._minimal_v3_rp())
        assert rp.id == "doi::10.1234/test.v3"
        assert rp.mainTitle == "A V3 Test Paper"

    def test_is_green_flag(self) -> None:
        rp = ResearchProduct.model_validate(self._minimal_v3_rp())
        assert rp.isGreen is True

    def test_is_in_diamond_journal_flag(self) -> None:
        rp = ResearchProduct.model_validate(self._minimal_v3_rp())
        assert rp.isInDiamondJournal is False

    def test_publicly_funded_flag(self) -> None:
        rp = ResearchProduct.model_validate(self._minimal_v3_rp())
        assert rp.publiclyFunded is True

    def test_eosc_if_guidelines(self) -> None:
        rp = ResearchProduct.model_validate(self._minimal_v3_rp())
        assert len(rp.eoscIfGuidelines) == 2
        assert rp.eoscIfGuidelines[0].code == "eoscfu"
        assert rp.eoscIfGuidelines[1].code == "osr"

    def test_author_id_accessible(self) -> None:
        rp = ResearchProduct.model_validate(self._minimal_v3_rp())
        assert len(rp.authors) == 1
        assert rp.authors[0].id == "0000-0001-9999-8888"

    def test_subject_provenance_accessible(self) -> None:
        rp = ResearchProduct.model_validate(self._minimal_v3_rp())
        assert len(rp.subjects) == 1
        assert rp.subjects[0].provenance is None
        assert rp.subjects[0].subject == {
            "scheme": "FOS",
            "value": "03 medical and health sciences",
        }

    def test_container_conference_fields_accessible(self) -> None:
        rp = ResearchProduct.model_validate(self._minimal_v3_rp())
        assert rp.container.conferencePlace == "Berlin"
        assert rp.container.conferenceDate == "2024-09-01"

    def test_access_right_open_access_route(self) -> None:
        rp = ResearchProduct.model_validate(self._minimal_v3_rp())
        assert rp.bestAccessRight.openAccessRoute == "gold"

    def test_missing_new_fields_default_to_none(self) -> None:
        """Ensure backward compat when V3 fields are absent."""
        minimal = {
            "id": "doi::10.1234/old",
            "type": "publication",
            "mainTitle": "Old Record",
        }
        rp = ResearchProduct.model_validate(minimal)
        assert rp.eoscIfGuidelines == []
        assert rp.authors == []
        assert rp.subjects == []
