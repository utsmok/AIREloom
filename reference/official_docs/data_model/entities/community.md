
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