from typing import Dict, List

import openslides_backend.services.datastore.commands as commands
from openslides_backend.services.datastore.adapter.interface import GetManyRequest
from openslides_backend.services.datastore.engine import Reader, Writer
from openslides_backend.shared.filters import Filter
from openslides_backend.shared.interfaces import LoggingModule, WriteRequestElement
from openslides_backend.shared.patterns import Collection, FullQualifiedId

from .interface import Aggregate, Count, Found, PartialModel


class Adapter:
    """
    Adapter to connect to (read-only) datastore.
    """

    def __init__(self, reader: Reader, writer: Writer, logging: LoggingModule) -> None:
        self.logger = logging.getLogger(__name__)
        self.reader = reader
        self.writer = writer

    def get(
        self,
        fqid: FullQualifiedId,
        mapped_fields: List[str] = None,
        position: int = None,
        get_deleted_models: int = None,
    ) -> PartialModel:
        command = commands.Get(fqid=fqid, mappedFields=mapped_fields)
        self.logger.debug(
            f"Start request to datastore with the following data: {command.data}"
        )
        response = self.reader.get(command)
        return response

    def getMany(
        self,
        get_many_requests: List[GetManyRequest],
        mapped_fields: List[str] = None,
        position: int = None,
        get_deleted_models: int = None,
    ) -> Dict[str, Dict[int, PartialModel]]:
        command = commands.GetMany(
            get_many_requests=get_many_requests,
            mapped_fields=mapped_fields,
            position=position,
            get_deleted_models=get_deleted_models,
        )
        self.logger.debug(
            f"Start request to datastore with the following data: {command.data}"
        )
        response = self.reader.getMany(command)
        return response

    def getManyByFQIDs(
        self, ids: List[FullQualifiedId],
    ) -> Dict[str, Dict[int, PartialModel]]:
        command = commands.GetManyByFQIDs(ids=ids,)
        self.logger.debug(
            f"Start request to datastore with the following data: {command.data}"
        )
        response = self.reader.getMany(command)
        return response

    def getAll(
        self,
        collection: Collection,
        mapped_fields: List[str] = None,
        get_deleted_models: int = None,
    ) -> List[PartialModel]:
        command = commands.GetAll(collection=collection, mapped_fields=mapped_fields)
        self.logger.debug(
            f"Start request to datastore with the following data: {command.data}"
        )
        response = self.reader.getAll(command)
        return response

    def filter(
        self,
        collection: Collection,
        filter: Filter,
        meeting_id: int = None,
        mapped_fields: List[str] = None,
    ) -> List[PartialModel]:
        command = commands.Filters(collection=collection, filter=filter)
        self.logger.debug(
            f"Start request to datastore with the following data: {command.data}"
        )
        response = self.reader.filter(command)
        return response

    def exists(self, collection: Collection, filter: Filter) -> Found:
        command = commands.Exists(collection=collection, filter=filter)
        self.logger.debug(
            f"Start request to datastore with the following data: {command.data}"
        )
        response = self.reader.exists(command)
        return {"exists": response["exists"], "position": response["position"]}

    def count(self, collection: Collection, filter: Filter) -> Count:
        command = commands.Count(collection=collection, filter=filter)
        self.logger.debug(
            f"Start request to datastore with the following data: {command.data}"
        )
        response = self.reader.count(command)
        return {"count": response["count"], "position": response["position"]}

    def min(
        self, collection: Collection, filter: Filter, field: str, type: str = None
    ) -> Aggregate:
        command = commands.Min(
            collection=collection, filter=filter, field=field, type=type
        )
        self.logger.debug(
            f"Start request to datastore with the following data: {command.data}"
        )
        response = self.reader.min(command)
        return response

    def max(
        self, collection: Collection, filter: Filter, field: str, type: str = None
    ) -> Aggregate:
        command = commands.Max(
            collection=collection, filter=filter, field=field, type=type
        )
        self.logger.debug(
            f"Start request to datastore with the following data: {command.data}"
        )
        response = self.reader.max(command)
        return response

    def write(self, write_request: WriteRequestElement) -> None:
        command = commands.Write(write_request=write_request)
        self.logger.debug(
            f"Start write-request to datastore with the following data: {command.data}"
        )
        self.writer.write(command)

    def reserveIds(self, collection: Collection, number: int) -> List[int]:
        command = commands.ReserveIDs(collection=collection, number=number)
        self.logger.debug(
            f"Start write-request to datastore with the following data: {command.data}"
        )
        self.writer.reserveIds(command)
        return [1, 2, 3]
