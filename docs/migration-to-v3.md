# Migrating to AIREloom 0.5 (OpenAIRE Graph API v3)

AIREloom 0.5 is a **breaking** release that moves the library onto the
[OpenAIRE Graph API **v3**](https://api.openaire.eu/graph/v3). OpenAIRE has
deprecated v1/v2 (removal expected ~6 months after the v3 release); 0.5 is the
path forward.

This guide enumerates every breaking change from 0.4.x and shows how to update
your code. Additive changes (new optional fields, new filters) are listed at the
end — they cannot break existing code but are worth knowing about.

!!! tip "Pre-release opt-in"
    0.5 ships first as `0.5.0a1` (alpha). Pre-releases are **not** installed by
    default — `pip install aireloom` keeps resolving to 0.4.0 until 0.5.0
    stable. To opt in early:

    ```bash
    pip install "aireloom>=0.5.0a1"
    ```

## Summary of breaking changes

| Area | Change |
|---|---|
| Base URL | Single `https://api.openaire.eu/graph/v3` for **all** Graph entities (was a v1/v2 split) |
| Paths | Kebab-case (handled automatically by the library) |
| Filter renames | `authorOrcid`→`authorId`, `bestOpenAccessRightLabel`→`accessRightLabel`, `sdg`→`sdgLabel` |
| Cardinality | `sdg: list[str]` → `sdgLabel: str` |
| Type change | Projects `fromStartDate`/`toStartDate`/`fromEndDate`/`toEndDate` now `str` (was `date`) |
| Removed | `grantID` (Projects filter); persons `startDate`/`endDate` sort fields |
| Links pagination | `/research-products/links` is **0-indexed** (first page `page=0`) and page size caps at 99 |

Because filter models use `extra="forbid"`, a removed or renamed filter produces
a clear Pydantic `ValidationError` listing the valid fields — fix the field name
and you're done.

## 1. Filter renames (Research Products)

Three filters were renamed to match the v3 parameter names.

| 0.4 (v1/v2) | 0.5 (v3) |
|---|---|
| `authorOrcid` | `authorId` |
| `bestOpenAccessRightLabel` | `accessRightLabel` |
| `sdg` | `sdgLabel` |

```python
# Before (0.4)
ResearchProductsFilters(authorOrcid="0000-0001-2345-6789",
                        bestOpenAccessRightLabel="OPEN",
                        sdg=["SDG 3", "SDG 7"])

# After (0.5)
ResearchProductsFilters(authorId="0000-0001-2345-6789",
                        accessRightLabel="Open Access",
                        sdgLabel="SDG 3")  # see cardinality note below
```

## 2. Cardinality change: `sdg` → `sdgLabel`

`sdg` was a `list[str]`; `sdgLabel` is a single `str`. For multiple SDGs, use
the inline `OR` operator inside the value — the library auto-quotes it:

```python
# Multiple SDGs in v3:
ResearchProductsFilters(sdgLabel="SDG 3 OR SDG 7")
```

## 3. Type change: Projects date filters

The Projects date-range filters changed from `date | None` to `str | None`
because v3 accepts bare years. Passing `date(...)` objects no longer works;
pass strings:

```python
# Before (0.4)
ProjectsFilters(fromStartDate=date(2020, 1, 1), toEndDate=date(2022, 12, 31))

# After (0.5) — a bare year is enough
ProjectsFilters(fromStartDate="2020", toEndDate="2022")
# full dates still work as strings:
ProjectsFilters(fromStartDate="2020-01-01")
```

## 4. Removed filters and sort fields

- **`grantID`** is gone from `ProjectsFilters` (v3 dropped the parameter). Use
  `fundingShortName` plus a code/text search instead.
- **Persons sort fields `startDate` / `endDate`** were removed (v3 validation
  rejects them). Persons now supports `search` and `bestAccessRightLabel` sorts.

## 5. Base URL & paths

You do not need to change client construction — `AireloomSession()`/`AireloomClient()`
now target `https://api.openaire.eu/graph/v3` for every Graph entity. The v1/v2
per-entity routing is gone. If you previously relied on research products being
served from v2 and the rest from v1, note they are now all v3.

## 6. Links endpoint: 0-indexed pagination

The `/research-products/links` endpoint is **0-indexed**: the first page is
`page=0`, not `page=1`. The library handles this for you in `search_links()` and
`iterate_links()`, but if you pass an explicit `page`, start at `0`.

Additionally, the server **silently caps page size at 99** (requesting 100
returns only 10). The library clamps `page_size`/`size` to 99 and warns if you
ask for more. This cap also applies to the Scholix API.

## 7. Auto-quoting of filter values

Filter values that contain spaces or the operators `AND`/`OR`/`NOT` or
parentheses are now **automatically double-quoted** by the library so v3's Solr
parser treats them as phrases. You no longer need to quote manually:

```python
# Works as-is — "Open Access" is quoted for you on the wire
ResearchProductsFilters(accessRightLabel="Open Access")
```

`logicalOperator` is excluded from quoting (it is sent bare). The meta-filter
keys (`logicalOperator`) are passed through unchanged.

## Additive (non-breaking) changes

These do not affect existing code (`extra="allow"` already absorbed them), but
you can now use them with typed access:

- **41 new filter parameters** across entities (Research Products +20, Projects
  +13, Data Sources +8), including `fromPublicationYear`, `hasLicense`,
  `relFunder`, `country`, `eoscdatasourcetype`, `thematic`, and more.
- **`logicalOperator`** widened to accept `"AND"`, `"OR"`, `"NOT"` on all Graph
  filter models.
- **New typed response fields**: `eoscIfGuidelines`, `publiclyFunded`,
  `isGreen`, `isInDiamondJournal`, `openAccessRoute` (on access rights),
  `conferencePlace`/`conferenceDate` (containers), `originalIds`/`collectedFrom`/
  `fundings` (organizations), hierarchical `funding` + `links` (projects),
  `collectedFrom`/`eoscdatasourcetype`/`jurisdiction`/`odlanguages`/`links`
  (data sources), and `Subject.provenance`.
- **`popularity`** is now a valid sort field for Research Products.

## Need help?

If a `ValidationError` blocks you, its message lists every accepted field for
the filter model — that is the fastest way to find the v3 name for an old
parameter. For the full investigation behind these changes (including server
bugs that remain open in v3), see the research notes under
[`docs/v3-migration/`](https://github.com/utsmok/aireloom/tree/main/docs/v3-migration).
