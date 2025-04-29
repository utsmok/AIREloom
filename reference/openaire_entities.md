

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
