def default_validation() -> callable:
    return lambda x: x if x else ""

class BaseEndpoint:
    url = "https://api.openaire.eu/graph/"
    params: dict = {
        "debugQuery": False,
        "page": 1,
        "pageSize": 10,
        "cursor": '*'
    }
    valid_filters:dict[str, callable] = {} # dict with valid filter names and validation functions for this endpoint


    # generic functions here!

    def _update_params(self, **kwargs):
        """
        Updates self.params with kwargs.
        Note: validation should happen before using this method

        In case of conflicts, will overwrite existing values
        """
        for k, v in kwargs.items():
            self.params[k] = v

    # filtering
    # TODO:
    # include AND OR NOT operators, used by combining param values with e.g. whitespaceANDwhitespace: val1 AND val2
    # enclose vals in double quotes if they contain whitespace
    # each implementation class has list of valid params for filter

    def filter(self, **kwargs):
        self._verify_filters(**kwargs)
        self.params = kwargs

    def _verify_filters(self, **kwargs):
        for k, v in kwargs.items():
            if k not in self.valid_filters:
                raise ValueError(f"Invalid filter: {k}")
            if not self.valid_filters[k](v):
                raise ValueError(f"Invalid filter value: {v}")

    def sort(self, **kwargs):
        ...

        """
        sortBy
        Defines the field and the sort direction.
        See researchProducts for details

        set final data as param
        """
    # paging

class researchProducts(BaseEndpoint):
    url = "https://api.openaire.eu/graph/researchProducts/"

    # TODO: add more validation functions
    valid_filters:dict[str, callable] = {
        "search": default_validation, #searchfield
        "mainTitle": default_validation, #searchfield
        "description": default_validation, #searchfield
        "id":validate_openaire_id,
        "pid":default_validation,
        "originalId":default_validation,
        "type":validate_enum_type,
        "fromPublicationDate":validate_date,
        "toPublicationDate":validate_date,
        "subjects":default_validation,
        "countryCode":validate_country,
        "authorFullName":default_validation,
        "authorOrcid":validate_orcid,
        "publisher":default_validation,
        "bestOpenAccessRightLabel":validate_enum,
        "influenceClass":validate_enum,
        "impulseClass":validate_enum,
        "popularityClass":validate_enum,
        "citationCountClass":validate_enum,
        "instanceType":validate_enum,
        "sdg":validate_int,
        "fos":default_validation,
        "isPeerReviewed":validate_bool,
        "isInDiamondJournal":validate_bool,
        "isPubliclyFunded":validate_bool,
        "isGreen":validate_bool,
        "openAccessColor":validate_enum,
        "relOrganizationId":validate_openaire_id,
        "relCommunityId":validate_openaire_id,
        "relProjectId":validate_openaire_id,
        "relProjectCode":default_validation,
        "hasProjectRel":validate_bool,
        "relProjectFundingShortName":default_validation,
        "relProjectFundingStreamId":default_validation,
        "relHostingDataSourceId":validate_openaire_id,
        "relCollectedFromDatasourceId":validate_openaire_id,
        }

    # specific implementation here!

    """
    sortBy
    The field to set the sorting order of the results.
    Should be provided in the format
            fieldname sortDirection,
    where:
            sortDirection = [ASC, DESC]
            fieldname = [relevance, publicationDate, dateOfCollection, influence, popularity, citationCount, impulse]

    Multiple sorting parameters should be comma-separated.
    """
class organizations(BaseEndpoint):
    url = "https://api.openaire.eu/graph/organizations/"
    # specific implementation here!

    # sorting
    # see researchProducts, only available field is 'relevance'

class dataSources(BaseEndpoint):
    url = "https://api.openaire.eu/graph/dataSources/"
    # specific implementation here!

    # sorting
    # see researchProducts, only available field is 'relevance'

class projects(BaseEndpoint):
    url = "https://api.openaire.eu/graph/projects/"
    # specific implementation here!

    # sorting
    # see researchProducts. available fields are:
    # [relevance, startDate, endDate]


