# V3 Migration Research — Models, Ergonomics & Packaging

## Scope

Cross-cutting audit covering:
1. **All response data models** — field-by-field V3 verification against live API
2. **Ergonomics layer (`queries.py`)** — convenience function filter field mapping and required renames
3. **V3 filter-value quoting requirement** — live verification of `%22` quoting for spaces/parens
4. **Packaging/exports/type-marker** — version, `py.typed`, classifiers

## Method

- Read all model files under `src/aireloom/models/` (base, research_product, project, organization, data_source, person, relation, scholix, safe_types)
- Read filter definitions in `src/aireloom/endpoints.py` (7 filter models)
- Read ergonomics layer `src/aireloom/queries.py` (11 convenience functions + `_resolve_identifier`)
- Queried **live V3 API** via `reference/v3-investigation/v3_live.py` for each entity type with `--full` to inspect actual response JSON
- Cross-referenced V3 OpenAPI spec (`graph_v3_openapi.json`) — 60 params for research-products alone
- Tested old vs new filter names live to confirm renames

---

## Findings

### 1. Response Data Models — Field-by-Field V3 Verification

#### 1.1 Header Model (`src/aireloom/models/base.py`)

| Current Field | V3 Live Field | Type | Status | Notes |
|---|---|---|---|---|
| `queryTime` | `queryTime` | int | ✅ OK | |
| `numFound` | `numFound` | int | ✅ OK | |
| `nextCursor` | `nextCursor` | str\|null | ✅ OK | Present even when no more pages (null) |
| `pageSize` | `pageSize` | int | ✅ OK | |
| `page` | `page` | int | ✅ OK | 1-indexed on regular endpoints |
| `maxScore` | `maxScore` | float | ✅ OK | |
| `totalPages` | *(not in regular header)* | — | ⚠️ Links-only | Only appears in `/research-products/links` envelope |
| `totalLinks` | *(not in regular header)* | — | ⚠️ Links-only | Only appears in `/research-products/links` envelope |

#### 1.2 ResearchProduct (`src/aireloom/models/research_product.py`)

| Current Field | V3 Live Field | Type | Gap? | Notes |
|---|---|---|---|---|
| `id` | `id` | str | ✅ | |
| `pid` | `pids` | list[Pid] | ✅ | Model maps correctly |
| `mainTitle` | `mainTitle` | str | ✅ | |
| `subTitle` | `subTitle` | str\|null | ✅ | |
| `otherTitles` | *null* | — | ✅ | Correctly optional |
| `descriptions` | *null* | — | ✅ | |
| `authors` | `authors` | list[dict] | ✅ | Contains orcid, fullName, rank, order |
| `contributors` | *null* | — | ✅ | |
| `publicationDate` | `publicationDate` | str | ✅ | ISO date string |
| `publisher` | `publisher` | str\|null | ✅ | |
| `sources` | `sources` | list[str] | ✅ | List of DOI-like strings |
| `type` | `type` | str | ✅ | "publication", "dataset", etc. |
| `language` | `language` | {code,label} | ✅ | |
| `countries` | *null* | — | ✅ | |
| `subjects` | `subjects` | list[{provenance,subject}] | ✅ | |
| `pids` | `pids` | {scheme,value} | ✅ | |
| `instances` | `instances` | list[dict] | ✅ | Rich: collectedFrom, hostedBy, pids, urls, type, refereed, publicationDate |
| `container` | `container` | object | ✅ | Has conferenceDate/Place, edition, ep, iss, issnLinking/Online/Printed, name, sp, vol |
| `bestAccessRight` | `bestAccessRight` | null | ✅ | Null when no access right info |
| `codeRepositoryUrl` | *null* | — | ✅ | |
| `embargoEndDate` | *null* | — | ✅ | |
| `openAccessColor` | *null* | — | ✅ | |
| `indicators` | `indicators` | {citationImpact:{...}} | ✅ | citationCount, impulse, influence, popularity + classes |
| `collectedFrom` | `collectedFrom` | list[dict] | ✅ | {key,value} format |
| `communities` | `communities` | list[dict] | ✅ | {code,acronym,label,id,type} |
| `contactGroups` | *null* | — | ✅ | |
| `contactPeople` | *null* | — | ✅ | |
| `coverages` | *null* | — | ✅ | |
| `dateOfCollection` | *null* | — | ✅ | |
| `documentationUrls` | *null* | — | ✅ | |
| `formats` | *null* | — | ✅ | |
| `geoLocations` | *null* | — | ✅ | |
| `tools` | *null* | — | ✅ | |
| `version` | *null* | — | ✅ | |
| `size` | *null* | — | ✅ | |
| `programmingLanguage` | *null* | — | ✅ | |
| `lastUpdateTimeStamp` | *null* | — | ✅ | |
| `organizations` | `organizations` | list[dict] | ✅ | {name,id,type,shortname} |
| `projects` | *null* | — | ✅ | |
| `links` | `links` | list | ✅ | Empty array when none |
| `originalIds` | `originalIds` | list[str] | ✅ | |
| **NEW: `eoscIfGuidelines`** | `eoscIfGuidelines` | null | 🆕 **MISSING from model** | Field exists in V3 response; not declared in Pydantic model |
| **NEW: `green`** | `green` | bool | 🆕 **MISSING from model** | Boolean flag in V3 response |
| **NEW: `inDiamondJournal`** | `inDiamondJournal` | bool | 🆕 **MISSING from model** | Boolean flag in V3 response |
| **NEW: `isGreen`** | `isGreen` | bool | 🆕 **MISSING from model** | Boolean flag in V3 response |
| **NEW: `isInDiamondJournal`** | `isInDiamondJournal` | bool | 🆕 **MISSING from model** | Boolean flag in V3 response |
| **NEW: `publiclyFunded`** | `publiclyFunded` | bool | 🆕 **MISSING from model** | Boolean flag in V3 response |

