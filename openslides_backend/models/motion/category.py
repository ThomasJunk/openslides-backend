from openslides_backend.models import fields
from openslides_backend.models.base import Model


class Category(Model):
    id = fields.IdField(description="The id")
    # name
    # parent
    # prefix
    # weight
