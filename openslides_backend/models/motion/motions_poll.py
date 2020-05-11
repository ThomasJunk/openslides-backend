from openslides_backend.models import fields
from openslides_backend.models.base import Model


class MotionsPoll(Model):
    id = fields.IdField(description="The id")
    # motion
    # objects
    # option_class
    # pollmethod
