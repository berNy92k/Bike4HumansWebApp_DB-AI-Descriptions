from datetime import datetime, timezone

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.bike import Bike
from app.repositories.bike_repository import BikeRepository
from app.schemas.admin.bike.admin_bike_list_request_dto import BikeListRequestDto
from app.schemas.admin.bike.admin_bike_list_response_dto import BikeListResponseDto
from app.schemas.admin.bike.admin_bike_read_dto import BikeReadDto
from app.schemas.front.bike.bike_similar_response_dto import BikeSimilarRecommendationResponseDto, SimilarBikeDto
from app.services.ai.bike_recommendation_ai_service import BikeRecommendationAiService


class BikeService:

    def __init__(self, db: Session, ai_recommendation_service: BikeRecommendationAiService | None = None):
        self.bike_repository = BikeRepository(db)
        self.ai_recommendation_service = ai_recommendation_service or BikeRecommendationAiService()

    def get_all_bikes(self) -> list[Bike]:
        return self.bike_repository.get_all_bikes()

    def get_last_x_bikes(self, size: int) -> list[BikeReadDto]:
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

    def get_bike_by_id(self, bike_id: int) -> Bike:
        bike = self.bike_repository.get_bike_by_id(bike_id)

        if not bike:
            raise HTTPException(status_code=404, detail="Bike not found")

        return bike

    def get_bikes_by_manufacturer_id(self, manufacturer_id: int) -> list[Bike]:
        return self.bike_repository.get_bikes_by_manufacturer_id(manufacturer_id)

    def get_similar_bikes_recommendation(self, bike_id: int) -> BikeSimilarRecommendationResponseDto:
        bike = self.get_bike_by_id(bike_id)
        similar_bikes = self.bike_repository.get_similar_bikes(bike)

        note = None
        if similar_bikes:
            note = bike.similar_bikes_ai_note
            if note is None:
                note = self.ai_recommendation_service.generate_recommendation_note(bike, similar_bikes)
                bike.similar_bikes_ai_note = note
                bike.similar_bikes_ai_note_generated_at = datetime.now(timezone.utc)
                self.bike_repository.update_bike(bike)

        return BikeSimilarRecommendationResponseDto(
            note=note,
            bikes=[SimilarBikeDto.model_validate(similar) for similar in similar_bikes],
        )
