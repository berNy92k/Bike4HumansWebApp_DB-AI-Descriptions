from pathlib import Path
from random import choice

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.manufacturer import Manufacturer
from app.repositories.manufacturer_repository import ManufacturerRepository
from app.schemas.admin.manufacturers.admin_manufacturer_create_dto import ManufacturerCreateDto
from app.schemas.admin.manufacturers.admin_manufacturer_list_request_dto import ManufacturerListRequestDto
from app.schemas.admin.manufacturers.admin_manufacturer_list_response_dto import ManufacturerListResponseDto
from app.schemas.admin.manufacturers.admin_manufacturer_read_dto import ManufacturerReadDto
from app.schemas.admin.manufacturers.admin_manufacturer_update_dto import ManufacturerUpdateDto


class AdminManufacturerService:
    PLACEHOLDER_IMAGES_DIR = Path("app/static/images/manufacturers/placeholders")

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

    def create_manufacturer(self, manufacturer_create_dto: ManufacturerCreateDto, current_user: dict):
        manufacturer = Manufacturer(
            name=manufacturer_create_dto.name,
            description=manufacturer_create_dto.description,
            image_url=self._pick_random_image(),
            created_by=current_user["user_id"]
        )

        self.manufacturer_repository.create_manufacturer(manufacturer)

    def update_manufacturer_all_fields(self, manufacturer_id: int, manufacturer_update_dto: ManufacturerUpdateDto):
        manufacturer = self.get_manufacturer_by_id(manufacturer_id)
        update_manufacturer_data = manufacturer_update_dto.model_dump()

        for f, v in update_manufacturer_data.items():
            setattr(manufacturer, f, v)

        self.manufacturer_repository.update_manufacturer(manufacturer)

    def update_manufacturer_separate_fields(self, manufacturer_id, manufacturer_update_dto):
        manufacturer = self.get_manufacturer_by_id(manufacturer_id)
        update_manufacturer_data = manufacturer_update_dto.model_dump(exclude_unset=True)

        for f, v in update_manufacturer_data.items():
            setattr(manufacturer, f, v)

        self.manufacturer_repository.update_manufacturer(manufacturer)

    def delete_manufacturer_by_id(self, manufacturer_id):
        manufacturer = self.get_manufacturer_by_id(manufacturer_id)

        self.manufacturer_repository.delete(manufacturer)

    def _pick_random_image(self) -> str | None:
        if not self.PLACEHOLDER_IMAGES_DIR.exists():
            return None

        images = [
            path for path in self.PLACEHOLDER_IMAGES_DIR.iterdir() if
            path.is_file() and path.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}
        ]

        if not images:
            return None

        chosen = choice(images)
        return f"/static/images/manufacturers/placeholders/{chosen.name}"
