from openslides_backend.models import fields
from openslides_backend.models.base import Model


class BasePoll(Model):
    id = fields.IdField(description="The id")
    # db_votescast
    # db_votesvalid
    # db_votesinvalid
    # groups
    # majority_method
    # onehundred_percent_base
    # option_class
    # state
    # title
    # type
    # voted
    # votes_cast
    # votes_invalid
    # votes_valid
