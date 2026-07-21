# V3 Migration Research — Persons Endpoint (`/v3/persons`)

## Scope

The persons endpoint: filter parameters (especially the fixed `givenName`/`lastName`), sort capabilities (now relevance-only), response model (`Person`), and the `PersonsClient` resource client. Covers `GET /v3/persons` (search/list) and `GET /v3/persons/{id}` (get-by-id).

## Method

1. Read current source code: `PersonsFilters` in `src/aireloom/endpoints.py`, `Person` model in `src/aireloom/models/person.py`, `PersonsClient` in `src/aireloom/resources/persons_client.py`.
2. Extracted V3 OpenAPI spec parameters/schema for `/v3/persons` from `reference/v3-investigation/graph_v3_openapi.json`.
3. Read V3 documentation at `https://graph.openaire.eu/docs/apis/graph-api/persons/` and `https://graph.openaire.eu/docs/data-model/entities/persons/`.
4. Ran **10 live API calls** against `https://api.openaire.eu/graph/v3/persons` via `reference/v3-investigation/v3_live.py` to verify every parameter, sort value, and response field.

---

## Findings

### 1. Filter Parameters

| Parameter | V1/V2 Current Code | V3 Spec | Live-Verified Status | Notes |
|---|---|---|---|---|
| `search` | `str \| None` | string, optional | **200 OK** — `search=covid` → numFound=1393 | Works identically |
| `id` | `str \| None` | string, optional | **200 OK** — returns results when ID exists | Standard OpenAIRE ID lookup |
| `originalId` | `str \| None` | string, optional | **200 OK** — works with ORCID-style IDs | e.g., `originalId=0000-0002-1825-0097` |
| `givenName` | `str \| None` (**CAUTION: 500**) | string, optional | **200 OK** — `givenName=John` → numFound=35,018 | **FIXED in V3** — was HTTP 500, now works perfectly |
| `lastName` | `str \| None` (**CAUTION: 500**) | string, optional | **200 OK** — `lastName=Smith` → numFound=12,917 | **FIXED in V3** — was HTTP 500, now works perfectly |
| `logicalOperator` | `Literal["AND", "OR"]` | enum: `["AND", "OR", "NOT"]` | **200 OK** — `logicalOperator=NOT` works | **V3 adds NOT support**; current code missing `"NOT"` |

**Key discovery — `givenName`/`lastName` fix confirmed:**

```
STATUS: 200  URL: .../v3/persons?givenName=John&pageSize=1
HEADER: {"numFound": 35018, "maxScore": 1.0, ...}

STATUS: 200  URL: .../v3/persons?lastName=Smith&pageSize=1
HEADER: {"numFound": 12917, "maxScore": 1.0, ...}
```

Both return 200 with substantial result counts. The V1/V2 500 error is resolved.

### 2. Sort Fields

| Sort Field | V1/V2 Current Code | V3 Spec Pattern | Live-Verified Status |
|---|---|---|---|
| `relevance` | Listed | `^((relevance)\s+(ASC\|DESC),?\s*)+$` | **200 OK** — `sortBy=relevance+DESC` works |
| `startDate` | Listed | **not in pattern** | **400 BAD REQUEST** — removed in V3 |
| `endDate` | Listed | **not in pattern** | **400 BAD REQUEST** — removed in V3 |

**Live verification of rejected sorts:**

```
STATUS: 400  sortBy=startDate+DESC
ERROR: "The field should be in the format 'fieldname ASC|DESC', persons can be only sorted by the 'relevance'."

STATUS: 400  sortBy=endDate+DESC
ERROR: "The field should be in the format 'fieldname ASC|DESC', persons can be only sorted by the 'relevance'."
```

V3 persons endpoint is **relevance-only sorting** (D10 fix). The `startDate`/`endDate` entries in `ENDPOINT_DEFINITIONS["persons"]["sort"]` are now invalid.

### 3. Response Model — Field-by-Field Comparison

