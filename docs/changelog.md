# Changelog

All notable changes to AIREloom are documented here. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/); versions follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
