from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field

from app.models.user import UserModel


class CreateUserResponse(BaseModel):
    id: Annotated[UUID, Field()]
    email: Annotated[EmailStr, Field(max_length=255)]
    created_at: Annotated[datetime, Field()]
    updated_at: Annotated[datetime, Field()]

    @staticmethod
    def from_model(user: UserModel) -> "CreateUserResponse":
        return CreateUserResponse(
            id=user.id,
            email=user.email,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )
