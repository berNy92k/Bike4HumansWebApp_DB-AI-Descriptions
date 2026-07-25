from pydantic import BaseModel, Field


class OrderSummaryResponseDto(BaseModel):
    summary: str = Field(...)
