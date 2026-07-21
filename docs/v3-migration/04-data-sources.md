# V3 Migration Research — Data Sources (`/v3/datasources`)

## Scope

The data sources endpoint: path change to all-lowercase `datasources`, 8 new filter parameters, sort behavior, response model field gaps, the persistent "organizations" copy-paste bug in the V3 spec/live API, and resource client routing.

## Method

1. Parsed `/v3/datasources` and `/v3/datasources/{id}` from `reference/v3-investigation/graph_v3_openapi.json` — extracted all query parameters, sortBy description, and `ApiDataSourceResponse` schema.
2. Read current code: `src/aireloom/endpoints.py` (lines 19, 143–177, 344–347), `src/aireloom/resources/data_sources_client.py`, `src/aireloom/models/data_source.py`.
3. Ran **12 live API calls** against `https://api.openaire.eu/graph/v3/datasources` via `v3_live.py` — verified every new filter param, base path, sortBy (valid + invalid), and full response shape.

---

## Findings

### 1. Path Change: `dataSources` → `datasources`

| Item | Current Code | V3 Spec | Live Verified | Notes |
|---|---|---|---|---|
| Endpoint path constant | `DATA_SOURCES = "dataSources"` (endpoints.py:19) | `/v3/datasources` | **200** at `/v3/datasources?search=openaire&pageSize=1` | Must change to `"datasources"` |
| Resource client usage | `_entity_path: str = DATA_SOURCES` (data_sources_client.py:19) | — | — | Inherits constant; no other change needed |

**Live proof:**
```
STATUS: 200
URL: https://api.openaire.eu/graph/v3/datasources?search=openaire&pageSize=1
HEADER: {"numFound": 25, "maxScore": 9.555495, ...}
```

### 2. Filter Parameters — Full Matrix (26 total)

| # | Param | In Current `DataSourcesFilters`? | V3 Spec Type | Live Status | Notes |
|---|---|---|---|---|---|
| 1 | `search` | ✅ Yes (line 163) | string | ✅ 200 | Unchanged |
| 2 | `officialName` | ✅ Yes (line 164) | string | ✅ 200 | Unchanged |
| 3 | `englishName` | ✅ Yes (line 165) | string | ✅ 200 | Unchanged |
| 4 | `legalShortName` | ✅ Yes (line 166) | string | ✅ 200 | **BUG**: spec description says "organization" not "datasource" (see §4) |
| 5 | `id` | ✅ Yes (line 167) | string | ✅ 200 | Unchanged |
| 6 | `pid` | ✅ Yes (line 168) | string | ✅ 200 | Unchanged |
| 7 | `subjects` | ✅ Yes (line 169) | string (comma-separated) | ✅ 200 | Current model uses `list[str]`; spec says `string`. Serialization must join with `,` |
| 8 | `dataSourceTypeName` | ✅ Yes (line 170) | string | ✅ 200 | Unchanged |
| 9 | `contentTypes` | ✅ Yes (line 171) | string (comma-separated) | ✅ 200 | Same list→string serialization concern as subjects |
| 10 | `relOrganizationId` | ✅ Yes (line 172) | string | ✅ 200 | Unchanged |
| 11 | `relCommunityId` | ✅ Yes (line 173) | string | ✅ 200 | Unchanged |
| 12 | `relCollectedFromDatasourceId` | ✅ Yes (line 174) | string | ✅ 200 | Unchanged |
| 13 | `logicalOperator` | ✅ Yes (line 175) | enum: AND, OR, **NOT** | ⚠️ Spec adds NOT | Current code only allows `Literal["AND", "OR"]`. V3 spec includes `"NOT"` as valid value |
| **—** | **8 NEW params below** | **❌ Missing** | — | — | — |
| 14 | `collectedFromName` | ❌ Missing | string | ✅ 200, numFound=0 for test value | **NEW** |
| 15 | `country` | ❌ Missing | string | ✅ 200, numFound=966 for `IT` | **NEW** |
| 16 | `thematic` | ❌ Missing | **boolean** | ✅ 200, numFound=1549 for `true` | **NEW** — boolean type, not string |
| 17 | `jurisdiction` | ❌ Missing | string | ✅ 200 (0 results for `European Union`) | **NEW** — returns `CodeLabel{code, label}` in response |
| 18 | `eoscdatasourcetype` | ❌ Missing | string | ✅ 200, numFound=11686 for `Repository` | **NEW** — all-lowercase param name |
| 19 | `odLanguages` | ❌ Missing | string | ✅ 200, numFound=345 for `en` | **NEW** — note: response field is `odlanguages` (lowercase) |
| 20 | `compatibilityId` | ❌ Missing | string | ✅ 200, numFound=110 for `openaire2.0` | **NEW** — response field: `openaireCompatibilityId` |
| 21 | `compatibilityName` | ❌ Missing | string | ✅ 200, numFound=110 | **NEW** — requires URL-encoding of spaces/parens |

