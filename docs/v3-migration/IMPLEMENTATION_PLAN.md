# AIREloom V3 Migration — Consolidated Implementation Plan

**Date:** 2026-07-21 (rev 1.1 — incorporates independent review `PLAN_REVIEW.md`, verdict *SOUND WITH REVISIONS*)
**Status:** Ready for execution
**Scope:** Migrate AIREloom from the deprecated OpenAIRE Graph API V1/V2 to the unified V3 (`https://api.openaire.eu/graph/v3`), and align all models, filters, and clients with the live V3 API.
**Evidence base:** Consolidates 8 per-endpoint/facet research reports (`docs/v3-migration/01–08-*.md`). Every behavioral claim was verified against the **live V3 API** (`reference/v3-investigation/v3_live.py`), the V3 OpenAPI spec, and the docs site, then independently re-verified by the plan reviewer (13/13 spot-checks passed). Supersedes the earlier `V3_MIGRATION_PLAN.md` at repo root.

> **Revision log (1.0 → 1.1):** added explicit sort-dict actions to Phase 2 (C1); made the `Subject` model change concrete instead of "investigate" (C2); removed the stale "add py.typed" instruction — file already exists (I1); specified list-typed + logical-operator handling in the quoting helper (I2, I3); expanded the list→string serialization note to cover `keywords`/`fos` (I4); added a V1/V2-sunset contingency (I5); moved the low-priority unwrapper fallback out of Phase 1 (I6); added an explicit breaking-changes list for the migration guide (I7); fixed the new-filter count to a single definition (M1); distinguished the urgency of the two page-size clamps (M2); added notes on `funder` docstring (M4), re-verifying the batch comma-OR syntax (M5), and the Scholix `sort_by` no-op (M6); committed on the deprecation-shim question (M7).

> **Headline:** OpenAIRE V3 serves all entities from one base URL with kebab-case paths, adds 41 new filter parameters, renames 3, removes `grantID`, and fixes the persons 500s. AIREloom's response models need only additive field changes. The single most important fix is a **latent off-by-one bug in the links iteration** (currently skips the first page → data loss). The migration is a clean cutover, released as a phased pre-release.

---

## 1. Release & Versioning Strategy

This is a breaking change (renamed filters, removed `grantID`, new base URL, kebab-case paths, type changes). The library is currently **`0.4.0`, Development Status `3 - Alpha`** (`pyproject.toml`). The strategy below is the recommendation; alternatives and their rejection rationale follow.

### 1.1 Recommendation: phased clean cutover, no dual support

| Decision | Choice |
|---|---|
| Dual support via runtime toggle (env param)? | **No** — rejected (§1.2) |
| Separate repo branch + separate PyPI package? | **No** — rejected (§1.2) |
| Phased cutover, deprecating the V1/V2 surface? | **Yes** — adopted |
| Versioning | `0.5.0a1` → `0.5.0b1` → `0.5.0` (stable) |
| Where the work happens | A long-lived `v3` branch, merged to `main` at stable |
| Fate of 0.4.0 (V1/V2) | Remains on PyPI untouched; no backports. Dies naturally when OpenAIRE removes V1/V2 (~6 months). |
| Deprecation shim for old filter names? | **No.** Rely on `extra="forbid"` validation errors + a clear migration guide. Good docs beat a shim for an alpha lib (see M7 resolution). |

**Why a clean cutover (no V1/V2 retention):** V1/V2 are deprecated and will be removed in ~6 months. The filter models are *incompatible* (3 renames, `grantID` removed, type changes, `extra="forbid"`), so retaining V1/V2 would mean maintaining two parallel, divergent filter-model sets — unjustifiable complexity for an alpha library with a small user base.

**On the error UX (M7):** with `extra="forbid"`, an old field name (e.g. `authorOrcid`) raises a Pydantic `ValidationError` listing all valid fields. That is workable, not elegant. Rather than build a deprecation shim, we ship a thorough `docs/migration-to-v3.md` (Phase 8) that enumerates every breaking change. This is the right trade-off for an alpha library.

**Why pre-releases:** PEP 440 pre-release versions (`0.5.0a1`, `0.5.0b1`) are **not** installed by default — `pip install aireloom` continues to resolve to `0.4.0` until `0.5.0` (stable) ships. This gives early adopters an opt-in runway (`pip install "aireloom>=0.5.0a1"`) without surprising existing users.

