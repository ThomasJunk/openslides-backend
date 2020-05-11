from openslides_backend.models import fields
from openslides_backend.models.base import Model


class BaseVote(Model):
    id = fields.IdField(description="The id")
    # user
    # value
    # weight