#### Pagination Params (unchanged, inherited from framework)

| Param | Spec | Live Verified |
|---|---|---|
| `page` | integer ≥1, default 1 | ✅ Standard 1-indexed |
| `pageSize` | integer 1–100, default 10 | ✅ Enforced |
| `cursor` | string, init=`*` | ✅ Cursor pagination works |

### 3. The "Organizations" Copy-Paste Bug — Three Manifestations

This is a **server-side bug in OpenAIRE's V3 implementation**. All three confirmed:

| # | Location | Evidence |
|---|---|---|
| 1 | **sortBy parameter description in OpenAPI spec** | `"organizations can be only sorted by the 'relevance'"` — should say "data sources" |
| 2 | **Live API 400 error message for invalid sortBy** | `The field should be in the format 'fieldname ASC\|DESC', organizations can be only sorted by the 'relevance'.` |
| 3 | **legalShortName parameter description in OpenAPI spec** | `"The legal name of the organization in short form."` — should say "data source" |

**Live verification of manifestation #2:**
```
REQUEST: GET /v3/datasources?sortBy=invalid+DESC&pageSize=1
STATUS:  400
ERROR:   The field should be in the format 'fieldname ASC|DESC', organizations can be only sorted by the 'relevance'.
```

**Impact on AIREloom**: Cosmetic only — our code does not parse error messages from the API. But document for awareness. The actual sort behavior is correct (relevance-only).

### 4. Sort Fields

| Sort Field | In ENDPOINT_DEFINITIONS? | Live Verified | Notes |
|---|---|---|---|
| `relevance` | ✅ Yes (endpoints.py:346) | ✅ 200 with `sortBy=relevance+DESC` | **Only valid sort field** |

Sort is relevance-only. Confirmed both in spec ("organizations can be only sorted by the 'relevance'") and live. No changes needed to sort config.

### 5. Response Model — Field Gap Analysis

Comparison of current `DataSource` model vs live V3 response:

