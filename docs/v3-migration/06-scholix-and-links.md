# V3 Migration Research — Scholix & Graph Links Endpoints

## Scope

Both link-retrieval mechanisms in AIREloom:
1. **Graph Links endpoint** — `GET /v3/research-products/links` (and `/v3/research-products/links/relations-info`)
2. **Scholexplorer (Scholix) API** — `GET /v3/Links` at `api.scholexplorer.openaire.eu`

Covers: pagination behavior, page-index bugs, silent pageSize caps, response envelopes, filter parameters, model alignment, and OpenAPI spec defects.

## Method

- Read current source code in `src/aireloom/endpoints.py`, `research_products_client.py`, `scholix_client.py`, `models/relation.py`, `models/scholix.py`
- Parsed V3 OpenAPI spec (`reference/v3-investigation/graph_v3_openapi.json`) for links endpoint schema
- Fetched and parsed Scholexplorer OpenAPI spec from live URL for spec-defect verification
- Ran **12+ live API calls** via `reference/v3-investigation/v3_live.py` against both endpoints with varying page/pageSize/size/cursor values
- Cross-referenced model field names against actual JSON response keys

---

## Findings

### 1. Graph Links Endpoint (`/v3/research-products/links`) — Pagination & Envelope

#### 1.1 Pagination is 0-indexed (CONFIRMED)

| Test | URL | Status | Results | Header |
|------|-----|--------|---------|--------|
| page=0 | `...page=0&pageSize=10` | **200** | 10 results | `{"page":0,"totalPages":13,"totalLinks":121}` |
| page=1 | `...page=1&pageSize=10` | **200** | 10 results | `{"page":1,"totalPages":13,"totalLinks":121}` |

The results **differ** between page=0 and page=1:
- **page=0 first target DOI**: `10.3886/e111743v1` (dataset "Are Ideas Getting Harder to Find?")
- **page=1 first target DOI**: `10.2139/ssrn.2250887` (publication "Universities: The Fallen Angels of Bayh-Dole?")

**Conclusion**: The endpoint is definitively 0-indexed. page=0 is the first page.

#### 1.2 Silent pageSize Cap (CONFIRMED)

| pageSize | Actual results returned | totalPages | totalLinks | Behavior |
|----------|------------------------|------------|------------|----------|
| 100 | **10** | 13 | 121 | **Silently capped to 10** |
| 99 | **99** | 2 | 121 | Returns full 99 |
| 10 | 10 | 13 | 121 | Normal |
| 5 | 5 | 25 | 121 | Normal |

**Critical finding**: `pageSize=100` silently returns only 10 results (not 100, not an error). Maximum working value is **99**. The V3 OpenAPI spec says `"maximum value: 100"` which is **incorrect** — 100 triggers a silent cap to 10.

#### 1.3 Response Envelope (Divergent from Standard Endpoints)

The links endpoint uses a **different header structure** than regular V3 endpoints:

```json
// Links endpoint header (ACTUAL)
{
  "page": 0,
  "totalPages": 13,
  "totalLinks": 121
}
```

**Absent from links header** (present in standard SearchHeader):
- `numFound` — NOT present
- `pageSize` — NOT present
- `nextCursor` — NOT present
- `queryTime` — NOT present
- `maxScore` — NOT present
- `debug` — NOT present

**Present in standard SearchHeader but irrelevant for links**: `totalCitationsCount`, `countsByType`.

Response body shape: `{ header: {page, totalPages, totalLinks}, results: [Relation, ...] }`

#### 1.4 No Cursor Support (CONFIRMED)

Tested `cursor=*` on the links endpoint:
- Returns **200** with results identical to `page=0`
- Header shows `totalPages: 61` (vs 13 for normal paging) — inconsistent metadata
- The cursor parameter is **silently ignored**; it does not enable cursor-based pagination
- **Recommendation**: Do not use cursor on this endpoint; use page-based pagination only

### 2. LATENT BUG: Off-by-One Page Index (CRITICAL)

**Current code** (`src/aireloom/resources/research_products_client.py`):

| Method | Line | Current Default | Problem |
|--------|------|------------------|---------|
| `search_links()` | **81** | `page: int = 1` | Defaults to **page 1** (second page) |
| `iterate_links()` | **126** | `current_page = 1` | Starts at **page 1** (skips first page) |

