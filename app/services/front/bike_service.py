from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.bike_repository import BikeRepository
from app.schemas.admin.bike.admin_bike_list_request_dto import BikeListRequestDto
from app.schemas.admin.bike.admin_bike_list_response_dto import BikeListResponseDto
from app.schemas.admin.bike.admin_bike_read_dto import BikeReadDto


class BikeService:

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
