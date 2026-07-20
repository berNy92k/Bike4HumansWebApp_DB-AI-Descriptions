from unittest.mock import MagicMock, patch

import pytest
from fastapi import HTTPException

from app.models.manufacturer import Manufacturer
from app.repositories.manufacturer_repository import ManufacturerRepository
from app.schemas.admin.manufacturers.admin_manufacturer_ai_description_request_dto import ManufacturerAiDescriptionRequestDto
from app.schemas.admin.manufacturers.admin_manufacturer_create_dto import ManufacturerCreateDto
from app.schemas.admin.manufacturers.admin_manufacturer_list_request_dto import ManufacturerListRequestDto
from app.schemas.admin.manufacturers.admin_manufacturer_update_dto import ManufacturerUpdateDto
from app.services.admin.admin_manufacturer_service import AdminManufacturerService
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
def clean_manufacturer_table(db_session):
    # Given
    db_session.query(Manufacturer).delete()
    db_session.commit()

    yield

    db_session.query(Manufacturer).delete()
    db_session.commit()


@pytest.fixture
def seeded_manufacturers(db_session, clean_manufacturer_table):
    # Given
    manufacturers = [
        Manufacturer(name="Trek", description="Bike brand", image_url="/static/trek.png", created_by=1),
        Manufacturer(name="Giant", description="Bike brand", created_by=1),
        Manufacturer(name="Specialized", description="Bike brand", created_by=1),
    ]

    for manufacturer in manufacturers:
        db_session.add(manufacturer)
    db_session.commit()

    return manufacturers


def test_get_all_manufacturers(db_session, seeded_manufacturers):
    # Given
    service = AdminManufacturerService(db_session)

    # When
    result = service.get_all_manufacturers()

    # Then
    assert len(result) == 3


def test_get_manufacturers_paginated(db_session, seeded_manufacturers):
    # Given
    service = AdminManufacturerService(db_session)
    request_dto = ManufacturerListRequestDto(page=1, size=2)

    # When
    result = service.get_manufacturers_paginated(request_dto)

    # Then
    assert result.page == 1
    assert result.size == 2
    assert result.total == 3
    assert result.pages == 2


def test_get_manufacturer_by_id_found(db_session, seeded_manufacturers):
    # Given
    manufacturer_id = seeded_manufacturers[0].id
    service = AdminManufacturerService(db_session)

    # When
    result = service.get_manufacturer_by_id(manufacturer_id)

    # Then
    assert result.id == manufacturer_id


def test_get_manufacturer_by_id_not_found(db_session, seeded_manufacturers):
    # Given
    service = AdminManufacturerService(db_session)

    # When / Then
    with pytest.raises(HTTPException) as exc:
        service.get_manufacturer_by_id(999999)

    assert exc.value.status_code == 404


def test_create_manufacturer(db_session, seeded_manufacturers):
    # Given
    service = AdminManufacturerService(db_session)
    manufacturer_create_dto = ManufacturerCreateDto(name="Cannondale", description="Bike brand")
    current_user = {"user_id": 10}
    manufacturers_before = service.get_all_manufacturers()

    with patch.object(service, "_pick_random_image", return_value="/static/test.png"):
        # When
        service.create_manufacturer(manufacturer_create_dto, current_user)

    # Then
    manufacturers_after = service.get_all_manufacturers()
    assert len(manufacturers_before) < len(manufacturers_after)


def test_update_manufacturer_all_fields(db_session, seeded_manufacturers):
    # Given
    service = AdminManufacturerService(db_session)
    manufacturer_id = seeded_manufacturers[0].id
    update_dto = ManufacturerUpdateDto(name="Trek Bicycle Corporation", description="Updated description")

    # When
    service.update_manufacturer_all_fields(manufacturer_id, update_dto)

    # Then
    db_session.expire_all()
    updated = service.get_manufacturer_by_id(manufacturer_id)
    assert updated.name == "Trek Bicycle Corporation"
    assert updated.description == "Updated description"


def test_update_manufacturer_separate_fields_leaves_omitted_fields_untouched(db_session, seeded_manufacturers):
    # Given
    service = AdminManufacturerService(db_session)
    manufacturer_id = seeded_manufacturers[0].id
    update_dto = ManufacturerUpdateDto(name="Trek", description="Only description changed")

    # When
    service.update_manufacturer_separate_fields(manufacturer_id, update_dto)

    # Then
    db_session.expire_all()
    updated = service.get_manufacturer_by_id(manufacturer_id)
    assert updated.description == "Only description changed"
    assert updated.image_url == "/static/trek.png"


def test_create_manufacturer_persists_is_description_ai_generated(db_session, seeded_manufacturers):
    # Given
    service = AdminManufacturerService(db_session)
    manufacturer_repository = ManufacturerRepository(db_session)
    manufacturer_create_dto = ManufacturerCreateDto(
        name="Cannondale",
        description="Opis wygenerowany przez AI",
        is_description_ai_generated=True,
    )
    current_user = {"user_id": 10}

    with patch.object(service, "_pick_random_image", return_value="/static/test.png"):
        # When
        service.create_manufacturer(manufacturer_create_dto, current_user)

    # Then
    created = next(m for m in manufacturer_repository.get_all_manufacturers() if m.name == "Cannondale")
    assert created.is_description_ai_generated is True


def test_create_ai_description(db_session, seeded_manufacturers):
    # Given
    mock_ai_description_service = MagicMock()
    mock_ai_description_service.generate_description.return_value = "Wygenerowany opis producenta."
    service = AdminManufacturerService(db_session, ai_description_service=mock_ai_description_service)
    request_dto = ManufacturerAiDescriptionRequestDto(name="Trek")

    # When
    result = service.create_ai_description(request_dto)

    # Then
    assert result.description == "Wygenerowany opis producenta."
    mock_ai_description_service.generate_description.assert_called_once_with(request_dto)


def test_delete_manufacturer_by_id(db_session, seeded_manufacturers):
    # Given
    service = AdminManufacturerService(db_session)
    manufacturer_repository = ManufacturerRepository(db_session)
    manufacturer_id = seeded_manufacturers[0].id

    # When
    service.delete_manufacturer_by_id(manufacturer_id)

    # Then
    assert manufacturer_repository.get_manufacturer_by_id(manufacturer_id) is None
