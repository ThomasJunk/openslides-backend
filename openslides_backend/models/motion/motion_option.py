from openslides_backend.models import fields
from openslides_backend.models.base import Model


class MotionOption(Model):
    id = fields.IdField(description="The id")
    # objects
    # poll
    # vote_class
