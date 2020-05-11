from . import fields
from .base import Model


class Configuration(Model):
    id = fields.IdField(description="The id")
