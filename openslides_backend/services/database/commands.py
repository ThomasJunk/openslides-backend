from typing import Any, Dict, List, Optional

from openslides_backend.shared.interfaces import Filter
from openslides_backend.shared.patterns import Collection, FullQualifiedId


class Command:
    """Command is the base class for commands used by the Engine interface
    """

    @property
    def data(self) -> Any:
        pass

    def __eq__(self, other: Any) -> bool:
        return self.data == other.data


class Get(Command):
    """Get command
    """

    def __init__(self, fqid: FullQualifiedId, mappedFields: Optional[List[str]]):
        self.fqid = fqid
        self.mappedFields = mappedFields

    @property
    def data(self) -> Dict[str, Any]:
        return {"fqid": self.fqid, "mapped_fields": self.mappedFields}


class GetMany(Command):
    """GetMany command
    """

    def __init__(
        self, collection: Collection, mapped_fields: Optional[List[str]], ids: List[int]
    ):
        self.collection = collection
        self.mapped_fields = mapped_fields
        self.ids = ids

    @property
    def data(self) -> Dict[str, Any]:
        return {
            "requests": [
                {
                    "collection": self.collection,
                    "mapped_fields": self.mapped_fields,
                    "ids": self.ids,
                }
            ]
        }


class GetAll(Command):
    """GetAll command
    """

    def __init__(self, collection: Collection, mapped_fields: Optional[List[str]]):
        self.collection = collection
        self.mapped_fields = mapped_fields

    @property
    def data(self) -> Dict[str, Any]:
        return {"collection": self.collection, "mapped_fields": self.mapped_fields}


class Exists(Command):
    """Exists command
    """

    def __init__(self, collection: Collection, filter: Filter):
        self.collection = collection
        self.filter = filter

    @property
    def data(self) -> Dict[str, Any]:
        return {"collection": self.collection, "filter": self.filter.to_dict()}


class Count(Command):
    """Count command
    """

    def __init__(self, collection: Collection, filter: Filter):
        self.collection = collection
        self.filter = filter

    @property
    def data(self) -> Dict[str, Any]:
        return {"collection": self.collection, "filter": self.filter.to_dict()}


class Min(Command):
    """Min command
    """

    def __init__(
        self, collection: Collection, filter: Filter, field: str, type: Optional[str]
    ):
        self.collection = collection
        self.filter = filter
        self.field = field
        self.type = type

    @property
    def data(self) -> Dict[str, Any]:
        result = {
            "collection": self.collection,
            "filter": self.filter.to_dict(),
            "field": self.field,
        }
        if self.type is not None:
            result["type"] = self.type
        return result


class Max(Command):
    """Max command
    """

    def __init__(
        self, collection: Collection, filter: Filter, field: str, type: Optional[str]
    ):
        self.collection = collection
        self.filter = filter
        self.field = field
        self.type = type

    @property
    def data(self) -> Dict[str, Any]:
        result = {
            "collection": self.collection,
            "filter": self.filter.to_dict(),
            "field": self.field,
        }
        if self.type is not None:
            result["type"] = self.type
        return result