| Field | Current Model (data_source.py) | V3 Live Response | V3 Spec Schema | Gap? |
|---|---|---|---|---|
| `id` | inherited from BaseEntity | `string` ✅ | `string` | — |
| `originalIds` | `SafeList[str]` (line 59) | `array[string]` ✅ | `array[string]` | — |
| `pids` | `SafeList[ControlledField]` (line 60) | `null` / `array[DatasourcePid]` ✅ | `array[DatasourcePid]` | — |
| `type` | `SafeControlledField` (line 61) | `{scheme, value} object` ✅ | `DatasourceSchemeValue` | — |
| `openaireCompatibility` | `str \| None` (line 62) | `"OpenAIRE 2.0 (EC funding)"` ✅ | `string` | — |
| `officialName` | `SafeStr` (line 63) | `"OpenAIRE"` ✅ | `string` | — |
| `englishName` | `SafeStr` (line 64) | `"OpenAIRE"` ✅ | `string` | — |
| `websiteUrl` | `str \| None` (line 65) | URL string ✅ | `string` | — |
| `logoUrl` | `str \| None` (line 66) | URL string ✅ | `string` | — |
| `dateOfValidation` | `str \| None` (line 67) | `null` ✅ | `string` | — |
| `description` | `SafeStr` (line 68) | `null` ✅ | `string` | — |
| `subjects` | `SafeList[str]` (line 69) | `["{NULL}"]` ✅ | `array[string]` | — |
| `languages` | `SafeList[str]` (line 70) | `null` ✅ | `array[string]` | — |
| `contentTypes` | `SafeList[str]` (line 71) | `null` ✅ | `array[string]` | — |
| `releaseStartDate` | `str \| None` (line 72) | `null` ✅ | `string` | — |
| `releaseEndDate` | `str \| None` (line 73) | `null` ✅ | `string` | — |
| `missionStatementUrl` | `str \| None` (line 83) | `null` ✅ | `string` | — |
| `accessRights` | `AccessRightType` (Literal, line 74) | `null` | `string` | ⚠️ Spec says plain `string`, model restricts to 3 literals |
| `uploadRights` | `AccessRightType` (Literal, line 75) | `null` | `string` | ⚠️ Same literal restriction |
| `databaseAccessRestriction` | `DatabaseRestrictionType` (Literal, line 76) | `null` | `string` | ⚠️ Same literal restriction |
| `dataUploadRestriction` | `str \| None` (line 77) | `null` ✅ | `string` | — |
| `versioning` | `bool \| None` (line 78) | `false` ✅ | `boolean` | — |
| `citationGuidelineUrl` | `str \| None` (line 79) | `null` ✅ | `string` | — |
| `pidSystems` | `str \| None` (line 80) | `null` ✅ | `string` | — |
| `certificates` | `str \| None` (line 81) | `null` ✅ | `string` | — |
| `policies` | `SafeList[str]` (line 82) | `null` ✅ | `array[string]` | — |
| `journal` | `SafeContainer` (line 84) | `null` ✅ | `Container` ref | — |
| **`collectedFrom`** | **❌ MISSING** | `null` / `array[CfHbKeyValue]` | `array[CfHbKeyValue]` | **🔴 NEW — add** |
| **`thematic`** | **❌ MISSING** | `false` (boolean) | `boolean` | **🔴 NEW — add** |
| **`eoscdatasourcetype`** | **❌ MISSING** | `{code:"Aggregator", label:"Aggregator"}` | `CodeLabel` | **🔴 NEW — add as CodeLabel object** |
| **`links`** | **❌ MISSING** | `null` / `array[RelatedRecord]` | `array[RelatedRecord]` | **🔴 NEW — add** |
| **`jurisdiction`** | **❌ MISSING** | `{code:"Global", label:"Global"}` | `CodeLabel` | **🔴 NEW — add as CodeLabel object** |
| **`odlanguages`** | **❌ MISSING** | `null` / `array[string]` | `array[string]` | **🔴 NEW — add** (note lowercase vs filter param `odLanguages`) |
| **`openaireCompatibilityId`** | **❌ MISSING** | `"openaire2.0"` | `string` | **🔴 NEW — add** |

**Summary: 7 new response fields missing from model.** Plus 3 fields where model uses overly restrictive Literals vs spec's plain `string`.

#### Key Response Field Notes

- **`openaireCompatibility`** stays as a flat string (e.g., `"OpenAIRE 2.0 (EC funding)"`). The **new** `openaireCompatibilityId` field provides the machine-readable ID (e.g., `"openaire2.0"`). These are separate fields.
- **`eoscdatasourcetype`** and **`jurisdiction`** are `CodeLabel` objects `{code: str, label: str}`, not plain strings.
- **`odlanguages`** in the response is all-lowercase; the filter param is `odLanguages` (camelCase). Case mismatch is server-side.
- **`collectedFrom`** is an array of `{key: str, data?: {...}}` objects (CfHbKeyValue schema).

### 6. Resource Client Routing

`DataSourcesClient` (data_sources_client.py:9–25) inherits from `StandardResourceClient`. It uses:
- `_entity_path = DATA_SOURCES` — **only change needed**: the constant value (endpoints.py:19)
- `_entity_model = DataSource` — will pick up model additions automatically
- `_search_response_model = DataSourceResponse` — same
- `_batch_fields` — unchanged

No base URL override needed (uses default graph/v3).

---

## Live Verification Log

All commands run from repo root via `python3 reference/v3-investigation/v3_live.py`:

