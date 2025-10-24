from typing import Annotated

from pydantic import BaseModel, Field


class LoginResponse(BaseModel):
    access_token: Annotated[str, Field()]
    token_type: Annotated[str, Field(default="bearer")]
