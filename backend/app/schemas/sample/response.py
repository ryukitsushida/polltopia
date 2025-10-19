from typing import Annotated

from pydantic import BaseModel, Field

from app.models.sample import SampleModel


class SampleResponse(BaseModel):
    id: Annotated[int, Field(gt=0)]
    name: Annotated[str, Field(max_length=100)]
    description: Annotated[str | None, Field(default=None, max_length=255)]

    def to(sample: SampleModel) -> "SampleResponse":
        return SampleResponse(
            id=sample.id,
            name=sample.name,
            description=sample.description,
        )


class CreateSampleResponse(BaseModel):
    id: Annotated[int, Field(gt=0)]
    name: Annotated[str, Field(max_length=100)]
    description: Annotated[str | None, Field(default=None, max_length=255)]
