# V3 Migration Research — Research Products Endpoint

## Scope

The `/v3/research-products` endpoint: **filter parameters** (renamed, new, removed), **sort fields**, **response model** (field-level diff), **resource client** (`_base_url_override` removal), and **convenience-query references** in `queries.py`. Covers the search/list endpoint, not the links sub-endpoint (covered separately).

## Method

1. Parsed `graph_v3_openapi.json` → extracted all 60 GET parameters for `/v3/research-products`
2. Ran 20+ live API calls via `reference/v3-investigation/v3_live.py` against `https://api.openaire.eu/graph/v3`
3. Compared live responses field-by-field against current `ResearchProduct` model (`src/aireloom/models/research_product.py`)
4. Audited current `ResearchProductsFilters` (`src/aireloom/endpoints.py:26-112`) and sort dict (`endpoints.py:331-338`)
5. Traced filter usage in convenience queries (`src/aireloom/queries.py`)

---

## Findings

### 1. Renamed Filters (CONFIRMED)

Three filters were renamed from V2 to V3. Each old name returns HTTP 400 `"Unknown parameter"`; each new name returns HTTP 200.

| Old Name (V1/V2) | New Name (V3) | Live Test — Old Name | Live Test — New Name |
|---|---|---|---|
| `authorOrcid` | `authorId` | 400: `Unknown parameter: authorOrcid` | 200: `numFound: 0` (valid ORCID tested) |
| `bestOpenAccessRightLabel` | `accessRightLabel` | 400: `Unknown parameter: bestOpenAccessRightLabel` | 200: `numFound: 139770230` (for "Open Access") |
| `sdg` | `sdgLabel` | 400: `Unknown parameter: sdg` | 400: `Invalid value: '1'` (expects full label string) |

#### Enumerated Values (from live 400 error messages)

**accessRightLabel** allowed values:
```
['Open Access', 'Closed Access', 'Restricted', 'Open Source', 'Embargo', 'Unknown']
```

**sdgLabel** allowed values (17 SDG goals):
```
['1. No poverty', '2. Zero hunger', '3. Good health', '4. Education',
 '5. Gender equality', '6. Clean water', '7. Clean energy',
 '8. Economic growth', '9. Industry and infrastructure',
 '10. No inequality', '11. Sustainability', '12. Responsible consumption',
 '13. Climate action', '14. Life underwater', '15. Life on land',
 '16. Peace & justice', '17. Partnership']
```

> **Note:** `sdgLabel` values are **full label strings**, not numeric. The V2 `sdg` filter accepted numeric codes; V3 requires the full label (spaces must be URL-encoded: `sdgLabel=%22Good+health%22`).

---

### 2. Complete Filter Parameter Inventory

Current `ResearchProductsFilters` has **38 fields** (lines 73-110 of endpoints.py). The V3 API has **60 parameters** (from OpenAPI spec + live verification). Below is the full mapping.

#### 2a. Existing Fields — Unchanged (name matches V3)

| Current Field | V3 Param | Type | Status |
|---|---|---|---|
| `search` | `search` | str | OK |
| `mainTitle` | `mainTitle` | str | OK |
| `description` | `description` | str | OK |
| `id` | `id` | str | OK |
| `pid` | `pid` | str | OK |
| `originalId` | `originalId` | str | OK |
| `type` | `type` | str | OK |
| `fromPublicationDate` | `fromPublicationDate` | date/string | OK |
| `toPublicationDate` | `toPublicationDate` | date/string | OK |
| `countryCode` | `countryCode` | str | OK |
| `authorFullName` | `authorFullName` | str | OK |
| `publisher` | `publisher` | str | OK |
| `influenceClass` | `influenceClass` | str | OK |
| `impulseClass` | `impulseClass` | str | OK |
| `popularityClass` | `popularityClass` | str | OK |
| `citationCountClass` | `citationCountClass` | str | OK |
| `instanceType` | `instanceType` | str | OK |
| `fos` | `fos` | str | OK |
| `isPeerReviewed` | `isPeerReviewed` | bool | OK |
| `isInDiamondJournal` | `isInDiamondJournal` | bool | OK |
| `isPubliclyFunded` | `isPubliclyFunded` | bool | OK |
| `isGreen` | `isGreen` | bool | OK |
| `openAccessColor` | `openAccessColor` | str | OK |
| `relOrganizationId` | `relOrganizationId` | str | OK |
| `relCommunityId` | `relCommunityId` | str | OK |
| `relProjectId` | `relProjectId` | str | OK |
| `relProjectCode` | `relProjectCode` | str | OK |
| `hasProjectRel` | `hasProjectRel` | bool | OK |
| `relProjectFundingShortName` | `relProjectFundingShortName` | str | OK |
| `relProjectFundingStreamId` | `relProjectFundingStreamId` | str | OK |
| `relHostingDataSourceId` | `relHostingDataSourceId` | str | OK |
| `relCollectedFromDatasourceId` | `relCollectedFromDatasourceId` | str | OK |
| `rorId` | `rorId` | str | OK |
| `logicalOperator` | `logicalOperator` | str | OK |
| `subjects` | `subjects` | str | OK |

