from typing import Annotated

from pydantic import BaseModel, EmailStr, Field

from app.common.type import PasswordStr


class CreateUserRequest(BaseModel):
    name: Annotated[str, Field(max_length=100)]
    email: Annotated[EmailStr, Field(max_length=255)]
    password: PasswordStr