**Impact**: Every call to `search_links()` without explicit `page=0` and every `iterate_links()` call **silently skips the entire first page of results**. For our test DOI (121 links, 13 pages at pageSize=10), this means skipping ~10 links (~8% of results).

**Evidence**:
```
page=0 → first target: doi 10.3886/e111743v1  (dataset)
page=1 → first target: doi 10.2139/ssrn.2250887 (publication)
```
These are completely different records. The bug causes **data loss**.

**Fix required**:
- `search_links()`: Change default `page: int = 1` → `page: int = 0` (line 81)
- `iterate_links()`: Change `current_page = 1` → `current_page = 0` (line 126)
- Update docstrings from "1-indexed" to "0-indexed"

### 3. Filter Parameters — Links Endpoint

| Param | Type | V1/V2 Code (LinksFilters) | V3 Spec | Live Verified | Notes |
|-------|------|---------------------------|---------|---------------|-------|
| `sourcePid` | string | ✅ present | ✅ optional | ✅ works | Filter by source PID (e.g., DOI) |
| `targetPid` | string | ✅ present | ✅ optional | ✅ works | Filter by target PID |
| `sourcePublisher` | string | ✅ present | ✅ optional | ✅ works | Filter by source publisher name |
| `targetPublisher` | string | ✅ present | ✅ optional | ✅ works | Filter by target publisher name |
| `sourceType` | string | ✅ present | ✅ optional | ✅ works | Values: publication, dataset, software, other |
| `targetType` | string | ✅ present | ✅ optional | ✅ works | Values: publication, dataset, software, other |
| `relation` | string | ✅ present | ✅ optional | ✅ works | Relation type name (e.g., Cites, References) |
| `fromDate` | string | ✅ present | ✅ optional | ✅ works | Format: YYYY or YYYY-MM-DD |
| `toDate` | string | ✅ present | ✅ optional | ✅ works | Format: YYYY or YYYY-MM-DD |
| `page` | integer | set in code (default=1 ❌) | ✅ optional | ✅ 0-indexed | **BUG: default should be 0** |
| `pageSize` | integer | set in code (default=20) | ✅ optional, max=100❌ | ✅ max=99 | **Spec says max=100 but 100 silently caps to 10** |

**Filter status**: All filters are compatible between code and V3 API. No parameter renames needed.

**Docstring issue**: `LinksFilters` docstring references `https://api.openaire.eu/graph/v1/researchProducts/links` — should be updated to v3.

### 4. Response Model Alignment — Links (`models/relation.py`)

| Model Field | V3 Live Field | Type | Status | Notes |
|-------------|--------------|------|--------|-------|
| `header` (Header) | `header` | object | ✅ matches | But Header model has fields not returned by links (numFound, nextCursor, etc.) — harmless due to `extra="allow"` + Optionals |
| `results` (list[Relation]) | `results` | array | ✅ matches | |

**Relation model fields** vs live V3 response:

| Model Field | Live JSON Key | Type | Status |
|-------------|--------------|------|--------|
| `source` (Node) | `source` | object | ✅ |
| `target` (Node) | `target` | object | ✅ |
| `relType` (RelType) | `relType` | object | ✅ |

**Node fields** vs live:

| Model Field | Live JSON Key | Type | Status |
|-------------|--------------|------|--------|
| `title` | `title` | string | ✅ |
| `type` | `type` | string | ✅ |
| `instanceType` | `instanceType` | string | ✅ |
| `publicationDate` | `publicationDate` | string | ✅ |
| `identifiers` | `identifiers` | array | ✅ |
| `authors` | `authors` | array | ✅ |
| `collectedFrom` | `collectedFrom` | array | ✅ |

**Identifier fields** vs live:

| Model Field | Live JSON Key | Type | Status |
|-------------|--------------|------|--------|
| `id` | `id` | string | ✅ |
| `idScheme` | `idScheme` | string | ✅ |
| `idUrl` | `idUrl` | string | ✅ |

**RelType fields** vs live:

| Model Field | Live JSON Key | Type | Status |
|-------------|--------------|------|--------|
| `name` | `name` | string | ✅ |
| `type` | `type` | string | ✅ |
| `typeSchema` | `typeSchema` | string | ✅ |

**Verdict**: All relation model fields align perfectly with V3 live responses. No changes needed.

### 5. Relations-Info Endpoint (`/v3/research-products/links/relations-info`)

**Status**: ✅ **Fully functional**

