from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.manufacturer_repository import ManufacturerRepository
from app.schemas.admin.manufacturers.admin_manufacturer_list_request_dto import ManufacturerListRequestDto
from app.schemas.admin.manufacturers.admin_manufacturer_list_response_dto import ManufacturerListResponseDto
from app.schemas.admin.manufacturers.admin_manufacturer_read_dto import ManufacturerReadDto


class ManufacturerService:

    def __init__(self, db: Session):
        self.manufacturer_repository = ManufacturerRepository(db)

    def get_all_manufacturers(self):
        return self.manufacturer_repository.get_all_manufacturers()

    def get_manufacturers_paginated(self, request_dto: ManufacturerListRequestDto) -> ManufacturerListResponseDto:
        items, total = self.manufacturer_repository.get_manufacturers_paginated(
            page=request_dto.page,
            size=request_dto.size,
        )
        pages = (total + request_dto.size - 1) // request_dto.size if total > 0 else 0

        manufacturer_items = [ManufacturerReadDto.model_validate(m) for m in items]

        return ManufacturerListResponseDto(
            items=manufacturer_items,
            page=request_dto.page,
            size=request_dto.size,
            total=total,
            pages=pages,
        )

    def get_manufacturer_by_id(self, manufacturer_id):
        manufacturer = self.manufacturer_repository.get_manufacturer_by_id(manufacturer_id)

        if not manufacturer:
            raise HTTPException(status_code=404, detail="Manufacturer not found")

        return manufacturer
