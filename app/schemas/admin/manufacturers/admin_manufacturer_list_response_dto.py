from pydantic import BaseModel

from app.schemas.admin.manufacturers.admin_manufacturer_read_dto import ManufacturerReadDto


class ManufacturerListResponseDto(BaseModel):
    items: list[ManufacturerReadDto]
    page: int
    size: int
    total: int
    pages: int
