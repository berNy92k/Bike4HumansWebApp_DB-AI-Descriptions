from pydantic import Field, BaseModel


class ManufacturerAiDescriptionResponseDto(BaseModel):
    description: str | None = Field(...)