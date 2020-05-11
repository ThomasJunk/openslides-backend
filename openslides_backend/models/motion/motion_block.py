from openslides_backend.models import fields
from openslides_backend.models.base import Model


class MotionBlock(Model):
    id = fields.IdField(description="The id")
    # internal
    # objects
    # title
