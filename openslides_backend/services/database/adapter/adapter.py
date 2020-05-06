from typing import Dict, List, Tuple

import openslides_backend.services.database.commands as commands
from openslides_backend.services.database.engine import Engine
from openslides_backend.shared.interfaces import Filter, LoggingModule
from openslides_backend.shared.patterns import Collection, FullQualifiedId

from .interface import Aggregate, Count, Found, PartialModel


class Adapter:
    """
    Adapter to connect to (read-only) database.
    """

    def __init__(self, adapter: Engine, logging: LoggingModule) -> None:
        self.logger = logging.getLogger(__name__)
        self.adapter = adapter

    def get(
        self, fqid: FullQualifiedId, mapped_fields: List[str] = None
    ) -> Tuple[PartialModel, int]:
        command = commands.Get(fqid=fqid, mappedFields=mapped_fields)
        self.logger.debug(
            f"Start request to database with the following data: {command.data}"
        )
        response = self.adapter.get(command)
        return (response, 0)

    def getMany(
        self, collection: Collection, ids: List[int], mapped_fields: List[str] = None
    ) -> Dict[str, PartialModel]:
        command = commands.GetMany(
            collection=collection, ids=ids, mapped_fields=mapped_fields
        )
        self.logger.debug(
            f"Start request to database with the following data: {command.data}"
        )
        response = self.adapter.getMany(command)
        return response

    def getAll(
        self, collection: Collection, mapped_fields: List[str] = None
    ) -> List[PartialModel]:
        command = commands.GetAll(collection=collection, mapped_fields=mapped_fields)
        self.logger.debug(
            f"Start request to database with the following data: {command.data}"
        )
        response = self.adapter.getAll(command)
        return response

    def filter(
        self,
        collection: Collection,
        filter: Filter,
        meeting_id: int = None,
        mapped_fields: List[str] = None,
    ) -> Tuple[Dict[int, PartialModel], int]:
        raise

    def exists(self, collection: Collection, filter: Filter) -> Found:
        command = commands.Exists(collection=collection, filter=filter)
        self.logger.debug(
            f"Start request to database with the following data: {command.data}"
        )
        response = self.adapter.exists(command)
        return {"exists": response["exists"], "position": response["position"]}

    def count(self, collection: Collection, filter: Filter) -> Count:
        command = commands.Count(collection=collection, filter=filter)
        self.logger.debug(
            f"Start request to database with the following data: {command.data}"
        )
        response = self.adapter.count(command)
        return {"count": response["count"], "position": response["position"]}

    def min(
        self, collection: Collection, filter: Filter, field: str, type: str
    ) -> Aggregate:
        command = commands.Min(
            collection=collection, filter=filter, field=field, type=type
        )
        self.logger.debug(
            f"Start request to database with the following data: {command.data}"
        )
        response = self.adapter.min(command)
        return response

    def max(
        self, collection: Collection, filter: Filter, field: str, type: str
    ) -> Aggregate:
        command = commands.Max(
            collection=collection, filter=filter, field=field, type=type
        )
        self.logger.debug(
            f"Start request to database with the following data: {command.data}"
        )
        response = self.adapter.max(command)
        return response
