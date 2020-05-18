from typing import Callable, Dict, Iterable, List, Type

import fastjsonschema  # type: ignore
from fastjsonschema import JsonSchemaException  # type: ignore

from ..shared.exceptions import ActionException, EventStoreException
from ..shared.handlers import Base as HandlerBase
from ..shared.interfaces import WriteRequestElement
from ..shared.schema import schema_version
from .actions_interface import ActionResult, Payload
from .base import Action


def prepare_actions_map() -> None:
    """
    This function just imports all actions modules so that the actions are
    recognized by the system and the register decorator can do its work.

    New modules have to be added here.
    """
    from . import agenda_item, committee, meeting, topic, motion  # type: ignore # noqa


actions_map: Dict[str, Type[Action]] = {}


def register_action(name: str) -> Callable[[Type[Action]], Type[Action]]:
    """
    Decorator to be used for action classes. Registers the class so that it can
    be found by the handler.
    """

    def wrapper(clazz: Type[Action]) -> Type[Action]:
        actions_map[name] = clazz
        return clazz

    return wrapper


prepare_actions_map()


payload_schema = fastjsonschema.compile(
    {
        "$schema": schema_version,
        "title": "Schema for actions API",
        "description": "An array of actions.",
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "action": {
                    "description": "Name of the action to be performed on the server",
                    "type": "string",
                    "minLength": 1,
                },
                "data": {
                    "oneOf": [
                        {
                            "description": "Data for the action (array)",
                            "type": "array",
                            "items": {"type": "object"},
                            "minItems": 1,
                            "uniqueItems": True,
                        },
                        {
                            "description": "Data for the action (object)",
                            "type": "object",
                        },
                    ],
                },
            },
            "required": ["action", "data"],
            "additionalProperties": False,
        },
        "minItems": 1,
        "uniqueItems": True,
    }
)


class ActionsHandler(HandlerBase):
    """
    Actions handler. It is the concret implementation of Actions interface.
    """

    def handle_request(self, payload: Payload, user_id: int) -> List[ActionResult]:
        """
        Takes payload and user id and handles this request by validating and
        parsing all actions. In the end it sends everything to the event store.
        """
        self.user_id = user_id

        # Validate payload of request
        try:
            self.validate(payload)
        except JsonSchemaException as exception:
            raise ActionException(exception.message)

        # TODO: Start a loop here and retry parsing actions and writing to event
        # store for some time if event store sends ModelLocked Exception

        # Parse actions and creates events
        write_request_elements = self.parse_actions(payload)

        # Send events to datastore
        try:
            self.services.event_store().send(write_request_elements)
        except EventStoreException as exception:
            raise ActionException(exception.message)

        # Return action result
        # TODO: This is a fake result because in this place all actions were
        # always successful.
        self.logger.debug("Request was successful. Send response now.")
        return [
            ActionResult(success=True, message="Action handled successfully")
        ] * len(payload)

    def validate(self, payload: Payload) -> None:
        """
        Validates actions requests sent by client. Raises JsonSchemaException if
        input is invalid.
        """
        self.logger.debug("Validate actions request.")
        payload_schema(payload)

    def parse_actions(self, payload: Payload) -> Iterable[WriteRequestElement]:
        """
        Parses actions request send by client. Raises ActionException or
        PermissionDenied if something went wrong.
        """
        all_write_request_elements: List[WriteRequestElement] = []
        for element in payload:
            self.logger.debug(
                f"Actions map contains the following actions: {actions_map}."
            )
            action = actions_map.get(element["action"])
            if action is None:
                raise ActionException(f"Action {element['action']} does not exist.")
            self.logger.debug(f"Perform action {element['action']}.")
            write_request_elements = action(
                self.permission(), self.datastore()
            ).perform(element["data"], self.user_id)
            self.logger.debug(
                f"Prepared write request element {write_request_elements}."
            )
            all_write_request_elements.extend(write_request_elements)
        self.logger.debug("All write request elements ready.")
        return all_write_request_elements
