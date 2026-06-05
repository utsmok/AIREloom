"""Convenience query functions for common AIREloom workflows.

These functions provide high-level, ergonomic access to common queries
against the OpenAIRE Graph API. Each function wraps the underlying filter
and iteration mechanics into a single call with sensible defaults.

Usage::

    from aireloom import AireloomSession
    from aireloom.queries import publications_by_doi

    async with AireloomSession() as session:
        papers = await publications_by_doi(session, "10.1234/example")
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from .endpoints import (
    ProjectsFilters,
    ResearchProductsFilters,
    ScholixFilters,
)

if TYPE_CHECKING:
    from .models import (
        Organization,
        Person,
        Project,
        ResearchProduct,
        ScholixRelationship,
    )
    from .session import AireloomSession


# ---------------------------------------------------------------------------
# Research product queries
# ---------------------------------------------------------------------------


async def publications_by_doi(
    session: AireloomSession,
    *dois: str,
) -> list[ResearchProduct]:
    """Fetch research products by DOI(s).

    Args:
        session: Active AireloomSession.
        *dois: One or more DOI strings.

    Returns:
        List of matching ResearchProduct instances.
    """
    results: list[ResearchProduct] = []
    for doi in dois:
        filters = ResearchProductsFilters(pid=doi)
        items = await session.research_products.collect(filters=filters)
        results.extend(items)
    return results


async def publications_by_organization(
    session: AireloomSession,
    identifier: str | Organization,
    *,
    search_on: Literal["name", "openaire_id", "ror"] = "name",
    type: Literal["publication", "dataset", "software", "other"] | None = None,
    from_publication_date: str | None = None,
    to_publication_date: str | None = None,
    open_access_only: bool = False,
    sort_by: str | None = None,
    limit: int | None = None,
) -> list[ResearchProduct]:
    """Fetch research products associated with an organization.

    Args:
        session: Active AireloomSession.
        identifier: Organization name, OpenAIRE ID, ROR ID, or Organization object.
        search_on: How to interpret *identifier* — ``"name"`` uses ``search``,
            ``"openaire_id"`` uses ``relOrganizationId``, ``"ror"`` uses ``rorId``.
        type: Restrict to a specific product type.
        from_publication_date: Start date filter (inclusive).
        to_publication_date: End date filter (inclusive).
        open_access_only: Only return open access products.
        sort_by: Sort expression (e.g. ``"publicationDate desc"``).
        limit: Maximum results to return.

    Returns:
        List of matching ResearchProduct instances.
    """
    filter_kwargs: dict = {}
    _resolve_org_filter(identifier, search_on, filter_kwargs)

    if type is not None:
        filter_kwargs["type"] = type
    if from_publication_date is not None:
        filter_kwargs["fromPublicationDate"] = from_publication_date
    if to_publication_date is not None:
        filter_kwargs["toPublicationDate"] = to_publication_date
    if open_access_only:
        filter_kwargs["bestOpenAccessRightLabel"] = "OPEN"

    filters = ResearchProductsFilters(**filter_kwargs)
    return await session.research_products.collect(
        filters=filters, sort_by=sort_by, limit=limit,
    )


async def publications_by_author(
    session: AireloomSession,
    identifier: str | Person,
    *,
    search_on: Literal["name", "orcid"] = "name",
    type: Literal["publication", "dataset", "software", "other"] | None = None,
    sort_by: str | None = None,
    limit: int | None = None,
) -> list[ResearchProduct]:
    """Fetch research products by an author.

    Args:
        session: Active AireloomSession.
        identifier: Author name or ORCID, or a Person object.
        search_on: ``"name"`` searches by ``authorFullName``,
            ``"orcid"`` searches by ``authorOrcid``.
        type: Restrict to a specific product type.
        sort_by: Sort expression.
        limit: Maximum results.

    Returns:
        List of matching ResearchProduct instances.
    """
    filter_kwargs: dict = {}

    if isinstance(identifier, str):
        if search_on == "orcid":
            filter_kwargs["authorOrcid"] = identifier
        else:
            filter_kwargs["authorFullName"] = identifier
    # Person object
    elif search_on == "orcid":
        orcid = identifier.orcid
        if orcid:
            filter_kwargs["authorOrcid"] = orcid
        else:
            filter_kwargs["authorFullName"] = identifier.full_name
    else:
        filter_kwargs["authorFullName"] = identifier.full_name

    if type is not None:
        filter_kwargs["type"] = type

    filters = ResearchProductsFilters(**filter_kwargs)
    return await session.research_products.collect(
        filters=filters, sort_by=sort_by, limit=limit,
    )


async def publications_by_project(
    session: AireloomSession,
    identifier: str | Project,
    *,
    search_on: Literal["name", "openaire_id", "code"] = "name",
    type: Literal["publication", "dataset", "software", "other"] | None = None,
    sort_by: str | None = None,
    limit: int | None = None,
) -> list[ResearchProduct]:
    """Fetch research products associated with a project.

    Args:
        session: Active AireloomSession.
        identifier: Project name, OpenAIRE ID, or code, or a Project object.
        search_on: How to interpret *identifier* — ``"name"`` uses ``search``,
            ``"openaire_id"`` uses ``relProjectId``, ``"code"`` uses ``relProjectCode``.
        type: Restrict to a specific product type.
        sort_by: Sort expression.
        limit: Maximum results.

    Returns:
        List of matching ResearchProduct instances.
    """
    filter_kwargs: dict = {}

    if isinstance(identifier, str):
        if search_on == "openaire_id":
            filter_kwargs["relProjectId"] = identifier
        elif search_on == "code":
            filter_kwargs["relProjectCode"] = identifier
        else:
            # Use search for name-based lookup
            filter_kwargs["search"] = identifier
            filter_kwargs["hasProjectRel"] = True
    # Project object — use its ID
    elif identifier.id:
        filter_kwargs["relProjectId"] = identifier.id
    elif identifier.code:
        filter_kwargs["relProjectCode"] = identifier.code
    else:
        filter_kwargs["search"] = identifier.title
        filter_kwargs["hasProjectRel"] = True

    if type is not None:
        filter_kwargs["type"] = type

    filters = ResearchProductsFilters(**filter_kwargs)
    return await session.research_products.collect(
        filters=filters, sort_by=sort_by, limit=limit,
    )


async def count_publications(
    session: AireloomSession,
    *,
    type: Literal["publication", "dataset", "software", "other"] | None = None,
    open_access_only: bool = False,
    search: str | None = None,
    pid: str | None = None,
    author_orcid: str | None = None,
    rel_organization_id: str | None = None,
    rel_project_id: str | None = None,
) -> int:
    """Count research products matching criteria.

    Args:
        session: Active AireloomSession.
        type: Restrict to a specific product type.
        open_access_only: Only count open access products.
        search: Free-text search.
        pid: Persistent identifier.
        author_orcid: Author ORCID.
        rel_organization_id: Related organization OpenAIRE ID.
        rel_project_id: Related project OpenAIRE ID.

    Returns:
        Total count of matching products.
    """
    filters = ResearchProductsFilters(
        type=type,
        search=search,
        pid=pid,
        authorOrcid=author_orcid,
        relOrganizationId=rel_organization_id,
        relProjectId=rel_project_id,
        bestOpenAccessRightLabel="OPEN" if open_access_only else None,
    )
    return await session.research_products.count(filters=filters)


# ---------------------------------------------------------------------------
# Organization / Project queries
# ---------------------------------------------------------------------------


async def projects_by_organization(
    session: AireloomSession,
    identifier: str | Organization,
    *,
    search_on: Literal["name", "openaire_id"] = "name",
    sort_by: str | None = None,
    limit: int | None = None,
) -> list[Project]:
    """Fetch projects associated with an organization.

    Args:
        session: Active AireloomSession.
        identifier: Organization name, OpenAIRE ID, or Organization object.
        search_on: ``"name"`` uses ``relOrganizationName``,
            ``"openaire_id"`` uses ``relOrganizationId``.
        sort_by: Sort expression.
        limit: Maximum results.

    Returns:
        List of matching Project instances.
    """
    filter_kwargs: dict = {}
    _resolve_org_filter(identifier, search_on, filter_kwargs)

    filters = ProjectsFilters(**filter_kwargs)
    return await session.projects.collect(
        filters=filters, sort_by=sort_by, limit=limit,
    )


# ---------------------------------------------------------------------------
# Scholix link queries
# ---------------------------------------------------------------------------


async def citing_works(
    session: AireloomSession,
    doi: str,
    *,
    source_type: Literal["Publication", "Dataset", "Software", "Other"] | None = None,
    sort_by: str | None = None,
    limit: int | None = None,
) -> list[ScholixRelationship]:
    """Fetch works that cite the given DOI (via Scholix).

    Args:
        session: Active AireloomSession.
        doi: DOI of the cited work.
        source_type: Filter citing work type.
        sort_by: Sort expression.
        limit: Maximum results.

    Returns:
        List of ScholixRelationship instances.
    """
    filter_kwargs: dict = {"targetPid": doi, "relation": "References"}
    if source_type:
        filter_kwargs["sourceType"] = source_type

    filters = ScholixFilters(**filter_kwargs)
    return await session.scholix.collect(
        filters=filters, sort_by=sort_by, limit=limit,
    )


async def related_datasets(
    session: AireloomSession,
    doi: str,
    *,
    sort_by: str | None = None,
    limit: int | None = None,
) -> list[ScholixRelationship]:
    """Fetch datasets related to the given publication DOI (via Scholix).

    Args:
        session: Active AireloomSession.
        doi: DOI of the publication.
        sort_by: Sort expression.
        limit: Maximum results.

    Returns:
        List of ScholixRelationship instances.
    """
    filters = ScholixFilters(sourcePid=doi, targetType="Dataset")
    return await session.scholix.collect(
        filters=filters, sort_by=sort_by, limit=limit,
    )


async def all_links(
    session: AireloomSession,
    doi: str,
    *,
    direction: Literal["source", "target", "both"] = "both",
    sort_by: str | None = None,
    limit: int | None = None,
) -> list[ScholixRelationship]:
    """Fetch all Scholix links involving a DOI.

    Args:
        session: Active AireloomSession.
        doi: DOI to search for.
        direction: Search as ``"source"``, ``"target"``, or ``"both"``.
        sort_by: Sort expression.
        limit: Maximum results.

    Returns:
        List of ScholixRelationship instances.
    """
    results: list[ScholixRelationship] = []

    if direction in ("source", "both"):
        filters = ScholixFilters(sourcePid=doi)
        items = await session.scholix.collect(
            filters=filters, sort_by=sort_by, limit=limit,
        )
        results.extend(items)

    if direction in ("target", "both"):
        filters = ScholixFilters(targetPid=doi)
        remaining = (limit - len(results)) if limit else None
        if remaining is None or remaining > 0:
            items = await session.scholix.collect(
                filters=filters, sort_by=sort_by, limit=remaining,
            )
            results.extend(items)

    return results


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _resolve_org_filter(
    identifier: str | Organization,
    search_on: str,
    filter_kwargs: dict,
) -> None:
    """Resolve an organization identifier into the appropriate filter field.

    Mutates *filter_kwargs* in place.
    """

    if isinstance(identifier, str):
        if search_on == "openaire_id":
            filter_kwargs["relOrganizationId"] = identifier
        elif search_on == "ror":
            filter_kwargs["rorId"] = identifier
        else:
            filter_kwargs["search"] = identifier
    # Organization object
    elif search_on == "openaire_id":
        if identifier.id:
            filter_kwargs["relOrganizationId"] = identifier.id
        else:
            filter_kwargs["search"] = identifier.legalName
    elif search_on == "ror":
        ror = identifier.ror_id
        if ror:
            filter_kwargs["rorId"] = ror
        else:
            filter_kwargs["search"] = identifier.legalName
    else:
        filter_kwargs["search"] = identifier.legalName