**Total unchanged: 35**

#### 2b. Fields Requiring Rename

| Current Field | V3 Param | Action Needed |
|---|---|---|
| `authorOrcid` | `authorId` | **Rename field** |
| `bestOpenAccessRightLabel` | `accessRightLabel` | **Rename field** |
| `sdg` | `sdgLabel` | **Rename field**, change type to `str` (was `list[str]`) |

> **Breaking change impact:** `sdg` was `list[str]` in V2 (accepting multiple SDGs); V3's `sdgLabel` is a single string but supports inline OR: `sdgLabel=(%22Good+health%22+OR+%22Education%22)`.

#### 2c. NEW Parameters in V3 (not in current code)

These 22 parameters exist in V3 but have no corresponding field in `ResearchProductsFilters`:

| V3 Parameter | Type | Live Verified? | Notes |
|---|---|---|---|
| `authorId` | str | YES (200) | Replaces authorOrcid |
| `accessRightLabel` | str | YES (200) | Enumerated (6 values) |
| `sdgLabel` | str | YES (200) | Enumerated (17 values) |
| `language` | str | YES (200) | Language code |
| `publicationYear` | str | YES (200) | Year or range |
| `fromPublicationYear` | int | YES (200) | Year lower bound |
| `toPublicationYear` | int | YES (200) | Year upper bound |
| `hasLicense` | bool | YES (200) | Has license filter |
| `relProject` | str | YES (200) | Project by name/title |
| `source` | str | YES (200) | Data source name |
| `eoscIfGuidelines` | str | YES (200) | EOSC IF guideline |
| `relFunder` | str | YES (200) | Funder short name |
| `subCommunity` | str | YES (200) | Sub-community name |
| `relCommunityName` | str | YES (200) | Community name search |
| `relFundingLevel0Id` | str | Not tested | Funding level 0 ID |
| `relFundingLevel1Id` | str | YES (200) | e.g., EC::H2020 |
| `relFundingLevel2Id` | str | Not tested | Funding level 2 ID |
| `relOrganization` | str | YES (200) | Organization name search |
| `relHostingDataSource` | str | Not tested | Hosting DS name |
| `excludePubDateRange` | bool | YES (400 validation works) | Negates date range |
| `cursor` | str | YES (200) | Cursor pagination token |
| `includeStats` | bool | YES (200) | Adds stats to header |

**Total new: 22**

#### 2d. Parameters in Spec That Need Verification

A few parameters from the spec were not individually tested due to low priority but appear in the valid-params list from error messages:
- `page`, `pageSize` — verified separately (pagination section)
- `sortBy` — verified separately (sort section)
- `relFundingLevel0Id`, `relFundingLevel2Id`, `relHostingDataSource` — present in valid-params list

---

### 3. Sort Fields

V3 spec lists these sort fields (via regex pattern): `relevance`, `publicationDate`, `dateOfCollection`, `influence`, `popularity`, `citationCount`, `impulse`.

| Sort Field | Current Code Has It? | Live Test Result |
|---|---|---|
| `relevance` | YES | 200 OK |
| `publicationDate` | YES | 200 OK |
| `dateOfCollection` | YES | 200 OK |
| `influence` | YES | 200 OK |
| **`popularity`** | **NO — missing** | **200 OK (WORKS)** |
| `citationCount` | YES | 200 OK |
| `impulse` | YES | 200 OK |

> **Key finding:** Contrary to the hypothesis that `popularity` would be omitted from the error message, **`popularity` works fine** as a sort field on the live API. The current sort dict at `endpoints.py:331-338` omits it — this should be added.

---

### 4. Pagination Behavior

