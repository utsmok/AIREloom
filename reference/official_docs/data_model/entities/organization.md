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