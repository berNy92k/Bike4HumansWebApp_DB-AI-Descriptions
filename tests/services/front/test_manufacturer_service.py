import pytest
from fastapi import HTTPException

from app.models.manufacturer import Manufacturer
from app.schemas.admin.manufacturers.admin_manufacturer_list_request_dto import ManufacturerListRequestDto
from app.services.front.manufacturer_service import ManufacturerService
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
        Manufacturer(name="Trek", description="Bike brand", created_by=1),
        Manufacturer(name="Giant", description="Bike brand", created_by=1),
        Manufacturer(name="Specialized", description="Bike brand", created_by=1),
    ]

    for manufacturer in manufacturers:
        db_session.add(manufacturer)
    db_session.commit()

    return manufacturers


def test_get_all_manufacturers(db_session, seeded_manufacturers):
    # Given
    service = ManufacturerService(db_session)

    # When
    result = service.get_all_manufacturers()

    # Then
    assert len(result) == 3


def test_get_manufacturers_paginated(db_session, seeded_manufacturers):
    # Given
    service = ManufacturerService(db_session)
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
    service = ManufacturerService(db_session)

    # When
    result = service.get_manufacturer_by_id(manufacturer_id)

    # Then
    assert result.id == manufacturer_id


def test_get_manufacturer_by_id_not_found(db_session, seeded_manufacturers):
    # Given
    service = ManufacturerService(db_session)

    # When / Then
    with pytest.raises(HTTPException) as exc:
        service.get_manufacturer_by_id(999999)

    assert exc.value.status_code == 404