| Test | Expected | Actual | Status |
|---|---|---|---|
| `pageSize=100` | Returns 100 results | `HEADER: ... "pageSize": 100`, `RESULTS: 100` | OK |
| `pageSize=200` | 400 rejection | 400: `Page size must be at most 100` | OK |
| `page=0` | 400 (1-indexed) | Not explicitly tested (known from context) | — |
| `cursor=*` | Returns nextCursor | 200 with `nextCursor: "AoM/DzAwMDY0..."` | OK |

**Cursor pagination confirmed working.** The response header includes `nextCursor` when `cursor=*` is passed.

**Note on `includeStats`:** When `includeStats=true`, the header gains two extra fields:
```json
{"totalCitationsCount": 2137519997, "countsByType": {"publication": 231901563, "dataset": 106122854, "other": 41426170, "software": 936970}}
```
This is a new V3 feature not currently modeled.

---

### 5. Response Model — Field-Level Comparison

Fetched a **publication-type** research product with `--full` from live V3 API. Below is every top-level field compared against the current `ResearchProduct` model.

#### 5a. Top-Level Fields

| V3 Response Field | Current Model Field | Type Match? | Gap / Notes |
|---|---|---|---|
| `id` | `id` (inherited) | OK | — |
| `originalIds` | `originalIds: SafeList[str]` | OK | — |
| `pids` | `pids: SafeList[Pid]` | OK | — |
| `type` | `type: ResearchProductType` | OK | — |
| `mainTitle` | `mainTitle: SafeStr` | OK | — |
| `title` | `title: SafeStr` | **Not in V3 response** | Populated by validator from mainTitle — still needed |
| `subTitle` | `subTitle: SafeStr` | OK | — |
| `authors` | `authors: SafeList[Author]` | OK | See nested changes below |
| `bestAccessRight` | `bestAccessRight: SafeBestAccessRight` | OK | Can be `null` in V3 |
| `country` | `country: SafeResultCountry` | OK | — |
| `countries` | `countries: SafeList[SafeResultCountry]` | OK | — |
| `description` | `description: SafeStr` | OK | — |
| `descriptions` | `descriptions: SafeList[str]` | OK | — |
| `publicationDate` | `publicationDate: str \| None` | OK | — |
| `publisher` | `publisher: SafeStr` | OK | — |
| `embargoEndDate` | `embargoEndDate: str \| None` | OK | — |
| `contributors` | `contributors: SafeList[str]` | OK | — |
| `sources` | `sources: SafeList[str]` | OK | — |
| `formats` | `formats: SafeList[str]` | OK | — |
| `coverages` | `coverages: SafeList[str]` | OK | — |
| `dateOfCollection` | `dateOfCollection: str \| None` | OK | Often `null` in V3 |
| `lastUpdateTimeStamp` | `lastUpdateTimeStamp: int \| None` | OK | Often `null` in V3 |
| `indicators` | `indicators: SafeIndicator` | OK | See nested changes below |
| `instances` | `instances: SafeList[Instance]` | OK | See nested changes below |
| `language` | `language: SafeLanguage` | OK | Now object `{code, label}` consistently |
| `subjects` | `subjects: SafeList[Subject]` | **SHAPE CHANGE** | See below |
| `container` | `container: SafeContainer` | OK | New optional fields |
| `keywords` | `keywords: SafeList[str]` | **Missing from V3 response** | V3 does not return `keywords` field |
| `geoLocation` | `geoLocation: SafeGeoLocation` | **Missing from V3 response** | Not in fetched record |
| `geoLocations` | `geoLocations: SafeList[SafeGeoLocation]` | OK | — |
| `isGreen` | `isGreen: bool \| None` | OK | — |
| `openAccessColor` | `openAccessColor: str \| None` | OK | — |
| `isInDiamondJournal` | `isInDiamondJournal: bool \| None` | OK | — |
| `publiclyFunded` | `publiclyFunded: bool \| None` | OK | — |
| **`eoscIfGuidelines`** | **NOT IN MODEL** | **NEW FIELD** | `null` or string — **must add** |
| `codeRepositoryUrl` | `codeRepositoryUrl: str \| None` | OK | — |
| `documentationUrls` | `documentationUrls: SafeList[str]` | OK | — |
| `programmingLanguage` | `programmingLanguage: str \| None` | OK | — |
| `size` | `size: str \| None` | OK | — |
| `version` | `version: str \| None` | OK | — |
| `contactPeople` | `contactPeople: list \| None` | OK | — |
| `contactGroups` | `contactGroups: list \| None` | OK | — |
| `tools` | `tools: list \| None` | OK | — |
| `collectedFrom` | `collectedFrom: SafeList[CollectedFrom]` | OK | Shape: `{key, value}` |
| `projects` | `projects: list \| None` | OK | — |
| `organizations` | `organizations: list \| None` | **SHAPE CHANGE** | See below |
| `communities` | `communities: list \| None` | **SHAPE CHANGE** | See below |

