from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AddressReadDto(BaseModel):
    id: int
    type: str
    company_name: str | None = None
    vat_number: str | None = None
    address_line_1: str
    address_line_2: str | None = None
    city: str
    postal_code: str
    country_code: str
    state_province: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
