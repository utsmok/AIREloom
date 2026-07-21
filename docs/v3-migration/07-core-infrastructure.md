# V3 Migration Research — Core Infrastructure Layer

## Scope

Cross-cutting infrastructure examined:
- Base URL constants & version routing (`constants.py`, `client.py`, `session.py`)
- Session/client initialization and auth resolution (`client.py`, `session.py`)
- Response unwrapping logic (`unwrapper.py`)
- Header model and ApiResponse envelope (`models/base.py`)
- Pagination mechanics: page vs cursor, 0 vs 1 indexing (`_standard.py`, `_batch.py`, `research_products_client.py`)
- Batch mixin pagination assumption (`_batch.py`)

## Method

1. Read all source files listed in scope (constants, client, session, unwrapper, models/base, _standard, _batch, all resource clients, scholix_client)
2. Parsed V3 OpenAPI spec (`reference/v3-investigation/graph_v3_openapi.json`) for path list, `SearchHeader` schema, `SearchResponseRelation`, `ResearchProductsSearchResponseV3`
3. Executed **16 live API calls** against `https://api.openaire.eu/graph/v3/` and `https://api.scholexplorer.openaire.eu/v3/` using `reference/v3-investigation/v3_live.py`
4. Tested V1 and V2 reachability via curl
5. Cross-referenced live responses against current code assumptions

## Findings

### 1. Base URL Consolidation — One V3 URL Serves All Entities

**Current code has two Graph API base URLs plus a separate Scholix URL:**

| Constant | Value | Defined At |
|----------|-------|------------|
| `OPENAIRE_GRAPH_API_BASE_URL` | `https://api.openaire.eu/graph/v1` | `src/aireloom/constants.py:9` |
| `OPENAIRE_GRAPH_API_V2_BASE_URL` | `https://api.openaire.eu/graph/v2` | `src/aireloom/constants.py:10` |
| `OPENAIRE_SCHOLIX_API_BASE_URL` | `https://api.scholexplorer.openaire.eu/v3` | `src/aireloom/constants.py:11` |

**Live verification — all 5 entity types under `/graph/v3/`:**

| Entity | Path | Status | Header snippet |
|--------|------|--------|----------------|
| research-products | `/v3/research-products?pageSize=1` | **200** | `{"numFound":380387557,"page":1,"pageSize":1,...}` |
| projects | `/v3/projects?pageSize=1` | **200** | `{"numFound":3910921,"page":1,"pageSize":1,...}` |
| persons | `/v3/persons?givenName=John&pageSize=1` | **200** | `{"numFound":35018,"page":1,"pageSize":1,...}` |
| organizations | `/v3/organizations?pageSize=1` | **200** | `{"numFound":496636,"page":1,"pageSize":1,...}` |
| datasources | `/v3/datasources?pageSize=1` | **200** | `{"numFound":155484,"page":1,"pageSize":1,...}` |

**Conclusion:** A single V3 base URL (`https://api.openaire.eu/graph/v3`) serves all entities. The v1/v2 split (where ResearchProducts was routed to v2, everything else to v1) is eliminated.

**Current routing that must change:**

| File | Line | What it does | Needed change |
|------|------|-------------|---------------|
| `constants.py` | 9-10 | Defines two Graph URLs | Replace with single `OPENAIRE_GRAPH_API_BASE_URL = "https://api.openaire.eu/graph/v3"` |
| `research_products_client.py` | 50 | `_base_url_override = OPENAIRE_GRAPH_API_V2_BASE_URL` | Remove override; inherit from parent (now V3) |
| `client.py` | 73 | `base_url` param default=`OPENAIRE_GRAPH_API_BASE_URL` (v1) | Default changes automatically when constant updates |
| `session.py` | 100 | Falls back to `OPENAIRE_GRAPH_API_BASE_URL` | Changes automatically |

### 2. Pagination Indexing — Regular vs Links vs Scholix

This is the **most critical infrastructure finding**. There are THREE different pagination regimes:

#### 2a. Regular Graph Endpoints (research-products, projects, persons, organizations, datasources)

| Test | Query | Status | Observation |
|------|-------|--------|-------------|
| page=0 | `?pageSize=1&page=0` | **400** | `"must be greater than or equal to 1"` |
| page=1 | `?pageSize=1&page=1` | **200** | First page returned, `"page":1` in header |
| cursor=* | `?pageSize=2&cursor=*` | **200** | Returns `nextCursor` (base64 string) |
| cursor follow-up | `?pageSize=2&cursor=<nextCursor>` | **200** | Returns new `nextCursor`; results advance |

