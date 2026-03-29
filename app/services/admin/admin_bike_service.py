from pathlib import Path
from random import choice
from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.bike import Bike
from app.repositories.bike_repository import BikeRepository
from app.schemas.admin.bike.admin_bike_create_dto import BikeCreateDto
from app.schemas.admin.bike.admin_bike_list_request_dto import BikeListRequestDto
from app.schemas.admin.bike.admin_bike_list_response_dto import BikeListResponseDto
from app.schemas.admin.bike.admin_bike_read_dto import BikeReadDto
from app.schemas.admin.bike.admin_bike_update_dto import BikeUpdateDto


class AdminBikeService:
    PLACEHOLDER_IMAGES_DIR = Path("app/static/images/bikes/placeholders")

    def __init__(self, db: Session):
        self.bike_repository = BikeRepository(db)

    def get_all_bikes(self):
        return self.bike_repository.get_all_bikes()

    def get_last_x_bikes(self, size: int) -> List[BikeReadDto]:
        bikes = self.bike_repository.get_last_x_bikes(size)

        return [BikeReadDto.model_validate(bike) for bike in bikes]

    def get_bikes_paginated(self, request_dto: BikeListRequestDto) -> BikeListResponseDto:
        items, total = self.bike_repository.get_bikes_paginated(
            page=request_dto.page,
            size=request_dto.size,
        )
        pages = (total + request_dto.size - 1) // request_dto.size if total > 0 else 0

        bike_items = [BikeReadDto.model_validate(bike) for bike in items]

        return BikeListResponseDto(
            items=bike_items,
            page=request_dto.page,
            size=request_dto.size,
            total=total,
            pages=pages,
        )

    def get_bike_by_id(self, bike_id):
        bike = self.bike_repository.get_bike_by_id(bike_id)

        if not bike:
            raise HTTPException(status_code=404, detail="Bike not found")

        return bike

    def create_bike(self, bike_create_dto: BikeCreateDto, current_user: dict):
        bike = Bike(
            name=bike_create_dto.name,
            description=bike_create_dto.description,
            price=bike_create_dto.price,
            stock_quantity=bike_create_dto.stock_quantity,
            image_url=self._pick_random_image(),
            is_active=bike_create_dto.is_active,
            created_by=current_user["user_id"],
            brand_id=bike_create_dto.brand_id,
        )
        self.bike_repository.create_bike(bike)

    def update_bike_all_fields(self, bike_id: int, bike_update_dto: BikeUpdateDto):
        bike = self.get_bike_by_id(bike_id)
        update_bike_data = bike_update_dto.model_dump()

        for f, v in update_bike_data.items():
            setattr(bike, f, v)

        self.bike_repository.update_bike(bike)

    def update_bike_separate_fields(self, bike_id, bike_update_dto):
        bike = self.get_bike_by_id(bike_id)
        update_bike_data = bike_update_dto.model_dump(exclude_unset=True)

        for f, v in update_bike_data.items():
            setattr(bike, f, v)

        self.bike_repository.update_bike(bike)

    def delete_bike_by_id(self, bike_id):
        bike = self.get_bike_by_id(bike_id)

        self.bike_repository.delete(bike)

    def _pick_random_image(self) -> str | None:
        if not self.PLACEHOLDER_IMAGES_DIR.exists():
            return None

        images = [
            path for path in self.PLACEHOLDER_IMAGES_DIR.iterdir()
            if path.is_file() and path.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}
        ]

        if not images:
            return None

        chosen = choice(images)
        return f"/static/images/bikes/placeholders/{chosen.name}"