**Undeclared V3 fields found in live response that should be added to `ResearchProduct`:**
- `eoscIfGuidelines` (null in tested record)
- `green: bool = False`
- `inDiamondJournal: bool = False`
- `isGreen: bool`
- `isInDiamondJournal: bool`
- `publiclyFunded: bool`

#### 1.3 Project (`src/aireloom/models/project.py`)

| Current Field | V3 Live Field | Type | Gap? | Notes |
|---|---|---|---|---|
| `id` | `id` | str | ✅ | |
| `code` | `code` | str | ✅ | |
| `acronym` | *null* | — | ✅ | |
| `title` | `title` | str | ✅ | |
| `startDate` | `startDate` | str | ✅ | |
| `endDate` | `endDate` | str | ✅ | |
| `callIdentifier` | *null* | — | ✅ | |
| `summary` | *null* | — | ✅ | |
| `keywords` | *null* | — | ✅ | |
| `websiteUrl` | *null* | — | ✅ | |
| `funding` | `funding` | {funder,jurisdiction,level0,level1,level2} | ✅ | funder has id,shortname,name,jurisdiction,pid |
| `fundings` | `fundings` | list[dict] | ✅ | Array of funding objects |
| `granted` | `granted` | {currency,totalCost,fundedAmount} | ✅ | |
| `h2020Programmes` | *null* | — | ✅ | |
| `openAccessMandateForPublications` | `openAccessMandateForPublications` | bool | ✅ | |
| `openAccessMandateForDataset` | `openAccessMandateForDataset` | bool | ✅ | |
| `subjects` | *null* | — | ✅ | |
| `links` | `links` | list[dict] | ✅ | |

**No missing fields detected for Project model.**

#### 1.4 Organization (`src/aireloom/models/organization.py`)

| Current Field | V3 Live Field | Type | Gap? | Notes |
|---|---|---|---|---|
| `id` | `id` | str | ✅ | |
| `legalName` | `legalName` | str | ✅ | |
| `legalShortName` | *null* | — | ✅ | |
| `alternativeNames` | `alternativeNames` | list[str] | ✅ | |
| `country` | `country` | {code,label} | ✅ | |
| `pids` | `pids` | list[dict] | ✅ | |
| `websiteUrl` | *null* | — | ✅ | |
| `collectedFrom` | `collectedFrom` | list[dict] | ✅ | |
| `originalIds` | `originalIds` | list[str] | ✅ | |
| **NEW: `fundings`** | `fundings` | list[dict] | 🆕 **MISSING from model** | New in V3 — array of funding info |

**Missing field:** `fundings: list[Funding] | None = None`

#### 1.5 DataSource (`src/aireloom/models/data_source.py`)

