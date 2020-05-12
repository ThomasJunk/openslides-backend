from ..shared.patterns import Collection
from . import fields
from .base import Model


class User(Model):
    """
    Model for users.

    There are the following reverse relation fields:
        TODO
    """

    # TODO: Add reverse relation fields to docstring.

    collection = Collection("user")
    verbose_name = "user"

    id = fields.IdField(description="The id of this user.")

    # about_me
    # auth_type
    # comment
    # default_password
    # email
    # first_name
    # gender
    # is_active
    # is_commitee
    # is_present
    # last_email_send
    # last_name
    # number
    # objects
    # title
    # username
    # vote_weight
