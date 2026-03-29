import pytest

from app.models.manufacturer import Manufacturer
from app.repositories.manufacturer_repository import ManufacturerRepository
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
        Manufacturer(name="Trek", description="Bike brand", image_url="https://example.com/trek.png", created_by=1),
        Manufacturer(name="Giant", description="Bike brand", image_url="https://example.com/giant.png", created_by=1),
        Manufacturer(name="Specialized", description="Bike brand", image_url="https://example.com/specialized.png", created_by=1),
    ]

    for manufacturer in manufacturers:
        db_session.add(manufacturer)
    db_session.commit()

    return manufacturers


def test_get_all_manufacturers(db_session, seeded_manufacturers):
    # Given
    repo = ManufacturerRepository(db_session)

    # When
    result = repo.get_all_manufacturers()

    # Then
    assert len(result) == 3


def test_get_manufacturer_by_id(db_session, seeded_manufacturers):
    # Given
    repo = ManufacturerRepository(db_session)
    manufacturer_id = seeded_manufacturers[0].id

    # When
    result = repo.get_manufacturer_by_id(manufacturer_id)

    # Then
    assert result is not None
    assert result.name == "Trek"


def test_get_manufacturers_paginated(db_session, seeded_manufacturers):
    # Given
    repo = ManufacturerRepository(db_session)

    # When
    items, total = repo.get_manufacturers_paginated(page=1, size=2)

    # Then
    assert total == 3
    assert len(items) == 2