| Current Field | V3 Live Field | Type | Gap? | Notes |
|---|---|---|---|---|
| `id` | `id` | str | ✅ | |
| `officialName` | `officialName` | str | ✅ | |
| `englishName` | *null* | — | ✅ | |
| `openaireCompatibility` | `openaireCompatibility` | str | ✅ | |
| `type` | `type` | {scheme,value} | ✅ | |
| `dateOfValidation` | `dateOfValidation` | str | ✅ | |
| `description` | `description` | str\|null | ✅ | |
| `thematic` | `thematic` | bool | ✅ | |
| `versioning` | `versioning` | bool | ✅ | |
| `logoUrl` | *null* | — | ✅ | |
| `languages` | `languages` | list[str] | ✅ | |
| `subjects` | `subjects` | list[str] | ✅ | |
| `collectedFrom` | `collectedFrom` | list[dict] | ✅ | |
| `originalIds` | `originalIds` | list[str] | ✅ | |
| **NEW: `eoscdatasourcetype`** | `eoscdatasourcetype` | {code,label} | 🆕 **MISSING from model** | EOSC datasource type classification |
| **NEW: `jurisdiction`** | `jurisdiction` | null | 🆕 **MISSING from model** | Jurisdiction info |
| **NEW: `links`** | `links` | list[dict] | 🆕 **MISSING from model** | Related links |
| **NEW: `odlanguages`** | `odlanguages` | list[str] | 🆕 **MISSING from model** | OpenDOAR languages |
| **NEW: `openaireCompatibilityId`** | `openaireCompatibilityId` | str | 🆕 **MISSING from model** | Compatibility ID string |

**5 missing fields** for DataSource — all new in V3.

#### 1.6 Person (`src/aireloom/models/person.py`)

| Current Field | V3 Live Field | Type | Gap? | Notes |
|---|---|---|---|---|
| `id` | `id` | str | ✅ | |
| `givenName` | `givenName` | str | ✅ | |
| `familyName` | `familyName` | str | ✅ | |
| `alternativeNames` | `alternativeNames` | list[str] | ✅ | |
| `biography` | *null* | — | ✅ | |
| `coAuthors` | `coAuthors` | list[str] | ✅ | |
| `consent` | *null* | — | ✅ | |
| `context` | *null* | — | ✅ | |
| `indicator` | *null* | — | ✅ | |
| `originalId` | `originalId` | list[str] | ✅ | |
| `subject` | *null* | — | ✅ | |

**No missing fields detected for Person model.**

### 2. Filter Models — V3 Parameter Renames (LIVE VERIFIED)

The following filter field names **changed between V1/V2 and V3**. All three were confirmed by hitting the live V3 API:

| Old Name (V1/V2) | New Name (V3) | Live Test Result | Used In |
|---|---|---|---|
| `authorOrcid` | `authorId` | ❌ 400 → ✅ 200 | `queries.py:150`, `queries.py:256` |
| `bestOpenAccessRightLabel` | `accessRightLabel` | ❌ 400 → ✅ 200 | `queries.py:112`, `queries.py:259` |
| `sdg` | `sdgLabel` | ❌ 400 → ✅ 200 | `endpoints.py:93` |

Additionally, V3 introduces these **new filter parameters** not present in current code:

| New V3 Parameter | Type (OpenAPI) | Notes |
|---|---|---|
| `fromPublicationYear` | integer | Year-based filtering (separate from date range) |
| `toPublicationYear` | integer | Year upper bound |
| `publicationYear` | string | Exact year match |
| `excludePubDateRange` | boolean | Exclude publications in date range |
| `hasLicense` | boolean | Filter by license presence |
| `relFunder` | string | Filter by funder name/ID |
| `relFundingLevel0Id` | string | Funding hierarchy level 0 |
| `relFundingLevel1Id` | string | Funding hierarchy level 1 |
| `relFundingLevel2Id` | string | Funding hierarchy level 2 |
| `relHostingDataSource` | string | Hosting datasource name (vs ID) |
| `relOrganization` | string | Organization name (vs ID) |
| `relProject` | string | Project name (vs ID) |
| `includeStats` | boolean | Include statistics in response |
| `source` | string | Source filter |
| `subCommunity` | string | Sub-community filter |
| `eoscIfGuidelines` | string | EOSC IF guidelines filter |

**V3 parameters removed/no longer valid** (in current code but rejected by V3):

