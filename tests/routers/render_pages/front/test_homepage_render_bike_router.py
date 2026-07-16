import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.models.bike import Bike
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
def client():
    return TestClient(app)


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
    ]
    for bike in bikes:
        db_session.add(bike)
    db_session.commit()

    return bikes


def test_render_bikes_list(client, seeded_bikes):
    # Given

    # When
    response = client.get("/bikes/")

    # Then
    assert response.status_code == 200
    assert "Trek Marlin 7" in response.text
    assert "Giant Talon 1" in response.text


def test_render_bike_details(client, seeded_bikes):
    # Given
    bike_id = seeded_bikes[0].id

    # When
    response = client.get(f"/bikes/{bike_id}")

    # Then
    assert response.status_code == 200
    assert "Trek Marlin 7" in response.text


def test_render_bike_details_not_found(client, seeded_bikes):
    # Given

    # When
    response = client.get("/bikes/999999")

    # Then
    assert response.status_code == 404
