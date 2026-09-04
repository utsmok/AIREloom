# Changelog

All notable changes to AIREloom are documented here. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/); versions follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.5.0] - 2026-09-04

Stable promotion of the v3 line: identical feature set and breaking changes as
0.5.0a1 (see [Migration to v3](migration-to-v3.md)), plus the additions below.

### Added

- `ProjectLinkPid` model for PID entries inside V3 `Project.links[]` items
  (`value`/`type`/`typeLabel`)
- `Organization.fundings[].jurisdiction` tolerates `null` payloads (coerced to
  an empty model instead of failing validation)
- Documented live quirks: research-products `pageSize > 100` returns HTTP 400
  in page and cursor modes; unsorted-page ordering/membership instability;
  Scholix requires bare pids

### Changed

- `projects_by_organization(search_on="name")` uses full-text `search` —
  organization names rarely appear in project text fields, so
  `search_on="openaire_id"` is recommended for identifier lookups

## [0.5.0a1] - 2026-07-21

AIREloom now targets the OpenAIRE Graph API **v3** (v1/v2 deprecated by OpenAIRE). This is a **breaking** release; see [Migration to v3](migration-to-v3.md).

### Added

- V3 Graph API support: single base URL `https://api.openaire.eu/graph/v3` for all entities (kebab-case paths)
- 41 new filter parameters across Research Products (+20), Projects (+13), Data Sources (+8)
- `logicalOperator` accepts `AND`/`OR`/`NOT` on all Graph filter models
- Typed response fields: `eoscIfGuidelines`, `publiclyFunded`, `isGreen`, `isInDiamondJournal`, `openAccessRoute`, `conferencePlace`/`conferenceDate`, organizational `fundings`/`collectedFrom`/`originalIds`, project `funding`/`links`, data source `eoscdatasourcetype`/`jurisdiction`/`odlanguages`/`links`, `Subject.provenance`
- Auto-quoting of filter values containing spaces/operators/parentheses (`GraphV3FilterSerializationMixin`)
- `popularity` sort field for Research Products
- Migration guide (`docs/migration-to-v3.md`)

### Changed

- **BREAKING:** filter renames — `authorOrcid`→`authorId`, `bestOpenAccessRightLabel`→`accessRightLabel`, `sdg`→`sdgLabel`
- **BREAKING:** `sdg: list[str]` → `sdgLabel: str` (use inline OR for multiple)
- **BREAKING:** Projects date filters (`fromStartDate`/`toStartDate`/`fromEndDate`/`toEndDate`) are now `str` (accept bare years like `"2022"`)
- **BREAKING:** Links endpoint is 0-indexed (first page `page=0`); page size silently capped at 99 by the server (library clamps + warns)
- Data source `accessRights`/`uploadRights`/`databaseAccessRestriction` relaxed from `Literal` to `str` per v3 spec

### Removed

- **BREAKING:** `grantID` filter (Projects) — dropped by v3
- Persons `startDate`/`endDate` sort fields — rejected by v3 validation
- Per-entity v1/v2 base URL routing (`_base_url_override` on Graph resource clients)

## [0.3.0] - 2025-06-04

### Added

- Ergonomics layer: `SafeList`/`SafeStr` types, computed properties on all models
- Convenience query functions (`search_by_doi`, `search_publications`, etc.)
- Iterator helpers: `collect()`, `count()`, `first()` on all resource clients
- Persons endpoint (OpenAIRE Graph API v1)
- Research Product Links and Relations Info endpoints
- Per-entity API version routing (researchProducts → v2, others → v1)
- Scholix v3 pagination fix
- Marimo notebook examples (dual-purpose scripts + interactive notebooks)

### Changed

- All routine operational logging downgraded from INFO to DEBUG
- CI ruff format check replaced with pre-commit hook
- Examples converted to marimo notebooks

## [0.2.0] - 2025-06-03

### Added

- Initial public release
- Async client for OpenAIRE Graph API and Scholexplorer API
- Support for NoAuth, Static Token, and OAuth2 Client Credentials
- Pydantic models for all response types
- Cursor-based and page-based pagination
- Configurable retry logic and rate limiting
- Optional client-side caching
- Request hook system