| Parameter | Status |
|---|---|
| `description` | Not in V3 param list (may still work as undocumented) |
| `impulseClass` | Not in V3 error message's valid list, but IS in OpenAPI spec — needs live test |
| `popularityClass` | Same as above |
| `instanceType` | Same as above |
| `isInDiamondJournal` | Same as above |
| `isPubliclyFunded` | Same as above |
| `relCommunityId` | Still valid per error message |
| `relCollectedFromDatasourceId` | NOT in V3 valid list — renamed? |

### 3. Ergonomics Layer (`queries.py`) — Function Inventory

Every convenience function, its filter references, and required changes:

| Function | Line(s) | Filter Model | Filter Fields Referenced | Required Rename(s) |
|---|---|---|---|---|
| `publications_by_doi` | 50–62 | `ResearchProductsFilters` | `pid` | None |
| `publications_by_organization` | 94–119 | `ResearchProductsFilters` | `search`, `relOrganizationId`, `rorId`, `type`, `fromPublicationDate`, `toPublicationDate`, **`bestOpenAccessRightLabel`** | **`bestOpenAccessRightLabel` → `accessRightLabel`** (line 112) |
| `publications_by_author` | 145–163 | `ResearchProductsFilters` | `authorFullName`, **`authorOrcid`**, `type` | **`authorOrcid` → `authorId`** (line 150) |
| `publications_by_project` | 189–223 | `ResearchProductsFilters` | `search`, `relProjectId`, `relProjectCode`, `hasProjectRel`, `type` | None |
| `count_publications` | 252–261 | `ResearchProductsFilters` | `type`, `search`, `pid`, **`authorOrcid`**, `relOrganizationId`, `relProjectId`, **`bestOpenAccessRightLabel`** | **Both**: line 256 (`authorOrcid→authorId`), line 259 (`bestOpenAccessRightLabel→accessRightLabel`) |
| `projects_by_organization` | 290–306 | `ProjectsFilters` | `search`, `relOrganizationId` | None |
| `citing_works` | 334–343 | `ScholixFilters` | `targetPid`, `sourceType` | None (Scholix unchanged) |
| `related_datasets` | 364–369 | `ScholixFilters` | `sourcePid`, `targetType` | None |
| `all_links` | 392–414 | `ScholixFilters` | `sourcePid`, `targetPid` | None |
| `_resolve_identifier` | 422–463 | N/A (helper) | Populates `filter_kwargs` dict consumed by callers above | Indirect — callers pass wrong key names |

**Total impact: 4 lines across 2 functions need filter-key renames.**

### 4. Filter Value Quoting Requirement (LIVE VERIFIED)

V3 **requires double-quoting** of filter values containing spaces, parentheses, or logical operators.

| Test | Query String | HTTP Status | Response Snippet |
|---|---|---|---|
| Unquoted space value | `accessRightLabel=Open+Access` | **400** | `"Invalid value for 'accessRightLabel'. Values containing spaces, parentheses or logical operators must be wrapped in double quotes"` |
| Quoted space value | `accessRightLabel=%22Open+Access%22` | **200** | `numFound: 139770230` |
| Inline OR with quotes | `countryCode=(%22US%22+OR+%22GB%22)` | **200** | Returns results |
| SDG label (quoted) | `sdgLabel=%224.+Education%22` | **200** | `numFound: 5328980` |
| SDG label (unquoted number) | `sdgLabel=1` | **400** | Allowed values are full names like `'1. No poverty'` |

**Current serialization path:**
- `src/aireloom/resources/research_products_client.py:98`: `params.update(filters.model_dump(exclude_none=True))`
- `src/aireloom/resources/scholix_client.py:121`: `filters.model_dump(exclude_none=True, by_alias=True)`

Neither path applies any quoting. Values like `"OPEN"` for `accessRightLabel` (used in `queries.py:112,259`) will fail in V3 because the V3 parameter is now `accessRightLabel` which expects quoted values for anything with spaces.

**Note:** The value `"OPEN"` (no spaces) may work without quoting for `accessRightLabel=OPEN` — this needs testing. But user-facing values like `"Open Access"` definitely require quoting.

### 5. Packaging / Exports / Type Marker

