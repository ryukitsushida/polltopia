from enum import Enum
from typing import Annotated

from pydantic import StringConstraints

_PASSWORD_PATTERN = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9])(?!.*\s).{12,128}$"

PasswordStr = Annotated[
    str,
    StringConstraints(
        min_length=12,
        max_length=128,
        pattern=_PASSWORD_PATTERN,
        strip_whitespace=False,
    ),
]


class ProviderType(str, Enum):
    LOCAL = "local"
    GOOGLE = "google"
    GITHUB = "github"
