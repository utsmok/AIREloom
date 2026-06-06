from unittest.mock import AsyncMock, MagicMock

import pytest

from aireloom.models import Organization, Person, Project, ResearchProduct
from aireloom.queries import (
    all_links,
    citing_works,
    count_publications,
    projects_by_organization,
    publications_by_author,
    publications_by_doi,
    publications_by_organization,
    publications_by_project,
    related_datasets,
)


@pytest.fixture
def session():
    sess = MagicMock()
    sess.research_products.collect = AsyncMock(return_value=[])
    sess.research_products.count = AsyncMock(return_value=0)
    sess.projects.collect = AsyncMock(return_value=[])
    sess.scholix.collect = AsyncMock(return_value=[])
    return sess


# ---------------------------------------------------------------------------
# publications_by_doi
# ---------------------------------------------------------------------------


class TestPublicationsByDoi:
    @pytest.mark.asyncio
    async def test_single_doi(self, session):
        session.research_products.collect.return_value = [
            ResearchProduct.model_validate({"id": "1", "title": "Paper"}),
        ]
        results = await publications_by_doi(session, "10.1234/test")
        assert len(results) == 1
        session.research_products.collect.assert_called_once()
        call_kwargs = session.research_products.collect.call_args[1]
        assert call_kwargs["filters"].pid == "10.1234/test"

    @pytest.mark.asyncio
    async def test_multiple_dois(self, session):
        await publications_by_doi(session, "10.1/a", "10.2/b")
        assert session.research_products.collect.call_count == 2

    @pytest.mark.asyncio
    async def test_aggregates_results(self, session):
        rp1 = ResearchProduct.model_validate({"id": "1", "title": "A"})
        rp2 = ResearchProduct.model_validate({"id": "2", "title": "B"})
        session.research_products.collect.side_effect = [[rp1], [rp2]]
        results = await publications_by_doi(session, "10.1/a", "10.2/b")
        assert results == [rp1, rp2]

    @pytest.mark.asyncio
    async def test_no_dois(self, session):
        results = await publications_by_doi(session)
        assert results == []
        session.research_products.collect.assert_not_called()


# ---------------------------------------------------------------------------
# publications_by_organization
# ---------------------------------------------------------------------------


class TestPublicationsByOrganization:
    @pytest.mark.asyncio
    async def test_by_name(self, session):
        await publications_by_organization(session, "MIT")
        call_kwargs = session.research_products.collect.call_args[1]
        assert call_kwargs["filters"].search == "MIT"

    @pytest.mark.asyncio
    async def test_by_openaire_id(self, session):
        await publications_by_organization(
            session, "openaire:123", search_on="openaire_id"
        )
        call_kwargs = session.research_products.collect.call_args[1]
        assert call_kwargs["filters"].relOrganizationId == "openaire:123"

    @pytest.mark.asyncio
    async def test_by_ror(self, session):
        await publications_by_organization(session, "042tb2j39", search_on="ror")
        call_kwargs = session.research_products.collect.call_args[1]
        assert call_kwargs["filters"].rorId == "042tb2j39"

    @pytest.mark.asyncio
    async def test_with_type_filter(self, session):
        await publications_by_organization(session, "MIT", type="dataset")
        call_kwargs = session.research_products.collect.call_args[1]
        assert call_kwargs["filters"].type == "dataset"

    @pytest.mark.asyncio
    async def test_with_open_access(self, session):
        await publications_by_organization(session, "MIT", open_access_only=True)
        call_kwargs = session.research_products.collect.call_args[1]
        assert call_kwargs["filters"].bestOpenAccessRightLabel == "OPEN"

    @pytest.mark.asyncio
    async def test_with_date_range(self, session):
        from datetime import date

        await publications_by_organization(
            session,
            "MIT",
            from_publication_date="2020-01-01",
            to_publication_date="2023-12-31",
        )
        call_kwargs = session.research_products.collect.call_args[1]
        assert call_kwargs["filters"].fromPublicationDate == date(2020, 1, 1)
        assert call_kwargs["filters"].toPublicationDate == date(2023, 12, 31)

    @pytest.mark.asyncio
    async def test_with_sort_and_limit(self, session):
        await publications_by_organization(
            session,
            "MIT",
            sort_by="publicationDate desc",
            limit=10,
        )
        call_kwargs = session.research_products.collect.call_args[1]
        assert call_kwargs["sort_by"] == "publicationDate desc"
        assert call_kwargs["limit"] == 10

    @pytest.mark.asyncio
    async def test_with_org_object_by_openaire_id(self, session):
        org = Organization.model_validate(
            {
                "id": "openaire:org1",
                "legalName": "MIT",
            }
        )
        await publications_by_organization(session, org, search_on="openaire_id")
        call_kwargs = session.research_products.collect.call_args[1]
        assert call_kwargs["filters"].relOrganizationId == "openaire:org1"

    @pytest.mark.asyncio
    async def test_with_org_object_by_name(self, session):
        org = Organization.model_validate(
            {
                "id": "org_no_id",
                "legalName": "MIT",
            }
        )
        await publications_by_organization(session, org, search_on="name")
        call_kwargs = session.research_products.collect.call_args[1]
        assert call_kwargs["filters"].search == "MIT"

    @pytest.mark.asyncio
    async def test_with_org_object_by_ror(self, session):
        org = Organization.model_validate(
            {
                "id": "org_ror",
                "legalName": "MIT",
                "pids": [{"scheme": "ROR", "value": "042tb2j39"}],
            }
        )
        await publications_by_organization(session, org, search_on="ror")
        call_kwargs = session.research_products.collect.call_args[1]
        assert call_kwargs["filters"].rorId == "042tb2j39"


