import pytest

from app.models.bike import Bike
from app.repositories.bike_repository import BikeRepository
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
    repo = BikeRepository(db_session)

    # When
    result = repo.get_all_bikes()

    # Then
    assert len(result) == 3
    assert {bike.name for bike in seeded_bikes} == {bike.name for bike in result}


def test_get_last_x_bikes(db_session, seeded_bikes):
    # Given
    repo = BikeRepository(db_session)

    # When
    result = repo.get_last_x_bikes(2)

    # Then
    assert len(result) == 2


def test_get_bikes_paginated(db_session, seeded_bikes):
    # Given
    repo = BikeRepository(db_session)

    # When
    items, total = repo.get_bikes_paginated(page=1, size=2)

    # Then
    assert total == 3
    assert len(items) == 2


def test_get_bike_by_id(db_session, seeded_bikes):
    # Given
    repo = BikeRepository(db_session)
    bike_id = seeded_bikes[0].id

    # When
    result = repo.get_bike_by_id(bike_id)

    # Then
    assert result is not None
    assert result.name == seeded_bikes[0].name


def test_create_update_delete_bike(db_session, seeded_bikes):
    # Given
    repo = BikeRepository(db_session)
    result_before = repo.get_all_bikes()

    # When
    repo.delete(seeded_bikes[1])

    # Then
    result_after = repo.get_all_bikes()
    assert len(result_before) > len(result_after)
    assert 3 == len(result_before)
    assert 2 == len(result_after)