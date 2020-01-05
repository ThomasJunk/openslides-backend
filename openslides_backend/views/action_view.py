from typing import Dict, Iterable, List

from fastjsonschema import JsonSchemaException  # type: ignore
from werkzeug.exceptions import BadRequest
from werkzeug.wrappers import Response

from .. import logging
from ..actions.action_map import action_map
from ..exceptions import (
    ActionException,
    AuthException,
    BackendBaseException,
    EventStoreException,
    MediaTypeException,
)
from ..services.auth import AuthAdapter
from ..services.database import DatabaseAdapter
from ..services.event_store import EventStoreAdapter
from ..utils.types import Environment, Event
from .schema import action_view_schema
from .wrappers import Request

logger = logging.getLogger(__name__)


class ActionView:
    """
    During initialization we bind the viewpoint and services to the instance.
    """

    def __init__(self, environment: Environment) -> None:
        self.database_adapter = DatabaseAdapter(environment["database_url"])
        self.event_store_adapter = EventStoreAdapter(environment["event_store_url"])
        self.auth_adapter = AuthAdapter(environment["auth_url"])

    def dispatch(self, request: Request, **kwargs: dict) -> Response:
        """
        Dispatches request to the viewpoint.
        """
        logger.debug("Start dispatching request.")

        # Get request user id
        try:
            self.user_id = self.auth_adapter.get_user(request)
        except AuthException as exception:
            self.handle_error(exception)

        # Validate payload of request
        if not request.is_json:
            self.handle_error(
                MediaTypeException(
                    "Wrong media type. Use 'Content-Type: application/json' instead."
                )
            )
        action_requests = request.json
        try:
            self.validate(action_requests)
        except JsonSchemaException as exception:
            self.handle_error(exception)

        # Parse actions and creates events
        try:
            events = self.parse_actions(action_requests)
        except ActionException as exception:
            self.handle_error(exception)

        # Send events to database
        try:
            self.event_store_adapter.send(events)
        except EventStoreException as exception:
            self.handle_error(exception)

        logger.debug("Request was successful. Send response now.")
        return Response()

    def validate(self, action_requests: List[Dict]) -> None:
        """
        Validates action requests sent by client. Raises JsonSchemaException if
        input is invalid.
        """
        logger.debug("Validate action request.")
        action_view_schema(action_requests)

    def parse_actions(self, action_requests: List[Dict]) -> Iterable[Event]:
        """
        Parses action requests send by client. Raises ActionException if
        something went wrong.
        """
        all_events: List[Event] = []
        for element in action_requests:
            logger.debug(f"Action map contains the following actions: {action_map}.")
            action = action_map.get(element["action"])
            if action is None:
                raise BadRequest(f"Action {element['action']} does not exist.")
            logger.debug(f"Perform action {element['action']}.")
            events = action(self.database_adapter).perform(
                element["data"], self.user_id
            )
            logger.debug(f"Prepared events {events}.")
            all_events.extend(events)
        logger.debug("All events ready.")
        return events

    def handle_error(self, exception: BackendBaseException) -> None:
        """
        Handles some exceptions during dispatch of request. Raises HTTP 400.
        """
        logger.debug(f"Error in view. Exception message: {exception.message}")
        raise BadRequest(exception.message)