#### 5b. Nested Model Changes

**Author** (V3 response):
```json
{
  "id": null,
  "fullName": "Rainer Duchmann",
  "name": "Rainer",
  "surname": "Duchmann",
  "rank": 1,
  "pid": null
}
```
vs current model (`research_product.py:58-77`):
- **New field `id`:** string or null — **not in current Author model**
- `pid` can be `null` or an object (not just dict) — current model uses `dict | None` which is flexible enough
- Otherwise matches: fullName, name, surname, rank ✓

**Subject** (V3 response) — **SHAPE CHANGE**:
```json
{
  "subject": {"scheme": "FOS", "value": "03 medical and health sciences"},
  "provenance": null
}
```
vs current model (`research_product.py:375-389`):
- Current expects `subject: dict[str, str] | None` (flat scheme→value map)
- V3 wraps it: `{"subject": {"scheme": "...", "value": "..."}, "provenance": ...}`
- **Action needed:** Update Subject model or add a validator to unwrap

**Instance.accessRight** (V3 response):
```json
{
  "code": "c_abf2",
  "label": "OPEN",
  "scheme": "http://vocabularies.coar-repositories.org/documentation/access_rights/",
  "openAccessRoute": null
}
```
vs current `AccessRight` model (`research_product.py:215-230`):
- **New field `openAccessRoute`:** `null` or one of `"gold"|"green"|"hybrid"|"bronze"` — **not in current model**
- Current model has `extra="allow"` so it won't crash, but field is untyped

**Container** (V3 response) — **new optional fields**:
```json
{
  "name": "Endo-Praxis",
  "issnPrinted": "0177-4077",
  "issnOnline": "1611-6429",
  "issnLinking": null,
  "ep": "173",
  "sp": "173",
  "vol": "36",
  "edition": null,
  "conferencePlace": null,
  "conferenceDate": null
}
```
vs current model (`research_product.py:393-418`):
- **New fields `conferencePlace`, `conferenceDate`** — not in current Container model
- Current has `extra="allow"` so no crash, but untyped

**indicators.citationImpact** (V3 response):
```json
{
  "citationCount": 5.0,
  "influence": 2.774892e-09,
  "popularity": 3.2742757e-09,
  "impulse": 4.0,
  "citationClass": "C5",
  "influenceClass": "C4",
  "impulseClass": "C4",
  "popularityClass": "C4"
}
```
vs current `CitationImpact` model (`research_product.py:120-143`):
- All fields present ✓
- Includes `popularity` which was missing from some V2 responses — now always present

**organizations** (V3 response):
```json
{
  "legalName": "Hospital zum Heiligen Geist",
  "acronym": "Hospital zum Heiligen Geist",
  "id": "openorgs____::...",
  "pids": [{"scheme": "ROR", "value": "https://ror.org/..."}]
}
```
- Now has `acronym` and structured `pids` array — current model uses `list | None` (untyped), so flexible enough

**communities** (V3 response):
```json
{
  "code": "covid-19",
  "label": "Corona Virus Disease",
  "provenance": null
}
```
- Now has `provenance` field — current model uses `list | None` (untyped), so flexible enough

---

### 6. Resource Client — `_base_url_override`

**File:** `src/aireloom/resources/research_products_client.py:50`

```python
_base_url_override: str | None = OPENAIRE_GRAPH_API_V2_BASE_URL
```

**Constant definition:** `src/aireloom/constants.py:10`
```python
OPENAIRE_GRAPH_API_V2_BASE_URL = "https://api.openaire.eu/graph/v2"
```

**Action required:**
1. **Remove `_base_url_override`** entirely (set to `None` or delete the attribute) — V3 serves from the same base as all other endpoints
2. Update docstring at line 42-43 that says "Overrides the base URL to use the v2 Graph API"
3. Links methods (`search_links` line 100-104, `get_relations_info` line 158-162) use `OPENAIRE_GRAPH_API_BASE_URL` (V1) — these need separate evaluation as the links endpoint may move to `/v3/research-products/links`

