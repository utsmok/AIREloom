# tests/test_str_repr.py
from aireloom.models import (
    DataSource,
    Organization,
    Person,
    Project,
    ResearchProduct,
)


class TestResearchProductStr:
    def test_full_str(self):
        rp = ResearchProduct.model_validate({
            "id": "rp_test_1",
            "title": "A Very Long Paper Title About Something Important",
            "publicationDate": "2023-06-15",
            "pids": [{"scheme": "doi", "value": "10.1234/test"}],
            "instances": [],
        })
        s = str(rp)
        assert "A Very Long Paper Title About Something Important"[:80] in s
        assert "2023" in s
        assert "DOI:10.1234/test" in s

    def test_minimal_str(self):
        rp = ResearchProduct.model_validate({"id": "abc123"})
        s = str(rp)
        assert "ResearchProduct" in s
        assert "abc123" in s

    def test_repr(self):
        rp = ResearchProduct.model_validate({"id": "abc", "type": "publication"})
        r = repr(rp)
        assert "ResearchProduct" in r
        assert "abc" in r
        assert "publication" in r


class TestPersonStr:
    def test_full_name_with_orcid(self):
        p = Person.model_validate({
            "id": "person_orcid_1",
            "givenName": "John",
            "familyName": "Doe",
            "originalId": ["0000-0001-2345-6789"],
        })
        s = str(p)
        assert "John" in s
        assert "Doe" in s
        assert "ORCID" in s

    def test_name_only(self):
        p = Person.model_validate({"id": "person_name_1", "givenName": "Jane", "familyName": "Smith"})
        s = str(p)
        assert "Jane" in s
        assert "Smith" in s

    def test_fallback_to_id(self):
        p = Person.model_validate({"id": "person123"})
        s = str(p)
        assert "Person" in s
        assert "person123" in s


class TestOrganizationStr:
    def test_full_str(self):
        org = Organization.model_validate({
            "id": "org_test_1",
            "legalName": "MIT",
            "country": {"code": "US"},
            "pids": [{"scheme": "ror", "value": "042tb2j39"}],
        })
        s = str(org)
        assert "MIT" in s
        assert "US" in s
        assert "ror" in s.lower() or "ROR" in s

    def test_fallback(self):
        org = Organization.model_validate({"id": "org123"})
        s = str(org)
        assert "Organization" in s


class TestProjectStr:
    def test_full_str(self):
        proj = Project.model_validate({
            "id": "proj_test_1",
            "title": "Amazing Research Project",
            "code": "12345",
            "fundings": [{"shortName": "EC"}],
        })
        s = str(proj)
        assert "Amazing Research Project" in s
        assert "12345" in s
        assert "EC" in s

    def test_fallback(self):
        proj = Project.model_validate({"id": "proj123"})
        s = str(proj)
        assert "Project" in s


class TestDataSourceStr:
    def test_official_name(self):
        ds = DataSource.model_validate({"id": "ds_official_1", "officialName": "Zenodo"})
        assert "Zenodo" in str(ds)

    def test_english_name_fallback(self):
        ds = DataSource.model_validate({"id": "ds_english_1", "englishName": "DataRepo"})
        assert "DataRepo" in str(ds)

    def test_fallback(self):
        ds = DataSource.model_validate({"id": "ds123"})
        s = str(ds)
        assert "DataSource" in s
