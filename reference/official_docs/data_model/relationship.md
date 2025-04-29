
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

