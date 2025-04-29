
from aireloom.base_classes import BaseEndpoint
from aireloom.validators import (
    default_validation,
    validate_openaire_id,
    validate_date,
    validate_country,
    validate_orcid,
    validate_int,
    validate_bool,
    validate_enum_type,
    validate_enum_open_access,
    validate_enum_influence,
    validate_enum_impulse,
    validate_enum_popularity,
    validate_enum_citation_count,
    validate_enum_instance_type
)

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
        "bestOpenAccessRightLabel":validate_enum_open_access,
        "influenceClass":validate_enum_influence,
        "impulseClass":validate_enum_impulse,
        "popularityClass":validate_enum_popularity,
        "citationCountClass":validate_enum_citation_count,
        "instanceType":validate_enum_instance_type,
        "sdg":validate_int,
        "fos":default_validation,
        "isPeerReviewed":validate_bool,
        "isInDiamondJournal":validate_bool,
        "isPubliclyFunded":validate_bool,
        "isGreen":validate_bool,
        "openAccessColor":validate_enum_open_access,
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
