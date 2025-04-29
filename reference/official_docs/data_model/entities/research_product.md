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