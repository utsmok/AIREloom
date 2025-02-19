from collections import UserDict
from typing import Any

class BaseEndpoint:
    """
    Base class for API endpoints. This class and its subclasses are the primary method to interact with the OpenAIRE API.
    The core functionality is to parse input to parameters that are passed to an httpx client, which retrieves the data from the API,
    and returns it as an OpenAIRE entity.

    This base class is not meant to be used directly, but rather subclassed by specific endpoints, e.g. researchProducts, organizations, etc.
    """

    url = "https://api.openaire.eu/graph/"
    params: dict = {
        "debugQuery": False,
        "page": 1,
        "pageSize": 10,
        "cursor": '*'
    }
    valid_filters:dict[str, callable] = {} # dict with valid filter names and validation functions for this endpoint


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

    # sorting
    # TODO: implement sorting
    def sort(self, **kwargs):
        ...

        """
        sortBy
        Defines the field and the sort direction.
        See researchProducts for details

        set final data as param
        """

    # paging
    # should work 'by default' I think?


class SafeDict(UserDict):
    """
    A dictionary-like class that allows configurable default return values
    for missing keys.

    It uses a `_default_values` mapping (dictionary) to store default
    return values for specific keys. If a key is not found and it's
    in `_default_values`, the configured default is returned.
    If the key is not found and not in `_default_values`, it returns
    a fallback default (which is an empty list by default, but can be overridden).

    Used as a base class for entities.
    """

    fallback_default: Any = list()

    def __init__(self, data: dict = None, default_values: dict = None, fallback_default: Any = list()) -> None:
        """
        Initialize ConfigurableSafeDict.

        Args:
            data (dict, optional): Initial data for the dictionary.
            default_values (dict, optional): A dictionary mapping keys to their
                default return values when the key is missing.
            fallback_default (any, optional): The default value to return if a key is missing
                and not found in `default_values`. Overrides the class-level `fallback_default`.
                Defaults to list().
        """
        super().__init__(data)
        self._default_values: dict[str, Any] = default_values if default_values is not None else dict()
        if fallback_default is not None:
            self.fallback_default = fallback_default # Instance level fallback override

    def __getitem__(self, key) -> Any:
        """
        Overrides __getitem__ to return configured default or fallback default if key is missing.
        """
        try:
            return super().__getitem__(key)  # Try to get the item normally
        except KeyError:
            if key in self._default_values:
                return self._default_values[key]  # Return configured default
            else:
                return self.fallback_default  # Return fallback default

    def get(self, key, default=None) -> Any:
        """
        Overrides get method to prioritize configured default, then provided default, then fallback default.
        """
        if key in self:
            return super().get(key)
        elif key in self._default_values:
            return self._default_values[key]
        elif default is not None:
            return default
        else:
            return self.fallback_default

class BaseEntity(SafeDict):
    """
    The base class for all OpenAIRE entities, like ResearchProduct, Organization, etc.
    """
    ...