# ---------------------------------------------------------------------------
# publications_by_author
# ---------------------------------------------------------------------------


class TestPublicationsByAuthor:
    @pytest.mark.asyncio
    async def test_by_name(self, session):
        await publications_by_author(session, "John Doe")
        call_kwargs = session.research_products.collect.call_args[1]
        assert call_kwargs["filters"].authorFullName == "John Doe"

    @pytest.mark.asyncio
    async def test_by_orcid(self, session):
        await publications_by_author(session, "0000-0001-2345-6789", search_on="orcid")
        call_kwargs = session.research_products.collect.call_args[1]
        assert call_kwargs["filters"].authorOrcid == "0000-0001-2345-6789"

    @pytest.mark.asyncio
    async def test_with_type_filter(self, session):
        await publications_by_author(session, "John Doe", type="publication")
        call_kwargs = session.research_products.collect.call_args[1]
        assert call_kwargs["filters"].type == "publication"

    @pytest.mark.asyncio
    async def test_with_sort_and_limit(self, session):
        await publications_by_author(session, "John Doe", sort_by="relevance", limit=5)
        call_kwargs = session.research_products.collect.call_args[1]
        assert call_kwargs["sort_by"] == "relevance"
        assert call_kwargs["limit"] == 5

    @pytest.mark.asyncio
    async def test_person_object_by_name(self, session):
        person = Person.model_validate(
            {
                "id": "person_name",
                "givenName": "Jane",
                "familyName": "Smith",
            }
        )
        await publications_by_author(session, person)
        call_kwargs = session.research_products.collect.call_args[1]
        assert call_kwargs["filters"].authorFullName == "Jane Smith"

    @pytest.mark.asyncio
    async def test_person_object_by_orcid(self, session):
        person = Person.model_validate(
            {
                "id": "person_orcid",
                "givenName": "Jane",
                "familyName": "Smith",
                "originalId": ["0000-0001-2345-6789"],
            }
        )
        await publications_by_author(session, person, search_on="orcid")
        call_kwargs = session.research_products.collect.call_args[1]
        assert call_kwargs["filters"].authorOrcid == "0000-0001-2345-6789"

    @pytest.mark.asyncio
    async def test_person_object_by_orcid_falls_back_to_name(self, session):
        """When Person has no orcid but search_on='orcid', fall back to full_name."""
        person = Person.model_validate(
            {
                "id": "person_no_orcid",
                "givenName": "Jane",
                "familyName": "Smith",
            }
        )
        await publications_by_author(session, person, search_on="orcid")
        call_kwargs = session.research_products.collect.call_args[1]
        assert call_kwargs["filters"].authorFullName == "Jane Smith"


# ---------------------------------------------------------------------------
# publications_by_project
# ---------------------------------------------------------------------------


