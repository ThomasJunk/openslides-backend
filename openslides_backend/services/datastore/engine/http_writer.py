from typing import List

import requests
import simplejson as json

from openslides_backend.shared.exceptions import DatastoreException
from openslides_backend.shared.interfaces import LoggingModule

from .interface import Command, EngineResponse


class HTTPWriter:
    """
    HTTPWriter implements the writer interface
    """

    def __init__(self, datastore_url: str, logging: LoggingModule):
        self.logger = logging.getLogger(__name__)
        self.url = datastore_url
        self.headers = {"Content-Type": "application/json"}

    def write(self, data: Command) -> None:
        command_url = f" {self.url}/write"
        payload = json.dumps(data.data)
        response = requests.post(command_url, data=payload, headers=self.headers)
        if not response.ok:
            if response.status_code >= 500:
                raise DatastoreException("Connection to datastore failed.")

    def reserveIds(self, data: Command) -> List[EngineResponse]:
        ...