### 1.2 Rejected alternatives

- **Runtime toggle (env var to switch v2↔v3):** the two APIs differ in base URL, path casing, pagination indexing, and filter names. A toggle would require runtime branching in serialization, two filter-model families, and dual test fixtures — essentially two libraries fused. Toggles are for *feature flags*, not *whole-API generations*.
- **Separate package / permanent branch with its own PyPI release:** fragments the user base, doubles maintenance, confuses discovery. Only warranted when a large installed base cannot migrate — not the case at `0.4.0` alpha.

### 1.3 Version numbering rationale

- **Stay on `0.x`** (do not jump to `1.0.0`). The library is not yet at the feature-complete, API-stable milestone `1.0.0` signals. `0.5.0` marks the V3 cutover as a significant-but-expected (for 0.x) breaking change.
- **Reserve `1.0.0`** for after the surface stabilizes — plausibly once OpenAIRE's V4 "unified filters" leaves BETA and AIREloom adopts it.
- **Use PEP 440 pre-release suffixes** (`a1`, `b1`, optional `rc1`). Recognized by pip/uv; excluded from default resolution.
- **Development Status classifier:** bump `3 - Alpha` → `4 - Beta` at the `0.5.0b1` tag; hold through `0.5.0`; promote to `5 - Production/Stable` only at a future `1.0.0`.

### 1.4 Branch, milestone & contingency plan

1. Cut branch `v3` from `main`.
2. Implement phases 0–9 (§3) on `v3`. (Phase 5 is additive and may run in parallel with 2–4.)
3. Tag `0.5.0a1` from `v3`; publish to TestPyPI first, then PyPI. Announce for early testing.
4. Incorporate feedback; tag `0.5.0b1` (raise classifier to Beta).
5. Tag `0.5.0` (stable); merge `v3` → `main`.
6. Legacy: `0.4.0` remains the last V1/V2 release; documented to stop working when OpenAIRE removes V1/V2.

**Contingency (I5) — V1/V2 sunset before 0.5.0 stable:** "Time-box the migration" is not a fallback. If OpenAIRE announces a firm V1/V2 sunset date before `0.5.0b1` tags, cut an **accelerated `0.5.0`** from whatever is complete at that moment — minimum viable = **Phase 1 (core infra) + Phase 4 §1 (links off-by-one fix)** — and ship without the additive model/filter work, which can follow in `0.5.1`. This guarantees users always have a working client against a live OpenAIRE.

---

## 2. Scope Summary (from the 8 research reports)

| Area | Headline | Source |
|---|---|---|
| Base URL | One V3 base serves all entities; remove the v1/v2 split + RP `_base_url_override` | `07` |
| Paths | **Kebab-case is a hard requirement** — V3 returns **405** for camelCase. `researchProducts`→`research-products`, `dataSources`→`datasources`; `projects`/`persons`/`organizations` unchanged | `07` |
| Filters | 3 RP renames; **41 new filter params** (RP 20, Projects 13, DS 8 — *excluding* meta-params `page`/`pageSize`/`cursor`/`sortBy`/`logicalOperator`/`includeStats`); `grantID` removed; `logicalOperator` gains `NOT`; Projects date filters → `str` | `01`,`03`,`04`,`08` |
| Sort | RP: re-add `popularity` (it works); Persons: relevance-only (drop `startDate`/`endDate`) | `01`,`05` |
| Models | Additive only (V3 uses same camelCase field names): RP (+`eoscIfGuidelines`, `green`, etc.), Org (+`fundings`,`originalIds`,`collectedFrom`), DS (+5–7 fields), Project (+`funding`,`links` nested) | `01`,`08`,`02`,`04`,`03` |
| Critical bug | **Links iteration off-by-one**: `search_links`/`iterate_links` start at `page=1` on a 0-indexed endpoint → silently skips the first page (data loss) | `06`,`07` |
| Behavior to keep | Links & Scholix: 0-indexed, silent `pageSize`/`size=100`→10 cap (clamp to 99), divergent envelope, no cursor | `06`,`07` |
| Filter serialization | NEW: V3 requires double-quoting filter values with spaces/parens/operators; inline OR/AND/NOT supported | `01`,`08` |
| Persons | `givenName`/`lastName` 500s are **fixed**; remove CAUTION docstrings | `05` |
| Scholix | Already correct (0-indexed, proper envelope); no code changes | `06` |

