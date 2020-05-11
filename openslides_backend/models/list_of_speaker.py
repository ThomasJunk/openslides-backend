from . import fields
from .base import Model


class ListOfSpeaker(Model):
    id = fields.IdField(description="the id the speakerlist")
    # closed
    # content_object
    # content_type
    # object_id
    # objects
