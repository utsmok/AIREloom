"""Safe types — re-exported from bibliofabric with aireloom-specific notes.

See ``bibliofabric.safe_types`` for the canonical implementations of
``SafeList`` and ``SafeStr``.

SafeModel aliases
-----------------
Due to type checker restrictions, function calls cannot appear in type
annotations.  Instead of calling ``safe_model()`` inline, define a
module-level type alias after the model class::

    from typing import Annotated
    from pydantic import BeforeValidator


    class Container(BaseModel):
        name: SafeStr = ""


    SafeContainer = Annotated[
        Container,
        BeforeValidator(
            lambda v: Container() if v is None else v
        ),
    ]


    class Product(BaseModel):
        container: SafeContainer = Field(
            default_factory=Container
        )

This pattern is used throughout ``aireloom/models/`` for each nested model
that should never be ``None``.
"""

from bibliofabric.safe_types import SafeList, SafeStr

__all__ = ["SafeList", "SafeStr"]