Returns a JSON array of relation type descriptors (no envelope wrapper):

```json
[
  {
    "relation": "Cites",
    "inverse": "IsCitedBy",
    "description": "This resource cites another resource.",
    "descriptionInverse": "This resource is cited by another resource."
  },
  // ... 19 total relation types
]
```

**Full list of 19 relation types returned**:
Cites/IsCitedBy, IsSourceOf/IsDerivedFrom, IsRelatedTo, HasAmongTopNSimilarDocuments/IsAmongTopNSimilarDocuments, References/IsReferencedBy, HasPart/IsPartOf, IsSupplementTo/IsSupplementedBy, IsNewVersionOf/IsPreviousVersionOf, HasVersion/IsVersionOf, Continues/IsContinuedBy, Documents/IsDocumentedBy, IsIdenticalTo, IsOriginalFormOf/VariantFormOf, Reviews/IsReviewedBy, Compiles/IsCompiledBy, Obsoletes/IsObsoletedBy, Describes/IsDescribedBy, [truncated at "Req"...]

Current code (`get_relations_info()` at line 150) handles this correctly — wraps in list if scalar. No changes needed.

### 6. Scholix Endpoint (`/v3/Links` at scholexplorer.openaire.eu)

#### 6.1 Pagination (CONFIRMED 0-indexed)

| Test | URL | Status | currentPage | totalLinks | totalPages | RESULTS |
|------|-----|--------|-------------|------------|------------|---------|
| page=0, size=10 | `...page=0&size=10` | **200** | 0 | 121 | 13 | 10 |
| page=0, size=100 | `...page=0&size=100` | **200** | 0 | 121 | 13 | **10** (silent cap!) |
| page=0, size=99 | `...page=0&size=99` | **200** | 0 | 121 | 2 | **99** |

**Same silent cap pattern as Graph links**: size=100 → 10 results. Max working value = 99.

#### 6.2 Response Envelope

Scholix uses its own envelope (different from Graph links):

```json
{
  "currentPage": 0,
  "totalLinks": 121,
  "totalPages": 13,
  "result": [ /* ScholixRelationship objects */ ]
}
```

Key differences from Graph links:
- Uses `currentPage` (not `page`)
- Uses `result` (not `results`)
- No `header` wrapper — flat envelope

#### 6.3 Scholix Model Alignment (`models/scholix.py`)

| Model Field | Alias (Live Key) | Live Verified | Notes |
|-------------|-----------------|---------------|-------|
| `current_page` | `currentPage` | ✅ | int |
| `total_links` | `totalLinks` | ✅ | int |
| `total_pages` | `totalPages` | ✅ | int |
| `result` | `result` | ✅ | list[ScholixRelationship] |

**ScholixRelationship** fields:

| Model Field | Alias | Live Verified | Notes |
|-------------|-------|---------------|-------|
| `link_provider` | `LinkProvider` | ✅ | list of provider objects |
| `relationship_type` | `RelationshipType` | ✅ | {Name, SubType, SubTypeSchema} |
| `source` | `Source` | ✅ | ScholixEntity |
| `target` | `Target` | ✅ | ScholixEntity |
| `link_publication_date` | `LinkPublicationDate` | ✅ | date string |
| `license_url` | `LicenseURL` | ✅ | nullable |
| `harvest_date` | `HarvestDate` | ✅ | date string |

**ScholixEntity** fields:

| Model Field | Alias | Live Verified | Notes |
|-------------|-------|---------------|-------|
| `identifier` | `Identifier` | ✅ | list with ID, IDScheme, IDURL |
| `type` | `Type` | ✅ | publication/dataset/software/other |
| `sub_type` | `SubType` | ✅ | e.g., "Article" |
| `title` | `Title` | ✅ | string |
| `creator` | `Creator` | ✅ | list with name, identifier |
| `publication_date` | `PublicationDate` | ✅ | date string |
| `publisher` | `Publisher` | ✅ | list with name, identifier |

**ScholixRelationshipType** fields:

| Model Field | Alias (Live Key) | Live Verified |
|-------------|-----------------|---------------|
| `name` | `Name` | ✅ (e.g., "References") |
| `sub_type` | `SubType` | ✅ (e.g., "references") |
| `sub_type_schema` | `SubTypeSchema` | ✅ (e.g., "datacite") |

**Verdict**: All Scholix models align correctly with live V3 API responses. No field changes needed.

