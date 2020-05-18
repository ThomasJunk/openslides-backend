import os

from mypy_extensions import TypedDict

Environment = TypedDict(
    "Environment",
    {
        "authentication_url": str,
        "permission_url": str,
        "datastore_read_url": str,
        "datastore_write_url": str,
    },
)

DEFAULT_PROTOCOL = "http"
DEFAULT_HOST = "localhost"
DEFAULT_AUTHENTICATION_PORT = 9000
DEFAULT_PERMISSION_PORT = 9001
DEFAULT_DATABASE_READ_PORT = 9002
DEFAULT_DATABASE_WRITE_PORT = 9003


def get_environment() -> Environment:
    """
    Parses environment variables and sets their defaults if they do not exist.
    """

    authentication_url = get_url_from_env(
        "OPENSLIDES_BACKEND_AUTHENTICATION_URL",
        get_fallback_url(DEFAULT_HOST, DEFAULT_AUTHENTICATION_PORT),
    )
    permission_url = get_url_from_env(
        "OPENSLIDES_BACKEND_PERMISSION_URL",
        get_fallback_url(DEFAULT_HOST, DEFAULT_PERMISSION_PORT),
    )
    datastore_read_url = get_url_from_env(
        "OPENSLIDES_BACKEND_DATASTORE_READ_URL",
        get_fallback_url(DEFAULT_HOST, DEFAULT_DATABASE_READ_PORT),
    )
    datastore_write_url = get_url_from_env(
        "OPENSLIDES_BACKEND__DATASTORE_WRITE_URL",
        get_fallback_url(DEFAULT_HOST, DEFAULT_DATABASE_WRITE_PORT),
    )

    return Environment(
        authentication_url=authentication_url,
        permission_url=permission_url,
        datastore_read_url=datastore_read_url,
        datastore_write_url=datastore_write_url,
    )


def get_url_from_env(env: str, fallback: str) -> str:
    return os.environ.get(env, fallback)


def get_fallback_url(host: str, port: int) -> str:
    """
    Helper function to build URL from given host and port.
    """
    return f"{DEFAULT_PROTOCOL}://{host}:{port}/"
