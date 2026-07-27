from pydantic import BaseModel, Field


class AddressUpsertDto(BaseModel):
    company_name: str | None = None
    vat_number: str | None = None
    address_line_1: str = Field(..., min_length=1)
    address_line_2: str | None = None
    city: str = Field(..., min_length=1)
    postal_code: str = Field(..., min_length=1)
    country_code: str = Field(..., min_length=1)
    state_province: str = Field(..., min_length=1)