class TestPublicationsByProject:
    @pytest.mark.asyncio
    async def test_by_name(self, session):
        await publications_by_project(session, "Graph Project")
        call_kwargs = session.research_products.collect.call_args[1]
        assert call_kwargs["filters"].search == "Graph Project"
        assert call_kwargs["filters"].hasProjectRel is True

    @pytest.mark.asyncio
    async def test_by_openaire_id(self, session):
        await publications_by_project(
            session, "openaire:proj1", search_on="openaire_id"
        )
        call_kwargs = session.research_products.collect.call_args[1]
        assert call_kwargs["filters"].relProjectId == "openaire:proj1"

    @pytest.mark.asyncio
    async def test_by_code(self, session):
        await publications_by_project(session, "H2020-1234", search_on="code")
        call_kwargs = session.research_products.collect.call_args[1]
        assert call_kwargs["filters"].relProjectCode == "H2020-1234"

    @pytest.mark.asyncio
    async def test_with_type_filter(self, session):
        await publications_by_project(session, "Graph Project", type="publication")
        call_kwargs = session.research_products.collect.call_args[1]
        assert call_kwargs["filters"].type == "publication"

    @pytest.mark.asyncio
    async def test_project_object_with_id(self, session):
        proj = Project.model_validate({"id": "openaire:proj1", "title": "Test"})
        await publications_by_project(session, proj)
        call_kwargs = session.research_products.collect.call_args[1]
        assert call_kwargs["filters"].relProjectId == "openaire:proj1"

    @pytest.mark.asyncio
    async def test_project_object_with_code_no_id(self, session):
        proj = Project.model_validate({"id": "", "code": "H2020-1234", "title": "Test"})
        await publications_by_project(session, proj)
        call_kwargs = session.research_products.collect.call_args[1]
        assert call_kwargs["filters"].relProjectCode == "H2020-1234"

    @pytest.mark.asyncio
    async def test_project_object_with_title_only(self, session):
        proj = Project.model_validate({"id": "", "title": "Graph Project"})
        await publications_by_project(session, proj)
        call_kwargs = session.research_products.collect.call_args[1]
        assert call_kwargs["filters"].search == "Graph Project"
        assert call_kwargs["filters"].hasProjectRel is True


# ---------------------------------------------------------------------------
# count_publications
# ---------------------------------------------------------------------------


class TestCountPublications:
    @pytest.mark.asyncio
    async def test_basic_count(self, session):
        session.research_products.count.return_value = 42
        result = await count_publications(session)
        assert result == 42

    @pytest.mark.asyncio
    async def test_count_with_type(self, session):
        await count_publications(session, type="publication")
        call_kwargs = session.research_products.count.call_args[1]
        assert call_kwargs["filters"].type == "publication"

    @pytest.mark.asyncio
    async def test_count_open_access(self, session):
        await count_publications(session, open_access_only=True)
        call_kwargs = session.research_products.count.call_args[1]
        assert call_kwargs["filters"].bestOpenAccessRightLabel == "OPEN"

    @pytest.mark.asyncio
    async def test_count_no_open_access_by_default(self, session):
        await count_publications(session)
        call_kwargs = session.research_products.count.call_args[1]
        assert call_kwargs["filters"].bestOpenAccessRightLabel is None

    @pytest.mark.asyncio
    async def test_count_with_search(self, session):
        await count_publications(session, search="machine learning")
        call_kwargs = session.research_products.count.call_args[1]
        assert call_kwargs["filters"].search == "machine learning"

    @pytest.mark.asyncio
    async def test_count_with_pid(self, session):
        await count_publications(session, pid="10.1234/test")
        call_kwargs = session.research_products.count.call_args[1]
        assert call_kwargs["filters"].pid == "10.1234/test"

    @pytest.mark.asyncio
    async def test_count_with_author_orcid(self, session):
        await count_publications(session, author_orcid="0000-0001-2345-6789")
        call_kwargs = session.research_products.count.call_args[1]
        assert call_kwargs["filters"].authorOrcid == "0000-0001-2345-6789"

    @pytest.mark.asyncio
    async def test_count_with_org_id(self, session):
        await count_publications(session, rel_organization_id="openaire:org1")
        call_kwargs = session.research_products.count.call_args[1]
        assert call_kwargs["filters"].relOrganizationId == "openaire:org1"

    @pytest.mark.asyncio
    async def test_count_with_project_id(self, session):
        await count_publications(session, rel_project_id="openaire:proj1")
        call_kwargs = session.research_products.count.call_args[1]
        assert call_kwargs["filters"].relProjectId == "openaire:proj1"


# ---------------------------------------------------------------------------
# projects_by_organization
# ---------------------------------------------------------------------------


