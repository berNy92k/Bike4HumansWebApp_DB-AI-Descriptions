from pydantic import BaseModel, Field


class ManufacturerListRequestDto(BaseModel):
    page: int = Field(default=1, ge=1)
    size: int = Field(default=5, ge=1, le=100)
