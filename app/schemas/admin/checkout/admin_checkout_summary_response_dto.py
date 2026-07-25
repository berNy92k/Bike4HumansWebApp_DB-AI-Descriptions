from pydantic import BaseModel, Field


class CheckoutSummaryResponseDto(BaseModel):
    summary: str = Field(...)