class TestProjectsByOrganization:
    @pytest.mark.asyncio
    async def test_by_name(self, session):
        await projects_by_organization(session, "MIT")
        call_kwargs = session.projects.collect.call_args[1]
        assert call_kwargs["filters"].search == "MIT"

    @pytest.mark.asyncio
    async def test_by_openaire_id(self, session):
        await projects_by_organization(session, "openaire:123", search_on="openaire_id")
        call_kwargs = session.projects.collect.call_args[1]
        assert call_kwargs["filters"].relOrganizationId == "openaire:123"

    @pytest.mark.asyncio
    async def test_with_sort_and_limit(self, session):
        await projects_by_organization(
            session, "MIT", sort_by="startDate desc", limit=5
        )
        call_kwargs = session.projects.collect.call_args[1]
        assert call_kwargs["sort_by"] == "startDate desc"
        assert call_kwargs["limit"] == 5

    @pytest.mark.asyncio
    async def test_with_org_object(self, session):
        org = Organization.model_validate(
            {
                "id": "openaire:org1",
                "legalName": "MIT",
            }
        )
        await projects_by_organization(session, org, search_on="openaire_id")
        call_kwargs = session.projects.collect.call_args[1]
        assert call_kwargs["filters"].relOrganizationId == "openaire:org1"


# ---------------------------------------------------------------------------
# citing_works
# ---------------------------------------------------------------------------


class TestCitingWorks:
    @pytest.mark.asyncio
    async def test_citing(self, session):
        await citing_works(session, "10.1234/test")
        call_kwargs = session.scholix.collect.call_args[1]
        assert call_kwargs["filters"].targetPid == "10.1234/test"
        assert (
            call_kwargs["filters"].relation is None
        )  # No relation filter — Scholix uses IsRelatedTo

    @pytest.mark.asyncio
    async def test_with_source_type(self, session):
        await citing_works(session, "10.1234/test", source_type="Publication")
        call_kwargs = session.scholix.collect.call_args[1]
        assert call_kwargs["filters"].sourceType == "Publication"

    @pytest.mark.asyncio
    async def test_with_sort_and_limit(self, session):
        await citing_works(session, "10.1234/test", sort_by="date", limit=10)
        call_kwargs = session.scholix.collect.call_args[1]
        assert call_kwargs["sort_by"] == "date"
        assert call_kwargs["limit"] == 10


# ---------------------------------------------------------------------------
# related_datasets
# ---------------------------------------------------------------------------


class TestRelatedDatasets:
    @pytest.mark.asyncio
    async def test_related(self, session):
        await related_datasets(session, "10.1234/test")
        call_kwargs = session.scholix.collect.call_args[1]
        assert call_kwargs["filters"].sourcePid == "10.1234/test"
        assert call_kwargs["filters"].targetType == "Dataset"

    @pytest.mark.asyncio
    async def test_with_sort_and_limit(self, session):
        await related_datasets(session, "10.1234/test", sort_by="date", limit=5)
        call_kwargs = session.scholix.collect.call_args[1]
        assert call_kwargs["sort_by"] == "date"
        assert call_kwargs["limit"] == 5


# ---------------------------------------------------------------------------
# all_links
# ---------------------------------------------------------------------------


class TestAllLinks:
    @pytest.mark.asyncio
    async def test_both_directions(self, session):
        session.scholix.collect.return_value = []
        await all_links(session, "10.1234/test")
        assert session.scholix.collect.call_count == 2

    @pytest.mark.asyncio
    async def test_source_only(self, session):
        await all_links(session, "10.1234/test", direction="source")
        assert session.scholix.collect.call_count == 1
        call_kwargs = session.scholix.collect.call_args[1]
        assert call_kwargs["filters"].sourcePid == "10.1234/test"

    @pytest.mark.asyncio
    async def test_target_only(self, session):
        await all_links(session, "10.1234/test", direction="target")
        assert session.scholix.collect.call_count == 1
        call_kwargs = session.scholix.collect.call_args[1]
        assert call_kwargs["filters"].targetPid == "10.1234/test"

    @pytest.mark.asyncio
    async def test_both_merges_results(self, session):
        link1 = MagicMock(name="link1")
        link2 = MagicMock(name="link2")
        session.scholix.collect.side_effect = [[link1], [link2]]
        results = await all_links(session, "10.1234/test", direction="both")
        assert results == [link1, link2]

    @pytest.mark.asyncio
    async def test_both_with_limit(self, session):
        """When direction='both' and limit is set, second call respects remaining limit."""
        link1 = MagicMock(name="link1")
        link2 = MagicMock(name="link2")
        session.scholix.collect.side_effect = [[link1], [link2]]
        await all_links(session, "10.1234/test", direction="both", limit=10)
        # First call gets limit=10, second call gets limit=9 (10 - 1 result)
        calls = session.scholix.collect.call_args_list
        assert calls[0][1]["limit"] == 10
        assert calls[1][1]["limit"] == 9

    @pytest.mark.asyncio
    async def test_source_with_limit(self, session):
        await all_links(session, "10.1234/test", direction="source", limit=5)
        call_kwargs = session.scholix.collect.call_args[1]
        assert call_kwargs["limit"] == 5
