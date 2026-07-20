from pydantic import Field, BaseModel


class ManufacturerCreateDto(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=2000)
    is_description_ai_generated: bool = Field(default=False)
    image_url: str | None = Field(default=None, max_length=500)
