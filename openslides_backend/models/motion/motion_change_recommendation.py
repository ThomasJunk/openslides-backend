from openslides_backend.models import fields
from openslides_backend.models.base import Model


class MotionChangeRecommendation(Model):
    id = fields.IdField(description="The id")
    # author
    # creation_time
    # internal
    # line_from
    # line_to
    # motion
    # other_description
    # rejected
    # text
    # type