> **Line-number caveat (M3):** all `file:line` references are approximate (±3 lines, verified at planning time). The executor should grep for the named symbol, not trust the number verbatim.

---

## 3. Phased Implementation

### Phase 0 — Branch & version setup
- Cut `v3` branch. Bump `pyproject.toml` `version` → `"0.5.0a1.dev0"` (tag `0.5.0a1` at first release).
- **`src/aireloom/py.typed` already exists** (PEP 561 compliant) — no action. Just verify it ships in the wheel (`[tool.hatch.build.targets.wheel] packages = ["src/aireloom"]` already includes it). *(I1 — removed the stale "add py.typed" instruction.)*

### Phase 1 — Core infrastructure (foundation; everything depends on this)
Implement first, alone. **Phase 1 contains ONLY blocking work**; non-blocking items are moved to later phases (I6).

1. **`src/aireloom/constants.py`** — replace the two Graph base-URL constants with one:
   ```python
   OPENAIRE_GRAPH_API_BASE_URL = "https://api.openaire.eu/graph/v3"
   ```
   Delete `OPENAIRE_GRAPH_API_V2_BASE_URL`. Keep `OPENAIRE_SCHOLIX_API_BASE_URL` unchanged. (`07`-R1)
2. **`src/aireloom/endpoints.py`** — kebab-case path constants (HARD requirement; V3 returns 405 for camelCase):
   - `RESEARCH_PRODUCTS = "research-products"`
   - `DATA_SOURCES = "datasources"`
   - `LINKS = "research-products/links"`
   - (`projects`, `persons`, `organizations`, `SCHOLIX` unchanged) (`07`-R5)
3. **`src/aireloom/resources/research_products_client.py`** — **remove** `_base_url_override = OPENAIRE_GRAPH_API_V2_BASE_URL` (around line 47–50). With one V3 base, RP inherits the default like every other entity. Drop the now-unused import. (`07`-R2, `01`-§6)
   - **Reconciliation (decided):** the Projects research report (`03`-R7) suggested *adding* a `_base_url_override` to `ProjectsClient`. **Wrong for V3** — no client overrides; the single default base is V3 and `ProjectsClient`/`OrganizationsClient`/etc. inherit it automatically. Verified by `07` and reviewer.
4. **`src/aireloom/resources/research_products_client.py`** — the links methods pass `base_url_override=OPENAIRE_GRAPH_API_BASE_URL` (around lines 104, 162). After §1 this resolves to V3; **remove the explicit override** since the inherited base is already V3. (`07`-R4)
5. **`src/aireloom/models/base.py` Header model** — no structural change; all-optional + `extra="allow"` already tolerates the three envelope shapes. (`07`-R7)

**Acceptance:** `async with AireloomSession() as s: await s.research_products.search(...)` and each other entity hits `/graph/v3/<kebab-path>` and returns 200.

### Phase 2 — Filter models & sort dicts (`endpoints.py`)
1. **Research Products renames** (`01`-§1, `08`-R4): `authorOrcid`→`authorId`, `bestOpenAccessRightLabel`→`accessRightLabel`, `sdg`→`sdgLabel`. Note: `sdg` was `list[str]`; `sdgLabel` is a single `str` (V3 supports inline OR within the value) — **a cardinality break to document** (see Phase 8).
2. **Research Products new params** (`01`-§2c, `08`-R7): add the 20 new V3 filter fields (`accessRightLabel`, `authorId`, `sdgLabel`, `eoscIfGuidelines`, `excludePubDateRange: bool`, `fromPublicationYear: int`, `toPublicationYear: int`, `publicationYear: str`, `hasLicense: bool`, `language`, `relCommunityName`, `relFunder`, `relFundingLevel0Id/1Id/2Id`, `relHostingDataSource`, `relOrganization`, `relProject`, `source`, `subCommunity`, `toPublicationYear`).
3. **Projects** (`03`-R1,R2,R3): add 13 new fields (`activeYear`, `startYear`, `endYear`, `fromStartYear`, `toStartYear`, `fromEndYear`, `toEndYear`, `country`, `funder`, `fundinglevel0Id`, `fundinglevel1Id`, `fundinglevel2Id`, `projectOAMandatePublications`); **remove `grantID`**; change `fromStartDate`/`toStartDate`/`fromEndDate`/`toEndDate` from `date | None` → `str | None` (V3 accepts bare years — **a type break to document**, see Phase 8).
   - **`funder` caveat (M4):** returns 0 results for all tested values as of 2026-07; `fundingShortName` works. Add a docstring note: *"returns 0 results for all known values as of 2026-07; prefer `fundingShortName`. Kept for forward-compat."* Do not block the migration on it.