| # | Command | Status | Key Observation |
|---|---|---|---|
| 1 | `graph datasources "search=openaire&pageSize=1" --full` | **200** | Base path `/v3/datasources` confirmed; full response captured (see §5) |
| 2 | `graph datasources "country=IT&pageSize=2"` | **200**, numFound=966 | `country` filter works |
| 3 | `graph datasources "thematic=true&pageSize=2"` | **200**, numFound=1549 | `thematic=true` boolean filter works |
| 4 | `graph datasources "eoscdatasourcetype=Repository&pageSize=2"` | **200**, numFound=11686 | `eoscdatasourcetype` filter works |
| 5 | `graph datasources "jurisdiction=European+Union&pageSize=2"` | **200**, numFound=0 | `jurisdiction` filter accepted (0 results for this value) |
| 6 | `graph datasources "collectedFromName=openaire&pageSize=2"` | **200**, numFound=0 | `collectedFromName` filter accepted |
| 7 | `graph datasources "compatibilityId=openaire2.0&pageSize=2"` | **200**, numFound=110 | `compatibilityId` filter works |
| 8 | `graph datasources 'compatibilityName="OpenAIRE 2.0 (EC+funding)"&pageSize=2'` | **200**, numFound=110 | `compatibilityName` with quoted value works |
| 9 | `graph datasources "odLanguages=en&pageSize=2"` | **200**, numFound=345 | `odLanguages` filter works |
| 10 | `graph datasources "sortBy=relevance+DESC&pageSize=2"` | **200** | Relevance sort works |
| 11 | `graph datasources "sortBy=invalid+DESC&pageSize=1"` | **400** | Error msg confirms "organizations" copy-paste bug |
| 12 | (implicit) `graph datasources/{id}` via spec | — | Schema extracted from OpenAPI |

