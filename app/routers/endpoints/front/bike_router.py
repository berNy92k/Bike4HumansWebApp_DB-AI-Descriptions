from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from app.database.database import get_db
from app.routers.utils.rate_limiter import InMemoryRateLimiter, rate_limit_dependency
from app.schemas.front.bike.bike_search_filters_response_dto import BikeSearchFiltersResponseDto
from app.schemas.front.bike.bike_search_request_dto import BikeSearchRequestDto
from app.schemas.front.bike.bike_similar_response_dto import BikeSimilarRecommendationResponseDto
from app.services.front.bike_service import BikeService

db_dependency = Annotated[Session, Depends(get_db)]

ai_rate_limiter = InMemoryRateLimiter(max_requests=15, window_seconds=60)
ai_rate_limit_dependency = Depends(rate_limit_dependency(ai_rate_limiter))

router = APIRouter(
    prefix="/bikes",
    tags=["Bikes"],
)


@router.post(
    "/{bike_id}/ai-similar-bikes",
    status_code=status.HTTP_201_CREATED,
    dependencies=[ai_rate_limit_dependency],
)
async def get_similar_bikes_recommendation(bike_id: int, db: db_dependency) -> BikeSimilarRecommendationResponseDto:
    service = BikeService(db)
    return service.get_similar_bikes_recommendation(bike_id)


@router.post(
    "/ai-search",
    status_code=status.HTTP_201_CREATED,
    dependencies=[ai_rate_limit_dependency],
)
async def generate_search_filters(search_request_dto: BikeSearchRequestDto, db: db_dependency) -> BikeSearchFiltersResponseDto:
    service = BikeService(db)
    return service.generate_search_filters(search_request_dto.query)
