# V3 Migration Research — Organizations Endpoint (`/v3/organizations`)

## Scope

The organizations endpoint: filter parameters, sort fields, response model (Organization entity), resource client routing, and pagination behavior. Compared current AIREloom code against V3 OpenAPI spec, V3 documentation, and live V3 API at `https://api.openaire.eu/graph/v3/organizations`.

## Method

1. Parsed V3 OpenAPI spec (`reference/v3-investigation/graph_v3_openapi.json`) for `/v3/organizations` and `/v3/organizations/{id}` endpoints.
2. Read V3 documentation pages for organizations filtering, sorting, and general endpoint info.
3. Ran 12+ live API queries via `v3_live.py` covering every filter parameter, sort values, invalid inputs, get-by-id, and inline logical operators.
4. Compared all findings to current source code: `OrganizationsFilters` (endpoints.py:115–140), `Organization` model (models/organization.py:53–105), `OrganizationsClient` (resources/organizations_client.py:9–25), and `ENDPOINT_DEFINITIONS[ORGANIZATIONS]` (endpoints.py:340–343).

---

## Findings

### 1. Filter Parameters

| Param | V1/V2 Current Code | V3 Spec Enum | Live Status | Notes |
|---|---|---|---|---|
| `search` | `str \| None` | string (no enum) | **200 OK** | Works identically |
| `legalName` | `str \| None` | string (no enum) | **200 OK** | Works identically |
| `legalShortName` | `str \| None` | string (no enum) | **200 OK** | Works identically |
| `id` | `str \| None` | string (no enum) | **200 OK** | Works identically |
| `pid` | `str \| None` | string (no enum) | **200 OK** | Works identically |
| `countryCode` | `str \| None` | string (no enum) | **200 OK** | Works identically |
| `relCommunityId` | `str \| None` | string (no enum) | **200 OK** | Works identically |
| `relCollectedFromDatasourceId` | `str \| None` | string (no enum) | **200 OK** | Works identically |
| `logicalOperator` | `Literal["AND", "OR"]` | **`["AND", "OR", "NOT"]`** | **See note below** | **GAP: "NOT" missing from Literal** |

**Verdict:** Filter parameter set is otherwise identical between V1 and V3. No new filter params added in V3. The sole difference is `logicalOperator` gaining `"NOT"` as an accepted value.

#### logicalOperator NOT behavior

| Test | Status | numFound | Observation |
|---|---|---|---|
| `countryCode=US&logicalOperator=NOT` | 200 | 61,082 | Same count as `countryCode=US` alone — NOT appears silently ignored or no-op when used as top-level operator |
| `countryCode=("US" AND NOT "GB")` (inline) | 200 | 61,082 | Inline NOT within filter value works per docs |

**Doc/spec discrepancy:** The V3 docs main page state `logicalOperator` accepts `AND` or `OR` only. The V3 OpenAPI spec lists `enum=["AND", "OR", "NOT"]`. The filtering sub-page documents `NOT` as an **inline** operator *within* filter values (e.g., `search="institute" NOT "medical"`), not as a top-level `logicalOperator` value. The live API accepts `logicalOperator=NOT` without error but produces identical results to omitting it entirely — suggesting it may be accepted but treated as a no-op at the top level.

**Recommendation:** Add `"NOT"` to the `LogicalOperator` literal for forward compatibility, since the spec allows it and it costs nothing. Document that NOT is primarily useful as an inline operator within filter values.

### 2. Sort Fields

| Sort Field | Current Code | V3 Spec | V3 Docs | Live Verified |
|---|---|---|---|---|
| `relevance` | `{"relevance": {}}` | Only valid field | Only valid field; default `relevance DESC` | **200 OK** (ASC and DESC both work) |

**Invalid sort test:**
```
GET /v3/organizations?sortBy=invalidField+DESC&pageSize=2
→ STATUS 400
→ ERROR: "The field should be in the format 'fieldname ASC|DESC', organizations can be only sorted by the 'relevance'."
```

**Verdict:** Sort is relevance-only, correctly modeled. No change needed.

### 3. Response Model — Field Comparison

V3 live response (from `search=Harvard University` with `--full`):

```json
{
  "legalShortName": "IQSS",
  "legalName": "Harvard University, Institute of Quantitative Social Science",
  "websiteUrl": "https://www.iq.harvard.edu",
  "alternativeNames": ["IQSS"],
  "country": {"code": "US", "label": "United States"},
  "id": "pending_org_::18aa4d8d7ea282fe0246903a8c2d3aa2",
  "pids": null,
  "originalIds": ["pending_org_::abde8d72214cd15facc2fb7cab6e50b9"],
  "fundings": [],
  "collectedFrom": [{"key": "openaire____::0362fcdb3076765d9c0041ad331553e8", "value": "OpenOrgs Database"}]
}
```

