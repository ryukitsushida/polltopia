import string
from typing import Annotated

from pydantic import AfterValidator, StringConstraints


def _validate_password_complexity(value: str) -> str:
    # TODO:　正規表現での実装ができなかったので、ひとまずCopilot提案のパスワード検証ロジックとするが、後々修正必須。
    """Ensure password has lower/upper/digit/symbol and no whitespace."""
    if not any(c.islower() for c in value):
        raise ValueError("password must contain at least one lowercase letter")
    if not any(c.isupper() for c in value):
        raise ValueError("password must contain at least one uppercase letter")
    if not any(c.isdigit() for c in value):
        raise ValueError("password must contain at least one digit")
    if not any(c in string.punctuation for c in value):
        raise ValueError("password must contain at least one symbol")
    if any(ch.isspace() for ch in value):
        raise ValueError("password must not contain whitespace")
    return value


PasswordStr = Annotated[
    str,
    StringConstraints(min_length=12, max_length=128, strip_whitespace=False),
    AfterValidator(_validate_password_complexity),
]
