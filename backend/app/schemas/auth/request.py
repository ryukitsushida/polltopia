from typing import Annotated

from pydantic import BaseModel, EmailStr, Field

from app.schemas.types import PasswordStr


class LoginRequest(BaseModel):
    email: Annotated[EmailStr, Field(max_length=255)]
    password: PasswordStr