| V3 Live Field | Current Model Field | Type | Gap? |
|---|---|---|---|
| `id` | `id` (inherited from BaseEntity) | `str` | OK |
| `legalName` | `legalName` | `SafeStr` | OK |
| `legalShortName` | `legalShortName` | `SafeStr` | OK |
| `websiteUrl` | `websiteUrl` | `str \| None` | OK |
| `alternativeNames` | `alternativeNames` | `SafeList[str]` | OK |
| `country` | `country` (with `.code`, `.label`) | `SafeCountry` → `Country` | OK |
| `pids` | `pids` (with `.scheme`, `.value`) | `SafeList[OrganizationPid]` | OK |
| **`originalIds`** | **ABSENT** | `list[str]` | **GAP** |
| **`fundings`** | **ABSENT** | `list[Funding]` (nested: funder, level0, level1, level2) | **GAP** |
| **`collectedFrom`** | **ABSENT** | `list[CfHbKeyValue]` (key, value) | **GAP** |

**Three fields are missing from the current `Organization` model.** All three are present in the V3 OpenAPI schema (`ApiOrganizationResponse`). Since the model uses `ConfigDict(extra="allow")`, these fields are silently absorbed into `__pydantic_extra__` and not lost on deserialization — but they are not type-accessible.

#### Missing Field Details

**`originalIds`: `list[str]`**
- Array of original/source IDs for the organization.
- Example value: `["pending_org_::abde8d72214cd15facc2fb7cab6e50b9"]`
- Present even on sparse records (the first pageSize=1 result had this populated).

**`fundings`: `list[Funding]`**
- Complex nested structure. Each Funding object contains:
  - `funder`: `{id, shortname, name, jurisdiction: {code, label}, pid}`
  - `level0`: `{id, description, name}`
  - `level1`: `{id, description, name}`
  - `level2`: `{id, description, name}`
- Empty array `[]` on organizations without funding data.
- This is a significant structural addition — the Funding sub-model does not exist anywhere in the current codebase.

**`collectedFrom`: `list[CfHbKeyValue]`**
- Simple key-value pairs identifying the datasource(s) the organization was collected from.
  - `key`: OpenAIRE datasource ID (e.g., `"openaire____::0362fcdb3076765d9c0041ad331553e8"`)
  - `value`: Human-readable datasource name (e.g., `"OpenOrgs Database"`)

### 4. Pagination & Routing

| Aspect | Current Code | V3 Behavior | Match? |
|---|---|---|---|
| Base path | `ORGANIZATIONS = "organizations"` | `/v3/organizations` | Yes — path unchanged |
| Page indexing | Uses bibliofabric default (1-indexed) | 1-indexed (page=0 → 400) | Yes |
| pageSize range | Not explicitly constrained client-side | 1–100 (>100 → 400) | N/A (server-enforced) |
| Cursor pagination | Supported via bibliofabric mixin | `cursor=*` with `nextCursor` | Yes |
| Base URL override | **None** (uses default) | Should route to `/graph/v3/...` once default base changes | Yes |
| `_batch_fields` | `{"pid": "pid", "openaire_id": "id"}` | Unchanged | Yes |

**Routing verdict:** `OrganizationsClient` has NO `_base_url_override` (cf. `ResearchProductsClient` which overrides to v2). It inherits the default base URL from `AireloomClient`. Once the default base is updated from `/graph/v1` to `/graph/v3`, organizations will route correctly with zero changes to the client file.

---

## Live Verification Log

All commands run from repo root via `python3 reference/v3-investigation/v3_live.py`.

### Basic search + full response
```bash
python3 reference/v3-investigation/v3_live.py graph "organizations" "pageSize=1" --full
```
**STATUS: 200**, numFound=496,636. Response confirmed all 10 fields including `originalIds`, `fundings`, `collectedFrom`.

### Filter-by-filter verification
```bash
# search
python3 reference/v3-investigation/v3_live.py graph "organizations" "search=Harvard&pageSize=2"
# → STATUS 200, numFound=627

# legalName
python3 reference/v3-investigation/v3_live.py graph "organizations" "legalName=Harvard+University&pageSize=2"
# → STATUS 200, numFound=13

# legalShortName
python3 reference/v3-investigation/v3_live.py graph "organizations" "legalShortName=MIT&pageSize=2"
# → STATUS 200, numFound=23,849

# id
python3 reference/v3-investigation/v3_live.py graph "organizations" "id=openaire____::Universities&pageSize=2"
# → STATUS 200, numFound=0 (valid query, no matches)

# pid
python3 reference/v3-investigation/v3_live.py graph "organizations" "pid=10.5555/12345&pageSize=2"
# → STATUS 200, numFound=0 (valid query, no matches)

# countryCode
python3 reference/v3-investigation/v3_live.py graph "organizations" "countryCode=US&pageSize=2"
# → STATUS 200, numFound=61,082

# relCommunityId
python3 reference/v3-investigation/v3_live.py graph "organizations" "relCommunityId=openaire____::ec&pageSize=2"
# → STATUS 200, numFound=0 (valid query)

# relCollectedFromDatasourceId
python3 reference/v3-investigation/v3_live.py graph "organizations" "relCollectedFromDatasourceId=openaire____::6ac933301a3933c8a22ceebea7000326&pageSize=2"
# → STATUS 200, numFound=496,636
```