4. **Data Sources** (`04`-R2): add 8 new fields (`collectedFromName`, `compatibilityId`, `compatibilityName`, `country`, `eoscdatasourcetype`, `jurisdiction`, `odLanguages`, `thematic: bool`).
5. **All entities** (`02`,`05`,`08`): widen `logicalOperator` to `Literal["AND", "OR", "NOT"]`. Document that `NOT` is primarily an inline operator within filter values (top-level `NOT` is accepted but near-no-op).
6. **Persons** (`05`-R1): remove the CAUTION docstrings on `givenName`/`lastName` — both now return 200.
7. **Sort dicts (C1 — previously missing action):**
   - `ENDPOINT_DEFINITIONS[RESEARCH_PRODUCTS]["sort"]`: **add `"popularity": {}`** (live-verified working on V3).
   - `ENDPOINT_DEFINITIONS[PERSONS]["sort"]`: **remove `"startDate": {}` and `"endDate": {}`** (both return 400 on V3; relevance-only).

**Acceptance:** `ResearchProductsFilters(authorId=..., accessRightLabel=..., sdgLabel=...)` validates; old names raise a validation error (`extra="forbid"`); `popularity` is a declared RP sort; persons sort is relevance-only.

### Phase 3 — Filter-value serialization (quoting) [NEW V3 behavior]
V3 requires filter values containing spaces/parens/**logical operators** to be **double-quoted**, and supports inline `OR/AND/NOT`. Currently `model_dump(exclude_none=True)` sends raw values → 400 for multi-word values (`08`-§4, `01`-§1).

1. Add a serialization helper that quotes a value **iff** it matches the server's own trigger rule. Trigger = contains whitespace, a parenthesis, **or a bare logical-operator token** (regex `\b(OR|AND|NOT)\b|[\s()]`), and the value does **not** already start with `"` or `(` (so power-user expressions like `("US" OR "GB") AND NOT "DE"` pass through untouched). *(I3 — trigger now matches the V3 error message exactly.)*
2. **List-typed fields (I2):** apply the quoting rule **element-wise** to each string item of list-valued filters (`subjects`, `contentTypes`, `keywords`, `fos`); leave non-string items (bool, int) untouched.
3. **List→string serialization (I4):** V3 specs `subjects`/`contentTypes` (ResearchProducts) and `keywords` (Projects) and `fos` (ResearchProducts) as comma-separated strings while the models use `list[str]`. **Verify** how `bibliofabric` serializes list fields (repeated key `subjects=a&subjects=b` vs `subjects=a,b`). If repeated-key, either switch those fields to `str | None` or add a join serializer. All four affected fields are in scope.
4. Apply the quoting at the filter→query-param boundary. AIREloom's standard clients serialize via `bibliofabric.BaseResourceClient`; the links path dumps filters directly (`research_products_client.py:98`). Implement as a thin AIREloom-side override of param-building **or** a `field_serializer` on the filter base model.
5. Affects **Graph V3 filters only** — Scholix/links filters do not use this syntax.

**Acceptance:** `ResearchProductsFilters(accessRightLabel="Open Access")` serializes to `accessRightLabel="Open Access"` and returns 200; `subjects=["Open Access Research"]` round-trips correctly.

### Phase 4 — Resource clients & pagination fixes
1. **CRITICAL — links off-by-one fix** (`06`-§2, `07`-R3): `research_products_client.py` — change `search_links` default `page: int = 1` → `0`; change `iterate_links` `current_page = 1` → `0`; fix docstrings to "0-indexed". This is a **data-loss bug** (currently skips the first page).
2. **Clamp page size (M2 — differentiated urgency):**
   - **Graph links (urgent):** default `page_size` `100` → `99`; add a clamp so values >99 become 99. The default of 100 is silently truncated to 10 today.
   - **Scholix (defensive only):** clamp `size` to 99. Scholix's default is `DEFAULT_PAGE_SIZE = 20` (`constants.py:14`), so users only hit the cap if they explicitly pass ≥100. Clamp protects against silent truncation regardless.
3. **Scholix client** — **no changes** (already 0-indexed, correct envelope). (`06`-§6)
4. **`_batch.py`** — `page=1` is **correct** for regular 1-indexed endpoints; leave as-is. **(M5) Re-verify** during Phase 9 that V3 still honors the `pid=a,b,c` comma-separated OR syntax the docstring claims.
5. **(M6, future cleanup — not blocking):** `queries.py` `citing_works`/`related_datasets`/`all_links` forward a `sort_by` to `session.scholix.collect()`, but Scholix has no sort support (`06`-§6.4). File a follow-up; do not block the migration.

**Acceptance:** `iterate_links(sourcePid=...)` yields relations starting from the first page; page=0 and page=1 return different (correct, ordered) records; no path silently returns 10 results when 99 were requested.

### Phase 5 — Response models (additive) + unwrapper hardening
V3 uses the same camelCase field names as V2; `extra="allow"` already absorbs new fields without data loss. Declare useful new fields explicitly for type access (`01`-§5, `08`-R1/R2/R3, `02`, `04`):

- **`models/research_product.py`** (`ResearchProduct`): add `eoscIfGuidelines`, `green`, `inDiamondJournal`, `isGreen`, `isInDiamondJournal`, `publiclyFunded`. Nested: add `id` to `Author`; add `openAccessRoute` to `Instance.accessRight`; add `conferencePlace`/`conferenceDate` to `Container`.
- **`Subject` model (C2 — concrete decision, no longer "investigate"):** V3 returns `{"subject": {"scheme": "FOS", "value": "..."}, "provenance": null}` (verified live), which is incompatible with the current `Subject.subject: dict[str,str] | None`. Reshape `Subject` to typed fields:
  ```python
  class SubjectV3(BaseModel):
      subject: dict[str, str] | None = None   # {scheme, value}
      provenance: dict | None = None
      model_config = ConfigDict(extra="allow")
  ```
  (or equivalent). The current model degrades gracefully today (no data loss), so this is not a runtime break — but ship a typed model so users get `.subject["scheme"]` access safely.
- **`models/organization.py`**: add `originalIds: list[str]`, `fundings: list[Funding]`, `collectedFrom: list[CfHbKeyValue]`.
- **`models/data_source.py`**: add `collectedFrom`, `thematic`, `eoscdatasourcetype` (CodeLabel), `jurisdiction` (CodeLabel), `odlanguages`, `openaireCompatibilityId`, `links`. Consider `CodeLabel`/`CfHbKeyValue` helper models. Optionally relax 3 overly-restrictive `Literal` types to `str | None` per V3 spec.
- **`models/project.py`**: add `funding` (hierarchical ProjectFunding) and `links` (inline related entities). Model `links` as raw `list | None` initially (dedicated relation endpoints exist).
- **`models/person.py`** — no structural change; update the module docstring's v1 reference. (`05`-R4)
- **`unwrapper.py` (moved here from Phase 1 — I6):** low-priority, add a `result` fallback in `unwrap_results()` for future-proofing (Scholix currently bypasses the unwrapper). Not blocking.

**Acceptance:** `model_validate(<live v3 response>)` succeeds for every entity; new fields (incl. the reshaped `Subject`) are typed.

### Phase 6 — Ergonomics layer (`queries.py`)
Rename filter references (4 lines, `08`-§3, R5, `01`-§7): `authorOrcid`→`authorId`; `bestOpenAccessRightLabel`→`accessRightLabel`; value `"OPEN"`→`"Open Access"` (V3 enum); `sdg`→`sdgLabel`.

**Acceptance:** `publications_by_author(..., search_on="orcid", ...)` works against V3.

### Phase 7 — Tests (7 files)
Update v1/v2 URL constants and camelCase path assertions (per `07`):
- `tests/test_config.py`, `tests/test_session.py`, `tests/test_actual_data.py` (v2 URLs → v3, camelCase → kebab-case paths), `tests/resources/test_research_products_client.py` (remove v2 override assertions), `tests/resources/test_links.py` (0-indexed expectations, path), `tests/resources/test_persons_client.py` (rename v1 test, assert V3 default).
- Add tests for: renamed filters, `popularity` sort, persons `givenName`/`lastName` 200, filter-value auto-quoting (incl. list-typed), `iterate_links` starting at page 0, the reshaped `Subject`, new DS/Org/Project fields.
- Keep the `live_api` marker pattern; add live smoke tests (skipped in CI) exercising V3 endpoints.

**Acceptance:** `uv run pytest tests/` green; `--cov=aireloom` ≥ 95%.

### Phase 8 — Docs, changelog, packaging, migration guide
- **New `docs/migration-to-v3.md` (I7) — explicit breaking-changes list** for 0.4.0→0.5.0 users:
  - Filter renames: `authorOrcid`→`authorId`, `bestOpenAccessRightLabel`→`accessRightLabel`, `sdg`→`sdgLabel`.
  - **Cardinality change:** `sdg: list[str]` → `sdgLabel: str` (use inline OR for multiple).
  - **Type change:** Projects `fromStartDate`/`toStartDate`/`fromEndDate`/`toEndDate` now `str` (accepts bare years like `"2022"`); passing `date(...)` objects no longer works.
  - Removed: `grantID` (Projects); `startDate`/`endDate` persons sorts.
  - Base URL/path change; default `popularity` sort now declared.
- `AGENTS.md`: rewrite API Version Routing for V3; remove "Graph API v3: Not yet supported"; update Known Issues (drop fixed items; document retained server bugs: links/Scholix page-size cap, 0-indexed links, envelope divergence).
- `docs/advanced/configuration.md` (base URL), `docs/usage/links.md` & `persons.md` (remove "v1-only" admonitions), `docs/endpoints/links.md` (path), `docs/changelog.md` (V3 entry).
- `pyproject.toml`: bump version per §1.4; bump classifier to `4 - Beta` at the `b1` tag; confirm `py.typed` ships in the wheel.

### Phase 9 — Verification
1. `uv run ruff check src/ && uv run ruff format src/ && uvx ty check src/`.
2. `uv run pytest tests/` green, coverage ≥ 95%.
3. Live smoke test against `/graph/v3`: every entity search; renamed filters + quoting; `popularity` sort; persons `givenName`; `iterate_links` yields from page 0; `_batch_get` correctness; **re-verify the `pid=a,b,c` comma-OR syntax** (M5).
4. Confirm the tagged pre-release resolves correctly (excluded from default until stable).

---

## 4. Reconciliation Notes

- **Per-client `_base_url_override` (decided):** `03`-R7 (add override to ProjectsClient) vs `07`-R2 (remove RP override). **`07` is correct** — V3 is one base; no client overrides. Phase 1 §3.
- **List-vs-string filter serialization (expanded, I4):** V3 specs `subjects`, `contentTypes`, `keywords`, `fos` as comma-separated `string`; current code uses `list[str]`. **Must verify** how `bibliofabric` serializes list fields (repeated key vs comma-join) — Phase 3 §3 covers all four.
- **`Subject` model shape (decided, C2):** V3 returns `{subject:{scheme,value}, provenance}` — reshape the model in Phase 5; not a runtime break today.
- **`funder` filter returns 0 results:** documented but non-functional; `fundingShortName` works. Document preference; do not block (Phase 2 §3, M4).

## 5. Risk Register

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Links/Scholix silent page-size cap changes upstream | Med | Low (clamp isolates us) | Clamp to 99 (Phase 4) |
| Filter quoting breaks power-user expressions | Low | Med | Pass through values already starting with `"`/`(`; trigger matches server rule (Phase 3) |
| List-filter serialization mismatch with V3 | Med | Med | Verify in Phase 3 §3; add join serializer if needed |
| `Subject`/nested model shape drift | Med | Low | `extra="allow"` prevents data loss; typed fixes in Phase 5 |
| **OpenAIRE removes V1/V2 before 0.5.0 stable** | Low | Med | **Accelerated 0.5.0 from Phase 1 + Phase 4 §1 (§1.4 contingency)** |

## 6. Open Questions (resolved where noted)
1. Versioning: `0.5.0a1/b1/0.5.0` cadence adopted (§1.3). *(Could go straight to `0.5.0` given alpha maturity — but pre-releases give a safer opt-in runway; recommend keeping them.)*
2. `links`/`projects.links` nested structures: model `links` as `list | None` for 0.5.0 (dedicated relation endpoints exist); promote to full models on demand.
3. Branch: `v3` branch preferred over direct-to-`main` for a clean reviewable diff; merged at stable.
4. Deprecation shim: **no** (M7) — rely on `extra="forbid"` errors + the migration guide.