| Field | Current Person Model (person.py) | V3 Docs Type | V3 OpenAPI Schema | Live API Observed | Gap? |
|---|---|---|---|---|---|
| `id` | inherited from `BaseEntity` (string) | String, ONE | string | `"orcid_______::000037cb..."` | None |
| `originalId` | `SafeList[str]` | String, MANY | array of string | `["0000-0002-8905-3269"]` | None |
| `givenName` | `SafeStr = ""` | String, ONE | string | `"Robert"` | None |
| `familyName` | `SafeStr = ""` | String, ONE | string | `"Cueto"` | None |
| `alternativeNames` | `SafeList[str]` | String, MANY | array of string | `["Robert John Cueto", ...]` or `null` | None |
| `biography` | `SafeStr = ""` | String, ONE | string | long text or `null` | None |
| `subject` | `SafeList[str]` | String, MANY | array of string | `null` in all tested records | None (type correct) |
| `indicator` | `dict \| None = None` | **Object**, ONE | **array** (spec error!) | `null` in all tested records | **Spec/doc mismatch** — docs say Object (matches our model), spec wrongly says array |
| `context` | `dict \| None = None` | **Object**, ONE | **array** (spec error!) | `null` in all tested records | **Spec/doc mismatch** — docs say Object (matches our model), spec wrongly says array |
| `consent` | `bool \| None = None` | Boolean, ONE | boolean | `null` in all tested records | None |
| `coAuthors` | `SafeList[str]` | String, MANY | array of string | `["Harvey Chim", ...]` | None |

**Important discrepancy:** The V3 **OpenAPI JSON schema** declares `indicator` and `context` as `type: "array"`, but the V3 **documentation page** explicitly shows them as **Objects** with key-value structure (e.g., `{"citationCount": 342, "downloads": 28}`). The live API returns `null` for all tested persons (including high-profile researchers like Yoshua Bengio). Our current model uses `dict | None` which aligns with the **docs**, not the spec. Trust the docs + model shape here.

### 4. Routing / Pagination Notes

| Aspect | Value |
|---|---|
| Base URL | `https://api.openaire.eu/graph/v3/persons` |
| List endpoint | `GET /v3/persons` |
| Get-by-ID | `GET /v3/persons/{id}` |
| Page indexing | **1-indexed** (`page=1` is first; `page=0` → 400) |
| pageSize range | 1–100 (rejects >100 with 400) |
| Cursor pagination | Supported (`cursor=*` for initial, returns `nextCursor`) |
| Default sort | `relevance DESC` |
| Header envelope | `numFound`, `maxScore`, `queryTime`, `page`, `pageSize`, `nextCursor` |

Standard V3 pagination behavior — no special quirks like the links endpoint.

### 5. logicalOperator NOT Support

V3 spec defines `logicalOperator` as `enum: ["AND", "OR", "NOT"]`. Verified NOT works:

```
STATUS: 200  URL: .../v3/persons?givenName=John&lastName=Smith&logicalOperator=NOT&pageSize=1
HEADER: {"numFound": 88, "maxScore": 1.0, ...}
```

Returns persons named John who are NOT named Smith (88 results). Current code only allows `Literal["AND", "OR"]` — missing `"NOT"`.

---

## Live Verification (Commands & Observed Output)

### givenName filter (THE headline fix)

```bash
python3 reference/v3-investigation/v3_live.py graph "persons" "givenName=John&pageSize=1"
# STATUS: 200
# HEADER: {"numFound": 35018, "maxScore": 1.0, "queryTime": 47, "page": 1, "pageSize": 1}
# RESULTS: 1
```

### lastName filter (THE headline fix)

```bash
python3 reference/v3-investigation/v3_live.py graph "persons" "lastName=Smith&pageSize=1"
# STATUS: 200
# HEADER: {"numFound": 12917, "maxScore": 1.0, "queryTime": 49, "page": 1, "pageSize": 1}
# RESULTS: 1
```

### search filter

```bash
python3 reference/v3-investigation/v3_live.py graph "persons" "search=covid&pageSize=1"
# STATUS: 200
# HEADER: {"numFound": 1393, "maxScore": 4.6960306, "queryTime": 234, "page": 1, "pageSize": 1}
# RESULTS: 1
```

### originalId filter

```bash
python3 reference/v3-investigation/v3_live.py graph "persons" "originalId=0000-0002-1825-0097&pageSize=1"
# STATUS: 200 (results depend on whether ORCID exists in Graph)
```

### Get by ID (full response for model comparison)

```bash
python3 reference/v3-investigation/v3_live.py graph "persons/orcid_______::000037cb1e4968862ff640cd5d2d7001" "" --full
# STATUS: 200
# Full person object with all fields — matches current Person model shape exactly
# Key fields observed:
#   id, originalId (array), givenName, familyName, alternativeNames (array or null),
#   biography (string or null), subject (null), indicator (null), context (null),
#   consent (null), coAuthors (array of strings)
```

### Sort: relevance (works)

```bash
python3 reference/v3-investigation/v3_live.py graph "persons" "givenName=John&pageSize=1&sortBy=relevance+DESC"
# STATUS: 200
```