### Sort verification
```bash
# Valid sort
python3 reference/v3-investigation/v3_live.py graph "organizations" "sortBy=relevance+DESC&pageSize=2"
# → STATUS 200

python3 reference/v3-investigation/v3_live.py graph "organizations" "sortBy=relevance+ASC&pageSize=2"
# → STATUS 200

# Invalid sort
python3 reference/v3-investigation/v3_live.py graph "organizations" "sortBy=invalidField+DESC&pageSize=2"
# → STATUS 400, ERROR: "The field should be in the format 'fieldname ASC|DESC',
#    organizations can be only sorted by the 'relevance'."
```

### logicalOperator NOT
```bash
# Top-level NOT (accepted by API)
python3 reference/v3-investigation/v3_live.py graph "organizations" "countryCode=%22US%22&logicalOperator=NOT&pageSize=2"
# → STATUS 200, numFound=61,082 (same as without NOT — appears no-op)

# Inline NOT within filter value
python3 reference/v3-investigation/v3_live.py graph "organizations" "countryCode=(%22US%22+AND+NOT+%22GB%22)&pageSize=2"
# → STATUS 200, numFound=61,082
```

### Get-by-ID
```bash
python3 reference/v3-investigation/v3_live.py graph "organizations/aka_________::74be16979710d4c4e7c6647856088456" "" --full
# → STATUS 200, full record returned with fundings and collectedFrom populated
```

---

## Recommendations

### R1. Add `"NOT"` to `logicalOperator` Literal (Priority: Low)

**File:** `src/aireloom/endpoints.py:138`

Change:
```python
logicalOperator: Literal["AND", "OR"] | None = None
```
To:
```python
logicalOperator: Literal["AND", "OR", "NOT"] | None = None
```

Rationale: V3 OpenAPI spec lists `NOT` in the enum. The cost of adding it is zero (one string in a Literal). Even if top-level NOT behaves as a no-op today, future API changes may activate it.

### R2. Add missing V3 response fields to Organization model (Priority: Medium)

**File:** `src/aireloom/models/organization.py`

Add three new fields to the `Organization` class:

1. **`originalIds: SafeList[str] = Field(default_factory=list)`** — trivial addition, flat list of strings.

2. **`collectedFrom: SafeList[CfHbKeyValue] = Field(default_factory=list)`** — requires importing or defining `CfHbKeyValue` (a simple `{key: str, value: str}` model). Check if this model already exists elsewhere in the codebase (used by other entities). If not, define it in `organization.py` or extract to a shared location.

3. **`fundings: SafeList[Funding] = Field(default_factory=list)`** — requires creating a new `Funding` model with nested `Funder` (itself containing `Jurisdiction`) and `FundingLevel` (level0/1/2) sub-models. This is the most complex addition. The `Funding` structure mirrors what likely exists (or will be needed) for projects. Investigate whether a shared `Funding` model already exists or is planned.

### R3. No changes needed for sort, pagination, or routing (Priority: N/A)

- Sort is correctly modeled as relevance-only.
- Pagination behavior matches V3 expectations.
- Resource client needs no code changes — will inherit correct base URL automatically.

---

## Open Questions / Risks

1. **`logicalOperator=NOT` semantics unclear**: The API accepts it without error but appears to produce identical results to omitting it. Is NOT intended only as an inline filter-value operator (as the docs emphasize), with the top-level enum entry being speculative? Recommend documenting this ambiguity rather than relying on top-level NOT behavior.

2. **`Funding` model cross-entity consistency**: The `fundings` field on organizations uses the same Funding/funder structure as projects. If a `Funding` model is created here, it should be coordinated with the Projects migration to avoid duplicate divergent definitions. Check if `ResearchProducts` also gains a `fundings` field in V3.

3. **`CfHbKeyValue` reuse**: The `collectedFrom` field uses `{key, value}` objects. Other entities (research products, datasources) likely also have `collectedFrom`. A shared model should be preferred over per-entity definitions.

4. **Backward compatibility risk LOW**: Since `extra="allow"` is set on both `Organization` and `BaseEntity`, existing code deserializing V3 responses will not crash — new fields are silently stored in `__pydantic_extra__`. The gap is purely one of type-accessibility, not data loss.
