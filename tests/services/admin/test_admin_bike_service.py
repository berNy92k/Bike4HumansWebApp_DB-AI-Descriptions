from decimal import Decimal
from unittest.mock import patch

import pytest
from fastapi import HTTPException

from app.models.bike import Bike
from app.repositories.bike_repository import BikeRepository
from app.schemas.admin.bike.admin_bike_create_dto import BikeCreateDto
from app.schemas.admin.bike.admin_bike_list_request_dto import BikeListRequestDto
from app.services.admin.admin_bike_service import AdminBikeService
from tests.database.database import override_get_db


@pytest.fixture
def db_session():
    db_gen = override_get_db()
    db = next(db_gen)
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def clean_bikes_table(db_session):
    # Given
    db_session.query(Bike).delete()
    db_session.commit()

    yield

    db_session.query(Bike).delete()
    db_session.commit()


@pytest.fixture
def seeded_bikes(db_session, clean_bikes_table):
    # Given
    bikes = [
        Bike(name="Trek Marlin 7", price=3999.99, stock_quantity=5, created_by=1, brand_id=1),
        Bike(name="Giant Talon 1", price=3499.00, stock_quantity=3, created_by=1, brand_id=1),
        Bike(name="Specialized Rockhopper", price=4299.50, stock_quantity=2, created_by=1, brand_id=1),
    ]

    for bike in bikes:
        db_session.add(bike)
    db_session.commit()

    return bikes

def test_get_all_bikes(db_session, seeded_bikes):
    # Given
    bike_service = AdminBikeService(db_session)

    # When
    result = bike_service.get_all_bikes()

    # Then
    assert len(result) == 3


def test_get_last_x_bikes(db_session, seeded_bikes):
    # Given
    bike_service = AdminBikeService(db_session)

    # When
    result = bike_service.get_last_x_bikes(2)

    # Then
    assert len(result) == 2


def test_get_bikes_paginated(db_session, seeded_bikes):
    # Given
    bike_service = AdminBikeService(db_session)
    request_dto = BikeListRequestDto(page=1, size=2)

    # When
    result = bike_service.get_bikes_paginated(request_dto)

    # Then
    assert result.page == 1
    assert result.size == 2
    assert result.total == 3
    assert result.pages == 2


def test_get_bike_by_id_found(db_session, seeded_bikes):
    # Given
    bike_id = 1
    bike_service = AdminBikeService(db_session)

    # When
    result = bike_service.get_bike_by_id(bike_id)

    # Then
    assert result.id == bike_id


def test_get_bike_by_id_not_found(db_session, seeded_bikes):
    # Given
    bike_service = AdminBikeService(db_session)

    # When / Then
    with pytest.raises(HTTPException) as exc:
        bike_service.get_bike_by_id(10)

    assert exc.value.status_code == 404


def test_create_bike(db_session, seeded_bikes):
    # Given
    bike_service = AdminBikeService(db_session)
    bike_create_dto = BikeCreateDto(
        name="Trek",
        description="Rower",
        price=Decimal("3999.99"),
        stock_quantity=5,
        is_active=True,
        brand_id=2,
    )
    current_user = {"user_id": 10}
    bikes_before = bike_service.get_all_bikes()

    with patch.object(bike_service, "_pick_random_image", return_value="/static/test.png"):
        # When
        bike_service.create_bike(bike_create_dto, current_user)

    # Then
    bikes_after = bike_service.get_all_bikes()
    assert len(bikes_before) < len(bikes_after)


def test_delete_bike_by_id(db_session, seeded_bikes):
    # Given
    bike_service = AdminBikeService(db_session)
    bike_repository = BikeRepository(db_session)

    # When
    bike_service.delete_bike_by_id(1)

    # Then
    assert bike_repository.get_bike_by_id(1) is None