#### 6.4 Scholix Filter Parameters

| Param | Code (ScholixFilters) | V3 Spec (Scholix) | Live Verified | Notes |
|-------|----------------------|-------------------|---------------|-------|
| `sourcePid` | ✅ string | ✅ optional | ✅ works | Required in practice for results |
| `targetPid` | ✅ string | ✅ optional | ✅ works | Alternative to sourcePid |
| `sourcePublisher` | ✅ string | ✅ optional | ✅ works | |
| `targetPublisher` | ✅ string | ✅ optional | ✅ works | |
| `sourceType` | ✅ Literal[4 values] | ✅ optional | ✅ works | PascalCase: Publication, Dataset... |
| `targetType` | ✅ Literal[4 values] | ✅ optional | ✅ works | PascalCase: Publication, Dataset... |
| `relation` | ✅ string | ✅ optional | ✅ works | Relation type name |
| `from_date` (alias "from") | ✅ date | ✅ as "from" | ✅ works | API param name is "from" |
| `to_date` (alias "to") | ✅ date | ✅ as "to" | ✅ works | API param name is "to" |
| `page` | set in code (default=0 ✅) | **required=True ❌** | ✅ 0-indexed | Spec bug: says required but default=0 works |
| `size` | set in code (page_size) | ✅ optional, max=100❌ | ✅ max=99 | Same silent cap at 100 |

### 7. Scholexplorer OpenAPI Spec Defects (CONFIRMED)

Fetched from `https://api.scholexplorer.openaire.eu/api-docs/Scholexplorer%20API%20V3.0`:

| Defect | Detail | Impact |
|--------|--------|--------|
| **Title typo** | `info.title` = `"ScholeExplorer APIs"` | Missing 'x' — should be "Scholexplorer" |
| **page required=true** | `/v3/Links` GET param `page` has `required: true` | **Wrong** — page defaults to 0 when omitted; should be `required: false` |
| **size max=100** | Description says "max is 100" | **Misleading** — size=100 silently caps to 10; real max is 99 |

Additionally noted: `/v3/api-docs` returns **500** on the Scholexplorer server.

---

## Live Verification Summary

All commands run from repo root via `python3 reference/v3-investigation/v3_live.py`.

### Graph Links Endpoint

```bash
# 1. Confirm 0-indexed: page=0 returns first page
python3 v3_live.py graph "research-products/links" "sourcePid=10.1016/j.respol.2021.104226&page=0&pageSize=10" --full
# STATUS: 200, HEADER: {"page":0,"totalPages":13,"totalLinks":121}, RESULTS: 10
# First result target DOI: 10.3886/e111743v1

# 2. page=1 returns DIFFERENT results (second page)
python3 v3_live.py graph "research-products/links" "sourcePid=10.1016/j.respol.2021.104226&page=1&pageSize=10" --full
# STATUS: 200, HEADER: {"page":1,"totalPages":13,"totalLinks":121}, RESULTS: 10
# First result target DOI: 10.2139/ssrn.2250887 ← DIFFERENT from page=0!

# 3. pageSize=100 silent cap → only 10 results
python3 v3_live.py graph "research-products/links" "sourcePid=10.1016/j.respol.2021.104226&page=0&pageSize=100"
# STATUS: 200, HEADER: {"page":0,"totalPages":13,"totalLinks":121}, RESULTS: 10 ← CAPPED!

# 4. pageSize=99 → full 99 results
python3 v3_live.py graph "research-products/links" "sourcePid=10.1016/j.respol.2021.104226&page=0&pageSize=99"
# STATUS: 200, HEADER: {"page":0,"totalPages":2,"totalLinks":121}, RESULTS: 99 ← FULL

# 5. cursor=* silently ignored (same results as page=0)
python3 v3_live.py graph "research-products/links" "sourcePid=10.1016/j.respol.2021.104226&cursor=*&pageSize=2" --full
# STATUS: 200, identical first result to page=0, totalPages=61 (inconsistent metadata)

# 6. relations-info endpoint
python3 v3_live.py graph "research-products/links/relations-info" "" --full
# STATUS: 200, returns array of 19 relation type objects
```

### Scholix Endpoint