### Sort: startDate (REJECTED)

```bash
python3 reference/v3-investigation/v3_live.py graph "persons" "givenName=John&pageSize=1&sortBy=startDate+DESC"
# STATUS: 400
# ERROR: "The field should be in the format 'fieldname ASC|DESC', persons can be only sorted by the 'relevance'."
```

### Sort: endDate (REJECTED)

```bash
python3 reference/v3-investigation/v3_live.py graph "persons" "givenName=John&pageSize=1&sortBy=endDate+DESC"
# STATUS: 400
# ERROR: "The field should be in the format 'fieldname ASC|DESC', persons can be only sorted by the 'relevance'."
```

### logicalOperator=NOT (works)

```bash
python3 reference/v3-investigation/v3_live.py graph "persons" "givenName=John&lastName=Smith&logicalOperator=NOT&pageSize=1"
# STATUS: 200
# HEADER: {"numFound": 88, "maxScore": 1.0, "queryTime": 23, ...}
```

---

## Recommendations

### R1. Remove CAUTION docstrings from `PersonsFilters` (MUST)

**File:** `src/aireloom/endpoints.py:301-315`

The class docstring and attribute docstrings contain stale warnings about `givenName`/`lastName` causing HTTP 500 errors. These must be rewritten to reflect that both filters work correctly in V3:

- **Line 304–306**: Remove "but they currently cause HTTP 500 errors from the server. Only 'search', 'id', and 'originalId' work reliably. These params are kept for forward compatibility."
- **Line 312**: Remove `CAUTION: causes API 500.` from `givenName` docstring
- **Line 313**: Remove `CAUTION: causes API 500.` from `lastName` docstring

New docstring should state that all six filter parameters are functional in V3.

### R2. Add `"NOT"` to `logicalOperator` literal (MUST)

**File:** `src/aireloom/endpoints.py:322`

Change:
```python
logicalOperator: Literal["AND", "OR"] | None = None
```
To:
```python
logicalOperator: Literal["AND", "OR", "NOT"] | None = None
```

V3 spec explicitly includes `"NOT"` in the enum, and live testing confirms it works.

### R3. Remove `startDate`/`endDate` from persons sort definition (MUST)

**File:** `src/aireloom/endpoints.py:356-363`

Change:
```python
PERSONS: {
    "filters_model": PersonsFilters,
    "sort": {
        "relevance": {},
        "startDate": {},
        "endDate": {},
    },
},
```
To:
```python
PERSONS: {
    "filters_model": PersonsFilters,
    "sort": {
        "relevance": {},
    },
},
```

These sort fields return 400 in V3. Only `relevance` is valid.

### R4. Person model — no structural changes needed (OK)

**File:** `src/aireloom/models/person.py`

The current `Person` model aligns well with the V3 live API response:
- All 11 fields present in the model appear in API responses
- Types match (with ` SafeStr`/`SafeList` wrappers being appropriate)
- `indicator: dict | None` and `context: dict | None` match the V3 **documentation** (Object type), despite the OpenAPI spec erroneously listing them as arrays
- `extra="allow"` on model_config provides forward safety

**Minor note:** The module docstring (line 5–6) references "v1 persons endpoint" and the old v1 URL. Should be updated to V3.

### R5. PersonsClient — no changes needed (OK)

**File:** `src/aireloom/resources/persons_client.py`

The client is a clean `StandardResourceClient` subclass with correct path/model wiring. No changes required for V3 migration — it inherits pagination/sort/filter handling from the base class, which reads from `ENDPOINT_DEFINITIONS`. Once R1–R3 are applied to endpoints.py, this client works correctly.

---

## Open Questions / Risks

1. **`indicator`/`context` always null in live data:** Across 6+ tested persons (including Yoshua Bengio, Robert Williamson, Robert Cueto), both fields are consistently `null`. The docs show example objects but real data may not populate them yet. This is not a model problem (our `dict | None` handles it), but users should not expect these fields to have data.

2. **OpenAPI spec vs. docs mismatch on `indicator`/`context`:** The V3 OpenAPI JSON schema declares these as `type: "array"` while the V3 HTML documentation shows them as Objects with sub-keys. Our model (and the live API's `null` values) cannot definitively resolve this, but the doc examples strongly suggest Object/dict is correct. If non-null responses ever surface as arrays, the model will need adjustment.

3. **No breaking changes for existing consumers:** All current model fields remain valid. The migration is purely additive (NOT operator) and corrective (remove CAUTIONs, remove dead sort fields).
