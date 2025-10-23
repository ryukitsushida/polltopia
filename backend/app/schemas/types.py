from typing import Annotated

from pydantic import StringConstraints

PasswordStr = Annotated[
    str,
    StringConstraints(
        min_length=8,
        max_length=128,
        pattern=r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*(),.?":{}|<>]).+$',
    ),
]
