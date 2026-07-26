import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.models.bike import Bike
from app.models.manufacturer import Manufacturer
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
def clean_manufacturers_table(db_session):
    # Given
    db_session.query(Manufacturer).delete()
    db_session.commit()

    yield

    db_session.query(Manufacturer).delete()
    db_session.commit()


@pytest.fixture
def seeded_manufacturers(db_session, clean_manufacturers_table):
    # Given
    manufacturers = [
        Manufacturer(name="Trek", description="Bike brand", created_by=1),
        Manufacturer(name="Giant", description="Bike brand", created_by=1),
    ]
    for manufacturer in manufacturers:
        db_session.add(manufacturer)
    db_session.commit()

    return manufacturers


def test_find_manufacturers(client, seeded_manufacturers):
    # Given

    # When
    response = client.get("/api/manufacturers/")

    # Then
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 2
    assert data["total"] == 2


def test_find_manufacturer_by_id(client, seeded_manufacturers):
    # Given
    manufacturer_id = seeded_manufacturers[0].id

    # When
    response = client.get(f"/api/manufacturers/{manufacturer_id}")

    # Then
    assert response.status_code == 200
    assert response.json()["name"] == "Trek"


def test_find_manufacturer_by_id_not_found(client, seeded_manufacturers):
    # Given

    # When
    response = client.get("/api/manufacturers/999999")

    # Then
    assert response.status_code == 404


def test_find_bikes_by_manufacturer(client, seeded_manufacturers, db_session):
    # Given
    manufacturer_id = seeded_manufacturers[0].id
    other_id = seeded_manufacturers[1].id
    bikes = [
        Bike(name="Trek Marlin 7", price=100.0, stock_quantity=1, created_by=1, brand_id=manufacturer_id),
        Bike(name="Giant Talon 1", price=100.0, stock_quantity=1, created_by=1, brand_id=other_id),
    ]
    for bike in bikes:
        db_session.add(bike)
    db_session.commit()

    # When
    response = client.get(f"/api/manufacturers/{manufacturer_id}/bikes")

    # Then
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Trek Marlin 7"

    db_session.query(Bike).delete()
    db_session.commit()
