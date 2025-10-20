from typing import Annotated

from pydantic import BaseModel, Field


class CreateSampleRequest(BaseModel):
    name: Annotated[str, Field(max_length=100)]
    description: Annotated[str | None, Field(default=None, max_length=255)]
