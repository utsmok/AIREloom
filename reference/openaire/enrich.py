from dataclasses import dataclass, field

from db.duckdb import DuckDBInstance

from .mappings import OAIREEndpoint
from .queries import OAIREQuerySet


@dataclass
class OAEnricher:
    # BaseEnricher protocol
    db: DuckDBInstance
    queryset: dict[OAIREEndpoint, OAIREQuerySet] = field(
        default_factory=dict, init=False
    )

    def retrieve_related_items(self, table_name: str) -> None:
        """
        For a given table name in the DB instance,
        retrieve all fields in the table that hold a retrievable id, and then retrieve them using a queryset.
        """