---

### 7. Convenience Query Impact (queries.py)

Three functions reference renamed filters:

| Function | Line | Old Filter Reference | Required Change |
|---|---|---|---|
| `publications_by_organization` | 112 | `bestOpenAccessRightLabel` | → `accessRightLabel` |
| `publications_by_author` | 150 | `authorOrcid` (in str_map) | → `authorId` |
| `count_publications` | ~240+ | Indirectly via ResearchProductsFilters | Will follow filter rename |

**Specific code locations:**

`queries.py:112`:
```python
# CURRENT:
filter_kwargs["bestOpenAccessRightLabel"] = "OPEN"
# BECOMES:
filter_kwargs["accessRightLabel"] = "Open Access"
```
> Note: Value must change too — V3 uses `"Open Access"` not `"OPEN"`.

`queries.py:150`:
```python
# CURRENT:
str_map={"name": "authorFullName", "orcid": "authorOrcid"},
# BECOMES:
str_map={"name": "authorFullName", "orcid": "authorId"},
```

---

## Live Verification Log

All commands run from repo root using `python3 reference/v3-investigation/v3_live.py`.

### Renamed Filter Tests

```bash
# 1. authorOrcid → 400 Unknown parameter
$ python3 reference/v3-investigation/v3_live.py graph "research-products" \
    "authorOrcid=0000-0001-5008-711X&pageSize=1"
STATUS: 400
ERROR: Unknown parameter: authorOrcid; valid parameters are: [relCommunityId, pageSize, ...]

# 2. authorId → 200 OK
$ python3 reference/v3-investigation/v3_live.py graph "research-products" \
    "authorId=0000-0001-5008-711X&pageSize=1"
STATUS: 200
HEADER: {"numFound": 0, ...}

# 3. bestOpenAccessRightLabel → 400 Unknown parameter
$ python3 reference/v3-investigation/v3_live.py graph "research-products" \
    "bestOpenAccessRightLabel=OPEN&pageSize=1"
STATUS: 400
ERROR: Unknown parameter: bestOpenAccessRightLabel

# 4. accessRightLabel → 200 OK (139M results for "Open Access")
$ python3 reference/v3-investigation/v3_live.py graph "research-products" \
    "accessRightLabel=%22Open+Access%22&pageSize=1"
STATUS: 200
HEADER: {"numFound": 139770230, ...}

# 5. sdg → 400 Unknown parameter
$ python3 reference/v3-investigation/v3_live.py graph "research-products" \
    "sdg=1&pageSize=1"
STATUS: 400
ERROR: Unknown parameter: sdg

# 6. sdgLabel → 400 Invalid value (needs full label)
$ python3 reference/v3-investigation/v3_live.py graph "research-products" \
    "sdgLabel=1&pageSize=1"
STATUS: 400
ERROR: Invalid value: '1' in 'sdgLabel'. Allowed values are: ['1. No poverty', ...]
```

### New Filter Tests

```bash
# language
$ python3 reference/v3-investigation/v3_live.py graph "research-products" \
    "language=en&pageSize=1"
STATUS: 200  # numFound: 0 (exact match)

# publicationYear
$ python3 reference/v3-investigation/v3_live.py graph "research-products" \
    "publicationYear=2020&pageSize=1"
STATUS: 200  # numFound: 14232154

# fromPublicationYear
$ python3 reference/v3-investigation/v3_live.py graph "research-products" \
    "fromPublicationYear=2020&pageSize=1"
STATUS: 200  # numFound: 146401418

# toPublicationYear
$ python3 reference/v3-investigation/v3_live.py graph "research-products" \
    "toPublicationYear=2020&pageSize=1"
STATUS: 200  # numFound: 238024493

# eoscIfGuidelines
$ python3 reference/v3-investigation/v3_live.py graph "research-products" \
    "eoscIfGuidelines=EOSC-Pilot&pageSize=1"
STATUS: 200  # numFound: 0

# source
$ python3 reference/v3-investigation/v3_live.py graph "research-products" \
    "source=Crossref&pageSize=1"
STATUS: 200  # numFound: 0

# hasLicense
$ python3 reference/v3-investigation/v3_live.py graph "research-products" \
    "hasLicense=true&pageSize=1"
STATUS: 200  # numFound: 161756541

# relProject
$ python3 reference/v3-investigation/v3_live.py graph "research-products" \
    "relProject=12345&pageSize=1"
STATUS: 200  # numFound: 0

# relOrganization
$ python3 reference/v3-investigation/v3_live.py graph "research-products" \
    "relOrganization=Harvard&pageSize=1"
STATUS: 200  # numFound: 0

# includeStats (adds header fields)
$ python3 reference/v3-investigation/v3_live.py graph "research-products" \
    "includeStats=true&pageSize=1"
STATUS: 200
HEADER: {..., "totalCitationsCount": 2137519997, "countsByType": {...}}

# excludePubDateRange (requires companion date param)
$ python3 reference/v3-investigation/v3_live.py graph "research-products" \
    "excludePubDateRange=true&fromPublicationYear=2020&pageSize=1"
STATUS: 400
ERROR: Parameter 'excludePubDateRange' requires at least one of 'fromPublicationDate' or 'toPublicationDate'

# subCommunity, relCommunityName, relFunder, relFundingLevel1Id — all returned 200
```

