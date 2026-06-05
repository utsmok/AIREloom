"""Reusable Pydantic annotated types that make API data safe to traverse.

- ``SafeList[T]`` — coerces ``None`` → ``[]``, filters null elements
- ``SafeStr`` — coerces ``None`` → ``""``
 - ``SafeModel`` aliases — coerce ``None`` → ``Model()`` (defined per-file)

Every type uses ``BeforeValidator`` so coercion happens *before* Pydantic's
core validation. This means:

* ``model_validate({"field": null})`` → field is ``[]`` / ``""`` / empty model
* ``model_validate({"field": [null, {...}]})`` → null elements stripped
* ``model_validate({})`` → ``default_factory`` / ``default`` kicks in
"""

from typing import Annotated, TypeVar

from pydantic import BeforeValidator

T = TypeVar("T")

# ---------------------------------------------------------------------------
# SafeList — list fields that are never None and never contain null elements
# ---------------------------------------------------------------------------

SafeList = Annotated[
    list[T],
    BeforeValidator(lambda v: [] if v is None else [x for x in v if x is not None]),
]
"""Annotated type for list fields that coerce ``None`` → ``[]`` and strip null entries.

Usage::

    class Product(BaseModel):
        pids: SafeList[Pid] = Field(default_factory=list)
        keywords: SafeList[str] = Field(default_factory=list)

Iterable without guards::

    [pid.value for pid in product.pids]  # always works
"""

# ---------------------------------------------------------------------------
# SafeStr — string fields that are never None
# ---------------------------------------------------------------------------

SafeStr = Annotated[str, BeforeValidator(lambda v: "" if v is None else v)]
"""Annotated type for string fields that coerce ``None`` → ``""``.

Usage::

    class Container(BaseModel):
        name: SafeStr = ""

Safe to call string methods without guards::

    product.title.upper()  # never crashes
"""

# ---------------------------------------------------------------------------
# SafeModel aliases — nested model fields that are never None
# ---------------------------------------------------------------------------

# NOTE: Due to type checker restrictions, function calls cannot appear in
# type annotations. Instead of calling safe_model() inline, define a
# module-level type alias after the model class:
#
#     from typing import Annotated
#     from pydantic import BeforeValidator
#
#     class Container(BaseModel):
#         name: SafeStr = ""
#
#     SafeContainer = Annotated[Container, BeforeValidator(lambda v: Container() if v is None else v)]
#
#     class Product(BaseModel):
#         container: SafeContainer = Field(default_factory=Container)
#
# This pattern is used throughout aireloom/models/ for each nested model
# that should never be None.
