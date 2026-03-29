from typing import Annotated, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from app.database.database import get_db
from app.schemas.admin.bike.admin_bike_create_dto import BikeCreateDto
from app.schemas.admin.bike.admin_bike_read_dto import BikeReadDto
from app.schemas.admin.bike.admin_bike_update_dto import BikeUpdateDto
from app.services.admin.admin_bike_service import AdminBikeService
from app.services.auth.auth_service import get_current_user

db_dependency = Annotated[Session, Depends(get_db)]
current_user_dependency = Annotated[dict, Depends(get_current_user)]

router = APIRouter(
    prefix="/admin/bikes",
    tags=["Admin - bikes"],
    dependencies=[Depends(get_current_user)],
)


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[BikeReadDto])
async def find_all_bikes(db: db_dependency):
    service = AdminBikeService(db)
    return service.get_all_bikes()


@router.get("/{bike_id}", status_code=status.HTTP_200_OK, response_model=BikeReadDto)
async def find_bike_by_id(bike_id: int, db: db_dependency):
    service = AdminBikeService(db)
    return service.get_bike_by_id(bike_id)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_bike(bike_create_dto: BikeCreateDto, db: db_dependency, current_user: current_user_dependency):
    service = AdminBikeService(db)
    service.create_bike(bike_create_dto, current_user)


@router.put("/{bike_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_bike_all_fields(bike_id: int, bike_update_dto: BikeUpdateDto, db: db_dependency):
    service = AdminBikeService(db)
    service.update_bike_all_fields(bike_id, bike_update_dto)


@router.patch("/{bike_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_bike_separate_fields(bike_id: int, bike_update_dto: BikeUpdateDto, db: db_dependency):
    service = AdminBikeService(db)
    service.update_bike_separate_fields(bike_id, bike_update_dto)


@router.delete("/{bike_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_bike_by_id(bike_id: int, db: db_dependency):
    service = AdminBikeService(db)
    service.delete_bike_by_id(bike_id)
