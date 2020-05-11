from openslides_backend.models import fields
from openslides_backend.models.base import Model


class AssignmentPoll(Model):
    id = fields.IdField(description="The id")
    # allow_mutiple:votes_per_candidate
    # amoint_global_abstain
    # amount_global_no
    # assignment
    # db_amount_global_abstain
    # db_amount_global:no
    # description
    # global_abstain
    # global_no
    # objects
    # one_hundered_percent_base
    # option_class
    # pollmethod
    # votes_amount