**Verdict:** 1-indexed pages. `page=1` is correct first page. Cursor pagination works as documented.

**`batch_get` correctness (`_batch.py:120`):**
```python
response = await self.search(page=1, page_size=batch_size, filters={...})
```
**CORRECT.** `page=1` is the correct first page for regular endpoints.

#### 2b. Links Endpoint (`/v3/research-products/links`) — DIFFERENT regime

| Test | Query | Status | Header | Results count |
|------|-------|--------|--------|---------------|
| page=0 | `?sourcePid=...&pageSize=1` | **200** | `{"page":0,"totalPages":121,"totalLinks":121}` | 1 |
| page=1 | `?sourcePid=...&pageSize=1` | **200** | `{"page":1,"totalPages":121,"totalLinks":121}` | 1 (this is page 2!) |
| pageSize=100 | `?...&pageSize=100` | **200** | `{"totalPages":13}` | **10** (silent cap!) |
| pageSize=99 | `?...&pageSize=99` | **200** | `{"totalPages":2}` | **99** (works) |

**Verdict:** Links is **0-indexed** (page=0 is first page). Has a silent pageSize cap at 100 (returns only 10); max working value is 99. No `numFound`, no `nextCursor`, no `queryTime`, no `maxScore`.

**CRITICAL BUG in current code (`research_products_client.py:81,112,126`):**

```python
async def search_links(self, *, ..., page: int = 1, ...):  # line 81 — defaults to 1
    ...
    current_page = 1  # line 126 — iterate_links starts at 1
```

When migrated to V3, `page=1` will **skip the entire first page** of link results. Must change to `page=0` default and start iteration at 0.

Also note: `iterate_links` currently passes `page_size=100` by default (line 112) — this will hit the silent cap and return only 10 results per page on V3. Should be reduced to 99.

#### 2c. Scholix Endpoint (`https://api.scholexplorer.openaire.eu/v3/Links`)

| Field | Live value | Notes |
|-------|-----------|-------|
| `currentPage` | `0` | 0-indexed |
| `totalLinks` | `121` | Total matching links |
| `totalPages` | `61` (with size=2) / `121` (with size=1) | Varies by size param |
| Result key | `result` (not `results`!) | Singular key name |

**Verdict:** 0-indexed. Uses completely flat envelope (no `header` wrapper). Result array is under `result` not `results`. Already handled correctly by `ScholixResponse` model (`scholix.py:190-214`) which maps `currentPage`→`current_page`, `totalLinks`→`total_links`, `result`→`result`.

### 3. Response Envelope Comparison

Three distinct envelope shapes exist. The table below maps each field across all three:

| Field | Regular Graph (live) | Links (live) | Scholix (live) | Current `Header` model has it? |
|--------|---------------------|--------------|----------------|-------------------------------|
| `numFound` | ✅ int | ❌ absent | ❌ absent | ✅ (`base.py:48`) |
| `nextCursor` | ✅ string (base64) | ❌ absent | ❌ absent | ✅ (`base.py:49`) |
| `pageSize` | ✅ int | ❌ absent | ❌ absent | ✅ (`base.py:50`) |
| `page` | ✅ int (1-based) | ✅ int (0-based) | N/A (uses `currentPage`) | ✅ (`base.py:51`) |
| `maxScore` | ✅ float | ❌ absent | ❌ absent | ✅ (`base.py:52`) |
| `queryTime` | ✅ int | ❌ absent | ❌ absent | ✅ (`base.py:47`) |
| `totalPages` | ❌ absent (regular) | ✅ int | ✅ int | ✅ (`base.py:53`) |
| `totalLinks` | ❌ absent | ✅ int | ✅ int | ✅ (`base.py:54`) |
| `status` | ❌ absent | ❌ absent | ❌ absent | ✅ (`base.py:43`) — optional |
| `code` | ❌ absent | ❌ absent | ❌ absent | ✅ (`base.py:44`) — optional |
| `message` | ❌ absent | ❌ absent | ❌ absent | ✅ (`base.py:45`) — optional |

**OpenAPI spec `SearchHeader`** declares all fields as optional (no `required` array), so the current `Header` model with all-optional fields + `extra="allow"` is structurally compatible with all three envelopes. This is good design.

### 4. Unwrapper Correctness Analysis

