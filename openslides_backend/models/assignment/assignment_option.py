from openslides_backend.models import fields
from openslides_backend.models.base import Model


class AssignmentOption(Model):
    id = fields.IdField(description="The id")
    # objects
    # poll
    # user
    # vote_class
    # weight
