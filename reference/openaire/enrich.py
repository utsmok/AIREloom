from collections import defaultdict
from ..base_classes import BaseEnricher, BaseQuery, BaseQuerySet
from db.duckdb import DuckDBInstance
from dataclasses import dataclass, field
from .queries import OAIREQuery, OAIREQuerySet
from .mappings import OAIREEndpoint
from rich import print

@dataclass
class OAEnricher:
    # BaseEnricher protocol
    db: DuckDBInstance
    queryset: dict[OAIREEndpoint, OAIREQuerySet] = field(default_factory=dict, init=False)

    def retrieve_related_items(self, table_name: str) -> None:
        """
        For a given table name in the DB instance,
        retrieve all fields in the table that hold a retrievable id, and then retrieve them using a queryset.
        """