from typing import List

from openslides_backend.shared.interfaces import LoggingModule
from openslides_backend.shared.patterns import Collection


class HTTPWriter:
    """
    HTTPWriter implements the writer interface
    """

    def __init__(self, database_url: str, logging: LoggingModule):
        self.logger = logging.getLogger(__name__)
        self.url = database_url
        self.headers = {"Content-Type": "application/json"}

    def write(self, data: object) -> None:
        ...

    def reserveIds(self, collection: Collection, number: int) -> List[int]:
        ...
