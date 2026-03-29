from pydantic import BaseModel

from app.schemas.admin.checkout.admin_checkout_read_dto import CheckoutReadDto


class CheckoutListResponseDto(BaseModel):
    checkouts: list[CheckoutReadDto]
    page: int
    size: int
    total: int
    pages: int
