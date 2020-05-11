from . import fields
from .base import Model


class Projector(Model):
    id = fields.IdField(description="The id")