**Full response sample (from call #1, --full):**
```json
{
  "id": "infrastruct_::f66f1bd369679b5b077dcdf006089556",
  "originalIds": ["infrastruct_::openaire", "piwik:109", "piwik:5"],
  "pids": null,
  "type": {"scheme": "scholarcomminfra", "value": "Scholarly Comm. Infrastructure"},
  "openaireCompatibility": "OpenAIRE 2.0 (EC funding)",
  "officialName": "OpenAIRE",
  "englishName": "OpenAIRE",
  "websiteUrl": "http://www.openaire.eu/",
  "logoUrl": "http://www.openaire.eu/images/openaire/logos/logo_openaire.png",
  "dateOfValidation": null,
  "description": null,
  "subjects": ["{NULL}"],
  "languages": null,
  "contentTypes": null,
  "releaseStartDate": null,
  "releaseEndDate": null,
  "missionStatementUrl": null,
  "accessRights": null,
  "uploadRights": null,
  "databaseAccessRestriction": null,
  "dataUploadRestriction": null,
  "versioning": false,
  "citationGuidelineUrl": null,
  "pidSystems": null,
  "certificates": null,
  "policies": null,
  "journal": null,
  "collectedFrom": null,
  "thematic": false,
  "eoscdatasourcetype": {"code": "Aggregator", "label": "Aggregator"},
  "links": null,
  "jurisdiction": {"code": "Global", "label": "Global"},
  "odlanguages": null,
  "openaireCompatibilityId": "openaire2.0"
}
```

---

## Recommendations

### R1. Change endpoint path constant (MUST)
**File:** `src/aireloom/endpoints.py:19`
```python
# BEFORE:
DATA_SOURCES = "dataSources"
# AFTER:
DATA_SOURCES = "datasources"
```
Single-line change. This propagates to `ENDPOINT_DEFINITIONS` key (line 344) and `DataSourcesClient._entity_path` (data_sources_client.py:19) automatically since they reference the constant.

### R2. Add 8 new filter fields to `DataSourcesFilters` (MUST)
**File:** `src/aireloom/endpoints.py:143-177`

Add after `relCollectedFromDatasourceId` (line 174):
```python
collectedFromName: str | None = None
country: str | None = None
thematic: bool | None = None           # NOTE: boolean type, not string
jurisdiction: str | None = None
eoscdatasourcetype: str | None = None   # NOTE: all-lowercase
odLanguages: str | None = None          # NOTE: camelCase in filter, odlanguages in response
compatibilityId: str | None = None
compatibilityName: str | None = None
```

### R3. Extend `logicalOperator` enum to include "NOT" (SHOULD)
**File:** `src/aireloom/endpoints.py:175`
```python
# BEFORE:
logicalOperator: Literal["AND", "OR"] | None = None
# AFTER:
logicalOperator: Literal["AND", "OR", "NOT"] | None = None
```
V3 spec lists NOT as a valid value. Note: NOT is a field-level operator here (not a replacement for logicalOperator in all endpoints — verify consistency across other endpoints' migration).

### R4. Add 7 new response fields to `DataSource` model (MUST)
**File:** `src/aireloom/models/data_source.py`

New fields to add (after `journal` at line 84):
```python
collectedFrom: SafeList[dict] | None = None       # CfHbKeyValue objects
thematic: bool | None = None                       # boolean
eoscdatasourcetype: dict | None = None             # CodeLabel {code, label}
links: SafeList[dict] | None = None                # RelatedRecord objects
jurisdiction: dict | None = None                   # CodeLabel {code, label}
odlanguages: SafeList[str] | None = None           # array of strings (lowercase!)
openaireCompatibilityId: str | None = None         # machine-readable compat ID
```

Consider creating proper `CodeLabel` and `CfHbKeyValue` Pydantic models instead of raw `dict` for typed access to `eoscdatasourcetype`, `jurisdiction`, and `collectedFrom`.

### R5. Relax Literal types on 3 fields to plain `str | None` (SHOULD)
**File:** `src/aireloom/models/data_source.py:74-76`

V3 spec defines these as plain `string`, not enums:
- `accessRights`: currently `AccessRightType` (Literal["open","restricted","closed"]) → change to `str | None`
- `uploadRights`: same → `str | None`
- `databaseAccessRestriction`: currently `DatabaseRestrictionType` (Literal["feeRequired","registration","other"]) → `str | None`

The existing Literal types may be from V1 documentation that was more restrictive. If these literals represent the *known* controlled vocabulary, consider keeping them but allowing additional values via a union or removing the strict Literal constraint.

### R6. Verify list→string serialization for `subjects` and `contentTypes` (CHECK)
**File:** `src/aireloom/endpoints.py:169,171`

Current model types these as `list[str] | None`, but V3 spec says `string` (comma-separated). The framework serializer must flatten lists to comma-separated strings. Verify this works correctly or change to `str | None` and handle splitting/joining at the boundary.

### R7. No changes needed for resource client or sort config
`data_sources_client.py` needs no edits beyond the constant propagation from R1. Sort config at `endpoints.py:346` is already correct (`{"relevance": {}}`).

---

## Open Questions / Risks

1. **`subjects`/`contentTypes` serialization**: The V3 spec types these as `string` (not array), implying comma-separated values. The current Pydantic model uses `list[str]`. How does the framework serialize list fields to query params? If it sends `subjects=a&subjects=b` (repeated key) instead of `subjects=a,b`, the V3 API may not interpret it correctly. **Must test.**

2. **`thematic` boolean serialization**: Some HTTP clients serialize `bool` as `true/false` (JSON-style) and others as `1/0` or `True/False`. The live test used `thematic=true` and got 200. Confirm the framework's bool serialization matches what V3 expects.

3. **`CodeLabel` type reuse**: Both `eoscdatasourcetype` and `jurisdiction` return `{code, label}` objects. Other endpoints (research-products, organizations) likely also return CodeLabel patterns. Should there be a shared `CodeLabel` model in `models/base.py` or `models/shared.py`? Coordinate with Research-ResearchProducts and Research-Organizations agents.

4. **`odLanguages` → `odlanguages` case mismatch**: Filter param is camelCase `odLanguages`, response field is lowercase `odlanguages`. This is a server-side inconsistency. Our model should use the response-side name (`odlanguages`) for deserialization, while the filter uses `odLanguages`.

5. **`compatibilityName` with special characters**: Requires URL-encoding of spaces, parentheses, quotes. Test value `%22OpenAIRE+2.0+(EC+funding)%22` worked. Ensure framework's filter serializer properly URL-encodes string values containing spaces and special chars.

6. **"organizations" bug longevity**: This copy-paste bug exists in both the OpenAPI spec and the live error messaging. It has persisted through multiple V3 releases. It does not affect functionality but indicates low QA attention to the datasources endpoint docs. Do not expect a fix soon.
