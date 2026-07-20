from unittest.mock import MagicMock

import pytest
from fastapi import HTTPException

from app.models.bike import Bike
from app.schemas.admin.bike.admin_bike_list_request_dto import BikeListRequestDto
from app.services.front.bike_service import BikeService
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
    service = BikeService(db_session)

    # When
    result = service.get_all_bikes()

    # Then
    assert len(result) == 3


def test_get_last_x_bikes(db_session, seeded_bikes):
    # Given
    service = BikeService(db_session)

    # When
    result = service.get_last_x_bikes(2)

    # Then
    assert len(result) == 2


def test_get_bikes_paginated(db_session, seeded_bikes):
    # Given
    service = BikeService(db_session)
    request_dto = BikeListRequestDto(page=1, size=2)

    # When
    result = service.get_bikes_paginated(request_dto)

    # Then
    assert result.page == 1
    assert result.size == 2
    assert result.total == 3
    assert result.pages == 2


def test_get_bike_by_id_found(db_session, seeded_bikes):
    # Given
    bike_id = seeded_bikes[0].id
    service = BikeService(db_session)

    # When
    result = service.get_bike_by_id(bike_id)

    # Then
    assert result.id == bike_id


def test_get_bike_by_id_not_found(db_session, seeded_bikes):
    # Given
    service = BikeService(db_session)

    # When / Then
    with pytest.raises(HTTPException) as exc:
        service.get_bike_by_id(999999)

    assert exc.value.status_code == 404


def test_get_bikes_by_manufacturer_id(db_session, seeded_bikes):
    # Given
    service = BikeService(db_session)
    other_brand_bike = Bike(name="Cannondale Trail", price=2999.00, stock_quantity=1, created_by=1, brand_id=2)
    db_session.add(other_brand_bike)
    db_session.commit()

    # When
    result = service.get_bikes_by_manufacturer_id(1)

    # Then
    assert len(result) == 3
    assert all(bike.brand_id == 1 for bike in result)


def test_get_similar_bikes_recommendation(db_session, seeded_bikes):
    # Given
    mock_ai_recommendation_service = MagicMock()
    mock_ai_recommendation_service.generate_recommendation_note.return_value = "Warto rozważyć te opcje."
    service = BikeService(db_session, ai_recommendation_service=mock_ai_recommendation_service)
    bike_id = seeded_bikes[0].id

    # When
    result = service.get_similar_bikes_recommendation(bike_id)

    # Then
    assert result.note == "Warto rozważyć te opcje."
    assert len(result.bikes) == 2
    mock_ai_recommendation_service.generate_recommendation_note.assert_called_once()


def test_get_similar_bikes_recommendation_skips_ai_call_when_no_similar_bikes(db_session, clean_bikes_table):
    # Given
    mock_ai_recommendation_service = MagicMock()
    service = BikeService(db_session, ai_recommendation_service=mock_ai_recommendation_service)
    only_bike = Bike(name="Trek Marlin 7", price=3999.99, stock_quantity=5, created_by=1, brand_id=1)
    db_session.add(only_bike)
    db_session.commit()

    # When
    result = service.get_similar_bikes_recommendation(only_bike.id)

    # Then
    assert result.note is None
    assert result.bikes == []
    mock_ai_recommendation_service.generate_recommendation_note.assert_not_called()


def test_get_similar_bikes_recommendation_caches_note_in_db(db_session, seeded_bikes):
    # Given
    mock_ai_recommendation_service = MagicMock()
    mock_ai_recommendation_service.generate_recommendation_note.return_value = "Warto rozważyć te opcje."
    service = BikeService(db_session, ai_recommendation_service=mock_ai_recommendation_service)
    bike_id = seeded_bikes[0].id

    # When
    service.get_similar_bikes_recommendation(bike_id)
    service.get_similar_bikes_recommendation(bike_id)
    result = service.get_similar_bikes_recommendation(bike_id)

    # Then
    assert result.note == "Warto rozważyć te opcje."
    mock_ai_recommendation_service.generate_recommendation_note.assert_called_once()

    db_session.expire_all()
    cached_bike = service.get_bike_by_id(bike_id)
    assert cached_bike.similar_bikes_ai_note == "Warto rozważyć te opcje."
    assert cached_bike.similar_bikes_ai_note_generated_at is not None