| Item | Value | Location | Status |
|---|---|---|---|
| Version | `0.4.0` | `pyproject.toml` | ✅ Current |
| Python requirement | `>=3.12` | `pyproject.toml` | ✅ Enforces modern syntax |
| `py.typed` marker | Exists | `src/aireloom/py.typed` | ✅ PEP 561 compliant |
| Typing classifier | `"Typing :: Typed"` | `pyproject.toml` | ✅ Declared |
| Dev status classifier | `"Development Status :: 3 - Alpha"` | `pyproject.toml` | ⚠️ Should update to Beta after V3 migration |
| Main export (`__init__.py`) | Exports: client, session, exceptions, `Header`, `BaseEntity`, all entity models, all relation models | `src/aireloom/__init__.py` | ✅ Complete |
| Dependency | `bibliofabric>=0.4.2,<0.5.0` | `pyproject.toml` | ✅ Provides `SafeList`, `SafeStr` |

---

## Live Verification

### Commands Run

```bash
# ResearchProduct full response
python3 reference/v3-investigation/v3_live.py graph "research-products" "search=covid&pageSize=1" --full

# Project full response  
python3 reference/v3-investigation/v3_live.py graph "projects" "title=covid&pageSize=1" --full

# Organization full response
python3 reference/v3-investigation/v3_live.py graph "organizations" "legalName=utrecht&pageSize=1" --full

# DataSource full response
python3 reference/v3-investigation/v3_live.py graph "datasources" "officialName=zenodo&pageSize=1" --full

# Person full response
python3 reference/v3-investigation/v3_live.py graph "persons" "givenName=John&pageSize=1" --full

# Old filter name rejections (all 400):
python3 reference/v3-investigation/v3_live.py graph "research-products" "authorOrcid=0000-0001-8569-7X&pageSize=1"
python3 reference/v3-investigation/v3_live.py graph "research-products" "bestOpenAccessRightLabel=OPEN&pageSize=1"
python3 reference/v3-investigation/v3_live.py graph "research-products" "sdg=1&pageSize=1"

# New filter name acceptances (all 200):
python3 reference/v3-investigation/v3_live.py graph "research-products" "authorId=0000-0001-8569-7990-364e6a3c&pageSize=1"
python3 reference/v3-investigation/v3_live.py graph "research-products" "accessRightLabel=%22Open+Access%22&pageSize=1"
python3 reference/v3-investigation/v3_live.py graph "research-products" "sdgLabel=%224.+Education%22&pageSize=1"

# Quoting requirement tests:
python3 reference/v3-investigation/v3_live.py graph "research-products" "accessRightLabel=Open+Access&pageSize=1"     # 400
python3 reference/v3-investigation/v3_live.py graph "research-products" "accessRightLabel=%22Open+Access%22&pageSize=1"  # 200
python3 reference/v3-investigation/v3_live.py graph "research-products" "countryCode=(%22US%22+OR+%22GB%22)&pageSize=1"  # 200

# New V3-only parameters:
python3 reference/v3-investigation/v3_live.py graph "research-products" "publicationYear=2024&pageSize=1"  # 200

# Full V3 valid parameter list extracted from 400 error message (31 params)
```

### Key Observed Responses

**ResearchProduct (first result, truncated):**
```json
{
  "id": "__oaipool__oai:arXiv.org:2412.12345",
  "mainTitle": "...",
  "type": "publication",
  "eoscIfGuidelines": null,
  "green": false,
  "inDiamondJournal": false,
  "isGreen": true,
  "isInDiamondJournal": false,
  "publiclyFunded": true,
  "indicators": {
    "citationImpact": {"citationCount": ..., "impulse": ..., ...}
  },
  ...
}
```

**Organization (new `fundings` field):**
```json
{
  "id": "__oaipool__...",
  "legalName": "Utrecht University",
  "fundings": [{"funder": "...", "fundingStream": "..."}],
  ...
}
```

**DataSource (5 new fields):**
```json
{
  "id": "__oaipool__...",
  "eoscdatasourcetype": {"code": "pubsrepository::institutional", "label": "..."},
  "jurisdiction": null,
  "links": [...],
  "odlanguages": ["eng"],
  "openaireCompatibilityId": "...",
  ...
}
```

---

## Recommendations

### R1: Add Missing Fields to ResearchProduct Model
**File:** `src/aireloom/models/research_product.py`

Add these fields to the `ResearchProduct` class:
```python
eoscIfGuidelines: str | None = None
green: bool = False
inDiamondJournal: bool = False
isGreen: bool | None = None
isInDiamondJournal: bool | None = None
publiclyFunded: bool | None = None
```

### R2: Add Missing `fundings` Field to Organization Model
**File:** `src/aireloom/models/organization.py`
```python
fundings: list[dict] | None = None  # or define a proper Funding sub-model
```

