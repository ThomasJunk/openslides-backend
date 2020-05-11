from openslides_backend.models import fields
from openslides_backend.models.base import Model


class AssignmentReleatedUser(Model):
    id = fields.IdField(description="The id")
    # assignment
    # user
    # weight
