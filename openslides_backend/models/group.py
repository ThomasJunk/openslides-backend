from . import fields
from .base import Model


class Group(Model):
    id = fields.IdField(description="The id")
