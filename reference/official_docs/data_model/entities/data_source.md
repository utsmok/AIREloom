
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