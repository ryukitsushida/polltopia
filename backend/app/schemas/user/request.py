from typing import Annotated

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.schemas.types import PasswordStr


class CreateUserRequest(BaseModel):
    model_config = ConfigDict(regex_engine="python-re")

    name: Annotated[str, Field(max_length=100)]
    email: Annotated[EmailStr, Field(max_length=255)]
    # password: PasswordStr
    password: PasswordStr