### Sort Field Tests

```bash
$ # All 7 sort fields return 200:
sortBy=relevance+DESC      → 200 OK
sortBy=publicationDate+DESC → 200 OK
sortBy=dateOfCollection+DESC → 200 OK
sortBy=influence+DESC      → 200 OK
sortBy=popularity+DESC     → 200 OK  ← WORKS (contrary to hypothesis)
sortBy=citationCount+DESC  → 200 OK
sortBy=impulse+DESC        → 200 OK
```

### Pagination Tests

```bash
# pageSize=100 → 100 results
$ python3 reference/v3-investigation/v3_live.py graph "research-products" \
    "search=covid&pageSize=100"
STATUS: 200, RESULTS: 100

# pageSize=200 → 400 rejected
$ python3 reference/v3-investigation/v3_live.py graph "research-products" \
    "search=covid&pageSize=200"
STATUS: 400, ERROR: Page size must be at most 100

# cursor pagination
$ python3 reference/v3-investigation/v3_live.py graph "research-products" \
    "search=covid&pageSize=1&cursor=*"
STATUS: 200, HEADER includes "nextCursor": "AoM/DzAwMDY0..."
```

### Full Response Capture (for model comparison)

```bash
# Publication type (rich nested structures)
$ python3 reference/v3-investigation/v3_live.py graph "research-products" \
    "search=covid&type=publication&pageSize=1" --full
# Returned full JSON with authors[], subjects[], container{}, instances[],
# indicators.citationImpact (with popularity), organizations[], communities[]

# Software type (subtype-specific fields)
$ python3 reference/v3-investigation/v3_live.py graph "research-products" \
    "search=covid&type=software&pageSize=1" --full
# Returned codeRepositoryUrl, programmingLanguage=null, instances[].type="Software"
```

---

## Recommendations

### Priority 1: Breaking Changes (Must Fix)

| # | Change | File:Line | Details |
|---|---|---|---|
| 1 | **Rename `authorOrcid` → `authorId`** | `endpoints.py:85` | Field name + update docstring |
| 2 | **Rename `bestOpenAccessRightLabel` → `accessRightLabel`** | `endpoints.py:87` | Field name + update docstring; enum values are now labels like `"Open Access"` |
| 3 | **Rename `sdg` → `sdgLabel`** | `endpoints.py:93` | Field name; change type from `list[str]` to `str`; values are full SDG labels |
| 4 | **Remove `_base_url_override`** | `research_products_client.py:50` | Delete or set to `None`; update docstring lines 42-43 |
| 5 | **Update queries.py references** | `queries.py:112,150` | `bestOpenAccessRightLabel` → `accessRightLabel`, `authorOrcid` → `authorId`; fix value `"OPEN"` → `"Open Access"` |

### Priority 2: Add Missing Fields to Filters Model