| Method | What it does | Works for Regular? | Works for Links? | Works for Scholix? |
|--------|-------------|-------------------|------------------|--------------------|
| `unwrap_results()` | `response_json.get("results")` | ✅ | ✅ (links uses `results`) | ❌ Scholix uses `result` |
| `unwrap_single_item()` | Calls `unwrap_results()[0]` | ✅ | ✅ | ❌ (same root cause) |
| `get_next_page_token()` | `header.get("nextCursor")` | ✅ | Returns `None` (correct) | Returns `None` (correct) |
| `get_total_results()` | `header.get("numFound")` | ✅ | Returns `None` (acceptable) | Returns `None` (acceptable) |

**Key gap:** The unwrapper cannot extract results from a Scholix response because Scholix uses `result` (singular) not `results` (plural). **However**, this is NOT a blocking issue because:

1. `ScholixClient` does NOT use the standard unwrapper path — it has its own `search_links()` method (`scholix_client.py:104`) that calls `self._request_raw()` directly and validates into `ScholixResponse` manually.
2. The `BaseResourceClient.collect()/count()/first()` convenience methods on `ScholixClient` delegate to `self.search()` which aliases to `self.search_links()` — also bypassing the unwrapper.

**Recommendation:** Add a fallback to `unwrap_results()` that checks `result` if `results` is missing, for future-proofing. Low priority since Scholix is correctly handled independently today.

### 5. V1/V2 Deprecation Window

| Version | Endpoint tested | HTTP Status | Notes |
|---------|----------------|-------------|-------|
| V1 | `https://api.openaire.eu/graph/v1/researchProducts?pageSize=1` | **200** | Still reachable |
| V2 | `https://api.openaire.eu/graph/v2/researchProducts?pageSize=1` | **200** | Still reachable |
| V3 | `https://api.openaire.eu/graph/v3/research-products?pageSize=1` | **200** | Current target |

All three versions are live simultaneously. No sunset date announced. Migration should proceed to V3 but V1/V2 availability provides a safety net.

## Live Verification (Commands & Observed Output)

### All 5 entities under V3:
```bash
# research-products
python3 reference/v3-investigation/v3_live.py graph "research-products" "pageSize=1"
# STATUS: 200, HEADER: {"numFound": 380387557, "maxScore": 1.0, "queryTime": 2419, "page": 1, "pageSize": 1}

# projects
python3 reference/v3-investigation/v3_live.py graph "projects" "pageSize=1"
# STATUS: 200, HEADER: {"numFound": 3910921, ... "page": 1, "pageSize": 1}

# persons
python3 reference/v3-investigation/v3_live.py graph "persons" "givenName=John&pageSize=1"
# STATUS: 200, HEADER: {"numFound": 35018, ... "page": 1, "pageSize": 1}

# organizations
python3 reference/v3-investigation/v3_live.py graph "organizations" "pageSize=1"
# STATUS: 200, HEADER: {"numFound": 496636, ... "page": 1, "pageSize": 1}

# datasources
python3 reference/v3-investigation/v3_live.py graph "datasources" "pageSize=1"
# STATUS: 200, HEADER: {"numFound": 155484, ... "page": 1, "pageSize": 1}
```

### Regular endpoint pagination indexing:
```bash
# page=0 → REJECTED
python3 reference/v3-investigation/v3_live.py graph "research-products" "pageSize=1&page=0"
# STATUS: 400, ERROR MESSAGE: must be greater than or equal to 1

# page=1 → OK (first page)
python3 reference/v3-investigation/v3_live.py graph "research-products" "pageSize=1&page=1"
# STATUS: 200, HEADER: {..., "page": 1, ...}
```

### Cursor pagination round-trip:
```bash
# Initial cursor request
python3 reference/v3-investigation/v3_live.py graph "research-products" "pageSize=2&cursor=*" --full
# STATUS: 200, HEADER: {..., "nextCursor": "AoM/DzAwMDY0YWFiYmRhOTo6MDAwN2ZjN2NiNGVmZjc3YmIzMGQ1OGI1ZGJjMDIyMjEIP4AAAD8P..."}

# Follow-up with nextCursor
python3 reference/v3-investigation/v3_live.py graph "research-products" "pageSize=2&cursor=AoM/DzAwMDY0YWFiYmRhOTo6MDAwN2ZjN2NiNGVmZjc3YmIzMGQ1OGI1ZGJjMDIyMjEIP4AAAD8P..."
# STATUS: 200, HEADER: {..., "nextCursor": "AoM/DzAwMDY0YWFiYmRhOTo6MDAwYjVlNTEyMjMxNzk5YTA4YjIyNjdkYzQyODZlZDgIP4AAAD8P..."}
# RESULTS: 2 (different records — cursor advanced)
```

