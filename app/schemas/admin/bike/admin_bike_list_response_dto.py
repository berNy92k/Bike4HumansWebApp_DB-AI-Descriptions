from pydantic import BaseModel

from app.schemas.admin.bike.admin_bike_read_dto import BikeReadDto


class BikeListResponseDto(BaseModel):
    items: list[BikeReadDto]
    page: int
    size: int
    total: int
    pages: int