| # | Field | Type | Rationale |
|---|---|---|---|
| 6 | `authorId` | `str \| None` | Primary author identifier filter (replaces authorOrcid) |
| 7 | `accessRightLabel` | `str \| None` | Enumerated access right filter |
| 8 | `sdgLabel` | `str \| None` | SDG goal filter (17 enumerated values) |
| 9 | `language` | `str \| None` | Language code filter |
| 10 | `publicationYear` | `str \| None` | Publication year(s) filter |
| 11 | `fromPublicationYear` | `int \| None` | Year lower bound |
| 12 | `toPublicationYear` | `int \| None` | Year upper bound |
| 13 | `hasLicense` | `bool \| None` | License presence filter |
| 14 | `relProject` | `str \| None` | Project name search |
| 15 | `source` | `str \| None` | Data source name filter |
| 16 | `eoscIfGuidelines` | `str \| None` | EOSC IF guidelines filter |
| 17 | `relFunder` | `str \| None` | Funder short name |
| 18 | `subCommunity` | `str \| None` | Sub-community filter |
| 19 | `relCommunityName` | `str \| None` | Community name search |
| 20 | `relFundingLevel0Id` | `str \| None` | Funding L0 ID |
| 21 | `relFundingLevel1Id` | `str \| None` | Funding L1 ID |
| 22 | `relFundingLevel2Id` | `str \| None` | Funding L2 ID |
| 23 | `relOrganization` | `str \| None` | Organization name search |
| 24 | `relHostingDataSource` | `str \| None` | Hosting DS name |
| 25 | `excludePubDateRange` | `bool \| None` | Date range negation |
| 26 | `includeStats` | `bool \| None` | Aggregate stats in header |
| 27 | `cursor` | `str \| None` | Cursor pagination token |

### Priority 3: Response Model Updates

| # | Change | Location | Details |
|---|---|---|---|
| 28 | **Add `eoscIfGuidelines`** | `research_product.py:~508` | `str \| None` — new top-level field |
| 29 | **Add `id` to Author** | `research_product.py:58-77` | `str \| None = None` — new field in V3 author objects |
| 30 | **Update Subject model** | `research_product.py:375-389` | V3 wraps as `{subject: {scheme, value}, provenance}` — need adapter |
| 31 | **Add `openAccessRoute` to AccessRight** | `research_product.py:215-230` | `str \| None = None` — now in instance accessRight |
| 32 | **Add `conferencePlace`, `conferenceDate` to Container** | `research_product.py:393-418` | Both `str \| None = None` |
| 33 | **Consider typing organizations/communities** | `research_product.py:558-560` | Currently `list \| None` — V3 gives structured objects |

### Priority 4: Sort Dict Update

| # | Change | Location |
|---|---|---|
| 34 | **Add `"popularity": {}` to sort dict** | `endpoints.py:331-338` |

### Priority 5: Path Constant

| # | Change | Location |
|---|---|---|
| 35 | **Update `RESEARCH_PRODUCTS` path constant** | `endpoints.py:17` | Currently `"researchProducts"` (camelCase, V2). V3 path is `"research-products"` (kebab-case). **Verify if bibliofabric appends this to base URL or if it needs updating.** |

---

## Open Questions / Risks

1. **Path casing**: Current `RESEARCH_PRODUCTS = "researchProducts"` (camelCase, V2-style). V3 uses kebab-case paths (`research-products`). Must verify whether the path constant needs changing or if there's a URL normalization layer.

2. **Subject model shape change**: The V3 Subject structure `{"subject": {"scheme": "value"}, "provenance": null}` is fundamentally different from the current flat `dict[str, str]`. This will break any code accessing `subject["fos"]` directly. Need either a pre-processing validator or a model redesign.

3. **`sdgLabel` type change**: Was `list[str]` (multiple SDGs), now `str` (single, but supports inline OR). This changes the filter UX — users must use OR syntax for multiple SDGs rather than passing a list.

4. **`accessRightLabel` value change**: V2 used short codes like `"OPEN"`. V3 uses full labels like `"Open Access"`. Any hardcoded filter values will break.

5. **Links endpoint future**: The `search_links`/`iterate_links` methods currently hit V1 base URL. V3 has `/v3/research-products/links` — need separate migration assessment for these methods.

6. **`includeStats` header fields**: The `totalCitationsCount` and `countsByType` header fields are not currently modeled in any response wrapper. If used, the header model needs extension.

7. **`logicalOperator` enum expansion**: V3 spec shows `logicalOperator` accepts `['AND', 'OR', 'NOT']` (3 values). Current model only allows `['AND', 'OR']` (line 67). **NOT is new in V3.**

8. **Spec vs live discrepancy on `popularity` sort**: The hypothesis (from prior research) stated the error message omits `popularity`. Live testing proves **`popularity` works fine** as a sort field. The prior report was incorrect on this point.