### Links endpoint (different envelope, 0-indexed):
```bash
# page=0 → first page (0-indexed)
python3 reference/v3-investigation/v3_live.py graph "research-products/links" "sourcePid=10.1016/j.respol.2021.104226&pageSize=1"
# STATUS: 200, HEADER: {"page": 0, "totalPages": 121, "totalLinks": 121}, RESULTS: 1
# NOTE: no numFound, no nextCursor, no pageSize, no queryTime, no maxScore

# page=1 → second page (NOT first!)
python3 reference/v3-investigation/v3_live.py graph "research-products/links" "sourcePid=10.1016/j.respol.2021.104226&page=1&pageSize=1"
# STATUS: 200, HEADER: {"page": 1, "totalPages": 121, "totalLinks": 121}, RESULTS: 1

# pageSize=100 → silent cap to 10 results
python3 reference/v3-investigation/v3_live.py graph "research-products/links" "sourcePid=10.1016/j.respol.2021.104226&pageSize=100"
# STATUS: 200, HEADER: {"totalPages": 13}, RESULTS: 10 (expected 100!)

# pageSize=99 → works correctly
python3 reference/v3-investigation/v3_live.py graph "research-products/links" "sourcePid=10.1016/j.respol.2021.104226&pageSize=99"
# STATUS: 200, HEADER: {"totalPages": 2}, RESULTS: 99
```

### Scholix envelope (flat, no header wrapper):
```bash
python3 reference/v3-investigation/v3_live.py scholix "Links" "sourcePid=10.1016/j.respol.2021.104226&size=2" --full
# STATUS: 200
# CURRENTPAGE: 0, TOTALLINKS: 121, TOTALPAGES: 61
# Uses "result" key (not "results"), flat structure (no "header")
```

### V1/V2 reachability:
```bash
curl -s -o /dev/null -w "%{http_code}" "https://api.openaire.eu/graph/v1/researchProducts?pageSize=1"
# → 200

curl -s -o /dev/null -w "%{http_code}" "https://api.openaire.eu/graph/v2/researchProducts?pageSize=1"
# → 200
```

### CamelCase path rejection on V3 (R5 hard requirement proof):
```bash
python3 reference/v3-investigation/v3_live.py graph "researchProducts" "pageSize=1"
# STATUS: 405, ERROR: No static resource v3/researchProducts.

python3 reference/v3-investigation/v3_live.py graph "dataSources" "pageSize=1"
# STATUS: 405, ERROR: No static resource v3/dataSources.
```

## Recommendations

### R1. Merge base URL constants to single V3 constant
**File:** `src/aireloom/constants.py:9-11`

**Change:**
```python
# BEFORE (two Graph URLs):
OPENAIRE_GRAPH_API_BASE_URL = "https://api.openaire.eu/graph/v1"
OPENAIRE_GRAPH_API_V2_BASE_URL = "https://api.openaire.eu/graph/v2"

# AFTER (single V3 URL):
OPENAIRE_GRAPH_API_BASE_URL = "https://api.openaire.eu/graph/v3"
```

Remove `OPENAIRE_GRAPH_API_V2_BASE_URL` entirely. Keep `OPENAIRE_SCHOLIX_API_BASE_URL` unchanged (Scholix remains on a different host).

**Impact:** Cascades automatically to `client.py:73` (default param), `session.py:100` (fallback), and every resource client that inherits `base_url` from `AireloomClient`.

### R2. Remove ResearchProductsClient's _base_url_override
**File:** `src/aireloom/resources/research_products_client.py:50`

**Change:**
```python
# BEFORE:
_base_url_override: str | None = OPENAIRE_GRAPH_API_V2_BASE_URL

# AFTER: (delete this line entirely — inherit V3 from parent)
```

The v2 override was the sole reason for the split routing. With all entities on V3, `ResearchProductsClient` should use the same base URL as `ProjectsClient`, `OrganizationsClient`, etc.

### R3. Fix links endpoint pagination — CRITICAL bug
**File:** `src/aireloom/resources/research_products_client.py:81,112,126`

**Changes needed:**

