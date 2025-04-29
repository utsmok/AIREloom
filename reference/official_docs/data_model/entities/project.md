
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
