from openslides_backend.models import fields
from openslides_backend.models.base import Model


class State(Model):
    id = fields.IdField(description="The id")
    # allow_create_poll
    # allow_submitter_edit
    # allow_support
    # css_class
    # dont_set_identifier
    # merge_amendment_into_final
    # name
    # next_states
    # recommendation_label
    # restriction
    # show_recommendation_extension_field
    # show_state_extension_field
