from warnings import warn
from datetime import datetime
from aireloom.constants import COUNTRY_CODES
import re
"""
Validator functions for endpoint filters
"""



def default_validation() -> callable:
    return lambda x: x if x else None
def validate_date() -> callable:
    # date format should be
    return lambda x: x if any([isinstance(x, datetime), datetime.strptime(str(x), "%Y-%m-%dT%H:%M:%S.%fZ")]) else None
def validate_int() -> callable:
    return lambda x: x if any([isinstance(x,int), str(x).isnumeric()]) else None
def validate_bool() -> callable:
    return lambda x: bool(x) if any([isinstance(x, bool),str(x).lower() == "true", str(x).lower() == "false"]) else None
def validate_country() -> callable:
    return lambda x: x if isinstance(x,str) and len(x)==2 and x in COUNTRY_CODES else None
def validate_openaire_id() -> callable:
    warn("validate_openaire_id not implemented")
    return default_validation()
def validate_orcid() -> callable:
    return lambda x: x if re.match(r"\d{4}-\d{4}-\d{4}-\d{3}[\dX]", x) else None
def validate_enum_type() -> callable:
    return lambda x: x if isinstance(x, str) and x in ["publication","data","software","other"] else None
def validate_enum_open_access() -> callable:
    warn("validate_enum_open_access not implemented")
    return lambda x: x
def validate_enum_influence() -> callable:
    warn("validate_enum_influence not implemented")
    return lambda x: x
def validate_enum_impulse() -> callable:
    warn("validate_enum_impulse not implemented")
    return lambda x: x
def validate_enum_popularity() -> callable:
    warn("validate_enum_popularity not implemented")
    return lambda x: x
def validate_enum_citation_count() -> callable:
    warn("validate_enum_citation_count not implemented")
    return lambda x: x
def validate_enum_instance_type() -> callable:
    warn("validate_enum_instance_type not implemented")
    return lambda x: x
