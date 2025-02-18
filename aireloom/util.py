from collections import UserDict
from typing import Any

class SafeDict(UserDict):
    """
    A dictionary-like class that allows configurable default return values
    for missing keys.

    It uses a `_default_values` mapping (dictionary) to store default
    return values for specific keys. If a key is not found and it's
    in `_default_values`, the configured default is returned.
    If the key is not found and not in `_default_values`, it returns
    a fallback default (which is an empty list by default, but can be overridden).
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

