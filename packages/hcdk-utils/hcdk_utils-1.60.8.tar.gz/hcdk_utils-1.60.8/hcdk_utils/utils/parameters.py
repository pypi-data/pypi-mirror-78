import os
from distutils.util import strtobool


def get_optional(key: str, value=None):
    return os.getenv(key, value)


def get_mandatory(key: str):
    value = os.getenv(key)
    if not value:
        raise ValueError(f'The ENV VAR {key} is required.')
    return value


def get_boolean(
    key: str,
    default: str
) -> bool:
    value = os.getenv(key, default)
    return bool(strtobool(value))
