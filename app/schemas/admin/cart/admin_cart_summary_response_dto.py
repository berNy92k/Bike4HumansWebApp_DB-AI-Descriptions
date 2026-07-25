from pydantic import BaseModel, Field


class CartSummaryResponseDto(BaseModel):
    summary: str = Field(...)
