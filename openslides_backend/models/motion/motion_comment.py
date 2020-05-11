from openslides_backend.models import fields
from openslides_backend.models.base import Model


class MotionComment(Model):
    id = fields.IdField(description="The id")
    # comment
    # motion
    # section
