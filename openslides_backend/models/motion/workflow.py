from openslides_backend.models import fields
from openslides_backend.models.base import Model


class Workflow(Model):
    id = fields.IdField(description="The id")
    # first_state
    # name
    # objects