### R3: Add 5 Missing DataSource Fields
**File:** `src/aireloom/models/data_source.py`
```python
eoscdatasourcetype: ControlledField | None = None
jurisdiction: ControlledField | None = None
links: list[dict] | None = None
odlanguages: list[str] | None = None
openaireCompatibilityId: str | None = None
```

### R4: Rename Filter Fields in `endpoints.py`
**File:** `src/aireloom/endpoints.py`

| Line | Old | New |
|---|---|---|
| 85 | `authorOrcid: str \| None = None` | `authorId: str \| None = None` |
| 87 | `bestOpenAccessRightLabel: str \| None = None` | `accessRightLabel: str \| None = None` |
| 93 | `sdg: list[str] \| None = None` | `sdgLabel: list[str] \| None = None` |

Update docstrings and the `model_config` line accordingly.

### R5: Update Ergonomics Layer Filter References
**File:** `src/aireloom/queries.py`

| Line | Old | New |
|---|---|---|
| 112 | `filter_kwargs["bestOpenAccessRightLabel"]` | `filter_kwargs["accessRightLabel"]` |
| 150 | `"orcid": "authorOrcid"` | `"orcid": "authorId"` |
| 256 | `authorOrcid=author_orcid` | `authorId=author_orcid` |
| 259 | `bestOpenAccessRightLabel="OPEN"` | `accessRightLabel="OPEN"` |

### R6: Implement Auto-Quoting for Filter Values
**File:** `src/aireloom/resources/base_resource.py` (or wherever `model_dump` is called)

Before calling `filters.model_dump()`, detect values containing spaces, parentheses, `OR`, `AND`, `NOT` and wrap them in `%22...%22`. Implementation options:

1. **Pydantic validator** on each filter model field — complex, repetitive
2. **Custom serializer** in `model_dump()` via `serializer` decorator — cleanest
3. **Post-processing function** applied after `model_dump()` before URL encoding — simplest, most maintainable

Recommended approach: Option 3 — add a helper function:
```python
def _quote_filter_values(params: dict[str, Any]) -> dict[str, Any]:
    """Wrap filter values containing spaces/parens/operators in double quotes."""
    import re
    out = {}
    for k, v in params.items():
        if isinstance(v, str) and re.search(r'[\s()\w+(OR|AND|NOT)\b]', v):
            v = f'"{v}"'
        elif isinstance(v, list):
            v = [f'"{item}" if isinstance(item, str) and re.search(r'[\s()]', item) else item for item in v]
        out[k] = v
    return out
```

Apply at `research_products_client.py:98` and equivalent points.

### R7: Consider Adding New V3-Only Filter Parameters
**File:** `src/aireloom/endpoints.py` — `ResearchProductsFilters`

High-value additions:
- `fromPublicationYear: int | None = None`
- `toPublicationYear: int | None = None`
- `publicationYear: str | None = None`
- `relFunder: str | None = None`
- `includeStats: bool | None = None`

### R8: Update Development Status Classifier
**File:** `pyproject.toml`

Change `"Development Status :: 3 - Alpha"` → `"Development Status :: 4 - Beta"` after V3 migration completes.

---

## Open Questions / Risks

1. **`impulseClass`, `popularityClass`, `instanceType`, `isInDiamondJournal`, `isPubliclyFunded` as filters**: These appear in the V3 OpenAPI spec but were NOT listed in the live API's "valid parameters" error message. They may be accepted silently or may cause 400s. Needs individual live testing.

2. **`relCollectedFromDatasourceId` filter**: Not in V3's valid-parameter list from the error message. May have been renamed to something else in V3.

3. **SDG label values changed format**: V3 uses full text labels (`"4. Education"`) rather than numeric codes. Code passing numeric SDG values must be updated.

4. **Quoting edge cases**: Need to test whether simple alphanumeric values like `"OPEN"` for `accessRightLabel` work without quoting. If they do, only user-facing values need auto-quoting.

5. **`description` filter**: Present in current `ResearchProductsFilters` but absent from both V3 error-message param list AND OpenAPI spec. Likely dead code for V3.

6. **Backward compatibility**: Users constructing `ResearchProductsFilters(authorOrcid=...)` directly will get Pydantic errors after rename unless aliases are added. Recommend adding `Field(alias="authorOrcid")` during transition or making a hard break for the major version bump.
