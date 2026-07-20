from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ManufacturerReadDto(BaseModel):
    id: int
    name: str
    description: str | None = None
    is_description_ai_generated: bool
    image_url: str | None = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
