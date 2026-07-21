# Implementation Plan Review

**Reviewer:** Independent review (PlanReview agent)
**Date:** 2026-07-21
**Subject:** `docs/v3-migration/IMPLEMENTATION_PLAN.md` and its 8 supporting research reports (`01`–`08`)
**Method:** Read plan + all 8 reports + `AGENTS.md` + `OPENAIRE_V3_INVESTIGATION_REPORT.md` in full; spot-checked every headline claim against the live V3 API via `reference/v3-investigation/v3_live.py`; cross-checked file:line references against the current source tree.

## Verdict

**SOUND WITH REVISIONS**

## Summary

The plan's factual claims are accurate — every behavioral assertion I tested against the live V3 API checked out, including the four highest-risk ones (kebab-case 405, links off-by-one, persons 500s fixed, `popularity` sort works). The release/versioning strategy (phased clean cutover, PEP 440 pre-releases, reject runtime toggle, stay on `0.x`) is the right call for an alpha-stage library, and the Phase 1 reconciliation of the Projects-vs-CoreInfrastructure `_base_url_override` contradiction is correct. The plan's main weaknesses are **execution-completeness gaps, not correctness errors**: two scope-summary items (the RP `popularity` sort addition and the Persons `startDate`/`endDate` sort removal) have no corresponding action in any phase, the `Subject` shape change is deferred to "investigate" despite a known incompatible V3 structure, and a few claims (e.g., "add `py.typed`") are stale.

## Verified claims

All spot-checks were run from repo root against the live V3 API on 2026-07-21 using `reference/v3-investigation/v3_live.py` (OAuth2 client-credentials auth from `.env`).

