# "Other component objects | OpenAIRE Graph Documentation"

[Source](https://graph.openaire.eu/docs/data-model/entities/other#container)

Here we describe other component objects that are used as part of the main graph entities.

## AccessRight

Subclass of [BestAccessRight](https://graph.openaire.eu/docs/data-model/entities/#bestaccessright), indicates information about rights held in and over the resource and the open Access Route.

### openAccessRoute

*Type: One of `{ gold, green, hybrid, bronze }` • Cardinality: ONE*

Indicates the OpenAccess status. Values are set according to the [Unpaywall methodology](https://support.unpaywall.org/support/solutions/articles/44001777288-what-do-the-types-of-oa-status-green-gold-hybrid-and-bronze-mean-).

```
"openAccessRoute": "gold"
```

## AlternateIdentifier

Type used to represent the information associated to persistent identifiers associated to the research product that have not been forged by an authority for that pid type. For example we collect metadata from an institutional repository that provides as identifier for the research product also the DOI.

### scheme

*Type: String • Cardinality: ONE*

Vocabulary reference.

```
"scheme": "doi"
```

### value

*Type: String • Cardinality: ONE*

Value from the given scheme/vocabulary.

```
"value": "10.1016/j.respol.2021.104226"
```

## APC

Indicates the money spent to make a book or article available in Open Access. Sources for this information includes the OpenAPC initiative.

### currency

*Type: String • Cardinality: ONE*

The system of money in which the amount is expressed (Euro, USD, etc).

```
"currency": "EU"
```

### amount

*Type: String • Cardinality: ONE*

The quantity of money.

```
"amount": "1000"
```

## Author

Represents the research product author.

### fullName

*Type: String • Cardinality: ONE*

Author's full name.

```
"fullName": "Turunen, Heidi"
```

### name

*Type: String • Cardinality: ONE*

Author's given name.

```
"name": "Heidi"
```

### surname

*Type: String • Cardinality: ONE*

Author's family name.

```
"surname": "Turunen"
```

### rank

*Type: String • Cardinality: ONE*

Author's order in the list of authors for the given research product.

```
"rank": 1
```

### pid

*Type: [AuthorPid](https://graph.openaire.eu/docs/data-model/entities/#authorpid) • Cardinality: ONE*

Persistent identifier associated with this author.

```
"pid": {    "id": {        "scheme": "orcid",        "value": "0000-0001-7169-1177"     },    "provenance": {        "provenance": "Harvested",        "trust": "0.9"     }}
```

## AuthorPid

The author's persistent identifier.

### id

*Type: [AuthorPidSchemaValue](https://graph.openaire.eu/docs/data-model/entities/#authorpidschemavalue) • Cardinality: ONE*

```
"id": {    "scheme": "orcid",    "value": "0000-0001-7169-1177" }
```

### provenance

*Type: [Provenance](https://graph.openaire.eu/docs/data-model/entities/#provenance-2) • Cardinality: ONE*

The reason why the pid was associated to the author.

```
"provenance": {    "provenance": "Inferred by OpenAIRE",    "trust": "0.85" }
```

## AuthorPidSchemaValue

Type used to represent the scheme and value for the author's pid.

### schema

*Type: String • Cardinality: ONE*

The author's pid scheme. OpenAIRE currently supports ORCID.

```
"scheme": "orcid"
```

### value

*Type: String • Cardinality: ONE*

The author's pid value in that scheme.

```
"value": "0000-1111-2222-3333"
```

## BestAccessRight

Indicates the most open access rights \*available among the research product instances.

\* where the openness is defined by the ordering of the access right terms in the following.

```
OPEN SOURCE > OPEN > EMBARGO (6MONTHS) > EMBARGO (12MONTHS) > RESTRICTED > CLOSED > UNKNOWN
```

### code

*Type: String • Cardinality: ONE*

COAR access mode code: [http://vocabularies.coar-repositories.org/documentation/access\_rights/](http://vocabularies.coar-repositories.org/documentation/access_rights/).

```
"code": "c_16ec"
```

### label

*Type: String • Cardinality: ONE*

Label for the access mode.

```
"label": "RESTRICTED"
```

### scheme

*Type: String • Cardinality: ONE*

Scheme of reference for access right code. Currently, always set to COAR access rights vocabulary: [http://vocabularies.coar-repositories.org/documentation/access\_rights/](http://vocabularies.coar-repositories.org/documentation/access_rights/).

```
"scheme": "http://vocabularies.coar-repositories.org/documentation/access_rights/"
```

## CitationImpact

The different citation-based impact indicators as computed by [BIP!](https://bip.imsi.athenarc.gr/).

### indicator

*Type: String • Cardinality: ONE*

The name of indicator; it can be either one of:

- `influence`: it reflects the overall/total (citation-based) impact of an article in the research community at large, based on the underlying citation network (diachronically).
- `citationCount`: it is an alternative to the "Influence" indicator, which also reflects the overall/total (citation-based) impact of an article in the research community at large, based on the underlying citation network (diachronically).
- `popularity`: it reflects the "current" (citation-based) impact/attention (the "hype") of an article in the research community at large, based on the underlying citation network.
- `impulse`: it reflects the initial momentum of an article directly after its publication, based on the underlying citation network.

For more details on how these indicators are calculated, please refer [here](https://graph.openaire.eu/docs/graph-production-workflow/indicators-ingestion/impact-indicators).

```
"citationImpact": {        "influence": 123,        "influenceClass": "C2",        "citationCount": 456,        "citationClass": "C3",        "popularity": 234,        "popularityClass": "C1",        "impulse": 987,        "impulseClass": "C3"}
```

### class

*Type: String • Cardinality: ONE*

The impact class assigned based on the indicator score.

To facilitate comprehension, BIP! also offers impact classes for articles, to group together those that have similar impact. The following 5 classes are provided:

- `C1`: Top 0.01%
- `C2`: Top 0.1%
- `C3`: Top 1%
- `C4`: Top 10%
- `C5`: Bottom 90%

## Container

This field has information about the conference or journal where the research product has been presented or published.

```
"container": {  "name": "Research Policy",  "edition": "xyz",  "issnLinking": "0048-7333",  "issnOnline": "1873-7625",  "issnPrinted": "1377-9655",  "sp": "xyz",  "ep": "xyz",  "iss": "xyz",  "vol": "xyz"}
```

```
"container": {  "name": "Research Policy",  "conferenceDate": "2022-09-22",  "conferencePlace": "Padua, Italy"}
```

### name

*Type: String • Cardinality: ONE*

Name of the journal or conference.

### issnPrinted

*Type: String • Cardinality: ONE*

The journal printed issn.

### issnOnline

*Type: String • Cardinality: ONE*

The journal online issn.

### issnLinking

*Type: String • Cardinality: ONE*

The journal linking issn.

### iss

*Type: String • Cardinality: ONE*

The journal issue.

### sp

*Type: String • Cardinality: ONE*

The start page.

### ep

*Type: String • Cardinality: ONE*

The end page.

### vol

*Type: String • Cardinality: ONE*

The journal volume.

### edition

*Type: String • Cardinality: ONE*

The edition of the journal or conference.

### conferencePlace

*Type: String • Cardinality: ONE*

The place of the conference.

### conferenceDate

*Type: String • Cardinality: ONE*

The date of the conference.

## ControlledField

Generic type used to represent the information described by a scheme and a value in that scheme (i.e. pid).

```
{    "scheme": "DOI",    "value": "10.5281/zenodo.4707307"}
```

### scheme

*Type: String • Cardinality: ONE*

Vocabulary reference.

### value

*Type: String • Cardinality: ONE*

Value from the given scheme/vocabulary.

## Country

To represent the generic country code and label.

```
{    "code" : "IT",    "label": "Italy"}
```

### code

*Type: String • Cardinality: ONE*

ISO 3166-1 alpha-2 country code.

### label

*Type: String • Cardinality: ONE*

The country label.

## Funding

Funding information for a project.

### fundingStream

*Type: [FundingStream](https://graph.openaire.eu/docs/data-model/entities/#fundingstream) • Cardinality: ONE*

Funding information for the project.

```
"fundingStream": {    "description": "Horizon 2020 Framework Programme - Research and Innovation action",    "id": "EC::H2020::RIA"}
```

### jurisdiction

*Type: String • Cardinality: ONE*

Geographical jurisdiction (e.g. for European Commission is EU, for Croatian Science Foundation is HR).

```
"jurisdiction": "EU"
```

### name

*Type: String • Cardinality: ONE*

The name of the funder.

```
"name": "European Commission"
```

### shortName

*Type: String • Cardinality: ONE*

The short name of the funder.

```
"shortName": "EC"
```

## FundingStream

Description of a funding stream.

### id

*Type: String • Cardinality: ONE*

The identifier of the funding stream.

```
"id": "EC::H2020::RIA"
```

### description

*Type: String • Cardinality: ONE*

Short description of the funding stream.

```
"description": "Horizon 2020 Framework Programme - Research and Innovation action"
```

## GeoLocation

Represents the geolocation information.

### point

*Type: String • Cardinality: ONE*

A point with Latitude and Longitude.

```
"point": "7.72486 50.1084"
```

### box

*Type: String • Cardinality: ONE*

A specified bounding box defined by two longitudes (min and max) and two latitudes (min and max).

```
"box": "18.569386 54.468973  18.066832 54.83707"
```

### place

*Type: String • Cardinality: ONE*

The name of a specific place.

```
"place": "Tübingen, Baden-Württemberg, Southern Germany"
```

## Grant

The money granted to a project.

### currency

*Type: String • Cardinality: ONE*

The currency of the granted amount (e.g. EUR).

```
"currency": "EUR"
```

### fundedAmount

*Type: Number • Cardinality: ONE*

The funded amount.

```
"fundedAmount": 1.0E7
```

### totalCost

*Type: Number • Cardinality: ONE*

The total cost of the project.

```
"totalcost": 1.0E7
```

## H2020Programme

The H2020 programme funding a project.

### code

*Type: String • Cardinality: ONE*

The code of the programme.

```
"code": "H2020-EU.1.4.1.3."
```

### description

*Type: String • Cardinality: ONE*

The description of the programme.

```
"description": "Development, deployment and operation of ICT-based e-infrastructures"
```

## Instance

An instance is one specific materialization or version of the research product. For example, you can have one research product with three instances due to deduplication:

- one is the pre-print
- one is the post-print
- one is the published version

Each instance is characterized by the properties that follow.

### accessRight

*Type: [AccessRight](https://graph.openaire.eu/docs/data-model/entities/#accessright) • Cardinality: ONE*

Maps [dc:rights](https://www.dublincore.org/specifications/dublin-core/dcmi-terms/elements11/rights/), describes the access rights of the web resources relative to this instance.

```
"accessRight": {    "code": "c_abf2",    "label": "OPEN",    "openAccessRoute": "gold",    "scheme": "http://vocabularies.coar-repositories.org/documentation/access_rights/" }
```

### alternateIdentifiers

*Type: [AlternateIdentifier](https://graph.openaire.eu/docs/data-model/entities/#alternateidentifier) • Cardinality: MANY*

All the identifiers associated to the research product other than the authoritative ones.

```
"alternateIdentifiers": [    {        "scheme": "doi",        "value": "10.1016/j.respol.2021.104226"    },    ...]
```

### articleProcessingCharge

*Type: [APC](https://graph.openaire.eu/docs/data-model/entities/#apc) • Cardinality: ONE*

The money spent to make this book or article available in Open Access. Source for this information is the OpenAPC initiative.

```
"articleProcessingCharge": {    "currency": "EUR",    "amount": "1000" }
```

### license

*Type: String • Cardinality: ONE*

The license URL.

```
"license": "http://creativecommons.org/licenses/by-nc/4.0"
```

### pids

*Type: [ResultPid](https://graph.openaire.eu/docs/data-model/entities/#resultpid) • Cardinality: MANY*

The set of persistent identifiers associated to this instance that have been collected from an authority for the pid type (i.e. Crossref/Datacite for doi). See the [OpenAIRE entity identifier and PID mapping policy](https://graph.openaire.eu/docs/data-model/pids-and-identifiers) for more information.

```
"pids": [    {        "scheme": "pmc",        "value": "PMC8024784"    },    ...]
```

### publicationDate

*Type: String • Cardinality: ONE*

The publication date of the research product.

```
"publicationDate": "2009-02-12"
```

### refereed

*Type: String • Cardinality: ONE*

Describes if this instance has been peer-reviewed or not. Allowed values are peerReviewed, nonPeerReviewed, UNKNOWN (as defined in [https://api.openaire.eu/vocabularies/dnet:review\_levels](https://api.openaire.eu/vocabularies/dnet:review_levels)). For example:

- peerReviewed: [https://api.openaire.eu/vocabularies/dnet:review\_levels/0001](https://api.openaire.eu/vocabularies/dnet:review_levels/0001)
- nonPeerReviewed: [https://api.openaire.eu/vocabularies/dnet:review\_levels/0002](https://api.openaire.eu/vocabularies/dnet:review_levels/0002)

based on guidelines covers the vocabularies

- [DRIVE guidelines 2.0 - info:eu-repo/semantic](https://wiki.surfnet.nl/download/attachments/10851536/DRIVER_Guidelines_v2_Final_2008-11-13.pdf) (OpenAIRE v1.0 till v3.0 - Literature)
- [COAR Vocabulary v2.0 and v3.0](https://vocabularies.coar-repositories.org/resource_types/) (OpenAIRE v4 - Inst.+Them.)

```
"refereed": "UNKNOWN"
```

### type

*Type: String • Cardinality: ONE*

The specific sub-type of this instance (see [https://api.openaire.eu/vocabularies/dnet:result\_typologies](https://api.openaire.eu/vocabularies/dnet:result_typologies) following the links)

```
"type": "Article"
```

### urls

*Type: String • Cardinality: MANY*

URLs to the instance. They may link to the actual full-text or to the landing page at the hosting source.

```
"urls": [    "https://periodicos2.uesb.br/index.php/folio/article/view/4296",    ...    ]
```

## Indicator

These are indicators computed for a specific OpenAIRE research product.

Each Indicator object is composed of the following properties:

### citationImpact

*Type: [CitationImpact](https://graph.openaire.eu/docs/data-model/entities/#citationImpact) • Cardinality: MANY*

These indicators, provided by [BIP!](https://bip.imsi.athenarc.gr/), estimate the citation-based impact of a research product.

For details about their calculation, please refer [here](https://graph.openaire.eu/docs/graph-production-workflow/indicators-ingestion/impact-indicators).

```
"citationImpact": {        "influence": 123,        "influenceClass": "C2",        "citationCount": 456,        "citationClass": "C3",        "popularity": 234,        "popularityClass": "C1",        "impulse": 987,        "impulseClass": "C3"}
```

### usageCounts

*Type: [UsageCounts](https://graph.openaire.eu/docs/data-model/entities/#usagecounts-1) • Cardinality: ONE*

These measures, computed by the [UsageCounts Service](https://usagecounts.openaire.eu/), are based on usage statistics.

Please refer [here](https://graph.openaire.eu/docs/graph-production-workflow/indicators-ingestion/usage-counts) for more details.

```
"usageCounts": {      "downloads": "10",      "views": "20"}
```

## Language

Represents information for the language of the research product.

```
"language": {      "code": "eng",      "label": "English"}
```

### code

*Type: String • Cardinality: ONE*

Alpha-3/ISO 639-2 code of the language. Values controlled by the [dnet:languages vocabulary](https://api.openaire.eu/vocabularies/dnet:languages).

### label

*Type: String • Cardinality: ONE*

Language label in English.

## OrganizationPid

The schema and value for identifiers of the organization.

```
{      "scheme" : "GRID",      "value" : "grid.7119.e"}
```

### scheme

*Type: String • Cardinality: ONE*

Vocabulary reference (i.e. isni).

### value

*Type: String • Cardinality: ONE*

Value from the given scheme/vocabulary (i.e. 0000000090326370).

## Provenance

Indicates the process that produced (or provided) the information, and the trust associated to the information.

```
{      "provenance" : "Harvested",      "trust": "0.9"}
```

### provenance

*Type: String • Cardinality: ONE*

Provenance term from the vocabulary [dnet:provenanceActions](https://api.openaire.eu/vocabularies/dnet:provenanceActions).

### trust

*Type: String • Cardinality: ONE*

Trust, expressed as a number in the range \[0-1\].

## ResultCountry

Indicates the country associated to the research product. It is a subclass of [Country](https://graph.openaire.eu/docs/data-model/entities/#country) and extends it with provenance information.

### provenance

*Type: [Provenance](https://graph.openaire.eu/docs/data-model/entities/#provenance-2) • Cardinality: ONE*

Indicates the reason why this country is associated to this research product.

```
{    "code" : "IT",    "label": "Italy",    "provenance": {        "provenance": "inferred by OpenAIRE",        "trust": "0.85"    }}
```

## ResultPid

Type used to represent the information associated to persistent identifiers for the research product that have been forged by an authority for that pid type.

```
{      "scheme" : "doi",      "value" : "10.21511/bbs.13(3).2018.13"}
```

### scheme

*Type: String • Cardinality: ONE*

The scheme of the persistent identifier for the research product (i.e. doi). If the pid is here it means the information for the pid has been collected from an authority for that pid type (i.e. Crossref/Datacite for doi). The set of authoritative pid is: `doi` when collected from Crossref or Datacite, `pmid` when collected from EuroPubmed, `arxiv` when collected from arXiv, `handle` from the repositories.

### value

*Type: String • Cardinality: ONE*

The value expressed in the scheme (i.e. 10.1000/182).

## Subject

Represents keywords associated to the research product.

### subject

*Type: [SubjectSchemeValue](https://graph.openaire.eu/docs/data-model/entities/#subjectschemevalue) • Cardinality: ONE*

Contains the subject term: subject type (keyword, MeSH, etc) and the subject term (medicine, chemistry, etc.).

```
"subject": {    "scheme": "keyword",    "value": "SVOC",    "provenance": {        "provenance": "Harvested",        "trust": "0.9"    }}
```

### scheme

*Type: String • Cardinality: ONE*

OpenAIRE subject classification scheme ([https://api.openaire.eu/vocabularies/dnet:subject\_classification\_typologies](https://api.openaire.eu/vocabularies/dnet:subject_classification_typologies)).

```
"scheme" : "keyword"
```

### value

*Type: String • Cardinality: ONE*

The value for the subject in the selected scheme. When the scheme is 'keyword', it means that the subject is free-text (i.e. not a term from a controlled vocabulary).

### provenance

*Type: [Provenance](https://graph.openaire.eu/docs/data-model/entities/#provenance-2) • Cardinality: ONE*

Contains provenance information for the subject term.

## UsageCounts

The usage counts indicator computed for this research product.

```
"usageCounts": {      "downloads": "10",      "views": "20"}
```

### views

*Type: String • Cardinality: ONE*

The number of views for this research product.

### downloads

*Type: String • Cardinality: ONE*

The number of downloads for this research product.

-