"""
参考
https://omomuki-tech.com/archives/1431
"""

import base64
import hashlib
import hmac
import secrets

_ALGORITHM = "pbkdf2_sha256"
_ITERATIONS = 600000
_SALT_BYTES = 16


def _b64encode(b: bytes) -> str:
    return base64.b64encode(b).decode("ascii")


def _b64decode(s: str) -> bytes:
    return base64.b64decode(s.encode("ascii"))


def get_password_hash(password: str) -> str:
    salt = secrets.token_bytes(_SALT_BYTES)
    derived_key = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, _ITERATIONS)
    return f"{_ALGORITHM}${_ITERATIONS}${_b64encode(salt)}${_b64encode(derived_key)}"


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        algorithm, iterations_str, salt_b64, hash_b64 = hashed_password.split("$", 3)
        if algorithm != _ALGORITHM:
            return False
        iterations = int(iterations_str)
        salt = _b64decode(salt_b64)
        expected = _b64decode(hash_b64)
        derived_key = hashlib.pbkdf2_hmac("sha256", plain_password.encode("utf-8"), salt, iterations)
        return hmac.compare_digest(derived_key, expected)
    except Exception:
        # TODO: return Exception
        return False