| # | Claim in plan/report | Spot-check command | Result | Verdict |
|---|---|---|---|---|
| 1 | V3 returns **405** for camelCase paths (`researchProducts`, `dataSources`) — "hard requirement" | `graph "researchProducts" "pageSize=1"`; `graph "dataSources" "pageSize=1"` | Both → `405 "No static resource v3/researchProducts."` / `v3/dataSources.` | ✅ CONFIRMED |
| 2 | Links endpoint is 0-indexed; **page=0 and page=1 return different records** (data-loss bug) | Fetched `research-products/links?sourcePid=10.1016/j.respol.2021.104226&page={0,1}&pageSize=10` and compared target DOIs | page 0 first target = `10.3886/e111743v1` ("Are Ideas Getting Harder to Find?"); page 1 first target = `10.1162/daed_a_00521` ("Universities: The Fallen Angels of Bayh-Dole?") — completely disjoint | ✅ CONFIRMED (the off-by-one bug is real; current `current_page = 1` skips the first page) |
| 3 | Reconciliation: `_base_url_override` should be **removed** from `ResearchProductsClient`; **not** added to `ProjectsClient` (rejects `03`-R7) | Read `src/aireloom/resources/projects_client.py` — `ProjectsClient` has no override and currently inherits `OPENAIRE_GRAPH_API_BASE_URL` (V1) | `ProjectsClient` confirms no override; once `constants.py:9` flips to V3, all clients inherit V3 automatically. Adding a Projects override would be redundant. | ✅ CONFIRMED (plan's `07`-wins reconciliation is correct) |
| 4 | Persons `givenName`/`lastName` 500s are **fixed** in V3 | `graph "persons" "givenName=John&pageSize=1"`; `graph "persons" "lastName=Smith&pageSize=1"` | Both → `200`; `numFound=35018` and `12917` respectively | ✅ CONFIRMED |
| 5 | `popularity` sort works on V3 (despite being omitted from the sortBy error message) | `graph "research-products" "search=covid&pageSize=1&sortBy=popularity+DESC"` | `200`, `numFound=1687589` | ✅ CONFIRMED |
| 6 | Filter values containing spaces **must be double-quoted** (NEW V3 behavior) | `accessRightLabel=Open+Access` (unquoted) vs `accessRightLabel=%22Open+Access%22` (quoted) | Unquoted → `400 "Values containing spaces, parentheses or logical operators must be wrapped in double quotes"`; quoted → `200`, `numFound=139770253` | ✅ CONFIRMED (exact error text validates the plan's Phase 3 trigger conditions) |
| 7 | Links endpoint **silently caps `pageSize=100` → 10**; max working = 99 | `research-products/links?...&pageSize=100` vs `pageSize=99` | `pageSize=100` → 10 results, `totalPages=13`; `pageSize=99` → 99 results, `totalPages=2` | ✅ CONFIRMED |
| 8 | Regular endpoints **reject `pageSize>100`** with 400 (no silent cap) | `research-products?search=covid&pageSize=200` | `400 "Page size must be at most 100"`; `pageSize=100` returns 100 results | ✅ CONFIRMED |
| 9 | Regular endpoints are **1-indexed** (`page=0` → 400); links are 0-indexed | `research-products?pageSize=1&page=0` vs `page=1` | `page=0` → `400 "must be greater than or equal to 1"`; `page=1` → `200` | ✅ CONFIRMED |
| 10 | Scholix silent cap: `size=100` → 10 results | `scholix "Links" "...&size=100"` | `200`, returns 10 results (`currentPage=0, totalLinks=121, totalPages=13`) | ✅ CONFIRMED |
| 11 | Cursor pagination works on regular endpoints | `research-products?...&cursor=*` | `200` with `nextCursor: "AoM/DzAwMDY0..."` returned in header | ✅ CONFIRMED |
| 12 | Projects `funder=EC` returns 0 results (filter non-functional); `fundingShortName=EC` works | Both queries | `funder=EC` → `numFound=0`; `fundingShortName=EC` → `numFound=129486` | ✅ CONFIRMED |
| 13 | (Resolves `08` open question) `impulseClass`, `popularityClass`, `instanceType`, `isInDiamondJournal`, `isPubliclyFunded`, `description`, `relCollectedFromDatasourceId` all still work as V3 filters | One live call per param, all `pageSize=1` | All returned `200` with non-trivial `numFound` (e.g., `instanceType=Article` → 170M, `description=covid` → 1.29M, `isInDiamondJournal=true` → 1.69M) | ✅ CONFIRMED — the plan is right to **keep** these fields; `08`'s speculation about their removal was unfounded |

## Critical issues (must-fix before execution)

None of the issues below block the migration's correctness, but two are severe enough that an executor working phase-by-phase would silently miss required work. They are "critical" in the sense of *execution-completeness*, not API correctness.

### C1. Two `ENDPOINT_DEFINITIONS` sort-dict changes appear in the Scope Summary but have NO action item in any phase

**Where:** Plan §2 Scope Summary table (line ~60, "Sort" row) promises: *"RP: re-add `popularity` (it works); Persons: relevance-only (drop `startDate`/`endDate`)"*. Neither task appears in Phase 1–9.

**Current code (`src/aireloom/endpoints.py:331-362`):**
- `RESEARCH_PRODUCTS` sort dict (lines 331–338): missing `"popularity"` — confirmed working on V3 (see Verified Claim #5).
- `PERSONS` sort dict (lines 358–362): includes `"startDate"` and `"endDate"`, both of which return `400` on V3 (per `05`-§2: *"persons can be only sorted by the 'relevance'"*).

**Impact:** Although `StandardResourceClient` does not currently override `_validate_sort_field` (so the sort dict is advisory, not enforced — verified in `.venv/lib/python3.13/site-packages/bibliofabric/resources.py:106-111`), the dict is the documented contract for users and is read by tooling. After migration, users who call `session.persons.search(sort_by="startDate DESC")` will get a `400` from V3 with no client-side guard, and the popularity-sort feature advertised in the scope summary simply won't be declared.

**Fix:** Add an explicit bullet to Phase 2 (or a new Phase 2.5 / Phase 4 item):
> - `endpoints.py:331-338` — add `"popularity": {}` to `ENDPOINT_DEFINITIONS[RESEARCH_PRODUCTS]["sort"]`.
> - `endpoints.py:358-362` — remove `"startDate": {}` and `"endDate": {}` from `ENDPOINT_DEFINITIONS[PERSONS]["sort"]` (V3 rejects both).

Without these bullets, an executor reading only the phase actions will ship 0.5.0 with the same sort-dict drift the migration was supposed to fix.

### C2. `Subject` model shape change is deferred to "investigate" despite a known, documented, incompatible V3 structure

**Where:** Plan §3 Phase 5: *"Investigate the **`Subject` shape change** (V3 returns a different structure — verify and adjust `Subject` model)."* Repeated in §4 Reconciliation Notes: *"Needs targeted live re-verification and a model adjustment in Phase 5."*

**The shape is already known** — `01`-§5b gives it explicitly. Verified live:
```json
{"subject": {"scheme": "FOS", "value": "03 medical and health sciences"}, "provenance": null}
```
Current model (`src/aireloom/models/research_product.py:375-389`):
```python
class Subject(BaseModel):
    subject: dict[str, str] | None = None
    model_config = ConfigDict(extra="allow")
```

**Impact:** The current model does not crash on V3 data (Pydantic accepts `{scheme, value}` as `dict[str, str]`; `provenance` falls into `__pydantic_extra__`), so this is not a runtime break. But the deferral creates three risks: (a) the executor may treat "investigate" as optional and ship without touching the model, leaving users with untyped access to `.subject["scheme"]`; (b) the deferral invites scope creep at execution time; (c) the `extra="allow"` fallback hides the structural change from any test that doesn't assert on the new field set.

**Fix:** Replace "Investigate…" with a concrete decision in Phase 5. Recommended minimal design:
```python
class SubjectValue(BaseModel):
    scheme: str | None = None
    value: SafeStr = ""
    model_config = ConfigDict(extra="allow")

class Subject(BaseModel):
    subject: SubjectValue | None = None
    provenance: dict | None = None
    model_config = ConfigDict(extra="allow")
```
Either adopt this (or equivalent) or explicitly document that `Subject` stays lossy/untyped for 0.5.0 and bump to a future release. Don't leave it as "investigate."

## Important issues (should-fix)

### I1. Phase 0 instructs adding `src/aireloom/py.typed`, but the file already exists

**Where:** Plan §3 Phase 0, second bullet: *"Add `src/aireloom/py.typed` (empty) — PEP 561 marker (currently missing despite `Typing :: Typed` classifier; noted in `AIRELOOM_IMPROVEMENT_PLAN.md`)."*

**Reality:** `src/aireloom/py.typed` already exists (verified with `ls src/aireloom/py.typed`). This is also explicitly confirmed in `08`-§5 (*"`py.typed` marker | Exists | `src/aireloom/py.typed` | ✅ PEP 561 compliant"*) — so the plan contradicts its own research base. The source of the stale claim is `AIRELOOM_IMPROVEMENT_PLAN.md:10-14`, which predates the file's addition.

**Fix:** Delete this bullet from Phase 0, or reword to *"Verify `src/aireloom/py.typed` ships in the wheel (already present in source)."* Keep the `pyproject.toml` wheel-inclusion check.

### I2. Phase 3 quoting helper under-specifies list-typed filter values

**Where:** Plan §3 Phase 3 §1: *"Add a serialization helper that wraps a string filter value in `"..."` iff it contains a space/paren and does not already start with `"` or `(`."*

**Gap:** Several filter fields are `list[str]` (`subjects`, `contentTypes`, `keywords`, `fos`, `sdg` pre-rename). `08`-R6's reference pseudo-code handles lists element-wise, but the plan's prose only mentions "a string filter value". If implemented literally as written, a value like `subjects=["Open Access Research"]` would not get its inner strings quoted → V3 400.

**Fix:** Add to Phase 3: *"For list-typed filter fields, apply the quoting rule element-wise to each string item; leave non-string items (bool, int) untouched."*

### I3. Phase 3 trigger regex omits "logical operators," which V3's own error message requires

**Where:** Plan §3 Phase 3 §1 trigger condition ("contains a space/paren"). V3's live error (Verified Claim #6) reads: *"Values containing **spaces, parentheses or logical operators** must be wrapped in double quotes."*

**Gap:** A bare value of `OR`, `AND`, or `NOT` (or any string containing those tokens without spaces) would not be wrapped by the plan's helper but would be rejected by V3. This is an edge case (most filter values aren't bare operators), but the helper's trigger set should match the server's documented rule.

**Fix:** Either expand the trigger regex to `\b(OR|AND|NOT)\b|[\s()]`, or explicitly document the limitation (and that power-users can pre-quote).

### I4. Reconciliation note about list→string serialization only flags `subjects`/`contentTypes`; same concern applies to `keywords` and `fos`

**Where:** Plan §4 second bullet (*"V3 specs `subjects`/`contentTypes` as `string` (comma-separated); current code uses `list[str]`."*).

**Gap:** `ResearchProductsFilters` has `fos: list[str] | None` and `subjects: list[str] | None`; `ProjectsFilters` has `keywords: list[str] | None`. All share the same list-vs-comma-string serialization question. The reconciliation note covers only two of four affected fields.

**Fix:** Expand the verification item to cover all list-typed filter fields, or state explicitly which fields are in scope for the serializer change.

### I5. No contingency if OpenAIRE removes V1/V2 before 0.5.0 stable ships

**Where:** Plan §1.4 step 6 (*"0.4.0 remains the last V1/V2 release… Dies naturally when OpenAIRE removes V1/V2 (~6 months)"*) and §5 Risk Register last row (*"OpenAIRE removes V1/V2 before 0.5.0 stable | Low | Med | Time-box the migration; 0.4.0 is best-effort legacy"*).

**Gap:** "Time-box the migration" is not a contingency, it's a hope. The plan rejects a runtime toggle and a separate package (correctly, for an alpha lib), but offers no fallback if the migration slips past the V1/V2 sunset. All 0.4.0 users would be broken with no patched release available.

**Fix:** Add a contingency: e.g., "If OpenAIRE announces a firm V1/V2 sunset date before 0.5.0b1 tags, cut an accelerated `0.5.0` from whatever phase is complete (minimum: Phase 1 + Phase 4 §1) and ship without the additive model/filter work." This is a strategy note, not new code.

### I6. Phase 1 §6 (unwrapper fallback) is placed in Phase 1 but rated "low priority / not blocking" by the research

**Where:** Plan §3 Phase 1 §6 (*"`unwrapper.py:62-64` (low priority) — add a `result` fallback…"*) — but it's listed under Phase 1 ("foundation; everything depends on this"), which the plan says to "Implement first, alone."

**Gap:** Phase 1 is described as the blocking foundation, but this item is explicitly low-priority and not blocking (`07`-R6: *"Not blocking today (Scholix bypasses unwrapper)"*). Mixing critical and cosmetic items in the "foundation" phase muddies the gate.

**Fix:** Move this item to Phase 5 (Response models / cleanup) or Phase 8, so Phase 1's acceptance criterion is unambiguously the blocking core-infra work.

### I7. `ProjectsFilters` date-filter type change (`date | None` → `str | None`) is a user-facing break not flagged for the migration guide

**Where:** Plan §3 Phase 2 §3: *"change `fromStartDate`/`toStartDate`/`fromEndDate`/`toEndDate` from `date | None` → `str | None`."*

**Gap:** Current users passing Python `date(2022, 1, 1)` will get a Pydantic coercion error after this change. This is exactly the kind of break the new `docs/migration-to-v3.md` (Phase 8) should call out, but Phase 8's docs bullet is generic.

**Fix:** Add the four Projects date fields (and the `sdg: list[str]` → `sdgLabel: str` cardinality change) to the explicit "breaking changes" list for the migration guide.

## Minor issues / suggestions

- **M1. New-filter count is inconsistent across documents.** Plan §2 Scope Summary says *"~43 new filter parameters (RP 22, Projects 13, DS 8)"*, but `OPENAIRE_V3_INVESTIGATION_REPORT.md` §4 says *"20 added"* for RP, and `01`-§2c says *"22 new"* (counting `includeStats` and `cursor` as filters). Depending on whether meta-params are counted, the RP number is 20 or 22; total is 41 or 43. Pick one definition and use it consistently.

- **M2. Phase 4 §2 treats Graph-links and Scholix page-size clamps with equal urgency, but Scholix's default is `DEFAULT_PAGE_SIZE = 20`** (`src/aireloom/constants.py:14`), not 100. Scholix users only hit the cap if they explicitly pass `page_size≥100`. The Graph-links clamp is urgent (default is 100, silently truncated); Scholix is defensive-only. Note the distinction.

- **M3. Some file:line references are slightly off.** Examples: `_base_url_override` is at `research_products_client.py:47`, not `:50`; the `ENDPOINT_DEFINITIONS` sort dict is at lines 328-368, broader than the cited `:331-338`. All are within ±3 lines and easy to relocate, but the executor should grep rather than trust line numbers verbatim.

- **M4. The plan retains the non-functional `funder` filter in `ProjectsFilters`** (Phase 2 §3 lists `funder` among the 13 new fields). This is defensible (forward-compat; the spec lists it), but the model docstring should explicitly say *"returns 0 results for all known values as of 2026-07; prefer `fundingShortName`"*, mirroring the reconciliation note. Otherwise users will hit the same dead-end the research did.

- **M5. The `_batch.py:120` comma-separated OR syntax is not re-verified on V3.** The plan says Phase 4 §4 (*"`_batch.py:120` — `page=1` is correct… leave as-is"*), but doesn't confirm V3 still honors `pid=10.1038/a,10.1038/b,10.1038/c` (the docstring claims this is OpenAIRE's OR syntax). A spot-check during Phase 9 live verification would be cheap insurance.

- **M6. Pre-existing issue surfaced but not introduced by the plan:** `queries.py` `citing_works` / `related_datasets` / `all_links` accept a `sort_by` parameter and forward it to `session.scholix.collect()`, but Scholix has no sort support (`06`-§6.4). Not a migration blocker; consider noting for a future cleanup.

- **M7. The `extra="forbid"` UX story is understated.** Plan §1.1 says *"users get a clean, explicit error if they pass an old field name."* In practice the error is a Pydantic `ValidationError` listing all valid fields — workable but not "clean" for casual users. Plan §6.4 raises a deprecation shim as an open question; for an alpha lib the answer is probably "no shim, just good docs," but the plan should commit either way rather than leaving it open.

## What the plan gets right

- **Every behavioral claim tested against the live API checked out** (13 of 13 spot-checks in this review, including the four highest-risk ones). The research base is solid.
- **The `_base_url_override` reconciliation is correct.** The plan correctly picks `07`-R2 (remove RP override) over `03`-R7 (add Projects override), and the ProjectsClient source confirms it has no override and currently inherits V1.
- **The off-by-one bug analysis is correct and the fix is right.** `current_page = 1` on a 0-indexed endpoint silently drops page 0; switching both `search_links(page=0)` and `iterate_links(current_page=0)` resolves it. Verified with disjoint page-0 vs page-1 records.
- **The page-size clamp to 99 is the correct mitigation** for the silent `100→10` cap on links/Scholix, and the regular endpoints' proper 1–100 enforcement means no clamp is needed there.
- **The release strategy is sound for an alpha-stage library.** PEP 440 pre-releases (`0.5.0a1`/`b1`) give opt-in runway without surprising `pip install aireloom` users; rejecting the runtime toggle avoids doubling the test matrix; rejecting a separate package avoids fragmenting a tiny user base; staying on `0.x` (rather than jumping to `1.0.0`) correctly signals that the API surface isn't yet stable.
- **Phasing is in the right dependency order.** Phase 1 (core infra) correctly blocks everything; Phase 2 (filters) → Phase 3 (quoting) → Phase 6 (queries) is the right chain (renamed filters need quoting to round-trip); Phase 4 (clients) depends on Phase 1 constants; Phase 5 (models) is additive and could even run in parallel with 2–4.
- **"Scholix needs no changes" is correct.** The Scholix client already uses 0-indexed pages, the correct `result`-singular envelope, and the right base URL (`api.scholexplorer.openaire.eu/v3`). Verified live.
- **Persons `givenName`/`lastName` "now fixed" claim is correct**, and the plan correctly removes the CAUTION docstrings.
- **The plan correctly retains the fields `08` speculated might be removed** (`impulseClass`, `popularityClass`, `instanceType`, `isInDiamondJournal`, `isPubliclyFunded`, `description`, `relCollectedFromDatasourceId`) — all returned 200 in live testing.
- **The "investigate but don't block on `funder`" decision** is the right call: documented, prefer `fundingShortName`, ship the field for forward-compat.
- **Pre-release gating on Phase 9** (ruff, ty, pytest ≥95% cov, live smoke) is concrete and verifiable.
- **The plan correctly preserves `extra="allow"` on response models** to avoid data loss from spec drift, while adding typed declarations for high-value new fields.
