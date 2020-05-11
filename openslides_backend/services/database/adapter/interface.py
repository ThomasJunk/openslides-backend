from typing import Any, Dict, List, Tuple

from mypy_extensions import TypedDict
from typing_extensions import Protocol

from openslides_backend.shared.interfaces import Filter
from openslides_backend.shared.patterns import Collection, FullQualifiedId

PartialModel = Dict[str, Any]
Found = TypedDict("Found", {"exists": bool, "position": int})
Count = TypedDict("Count", {"count": int, "position": int})
Aggregate = Dict[str, Any]


class Datastore(Protocol):
    """Datastore defines the interface to the datastore
    """

    def get(
        self, fqid: FullQualifiedId, mapped_fields: List[str] = None
    ) -> Tuple[PartialModel, int]:
        ...

    def getMany(
        self, collection: Collection, ids: List[int], mapped_fields: List[str] = None
    ) -> Tuple[Dict[int, PartialModel], int]:
        ...

    def getAll(
        self, collection: Collection, mapped_fields: List[str] = None
    ) -> List[PartialModel]:
        ...

    def filter(
        self,
        collection: Collection,
        filter: Filter,
        meeting_id: int = None,
        mapped_fields: List[str] = None,
    ) -> Tuple[Dict[int, PartialModel], int]:
        ...

    def exists(self, collection: Collection, filter: Filter) -> Found:
        ...

    def count(self, collection: Collection, filter: Filter) -> Count:
        ...

    def min(
        self, collection: Collection, filter: Filter, field: str, type: str = None
    ) -> Aggregate:
        ...

    def max(
        self, collection: Collection, filter: Filter, field: str, type: str = None
    ) -> Aggregate:
        ...
