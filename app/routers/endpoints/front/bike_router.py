from decimal import Decimal
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from starlette import status

from app.database.database import get_db
from app.routers.utils.rate_limiter import InMemoryRateLimiter, rate_limit_dependency
from app.schemas.admin.bike.admin_bike_list_request_dto import BikeListRequestDto
from app.schemas.admin.bike.admin_bike_list_response_dto import BikeListResponseDto
from app.schemas.admin.bike.admin_bike_read_dto import BikeReadDto
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

# Separate prefix ("/api/bikes" instead of "/bikes") for the list/detail read endpoints below:
# the React SPA's client-side catalog pages live at bare "/bikes" and "/bikes/{id}" (see
# frontend/src/App.tsx), served by the catch-all in init_spa() (app/routers/init_routers.py),
# which is registered last. If this JSON API reused those same paths, it would be matched
# first and a browser hard-refresh on "/bikes/5" would get JSON instead of the SPA shell.
public_router = APIRouter(
    prefix="/api/bikes",
    tags=["Bikes"],
)


@public_router.get("/", status_code=status.HTTP_200_OK, response_model=BikeListResponseDto)
async def find_bikes(
    db: db_dependency,
    page: int = Query(1, ge=1),
    size: int = Query(16, ge=1, le=100),
    bike_type: str | None = Query(None),
    usage: str | None = Query(None),
    target_user: str | None = Query(None),
    price_min: Decimal | None = Query(None, ge=0),
    price_max: Decimal | None = Query(None, ge=0),
):
    service = BikeService(db)
    return service.get_bikes_paginated(BikeListRequestDto(
        page=page,
        size=size,
        bike_type=bike_type,
        usage=usage,
        target_user=target_user,
        price_min=price_min,
        price_max=price_max,
    ))


@public_router.get("/{bike_id}", status_code=status.HTTP_200_OK, response_model=BikeReadDto)
async def find_bike_by_id(bike_id: int, db: db_dependency):
    service = BikeService(db)
    return service.get_bike_by_id(bike_id)


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