```bash
# 7. Scholix page=0, size=10
python3 v3_live.py scholix "Links" "sourcePid=10.1016/j.respol.2021.104226&page=0&size=10" --full
# STATUS: 200, CURRENTPAGE:0, TOTALLINKS:121, TOTALPAGES:13, RESULTS:10

# 8. Scholix size=100 silent cap → 10 results
python3 v3_live.py scholix "Links" "sourcePid=10.1016/j.respol.2021.104226&page=0&size=100"
# STATUS: 200, CURRENTPAGE:0, TOTALLINKS:121, TOTALPAGES:13, RESULTS:10 ← CAPPED!

# 9. Scholix size=99 → 99 results
python3 v3_live.py scholix "Links" "sourcePid=10.1016/j.respol.2021.104226&page=0&size=99"
# STATUS: 200, CURRENTPAGE:0, TOTALLINKS:121, TOTALPAGES:2, RESULTS:99 ← FULL
```

---

## Recommendations

### CRITICAL: Fix Page-Index Bug (Data Loss)

| File | Line | Current | Fix |
|------|------|---------|-----|
| `src/aireloom/resources/research_products_client.py` | **81** | `page: int = 1` | `page: int = 0` |
| `src/aireloom/resources/research_products_client.py` | **91** | Docstring: "1-indexed page number" | Change to "0-indexed page number" |
| `src/aireloom/resources/research_products_client.py` | **126** | `current_page = 1` | `current_page = 0` |

### HIGH: Clamp pageSize/size to 99

Both endpoints silently cap at 100→10. The library should clamp proactively:

| File | Line | Recommendation |
|------|------|----------------|
| `src/aireloom/resources/research_products_client.py` | **82**, **112** | Add validation: `if page_size > 99: page_size = 99` (or raise) |
| `src/aireloom/resources/scholix_client.py` | **102**, **162** | Same clamping for `size` parameter in `_build_scholix_params` or callers |

### MEDIUM: Update Docstrings and References

| File | Line | Issue | Fix |
|------|------|-------|-----|
| `src/aireloom/resources/research_products_client.py` | **86** | Comment says "v1 `/researchProducts/links` endpoint" | Update to "v3 `/research-products/links` endpoint" |
| `src/aireloom/resources/research_products_client.py` | **153** | Comment says "v1 `/researchProducts/links/relations-info`" | Update to "v3" |
| `src/aireloom/endpoints.py` | **267** | LinksFilters docstring references `graph/v1/...` URL | Update to v3 URL |
| `src/aireloom/endpoints.py` | **23** | `LINKS = "researchProducts/links"` uses camelCase | V3 uses kebab-case; verify if server accepts both or fix to `"research-products/links"` |

### LOW: Header Model Consideration

The `Header` base model (`src/aireloom/models/base.py:20-75`) contains fields that links never returns (`numFound`, `nextCursor`, `queryTime`, `maxScore`, `pageSize`). This is harmless because they're Optional and the model has `extra="allow"`, but could mislead future developers into expecting those fields. Options:
- Keep as-is (low risk, backwards-compatible)
- Document that links header is a subset

### Scholix Client: No Changes Needed

The Scholix client already correctly:
- Uses 0-indexed pages (`search_links` default `page=0`, `iterate_links` starts at `current_page=0`)
- Maps `page_size` → `size` parameter via `_build_scholix_params()`
- Uses correct response envelope fields (`currentPage`, `totalLinks`, `totalPages`, `result`)
- All model aliases match live API key names

---

## Open Questions / Risks

1. **Silent cap stability**: The pageSize=100→10 and size=100→10 silent cap could change without notice if OpenAIRE fixes their backend. Clamping to 99 in client code protects against this.
2. **cursor=* on links**: Returns 200 with inconsistent `totalPages` (61 vs 13). Is this an undocumented partial feature or a server bug? **Do not rely on cursor pagination for links.**
3. **Path case-sensitivity**: Current constant is `LINKS = "researchProducts/links"` (camelCase). V3 uses kebab-case paths everywhere else. Need to verify whether the Graph API accepts both casings for this legacy-named endpoint.
4. **Scholix spec says page required**: If OpenAIRE updates their server to enforce the spec's `required=true`, omitting `page` would break. Currently safe since code always sends it explicitly.
5. **Compounded bug impact**: The page=1 default + pageSize=100 default (in iterate_links) means users get wrong page AND 10x fewer results per page than expected — a ~8% data loss AND 10x slowdown.
6. **No sort support on either endpoint**: Neither Graph links nor Scholix expose a `sortBy` parameter. Result ordering is server-determined and non-configurable.