| Line | Current | Fix | Reason |
|------|---------|-----|--------|
| 81 | `page: int = 1` | `page: int = 0` | V3 links is 0-indexed; page=1 skips first page |
| 112 | `page_size: int = 100` | `page_size: int = 99` | pageSize=100 silently capped to 10 on V3 |
| 126 | `current_page = 1` | `current_page = 0` | Iteration must start at page 0 |

Also update the docstring at line 90 to say "0-indexed page number" instead of "1-indexed".

### R4. Update search_links base_url_override target
**File:** `src/aireloom/resources/research_products_client.py:104`

```python
# BEFORE:
base_url_override=OPENAIRE_GRAPH_API_BASE_URL,  # resolves to v1 today

# AFTER (once R1 applied, this becomes V3 automatically; or remove explicitly)
```

After R1, `OPENAIRE_GRAPH_API_BASE_URL` points to V3, so this line resolves correctly. But consider whether the explicit override is still needed — if ResearchProductsClient no longer has `_base_url_override` (R2), the inherited base URL is already V3.

Same applies to `get_relations_info()` at line 162.

### R5. Update endpoint path constants to kebab-case [HARD REQUIREMENT]
**File:** `src/aireloom/endpoints.py:17-23`

V3 uses kebab-case paths. Current constants:
```python
RESEARCH_PRODUCTS = "researchProducts"      # camelCase (V1/V2 style)
ORGANIZATIONS = "organizations"            # already correct
DATA_SOURCES = "dataSources"               # camelCase
PROJECTS = "projects"                      # already correct
PERSONS = "persons"                        # already correct
SCHOLIX = "Links"                          # correct (Scholix path)
LINKS = "researchProducts/links"           # needs update
```

**Needed changes:**
- `RESEARCH_PRODUCTS`: `"researchProducts"` → `"research-products"`
- `DATA_SOURCES`: `"dataSources"` → `"datasources"`
- `LINKS`: `"researchProducts/links"` → `"research-products/links"`

**Verified against live API:** V3 returns **405** for both `researchProducts` and `dataSources` paths ("No static resource"). Kebab-case is the ONLY accepted format.

### R6. Harden unwrapper for Scholix compatibility (low priority)
**File:** `src/aireloom/unwrapper.py:62-64`

Add a fallback in `unwrap_results()`:
```python
results = response_json.get("results")
if results is None:
    results = response_json.get("result")  # Scholix uses singular key
```

Not blocking today (Scholix bypasses unwrapper), but prevents future breakage if someone wires Scholix through the standard pipeline.

### R7. Header model — no structural change needed
**File:** `src/aireloom/models/base.py:20-75`

The current `Header` model already has all fields optional with `extra="allow"`. It correctly deserializes all three envelope types (regular Graph header, links header, and tolerates Scholix's flat structure via `ScholixResponse`'s own mapping). No change required.

## Open Questions / Risks

1. **[RESOLVED] Endpoint path case-sensitivity**: V3 **rejects** camelCase paths with 405. R5 (kebab-case path constants) is a **hard requirement**. See Live Verification section for proof.

2. **Scholix V3 under graph host**: The V3 Graph API now includes a `/research-products/links` endpoint that returns structured relation data (similar to Scholix but with a different envelope). Post-migration, evaluate whether the separate Scholix client/host can be retired in favor of the unified Graph links endpoint. The Graph links endpoint returns richer metadata (authors, publicationDate, instanceType) vs Scholix's simpler format.

3. **V1/V2 sunset timeline**: OpenAIRE has not announced deprecation dates for V1/V2. Plan to support a transition period where either the library targets V3 exclusively OR accepts a version parameter. Recommend cutting over to V3-only in the next major release.

4. **Links `totalPages` accuracy**: When `pageSize=100` (silently capped to 10), `totalPages=13` (121/10≈12.1, rounded up). When `pageSize=99`, `totalPages=2` (121/99≈1.22, rounded up). The `totalPages` calculation appears to use the *requested* pageSize, not the actual capped count. This means iteration logic relying on `totalPages` for loop termination will work correctly as long as `pageSize ≤ 99`.

5. **Batch get with page=1 on non-standard endpoints**: If `batch_get` is ever used with a client whose `search()` targets the links endpoint, `page=1` would be wrong. Currently `batch_get` is only used by entity clients (ResearchProducts, Projects, etc.) for their standard search endpoints, so this is theoretical. Worth a code comment guard.
