# -------------------------------------------------------
#
# C:\dev\AIREloom\reference\official_docs\data_model\entities\community.md
#
# ------------------------------------------------------


# "Communities | OpenAIRE Graph Documentation"

(Source)[https://graph.openaire.eu/docs/data-model/entities/community]

Research communities and research initiatives are intended as groups of people with a common research intent and can be of two types: ​research initiatives or ​research communities​:

- Research initiatives are intended to capture a view of the information space that is "research impact"-oriented, i.e. all products generated due to my research initiative;
- Research communities the latter “research activity” oriented, i.e. all products that may be of interest or related to my research initiative.

For example, the organizations supporting a research infrastructure fall in the first category, while the researchers involved in a discipline fall in the second.

## The `Community` object

### id

*Type: String • Cardinality: ONE*

The OpenAIRE id for the community/research infrastructure, created according to the [OpenAIRE entity identifier and PID mapping policy](https://graph.openaire.eu/docs/data-model/pids-and-identifiers).

```
"id": "context_____::5b7f9fa40bdc12072249204cedfa7808"
```

### acronym

*Type: String • Cardinality: ONE*

The acronym of the community.

```
"acronym": "covid-19"
```

### description

*Type: String • Cardinality: ONE*

Description of the research community/research infrastructure

```
"description": "This portal provides access to publications, research data, projects and software that may be relevant to the Corona Virus Disease (COVID-19). The OpenAIRE COVID-19 Gateway aggregates COVID-19 related records, links them and provides a single access point for discovery and navigation. We tag content from the OpenAIRE Graph (10,000+ data sources) and additional sources. All COVID-19 related research results are linked to people, organizations and projects, providing a contextualized navigation."
```

### name

*Type: String • Cardinality: ONE*

The long name of the community.

```
"name": "Corona Virus Disease"
```

### subjects

*Type: String • Cardinality: MANY*

The list of the subjects associated to the research community (only appies to research communities).

```
"subjects": [    "COVID19",    "SARS-CoV",    "HCoV-19",    ...]
```

### type

*Type: String • Cardinality: ONE*

The type of the community; one of `{ Research Community, Research infrastructure }`.

```
"type": "Research Community"
```

### zenodoCommunity

*Type: String • Cardinality: ONE*

The URL of the Zenodo community associated to the Research community/Research infrastructure.

```
"zenodoCommunity": "https://zenodo.org/communities/covid-19"
```


# -------------------------------------------------------
#
# C:\dev\AIREloom\reference\official_docs\data_model\entities\data_source.md
#
# ------------------------------------------------------


# "Data sources | OpenAIRE Graph Documentation"

[Source](https://graph.openaire.eu/docs/data-model/entities/data-source)

OpenAIRE entity instances are created out of data collected from various data sources of different kinds, such as publication repositories, research data archives, CRIS systems, funder databases, etc. Data sources export information packages (e.g., XML records, HTTP responses, RDF data, JSON) that may contain information on one or more of such entities and possibly relationships between them.

For example, a metadata record about a project carries information for the creation of a Project entity and its participants (as Organization entities). It is important, once each piece of information is extracted from such packages and inserted into the OpenAIRE information space as an entity, for such pieces to keep provenance information relative to the originating data source. This is to give visibility to the data source, but also to enable the reconstruction of the very same piece of information if problems arise.

---

## The `DataSource` object

### id

*Type: String • Cardinality: ONE*

The OpenAIRE id of the data source, created according to the [OpenAIRE entity identifier and PID mapping policy](https://graph.openaire.eu/docs/data-model/pids-and-identifiers).

```
"id": "issn___print::22c514d022b199c346e7f29ca06efc95"
```

### originalIds

*Type: String • Cardinality: MANY*

The list of original identifiers associated to the datasource.

```
"originalIds": [    "issn___print::2451-8271",    ...]
```

### pids

*Type: [ControlledField](https://graph.openaire.eu/docs/data-model/entities/other#controlledfield) • Cardinality: MANY*

The persistent identifiers for the datasource.

```
"pids": [    {        "scheme": "DOI",        "value": "10.5281/zenodo.4707307"     },    ...]
```

### type

*Type: [ControlledField](https://graph.openaire.eu/docs/data-model/entities/other#controlledfield) • Cardinality: ONE*

The datasource type; see the vocabulary [dnet:datasource\_typologies](https://api.openaire.eu/vocabularies/dnet:datasource_typologies).

```
"type": {    "scheme": "pubsrepository::journal",    "value": "Journal"}
```

### openaireCompatibility

*Type: String • Cardinality: ONE*

The OpenAIRE compatibility of the ingested research products, indicates which guidelines they are compliant according to the vocabulary [dnet:datasourceCompatibilityLevel](https://api.openaire.eu/vocabularies/dnet:datasourceCompatibilityLevel).

```
"openaireCompatibility": "collected from a compatible aggregator"
```

### officialName

*Type: String • Cardinality: ONE*

The official name of the datasource.

```
"officialBame": "Recent Patents and Topics on Medical Imaging"
```

### englishName

*Type: String • Cardinality: ONE*

The English name of the datasource.

```
"englishName": "Recent Patents and Topics on Medical Imaging"
```

### websiteUrl

*Type: String • Cardinality: ONE*

The URL of the website of the datasource.

```
"websiteUrl": "http://dspace.unict.it/"
```

### logoUrl

*Type: String • Cardinality: ONE*

The URL of the logo for the datasource.

```
"logoUrl": "https://impactum-journals.uc.pt/public/journals/26/pageHeaderLogoImage_en_US.png"
```

### dateOfValidation

*Type: String • Cardinality: ONE*

The date of validation against the OpenAIRE guidelines for the datasource records.

```
"dateOfValidation": "2016-10-10"
```

### description

*Type: String • Cardinality: ONE*

The description for the datasource.

```
"description": "Recent Patents on Medical Imaging publishes review and research articles, and guest edited single-topic issues on recent patents in the field of medical imaging. It provides an important and reliable source of current information on developments in the field. The journal is essential reading for all researchers involved in Medical Imaging."
```

### subjects

*Type: String • Cardinality: MANY*

List of subjects associated to the datasource

```
"subjects": [    "Medicine",    "Imaging",    ...]
```

### languages

*Type: String • Cardinality: MANY*

The languages present in the data source's content, as defined by OpenDOAR.

```
"languages": [     "eng",    ...]
```

### contentTypes

*Type: String • Cardinality: MANY*

Types of content in the data source, as defined by OpenDOAR

```
"contentTypes": [    "Journal articles",    ...]
```

### releaseStartDate

*Type: String • Cardinality: ONE*

Releasing date of the data source, as defined by re3data.org.

```
"releaseStartDate": "2010-07-24"
```

### releaseEndDate

*Type: String • Cardinality: ONE*

Date when the data source went offline or stopped ingesting new research data. As defined by re3data.org

```
"releaseEndDate": "2016-03-28"
```

### accessRights

*Type: String • Cardinality: ONE*

Type of access to the data source, as defined by re3data.org. Possible values: `{ open, restricted, closed }`.

```
"accessRights": "open"
```

### uploadRights

*Type: String • Cardinality: ONE*

Type of data upload, as defined by re3data.org; one of `{ open, restricted, closed }`.

```
"uploadRights": "closed"
```

### databaseAccessRestriction

*Type: String • Cardinality: ONE*

Access restrictions to the research data repository. Allowed values are: `{ feeRequired, registration, other }`.

This field only applies for re3data data source; see [re3data schema specification](https://gfzpublic.gfz-potsdam.de/rest/items/item_758898_6/component/file_775891/content) for more details.

```
"databaseAccessRestriction": "registration"
```

### dataUploadRestriction

*Type: String • Cardinality: ONE*

Upload restrictions applied by the datasource, as defined by re3data.org. One of `{ feeRequired, registration, other }`.

This field only applies for re3data data source; see [re3data schema specification](https://gfzpublic.gfz-potsdam.de/rest/items/item_758898_6/component/file_775891/content) for more details.

```
"dataUploadRestriction": "feeRequired registration"
```

### versioning

*Type: Boolean • Cardinality: ONE*

Whether the research data repository supports versioning: `yes` if the data source supports versioning, `no` otherwise.

This field only applies for re3data data source; see [re3data schema specification](https://gfzpublic.gfz-potsdam.de/rest/items/item_758898_6/component/file_775891/content) for more details.

```
"versioning": true
```

### citationGuidelineUrl

*Type: String • Cardinality: ONE*

The URL of the data source providing information on how to cite its items. The DataCite citation format is recommended ([http://www.datacite.org/whycitedata](http://www.datacite.org/whycitedata)).

This field only applies for re3data data source; see [re3data schema specification](https://gfzpublic.gfz-potsdam.de/rest/items/item_758898_6/component/file_775891/content) for more details.

```
"citationGuidelineUrl": "https://physionet.org/about/#citation"
```

### pidSystems

*Type: String • Cardinality: ONE*

The persistent identifier system that is used by the data source. As defined by re3data.org.

```
"pidSystems": "hdl"
```

### certificates

*Type: String • Cardinality: ONE*

The certificate, seal or standard the data source complies with. As defined by re3data.org.

```
"certificates": "WDS"
```

### policies

*Type: String • Cardinality: MANY*

Policies of the data source, as defined in OpenDOAR.

### journal

*Type: [Container](https://graph.openaire.eu/docs/data-model/entities/other#container) • Cardinality: ONE*

Information about the journal, if this data source is of type Journal.

```
"journal": {    "edition": "",    "iss": "5",    "issnLinking": "",    "issnOnline": "1873-7625",    "issnPrinted":"2451-8271",    "name": "Recent Patents and Topics on Imaging",    "sp": "12",    "ep": "22",    "vol": "50"}
```

### missionStatementUrl

*Type: String • Cardinality: ONE*

The URL of a mission statement describing the designated community of the data source. As defined by re3data.org

```
"missionStatementUrl": "https://www.sigma2.no/content/nird-research-data-archive"
```

[

](https://graph.openaire.eu/docs/data-model/entities/research-product)


# -------------------------------------------------------
#
# C:\dev\AIREloom\reference\official_docs\data_model\entities\organization.md
#
# ------------------------------------------------------

# "Organizations | OpenAIRE Graph Documentation"

(Source)["https://graph.openaire.eu/docs/data-model/entities/organization"]

Organizations include companies, research centers or institutions involved as project partners or as responsible of operating data sources. Information about organizations are collected from funder databases like CORDA, registries of data sources like OpenDOAR and re3Data, and CRIS systems, as being related to projects or data sources.

---

## The `Organization` object

### id

*Type: String • Cardinality: ONE*

The OpenAIRE id for the organization, created according to the [OpenAIRE entity identifier and PID mapping policy](https://graph.openaire.eu/docs/data-model/pids-and-identifiers).

```
"id": "openorgs____::b84450f9864182c67b8611b5593f4250"
```

### legalShortName

*Type: String • Cardinality: ONE*

The legal name in short form of the organization.

```
"legalShortName": "ARC"
```

### legalName

*Type: String • Cardinality: ONE*

The legal name of the organization.

```
"legalName": "Athena Research and Innovation Center In Information Communication & Knowledge Technologies"
```

### alternativeNames

*Type: String • Cardinality: MANY*

Alternative names that identify the organization.

```
"alternativeNames": [    "Athena Research and Innovation Center In Information Communication & Knowledge Technologies",    "Athena RIC",    "ARC",    ...]
```

### websiteUrl

*Type: String • Cardinality: ONE*

The websiteurl of the organization.

```
"websiteUrl": "https://www.athena-innovation.gr/el/announce/pressreleases.html"
```

### country

*Type: [Country](https://graph.openaire.eu/docs/data-model/entities/other#country) • Cardinality: ONE*

The country where the organization is located.

```
"country":{    "code": "GR",    "label": "Greece"}
```

### pids

*Type: [OrganizationPid](https://graph.openaire.eu/docs/data-model/entities/other#organizationpid) • Cardinality: MANY*

The list of persistent identifiers for the organization.

```
"pids": [    {        "scheme": "ISNI",        "value": "0000 0004 0393 5688"    },    {         "scheme": "GRID",        "value": "grid.19843.37"    },    ...]
```

[

](https://graph.openaire.eu/docs/data-model/entities/data-source)


# -------------------------------------------------------
#
# C:\dev\AIREloom\reference\official_docs\data_model\entities\other_entities.md
#
# ------------------------------------------------------

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


# -------------------------------------------------------
#
# C:\dev\AIREloom\reference\official_docs\data_model\entities\project.md
#
# ------------------------------------------------------


# "Projects | OpenAIRE Graph Documentation"

(Source)[https://graph.openaire.eu/docs/data-model/entities/project]

Of crucial interest to OpenAIRE is also the identification of the funders (e.g. European Commission, WellcomeTrust, FCT Portugal, NWO The Netherlands) that co-funded the projects that have led to a given research product. Projects are characterized by a list of funding streams (e.g. FP7, H2020 for the EC), which identify the strands of fundings. Funding streams can be nested to form a tree of sub-funding streams.

---

## The `Project` object

### id

*Type: String • Cardinality: ONE*

Main entity identifier, created according to the [OpenAIRE entity identifier and PID mapping policy](https://graph.openaire.eu/docs/data-model/pids-and-identifiers).

```
"id": "corda__h2020::70ea22400fd890c5033cb31642c4ae68"
```

### code

*Type: String • Cardinality: ONE*

Τhe grant agreement code of the project.

```
"code": "777541"
```

### acronym

*Type: String • Cardinality: ONE*

Project's acronym.

```
"acronym": "OpenAIRE-Advance"
```

### title

*Type: String • Cardinality: ONE*

Project's title.

```
"title": "OpenAIRE Advancing Open Scholarship"
```

### callIdentifier

*Type: String • Cardinality: ONE*

The identifier of the research call.

```
"callIdentifier": "H2020-EINFRA-2017"\`
```

### fundings

*Type: [Funding](https://graph.openaire.eu/docs/data-model/entities/other#funding) • Cardinality: MANY*

Funding information for the project.

```
"fundings": [    {        "fundingStream": {            "description": "Horizon 2020 Framework Programme - Research and Innovation action",            "id": "EC::H2020::RIA"        },        "jurisdiction": "EU",        "name": "European Commission",        "shortName": "EC"    }]
```

### granted

*Type: [Grant](https://graph.openaire.eu/docs/data-model/entities/other#grant) • Cardinality: ONE*

The money granted to the project.

```
"granted": {    "currency": "EUR",    "fundedAmount": 1.0E7,    "totalCost": 1.0E7}
```

### h2020Programmes

*Type: [H2020Programme](https://graph.openaire.eu/docs/data-model/entities/other#h2020programme) • Cardinality: MANY*

The H2020 programme funding the project.

```
"h2020Programmes":[    {        "code": "H2020-EU.1.4.1.3.",        "description": "Development, deployment and operation of ICT-based e-infrastructures"    }]
```

### keywords

*Type: String • Cardinality: ONE*

```
"keywords": "Aquaculture,NMR,Metabolomics,Microbiota,..."
```

### openAccessMandateForDataset

*Type: Boolean • Cardinality: ONE*

```
"openAccessMandateForDataset": true
```

### openAccessMandateForPublications

*Type: Boolean • Cardinality: ONE*

```
"openAccessMandateForPublications": true
```

### startDate

*Type: String • Cardinality: ONE*

The start year of the project.

```
"startDate": "2018-01-01"
```

### endDate

*Type: String • Cardinality: ONE*

The end year pf the project.

```
"endDate": "2021-02-28"
```

### subjects

*Type: String • Cardinality: MANY*

The subjects of the project

```
"subjects": [    "Data and Distributed Computing e-infrastructures for Open Science",    ...]
```

### summary

*Type: String • Cardinality: ONE*

Short summary of the project.

```
"summary": "OpenAIRE-Advance continues the mission of OpenAIRE to support the Open Access/Open Data mandates in Europe. By sustaining the current successful infrastructure, comprised of a human network and robust technical services, it consolidates its achievements while working to shift the momentum among its communities to Open Science, aiming to be a trusted e-Infrastructurewithin the realms of the European Open Science Cloud.In this next phase, OpenAIRE-Advance strives to empower its National Open Access Desks (NOADs) so they become a pivotal part within their own national data infrastructures, positioningOA and open science onto national agendas. The capacity building activities bring together experts ontopical task groups in thematic areas(open policies, RDM, legal issues, TDM), promoting a train the trainer approach, strengthening and expanding the pan-European Helpdesk with support and training toolkits, training resources and workshops.It examines key elements of scholarly communication, i.e., co-operative OA publishing and next generation repositories, to develop essential building blocks of the scholarly commons.On the technical level OpenAIRE-Advance focuses on the operation and maintenance of the OpenAIRE technical TRL8/9 services,and radically improvesthe OpenAIRE services on offer by: a) optimizing their performance and scalability, b) refining their functionality based on end-user feedback, c) repackagingthem into products, taking a professional marketing approach  with well-defined KPIs, d)consolidating the range of services/products into a common e-Infra catalogue to enable a wider uptake.OpenAIRE-Advancesteps up its outreach activities with concrete pilots with three major RIs,citizen science initiatives, and innovators via a rigorous Open Innovation programme. Finally, viaits partnership with COAR, OpenAIRE-Advance consolidatesOpenAIRE’s global roleextending its collaborations with Latin America, US, Japan, Canada, and Africa."
```

### websiteUrl

*Type: String • Cardinality: ONE*

The website of the project

```
"websiteUrl": "https://www.openaire.eu/advance/"
```



# -------------------------------------------------------
#
# C:\dev\AIREloom\reference\official_docs\data_model\entities\research_product.md
#
# ------------------------------------------------------

---
title: "Research products | OpenAIRE Graph Documentation"
source: "https://graph.openaire.eu/docs/data-model/entities/research-product"
author:
published:
created: 2025-03-21
description: "Research products are intended as digital objects, described by metadata, resulting from a scientific process."
tags:
  - "clippings"
---
## The `ResearchProduct` object

### id

*Type: String • Cardinality: ONE*

Main entity identifier, created according to the [OpenAIRE entity identifier and PID mapping policy](https://graph.openaire.eu/docs/data-model/pids-and-identifiers).

```
"id": "doi_dedup___::80f29c8c8ba18c46c88a285b7e739dc3"
```

### type

*Type: String • Cardinality: ONE*

Type of the research products. Possible types:

- `publication`
- `data`
- `software`
- `other`

as declared in the terms from the [dnet:result\_typologies vocabulary](https://api.openaire.eu/vocabularies/dnet:result_typologies).

```
"type": "publication"
```

### originalIds

*Type: String • Cardinality: MANY*

Identifiers of the record at the original sources.

```
"originalIds": [    "oai:pubmedcentral.nih.gov:8024784",    "S0048733321000305",    "10.1016/j.respol.2021.104226",    "3136742816"]
```

### mainTitle

*Type: String • Cardinality: ONE*

A name or title by which a research product is known. It may be the title of a publication or the name of a piece of software.

```
"mainTitle": "The fall of the innovation empire and its possible rise through open science"
```

### subTitle

*Type: String • Cardinality: ONE*

Explanatory or alternative name by which a research product is known.

```
"subTitle": "An analysis of cases from 1980 - 2020"
```

### authors

*Type: [Author](https://graph.openaire.eu/docs/data-model/entities/other#author) • Cardinality: MANY*

The main researchers involved in producing the data, or the authors of the publication.

```
"authors": [    {        "fullName": "E. Richard Gold",        "rank": 1,         "name": "Richard",        "surname": "Gold",        "pid": {            "id": {                "scheme": "orcid",                "value": "0000-0002-3789-9238"             },            "provenance": {                "provenance": "Harvested",                "trust": "0.9"             }        }    },     ...]
```

### bestAccessRight

*Type: [BestAccessRight](https://graph.openaire.eu/docs/data-model/entities/other#bestaccessright) • Cardinality: ONE*

The most open access right associated to the manifestations of this research product.

```
"bestAccessRight": {    "code": "c_abf2",    "label": "OPEN",    "scheme": "http://vocabularies.coar-repositories.org/documentation/access_rights/"}
```

### contributors

*Type: String • Cardinality: MANY*

The institution or person responsible for collecting, managing, distributing, or otherwise contributing to the development of the resource.

```
"contributors": [    "University of Zurich",    "Wright, Aidan G C",    "Hallquist, Michael",     ...]
```

### countries

*Type: [ResultCountry](https://graph.openaire.eu/docs/data-model/entities/other#resultcountry) • Cardinality: MANY*

Country associated with the research product: it is the country of the organisation that manages the institutional repository or national aggregator or CRIS system from which this record was collected. Country of affiliations of authors can be found instead in the affiliation relation.

```
"countries": [    {        "code": "CH",        "label": "Switzerland",        "provenance": {            "provenance": "Inferred by OpenAIRE",            "trust": "0.85"        }    },     ...]
```

### coverages

*Type: String • Cardinality: MANY*

### dateOfCollection

*Type: String • Cardinality: ONE*

When OpenAIRE collected the record the last time.

```
"dateOfCollection": "2021-06-09T11:37:56.248Z"
```

### descriptions

*Type: String • Cardinality: MANY*

A brief description of the resource and the context in which the resource was created.

```
"descriptions": [    "Open science partnerships (OSPs) are one mechanism to reverse declining efficiency. OSPs are public-private partnerships that openly share publications, data and materials.",    "There is growing concern that the innovation system's ability to create wealth and attain social benefit is declining in effectiveness. This article explores the reasons for this decline and suggests a structure, the open science partnership, as one mechanism through which to slow down or reverse this decline.",    "The article examines the empirical literature of the last century to document the decline. This literature suggests that the cost of research and innovation is increasing exponentially, that researcher productivity is declining, and, third, that these two phenomena have led to an overall flat or declining level of innovation productivity.",     ...]
```

### embargoEndDate

*Type: String • Cardinality: ONE*

Date when the embargo ends and this research product turns Open Access.

```
"embargoEndDate": "2017-01-01"
```

### indicators

*Type: [Indicator](https://graph.openaire.eu/docs/data-model/entities/other#indicator-1) • Cardinality: ONE*

The indicators computed for this research product; currently, the following types of indicators are supported:

- [Citation-based impact indicators by BIP!](https://graph.openaire.eu/docs/data-model/entities/other#citationimpact)
- [Usage Statistics indicators](https://graph.openaire.eu/docs/data-model/entities/other#usagecounts)

```
"indicators": {        "citationImpact": {                "influence": 123,                "influenceClass": "C2",                "citationCount": 456,                "citationClass": "C3",                "popularity": 234,                "popularityClass": "C1",                "impulse": 987,                "impulseClass": "C3"        },        "usageCounts": {                "downloads": "10",                 "views": "20"        }}
```

### instances

*Type: [Instance](https://graph.openaire.eu/docs/data-model/entities/other#instance) • Cardinality: MANY*

Specific materialization or version of the research product. For example, you can have one research product with three instances: one is the pre-print, one is the post-print, one is the published version.

```
"instances": [    {        "accessRight": {            "code": "c_abf2",            "label": "OPEN",            "openAccessRoute": "gold",            "scheme": "http://vocabularies.coar-repositories.org/documentation/access_rights/"        },        "alternateIdentifiers": [            {                "scheme": "doi",                "value": "10.1016/j.respol.2021.104226"            },            ...        ],        "articleProcessingCharge": {            "amount": "4063.93",            "currency": "EUR"        },        "license": "http://creativecommons.org/licenses/by-nc/4.0",        "pids": [            {                "scheme": "pmc",                "value": "PMC8024784"            },            ...        ],                "publicationDate": "2021-01-01",        "refereed": "UNKNOWN",        "type": "Article",        "urls": [            "http://europepmc.org/articles/PMC8024784"        ]    },    ...]
```

### language

*Type: [Language](https://graph.openaire.eu/docs/data-model/entities/other#language) • Cardinality: ONE*

The alpha-3/ISO 639-2 code of the language. Values controlled by the [dnet:languages vocabulary](https://api.openaire.eu/vocabularies/dnet:languages).

```
"language": {    "code": "eng",    "label": "English"}
```

### lastUpdateTimeStamp

*Type: Long • Cardinality: ONE*

Timestamp of last update of the record in OpenAIRE.

```
"lastUpdateTimeStamp": 1652722279987
```

### pids

*Type: [ResultPid](https://graph.openaire.eu/docs/data-model/entities/other#resultpid) • Cardinality: MANY*

Persistent identifiers of the research product. See also the [OpenAIRE entity identifier and PID mapping policy](https://graph.openaire.eu/docs/data-model/pids-and-identifiers) to learn more.

```
"pids": [    {        "scheme": "pmc",        "value": "PMC8024784"    },    {        "scheme": "doi",        "value": "10.1016/j.respol.2021.104226"    },    ...]
```

### publicationDate

*Type: String • Cardinality: ONE*

Main date of the research product: typically the publication or issued date. In case of a research product with different versions with different dates, the date of the research product is selected as the most frequent well-formatted date. If not available, then the most recent and complete date among those that are well-formatted. For statistics, the year is extracted and the research product is counted only among the research products of that year. Example: Pre-print date: 2019-02-03, Article date provided by repository: 2020-02, Article date provided by Crossref: 2020, OpenAIRE will set as date 2019-02-03, because it’s the most recent among the complete and well-formed dates. If then the repository updates the metadata and set a complete date (e.g. 2020-02-12), then this will be the new date for the research product because it becomes the most recent most complete date. However, if OpenAIRE then collects the pre-print from another repository with date 2019-02-03, then this will be the “winning date” because it becomes the most frequent well-formatted date.

```
"publicationDate": "2021-03-18"
```

### publisher

*Type: String • Cardinality: ONE*

The name of the entity that holds, archives, publishes prints, distributes, releases, issues, or produces the resource.

```
"publisher": "Elsevier, North-Holland Pub. Co"
```

### sources

*Type: String • Cardinality: MANY*

A related resource from which the described resource is derived. See definition of Dublin Core field [dc:source](https://www.dublincore.org/specifications/dublin-core/dcmi-terms/elements11/source).

```
"sources": [      "Research Policy",      "Crossref",      ...]
```

### formats

*Type: String • Cardinality: MANY*

The file format, physical medium, or dimensions of the resource.

```
"formats": [    "application/pdf",    "text/html",    ...]
```

### subjects

*Type: [Subject](https://graph.openaire.eu/docs/data-model/entities/other#subject) • Cardinality: MANY*

Subject, keyword, classification code, or key phrase describing the resource.

OpenAIRE classifies research products according to the [Field of Science](https://graph.openaire.eu/docs/graph-production-workflow/indicators-ingestion/fos-classification) and [Sustainable Development Goals](https://graph.openaire.eu/docs/graph-production-workflow/indicators-ingestion/sdg-classification) taxonomies. Check out the relative sections to know more.

```
"subjects": [    {        "subject": {            "scheme": "FOS",            "value": "01 natural sciences"        },        "provenance": {            "provenance": "inferred by OpenAIRE",            "trust": "0.85"        }    },    {        "subject": {            "scheme": "SDG",            "value": "2. Zero hunger"        },        "provenance": {            "provenance": "inferred by OpenAIRE",            "trust": "0.83"        }    },    {        "subject": {            "scheme": "keyword",            "value": "Open science"        },        "provenance": {            "provenance": "Harvested",            "trust": "0.9"        }    },    ...]
```

### isGreen

*Type: Boolean • Cardinality: ONE*

Indicates whether or not the scientific result was published following the green open access model.

### openAccessColor

*Type: String • Cardinality: ONE*

Indicates the specific open access model used for the publication; possible value is one of `bronze, gold, hybrid`.

### isInDiamondJournal

*Type: Boolean • Cardinality: ONE*

Indicates whether or not the publication was published in a diamond journal.

### publiclyFunded

*Type: String • Cardinality: ONE*

Discloses whether the publication acknowledges grants from public sources.

---

## Sub-types

There are the following sub-types of `Result`. Each inherits all its fields and extends them with the following.

### Publication

Metadata records about research literature (includes types of publications listed [here](http://api.openaire.eu/vocabularies/dnet:result_typologies/publication)).

#### container

*Type: [Container](https://graph.openaire.eu/docs/data-model/entities/other#container) • Cardinality: ONE*

Container has information about the conference or journal where the research product has been presented or published.

```
"container": {    "edition": "",    "iss": "5",    "issnLinking": "",    "issnOnline": "1873-7625",    "issnPrinted": "0048-7333",    "name": "Research Policy",    "sp": "12",    "ep": "22",    "vol": "50"}
```

### Data

Metadata records about research data (includes the subtypes listed [here](http://api.openaire.eu/vocabularies/dnet:result_typologies/dataset)).

#### size

*Type: String • Cardinality: ONE*

The declared size of the research data.

```
"size": "10129818"
```

#### version

*Type: String • Cardinality: ONE*

The version of the research data.

```
"version": "v1.3"
```

#### geolocations

*Type: [GeoLocation](https://graph.openaire.eu/docs/data-model/entities/other#geolocation) • Cardinality: MANY*

The list of geolocations associated with the research data.

```
"geolocations": [    {        "box": "18.569386 54.468973  18.066832 54.83707",        "place": "Tübingen, Baden-Württemberg, Southern Germany",        "point": "7.72486 50.1084"    },    ...]
```

### Software

Metadata records about research software (includes the subtypes listed [here](http://api.openaire.eu/vocabularies/dnet:result_typologies/software)).

#### documentationUrls

*Type: String • Cardinality: MANY*

The URLs to the software documentation.

```
"documentationUrls": [     "https://github.com/openaire/iis/blob/master/README.markdown",    ...]
```

#### codeRepositoryUrl

*Type: String • Cardinality: ONE*

The URL to the repository with the source code.

```
"codeRepositoryUrl": "https://github.com/openaire/iis"
```

#### programmingLanguage

*Type: String • Cardinality: ONE*

The programming language.

```
"programmingLanguage": "Java"
```

### Other research product

Metadata records about research products that cannot be classified as research literature, data or software (includes types of products listed [here](http://api.openaire.eu/vocabularies/dnet:result_typologies/other)).

#### contactPeople

*Type: String • Cardinality: MANY*

Information on the person responsible for providing further information regarding the resource.

```
"contactPeople": [    "Noémie Dominguez",    ...    ]
```

#### contactGroups

*Type: String • Cardinality: MANY*

Information on the group responsible for providing further information regarding the resource.

```
"contactGroups": [    "Networked Multimedia Information Systems (NeMIS)",    ...]
```

#### tools

*Type: String • Cardinality: MANY*

Information about tool useful for the interpretation and/or re-use of the research product.


# -------------------------------------------------------
#
# C:\dev\AIREloom\reference\official_docs\data_model\relationship.md
#
# ------------------------------------------------------


# The Relationship object | OpenAIRE Graph Documentation
(Source)[https://graph.openaire.eu/docs/data-model/relationships/relationship-object]

A relationship in the Graph is represented with the data type presented in this page, which aims to model a directed edge between two nodes, providing information about its semantics, provenance and validation.

This doc is separate from the 'base entities', which can be found in the /entities subfolder. 

### source

*Type: String • Cardinality: ONE*

OpenAIRE identifier of the node in the graph.

```
"source": "openorgs____::1cb75a3ad756e4c83e455e3e7347643b"
```

### sourceType

*Type: String • Cardinality: ONE*

Graph node type.

```
"sourceType": "organization"
```

### target

*Type: String • Cardinality: ONE*

OpenAIRE identifier of the node in the graph.

```
"target": "doajarticles::022409068174087a003647ff46070f7f"
```

### targetType

*Type: String • Cardinality: ONE*

Graph node type.

```
"target": "datasource"
```

### relType

*Type: [RelType](https://graph.openaire.eu/docs/data-model/relationships/#the-reltype-object) • Cardinality: ONE*

Represent the semantics of the relationship between two nodes of the graph.

```
"relType": {    "name": "provides",    "type": "provision"}
```

### provenance

*Type: [Provenance](https://graph.openaire.eu/docs/data-model/entities/other#provenance-1) • Cardinality: ONE*

Indicates the process that produced (or provided) the information.

```
"provenance": {    "provenance": "Harvested",    "trust":"0.900"}
```

### validated

*Type: Boolean • Cardinality: ONE*

Indicates weather or not the relationship was validated.

```
"validated": true
```

### validationDate

*Type: String • Cardinality: ONE*

Indicates the validation date of the relationship - applies only when the validated flag is set to true.

```
"validationDate": "2022-09-02"
```

---

## The `RelType` object

The RelType data type models the semantic of the relationship among two nodes.

### type

*Type: String • Cardinality: ONE*

The relationship category, e.g. affiliation, citation. (see [relationship types](https://graph.openaire.eu/docs/data-model/relationships/relationship-types)).

```
"name": "provides"
```

### name

*Type: String • Cardinality: ONE*

Further specifies the relationship semantic, indicating the relationship direction, e.g. Cites, isCitedBy.

```
"type": "provision"
```



# "Relationship types | OpenAIRE Graph Documentation"

(Source)[https://graph.openaire.eu/docs/data-model/relationships/relationship-types]

The following table lists all the possible relation semantics found in the Graph Dataset.

Note: the labels used to specify the semantic of the relationships are (for the large) inherited from the [DataCite metadata kernel](https://schema.datacite.org/meta/kernel-4.4/doc/DataCite-MetadataKernel_v4.4.pdf), which provides a description for them.

| # | Source entity type | Target entity type | Relation name / inverse | Provenance |
| --- | --- | --- | --- | --- |
| 1 | [Project](https://graph.openaire.eu/docs/data-model/entities/project) | [ResearchProduct](https://graph.openaire.eu/docs/data-model/entities/research-product) | produces / isProducedBy | Harvested, Inferred by OpenAIRE, Linked by user |
| 2 | [Project](https://graph.openaire.eu/docs/data-model/entities/project) | [Organization](https://graph.openaire.eu/docs/data-model/entities/organization) | hasParticipant / isParticipant | Harvested |
| 3 | [Project](https://graph.openaire.eu/docs/data-model/entities/project) | [Community](https://graph.openaire.eu/docs/data-model/entities/community) | IsRelatedTo / IsRelatedTo | Linked by user |
| 4 | [ResearchProduct](https://graph.openaire.eu/docs/data-model/entities/research-product) | [ResearchProduct](https://graph.openaire.eu/docs/data-model/entities/research-product) | IsAmongTopNSimilarDocuments / HasAmongTopNSimilarDocuments | Inferred by OpenAIRE |
| 5 | [ResearchProduct](https://graph.openaire.eu/docs/data-model/entities/research-product) | [ResearchProduct](https://graph.openaire.eu/docs/data-model/entities/research-product) | IsSupplementTo / IsSupplementedBy | Harvested |
| 6 | [ResearchProduct](https://graph.openaire.eu/docs/data-model/entities/research-product) | [ResearchProduct](https://graph.openaire.eu/docs/data-model/entities/research-product) | IsRelatedTo / IsRelatedTo | Harvested, Inferred by OpenAIRE, Linked by user |
| 7 | [ResearchProduct](https://graph.openaire.eu/docs/data-model/entities/research-product) | [ResearchProduct](https://graph.openaire.eu/docs/data-model/entities/research-product) | IsPartOf / HasPart | Harvested |
| 8 | [ResearchProduct](https://graph.openaire.eu/docs/data-model/entities/research-product) | [ResearchProduct](https://graph.openaire.eu/docs/data-model/entities/research-product) | IsDocumentedBy / Documents | Harvested |
| 9 | [ResearchProduct](https://graph.openaire.eu/docs/data-model/entities/research-product) | [ResearchProduct](https://graph.openaire.eu/docs/data-model/entities/research-product) | IsObsoletedBy / Obsoletes | Harvested |
| 10 | [ResearchProduct](https://graph.openaire.eu/docs/data-model/entities/research-product) | [ResearchProduct](https://graph.openaire.eu/docs/data-model/entities/research-product) | IsSourceOf / IsDerivedFrom | Harvested |
| 11 | [ResearchProduct](https://graph.openaire.eu/docs/data-model/entities/research-product) | [ResearchProduct](https://graph.openaire.eu/docs/data-model/entities/research-product) | IsCompiledBy / Compiles | Harvested |
| 12 | [ResearchProduct](https://graph.openaire.eu/docs/data-model/entities/research-product) | [ResearchProduct](https://graph.openaire.eu/docs/data-model/entities/research-product) | IsRequiredBy / Requires | Harvested |
| 13 | [ResearchProduct](https://graph.openaire.eu/docs/data-model/entities/research-product) | [ResearchProduct](https://graph.openaire.eu/docs/data-model/entities/research-product) | IsCitedBy / Cites | Harvested, Inferred by OpenAIRE |
| 14 | [ResearchProduct](https://graph.openaire.eu/docs/data-model/entities/research-product) | [ResearchProduct](https://graph.openaire.eu/docs/data-model/entities/research-product) | IsReferencedBy / References | Harvested |
| 15 | [ResearchProduct](https://graph.openaire.eu/docs/data-model/entities/research-product) | [ResearchProduct](https://graph.openaire.eu/docs/data-model/entities/research-product) | IsReviewedBy / Reviews | Harvested |
| 16 | [ResearchProduct](https://graph.openaire.eu/docs/data-model/entities/research-product) | [ResearchProduct](https://graph.openaire.eu/docs/data-model/entities/research-product) | IsOriginalFormOf / IsVariantFormOf | Harvested |
| 17 | [ResearchProduct](https://graph.openaire.eu/docs/data-model/entities/research-product) | [ResearchProduct](https://graph.openaire.eu/docs/data-model/entities/research-product) | IsVersionOf / HasVersion | Harvested |
| 18 | [ResearchProduct](https://graph.openaire.eu/docs/data-model/entities/research-product) | [ResearchProduct](https://graph.openaire.eu/docs/data-model/entities/research-product) | IsIdenticalTo / IsIdenticalTo | Harvested |
| 19 | [ResearchProduct](https://graph.openaire.eu/docs/data-model/entities/research-product) | [ResearchProduct](https://graph.openaire.eu/docs/data-model/entities/research-product) | IsPreviousVersionOf / IsNewVersionOf | Harvested |
| 20 | [ResearchProduct](https://graph.openaire.eu/docs/data-model/entities/research-product) | [ResearchProduct](https://graph.openaire.eu/docs/data-model/entities/research-product) | IsContinuedBy / Continues | Harvested |
| 21 | [ResearchProduct](https://graph.openaire.eu/docs/data-model/entities/research-product) | [ResearchProduct](https://graph.openaire.eu/docs/data-model/entities/research-product) | IsDescribedBy / Describes | Harvested |
| 22 | [ResearchProduct](https://graph.openaire.eu/docs/data-model/entities/research-product) | [Organization](https://graph.openaire.eu/docs/data-model/entities/organization) | hasAuthorInstitution / isAuthorInstitutionOf | Harvested, Inferred by OpenAIRE |
| 23 | [ResearchProduct](https://graph.openaire.eu/docs/data-model/entities/research-product) | [Data source](https://graph.openaire.eu/docs/data-model/entities/data-source) | isHostedBy / hosts | Harvested, Inferred by OpenAIRE |
| 24 | [ResearchProduct](https://graph.openaire.eu/docs/data-model/entities/research-product) | [Data source](https://graph.openaire.eu/docs/data-model/entities/data-source) | isProvidedBy / provides | Harvested |
| 25 | [ResearchProduct](https://graph.openaire.eu/docs/data-model/entities/research-product) | [Community](https://graph.openaire.eu/docs/data-model/entities/community) | IsRelatedTo / IsRelatedTo | Harvested, Inferred by OpenAIRE, Linked by user |
| 26 | [Organization](https://graph.openaire.eu/docs/data-model/entities/organization) | [Community](https://graph.openaire.eu/docs/data-model/entities/community) | IsRelatedTo / IsRelatedTo | Linked by user |
| 27 | [Organization](https://graph.openaire.eu/docs/data-model/entities/organization) | [Organization](https://graph.openaire.eu/docs/data-model/entities/organization) | IsChildOf / IsParentOf | Linked by user |
| 28 | [Data source](https://graph.openaire.eu/docs/data-model/entities/data-source) | [Community](https://graph.openaire.eu/docs/data-model/entities/community) | IsRelatedTo / IsRelatedTo | Linked by user |
| 29 | [Data source](https://graph.openaire.eu/docs/data-model/entities/data-source) | [Organization](https://graph.openaire.eu/docs/data-model/entities/organization) | isProvidedBy / provides | Harvested |




# -------------------------------------------------------
#
# C:\dev\AIREloom\reference\official_docs\auth.md
#
# ------------------------------------------------------

The OpenAIRE APIs can be accessed over HTTPS both by authenticated and non authenticated requests. You can use authenticated requests to increase the rate limit of your requests (please refer [here](https://graph.openaire.eu/docs/apis/terms#authentication--limits) for the current API rate limits). There are 2 main modes that you can use to authenticate API requests:

- [Personal access tokens](https://graph.openaire.eu/docs/apis/#personal-access-token)
- [Registered services](https://graph.openaire.eu/docs/apis/#registered-services)

In the following, we elaborate on these modes.

## Personal access token[​](https://graph.openaire.eu/docs/apis/#personal-access-token "Direct link to heading")

To access the OpenAIRE APIs with better rate limits you can use your personal access token. To have access to the following functionalities you need to login to OpenAIRE. In case you are not already a member you will need to register first and provide your [Personal information](https://develop.openaire.eu/personal-info).

New!

The registration process has been updated! In order to visit the Personal Token and Registered Services functionalities you need to fill in the Personal Information form available [here](https://develop.openaire.eu/personal-info). This update will not affect the operation of your existing services. However, if you want to register a new service or access/modify an existing one, you will need to provide your personal information first.

### How to create your personal access token[​](https://graph.openaire.eu/docs/apis/#how-to-create-your-personal-access-token "Direct link to heading")

To create your personal access token go to [your personal access token page](https://develop.openaire.eu/personal-token) and copy it!

info

Your access token is valid for an hour.

caution

Do not share your personal access token. Send your personal access token over HTTPS.

### How to use your personal access token[​](https://graph.openaire.eu/docs/apis/#how-to-use-your-personal-access-token "Direct link to heading")

To access the OpenAIRE APIs send your personal access token using the Authorization header.

```
GET https://api.openaire.eu/{resourceServicePath}Authorization: Bearer {ACCESS_TOKEN}
```

### An hour is not enough? What to do.[​](https://graph.openaire.eu/docs/apis/#an-hour-is-not-enough-what-to-do "Direct link to heading")

To prolong your access to our APIs you can use a **refresh token** that allows you to programmatically issue a new access token.

To get your refresh tokeng go to [your personal access token page](https://develop.openaire.eu/personal-token) and click the **"Get a refresh token"** button to get your refresh token.

OpenAIRE refresh token expires after 1 month.

In case you already have a refresh token a new one will be issued and the old one will no longer be valid.

Please copy your refresh token and store it confidentially. You will not be able to retrieve it. Do not share your refresh token. Send your refresh token over HTTPS.

Since the OpenAIRE refresh token expires after one month, when a client gets a refresh token, this token must be stored securely to keep it from being used by potential attackers. If a refresh token is leaked, it may be used to obtain new access tokens and access protected resources until a new one is issued or it expires.

To get a personal access token using your refresh token you need to make the following request:

```
GET https://services.openaire.eu/uoa-user-management/api/users/getAccessToken?refreshToken={your_refresh_token}
```

The response has the following format:

```
{     "access_token": "...",    "token_type": "Bearer",    "refresh_token": "...",    "expires_in": "...",    "scope": "...",    "id_token": "..."}
```

## Registered services[​](https://graph.openaire.eu/docs/apis/#registered-services "Direct link to heading")

If you have a service (client) that you want to interact with the OpenAIRE APIs you need to register it.

info

You can register up to 5 services.

We offer two ways of authenticting your service: the Basic Authentication and the Advanced Authentication.

### Which one is for me?[​](https://graph.openaire.eu/docs/apis/#which-one-is-for-me "Direct link to heading")

|  | How | Client Credential Issuer | Authentication Method |
| --- | --- | --- | --- |
| **Basic** | Client ID & Client Secret | OpenAIRE AAI server | Client Secret (Basic) |
| **Advanced** | Private Key signed JWT | Service owner | Private Key JWT Client Authentication |

For the **Basic Authentication** method the OpenAIRE AAI server generates a pair of *Client ID* and *Client Secret* credentials for your service upon its registration. The service sends the client id and client secret when authenticating to the OpenAIRE AAI Server to obtain the access token for the OpenAIRE APIs. The OpenAIRE AAI server checks whether the client id and client secret sent is valid. [Continue reading for the Basic Authentication](https://graph.openaire.eu/docs/apis/#basic-service-authentication-and-registration).

For the **Advanced Authentication** method your service does not send a client secret but it uses a *self signed client assertion* to authenticate to the OpenAIRE AAI server in order to obtain the access token for the OpenAIRE APIs. The client assertion is a JWT that must be signed with RSASSA using SHA-256 hash algorithm. The OpenAIRE AAI server validates the client assertion using the public key that you have provided upon the service registration. [Continue reading for the Advanced Authentication](https://graph.openaire.eu/docs/apis/#advanced-service-authentication-and-registration).

info

The Advanced Authentication method allows the OpenAIRE AAI server to verify that the client authentication request at the token endpoint was signed by your service and not altered in any way. This is more computation intensive compared to the Basic Authentication but it ensures non-repudiation. On the other hand, the Basic Authentication is more lightweight and easy to deploy but it does not provide signature verification, and there is always a possibility of the Client ID/secret credentials being stolen. Note that tThe Advanced authentication method gives a higher level of security to the process as long as it is used correctly, i.e. when the signed JWT has a short duration. When the duration of the JWT is long, the process is no different from the basic one.

### Basic service authentication and registration[​](https://graph.openaire.eu/docs/apis/#basic-service-authentication-and-registration "Direct link to heading")

To have access to the following functionalities you need to login to OpenAIRE. In case you are not already a member you will need to register first and provide your [Personal information](https://develop.openaire.eu/personal-info).

New!

The registration process has been updated! In order to visit the Personal Token and Registered Services functionalities you need to fill in the Personal Information form available [here](https://develop.openaire.eu/personal-info). This update will not affect the operation of your existing services. However, if you want to register a new service or access/modify an existing one, you will need to provide your personal information first.

For the **Basic Authentication** method the OpenAIRE AAI server generates a pair of *Client ID* and *Client Secret* for your service upon its registration. The service uses the client id and client secret to obtain the access token for the OpenAIRE APIs. The OpenAIRE AAI server checks whether the client id and client secret sent is valid.

#### How to register your service[​](https://graph.openaire.eu/docs/apis/#how-to-register-your-service "Direct link to heading")

To register your service you need to:

1. Go to your [Registered Services](https://develop.openaire.eu/apis) page and click the **\+ New Service** button.
2. Provide the mandatory information for your service.
3. Select the **Basic** Security level.
4. Click the **Create** button.

Once your service is created, the *Client ID* and *Client Secret* will appear on your screen. Click "OK" and your new service will be appear in the list of your [Registered Services](https://develop.openaire.eu/apis) page.

#### How to make a request[​](https://graph.openaire.eu/docs/apis/#how-to-make-a-request "Direct link to heading")

##### Step 1. Request for an access token[​](https://graph.openaire.eu/docs/apis/#step-1-request-for-an-access-token "Direct link to heading")

To make an access token request use the *Client ID* and *Client Secret* of your service.

```
curl -u {CLIENT_ID}:{CLIENT_SECRET} \-X POST 'https://aai.openaire.eu/oidc/token' \-d 'grant_type=client_credentials'
```

where **{CLIENT\_ID}** and **{CLIENT\_SECRET}** are the *Client ID* and *Client Secret* assigned to your service upon registration.

The response is:

```
{    "access_token": ...,    "token_type": "Bearer",    "expires_in": ...}
```

Store the access token confidentially on the service side.

##### Step 2. Make a request[​](https://graph.openaire.eu/docs/apis/#step-2-make-a-request "Direct link to heading")

To access the OpenAIRE APIs send the access token returned in **Step 1**.

```
GET https://api.openaire.eu/{resourceServicePath}Authorization: Bearer {ACCESS_TOKEN}
```

### Advanced service authentication and registration[​](https://graph.openaire.eu/docs/apis/#advanced-service-authentication-and-registration "Direct link to heading")

To have access to the following functionalities you need to login to OpenAIRE. In case you are not already a member you will need to register first and provide your [Personal information](https://develop.openaire.eu/personal-info).

New!

The registration process has been updated! In order to visit the Personal Token and Registered Services functionalities you need to fill in the Personal Information form available [here](https://develop.openaire.eu/personal-info). This update will not affect the operation of your existing services. However, if you want to register a new service or access/modify an existing one, you will need to provide your personal information first.

For the **Advanced Authentication** method your service does not send a client secret but it uses a *self signed client assertion* to obtain the access token for the OpenAIRE APIs. The client assertion is a JWT that must be signed with RSASSA using SHA-256 hash algorithm. The OpenAIRE AAI server validates the client assertion using the public key that you have provided upon the service registration.

#### Prepare to register your service[​](https://graph.openaire.eu/docs/apis/#prepare-to-register-your-service "Direct link to heading")

Before you register your service you need to prepare a pair of a private key and a public key on your side.

info

We accept keys signed with RSASSA using SHA-256 hash algorithm.

To create the key pair you have the following options:

- Use OpenAIRE authorization server built in tool. You can access the service here: [https://aai.openaire.eu/oidc/generate-oidc-keystore](https://aai.openaire.eu/oidc/generate-oidc-keystore).  
	The response is your **Public and Private Keypair** and has the following format:
	```
	{     "p" : ...,    "kty" : "RSA",    "q" : ...,    "d" : ...,    "e" : "AQAB",    "kid" : ...,    "qi" : ...,     "dp" : ...,     "alg" : "RS256",    "dq" : ...,    "n" : ....}
	```
	Use the public key parameters (kty, e, kid, alg, n) to create your **Public Key** in the following format:
	```
	{    "kty": "RSA",    "e": "AQAB",    "kid": ...,    "alg": "RS256",    "n": ...}
	```

info

Store both the **Public and Private keypair** and the **Public key**. You will need them to register your service.

caution

Store the **Public and Private keypair** confidentially on the service side.

- Use openssl and then convert the keys to jwk format using PEM to JWK scripts, such as [https://github.com/danedmunds/pem-to-jwk](https://github.com/danedmunds/pem-to-jwk). Alternatively, the client application can read the key pair in PEM format and then convert them, using JWK libraries. Use the public key parameters (kty, e, kid, alg, n) to the service registration.

info

You can also provide a public key in JWK format that can be accessed using a link.

#### How to register your service[​](https://graph.openaire.eu/docs/apis/#how-to-register-your-service-1 "Direct link to heading")

To register your service you need to:

1. Go to your [Registered Services](https://develop.openaire.eu/apis) page and click the **\+ New Service** button.
2. Provide the mandatory information for your service.
3. Select the **Advanced** Security level.
4. Use the public key parameters (kty, e, kid, alg, n) you previously produced to declare your **"Public Key"** **"By value"** in the following format:
	```
	{    "kty": "RSA",    "e": "AQAB",    "kid": ...,    "alg": "RS256",    "n": ...}
	```
	**\- OR -**
	If your service has a public key in JWK format that can be accessed using a link, you can set **“Public Key”** to **“By URL”**.
5. Click the **Create** button.

Once your service is created it will appear in the list of your [Registered Services](https://develop.openaire.eu/apis) page, with the **Service Id** that was automatically assigned to it by the AAI OpenAIRE service.

#### How to make a request[​](https://graph.openaire.eu/docs/apis/#how-to-make-a-request-1 "Direct link to heading")

##### Step 1. Create and sign a JWT[​](https://graph.openaire.eu/docs/apis/#step-1-create-and-sign-a-jwt "Direct link to heading")

Your service must create and sign a JWT and include it in the request to token endpoint as described in the [OpenID Connect Core 1.0, 9. Client Authentication](https://openid.net/specs/openid-connect-core-1_0.html#ClientAuthentication).

To create a JWT you can use [https://mkjose.org/](https://mkjose.org/). To do so you need to create a **payload** that should contain the following claims:

```
{    "iss": "{SERVICE_ID}",    "sub": "{SERVICE_ID}",    "aud": "https://aai.openaire.eu/oidc/token",    "jti": "{RANDOM_STRING}",    "exp": {EXPIRATION_TIME_OF_SIGNED_JWT}                            }
```

- **iss**, *(required)* the “issuer” claim identifies the principal that issued the JWT. The value is the **Service Id** that was created when you registered your service.
- **sub**, *(required)* the “subject” claim identifies the principal that is the subject of the JWT. The value is the **Service Id** that was created when you registered your service.
- aud, *(required)* the “audience” claim identifies the recipients that the JWT is intended for. The value is **[https://aai.openaire.eu/oidc/token](https://aai.openaire.eu/oidc/token)**\>.
- **jti**, *(required)* The “JWT ID” claim provides a unique identifier for the JWT. The value is a random string.
- **exp**, *(required)* the “expiration time” claim identifies the expiration time on or after which the JWT **MUST NOT** be accepted for processing. The value is a timestamp in **epoch format**.

Fill in the payload in the form available at [https://mkjose.org/](https://mkjose.org/), select the Signing Algorithm to be **RS256 using SHA-256** and paste the **Public and Private Keypair** previously created.

To check your JWT you can go to [https://jwt.io/](https://jwt.io/). The **header** should contain the following claims:

```
{    "alg": "RS256",    "kid": ...}
```

where **kid** is the one of your **Public and Private Keypair** you used to sign the JWT in **Step 1**.

caution

Store the signed key confidentially on the service side. You will need it in Step 2.

##### Step 2. Request for an access token[​](https://graph.openaire.eu/docs/apis/#step-2-request-for-an-access-token "Direct link to heading")

To make an access token request use the *signed JWT* that you created in **Step 1**. The OpenAIRE AAI server will check if the signed JWT is valid using the public key that you declared in the **"How to register your service"** process.

```
curl -k -X POST "https://aai.openaire.eu/oidc/token" \    -d "grant_type=client_credentials" \    -d "client_assertion_type=urn:ietf:params:oauth:client-assertion-type:jwt-bearer" \    -d "client_assertion={signedJWT}"
```

where **{signedJWT}** is the signed JWT created in **Step 1**.

The response is:

```
{    "access_token": {ACCESS_TOKEN}    "token_type":"Bearer",    "expires_in": ...,    "scope":"openid"}
```

Store the access token confidentially on the service side.

##### Step 3. Make a request[​](https://graph.openaire.eu/docs/apis/#step-3-make-a-request "Direct link to heading")

To access the OpenAIRE APIs send the access token returned in **Step 2**.

```
GET https://test.openaire.eu/{resourceServicePath}    Authorization: Bearer {ACCESS_TOKEN}
```

[

Previous

](https://graph.openaire.eu/docs/apis/terms)


# -------------------------------------------------------
#
# C:\dev\AIREloom\reference\official_docs\filtering.md
#
# ------------------------------------------------------

Version: 10.2.0

## Filtering search results

Filters can be used to narrow down the search results based on specific criteria. Filters are provided as query parameters in the request URL (see [here](https://graph.openaire.eu/docs/apis/graph-api/searching-entities/) for the available search entpoints).

Multiple filters can be provided in a single request; they should be formatted as follows:`param1=value1&param2=value2&...&paramN=valueN`.

Examples:

- Get all research products that contain the word `"covid"`, sorted by popularity in descending order:
	[https://api.openaire.eu/graph/v1/researchProducts?search=covid&sortBy=popularity DESC](https://api.openaire.eu/graph/v1/researchProducts?search=covid&sortBy=popularity%20DESC)
- Get all publications that are published after `2019-01-01`:
	[https://api.openaire.eu/graph/v1/researchProducts?type=publication&fromPublicationDate=2019-01-01](https://api.openaire.eu/graph/v1/researchProducts?type=publication&fromPublicationDate=2019-01-01)
- Get the organization with the ROR id `https://ror.org/0576by029`:
	[https://api.openaire.eu/graph/v1/organizations?pid=https://ror.org/0576by029](https://api.openaire.eu/graph/v1/organizations?pid=https://ror.org/0576by029)

## Available parameters

This section provides an overview of the available parameters for each entity type.

### Research products

The following query parameters are available for research products:

| **Parameter** | **Description** |
| --- | --- |
| **search** | Search in the content of the research product. |
| **mainTitle** | Search in the research product's main title. |
| **description** | Search in the research product's description. |
| **id** | The OpenAIRE id of the research product. |
| **pid** | The persistent identifier of the research product. |
| **originalId** | The identifier of the record at the original sources. |
| **type** | The type of the research product. One of `publication`, `dataset`, `software`, or `other` |
| **fromPublicationDate** | Gets the research products whose publication date is greater than or equal to the given date. A date formatted as `ΥΥΥΥ` or `YYYY-MM-DD` |
| **toPublicationDate** | Gets the research products whose publication date is less than or equal to the given date. A date formatted as `YYYY` or `YYYY-MM-DD` |
| **subjects** | List of subjects associated to the research product. |
| **countryCode** | The country code for the country associated with the research product. |
| **authorFullName** | The full name of the authors involved in producing this research product. |
| **authorOrcid** | The ORCiD of the authors involved in producing this research product. |
| **publisher** | The name of the entity that holds, archives, publishes prints, distributes, releases, issues, or produces the resource. |
| **bestOpenAccessRightLabel** | The best open access rights among the research product's instances. One of `OPEN SOURCE`, `OPEN`, `EMBARGO`, `RESTRICTED`, `CLOSED`, `UNKNOWN` |
| **influenceClass** | Citation-based indicator that reflects the overall impact of a research product. Please, choose a class among `C1`, `C2`, `C3`, `C4`, or `C5` for top 0.01%, top 0.1%, top 1%, top 10%, and average in terms of influence respectively. |
| **impulseClass** | Citation-based indicator that reflects the initial momentum of a research product directly after its publication. Please, choose a class among `C1`, `C2`, `C3`, `C4`, or `C5` for top 0.01%, top 0.1%, top 1%, top 10%, and average in terms of impulse respectively |
| **popularityClass** | Citation-based indicator that reflects current impact or attention of a research product. Please, choose a class among `C1`, `C2`, `C3`, `C4`, or `C5` for top 0.01%, top 0.1%, top 1%, top 10%, and average in terms of popularity respectively. |
| **citationCountClass** | Citation-based indicator that reflects the overall impact of a research product by summing all its citations. Please, choose a class among `C1`, `C2`, `C3`, `C4`, or `C5` for top 0.01%, top 0.1%, top 1%, top 10%, and average in terms of citation count respectively. |
| **instanceType** `[Only for publications]` | Retrieve publications of the given instance type. Check [here](http://api.openaire.eu/vocabularies/dnet:publication_resource) for all possible instance type values. |
| **sdg** `[Only for publications]` | Retrieves publications classified with the respective Sustainable Development Goal number. Integer in the range \[1, 17\] |
| **fos** `[Only for publications]` | Retrieves publications classified with a given Field of Science (FOS). A FOS classification identifier (see [here](https://explore.openaire.eu/assets/common-assets/vocabulary/fos.json) for details). |
| **isPeerReviewed** `[Only for publications]` | Indicates whether the publications are peerReviewed or not. (Boolean) |
| **isInDiamondJournal** `[Only for publications]` | Indicates whether the publication was published in a diamond journal or not. (Boolean) |
| **isPubliclyFunded** `[Only for publications]` | Indicates whether the publication was publicly funded or not. (Boolean) |
| **isGreen** `[Only for publications]` | Indicates whether the publication was published following the green open access model. (Boolean) |
| **openAccessColor** `[Only for publications]` | Specifies the Open Access color of the publication. One of `bronze`, `gold`, or `hybrid` |
| **relOrganizationId** | Retrieve research products connected to the organization (with OpenAIRE id). |
| **relCommunityId** | Retrieve research products connected to the community (with OpenAIRE id). |
| **relProjectId** | Retrieve research products connected to the project (with OpenAIRE id). |
| **relProjectCode** | Retrieve research products connected to the project with code. |
| **hasProjectRel** | Retrieve research products that are connected to a project. (Boolean) |
| **relProjectFundingShortName** | Retrieve research products connected to a project that has a funder with the given short name. |
| **relProjectFundingStreamId** | Retrieve research products connected to a project that has the given funding identifier. |
| **relHostingDataSourceId** | Retrieve research products hosted by the data source (with OpenAIRE id). |
| **relCollectedFromDatasourceId** | Retrieve research products collected from the data source (with OpenAIRE id). |
| **debugQuery** | Retrieve debug information for the search query. (Boolean) |
| **page** | Page number of the results. (Integer) |
| **pageSize** | Number of results per page. Integer in the range \[1, 100\] |
| **cursor** | Cursor-based pagination. Initial value: `cursor=*` |
| **sortBy** | The field to set the sorting order of the results. Should be provided in the format `fieldname sortDirection`, where the `sortDirection` can be either `ASC` for ascending order or `DESC` for descending order and `fielaname` is one of `relevance`, `publicationDate`, `dateOfCollection`, `influence`, `popularity`, `citationCount`, `impulse`. Multiple sorting parameters should be comma-separated. |

### Organizations

The following query parameters are available for organizations:

| **Parameter** | **Description** |
| --- | --- |
| **search** | Search in the content of the organization. |
| **legalName** | The legal name of the organization. |
| **legalShortName** | The legal name of the organization in short form. |
| **id** | The OpenAIRE id of the organization. |
| **pid** | The persistent identifier of the organization. |
| **countryCode** | The country code of the organization. |
| **relCommunityId** | Retrieve organizations connected to the community (with OpenAIRE id). |
| **relCollectedFromDatasourceId** | Retrieve organizations collected from the data source (with OpenAIRE id). |
| **debugQuery** | Retrieve debug information for the search query. |
| **page** | Page number of the results. |
| **pageSize** | Number of results per page. |
| **cursor** | Cursor-based pagination. Initial value: `cursor=*` |
| **sortBy** | The field to set the sorting order of the results. Should be provided in the format `fieldname sortDirection`, where the `sortDirection` can be either `ASC` for ascending order or `DESC` for descending order - organizations can only be sorted by `relevance`. |

### Data sources

The following query parameters are available for data sources:

| **Parameter** | **Description** |
| --- | --- |
| **search** | Search in the content of the data source. |
| **officialName** | The official name of the data source. |
| **englishName** | The English name of the data source. |
| **legalShortName** | The legal name of the organization in short form. |
| **id** | The OpenAIRE id of the data source. |
| **pid** | The persistent identifier of the data source. |
| **subjects** | List of subjects associated to the datasource. |
| **dataSourceTypeName** | The data source type; see all possible values [here](https://api.openaire.eu/vocabularies/dnet:datasource_typologies). |
| **contentTypes** | Types of content in the data source, as defined by OpenDOAR. |
| **relOrganizationId** | Retrieve data sources connected to the organization (with OpenAIRE id). |
| **relCommunityId** | Retrieve data sources connected to the community (with OpenAIRE id). |
| **relCollectedFromDatasourceId** | Retrieve data sources collected from the data source (with OpenAIRE id). |
| **debugQuery** | Retrieve debug information for the search query. |
| **page** | Page number of the results. |
| **pageSize** | Number of results per page. |
| **cursor** | Cursor-based pagination. Initial value: `cursor=*` |
| **sortBy** | The field to set the sorting order of the results. Should be provided in the format `fieldname sortDirection`, where the `sortDirection` can be either `ASC` for ascending order or `DESC` for descending order - data sources can only be sorted by `relevance`. |

### Projects

The following query parameters are available for projects:

| **Parameter** | **Description** |
| --- | --- |
| **search** | Search in the content of the projects. |
| **title** | Search in the project's title. |
| **keywords** | The project's keywords. |
| **id** | The OpenAIRE id of the project. |
| **code** | The grant agreement (GA) code of the project. |
| **acronym** | Project's acronym. |
| **callIdentifier** | The identifier of the research call. |
| **fundingShortName** | The short name of the funder. |
| **fundingStreamId** | The identifier of the funding stream. |
| **fromStartDate** | Gets the projects with start date greater than or equal to the given date. Please provide a date formatted as `YYYY` or `YYYY-MM-DD`. |
| **toStartDate** | Gets the projects with start date less than or equal to the given date. Please provide a date formatted as `YYYY` or `YYYY-MM-DD`. |
| **fromEndDate** | Gets the projects with end date greater than or equal to the given date. Please provide a date formatted as `YYYY` or `YYYY-MM-DD`. |
| **toEndDate** | Gets the projects with end date less than or equal to the given date. Please provide a date formatted as `YYYY` or `YYYY-MM-DD`. |
| **relOrganizationName** | The name or short name of the related organization. |
| **relOrganizationId** | The organization identifier of the related organization. |
| **relCommunityId** | Retrieve projects connected to the community (with OpenAIRE id). |
| **relOrganizationCountryCode** | The country code of the related organizations. |
| **relCollectedFromDatasourceId** | Retrieve projects collected from the data source (with OpenAIRE id). |
| **debugQuery** | Retrieve debug information for the search query. |
| **page** | Page number of the results. |
| **pageSize** | Number of results per page. |
| **cursor** | Cursor-based pagination. Initial value: `cursor=*` |
| **sortBy** | The field to set the sorting order of the results. Should be provided in the format `fieldname sortDirection`, where the `sortDirection` can be either `ASC` for ascending order or `DESC` for descending order and `fielaname` is one of `relevance`, `startDate`, `endDate`. Multiple sorting parameters should be comma-separated. |

## Using logical operators

The API supports the use of logical operators `AND`, `OR`, and `NOT` to refine your search queries. These operators help you combine or exclude one or more values for a specific filter.

### AND operator

Use the `AND` operator to retrieve results that include all specified values. This narrows your search.

Examples:

- Get research products that contain both `"climate"` and `"change"`:
	[https://api.openaire.eu/graph/v1/researchProducts?search=climate AND change](https://api.openaire.eu/graph/v1/researchProducts?search=climate%20AND%20change)
- Get research products that are classified with both Fields of Study (FOS) `"03 medical and health sciences"` and `"0502 economics and business"`:
	[https://api.openaire.eu/graph/v1/researchProducts?fos="03 medical and health sciences" AND "0502 economics and business"](https://api.openaire.eu/graph/v1/researchProducts?fos=%2203%20medical%20and%20health%20sciences%22%20AND%20%220502%20economics%20and%20business%22)

### OR operator

Use the `OR` operator to retrieve results that include any of the specified terms. This broadens your search. The same functionality can be achieved by providing multiple times the same query parameter or using a comma to separate the values.

Examples:

- Get research products with the OpenAIRE ids `doi_dedup___::2b3cb7130c506d1c3a05e9160b2c4108` or `pmid_dedup__::1591ebf0e0698ed4a99455ff2ba4adc0`:
	[https://api.openaire.eu/graph/v1/researchProducts?id=r3730f562f9e::539da48b3796663b17e6166bb966e5b1 OR pmid\_dedup\_\_::1591ebf0e0698ed4a99455ff2ba4adc0](https://api.openaire.eu/graph/v1/researchProducts?id=r3730f562f9e::539da48b3796663b17e6166bb966e5b1%20OR%20pmid_dedup__::1591ebf0e0698ed4a99455ff2ba4adc0)
- Get projects that are connected to organizations in the US or Greece:
	[https://api.openaire.eu/graph/v1/projects?relOrganizationCountryCode=US OR GR](https://api.openaire.eu/graph/v1/projects?relOrganizationCountryCode=US%20OR%20GR)
	or by using the same query parameter multiple times: [https://api.openaire.eu/graph/v1/projects?relOrganizationCountryCode=US&relOrganizationCountryCode=GR](https://api.openaire.eu/graph/v1/projects?relOrganizationCountryCode=US&relOrganizationCountryCode=GR)
	or just using comma: [https://api.openaire.eu/graph/v1/projects?relOrganizationCountryCode=US,GR](https://api.openaire.eu/graph/v1/projects?relOrganizationCountryCode=US,GR)

### NOT operator

Use the `NOT` operator to exclude specific terms from your search results. This refines your search by filtering out unwanted results.

Examples:

- Get research products that contain `"semantic"` but not `"web"`:
	[https://api.openaire.eu/graph/v1/researchProducts?search=semantic NOT web](https://api.openaire.eu/graph/v1/researchProducts?search=semantic%20NOT%20web)
- Get all data sources that are not journals:
	[https://api.openaire.eu/graph/v1/dataSources?dataSourceTypeName=NOT Journal](https://api.openaire.eu/graph/v1/dataSources?dataSourceTypeName=NOT%20Journal)


# -------------------------------------------------------
#
# C:\dev\AIREloom\reference\official_docs\requests.md
#
# ------------------------------------------------------

This guide provides examples of how to make requests to the OpenAIRE Graph API using different programming languages.

## Using `curl`[​](https://graph.openaire.eu/docs/apis/graph-api/#using-curl "Direct link to heading")

```bash
curl -X GET "https://api.openaire.eu/graph/v1/researchProducts?search=OpenAIRE%20Graph&type=publication&page=1&pageSize=10&sortBy=relevance%20DESC" -H "accept: application/json"
```

## Using Python (with `requests` library)[​](https://graph.openaire.eu/docs/apis/graph-api/#using-python-with-requests-library "Direct link to heading")

```python
import requestsurl = "https://api.openaire.eu/graph/v1/researchProducts"params = {    "search": "OpenAIRE Graph",    "type": "publication",    "page": 1,    "pageSize": 10,    "sortBy": "relevance DESC"}headers = {    "accept": "application/json"}response = requests.get(url, headers=headers, params=params)if response.status_code == 200:    data = response.json()    print(data)else:    print(f"Failed to retrieve data: {response.status_code}")
```

note

Note that when using `curl` you should ensure that the URL is properly encoded, especially when using special characters or spaces in the query parameters. On the contrary, the `requests` library in Python takes care of URL encoding automatically.


## Authentication & limits
The OpenAIRE APIs are free-to-use by any third-party service and can be accessed over HTTPS both by authenticated and unauthenticated requests. The rate limit for the former type of requests is up to 7200 requests per hour, while the latter is up to 60 requests per hour.

To make an authenticated request, you must first register. Then, you can go to the personal access token page in your account, copy your token and use it for up to one hour, find out more.

Our OAuth 2.0 implementation, conforms to the OpenID Connect specification, and is OpenID Certified. OpenID Connect is a simple identity layer on top of the OAuth 2.0 protocol. For more information about OAuth2.0 please visit the OAuth2.0 official site. For more information about OpenID Connect please visit the OpenID Connect official site. Also, check here for more information on our Privacy Policy.

### Quality of service
OpenAIRE API services are running in production 24/7 within the OpenAIRE infrastructure premises deployed at the data center facilities of the Interdisciplinary Centre for Mathematical and Computational Modelling (ICM).

### License
OpenAIRE Graph license is CC-BY: the records returned by the service can be freely re-used by commercial and non-commercial partners under CC-BY license, hence as long as OpenAIRE is acknowledged as a data source.


[

](https://graph.openaire.eu/docs/apis/graph-api/searching-entities/sorting-and-paging)


# -------------------------------------------------------
#
# C:\dev\AIREloom\reference\official_docs\scholexplorer_api.md
#
# ------------------------------------------------------

## API Overview[​](https://graph.openaire.eu/docs/apis/scholexplorer/#api-overview "Direct link to heading")

The Scholexplorer API is designed to help researchers, data scientists, and developers discover and navigate the relationships between research publications, datasets, software in the OpenAIRE Graph.

The OpenAIRE Graph gathers today the largest collection of relationships between all kinds of research outputs, providing a unique entry point merging the traditional space of citations between scientific articles, with the Open Science space of citations between publications, data, and software. Relationships are aggregated from OpenCitations.net, Crossref.org, DataCite.org and thousands of publication, data, software repositories world-wide. The collection is further expanded with the citation links text-mined by OpenAIRE over a pool of Open Access fullt-text counting today 65Mi entries (and growing).

The Scholexplorer API provide an unprecedented entry point that will enable deeper insights and a more comprehensive understanding of the citations within the research ecosystem.

## API Versions[​](https://graph.openaire.eu/docs/apis/scholexplorer/#api-versions "Direct link to heading")

The Scholexplorer API support the discovery of Scholix relationships filtering by the following parameters: source ID, target ID, semantics, publisher, entity type (publication, dataset, software, other), or publishing date. As of today, three API versions area available:

- [version 1.0](https://graph.openaire.eu/docs/apis/scholexplorer/v1/version)
- [version 2.0](https://graph.openaire.eu/docs/apis/scholexplorer/v2/version)
- [version 3.0](https://graph.openaire.eu/docs/apis/scholexplorer/v3/version)

While currently in beta, v3 is the future of the Scholexplorer API. It includes the latest features and improvements and will soon become the primary version, with v1 and v2 being phased out. We strongly recommend starting with v3 for any new development.

## Swagger API v3.0
The Scholexplorer version 3.0 APIs offer a Swagger entry point that allows access to all the relationships within the OpenAIRE graph.

The response format for requests to the Links endpoint complies with the Scholix Schema . The Scholix framework consists of a conceptual and information model containing standards, aspirational principles, practical guidelines, and options for encoding and exchange protocols to support linking between scholarly publications and related research data. It provides a standardized way of representing metadata related to these links, facilitating the exchange and integration of information about connections between publications, datasets, and other research entities. This allows for a more comprehensive and interoperable approach to understanding and exploring the relationships within the research landscape.

By using the Links endpoint and the Scholix response format, users can easily explore and analyze the relationships within the Scholixplorer graph, gaining a complete and detailed view of the connections between the various research resources.


Scholexplorer models relationships as links between pairs of research products, defined as **source** and **target**. Links are further characterized by the **type** of the two products (publication, dataset, software, or other), the **date** of publishing (typically the date of the source product), the **publisher** of the two products (a string), and the **PID** of the products (or the OpenAIRE ID, useful when the product does not come with a PID).

More specifically, here is the list of API parameters:

**Required parameters (at least one):**

- **sourcePid** Represents the unique identifier (PID) of the source entity in the relationship. This parameter is used to specify which entity is initiating or originating the relationship.
- **targetPid** Represents the unique identifier (PID) of the target entity in the relationship. This parameter is used to specify the entity that is receiving or being affected by the relationship.
- **sourcePublisher** Identifies the publisher of the source entity.
- **targetPublisher** Identifies the publisher of the target entity.
- **sourceType** The typology of the source entity like: Publication, Dataset, Software Other
- **targetType** The typology of the target entity like: Publication, Dataset, Software Other

**Optional parameters:**

- **relation** Defines the type of relationship between the source and target entities.
- **from**: Filter all relationships where the date is greater than or equal to the specified date
- **to**: Filter all relationships where the date is lower than or equal to the specified date

# "Scholix Schema 3.0 | OpenAIRE Graph Documentation"
(Source)[https://graph.openaire.eu/docs/apis/scholexplorer/v3/response_schema]

Below are the fields in the schema (aka the possible return values):

| **Field** | **Type** | **Description** |
| --- | --- | --- |
| `LinkPublicationDate` | `string` (date) | Date of the linking publication. |
| `LinkProvider[]` | `array` (object) | Information about the provider of the link. |
| `LinkProvider[].name` | `string` | Name of the Datasource provides links. |
| `LinkProvider[].identifier[]` | `array` (object) | Identifiers associated with the link provider. |
| `LinkProvider[].identifier[].ID` | `string` | Identifier value. |
| `LinkProvider[].identifier[].IDScheme` | `string` | Identifier scheme. |
| `LinkProvider[].identifier[].IDURL` | `string` (URI) | URL associated with the identifier. |
| `RelationshipType` | `object` | Semantic of relationship between scholarly objects. |
| `RelationshipType.Name` | `string` | Name of the relationship semantic should be one of the following values `("IsSupplementTo","IsSupplementedBy", "References", "IsReferencedBy", "IsRelatedTo")` |
| `RelationshipType.SubType` | `string` | Specific subtype of the relationship described [here](https://graph.openaire.eu/docs/data-model/relationships/relationship-types). |
| `RelationshipType.SubTypeSchema` | `string` (URI) | URL of the schema defining the relationship subtype. |
| `LicenseURL` | `string` (URI) | URL of the license associated with the data. |
| `Source` | `object` | Metadata of the source entity. |
| `Source.Identifier` | `array` (object) | Identifiers of the source entity. |
| `Source.Identifier[].ID` | `string` | Persistent Identifier value. |
| `Source.Identifier[].IDScheme` | `string` | Persistent Identifier scheme. |
| `Source.Identifier[].IDURL` | `string` (URI) | URL associated with the Persistent identifier. |
| `Source.Type` | `string` | entity type (publication, dataset, software, other). |
| `Source.SubType` | `string` | Specific subtype of entity (e.g., Article, Dataset). |
| `Source.Title` | `string` | Title of the entity. |
| `Source.Creator[]` | `array` (object) | Creators of the entity. |
| `Source.Creator[].Name` | `string` | Name of the creator. |
| `Source.Creator[].Identifier` | `object` | Persistent Identifier of the creator. |
| `Source.Creator[].Identifier.ID` | `string` | Persistent Identifier value. |
| `Source.Creator[].Identifier.IDScheme` | `string` | Identifier scheme. |
| `Source.Creator[].Identifier.IDURL` | `string` (URI) | URL associated with the Persistent identifier. |
| `Source.PublicationDate` | `string` (date) | Date of publication. |
| `Source.Publisher[]` | `array` (object) | Publishers of the Entity. |
| `Source.Publisher[].name` | `string` | Name of the publisher. |
| `Source.Publisher[].Identifier[]` | `object` | Persistent Identifier of the publisher. |
| `Source.Publisher[].Identifier[].ID` | `string` | Persistent Identifier value. |
| `Source.Publisher[].Identifier[].IDScheme` | `string` | Identifier scheme. |
| `Source.Publisher[].Identifier[].IDURL` | `string` (URI) | URL associated with the identifier. |
| `Target` | `object` | Metadata of the target entity |
| `Target.Identifier` | `array` (object) | Identifiers of the target entity. |
| `Target.Identifier[].ID` | `string` | Persistent Identifier value. |
| `Target.Identifier[].IDScheme` | `string` | Persistent Identifier scheme. |
| `Target.Identifier[].IDURL` | `string` (URI) | URL associated with the Persistent identifier. |
| `Target.Type` | `string` | entity type (publication, dataset, software, other). |
| `Target.SubType` | `string` | Specific subtype of entity (e.g., Article, Dataset). |
| `Target.Title` | `string` | Title of the entity. |
| `Target.Creator[]` | `array` (object) | Creators of the entity. |
| `Target.Creator[].Name` | `string` | Name of the creator. |
| `Target.Creator[].Identifier` | `object` | Persistent Identifier of the creator. |
| `Target.Creator[].Identifier.ID` | `string` | Persistent Identifier value. |
| `Target.Creator[].Identifier.IDScheme` | `string` | Identifier scheme. |
| `Target.Creator[].Identifier.IDURL` | `string` (URI) | URL associated with the Persistent identifier. |
| `Target.PublicationDate` | `string` (date) | Date of publication. |
| `Target.Publisher[]` | `array` (object) | Publishers of the Entity. |
| `Target.Publisher[].name` | `string` | Name of the publisher. |
| `Target.Publisher[].Identifier[]` | `object` | Persistent Identifier of the publisher. |
| `Target.Publisher[].Identifier[].ID` | `string` | Persistent Identifier value. |
| `Target.Publisher[].Identifier[].IDScheme` | `string` | Identifier scheme. |
| `Target.Publisher[].Identifier[].IDURL` | `string` (URI) | URL associated with the identifier. |


## Example uses
### 1\. Filter Relation by Semantic

The Scholixplorer APIs offer the ability to filter relationships by their semantics, using the relation parameter. This allows for finer control over the results obtained. It is important to note that all relationships are stored on the "*active side*" of the verb. For instance, the "*Cites*" relationship is recorded as "A cites B," and not as "B IsCitedBy A."  
To retrieve inverse relationships, those not represented by the active voice of the verb, the relation parameter alone is insufficient. The targetPid parameter must also be utilized in conjunction with relation.

The possible values for the semantic filter are:

- Cites
- IsSourceOf
- IsRelatedTo
- HasAmongTopNSimilarDocuments
- References
- HasPart
- IsSupplementTo
- IsNewVersionOf
- HasVersion
- Continues
- Documents
- IsIdenticalTo
- IsOriginalFormOf
- Reviews
- Compiles
- Obsoletes
- Describes
- Requires
- IsMetadataOf

#### Get all citations associated with a specific PID

The following example will return all citation to a specific PID

```bash
curl https://api-beta.scholexplorer.openaire.eu/v3/Links?targetPid=10.1007/s11356-023-25894-w&relation=Cites
```

```json
{  "currentPage": 0,  "totalLinks": 8,  "totalPages": 1,  "result": [    {      "RelationshipType": {        "Name": "IsRelatedTo",        "SubType": "cites",        "SubTypeSchema": "datacite"      },      "source": {        "Identifier": [          {            "ID": "10.1108/k-08-2023-1556",            "IDScheme": "doi",            "IDURL": "https://doi.org/10.1108/k-08-2023-1556"          },          {            "ID": "50|doi_________::368a80d3c098d7b866752a75f97f3aba",            "IDScheme": "openaireIdentifier",            "IDURL": null          }        ],        "Title": "Study on urban green development efficiency of Jiangsu, Zhejiang and Fujian in China: a mixed network SBM approach",        "Type": "literature",        "Creator": [          {            "name": "Dan Liu",            "identifier": [              {                "ID": "0000-0001-9655-9404",                "IDScheme": "orcid_pending",                "IDURL": null              }            ]          },          {            "name": "Tiange Liu",            "identifier": [              {                "ID": "0000-0003-2201-9661",                "IDScheme": "orcid_pending",                "IDURL": null              }            ]          },          {            "name": "Yuting Zheng",            "identifier": [              {                "ID": "0000-0003-4871-3299",                "IDScheme": "orcid_pending",                "IDURL": null              },              {                "ID": "0000-0003-4871-3299",                "IDScheme": "orcid",                "IDURL": null              }            ]          }        ],        "PublicationDate": "2024-05-15",        "Publisher": [          {            "name": "Kybernetes",            "identifier": [              {                "ID": "10|issn___print::802fba3b33fd96b1daf4235f3038adf7",                "IDScheme": "OpenAIRE Identifier",                "IDURL": null              }            ]          }        ]      },      "target": {        "Identifier": [          {            "ID": "10.1007/s11356-023-25894-w",            "IDScheme": "doi",            "IDURL": "https://doi.org/10.1007/s11356-023-25894-w"          },          {            "ID": "36869949",            "IDScheme": "pmid",            "IDURL": "https://pubmed.ncbi.nlm.nih.gov/36869949"          },          {            "ID": "50|doi_dedup___::34bf7dfe8dce5acc9fe32f2899fdf4b8",            "IDScheme": "openaireIdentifier",            "IDURL": null          }        ],        "Title": "The evolution and determinants of Chinese inter-provincial green development efficiency: an MCSE-DEA-Tobit-based perspective",        "Type": "literature",        "Creator": [          {            "name": "Lin, Yang",            "identifier": []          },          {            "name": "Zhanxin, Ma",            "identifier": [              {                "ID": "0000-0003-0185-1002",                "IDScheme": "orcid",                "IDURL": null              }            ]          },          {            "name": "Jie, Yin",            "identifier": [              {                "ID": "0009-0008-6335-7281",                "IDScheme": "orcid",                "IDURL": null              }            ]          },          {            "name": "Yiming, Li",            "identifier": []          },          {            "name": "Haodong, Lv",            "identifier": []          }        ],        "PublicationDate": "2023-03-04",        "Publisher": [          {            "name": "Environmental Science and Pollution Research",            "identifier": [              {                "ID": "10|issn___print::4b8f2549cf00fcb1f1c3f32634d506bf",                "IDScheme": "OpenAIRE Identifier",                "IDURL": null              }            ]          }        ]      },      "HarvestDate": "2024-05-15",      "LicenseURL": null,      "LinkProvider": [        {          "name": "Crossref",          "identifier": []        }      ],      "LinkPublicationDate": "2024-05-15"    },    ...
```


### 2\. Retrieve All Relations for a Persistent Identifier (PID)

This use case allows you to retrieve all connections associated with a specific research object identified by its PID. For example, you can find all datasets, software, and other research products related to a specific publication. As described in the [query parameters section](https://graph.openaire.eu/docs/apis/scholexplorer/v3/query_params) , you can specify the PID on either the source or target side of the relationships. Here are two examples to filter by each side of the relation:

#### Get all relations from a source PID

```bash
curl  https://api-beta.scholexplorer.openaire.eu/v3/Links?sourcePid=10.1007/s11356-023-25894-w
```

```json
{  "currentPage": 0,  "totalLinks": 46,  "totalPages": 1,  "result": [    {      "RelationshipType": {        "Name": "IsRelatedTo",        "SubType": "cites",        "SubTypeSchema": "datacite"      },      "source": {        "Identifier": [          {            "ID": "10.1007/s11356-023-25894-w",            "IDScheme": "doi",            "IDURL": "https://doi.org/10.1007/s11356-023-25894-w"          },          {            "ID": "36869949",            "IDScheme": "pmid",            "IDURL": "https://pubmed.ncbi.nlm.nih.gov/36869949"          },          {            "ID": "50|doi_dedup___::34bf7dfe8dce5acc9fe32f2899fdf4b8",            "IDScheme": "openaireIdentifier",            "IDURL": null          }        ],        "Title": "The evolution and determinants of Chinese inter-provincial green development efficiency: an MCSE-DEA-Tobit-based perspective",        "Type": "literature",        "Creator": [          {            "name": "Lin, Yang",            "identifier": []          },          {            "name": "Zhanxin, Ma",            "identifier": [              {                "ID": "0000-0003-0185-1002",                "IDScheme": "orcid",                "IDURL": null              }            ]          },          {            "name": "Jie, Yin",            "identifier": [              {                "ID": "0009-0008-6335-7281",                "IDScheme": "orcid",                "IDURL": null              }            ]          },          {            "name": "Yiming, Li",            "identifier": []          },          {            "name": "Haodong, Lv",            "identifier": []          }        ],        "PublicationDate": "2023-03-04",        "Publisher": [          {            "name": "Environmental Science and Pollution Research",            "identifier": [              {                "ID": "10|issn___print::4b8f2549cf00fcb1f1c3f32634d506bf",                "IDScheme": "OpenAIRE Identifier",                "IDURL": null              }            ]          }        ]      },      "target": {        "Identifier": [          {            "ID": "10.1016/j.jenvman.2021.113738",            "IDScheme": "doi",            "IDURL": "https://doi.org/10.1016/j.jenvman.2021.113738"          },          {            "ID": "34543964",            "IDScheme": "pmid",            "IDURL": "https://pubmed.ncbi.nlm.nih.gov/34543964"          },          {            "ID": "3199206491",            "IDScheme": "mag_id",            "IDURL": null          },          {            "ID": "10.1016/j.jenvman.2021.113738",            "IDScheme": "doi",            "IDURL": null          },          {            "ID": "50|doi_dedup___::c88441285a2df5560e515bf74338195e",            "IDScheme": "openaireIdentifier",            "IDURL": null          }        ],        "Title": "How industrial convergence affects regional green development efficiency: A spatial conditional process analysis",        "Type": "literature",        "Creator": [          {            "name": "Feng Dong",            "identifier": [              {                "ID": "0000-0002-5177-6453",                "IDScheme": "orcid_pending",                "IDURL": null              },              {                "ID": "0000-0002-5177-6453",                "IDScheme": "orcid",                "IDURL": null              }            ]          },          {            "name": "Yangfan Li",            "identifier": [              {                "ID": "0000-0001-7422-0004",                "IDScheme": "orcid",                "IDURL": null              }            ]          },          {            "name": "Chang Qin",            "identifier": []          },          {            "name": "Jiaojiao Sun",            "identifier": []          }        ],        "PublicationDate": "2021-12-01",        "Publisher": [          {            "name": "Journal of Environmental Management",            "identifier": [              {                "ID": "10|issn___print::1ef707b68adfcb67f0f5b78b34add1e1",                "IDScheme": "OpenAIRE Identifier",                "IDURL": null              }            ]          }        ]      },      "HarvestDate": "2023-03-04",      "LicenseURL": null,      "LinkProvider": [        {          "name": "Crossref",          "identifier": []        },        {          "name": "OpenCitations",          "identifier": []        }      ],      "LinkPublicationDate": "2023-03-04"    },    ...
```

#### Get all relations to a target PID

```bash
curl  https://api-beta.scholexplorer.openaire.eu/v3/Links?targetPid=10.1007/s11356-023-25894-w
```

```json
{  "currentPage": 0,  "totalLinks": 8,  "totalPages": 1,  "result": [    {      "RelationshipType": {        "Name": "IsRelatedTo",        "SubType": "cites",        "SubTypeSchema": "datacite"      },      "source": {        "Identifier": [          {            "ID": "10.1108/k-08-2023-1556",            "IDScheme": "doi",            "IDURL": "https://doi.org/10.1108/k-08-2023-1556"          },          {            "ID": "50|doi_________::368a80d3c098d7b866752a75f97f3aba",            "IDScheme": "openaireIdentifier",            "IDURL": null          }        ],        "Title": "Study on urban green development efficiency of Jiangsu, Zhejiang and Fujian in China: a mixed network SBM approach",        "Type": "literature",        "Creator": [          {            "name": "Dan Liu",            "identifier": [              {                "ID": "0000-0001-9655-9404",                "IDScheme": "orcid_pending",                "IDURL": null              }            ]          },          {            "name": "Tiange Liu",            "identifier": [              {                "ID": "0000-0003-2201-9661",                "IDScheme": "orcid_pending",                "IDURL": null              }            ]          },          {            "name": "Yuting Zheng",            "identifier": [              {                "ID": "0000-0003-4871-3299",                "IDScheme": "orcid_pending",                "IDURL": null              },              {                "ID": "0000-0003-4871-3299",                "IDScheme": "orcid",                "IDURL": null              }            ]          }        ],        "PublicationDate": "2024-05-15",        "Publisher": [          {            "name": "Kybernetes",            "identifier": [              {                "ID": "10|issn___print::802fba3b33fd96b1daf4235f3038adf7",                "IDScheme": "OpenAIRE Identifier",                "IDURL": null              }            ]          }        ]      },      "target": {        "Identifier": [          {            "ID": "10.1007/s11356-023-25894-w",            "IDScheme": "doi",            "IDURL": "https://doi.org/10.1007/s11356-023-25894-w"          },          {            "ID": "36869949",            "IDScheme": "pmid",            "IDURL": "https://pubmed.ncbi.nlm.nih.gov/36869949"          },          {            "ID": "50|doi_dedup___::34bf7dfe8dce5acc9fe32f2899fdf4b8",            "IDScheme": "openaireIdentifier",            "IDURL": null          }        ],        "Title": "The evolution and determinants of Chinese inter-provincial green development efficiency: an MCSE-DEA-Tobit-based perspective",        "Type": "literature",        "Creator": [          {            "name": "Lin, Yang",            "identifier": []          },          {            "name": "Zhanxin, Ma",            "identifier": [              {                "ID": "0000-0003-0185-1002",                "IDScheme": "orcid",                "IDURL": null              }            ]          },          {            "name": "Jie, Yin",            "identifier": [              {                "ID": "0009-0008-6335-7281",                "IDScheme": "orcid",                "IDURL": null              }            ]          },          {            "name": "Yiming, Li",            "identifier": []          },          {            "name": "Haodong, Lv",            "identifier": []          }        ],        "PublicationDate": "2023-03-04",        "Publisher": [          {            "name": "Environmental Science and Pollution Research",            "identifier": [              {                "ID": "10|issn___print::4b8f2549cf00fcb1f1c3f32634d506bf",                "IDScheme": "OpenAIRE Identifier",                "IDURL": null              }            ]          }        ]      },      "HarvestDate": "2024-05-15",      "LicenseURL": null,      "LinkProvider": [        {          "name": "Crossref",          "identifier": []        }      ],      "LinkPublicationDate": "2024-05-15"    },     ...
```

### 3\. Retrieve All Relations for a Publisher

This use case allows you to retrieve all the connections associated with a specific publisher. For example, you can find all the research outputs published by a specific organization and their interconnections. As described in the [query parameters section](https://graph.openaire.eu/docs/apis/scholexplorer/v3/query_params), you can specify the publisher on either the source or target side of the relationships. Here are two examples to filter by each side of the relation:

#### Get all relations from a source Publisher

The following example will return all relations where the source object is published in *Environmental Science and Pollution Research*

```bash
curl  https://api-beta.scholexplorer.openaire.eu/v3/Links?sourcePublisher=Environmental%20Science%20and%20Pollution%20Research
```

```json
{  "currentPage": 0,  "totalLinks": 662074307,  "totalPages": 6620744,  "result": [    {      "RelationshipType": {        "Name": "IsRelatedTo",        "SubType": "cites",        "SubTypeSchema": "datacite"      },      "source": {        "Identifier": [          {            "ID": "10.1016/j.envpol.2007.01.027",            "IDScheme": "doi",            "IDURL": "https://doi.org/10.1016/j.envpol.2007.01.027"          },          {            "ID": "17383782",            "IDScheme": "pmid",            "IDURL": "https://pubmed.ncbi.nlm.nih.gov/17383782"          },          {            "ID": "2103728545",            "IDScheme": "mag_id",            "IDURL": null          },          {            "ID": "10.1016/j.envpol.2007.01.027",            "IDScheme": "doi",            "IDURL": null          },          {            "ID": "50|doi_dedup___::a0b554380f893bccf88bbe4a4b4c32d7",            "IDScheme": "openaireIdentifier",            "IDURL": null          }        ],        "Title": "Demonstrating trend reversal of groundwater quality in relation to time of recharge determined by 3H/3He",        "Type": "literature",        "Creator": [          {            "name": "Ate Visser",            "identifier": [              {                "ID": "0000-0003-4048-4540",                "IDScheme": "orcid",                "IDURL": null              }            ]          },          {            "name": "Hans Peter Broers",            "identifier": [              {                "ID": "0000-0001-7156-7694",                "IDScheme": "orcid",                "IDURL": null              }            ]          },          {            "name": "Marc F. P. Bierkens",            "identifier": [              {                "ID": "0000-0002-7411-6562",                "IDScheme": "orcid",                "IDURL": null              }            ]          },          {            "name": "B. van der Grift",            "identifier": [              {                "ID": "0000-0003-4069-6703",                "IDScheme": "orcid",                "IDURL": null              }            ]          }        ],        "PublicationDate": "2007-08-01",        "Publisher": [          {            "name": "Environmental Pollution",            "identifier": [              {                "ID": "10|issn___print::6a69ef9b4914ebc44206556deed5180b",                "IDScheme": "OpenAIRE Identifier",                "IDURL": null              }            ]          },          {            "name": "Environmental Science and Pollution Research",            "identifier": [              {                "ID": "10|issn___print::4b8f2549cf00fcb1f1c3f32634d506bf",                "IDScheme": "OpenAIRE Identifier",                "IDURL": null              }            ]          }        ]      },      "target": {        "Identifier": [          {            "ID": "10.1029/wr025i006p01097",            "IDScheme": "doi",            "IDURL": "https://doi.org/10.1029/wr025i006p01097"          },          {            "ID": "2051481858",            "IDScheme": "mag_id",            "IDURL": null          },          {            "ID": "10.1029/wr025i006p01097",            "IDScheme": "doi",            "IDURL": "https://agupubs.onlinelibrary.wiley.com/doi/abs/10.1029/WR025i006p01097"          },          {            "ID": "50|doi_dedup___::9283c5d50b50daaf716cb1cb8c478964",            "IDScheme": "openaireIdentifier",            "IDURL": null          }        ],        "Title": "Tritium as an indicator of recharge and dispersion in a groundwater system in central Ontario",        "Type": "literature",        "Creator": [          {            "name": "William D. Robertson",            "identifier": []          },          {            "name": "John A. Cherry",            "identifier": []          }        ],        "PublicationDate": "1989-06-01",        "Publisher": [          {            "name": "Water Resources Research",            "identifier": [              {                "ID": "10|issn___print::ff3482a5fa102865b020642f90718b59",                "IDScheme": "OpenAIRE Identifier",                "IDURL": null              }            ]          }        ]      },      "HarvestDate": "2007-08-01",      "LicenseURL": null,      "LinkProvider": [        {          "name": "Microsoft Academic Graph",          "identifier": []        },        {          "name": "OpenCitations",          "identifier": []        }      ],      "LinkPublicationDate": "2007-08-01"    },...
```

#### Get all relations to a target Publisher

The following example will return all relations where the target object is published in *Environmental Science and Pollution Research*

```bash
curl  https://api-beta.scholexplorer.openaire.eu/v3/Links?targetPublisher=Environmental%20Science%20and%20Pollution%20Research
```

```json
{  "currentPage": 0,  "totalLinks": 685907234,  "totalPages": 6859073,  "result": [    {      "RelationshipType": {        "Name": "IsRelatedTo",        "SubType": "cites",        "SubTypeSchema": "datacite"      },      "source": {        "Identifier": [          {            "ID": "10.1039/c3em30955j",            "IDScheme": "doi",            "IDURL": "https://doi.org/10.1039/c3em30955j"          },          {            "ID": "23503885",            "IDScheme": "pmid",            "IDURL": "https://pubmed.ncbi.nlm.nih.gov/23503885"          },          {            "ID": "1963486219",            "IDScheme": "mag_id",            "IDURL": null          },          {            "ID": "10.1039/c3em30955j",            "IDScheme": "doi",            "IDURL": null          },          {            "ID": "50|doi_dedup___::495cc9e8e642d64a46900ab400b2e6d4",            "IDScheme": "openaireIdentifier",            "IDURL": null          }        ],        "Title": "Residence time as a key for comprehensive assessment of the relationship between changing land use and nitrates in regional groundwater systems",        "Type": "literature",        "Creator": [          {            "name": "Yingjie Cao",            "identifier": []          },          {            "name": "Yingjie Cao",            "identifier": []          },          {            "name": "Yinghua Zhang",            "identifier": []          },          {            "name": "Changming Liu",            "identifier": []          },          {            "name": "Changyuan Tang",            "identifier": []          },          {            "name": "Xianfang Song",            "identifier": []          }        ],        "PublicationDate": "2013-01-01",        "Publisher": [          {            "name": "Environmental Science Processes & Impacts",            "identifier": [              {                "ID": "10|issn___print::1a2de60262b1d65e546ca5acac39e019",                "IDScheme": "OpenAIRE Identifier",                "IDURL": null              }            ]          }        ]      },      "target": {        "Identifier": [          {            "ID": "10.1016/j.envpol.2007.01.027",            "IDScheme": "doi",            "IDURL": "https://doi.org/10.1016/j.envpol.2007.01.027"          },          {            "ID": "17383782",            "IDScheme": "pmid",            "IDURL": "https://pubmed.ncbi.nlm.nih.gov/17383782"          },          {            "ID": "2103728545",            "IDScheme": "mag_id",            "IDURL": null          },          {            "ID": "10.1016/j.envpol.2007.01.027",            "IDScheme": "doi",            "IDURL": null          },          {            "ID": "50|doi_dedup___::a0b554380f893bccf88bbe4a4b4c32d7",            "IDScheme": "openaireIdentifier",            "IDURL": null          }        ],        "Title": "Demonstrating trend reversal of groundwater quality in relation to time of recharge determined by 3H/3He",        "Type": "literature",        "Creator": [          {            "name": "Ate Visser",            "identifier": [              {                "ID": "0000-0003-4048-4540",                "IDScheme": "orcid",                "IDURL": null              }            ]          },          {            "name": "Hans Peter Broers",            "identifier": [              {                "ID": "0000-0001-7156-7694",                "IDScheme": "orcid",                "IDURL": null              }            ]          },          {            "name": "Marc F. P. Bierkens",            "identifier": [              {                "ID": "0000-0002-7411-6562",                "IDScheme": "orcid",                "IDURL": null              }            ]          },          {            "name": "B. van der Grift",            "identifier": [              {                "ID": "0000-0003-4069-6703",                "IDScheme": "orcid",                "IDURL": null              }            ]          }        ],        "PublicationDate": "2007-08-01",        "Publisher": [          {            "name": "Environmental Pollution",            "identifier": [              {                "ID": "10|issn___print::6a69ef9b4914ebc44206556deed5180b",                "IDScheme": "OpenAIRE Identifier",                "IDURL": null              }            ]          },          {            "name": "Environmental Science and Pollution Research",            "identifier": [              {                "ID": "10|issn___print::4b8f2549cf00fcb1f1c3f32634d506bf",                "IDScheme": "OpenAIRE Identifier",                "IDURL": null              }            ]          }        ]      },...
```

### 4\. Retrieve All Relations by typology of the entity

This use case allows you to retrieve all connections associated with a specific type of entity. For example, you can find all research outputs related to a publication, dataset, software, or other research typologies. As described in the [query parameters section](https://graph.openaire.eu/docs/apis/scholexplorer/v3/query_params), you can specify the filter on either the source or target side of the relationships. Here are two examples to filter by each side of the relation:

The possible values for the typology are:

- publication
- dataset
- software
- other

#### Get all relations from a publication
The following example will return all relations where the source object is a *publication*

```bash
curl  https://api-beta.scholexplorer.openaire.eu/v3/Links?sourceType=publication
```

```json
{  "currentPage": 0,  "totalLinks": -1986776433,  "totalPages": -19867763,  "result": [    {      "RelationshipType": {        "Name": "IsRelatedTo",        "SubType": "cites",        "SubTypeSchema": "datacite"      },      "source": {        "Identifier": [          {            "ID": "10.1016/j.geoderma.2014.02.022",            "IDScheme": "doi",            "IDURL": "https://doi.org/10.1016/j.geoderma.2014.02.022"          },          {            "ID": "10.1016/j.geoderma.2014.02.022",            "IDScheme": "doi",            "IDURL": null          },          {            "ID": "2035023866",            "IDScheme": "mag_id",            "IDURL": null          },          {            "ID": "20.500.14243/253435",            "IDScheme": "handle",            "IDURL": "https://hdl.handle.net/20.500.14243/253435"          },          {            "ID": "11577/2831516",            "IDScheme": "handle",            "IDURL": "https://hdl.handle.net/11577/2831516"          },          {            "ID": "50|doi_dedup___::fb2321e85affc9fbd892f5115634898b",            "IDScheme": "openaireIdentifier",            "IDURL": null          }        ],        "Title": "The impact of parent material, climate, soil type and vegetation on Venetian forest humus forms: A direct gradient approach",        "Type": "literature",        "Creator": [          {            "name": "Jean-François Ponge",            "identifier": [              {                "ID": "0000-0001-6504-5267",                "IDScheme": "orcid_pending",                "IDURL": null              },              {                "ID": "0000-0001-6504-5267",                "IDScheme": "orcid",                "IDURL": null              }            ]          },          {            "name": "Giacomo Sartori",            "identifier": []          },          {            "name": "Adriano Garlato",            "identifier": []          },          {            "name": "Fabrizio Ungaro",            "identifier": [              {                "ID": "0000-0003-0116-6611",                "IDScheme": "orcid_pending",                "IDURL": null              },              {                "ID": "0000-0003-0116-6611",                "IDScheme": "orcid",                "IDURL": null              }            ]          },          {            "name": "Augusto Zanella",            "identifier": [              {                "ID": "0000-0001-7066-779x",                "IDScheme": "orcid_pending",                "IDURL": null              },              {                "ID": "0000-0001-7066-779x",                "IDScheme": "orcid",                "IDURL": null              }            ]          },          {            "name": "Bernard Jabiol",            "identifier": []          },          {            "name": "Silvia Obber",            "identifier": []          }        ],        "PublicationDate": "2014-08-01",        "Publisher": [          {            "name": "Geoderma",            "identifier": [              {                "ID": "10|issn___print::12af254e77e895b470cf9ac4dafc47d9",                "IDScheme": "OpenAIRE Identifier",                "IDURL": null              }            ]          },          {            "name": "Hal",            "identifier": [              {                "ID": "10|openaire____::39e33d59918c2cb40d10ae244f1fe019",                "IDScheme": "OpenAIRE Identifier",                "IDURL": null              }            ]          },          {            "name": "CNR ExploRA",            "identifier": [              {                "ID": "10|openaire____::082404e0f6ecb6577f1760523598894c",                "IDScheme": "OpenAIRE Identifier",                "IDURL": null              }            ]          },          {            "name": "IRIS Cnr",            "identifier": [              {                "ID": "10|opendoar____::9f9d8edfbd4baab2060a115bbdcee1d6",                "IDScheme": "OpenAIRE Identifier",                "IDURL": null              }            ]          },          {            "name": "Hal-Diderot",            "identifier": [              {                "ID": "10|opendoar____::18bb68e2b38e4a8ce7cf4f6b2625768c",                "IDScheme": "OpenAIRE Identifier",                "IDURL": null              }            ]          },          {            "name": "Archivio istituzionale della ricerca - Università di Padova",            "identifier": [              {                "ID": "10|opendoar____::a22d33b4a00c165507a61f3bed4b5149",                "IDScheme": "OpenAIRE Identifier",                "IDURL": null              }            ]          },          {            "name": "HAL INRAE",            "identifier": [              {                "ID": "10|opendoar____::c7a9f13a6c0940277d46706c7ca32601",                "IDScheme": "OpenAIRE Identifier",                "IDURL": null              }            ]          },          {            "name": "Mémoires en Sciences de l'Information et de la Communication",            "identifier": [              {                "ID": "10|opendoar____::1534b76d325a8f591b52d302e7181331",                "IDScheme": "OpenAIRE Identifier",                "IDURL": null              }            ]          }        ]      },      "target": {        "Identifier": [          {            "ID": "10.1016/j.geomorph.2009.08.008",            "IDScheme": "doi",            "IDURL": "https://doi.org/10.1016/j.geomorph.2009.08.008"          },          {            "ID": "10.1016/j.geomorph.2009.08.008",            "IDScheme": "doi",            "IDURL": null          },          {            "ID": "10.5167/uzh-28909",            "IDScheme": "doi",            "IDURL": "https://dx.doi.org/10.5167/uzh-28909"          },          {            "ID": "1998447100",            "IDScheme": "mag_id",            "IDURL": null          },          {            "ID": "50|doi_dedup___::5c55d2a9be9268d0f0f1932f005c44d0",            "IDScheme": "openaireIdentifier",            "IDURL": null          }        ],        "Title": "The effects of exposure and climate on the weathering of late Pleistocene and Holocene Alpine soils",        "Type": "literature",        "Creator": [          {            "name": "Egli, M",            "identifier": [              {                "ID": "0000-0002-1528-3440",                "IDScheme": "orcid",                "IDURL": null              }            ]          },          {            "name": "Sartori, G",            "identifier": []          },          {            "name": "Mirabella, A",            "identifier": []          },          {            "name": "Giaccai, D",            "identifier": []          }        ],        "PublicationDate": "2010-01-01",        "Publisher": [          {            "name": "Geomorphology",            "identifier": [              {                "ID": "10|issn___print::ed5a370152cb6cafc3d5bff280a94c88",                "IDScheme": "OpenAIRE Identifier",                "IDURL": null              }            ]          },          {            "name": "Unknown Repository",            "identifier": [              {                "ID": "10|openaire____::55045bd2a65019fd8e6741a755395c8c",                "IDScheme": "OpenAIRE Identifier",                "IDURL": null              }            ]          },          {            "name": "Zurich Open Repository and Archive",            "identifier": [              {                "ID": "10|opendoar____::0efe32849d230d7f53049ddc4a4b0c60",                "IDScheme": "OpenAIRE Identifier",                "IDURL": null              }            ]          }        ]      },...
```

#### Get all relations to a dataset

The following example will return all relations where the target object type is a *dataset*

```bash
curl  https://api-beta.scholexplorer.openaire.eu/v3/Links?targetType=dataset
```

```json
{  "currentPage": 0,  "totalLinks": 1303573672,  "totalPages": 13035737,  "result": [    {      "RelationshipType": {        "Name": "IsRelatedTo",        "SubType": "isderivedfrom",        "SubTypeSchema": "datacite"      },      "source": {        "Identifier": [          {            "ID": "10.15468/dl.u5s8xu",            "IDScheme": "doi",            "IDURL": "https://dx.doi.org/10.15468/dl.u5s8xu"          },          {            "ID": "50|doi_________::0da3d4ab990ec74587aa0d4e5cd08cea",            "IDScheme": "openaireIdentifier",            "IDURL": null          }        ],        "Title": "Occurrence Download",        "Type": "dataset",        "Creator": [          {            "name": "GBIF.Org User",            "identifier": []          }        ],        "PublicationDate": "2024-01-01",        "Publisher": [          {            "name": "Global Biodiversity Information Facility",            "identifier": [              {                "ID": "10|re3data_____::194f60618405f8d2dc58ea68d968a104",                "IDScheme": "OpenAIRE Identifier",                "IDURL": null              }            ]          }        ]      },      "target": {        "Identifier": [          {            "ID": "10.15472/dhkstn",            "IDScheme": "doi",            "IDURL": "https://dx.doi.org/10.15472/dhkstn"          },          {            "ID": "50|doi_________::a7aff8a9d549a02c171f188b24b72890",            "IDScheme": "openaireIdentifier",            "IDURL": null          }        ],        "Title": "Plantación de árboles nativos con fines de restauración en el departamento de Cundinamarca, como parte de la iniciativa 180 millones de árboles nativos",        "Type": "dataset",        "Creator": [          {            "name": "Hernández, Luisa Fernanda Garzón",            "identifier": []          }        ],        "PublicationDate": "2021-01-01",        "Publisher": [          {            "name": "Unknown Repository",            "identifier": [              {                "ID": "10|openaire____::55045bd2a65019fd8e6741a755395c8c",                "IDScheme": "OpenAIRE Identifier",                "IDURL": null              }            ]          }        ]      },      "HarvestDate": "2024-01-01",      "LicenseURL": null,      "LinkProvider": [        {          "name": "Datacite",          "identifier": []        }      ],      "LinkPublicationDate": "2024-01-01"    },    {      "RelationshipType": {        "Name": "IsRelatedTo",        "SubType": "isderivedfrom",        "SubTypeSchema": "datacite"      },      "source": {        "Identifier": [          {            "ID": "10.15468/dl.bdr6pc",            "IDScheme": "doi",            "IDURL": "https://dx.doi.org/10.15468/dl.bdr6pc"          },          {            "ID": "50|doi_________::3cae8c2e04ec0fec9c1bbf7860b37f97",            "IDScheme": "openaireIdentifier",            "IDURL": null          }        ],        "Title": "Occurrence Download",        "Type": "dataset",        "Creator": [          {            "name": "GBIF.Org User",            "identifier": []          }        ],        "PublicationDate": "2024-01-01",        "Publisher": [          {            "name": "Global Biodiversity Information Facility",            "identifier": [              {                "ID": "10|re3data_____::194f60618405f8d2dc58ea68d968a104",                "IDScheme": "OpenAIRE Identifier",                "IDURL": null              }            ]          }        ]      },      "target": {        "Identifier": [          {            "ID": "10.15472/yziqrx",            "IDScheme": "doi",            "IDURL": "https://dx.doi.org/10.15472/yziqrx"          },          {            "ID": "50|doi_________::19f93c70a6c17c47d07748ac680abaaf",            "IDScheme": "openaireIdentifier",            "IDURL": null          }        ],        "Title": "Colecta de fauna y flora asociada al Estudio de Impacto Ambiental para la Variante Popayan, Cauca",        "Type": "dataset",        "Creator": [          {            "name": "Ortiz, Liz Anyury Lozano",            "identifier": []          }        ],        "PublicationDate": "2024-01-01",        "Publisher": [          {            "name": "Unknown Repository",            "identifier": [              {                "ID": "10|openaire____::55045bd2a65019fd8e6741a755395c8c",                "IDScheme": "OpenAIRE Identifier",                "IDURL": null              }            ]          }        ]      },...
```




# -------------------------------------------------------
#
# C:\dev\AIREloom\reference\official_docs\search_api.md
#
# ------------------------------------------------------

# Search API

The Search API allows developers to access metadata records of the OpenAIRE Graph by performing queries over research products (i.e., publications, data, software, other research products), and projects.

The API is intended for metadata discovery and exploration only, hence it does not provide access to the whole information space: the number of total results returned by one query is limited to 10,000.

For accessing the whole graph, developers are encouraged to use the OpenAIRE full Graph dataset.




## Endpoints[​](https://graph.openaire.eu/docs/apis/search-api/#endpoints "Direct link to heading")

For research products: [https://api.openaire.eu/search/researchProducts](https://api.openaire.eu/search/researchProducts)

By specific type:

- publications: [https://api.openaire.eu/search/publications](https://api.openaire.eu/search/publications)
- research data: [https://api.openaire.eu/search/datasets](https://api.openaire.eu/search/datasets)
- research software: [https://api.openaire.eu/search/software](https://api.openaire.eu/search/software)
- other research products: [https://api.openaire.eu/search/other](https://api.openaire.eu/search/other)

## General parameters[​](https://graph.openaire.eu/docs/apis/search-api/#general-parameters "Direct link to heading")

Endpoint: [https://api.openaire.eu/search/researchProducts](https://api.openaire.eu/search/researchProducts)

| Parameter | Option | Description |
| --- | --- | --- |
| page | integer | Page number of the search results. |
| size | integer | Number of results per page. |
| format | json \| xml \| csv \| tsv | The format of the response. The default is xml. |
| model | openaire \| sygma | The data model of the response. Default is openaire. Model sygma is a simplified version of the openaire model. For sygma, only the xml format is available. The relative XML schema is available [here](https://www.openaire.eu/schema/sygma/oaf_sygma_v2.1.xsd). |
| sortBy | `sortBy=field,[ascending\\|descending]`   **'field'** can one of: - `dateofcollection` - `resultstoragedate` - `resultstoragedate` - `resultembargoenddate` - `resultembargoendyear` - `resultdateofacceptance` - `resultacceptanceyear` - `influence` - `popularity` - `citationCount` - `impulse` Multiple sorting is supported by repeating the `sortBy` parameter. | The sorting order of the specified field. |
| hasECFunding | true \| false | If hasECFunding is true gets the entities funded by the EC. If hasECFunding is false gets the entities related to projects not funded by the EC. |
| hasWTFunding | true \| false | If hasWTFunding is true gets the entities funded by Wellcome Trust. The results are the same as those obtained with `funder=wt`. If hasWTFunding is false gets the entities related to projects not funded by Wellcome Trust. |
| funder | WT \| EC \| ARC \| ANDS \| NSF \| FCT \| NHMRC | Search for entities by funder. |
| fundingStream | ... | Search for entities by funding stream. |
| FP7scientificArea | ... | Search for FP7 entities by scientific area. |
| keywords | White-space separated list of keywords. | This parameter is used to support a keyword search functionality in various fields (e.g., for research products the keywords are used to search in the product’s title, description, authors, etc). Regarding the semantics, when you provide multiple keywords, all keywords should be present, hence the correct interpretation is `kwd1 AND kw2`. |
| doi | Comma separated list of DOIs.   Alternatively, it is possible to repeat the parameter for each requested doi. | Gets the research products with the given DOIs, if any. |
| orcid | Comma separated list of ORCID iDs of authors.   Alternatively, it is possible to repeat the parameter for each author ORCID iD. | Gets the research products linked to the given ORCID iD of an author, if any. |
| fromDateAccepted | Date formatted as `YYYY-MM-DD` | Gets the research products whose date of acceptance is greater than or equal the given date. |
| toDateAccepted | Date formatted as `YYYY-MM-DD` | Gets the research products whose date of acceptance is less than or equal the given date. |
| title | White-space separated list of keywords. | Gets the research products whose titles contain the given list of keywords. |
| author | White-space separated list of names and/or surnames. | Search for research products by authors. |
| OA | true \| false | If OA is true gets Open Access research products. If OA is false gets the non Open Access research products |
| projectID | The given grant identifier of the project | Search for research products of the project with the specified projectID |
| country | 2 letter country code | Search for research products associated to the country code |
| influence | Accepted values:   `C1` for top 0.01% in terms of influence   `C2` for top 0.1% in terms of influence   `C3` for top 1% in terms of influence   `C4` for top 10% in terms of influence   `C5` for average/low in terms of influence      Comma separated list of values or repeat of the parameter for each value will form a query with OR semantics, eg. `?influence=C1&influence=C2` | Search for research products based on their influence. |
| popularity | Accepted values:   `C1` for top 0.01% in terms of popularity   `C2` for top 0.1% in terms of popularity   `C3` for top 1% in terms of popularity   `C4` for top 10% in terms of popularity   `C5` for average/low in terms of popularity      Comma separated list of values or repeat of the parameter for each value will form a query with OR semantics, eg. `?popularity=C1&popularity=C2` | Search for research products based on their popularity. |
| impulse | Accepted values:   `C1` for top 0.01% in terms of impulse   `C2` for top 0.1% in terms of impulse   `C3` for top 1% in terms of impulse   `C4` for top 10% in terms of impulse   `C5` for average/low in terms of impulse      Comma separated list of values or repeat of the parameter for each value will form a query with OR semantics, eg. `?impulse=C1&impulse=C2` | Search for research products based on their impulse. |
| citationCount | Accepted values:   `C1` for top 0.01% in terms of citation count   `C2` for top 0.1% in terms of citation count   `C3` for top 1% in terms of citation count   `C4` for top 10% in terms of citation count   `C5` for average/low in terms of citation count      Comma separated list of values or repeat of the parameter for each value will form a query with OR semantics, eg. `?citationCount=C1&citationCount=C2` | Search for research products based on their number of citations. |
| openaireProviderID | Comma separated list of identifiers. | Search for research products by openaire data provider identifier.   Alternatively, it is possible to repeat the parameter for each provider id. In both cases, provider identifiers will form a query with OR semantics. |
| openaireProjectID | Comma separated list of identifiers.   Alternatively, it is possible to repeat the parameter for each provider id. In both cases, provider identifiers will form a query with OR semantics. | Search for research products by openaire project identifier. Alternatively, it is possible to repeat the parameter for each provider id. In both cases, provider identifiers will form a query with OR semantics. |
| hasProject | true \| false | If hasProject is true gets the research products that have a link to a project. If hasProject is false gets the publications with no links to projects. |
| FP7ProjectID | ... | Search for research products associated to a FP7 project with the given grant number. It is equivalent to a query by `funder=FP7&projectID={grantID}` |

## Parameters for publications[​](https://graph.openaire.eu/docs/apis/search-api/#parameters-for-publications "Direct link to heading")

Endpoint: [https://api.openaire.eu/search/publications](https://api.openaire.eu/search/publications)

You can use all the [general research products parameters](https://graph.openaire.eu/docs/apis/search-api/#general-parameters) as well as those in the following table.

| Parameter | Option | Description |
| --- | --- | --- |
| instancetype | Comma separated list of publication types. Check [here](http://api.openaire.eu/vocabularies/dnet:publication_resource) to see the possible values | Gets the publication of the given type, if any. |
| originalId | Comma separated list of original identifiers as we get them from the data source.   Alternatively, it is possible to repeat the parameter for each requested identifier. | Gets the publication with the given openaire identifier, if any. |
| sdg | The number of the Sustainable Development Goals `[1-17]`.   Check [here](https://sdgs.un.org/goals) to see the Sustainable Developemnt Goals. | Gets the publications that are classified with the respective Sustainable Development Goal number. |
| fos | The Field of Science classification value.   Check [here](https://graph.openaire.eu/docs/assets/files/athenarc_fos_hierarchy-3b6e1c7197e46bd3a3e9790115a8dec9.json) to see the Field of Science classification values | Gets the publications that are classified with the respective Field of Science classification value. |
| openairePublicationID | Comma separated list of OpenAIRE identifiers.   Alternatively, it is possible to repeat the parameter for each requested identifier. | Gets the publication with the given openaire identifier, if any. |
| peerReviewed | Accepted values:   true \| false | Specify if the publications are peerReviewed or not. |
| diamondJournal | Accepted values:   true \| false | Specify if the publications are published in a diamond journal or not. |
| publiclyFunded | Accepted values:   true \| false | Specify if the publications are publicly funded or not. |
| green | Accepted values:   true \| false | Specify if the publications are green open access or not. |
| openAccessColor | Accepted values:   `gold`\| `bronze`\| `hybrid`   Comma separated list of values or repeat of the parameter for each value will form a query with OR semantics, eg. `?openAccessColor=gold&openAccessColor=hybrid` | Specify the open access color of a publication. |

## Parameters for research data[​](https://graph.openaire.eu/docs/apis/search-api/#parameters-for-research-data "Direct link to heading")

Endpoint: [https://api.openaire.eu/search/datasets](https://api.openaire.eu/search/datasets)

You can use all the [general research products parameters](https://graph.openaire.eu/docs/apis/search-api/#general-parameters) as well as those in the following table.

| Parameter | Option | Description |
| --- | --- | --- |
| openaireDatasetID | Comma separated list of OpenAIRE identifiers.   Alternatively, it is possible to repeat the parameter for each requested identifier. | Gets the research data with the given openaire identifier, if any. |

## Parameters for research software[​](https://graph.openaire.eu/docs/apis/search-api/#parameters-for-research-software "Direct link to heading")

Endpoint: [https://api.openaire.eu/search/software](https://api.openaire.eu/search/software)

You can use all the [general research products parameters](https://graph.openaire.eu/docs/apis/search-api/#general-parameters) as well as those in the following table.

| Parameter | Option | Description |
| --- | --- | --- |
| openaireSoftwareID | Comma separated list of OpenAIRE identifiers.   Alternatively, it is possible to repeat the parameter for each requested identifier. | Gets the research software with the given openaire identifier, if any. |

## Parameters for other research products[​](https://graph.openaire.eu/docs/apis/search-api/#parameters-for-other-research-products "Direct link to heading")

Endpoint: [https://api.openaire.eu/search/other](https://api.openaire.eu/search/other)

You can use all the [general research products parameters](https://graph.openaire.eu/docs/apis/search-api/#general-parameters) as well as those in the following table.

| Parameter | Option | Description |
| --- | --- | --- |
| openaireOtherID | Comma separated list of OpenAIRE identifiers.   Alternatively, it is possible to repeat the parameter for each requested identifier. | Gets the other research products with the given openaire identifier, if any. |


## Searching for projects

## Endpoints

For research projects: [http://api.openaire.eu/search/projects](http://api.openaire.eu/search/projects)

## Parameters

| Parameter | Option | Description |
| --- | --- | --- |
| page | integer | Page number of the search results. |
| size | integer | Number of results per page. |
| format | json \| xml \| csv \| tsv | The format of the response. The default is xml. |
| model | openaire \| sygma | The data model of the response. Default is openaire. Model sygma is a simplified version of the openaire model. For sygma, only the xml format is available. The relative XML schema is available [here](https://www.openaire.eu/schema/sygma/oaf_sygma_v2.1.xsd). |
| sortBy | `sortBy=field,[ascending\\|descending]`; **'field'** is one of: `projectstartdate`, `projectstartyear`, `projectenddate`, `projectendyear`, `projectduration` | The sorting order of the specified field. |
| hasECFunding | true \| false | If hasECFunding is true gets the entities funded by the EC. If hasECFunding is false gets the entities related to projects not funded by the EC. |
| hasWTFunding | true \| false | If hasWTFunding is true gets the entities funded by Wellcome Trust. The results are the same as those obtained with `funder=wt`. If hasWTFunding is false gets the entities related to projects not funded by Wellcome Trust. |
| funder | WT \| EC \| ARC \| ANDS \| NSF \| FCT \| NHMRC | Search for entities by funder. |
| fundingStream | ... | Search for entities by funding stream. |
| FP7scientificArea | ... | Search for FP7 entities by scientific area. |
| keywords | White-space separated list of keywords. | N/A |
| sortBy | `sortBy=field,[ascending\\|descending]`; **'field'** is one of: `projectstartdate`, `projectstartyear`, `projectenddate`, `projectendyear`, `projectduration` | The sorting order of the specified field. |
| grantID | Comma separated list of grant identifiers. | Gets the project with the given grant identifier, if any. |
| openairePublicationID | Comma separated list of OpenAIRE identifiers. | Gets the publication with the given openaire identifier, if any. |
| name | White-space separated list of keywords. | Gets the projects whose names contain the given list of keywords. Using double quotes `"` you get an exact match, if any. |
| acronym | N/A | Gets the project with the given acronym, if any. |
| callID | N/A | Search for projects by call identifier. |
| startYear | Year formatted as `YYYY` | Gets the projects that started in the given year. |
| endYear | Year formatted as `YYYY`. | Gets the projects that ended in the given year. |
| participantCountries | Comma separeted list of 2 letter country codes. | Search for projects by participant countries. |
| participantAcronyms | White space separeted list of acronyms of institutions. | Search for projects by participant institutions. |

Version: 10.2.0

## Response metadata format

In this page, we elaborate on the metadata response format, as well as response headers and errors.

## Main response

The OpenAIRE Search API supports the following types of response formats:

- XML
- JSON
- CSV
- TSV

In the next paragraphs, we elaborate on the respective metadata formats.

### XML/JSON

The default format of delivered records is oaf (OpenAIRE Format - current version 1.0):

- XML schema: [https://www.openaire.eu/schema/1.0/oaf-1.0.xsd](https://www.openaire.eu/schema/1.0/oaf-1.0.xsd)
- Documentation: [https://www.openaire.eu/schema/1.0/doc/oaf-1.0.html](https://www.openaire.eu/schema/1.0/doc/oaf-1.0.html)

For the list of changes [click here](https://www.openaire.eu/openaire-xml-schema-change-announcement).

Note that latest versions of the XML schema and documentation are also available at the following permanent links:

- XML schema: [https://www.openaire.eu/schema/latest/oaf.xsd](https://www.openaire.eu/schema/latest/oaf.xsd)
- Documentation: [https://www.openaire.eu/schema/latest/doc/oaf.html](https://www.openaire.eu/schema/latest/doc/oaf.html)

Older versions:

- oaf v0.3 [XML schema](https://www.openaire.eu/schema/0.3/oaf-0.3.xsd) and [documentation](https://www.openaire.eu/schema/0.3/doc/oaf-0.3.html)
- oaf v0.2 [XML schema](https://www.openaire.eu/schema/0.2/oaf-0.2.xsd) and [documentation](https://www.openaire.eu/schema/0.2/doc/oaf-0.2.html)
- oaf v0.1 [XML schema](https://www.openaire.eu/schema/0.1/oaf-0.1.xsd) and [documentation](https://www.openaire.eu/schema/0.1/doc/oaf-0.1.html)

### CSV/TSV

The API returns in comma-separated files (CSV) or tab-separated files (TSV) the following fields:

- Title
- AUthors
- Publicatioy year
- DOI
- Download from
- Publication type
- Journal
- Funder
- Project name (GA Number)
- Access

## Headers

| Name | Description |
| --- | --- |
| x-ratelimit-limit | The maximum number of requests allowed for the client in one time window. |
| x-ratelimit-used | The number of requests already made by the client in the current time window. |

The OpenAIRE APIs use a sliding time window of one hour.

## Errors

### General

404 - Not found

```json
{
    "error": "Not found",
    "description": "Invald request path."
}
```

429 - Rate limit abuse

```json
{
    "error": "Too many requests",
    "description": "Request rate exceeded. Slow down."
}
```

### Only for authenticated requests

400 - Missing grant type

```json
{
    "error": "invalid_request",
    "error_description": "Missing grant type"
}
```

400 - Wrong grant type

```json
{
    "error": "unsupported_grant_type",
    "error_description": "Unsupported grant type: ..."
}
```

400 - Missing Refresh Token

```json
{  
    "status" : "error", 
    "code" : "400", 
    "message" : "Bad Request", 
    "description" : "Missing refreshToken parameter" 
}
```

401 - Missing username or/and password

```json
{
    "error": "unauthorized",
    "error_description": "Client id must not be empty!"
}
```

401 - Wrong username or/and password

```json
{
    "error": "unauthorized",
    "error_description": "Bad credentials"
}
```

401 - Invalid Refresh Token (for authenticated requests)

```json
{  
    "status" : "error", 
    "code" : "401", 
    "message" : "Unauthorised", 
    "description" : "Invalid refreshToken token" 
}
```

401 - Invalid client assertion

```json
{
    "error":"invalid_client",
    "error_description":"Bad client credentials"
}
```

401 - Client assertion for missing service

```json
{
    "error":"invalid_client",
    "error_description":"Could not find client {SERVICE_ID}"
}
```

401 - Expired signed jwt

```json
{
    "error":"unauthorized",
    "error_description":"Assertion Token in expired: {EXPIRATION_TIME}"
}
```

403 - Invalid Access Token
```json
{
    "error": "Token invalid",
    "description": "Authorization header value invalid."
}
```


# -------------------------------------------------------
#
# C:\dev\AIREloom\reference\official_docs\searching.md
#
# ------------------------------------------------------

This is a guide on how to search for specific entities using the OpenAIRE Graph API.

## Endpoints[​](https://graph.openaire.eu/docs/apis/graph-api/searching-entities/#endpoints "Direct link to heading")

Currently, the Graph API supports the following entity types:

- Research products - endpoint: [`GET /researchProducts`](https://api.openaire.eu/graph/v1/researchProducts)
- Organizations - endpoint: [`GET /organizations`](https://api.openaire.eu/graph/v1/organizations)
- Data sources - endpoint: [`GET /dataSources`](https://api.openaire.eu/graph/v1/dataSources)
- Projects - endpoint: [`GET /projects`](https://api.openaire.eu/graph/v1/projects)

Each of these endpoints can be used to list all entities of the corresponding type. Listing such entities can be more useful when using the [filtering](https://graph.openaire.eu/docs/apis/graph-api/searching-entities/filtering-search-results), [sorting](https://graph.openaire.eu/docs/apis/graph-api/searching-entities/sorting-and-paging#sorting), and [paging](https://graph.openaire.eu/docs/apis/graph-api/searching-entities/sorting-and-paging#paging) capabilities of the Graph API.

## Response[​](https://graph.openaire.eu/docs/apis/graph-api/searching-entities/#response "Direct link to heading")

The response of the aforementioned endpoints is an object of the following type:

```json
{    header: {        numFound: 36818386,        maxScore: 1,        queryTime: 21,        page: 1,        pageSize: 10    },    results: [        ...    ]}
```

It contains a `header` object with the following fields:

- `numFound`: the total number of entities found
- `maxScore`: the maximum relevance score of the search results
- `queryTime`: the time in milliseconds that the search took
- `page`: the current page of the search results (when using basic pagination)
- `pageSize`: the number of entities per page
- `nextCursor`: the next page cursor (when using cursor-based pagination, see: [paging](https://graph.openaire.eu/docs/apis/graph-api/searching-entities/sorting-and-paging#paging)

Finally, the `results` field contains an array of entities of the corresponding type (i.e., [Research product](https://graph.openaire.eu/docs/data-model/entities/research-product), [Organization](https://graph.openaire.eu/docs/data-model/entities/organization), [Data Source](https://graph.openaire.eu/docs/data-model/entities/data-source), or [Project](https://graph.openaire.eu/docs/data-model/entities/project)).

[

](https://graph.openaire.eu/docs/apis/graph-api/getting-a-single-entity)


# -------------------------------------------------------
#
# C:\dev\AIREloom\reference\official_docs\single_entity.md
#
# ------------------------------------------------------

This is a guide on how to retrieve detailed information on a single entity using the OpenAIRE Graph API.

## Endpoints[​](https://graph.openaire.eu/docs/apis/graph-api/#endpoints "Direct link to heading")

Currently, the Graph API supports the following entity types:

- Research products - endpoint: `GET /researchProducts/{id}`
- Organizations - endpoint: `GET /organizations/{id}`
- Data sources - endpoint: `GET /dataSources/{id}`
- Projects - endpoint: `GET /projects/{id}`

You can retrieve the data of a single entity by providing the entity's OpenAIRE identifier (id) in the corresponding endpoint. The OpenAIRE id is the primary key of an entity in the OpenAIRE Graph.

note

Note that if you want to retrieve multiple entities based on their OpenAIRE ids, you can use the [search endpoints and filter](https://graph.openaire.eu/docs/apis/graph-api/searching-entities/filtering-search-results#or-operator) by the `id` field using `OR`.

## Response[​](https://graph.openaire.eu/docs/apis/graph-api/#response "Direct link to heading")

The response of the Graph API is a [Research product](https://graph.openaire.eu/docs/data-model/entities/research-product), [Organization](https://graph.openaire.eu/docs/data-model/entities/organization), [Data Source](https://graph.openaire.eu/docs/data-model/entities/data-source), or [Project](https://graph.openaire.eu/docs/data-model/entities/project), depending on the endpoint used.

## Example[​](https://graph.openaire.eu/docs/apis/graph-api/#example "Direct link to heading")

In order to retrieve the research product with OpenAIRE id: `doi_dedup___::2b3cb7130c506d1c3a05e9160b2c4108`, you have to perform the following API call:

[https://api.openaire.eu/graph/v1/researchProducts/doi\_dedup\_\_\_::a55b42c0d32a4a24cf99e621623d110e](https://api.openaire.eu/graph/v1/researchProducts/doi_dedup___::a55b42c0d32a4a24cf99e621623d110e)

This will return all the data of the research product with the provided identifier:

```json
{  id: "doi_dedup___::a55b42c0d32a4a24cf99e621623d110e",  mainTitle: "OpenAIRE Graph Dataset",  description: [    "The OpenAIRE Graph is exported as several dataseta, so you can download the parts you are interested into. <strong>publication_[part].tar</strong>: metadata records about research literature (includes types of publications listed here)<br> <strong>dataset_[part].tar</strong>: metadata records about research data (includes the subtypes listed here) <br> <strong>software.tar</strong>: metadata records about research software (includes the subtypes listed here)<br> <strong>otherresearchproduct_[part].tar</strong>: metadata records about research products that cannot be classified as research literature, data or software (includes types of products listed here)<br> <strong>organization.tar</strong>: metadata records about organizations involved in the research life-cycle, such as universities, research organizations, funders.<br> <strong>datasource.tar</strong>: metadata records about data sources whose content is available in the OpenAIRE Graph. They include institutional and thematic repositories, journals, aggregators, funders' databases.<br> <strong>project.tar</strong>: metadata records about project grants.<br> <strong>relation_[part].tar</strong>: metadata records about relations between entities in the graph.<br> <strong>communities_infrastructures.tar</strong>: metadata records about research communities and research infrastructures Each file is a tar archive containing gz files, each with one json per line. Each json is compliant to the schema available at http://doi.org/10.5281/zenodo.8238874. The documentation for the model is available at https://graph.openaire.eu/docs/data-model/ Learn more about the OpenAIRE Graph at https://graph.openaire.eu. Discover the graph's content on OpenAIRE EXPLORE and our API for developers."  ],  type: "dataset",  publicationDate: "2023-08-08",  publisher: "Zenodo",  id: [    {      scheme: "Digital Object Identifier",      value: "10.5281/zenodo.8217359"    }  ],  // for brevity, the rest of the fields are omitted}
```

[

](https://graph.openaire.eu/docs/apis/graph-api/)


# -------------------------------------------------------
#
# C:\dev\AIREloom\reference\official_docs\sorting_and_paging.md
#
# ------------------------------------------------------

The OpenAIRE Graph API allows you to sort and page through the results of your search queries. This enables you to retrieve the most relevant results and manage large result sets more effectively.

## Sorting[​](https://graph.openaire.eu/docs/apis/graph-api/searching-entities/#sorting "Direct link to heading")

Sorting based on specific fields, helps to retrieve data in the preferred order. Sorting is achieved using the `sortBy` parameter, which specifies the field and the direction (ascending or descending) for sorting.

- `sortBy`: Defines the field and the sort direction. The format should be `fieldname sortDirection`, where the `sortDirection` can be either `ASC` for ascending order or `DESC` for descending order.

The field names that can be used for sorting are specific to each entity type and can be found in the `sortBy` field values of the [available paremeters](https://graph.openaire.eu/docs/apis/graph-api/searching-entities/filtering-search-results#available-parameters).

Note that the default sorting is based on the `relevance` score of the search results.

Examples:

- Get research products published after `2020-01-01` and sort them by the publication date in descending order:
	[https://api.openaire.eu/graph/v1/researchProducts?fromPublicationDate=2020-01-01&sortBy=publicationDate DESC](https://api.openaire.eu/graph/v1/researchProducts?fromPublicationDate=2020-01-01&sortBy=publicationDate%20DESC)
- Get research products with the keyword `"COVID-19"` and sort them by their (citation-based) popularity:
	[https://api.openaire.eu/graph/v1/researchProducts?search=COVID-19&sortBy=popularity DESC](https://api.openaire.eu/graph/v1/researchProducts?search=COVID-19&sortBy=popularity%20DESC)

Note that you can combine multiple sorting conditions by separating them with a comma.

Example:

- Get research products with the keyword `"COVID-19"` and sort them by their publication date in ascending order and then by their popularity in descending order:
	[https://api.openaire.eu/graph/v1/researchProducts?search=COVID-19&sortBy=publicationDate ASC,popularity DESC](https://api.openaire.eu/graph/v1/researchProducts?search=COVID-19&sortBy=publicationDate%20ASC,popularity%20DESC)

## Paging[​](https://graph.openaire.eu/docs/apis/graph-api/searching-entities/#paging "Direct link to heading")

The OpenAIRE Graph API supports basic and cursor-based pagination. In basic pagination, `page` and `pageSize` parameters are used, enabling you to specify which part of the result set to retrieve and how many results per page.

### Offset-based paging[​](https://graph.openaire.eu/docs/apis/graph-api/searching-entities/#offset-based-paging "Direct link to heading")

Offset-based paging should be used to retrieve a small dataset only (up to 10000 records).

- `page`: Specifies the page number of the results you want to retrieve. Page numbering starts from 1.
- `pageSize`: Defines the number of results to be returned per page. This helps limit the amount of data returned in a single request, making it easier to process.

Example:

- Get the top 10 most influential research products that contain the phrase "knowledge graphs":
	[https://api.openaire.eu/graph/v1/researchProducts?search="knowledge graphs"&page=1&pageSize=10&sortBy=influence DESC](https://api.openaire.eu/graph/v1/researchProducts?search=%22knowledge%20graphs%22&page=1&pageSize=10&sortBy=influence%20DESC)

response:

```
{    header: {        numFound: 36818386,        maxScore: 1,        queryTime: 21,        page: 1,        pageSize: 10    },    results: [        ...    ]}
```

### Cursor-based paging[​](https://graph.openaire.eu/docs/apis/graph-api/searching-entities/#cursor-based-paging "Direct link to heading")

Cursor should be used when it is required to retrieve a big dataset (more than 10000 records).

- `cursor`: Cursor-based pagination. Initial value: `cursor=*`.

Example:

- [https://api.openaire.eu/graph/v1/researchProducts?search="knowledge graphs"&pageSize=10&cursor=\*&sortBy=influence DESC](https://api.openaire.eu/graph/v1/researchProducts?search=%22knowledge%20graphs%22&pageSize=10&cursor=*&sortBy=influence%20DESC)

response:

```
{    header: {        numFound: 36818386,        maxScore: 1,        queryTime: 21,        pageSize: 10,        nextCursor: "AoI/D2M2NGU1YjVkNTQ4Nzo6NjlmZTBmNjljYzM4YTY1MjI5YjM3ZDRmZmIyMTU1NDAIP4AAAA=="    },    results: [        ...    ]}
```

Use `nextCursor` value, to get the next page of results.

[

](https://graph.openaire.eu/docs/apis/graph-api/searching-entities/filtering-search-results)


# -------------------------------------------------------
#
# C:\dev\AIREloom\reference\openaire_endpoints.md
#
# ------------------------------------------------------


# Endpoints
Base url: https://api.openaire.eu/graph/

Research products endpoint: /researchProducts
Organizations endpoint: /organizations
Data sources endpoint: /dataSources
Projects endpoint: /projects

# Examples


Get research products that contain both "climate" and "change":

[https://api.openaire.eu/graph/researchProducts?search=climate%20AND%20change](https://api.openaire.eu/graph/researchProducts?search=climate%20AND%20change)

Get research products that are classified with both Fields of Study (FOS) "03 medical and health sciences" and "0502 economics and business":

[https://api.openaire.eu/graph/researchProducts?fos="03 medical and health sciences" AND "0502 economics and business"](https://api.openaire.eu/graph/researchProducts?fos=%2203%20medical%20and%20health%20sciences%22%20AND%20%220502%20economics%20and%20business%22)

Get research products with the OpenAIRE ids doi_dedup___::2b3cb7130c506d1c3a05e9160b2c4108 or pmid_dedup__::1591ebf0e0698ed4a99455ff2ba4adc0:

[https://api.openaire.eu/graph/researchProducts?id=r3730f562f9e::539da48b3796663b17e6166bb966e5b1%20OR%20pmid_dedup__::1591ebf0e0698ed4a99455ff2ba4adc0](https://api.openaire.eu/graph/researchProducts?id=r3730f562f9e::539da48b3796663b17e6166bb966e5b1%20OR%20pmid_dedup__::1591ebf0e0698ed4a99455ff2ba4adc0)

Get projects that are connected to organizations in the US or Greece:

[https://api.openaire.eu/graph/projects?relOrganizationCountryCode=US%20OR%20GR](https://api.openaire.eu/graph/projects?relOrganizationCountryCode=US%20OR%20GR)

or by using the same query parameter multiple times: [https://api.openaire.eu/graph/projects?relOrganizationCountryCode=US&relOrganizationCountryCode=GR](https://api.openaire.eu/graph/projects?relOrganizationCountryCode=US&relOrganizationCountryCode=GR)

or just using commas:
[https://api.openaire.eu/graph/projects?relOrganizationCountryCode=US,GR](https://api.openaire.eu/graph/projects?relOrganizationCountryCode=US,GR)

Get research products that contain "semantic" but not "web":

[https://api.openaire.eu/graph/researchProducts?search=semantic%20NOT%20web](https://api.openaire.eu/graph/researchProducts?search=semantic%20NOT%20web)

Get all data sources that are not journals:

[https://api.openaire.eu/graph/dataSources?dataSourceTypeName=NOT%20Journal](https://api.openaire.eu/graph/dataSources?dataSourceTypeName=NOT%20Journal)

Get research products published after 2020-01-01 and sort them by the publication date in descending order:

[https://api.openaire.eu/graph/researchProducts?fromPublicationDate=2020-01-01&sortBy=publicationDate%20DESC](https://api.openaire.eu/graph/researchProducts?fromPublicationDate=2020-01-01&sortBy=publicationDate%20DESC)

Get research products with the keyword "COVID-19" and sort them by their (citation-based) popularity:
[https://api.openaire.eu/graph/researchProducts?fromPublicationDate=2020-01-01&sortBy=publicationDate%20DESC](https://api.openaire.eu/graph/researchProducts?fromPublicationDate=2020-01-01&sortBy=publicationDate%20DESC)






# Response format

{
    header: {
        numFound: 36818386,
        maxScore: 1,
        queryTime: 21,
        page: 1,
        pageSize: 10
        nextCursor: "AoI/D2M2NGU1YjVkNTQ4Nzo6NjlmZTBmNjljYzM4YTY1MjI5YjM3ZDRmZmIyMTU1NDAIP4AAAA=="   // note: only when cursor-based paging is active
    },
    results: [
        ...
    ]
}

# Parameters

## Sorting

`sortBy`:
    Defines the field and the sort direction. The format should be `fieldname` `sortDirection`, where the `sortDirection` can be either `ASC` or D`ESC.
    The default sorting is based on the relevance score of the search results.
    Valid values for `fieldname` depends on the endpoint:
    `researchProducts`: relevance, publicationDate, dateOfCollection, influence, popularity, citationCount, impulse
    `organizations`: relevance
    `dataSources`: relevance
    `projects`: relevance, startDate, endDate

## Paging
### Up to 10000 records

`page`:
    Specifies the page number of the results you want to retrieve. Page numbering starts from 1.
`pageSize`:
    Defines the number of results to be returned per page. This helps limit the amount of data returned in a single request, making it easier to process.

### Cursor based (no maximum)
`cursor`:
    initial value is `*`. response.header.nextCursor holds the value for the next set of results.

# Filters

Filters can be combined without limit. By default multiple filter params are joined using `AND`. `OR` and `NOT` operators are available.

Each endpoint has a specific set of valid filters.

## Research Products

`search`
    Search in the content of the research product.
`mainTitle`
	Search in the research product's main title.
`description`
	Search in the research product's description.
`id`
	The OpenAIRE id of the research product.
`pid`
	The persistent identifier of the research product.
`originalId`
	The identifier of the record at the original sources.
`type`
	The type of the research product. One of publication, dataset, software, or other
`fromPublicationDate`
	Gets the research products whose publication date is greater than or equal to the given date. A date formatted as `ΥΥΥΥ` or `YYYY-MM-DD`
`toPublicationDate`
	Gets the research products whose publication date is less than or equal to the given date. A date formatted as `YYYY` or `YYYY-MM-DD`
`subjects`
	List of subjects associated to the research product.
`countryCode`
	The country code for the country associated with the research product.
`authorFullName`
	The full name of the authors involved in producing this research product.
`authorOrcid`
	The ORCiD of the authors involved in producing this research product.
`publisher`
	The name of the entity that holds, archives, publishes prints, distributes, releases, issues, or produces the resource.
`bestOpenAccessRightLabel`
	The best open access rights among the research product's instances. One of `OPEN SOURCE`, `OPEN`, `EMBARGO`, `RESTRICTED`, `CLOSED`, `UNKNOWN`
`influenceClass`
	Citation-based indicator that reflects the overall impact of a research product. Please, choose a class among `C1`, `C2`, `C3`, `C4`, or `C5` for top 0.01%, top 0.1%, top 1%, top 10%, and average in terms of influence respectively.
`impulseClass`
	Citation-based indicator that reflects the initial momentum of a research product directly after its publication. Please, choose a class among `C1`, `C2`, `C3`, `C4`, or `C5` for top 0.01%, top 0.1%, top 1%, top 10%, and average in terms of impulse respectively
`popularityClass`
	Citation-based indicator that reflects current impact or attention of a research product. Please, choose a class among `C1`, `C2`, `C3`, `C4`, or `C5` for top 0.01%, top 0.1%, top 1%, top 10%, and average in terms of popularity respectively.
`citationCountClass`
	Citation-based indicator that reflects the overall impact of a research product by summing all its citations. Please, choose a class among `C1`, `C2`, `C3`, `C4`, or `C5` for top 0.01%, top 0.1%, top 1%, top 10%, and average in terms of citation count respectively.
`instanceType`
    [Only for publications]	Retrieve publications of the given instance type. Check [here](https://api.openaire.eu/vocabularies/dnet:publication_resource) for all possible instance type values.
`sdg`
    [Only for publications]	Retrieves publications classified with the respective Sustainable Development Goal number. Integer in the range `[1, 17]`
`fos`
    [Only for publications]	Retrieves publications classified with a given Field of Science (FOS). A FOS classification identifier (see [here](https://explore.openaire.eu/assets/common-assets/vocabulary/fos.json) for details).
`isPeerReviewed`
    [Only for publications]	Indicates whether the publications are peerReviewed or not. (Boolean)
`isInDiamondJournal`
    [Only for publications]	Indicates whether the publication was published in a diamond journal or not. (Boolean)
`isPubliclyFunded`
    [Only for publications]	Indicates whether the publication was publicly funded or not. (Boolean)
`isGreen`
    [Only for publications]	Indicates whether the publication was published following the green open access model. (Boolean)
`openAccessColor`
    [Only for publications]	Specifies the Open Access color of the publication. One of `bronze`, `gold`, or `hybrid`
`relOrganizationId`
    Retrieve research products connected to the organization (with OpenAIRE id).
`relCommunityId`
    Retrieve research products connected to the community (with OpenAIRE id).
`relProjectId`
    Retrieve research products connected to the project (with OpenAIRE id).
`relProjectCode`
    Retrieve research products connected to the project with code.
`hasProjectRel`
    Retrieve research products that are connected to a project. (Boolean)
`relProjectFundingShortName`
    Retrieve research products connected to a project that has a funder with the given short name.
`relProjectFundingStreamId`
    Retrieve research products connected to a project that has the given funding identifier.
`relHostingDataSourceId`
    Retrieve research products hosted by the data source (with OpenAIRE id).
`relCollectedFromDatasourceId`
    Retrieve research products collected from the data source (with OpenAIRE id).

# Organizations

`search`
	Search in the content of the organization.
`legalName`
	The legal name of the organization.
`legalShortName`
	The legal name of the organization in short form.
`id`
	The OpenAIRE id of the organization.
`pid`
	The persistent identifier of the organization.
`countryCode`
	The country code of the organization.
`relCommunityId`
	Retrieve organizations connected to the community (with OpenAIRE id).
`relCollectedFromDatasourceId`
	Retrieve organizations collected from the data source (with OpenAIRE id).

# Data sources

`search`
	Search in the content of the data source.
`officialName`
	The official name of the data source.
`englishName`
	The English name of the data source.
`legalShortName`
	The legal name of the organization in short form.
`id`
	The OpenAIRE id of the data source.
`pid`
	The persistent identifier of the data source.
`subjects`
	List of subjects associated to the datasource.
`dataSourceTypeName`
	The data source type; see all possible values here .
`contentTypes`
	Types of content in the data source, as defined by OpenDOAR.
`relOrganizationId`
	Retrieve data sources connected to the organization (with OpenAIRE id).
`relCommunityId`
	Retrieve data sources connected to the community (with OpenAIRE id).
`relCollectedFromDatasourceId`
	Retrieve data sources collected from the data source (with OpenAIRE id).

# Projects

`search`
	Search in the content of the projects.
`title`
	Search in the project's title.
`keywords`
	The project's keywords.
`id`
	The OpenAIRE id of the project.
`code`
	The grant agreement (GA) code of the project.
`acronym`
	Project's acronym.
`callIdentifier`
	The identifier of the research call.
`fundingShortName`
	The short name of the funder.
`fundingStreamId`
	The identifier of the funding stream.
`fromStartDate`
	Gets the projects with start date greater than or equal to the given date. Please provide a date formatted as YYYY or YYYY-MM-DD.
`toStartDate`
	Gets the projects with start date less than or equal to the given date. Please provide a date formatted as YYYY or YYYY-MM-DD.
`fromEndDate`
	Gets the projects with end date greater than or equal to the given date. Please provide a date formatted as YYYY or YYYY-MM-DD.
`toEndDate`
	Gets the projects with end date less than or equal to the given date. Please provide a date formatted as YYYY or YYYY-MM-DD.
`relOrganizationName`
	The name or short name of the related organization.
`relOrganizationId`
	The organization identifier of the related organization.
`relCommunityId`
	Retrieve projects connected to the community (with OpenAIRE id).
`relOrganizationCountryCode`
	The country code of the related organizations.
`relCollectedFromDatasourceId`
	Retrieve projects collected from the data source (with OpenAIRE id).



# -------------------------------------------------------
#
# C:\dev\AIREloom\reference\openaire_entities.md
#
# ------------------------------------------------------



# Entitities

This file describes all 4 major entities that the OpenAIRE API can return.

## Research Products

Research products are intended as digital objects, described by metadata, resulting from a scientific process. In this page, we descibe the properties of the `ResearchProduct` object.

Moreover, there are the following sub-types of a `ResearchProduct`, that inherit all its properties and further extend it. They are listed on the end of this entity.

- [Publication](https://graph.openaire.eu/docs/data-model/entities/#publication)
- [Data](https://graph.openaire.eu/docs/data-model/entities/#data)
- [Software](https://graph.openaire.eu/docs/data-model/entities/#software)
- [Other research product](https://graph.openaire.eu/docs/data-model/entities/#other-research-product)

## The ResearchProduct object

### id​

*Type: String • Cardinality: ONE*

Main entity identifier, created according to the [OpenAIRE entity identifier and PID mapping policy](https://graph.openaire.eu/docs/data-model/pids-and-identifiers).

```prism
"id": "doi_dedup___::80f29c8c8ba18c46c88a285b7e739dc3"
```

### type​

*Type: String • Cardinality: ONE*

Type of the research products. Possible types:

- `publication`
- `data`
- `software`
- `other`

as declared in the terms from the [dnet:result\_typologies vocabulary](https://api.openaire.eu/vocabularies/dnet:result_typologies).

```prism
"type": "publication"
```

### originalIds​

*Type: String • Cardinality: MANY*

Identifiers of the record at the original sources.

```prism
"originalIds": [
    "oai:pubmedcentral.nih.gov:8024784",
    "S0048733321000305",
    "10.1016/j.respol.2021.104226",
    "3136742816"
]
```

### mainTitle​

*Type: String • Cardinality: ONE*

A name or title by which a research product is known. It may be the title of a publication or the name of a piece of software.

```prism
"mainTitle": "The fall of the innovation empire and its possible rise through open science"
```

### subTitle​

*Type: String • Cardinality: ONE*

Explanatory or alternative name by which a research product is known.

```prism
"subTitle": "An analysis of cases from 1980 - 2020"
```

### authors​

*Type: [Author](https://graph.openaire.eu/docs/data-model/entities/other#author) • Cardinality: MANY*

The main researchers involved in producing the data, or the authors of the publication.

```prism
"authors": [
    {
        "fullName": "E. Richard Gold",
        "rank": 1,
        "name": "Richard",
        "surname": "Gold",
        "pid": {
            "id": {
                "scheme": "orcid",
                "value": "0000-0002-3789-9238"
            },
            "provenance": {
                "provenance": "Harvested",
                "trust": "0.9"
            }
        }
    },
    ...
]
```

### bestAccessRight​

*Type: [BestAccessRight](https://graph.openaire.eu/docs/data-model/entities/other#bestaccessright) • Cardinality: ONE*

The most open access right associated to the manifestations of this research product.

```prism
"bestAccessRight": {
    "code": "c_abf2",
    "label": "OPEN",
    "scheme": "http://vocabularies.coar-repositories.org/documentation/access_rights/"
}
```

### contributors​

*Type: String • Cardinality: MANY*

The institution or person responsible for collecting, managing, distributing, or otherwise contributing to the development of the resource.

```prism
"contributors": [
    "University of Zurich",
    "Wright, Aidan G C",
    "Hallquist, Michael",
    ...
]
```

### countries​

*Type: [ResultCountry](https://graph.openaire.eu/docs/data-model/entities/other#resultcountry) • Cardinality: MANY*

Country associated with the research product: it is the country of the organisation that manages the institutional repository or national aggregator or CRIS system from which this record was collected. Country of affiliations of authors can be found instead in the affiliation relation.

```prism
"countries": [
    {
        "code": "CH",
        "label": "Switzerland",
        "provenance": {
            "provenance": "Inferred by OpenAIRE",
            "trust": "0.85"
        }
    },
    ...
]
```

### coverages​

*Type: String • Cardinality: MANY*

### dateOfCollection​

*Type: String • Cardinality: ONE*

When OpenAIRE collected the record the last time.

```prism
"dateOfCollection": "2021-06-09T11:37:56.248Z"
```

### descriptions​

*Type: String • Cardinality: MANY*

A brief description of the resource and the context in which the resource was created.

```prism
"descriptions": [
    "Open science partnerships (OSPs) are one mechanism to reverse declining efficiency. OSPs are public-private partnerships that openly share publications, data and materials.",
    "There is growing concern that the innovation system's ability to create wealth and attain social benefit is declining in effectiveness. This article explores the reasons for this decline and suggests a structure, the open science partnership, as one mechanism through which to slow down or reverse this decline.",
    "The article examines the empirical literature of the last century to document the decline. This literature suggests that the cost of research and innovation is increasing exponentially, that researcher productivity is declining, and, third, that these two phenomena have led to an overall flat or declining level of innovation productivity.",
    ...
]
```

### embargoEndDate​

*Type: String • Cardinality: ONE*

Date when the embargo ends and this research product turns Open Access.

```prism
"embargoEndDate": "2017-01-01"
```

### indicators​

*Type: [Indicator](https://graph.openaire.eu/docs/data-model/entities/other#indicator-1) • Cardinality: ONE*

The indicators computed for this research product; currently, the following types of indicators are supported:

- [Citation-based impact indicators by BIP!](https://graph.openaire.eu/docs/data-model/entities/other#citationimpact)
- [Usage Statistics indicators](https://graph.openaire.eu/docs/data-model/entities/other#usagecounts)

```prism
"indicators": {
        "citationImpact": {
                "influence": 123,
                "influenceClass": "C2",
                "citationCount": 456,
                "citationClass": "C3",
                "popularity": 234,
                "popularityClass": "C1",
                "impulse": 987,
                "impulseClass": "C3"
        },
        "usageCounts": {
                "downloads": "10",
                 "views": "20"
        }
}
```

### instances​

*Type: [Instance](https://graph.openaire.eu/docs/data-model/entities/other#instance) • Cardinality: MANY*

Specific materialization or version of the research product. For example, you can have one research product with three instances: one is the pre-print, one is the post-print, one is the published version.

```prism
"instances": [
    {
        "accessRight": {
            "code": "c_abf2",
            "label": "OPEN",
            "openAccessRoute": "gold",
            "scheme": "http://vocabularies.coar-repositories.org/documentation/access_rights/"
        },
        "alternateIdentifiers": [
            {
                "scheme": "doi",
                "value": "10.1016/j.respol.2021.104226"
            },
            ...
        ],
        "articleProcessingCharge": {
            "amount": "4063.93",
            "currency": "EUR"
        },
        "license": "http://creativecommons.org/licenses/by-nc/4.0",
        "pids": [
            {
                "scheme": "pmc",
                "value": "PMC8024784"
            },
            ...
        ],

        "publicationDate": "2021-01-01",
        "refereed": "UNKNOWN",
        "type": "Article",
        "urls": [
            "http://europepmc.org/articles/PMC8024784"
        ]
    },
    ...
]
```

### language​

*Type: [Language](https://graph.openaire.eu/docs/data-model/entities/other#language) • Cardinality: ONE*

The alpha-3/ISO 639-2 code of the language. Values controlled by the [dnet:languages vocabulary](https://api.openaire.eu/vocabularies/dnet:languages).

```prism
"language": {
    "code": "eng",
    "label": "English"
}
```

### lastUpdateTimeStamp​

*Type: Long • Cardinality: ONE*

Timestamp of last update of the record in OpenAIRE.

```prism
"lastUpdateTimeStamp": 1652722279987
```

### pids​

*Type: [ResultPid](https://graph.openaire.eu/docs/data-model/entities/other#resultpid) • Cardinality: MANY*

Persistent identifiers of the research product. See also the [OpenAIRE entity identifier and PID mapping policy](https://graph.openaire.eu/docs/data-model/pids-and-identifiers) to learn more.

```prism
"pids": [
    {
        "scheme": "pmc",
        "value": "PMC8024784"
    },
    {
        "scheme": "doi",
        "value": "10.1016/j.respol.2021.104226"
    },
    ...
]
```

### publicationDate​

*Type: String • Cardinality: ONE*

Main date of the research product: typically the publication or issued date. In case of a research product with different versions with different dates, the date of the research product is selected as the most frequent well-formatted date. If not available, then the most recent and complete date among those that are well-formatted. For statistics, the year is extracted and the research product is counted only among the research products of that year. Example: Pre-print date: 2019-02-03, Article date provided by repository: 2020-02, Article date provided by Crossref: 2020, OpenAIRE will set as date 2019-02-03, because it’s the most recent among the complete and well-formed dates. If then the repository updates the metadata and set a complete date (e.g. 2020-02-12), then this will be the new date for the research product because it becomes the most recent most complete date. However, if OpenAIRE then collects the pre-print from another repository with date 2019-02-03, then this will be the “winning date” because it becomes the most frequent well-formatted date.

```prism
"publicationDate": "2021-03-18"
```

### publisher​

*Type: String • Cardinality: ONE*

The name of the entity that holds, archives, publishes prints, distributes, releases, issues, or produces the resource.

```prism
"publisher": "Elsevier, North-Holland Pub. Co"
```

### sources​

*Type: String • Cardinality: MANY*

A related resource from which the described resource is derived. See definition of Dublin Core field [dc:source](https://www.dublincore.org/specifications/dublin-core/dcmi-terms/elements11/source).

```prism
"sources": [
      "Research Policy",
      "Crossref",
      ...
]
```

### formats​

*Type: String • Cardinality: MANY*

The file format, physical medium, or dimensions of the resource.

```prism
"formats": [
    "application/pdf",
    "text/html",
    ...
]
```

### subjects​

*Type: [Subject](https://graph.openaire.eu/docs/data-model/entities/other#subject) • Cardinality: MANY*

Subject, keyword, classification code, or key phrase describing the resource.

OpenAIRE classifies research products according to the [Field of Science](https://graph.openaire.eu/docs/graph-production-workflow/indicators-ingestion/fos-classification) and [Sustainable Development Goals](https://graph.openaire.eu/docs/graph-production-workflow/indicators-ingestion/sdg-classification) taxonomies. Check out the relative sections to know more.

```prism
"subjects": [
    {
        "subject": {
            "scheme": "FOS",
            "value": "01 natural sciences"
        },
        "provenance": {
            "provenance": "inferred by OpenAIRE",
            "trust": "0.85"
        }
    },
    {
        "subject": {
            "scheme": "SDG",
            "value": "2. Zero hunger"
        },
        "provenance": {
            "provenance": "inferred by OpenAIRE",
            "trust": "0.83"
        }
    },
    {
        "subject": {
            "scheme": "keyword",
            "value": "Open science"
        },
        "provenance": {
            "provenance": "Harvested",
            "trust": "0.9"
        }
    },
    ...
]
```

### isGreen​

*Type: Boolean • Cardinality: ONE*

Indicates whether or not the scientific result was published following the green open access model.

### openAccessColor​

*Type: String • Cardinality: ONE*

Indicates the specific open access model used for the publication; possible value is one of `bronze, gold, hybrid`.

### isInDiamondJournal​

*Type: Boolean • Cardinality: ONE*

Indicates whether or not the publication was published in a diamond journal.

### publiclyFunded​

*Type: String • Cardinality: ONE*

Discloses whether the publication acknowledges grants from public sources.

---

## Sub-types​

There are the following sub-types of `Result`. Each inherits all its fields and extends them with the following.

### Publication​

Metadata records about research literature (includes types of publications listed [here](http://api.openaire.eu/vocabularies/dnet:result_typologies/publication)).

#### container​

*Type: [Container](https://graph.openaire.eu/docs/data-model/entities/other#container) • Cardinality: ONE*

Container has information about the conference or journal where the research product has been presented or published.

```prism
"container": {
    "edition": "",
    "iss": "5",
    "issnLinking": "",
    "issnOnline": "1873-7625",
    "issnPrinted": "0048-7333",
    "name": "Research Policy",
    "sp": "12",
    "ep": "22",
    "vol": "50"
}
```

### Data​

Metadata records about research data (includes the subtypes listed [here](http://api.openaire.eu/vocabularies/dnet:result_typologies/dataset)).

#### size​

*Type: String • Cardinality: ONE*

The declared size of the research data.

```prism
"size": "10129818"
```

#### version​

*Type: String • Cardinality: ONE*

The version of the research data.

```prism
"version": "v1.3"
```

#### geolocations​

*Type: [GeoLocation](https://graph.openaire.eu/docs/data-model/entities/other#geolocation) • Cardinality: MANY*

The list of geolocations associated with the research data.

```prism
"geolocations": [
    {
        "box": "18.569386 54.468973  18.066832 54.83707",
        "place": "Tübingen, Baden-Württemberg, Southern Germany",
        "point": "7.72486 50.1084"
    },
    ...
]
```

### Software​

Metadata records about research software (includes the subtypes listed [here](http://api.openaire.eu/vocabularies/dnet:result_typologies/software)).

#### documentationUrls​

*Type: String • Cardinality: MANY*

The URLs to the software documentation.

```prism
"documentationUrls": [
    "https://github.com/openaire/iis/blob/master/README.markdown",
    ...
]
```

#### codeRepositoryUrl​

*Type: String • Cardinality: ONE*

The URL to the repository with the source code.

```prism
"codeRepositoryUrl": "https://github.com/openaire/iis"
```

#### programmingLanguage​

*Type: String • Cardinality: ONE*

The programming language.

```prism
"programmingLanguage": "Java"
```

### Other research product​

Metadata records about research products that cannot be classified as research literature, data or software (includes types of products listed [here](http://api.openaire.eu/vocabularies/dnet:result_typologies/other)).

#### contactPeople​

*Type: String • Cardinality: MANY*

Information on the person responsible for providing further information regarding the resource.

```prism
"contactPeople": [
    "Noémie Dominguez",
    ...
]
```

#### contactGroups​

*Type: String • Cardinality: MANY*

Information on the group responsible for providing further information regarding the resource.

```prism
"contactGroups": [
    "Networked Multimedia Information Systems (NeMIS)",
    ...
]
```

#### tools​

*Type: String • Cardinality: MANY*

Information about tool useful for the interpretation and/or re-use of the research product.


# Organizations

Organizations include companies, research centers or institutions involved as project partners or as responsible of operating data sources. Information about organizations are collected from funder databases like CORDA, registries of data sources like OpenDOAR and re3Data, and CRIS systems, as being related to projects or data sources.

## The Organization object

### id​

*Type: String • Cardinality: ONE*

The OpenAIRE id for the organization, created according to the [OpenAIRE entity identifier and PID mapping policy](https://graph.openaire.eu/docs/data-model/pids-and-identifiers).

```prism
"id": "openorgs____::b84450f9864182c67b8611b5593f4250"
```

### legalShortName​

*Type: String • Cardinality: ONE*

The legal name in short form of the organization.

```prism
"legalShortName": "ARC"
```

### legalName​

*Type: String • Cardinality: ONE*

The legal name of the organization.

```prism
"legalName": "Athena Research and Innovation Center In Information Communication & Knowledge Technologies"
```

### alternativeNames​

*Type: String • Cardinality: MANY*

Alternative names that identify the organization.

```prism
"alternativeNames": [
    "Athena Research and Innovation Center In Information Communication & Knowledge Technologies",
    "Athena RIC",
    "ARC",
    ...
]
```

### websiteUrl​

*Type: String • Cardinality: ONE*

The websiteurl of the organization.

```prism
"websiteUrl": "https://www.athena-innovation.gr/el/announce/pressreleases.html"
```

### country​

*Type: [Country](https://graph.openaire.eu/docs/data-model/entities/other#country) • Cardinality: ONE*

The country where the organization is located.

```prism
"country":{
    "code": "GR",
    "label": "Greece"
}
```

### pids​

*Type: [OrganizationPid](https://graph.openaire.eu/docs/data-model/entities/other#organizationpid) • Cardinality: MANY*

The list of persistent identifiers for the organization.

```prism
"pids": [
    {
        "scheme": "ISNI",
        "value": "0000 0004 0393 5688"
    },
    {
        "scheme": "GRID",
        "value": "grid.19843.37"
    },
    ...
]
```

# Data sources

OpenAIRE entity instances are created out of data collected from various data sources of different kinds, such as publication repositories, research data archives, CRIS systems, funder databases, etc. Data sources export information packages (e.g., XML records, HTTP responses, RDF data, JSON) that may contain information on one or more of such entities and possibly relationships between them.

For example, a metadata record about a project carries information for the creation of a Project entity and its participants (as Organization entities). It is important, once each piece of information is extracted from such packages and inserted into the OpenAIRE information space as an entity, for such pieces to keep provenance information relative to the originating data source. This is to give visibility to the data source, but also to enable the reconstruction of the very same piece of information if problems arise.

## The DataSource object

### id​

*Type: String • Cardinality: ONE*

The OpenAIRE id of the data source, created according to the [OpenAIRE entity identifier and PID mapping policy](https://graph.openaire.eu/docs/data-model/pids-and-identifiers).

```prism
"id": "issn___print::22c514d022b199c346e7f29ca06efc95"
```

### originalIds​

*Type: String • Cardinality: MANY*

The list of original identifiers associated to the datasource.

```prism
"originalIds": [
    "issn___print::2451-8271",
    ...
]
```

### pids​

*Type: [ControlledField](https://graph.openaire.eu/docs/data-model/entities/other#controlledfield) • Cardinality: MANY*

The persistent identifiers for the datasource.

```prism
"pids": [
    {
        "scheme": "DOI",
        "value": "10.5281/zenodo.4707307"
    },
    ...
]
```

### type​

*Type: [ControlledField](https://graph.openaire.eu/docs/data-model/entities/other#controlledfield) • Cardinality: ONE*

The datasource type; see the vocabulary [dnet:datasource\_typologies](https://api.openaire.eu/vocabularies/dnet:datasource_typologies).

```prism
"type": {
    "scheme": "pubsrepository::journal",
    "value": "Journal"
}
```

### openaireCompatibility​

*Type: String • Cardinality: ONE*

The OpenAIRE compatibility of the ingested research products, indicates which guidelines they are compliant according to the vocabulary [dnet:datasourceCompatibilityLevel](https://api.openaire.eu/vocabularies/dnet:datasourceCompatibilityLevel).

```prism
"openaireCompatibility": "collected from a compatible aggregator"
```

### officialName​

*Type: String • Cardinality: ONE*

The official name of the datasource.

```prism
"officialBame": "Recent Patents and Topics on Medical Imaging"
```

### englishName​

*Type: String • Cardinality: ONE*

The English name of the datasource.

```prism
"englishName": "Recent Patents and Topics on Medical Imaging"
```

### websiteUrl​

*Type: String • Cardinality: ONE*

The URL of the website of the datasource.

```prism
"websiteUrl": "http://dspace.unict.it/"
```

### logoUrl​

*Type: String • Cardinality: ONE*

The URL of the logo for the datasource.

```prism
"logoUrl": "https://impactum-journals.uc.pt/public/journals/26/pageHeaderLogoImage_en_US.png"
```

### dateOfValidation​

*Type: String • Cardinality: ONE*

The date of validation against the OpenAIRE guidelines for the datasource records.

```prism
"dateOfValidation": "2016-10-10"
```

### description​

*Type: String • Cardinality: ONE*

The description for the datasource.

```prism
"description": "Recent Patents on Medical Imaging publishes review and research articles, and guest edited single-topic issues on recent patents in the field of medical imaging. It provides an important and reliable source of current information on developments in the field. The journal is essential reading for all researchers involved in Medical Imaging."
```

### subjects​

*Type: String • Cardinality: MANY*

List of subjects associated to the datasource

```prism
"subjects": [
    "Medicine",
    "Imaging",
    ...
]
```

### languages​

*Type: String • Cardinality: MANY*

The languages present in the data source's content, as defined by OpenDOAR.

```prism
"languages": [
    "eng",
    ...
]
```

### contentTypes​

*Type: String • Cardinality: MANY*

Types of content in the data source, as defined by OpenDOAR

```prism
"contentTypes": [
    "Journal articles",
    ...
]
```

### releaseStartDate​

*Type: String • Cardinality: ONE*

Releasing date of the data source, as defined by re3data.org.

```prism
"releaseStartDate": "2010-07-24"
```

### releaseEndDate​

*Type: String • Cardinality: ONE*

Date when the data source went offline or stopped ingesting new research data. As defined by re3data.org

```prism
"releaseEndDate": "2016-03-28"
```

### accessRights​

*Type: String • Cardinality: ONE*

Type of access to the data source, as defined by re3data.org. Possible values: `{ open, restricted, closed }`.

```prism
"accessRights": "open"
```

### uploadRights​

*Type: String • Cardinality: ONE*

Type of data upload, as defined by re3data.org; one of `{ open, restricted, closed }`.

```prism
"uploadRights": "closed"
```

### databaseAccessRestriction​

*Type: String • Cardinality: ONE*

Access restrictions to the research data repository. Allowed values are: `{ feeRequired, registration, other }`.

This field only applies for re3data data source; see [re3data schema specification](https://gfzpublic.gfz-potsdam.de/rest/items/item_758898_6/component/file_775891/content) for more details.

```prism
"databaseAccessRestriction": "registration"
```

### dataUploadRestriction​

*Type: String • Cardinality: ONE*

Upload restrictions applied by the datasource, as defined by re3data.org. One of `{ feeRequired, registration, other }`.

This field only applies for re3data data source; see [re3data schema specification](https://gfzpublic.gfz-potsdam.de/rest/items/item_758898_6/component/file_775891/content) for more details.

```prism
"dataUploadRestriction": "feeRequired registration"
```

### versioning​

*Type: Boolean • Cardinality: ONE*

Whether the research data repository supports versioning: `yes` if the data source supports versioning, `no` otherwise.

This field only applies for re3data data source; see [re3data schema specification](https://gfzpublic.gfz-potsdam.de/rest/items/item_758898_6/component/file_775891/content) for more details.

```prism
"versioning": true
```

### citationGuidelineUrl​

*Type: String • Cardinality: ONE*

The URL of the data source providing information on how to cite its items. The DataCite citation format is recommended ([http://www.datacite.org/whycitedata](http://www.datacite.org/whycitedata)).

This field only applies for re3data data source; see [re3data schema specification](https://gfzpublic.gfz-potsdam.de/rest/items/item_758898_6/component/file_775891/content) for more details.

```prism
"citationGuidelineUrl": "https://physionet.org/about/#citation"
```

### pidSystems​

*Type: String • Cardinality: ONE*

The persistent identifier system that is used by the data source. As defined by re3data.org.

```prism
"pidSystems": "hdl"
```

### certificates​

*Type: String • Cardinality: ONE*

The certificate, seal or standard the data source complies with. As defined by re3data.org.

```prism
"certificates": "WDS"
```

### policies​

*Type: String • Cardinality: MANY*

Policies of the data source, as defined in OpenDOAR.

### journal​

*Type: [Container](https://graph.openaire.eu/docs/data-model/entities/other#container) • Cardinality: ONE*

Information about the journal, if this data source is of type Journal.

```prism
"journal": {
    "edition": "",
    "iss": "5",
    "issnLinking": "",
    "issnOnline": "1873-7625",
    "issnPrinted":"2451-8271",
    "name": "Recent Patents and Topics on Imaging",
    "sp": "12",
    "ep": "22",
    "vol": "50"
}
```

### missionStatementUrl​

*Type: String • Cardinality: ONE*

The URL of a mission statement describing the designated community of the data source. As defined by re3data.org

```prism
"missionStatementUrl": "https://www.sigma2.no/content/nird-research-data-archive"
```


# Projects

Of crucial interest to OpenAIRE is also the identification of the funders (e.g. European Commission, WellcomeTrust, FCT Portugal, NWO The Netherlands) that co-funded the projects that have led to a given research product. Projects are characterized by a list of funding streams (e.g. FP7, H2020 for the EC), which identify the strands of fundings. Funding streams can be nested to form a tree of sub-funding streams.

## The Project object

### id​

*Type: String • Cardinality: ONE*

Main entity identifier, created according to the [OpenAIRE entity identifier and PID mapping policy](https://graph.openaire.eu/docs/data-model/pids-and-identifiers).

```prism
"id": "corda__h2020::70ea22400fd890c5033cb31642c4ae68"
```

### code​

*Type: String • Cardinality: ONE*

Τhe grant agreement code of the project.

```prism
"code": "777541"
```

### acronym​

*Type: String • Cardinality: ONE*

Project's acronym.

```prism
"acronym": "OpenAIRE-Advance"
```

### title​

*Type: String • Cardinality: ONE*

Project's title.

```prism
"title": "OpenAIRE Advancing Open Scholarship"
```

### callIdentifier​

*Type: String • Cardinality: ONE*

The identifier of the research call.

```prism
"callIdentifier": "H2020-EINFRA-2017"\`
```

### fundings​

*Type: [Funding](https://graph.openaire.eu/docs/data-model/entities/other#funding) • Cardinality: MANY*

Funding information for the project.

```prism
"fundings": [
    {
        "fundingStream": {
            "description": "Horizon 2020 Framework Programme - Research and Innovation action",
            "id": "EC::H2020::RIA"
        },
        "jurisdiction": "EU",
        "name": "European Commission",
        "shortName": "EC"
    }
]
```

### granted​

*Type: [Grant](https://graph.openaire.eu/docs/data-model/entities/other#grant) • Cardinality: ONE*

The money granted to the project.

```prism
"granted": {
    "currency": "EUR",
    "fundedAmount": 1.0E7,
    "totalCost": 1.0E7
}
```

### h2020Programmes​

*Type: [H2020Programme](https://graph.openaire.eu/docs/data-model/entities/other#h2020programme) • Cardinality: MANY*

The H2020 programme funding the project.

```prism
"h2020Programmes":[
    {
        "code": "H2020-EU.1.4.1.3.",
        "description": "Development, deployment and operation of ICT-based e-infrastructures"
    }
]
```

### keywords​

*Type: String • Cardinality: ONE*

```prism
"keywords": "Aquaculture,NMR,Metabolomics,Microbiota,..."
```

### openAccessMandateForDataset​

*Type: Boolean • Cardinality: ONE*

```prism
"openAccessMandateForDataset": true
```

### openAccessMandateForPublications​

*Type: Boolean • Cardinality: ONE*

```prism
"openAccessMandateForPublications": true
```

### startDate​

*Type: String • Cardinality: ONE*

The start year of the project.

```prism
"startDate": "2018-01-01"
```

### endDate​

*Type: String • Cardinality: ONE*

The end year pf the project.

```prism
"endDate": "2021-02-28"
```

### subjects​

*Type: String • Cardinality: MANY*

The subjects of the project

```prism
"subjects": [
    "Data and Distributed Computing e-infrastructures for Open Science",
    ...
]
```

### summary​

*Type: String • Cardinality: ONE*

Short summary of the project.

```prism
"summary": "OpenAIRE-Advance continues the mission of OpenAIRE to support the Open Access/Open Data mandates in Europe. By sustaining the current successful infrastructure, comprised of a human network and robust technical services, it consolidates its achievements while working to shift the momentum among its communities to Open Science, aiming to be a trusted e-Infrastructurewithin the realms of the European Open Science Cloud.In this next phase, OpenAIRE-Advance strives to empower its National Open Access Desks (NOADs) so they become a pivotal part within their own national data infrastructures, positioningOA and open science onto national agendas. The capacity building activities bring together experts ontopical task groups in thematic areas(open policies, RDM, legal issues, TDM), promoting a train the trainer approach, strengthening and expanding the pan-European Helpdesk with support and training toolkits, training resources and workshops.It examines key elements of scholarly communication, i.e., co-operative OA publishing and next generation repositories, to develop essential building blocks of the scholarly commons.On the technical level OpenAIRE-Advance focuses on the operation and maintenance of the OpenAIRE technical TRL8/9 services,and radically improvesthe OpenAIRE services on offer by: a) optimizing their performance and scalability, b) refining their functionality based on end-user feedback, c) repackagingthem into products, taking a professional marketing approach  with well-defined KPIs, d)consolidating the range of services/products into a common e-Infra catalogue to enable a wider uptake.OpenAIRE-Advancesteps up its outreach activities with concrete pilots with three major RIs,citizen science initiatives, and innovators via a rigorous Open Innovation programme. Finally, viaits partnership with COAR, OpenAIRE-Advance consolidatesOpenAIRE’s global roleextending its collaborations with Latin America, US, Japan, Canada, and Africa."
```

### websiteUrl​

*Type: String • Cardinality: ONE*

The website of the project

```prism
"websiteUrl": "https://www.openaire.eu/advance/"
```



# -------------------------------------------------------
#
# C:\dev\AIREloom\reference\pyalex_reference.md
#
# ------------------------------------------------------

 PyAlex is a Python library for [OpenAlex](https://openalex.org/). OpenAlex is
 an index of hundreds of millions of interconnected scholarly papers, authors,
 institutions, and more. OpenAlex offers a robust, open, and free [REST API](https://docs.openalex.) to extract, aggregate, or search scholarly data.
 PyAlex is a lightweight and thin Python interface to this API. PyAlex tries to
 stay as close as possible to the design of the original service.

 The following features of OpenAlex are currently supported by PyAlex:

 - [x] Get single entities
 - [x] Filter entities
 - [x] Search entities
 - [x] Group entities
 - [x] Search filters
 - [x] Select fields
 - [x] Sample
 - [x] Pagination
 - [x] Autocomplete endpoint
 - [x] N-grams
 - [x] Authentication

 We aim to cover the entire API, and we are looking for help. We are welcoming Pull Requests.

 ## Key features

 - **Pipe operations** - PyAlex can handle multiple operations in a sequence. This allows the loper to write understandable queries. For examples, see [code snippets](#code-snippets).
 - **Plaintext abstracts** - OpenAlex [doesn't include plaintext abstracts](https://docs.openalex.org/entities/works/work-object#abstract_inverted_index) due to legal constraints. PyAlex can convert the rted abstracts into [plaintext abstracts on the fly](#get-abstract).
 - **Permissive license** - OpenAlex data is CC0 licensed :raised_hands:. PyAlex is published under MIT license.

 ## Installation

 PyAlex requires Python 3.8 or later.

 ```sh
 pip install pyalex
 ```

 ## Getting started

 PyAlex offers support for all [Entity Objects](https://docs.openalex.org/api-entities/ties-overview): [Works](https://docs.openalex.org/api-entities/works), [Authors](https://docs.openalex.api-entities/authors), [Sources](https://docs.openalex.org/api-entities/sourcese), [Institutions]ps://docs.openalex.org/api-entities/institutions), [Topics](https://docs.openalex.org/api-entities/cs), [Publishers](https://docs.openalex.org/api-entities/publishers), and [Funders](https://docs.alex.org/api-entities/funders).

 ```python
 from pyalex import Works, Authors, Sources, Institutions, Topics, Publishers, Funders
 ```

 ### The polite pool

 [The polite pool](https://docs.openalex.org/how-to-use-the-api/-limits-and-authentication#the-polite-pool) has much
 faster and more consistent response times. To get into the polite pool, you
 set your email:

 ```python
 import pyalex

 pyalex.config.email = "mail@example.com"
 ```

 ### Max retries

 By default, PyAlex will raise an error at the first failure when querying the OpenAlex API. You can `max_retries` to a number higher than 0 to allow PyAlex to retry when an error occurs. ry_backoff_factor` is related to the delay between two retry, and `retry_http_codes` are the HTTP r codes that should trigger a retry.

 ```python
 from pyalex import config

 config.max_retries = 0
 config.retry_backoff_factor = 0.1
 config.retry_http_codes = [429, 500, 503]
 ```

 ### Get single entity

 Get a single Work, Author, Source, Institution, Concept, Topic, Publisher or Funder from OpenAlex by
 OpenAlex ID, or by DOI or ROR.

 ```python
 Works()["W2741809807"]

 # same as
 Works()["https://doi.org/10.7717/peerj.4375"]
 ```

 The result is a `Work` object, which is very similar to a dictionary. Find the available fields with ys()`.

 For example, get the open access status:

 ```python
 Works()["W2741809807"]["open_access"]
 ```

 ```python
 {'is_oa': True, 'oa_status': 'gold', 'oa_url': 'https://doi.org/10.7717/peerj.4375'}
 ```

 The previous works also for Authors, Sources, Institutions, Concepts and Topics

 ```python
 Authors()["A5027479191"]
 Authors()["https://orcid.org/0000-0002-4297-0502"]  # same
 ```

 #### Get random

 Get a [random Work, Author, Source, Institution, Concept, Topic, Publisher or Funder](https://docs.lex.org/how-to-use-the-api/get-single-entities/random-result).

 ```python
 Works().random()
 Authors().random()
 Sources().random()
 Institutions().random()
 Topics().random()
 Publishers().random()
 Funders().random()
 ```

 #### Get abstract

 Only for Works. Request a work from the OpenAlex database:

 ```python
 w = Works()["W3128349626"]
 ```

 All attributes are available like documented under [Works](https://docs.openalex.org/api-entities//work-object), as well as `abstract` (only if `abstract_inverted_index` is not None). This abstract human readable is create on the fly.

 ```python
 w["abstract"]
 ```

 ```python
 'Abstract To help researchers conduct a systematic review or meta-analysis as efficiently and parently as possible, we designed a tool to accelerate the step of screening titles and abstracts. For tasks—including but not limited to systematic reviews and meta-analyses—the scientific literature  to be checked systematically. Scholars and practitioners currently screen thousands of studies by to determine which studies to include in their review or meta-analysis. This is error prone and icient because of extremely imbalanced data: only a fraction of the screened studies is relevant. The e of systematic reviewing will be an interaction with machine learning algorithms to deal with the ous increase of available text. We therefore developed an open source machine learning-aided pipeline ing active learning: ASReview. We demonstrate by means of simulation studies that active learning can  far more efficient reviewing than manual reviewing while providing high quality. Furthermore, we ibe the options of the free and open source research software and present the results from user ience tests. We invite the community to contribute to open source projects such as our own that de measurable and reproducible improvements over current practice.'
 ```

 Please respect the legal constraints when using this feature.

 ### Get lists of entities

 ```python
 results = Works().get()
 ```

 For lists of entities, you can also `count` the number of records found
 instead of returning the results. This also works for search queries and
 filters.

 ```python
 Works().count()
 # 10338153
 ```

 For lists of entities, you can return the result as well as the metadata. By default, only the ts are returned.

 ```python
 topics = Topics().get()
 ```

 ```python
 print(topics.meta)
 {'count': 65073, 'db_response_time_ms': 16, 'page': 1, 'per_page': 25}
 ```

 #### Filter records

 ```python
 Works().filter(publication_year=2020, is_oa=True).get()
 ```

 which is identical to:

 ```python
 Works().filter(publication_year=2020).filter(is_oa=True).get()
 ```

 #### Nested attribute filters

 Some attribute filters are nested and separated with dots by OpenAlex. For
 example, filter on [`authorships.institutions.ror`](https://docs.openalex.org/api-entities/works/r-works).

 In case of nested attribute filters, use a dict to build the query.

 ```python
 Works()
   .filter(authorships={"institutions": {"ror": "04pp8hn57"}})
   .get()
 ```

 #### Search entities

 OpenAlex reference: [The search parameter](https://docs.openalex.org/api-entities/works/search-works)

 ```python
 Works().search("fierce creatures").get()
 ```

 #### Search filter

 OpenAlex reference: [The search filter](https://docs.openalex.org/api-entities/works/h-works#search-a-specific-field)

 ```python
 Authors().search_filter(display_name="einstein").get()
 ```

 ```python
 Works().search_filter(title="cubist").get()
 ```

 ```python
 Funders().search_filter(display_name="health").get()
 ```


 #### Sort entity lists

 OpenAlex reference: [Sort entity lists](https://docs.openalex.org/api-entities/works/ists-of-works#page-and-sort-works).

 ```python
 Works().sort(cited_by_count="desc").get()
 ```

 #### Select

 OpenAlex reference: [Select fields](https://docs.openalex.org/how-to-use-the-api/ists-of-entities/select-fields).

 ```python
 Works().filter(publication_year=2020, is_oa=True).select(["id", "doi"]).get()
 ```

 #### Sample

 OpenAlex reference: [Sample entity lists](https://docs.openalex.org/how-to-use-the-api/ists-of-entities/sample-entity-lists).

 ```python
 Works().sample(100, seed=535).get()
 ```

 #### Logical expressions

 OpenAlex reference: [Logical expressions](https://docs.openalex.org/how-to-use-the-api/ists-of-entities/filter-entity-lists#logical-expressions)

 Inequality:

 ```python
 Sources().filter(works_count=">1000").get()
 ```

 Negation (NOT):

 ```python
 Institutions().filter(country_code="!us").get()
 ```

 Intersection (AND):

 ```python
 Works().filter(institutions={"country_code": ["fr", "gb"]}).get()

 # same
 Works().filter(institutions={"country_code": "fr"}).filter(institutions={"country_code": "gb"}).get()
 ```

 Addition (OR):

 ```python
 Works().filter(institutions={"country_code": "fr|gb"}).get()
 ```

 #### Paging

 OpenAlex offers two methods for paging: [basic (offset) paging](https://docs.openalex.org/o-use-the-api/get-lists-of-entities/paging#basic-paging) and [cursor paging](https://docs.openalex.org/o-use-the-api/get-lists-of-entities/paging#cursor-paging). Both methods are supported by PyAlex.

 ##### Cursor paging (default)

 Use the method `paginate()` to paginate results. Each returned page is a list
 of records, with a maximum of `per_page` (default 25). By default,
 `paginate`s argument `n_max` is set to 10000. Use `None` to retrieve all
 results.

 ```python
 from pyalex import Authors

 pager = Authors().search_filter(display_name="einstein").paginate(per_page=200)

 for page in pager:
     print(len(page))
 ```

 > Looking for an easy method to iterate the records of a pager?

 ```python
 from itertools import chain
 from pyalex import Authors

 query = Authors().search_filter(display_name="einstein")

 for record in chain(*query.paginate(per_page=200)):
     print(record["id"])
 ```

 ##### Basic paging

 See limitations of [basic paging](https://docs.openalex.org/how-to-use-the-api/get-lists-of-entities/g#basic-paging) in the OpenAlex documentation.

 ```python
 from pyalex import Authors

 pager = Authors().search_filter(display_name="einstein").paginate(method="page", per_page=200)

 for page in pager:
     print(len(page))
 ```


 ### Autocomplete

 OpenAlex reference: [Autocomplete entities](https://docs.openalex.org/how-to-use-the-api/ists-of-entities/autocomplete-entities).

 Autocomplete a string:
 ```python
 from pyalex import autocomplete

 autocomplete("stockholm resilience centre")
 ```

 Autocomplete a string to get a specific type of entities:
 ```python
 from pyalex import Institutions

 Institutions().autocomplete("stockholm resilience centre")
 ```

 You can also use the filters to autocomplete:
 ```python
 from pyalex import Works

 r = Works().filter(publication_year=2023).autocomplete("planetary boundaries")
 ```


 ### Get N-grams

 OpenAlex reference: [Get N-grams](https://docs.openalex.org/api-entities/works/get-n-grams).


 ```python
 Works()["W2023271753"].ngrams()
 ```


 ### Serialize

 All results from PyAlex can be serialized. For example, save the results to a JSON file:

 ```python
 import json
 from pathlib import Path
 from pyalex import Work

 with open(Path("works.json"), "w") as f:
     json.dump(Works().get(), f)

 with open(Path("works.json")) as f:
     works = [Work(w) for w in json.load(f)]
 ```

 ## Code snippets

 A list of awesome use cases of the OpenAlex dataset.

 ### Cited publications (works referenced by this paper, outgoing citations)

 ```python
 from pyalex import Works

 # the work to extract the referenced works of
 w = Works()["W2741809807"]

 Works()[w["referenced_works"]]
 ```

 ### Citing publications (other works that reference this paper, incoming citations)

 ```python
 from pyalex import Works
 Works().filter(cites="W2741809807").get()
 ```

 ### Get works of a single author

 ```python
 from pyalex import Works

 Works().filter(author={"id": "A2887243803"}).get()
 ```

 ### Dataset publications in the global south

 ```python
 from pyalex import Works

 # the work to extract the referenced works of
 w = Works() \
   .filter(institutions={"is_global_south":True}) \
   .filter(type="dataset") \
   .group_by("institutions.country_code") \
   .get()

 ```

 ### Most cited publications in your organisation

 ```python
 from pyalex import Works

 Works() \
   .filter(authorships={"institutions": {"ror": "04pp8hn57"}}) \
   .sort(cited_by_count="desc") \
   .get()

 ```



