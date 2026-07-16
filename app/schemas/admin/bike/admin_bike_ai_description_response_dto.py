from pydantic import Field, BaseModel


class BikeAiDescriptionResponseDto(BaseModel):
    description: str | None = Field(...)
