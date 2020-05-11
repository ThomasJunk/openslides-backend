from . import fields
from .base import Model


class PersonalNote(Model):
    id = fields.IdField(description="The id")
