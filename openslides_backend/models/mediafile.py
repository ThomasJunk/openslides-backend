from . import fields
from .base import Model


class Mediafile(Model):
    id = fields.IdField(description="The id")
    # create_timestamp
    # filesize
    # is_directory
    # mediafile
    # mimetype
    # objects
    # original_filename
    # parent
    # pdf_information
    # title
