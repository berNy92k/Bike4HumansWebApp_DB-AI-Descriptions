from decimal import Decimal
from unittest.mock import MagicMock, patch

import pytest
from fastapi import HTTPException

from app.models.bike import Bike
from app.repositories.bike_repository import BikeRepository
from app.schemas.admin.bike.admin_bike_ai_description_request_dto import BikeAiDescriptionRequestDto
from app.schemas.admin.bike.admin_bike_auto_tag_request_dto import BikeAutoTagRequestDto
from app.schemas.admin.bike.admin_bike_auto_tag_response_dto import BikeAutoTagResponseDto
from app.schemas.admin.bike.admin_bike_create_dto import BikeCreateDto
from app.schemas.admin.bike.admin_bike_list_request_dto import BikeListRequestDto
from app.schemas.admin.bike.admin_bike_update_dto import BikeUpdateDto
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


def test_create_bike_persists_is_description_ai_generated(db_session, seeded_bikes):
    # Given
    bike_service = AdminBikeService(db_session)
    bike_repository = BikeRepository(db_session)
    bike_create_dto = BikeCreateDto(
        name="Trek",
        description="Opis wygenerowany przez AI",
        price=Decimal("3999.99"),
        stock_quantity=5,
        is_active=True,
        is_description_ai_generated=True,
        brand_id=2,
    )
    current_user = {"user_id": 10}

    with patch.object(bike_service, "_pick_random_image", return_value="/static/test.png"):
        # When
        bike_service.create_bike(bike_create_dto, current_user)

    # Then
    created_bike = next(bike for bike in bike_repository.get_all_bikes() if bike.name == "Trek")
    assert created_bike.is_description_ai_generated is True


def test_update_bike_all_fields_invalidates_similar_bikes_note_on_price_change(db_session, seeded_bikes):
    # Given
    bike_service = AdminBikeService(db_session)
    bike_repository = BikeRepository(db_session)
    bike = bike_repository.get_bike_by_id(seeded_bikes[0].id)
    bike.similar_bikes_ai_note = "Stara notatka."
    bike_repository.update_bike(bike)

    update_dto = BikeUpdateDto(name=bike.name, price=Decimal("4999.99"), stock_quantity=1, brand_id=bike.brand_id)

    # When
    bike_service.update_bike_all_fields(bike.id, update_dto)

    # Then
    db_session.expire_all()
    updated = bike_repository.get_bike_by_id(bike.id)
    assert updated.similar_bikes_ai_note is None
    assert updated.similar_bikes_ai_note_generated_at is None


def test_update_bike_all_fields_keeps_similar_bikes_note_when_price_unchanged(db_session, seeded_bikes):
    # Given
    bike_service = AdminBikeService(db_session)
    bike_repository = BikeRepository(db_session)
    bike = bike_repository.get_bike_by_id(seeded_bikes[0].id)
    bike.similar_bikes_ai_note = "Stara notatka."
    bike_repository.update_bike(bike)

    update_dto = BikeUpdateDto(
        name="Nowa nazwa", price=bike.price, stock_quantity=1, brand_id=bike.brand_id
    )

    # When
    bike_service.update_bike_all_fields(bike.id, update_dto)

    # Then
    db_session.expire_all()
    updated = bike_repository.get_bike_by_id(bike.id)
    assert updated.similar_bikes_ai_note == "Stara notatka."


def test_delete_bike_by_id(db_session, seeded_bikes):
    # Given
    bike_service = AdminBikeService(db_session)
    bike_repository = BikeRepository(db_session)

    # When
    bike_service.delete_bike_by_id(1)

    # Then
    assert bike_repository.get_bike_by_id(1) is None


def test_create_ai_description(db_session, seeded_bikes):
    # Given
    mock_ai_description_service = MagicMock()
    mock_ai_description_service.generate_description.return_value = "Wygenerowany opis roweru."
    bike_service = AdminBikeService(db_session, ai_description_service=mock_ai_description_service)
    request_dto = BikeAiDescriptionRequestDto(name="Trek Marlin 7", brand_id=1)

    # When
    result = bike_service.create_ai_description(request_dto)

    # Then
    assert result.description == "Wygenerowany opis roweru."
    mock_ai_description_service.generate_description.assert_called_once_with(request_dto)


def test_generate_auto_tags(db_session, seeded_bikes):
    # Given
    mock_ai_auto_tag_service = MagicMock()
    mock_ai_auto_tag_service.generate_tags.return_value = BikeAutoTagResponseDto(
        bike_type="MOUNTAIN", frame_material="ALUMINIUM"
    )
    bike_service = AdminBikeService(db_session, ai_auto_tag_service=mock_ai_auto_tag_service)
    request_dto = BikeAutoTagRequestDto(name="Trek Marlin 7", description="Lekki rower górski.")

    # When
    result = bike_service.generate_auto_tags(request_dto)

    # Then
    assert result.bike_type == "MOUNTAIN"
    assert result.frame_material == "ALUMINIUM"
    mock_ai_auto_tag_service.generate_tags.assert_called_once_with(request_dto)
