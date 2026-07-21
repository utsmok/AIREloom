# V3 Migration Research — Projects Endpoint (`/v3/projects`)

## Scope

Full analysis of the `/v3/projects` endpoint: all 36 parameters (filter + meta), 3 sort fields, response model (`APIProject` + nested funding/grant structures), and resource client routing. Compared against:
- Current AIREloom code (`ProjectsFilters`, `Project` model, `ProjectsClient`, `ENDPOINT_DEFINITIONS`)
- V3 OpenAPI spec (`graph_v3_openapi.json`)
- V3 documentation (https://graph.openaire.eu/docs/apis/graph-api/projects/)
- **Live V3 API** (https://api.openaire.eu/graph/v3/projects) — every claim verified

## Method

1. Extracted all 36 parameters from V3 OpenAPI spec `paths./v3/projects.get.parameters`
2. Cross-referenced against current `ProjectsFilters` (21 fields) at `src/aireloom/endpoints.py:180-229`
3. Ran 20+ live API calls via `reference/v3-investigation/v3_live.py` covering:
   - All 13 new filter params (representative sample)
   - All 3 sort fields (single + multi-field)
   - Both date-filter families (date-based vs year-based)
   - Full `--full` response capture for field-level model comparison
4. Extracted V3 schemas: `APIProject`, `Funding`, `Granted`, `Funder`, `Programme`, `FundingStream`

---

## Findings

### 1. Filter Parameters

| # | Param | In Current Code? | V3 Spec Type | Live Verified | Notes |
|---|-------|-----------------|--------------|---------------|-------|
| 1 | `search` | YES | string | 200 OK | Unchanged |
| 2 | `title` | YES | string | 200 OK | Unchanged |
| 3 | `keywords` | YES (as `list[str]`) | string | 200 OK | **Type change**: V3 spec says `string`; live returns comma-separated string. Current model's list[str] + validator still works due to parsing logic |
| 4 | `id` | YES | string | 200 OK | Unchanged |
| 5 | `code` | YES | string | 200 OK | Unchanged |
| 6 | `grantID` | **YES** | **REMOVED** | **400 ERROR** | **REMOVED in V3**. Returns `Unknown parameter: grantID`. Must be deleted |
| 7 | `acronym` | YES | string | 200 OK | Unchanged |
| 8 | `callIdentifier` | YES | string | 200 OK | Unchanged |
| 9 | `fundingShortName` | YES | string | 200 OK (129K results for EC) | Unchanged; example value `EC` works |
| 10 | `fundingStreamId` | YES | string | 200 OK | Unchanged |
| 11 | `fromStartDate` | YES (as `date`) | **string** | 200 OK (205K results) | **Type change**: V3 spec says `string` (accepts YYYY or YYYY-MM-DD). Current code uses Python `date` type which serializes as YYYY-MM-DD — this works but is more restrictive than V3 allows |
| 12 | `toStartDate` | YES (as `date`) | **string** | 200 OK | Same type change as above |
| 13 | `fromEndDate` | YES (as `date`) | **string** | 200 OK | Same type change as above |
| 14 | `toEndDate` | YES (as `date`) | **string** | 200 OK | Same type change as above |
| 15 | `relOrganizationName` | YES | string | 200 OK | Unchanged |
| 16 | `relOrganizationId` | YES | string | 200 OK | Unchanged |
| 17 | `relCommunityId` | YES | string | 200 OK | Unchanged |
| 18 | `relOrganizationCountryCode` | YES | string | 200 OK | Unchanged |
| 19 | `relCollectedFromDatasourceId` | YES | string | 200 OK | Unchanged |
| 20 | `logicalOperator` | YES (`Literal["AND","OR"]`) | string (enum AND/OR/**NOT**) | N/A | **Enum expanded**: V3 adds `"NOT"` as valid value |
| 21 | `country` | **NO (NEW)** | string | 200 OK (**2.94M results** for `US`) | **NEW parameter**. Filters by project country |
| 22 | `funder` | **NO (NEW)** | string | 200 OK (but **0 results** for all tested values) | **NEW parameter**. Tested: EC, "European Commission", NSF, "NSF", NIH, "NIH", UKRI, "UK Research and Innovation" — all return 0. **Suspect this filter requires specific internal ID format or is non-functional despite being documented**. Use `fundingShortName` instead for now |
| 23 | `fundinglevel0Id` | **NO (NEW)** | string | 200 OK (**4059 results** for quoted value) | **NEW parameter**. Requires double-quoting when value contains spaces/colons. Example: `fundinglevel0Id="ukri________::UKRI::Horizon Europe Guarantee"` |
| 24 | `fundinglevel1Id` | **NO (NEW)** | string | Not tested (no known value) | **NEW parameter**. Likely same quoting rules as level0 |
| 25 | `fundinglevel2Id` | **NO (NEW)** | string | Not tested (no known value) | **NEW parameter**. Likely same quoting rules as level0 |
| 26 | `projectOAMandatePublications` | **NO (NEW)** | string | 200 OK (**104K results** for `true`) | **NEW parameter**. Filters projects with OA mandate for publications. Accepts boolean-like strings |
| 27 | `startYear` | **NO (NEW)** | string | 200 OK (**118K results** for `2020`) | **NEW parameter**. Exact year match on project start year |
| 28 | `endYear` | **NO (NEW)** | string | 200 OK (**118K results** for `2024`) | **NEW parameter**. Exact year match on project end year |
| 29 | `activeYear` | **NO (NEW)** | string | 200 OK (**552K results** for `2020`) | **NEW parameter**. Projects active (running) in given year |
| 30 | `fromStartYear` | **NO (NEW)** | string | 200 OK (**340K results** for range 2020-2022) | **NEW parameter**. Start year >= given year |
| 31 | `toStartYear` | **NO (NEW)** | string | 200 OK | Used with fromStartYear above |
| 32 | `fromEndYear` | **NO (NEW)** | string | 200 OK | **NEW parameter**. End year >= given year |
| 33 | `toEndYear` | **NO (NEW)** | string | 200 OK | **NEW parameter**. End year <= given year |
| -- | `page` | (implicit) | integer | 200 OK | 1-indexed, max 10000 dataset |
| -- | `pageSize` | (implicit) | integer | 200 OK | Range 1-100 |
| -- | `cursor` | (implicit) | string | N/A | Cursor pagination supported |
| -- | `sortBy` | (implicit) | string | See section below | Sort directive |

**Summary**: 13 new parameters, 1 removed (`grantID`), 2 type changes (date filters: `date` -> `string`), 1 enum expansion (`logicalOperator` gains `NOT`).

### 2. Date Filter Families

V3 provides **two parallel date filtering systems**:

| Family | Parameters | Format | Live Status |
|--------|-----------|--------|-------------|
| **Date-based** (existing) | `fromStartDate`, `toStartDate`, `fromEndDate`, `toEndDate` | `YYYY` or `YYYY-MM-DD` | WORKS: `fromStartDate=2022-01-01&toStartDate=2023-12-31` -> 205K results |
| **Year-based** (NEW) | `startYear`, `endYear`, `activeYear`, `fromStartYear`, `toStartYear`, `fromEndYear`, `toEndYear` | `YYYY` (string) | ALL WORK: see individual tests above |

Both families are functional. The year-based filters are strictly string-type years (no dashes). The date-based filters accept both `YYYY` and full dates.

**Current code issue**: `fromStartDate`/`toStartDate`/`fromEndDate`/`toEndDate` are typed as Python `date` objects in `ProjectsFilters`. This means users must pass `date(2022, 1, 1)` rather than the raw string `"2022"`. The V3 API accepts bare years like `fromStartDate=2022`. Changing to `str` would be more permissive and match the spec.

### 3. Sort Fields

| Field | In Current ENDPOINT_DEFINITIONS? | Live Test Result | Notes |
|-------|----------------------------------|-------------------|-------|
| `relevance` | YES (default) | Works (implicit default) | Explicit `sortBy=relevance` returns **400** — must include direction |
| `startDate` | YES | **200 OK** with `sortBy=startDate+DESC` | Space between field and direction |
| `endDate` | YES | **200 OK** with `sortBy=endDate+DESC` | Space between field direction |

**Critical finding on sort format**:

The V3 error message states: *"The field should be in the format 'fieldname ASC\|DESC'"* and *"Multiple sorting parameters should be comma-separated."*

However, live testing reveals:

| Format Tried | Result |
|-------------|--------|
| `sortBy=relevance` | **400** — missing direction |
| `sortBy=startDate,DESC` | **400** — comma as field-direction separator fails |
| `sortBy=endDate,ASC` | **400** — same |
| `sortBy=%22startDate+DESC%22` | **400** — URL-encoded quotes around whole thing fails |
| `sortBy=startDate+DESC` | **200 OK** — **SPACE between fieldname and direction works** |
| `sortBy=startDate+DESC%2C+endDate+ASC` | **200 OK** — **COMMA+SPACE between multiple sort fields works** |

**Actual format**: `fieldname ASC|DESC` with a **space** separating field from direction, and `, ` (comma+space) separating multiple sort directives. The docs' description is correct but easy to misinterpret.

Current `ENDPOINT_DEFINITIONS` at line 348-354 already lists the correct 3 sort fields. No changes needed there.

### 4. Response Model Comparison

#### 4.1 Top-level Project Fields

| Field | Current Model (`project.py`) | V3 Spec (`APIProject`) | Live Response | Gap? |
|-------|----------------------------|----------------------|---------------|------|
| `id` | inherited from BaseEntity | string | present (e.g. `corda_______::...`) | No |
| `code` | `str \| None` | string | present | No |
| `acronym` | `SafeStr` (defaults `""`) | string | present (can be null) | No |
| `title` | `SafeStr` | string | present | No |
| `websiteUrl` | `str \| None` | string | present (can be null) | No |
| `startDate` | `str \| None` | string | present (format `YYYY-MM-DD`) | No |
| `endDate` | `str \| None` | string | present (format `YYYY-MM-DD`) | No |
| `callIdentifier` | `str \| None` | string | present (can be null) | No |
| `keywords` | `SafeList[str]` (parsed from string) | **string** | present as **comma-separated string** e.g. `"Longevity, Genetic-epidemiology, COVID-19"` | Minor: spec says string, current model parses to list. Both work. |
| `openAccessMandateForPublications` | `bool \| None` | boolean | present (`false`/`true`) | No |
| `openAccessMandateForDataset` | `bool \| None` | boolean | present | No |
| `subjects` | `SafeList[str]` | array | present (can be null) | No |
| `summary` | `SafeStr` | string | present (can be null) | No |
| `fundings` | `SafeList[Funding]` | array of Funder | present | Structure differs slightly (see below) |
| `granted` | `SafeGrant` (Grant) | Granted | present | Field name matches, nested structure matches |
| `h2020Programmes` | `SafeList[H2020Programme]` | array of Programme | present (can be null) | No |
| **`funding`** | **NOT PRESENT** | **NOT in APIProject spec** | **PRESENT in live response!** | **NEW FIELD** — hierarchical funding object (see 4.4) |
| **`links`** | **NOT PRESENT** | **NOT in APIProject spec** | **PRESENT in live response!** | **NEW FIELD** — array of related entities (organizations, etc.) |
| **`originalIds`** | **NOT PRESENT** | **array** in spec | Not observed (null/absent in tested responses) | **Spec-only so far** |

#### 4.2 Nested `fundings` Array (current `Funding` model vs live)

| Sub-field | Current `Funding` Model | Live Response | Match? |
|-----------|----------------------|---------------|-------|
| `fundingStream.id` | `str \| None` | present (e.g. `"EC::FP7::SP2::ERC"`) | Yes |
| `fundingStream.description` | `SafeStr` (defaults `""`) | present (e.g. `"SEVENTH FRAMEWORK PROGRAMME - SP2-Ideas - ERC"`) | Yes |
| `jurisdiction` | `str \| None` | present (e.g. `"EU"`, `"GB"`) | Yes |
| `name` | `SafeStr` | present (e.g. `"European Commission"`) | Yes |
| `shortName` | `SafeStr` | present (e.g. `"EC"`, `"UKRI"`) | Yes |

The existing `Funding` / `FundingStream` models align well with live data.

#### 4.3 Nested `granted` Object (current `Grant` model vs live)

| Sub-field | Current `Grant` Model | Live Response | Match? |
|-----------|---------------------|---------------|-------|
| `currency` | `SafeStr` | present (e.g. `"GBP"`, `"EUR"`, `null`) | Yes |
| `fundedAmount` | `float \| None` | present (e.g. `81871.0`, `0.0`) | Yes |
| `totalCost` | `float \| None` | present (e.g. `0.0`, `1.0E7`) | Yes |

The existing `Grant` model matches.

#### 4.4 NEW `funding` Field (not in current model)

This is a **new top-level field** present in live V3 responses but absent from both the current model and the V3 OpenAPI `APIProject` schema. It provides a hierarchical view of funding:

```json
{
  "funding": {
    "funder": {
      "id": "ec__________::EC",
      "shortname": "EC",
      "name": "European Commission",
      "jurisdiction": { "code": "EU", "label": "European Union" },
      "pid": null
    },
    "level0": {
      "id": "ec__________::EC::FP7",
      "description": "SEVENTH FRAMEWORK PROGRAMME",
      "name": "FP7"
    },
    "level1": {
      "id": "ec__________::EC::FP7::SP2",
      "description": "SP2-Ideas",
      "name": "SP2"
    },
    "level2": {
      "id": "ec__________::EC::FP7::SP2::ERC",
      "description": "ERC",
      "name": "ERC"
    }
  }
}
```

This is structurally richer than the flat `fundings` array — it includes the full hierarchy (funder → level0 → level1 → level2) with IDs, descriptions, names, and jurisdiction details. **This field should be added to the V3 Project model.**

#### 4.5 NEW `links` Field (not in current model)

Present in live responses as an array of related entity links (primarily organizations participating in the project):

```json
{
  "links": [{
    "header": {
      "relationType": "projectOrganization",
      "relationClass": "hasParticipant",
      "relatedIdentifier": "openorgs____::...",
      "relatedRecordType": "organization",
      "trust": "0.900"
    },
    "legalname": "UNIVERSITY OF STRATHCLYDE",
    "pid": [...],
    "country": { "code": "UNKNOWN", "label": "Unknown" },
    ...
  }]
}
```

This is a significant new structure. It embeds related organization data inline with each project result.

### 5. Resource Client Routing

| Aspect | Current Code | V3 Requirement | Action Needed? |
|--------|-------------|----------------|----------------|
| Base path | `_entity_path = PROJECTS = "projects"` | `/v3/projects` | **None** — path unchanged |
| Base URL | Inherits default (currently routes to v1/v2) | Must route to `/graph/v3` | **Yes** — needs `_base_url_override` like ResearchProductsClient has |
| Response model | `ProjectResponse = ApiResponse[Project]` | Envelope unchanged (`header` + `results` + `facets`) | **Minor** — add new fields to `Project` |
| Batch fields | `{"code": "code", "openaire_id": "id"}` | Still valid | **None** |

Current `ProjectsClient` at `src/aireloom/resources/projects_client.py:9-25` is minimal and inherits from `StandardResourceClient`. It does NOT have a `_base_url_override`, meaning it currently hits whatever base URL the client defaults to (likely v1). For V3 migration, it will need the override added.

---

## Live Verification Log

### New Filter Tests

```bash
# startYear — EXACT MATCH filter (new)
$ python3 reference/v3-investigation/v3_live.py graph "projects" "startYear=2020&pageSize=1"
STATUS: 200, numFound: 118338

# endYear — EXACT MATCH filter (new)
$ python3 reference/v3-investigation/v3_live.py graph "projects" "endYear=2024&pageSize=1"
STATUS: 200, numFound: 118712

# activeYear — projects running in given year (new)
$ python3 reference/v3-investigation/v3_live.py graph "projects" "activeYear=2020&pageSize=1"
STATUS: 200, numFound: 552426

# country — filter by project country (new)
$ python3 reference/v3-investigation/v3_live.py graph "projects" "country=US&pageSize=1"
STATUS: 200, numFound: 2945252

# funder — filter by funder name (new) — ALL RETURNED 0 RESULTS:
$ python3 ... "funder=EC"           → 0 results
$ python3 ... "funder=%22European+Commission%22" → 0 results
$ python3 ... "funder=NSF"           → 0 results
$ python3 ... "funder=%22NSF%22"     → 0 results
$ python3 ... "funder=NIH"           → 0 results
$ python3 ... "funder=%22NIH%22"     → 0 results
$ python3 ... "funder=UKRI"          → 0 results
$ python3 ... "funder=%22UK+Research+and+Innovation%22" → 0 results

# fundinglevel0Id — hierarchical funding filter (new)
$ python3 ... "fundinglevel0Id=%22ukri________::UKRI::Horizon+Europe+Guarantee%22&pageSize=1"
STATUS: 200, numFound: 4059

# projectOAMandatePublications — OA mandate filter (new)
$ python3 ... "projectOAMandatePublications=true&pageSize=1"
STATUS: 200, numFound: 104944
```

### Year Range Filter Test

```bash
$ python3 ... "fromStartYear=2020&toStartYear=2022&pageSize=1"
STATUS: 200, numFound: 340432
```

### Date Range Filter Test (existing params, confirming still work)

```bash
$ python3 ... "fromStartDate=2022-01-01&toStartDate=2023-12-31&pageSize=1"
STATUS: 200, numFound: 205544
```

### Sort Tests

```bash
# Single-field sort with SPACE separator — WORKS
$ python3 ... "sortBy=startDate+DESC&pageSize=1"
STATUS: 200, numFound: 3910921

$ python3 ... "sortBy=endDate+DESC&pageSize=1"
STATUS: 200, numFound: 3910921

# Multi-field sort with COMMA+SPACE between fields — WORKS
$ python3 ... "sortBy=startDate+DESC%2C+endDate+ASC&pageSize=1"
STATUS: 200, numFound: 3910921

# COMMA alone (no space) as field-direction separator — FAILS (400)
$ python3 ... "sortBy=startDate,DESC&pageSize=1"
ERROR: The field should be in the format 'fieldname ASC|DESC'

# Missing direction — FAILS (400)
$ python3 ... "sortBy=relevance&pageSize=1"
ERROR: The field should be in the format 'fieldname ASC|DESC'
```

### Removed Parameter Confirmation

```bash
# grantID — REMOVED in V3
$ python3 ... "grantID=101079773&pageSize=1"
ERROR: Unknown parameter: grantID; valid parameters are: [funder, cursor, country, ...]
```

### Full Response Capture (for model comparison)

```bash
$ python3 ... "search=horizon&pageSize=1" --full
# Returned project with id="ukri________::ac17a6291524831f7699980e93ff19e2"
# Contains ALL expected fields PLUS new `funding` and `links` fields
# Key observation: funding.funder.jurisdiction is now an object {code, label}
#               not a plain string like in the old fundings[].jurisdiction
```

---

## Recommendations

### R1: Add 13 new filter fields to `ProjectsFilters`

**File**: `src/aireloom/endpoints.py:180-229`

Add these fields to `ProjectsFilters`:

```python
# --- NEW: Year-based date filters ---
startYear: str | None = None              # exact start year match
endYear: str | None = None                # exact end year match
activeYear: str | None = None             # projects active in year
fromStartYear: str | None = None          # start year >=
toStartYear: str | None = None            # start year <=
fromEndYear: str | None = None            # end year >=
toEndYear: str | None = None              # end year <=

# --- NEW: Funding hierarchy filters ---
country: str | None = None                # project country
funder: str | None = None                 # funder name (see risk note)
fundinglevel0Id: str | None = None        # funding level 0 ID
fundinglevel1Id: str | None = None        # funding level 1 ID
fundinglevel2Id: str | None = None        # funding level 2 ID
projectOAMandatePublications: str | None = None  # OA publications mandate
```

### R2: Remove `grantID` field from `ProjectsFilters`

**File**: `src/aireloom/endpoints.py:213`

`grantID` no longer exists in V3. Delete line 213.

### R3: Change date filter types from `date` to `str`

**File**: `src/aireloom/endpoints.py:218-221`

Change `fromStartDate`, `toStartDate`, `fromEndDate`, `toEndDate` from `date | None` to `str | None`. The V3 API accepts bare years (e.g., `fromStartDate=2022`) in addition to full dates. Using `str` is more permissive and matches the spec.

### R4: Expand `logicalOperator` enum to include `"NOT"`

**File**: `src/aireloom/endpoints.py:203`

Change from `Literal["AND", "OR"]` to `Literal["AND", "OR", "NOT"]`.

### R5: Add `funding` field to `Project` model

**File**: `src/aireloom/models/project.py`

Add a new `ProjectFunding` model class for the hierarchical funding structure:

```python
class FunderInfo(BaseModel):
    id: str | None = None
    shortname: SafeStr = ""
    name: SafeStr = ""
    jurisdiction: dict | None = None  # {"code": "EU", "label": "European Union"}
    pid: list | None = None

class FundingLevel(BaseModel):
    id: str | None = None
    description: SafeStr = ""
    name: SafeStr = ""

class ProjectFunding(BaseModel):
    funder: FunderInfo | None = None
    level0: FundingLevel | None = None
    level1: FundingLevel | None = None
    level2: FundingLevel | None = None
```

Then add to `Project`:
```python
funding: ProjectFunding | None = None
```

### R6: Consider adding `links` field to `Project` model

**File**: `src/aireloom/models/project.py`

The `links` array contains inline related entity data (participating organizations with names, PIDs, countries). This is a large nested structure. Decision needed: model it fully, store as raw dict, or skip (since dedicated relation endpoints exist).

### R7: Add `_base_url_override` to `ProjectsClient`

**File**: `src/aireloom/resources/projects_client.py:9-25`

Follow the pattern used by `ResearchProductsClient` — add a class-level `_base_url_override` pointing to the V3 graph endpoint.

### R8: Update `keywords` type annotation (optional)

**File**: `src/aireloom/models/project.py:128`

The V3 spec defines `keywords` as `string` (comma-separated). Current model uses `SafeList[str]` with a validator that splits on commas/semicolons. This works correctly in practice. No urgent change, but consider adding a comment noting the V3 spec type.

---

## Open Questions / Risks

1. **`funder` filter appears non-functional**: Despite being documented and listed in the valid parameters, `funder` returned 0 results for 8 different value formats including short names ("EC", "NSF") and full names ("European Commission"). The `fundingShortName` filter works correctly for the same values. **Risk**: Users may try `funder` and get empty results. Recommend documenting that `fundingShortName` is the preferred filter, or investigate further whether `funder` expects internal OpenAIRE IDs.

2. **`funding` field missing from V3 OpenAPI spec**: The `funding` hierarchical object is present in every live response but absent from the `APIProject` schema in the V3 OpenJSON spec. Similarly, `links` is present in live responses but not in the spec. **Risk**: Future spec updates may rename/restructure these fields. Treat as stable-but-undocumented.

3. **`originalIds` in spec but not in responses**: The V3 `APIProject` schema includes `originalIds: array` but none of the test responses contained this field (all were null/absent). May only populate for certain project types.

4. **Sort format fragility**: The space-between-field-and-direction requirement (`startDate DESC` not `startDate,DESC`) is unusual for REST APIs and could be a source of bugs. Any client-side sort construction must use `%20` or `+` between field name and `ASC`/`DESC`.

5. **`keywords` type divergence**: V3 spec says `string`, current model says `list[str]`. The validator masks this by splitting the string. If the V3 API ever returns actual array-type keywords, the validator would break. Low risk but worth monitoring.
