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
def clean_tables(db_session):
    # Given
    db_session.query(Bike).delete()
    db_session.query(Manufacturer).delete()
    db_session.commit()

    yield

    db_session.query(Bike).delete()
    db_session.query(Manufacturer).delete()
    db_session.commit()


@pytest.fixture
def seeded_data(db_session, clean_tables):
    # Given
    manufacturers = [
        Manufacturer(name="Trek", description="Opis producenta Trek", created_by=1),
        Manufacturer(name="Giant", description="Opis producenta Giant", created_by=1),
    ]
    for manufacturer in manufacturers:
        db_session.add(manufacturer)
    db_session.flush()

    bikes = [
        Bike(name="Trek Marlin 7", price=3999.99, stock_quantity=5, created_by=1, brand_id=manufacturers[0].id),
        Bike(name="Trek Domane AL 2", price=5299.00, stock_quantity=2, created_by=1, brand_id=manufacturers[0].id),
    ]
    for bike in bikes:
        db_session.add(bike)
    db_session.commit()

    return manufacturers, bikes


def test_render_manufacturers_list(client, seeded_data):
    # Given
    manufacturers, _ = seeded_data

    # When
    response = client.get("/manufacturers/")

    # Then
    assert response.status_code == 200
    assert "Trek" in response.text
    assert "Giant" in response.text
    assert "2 modeli" in response.text
    assert "0 modeli" in response.text


def test_render_manufacturer_details(client, seeded_data):
    # Given
    manufacturers, bikes = seeded_data
    manufacturer_id = manufacturers[0].id

    # When
    response = client.get(f"/manufacturers/{manufacturer_id}")

    # Then
    assert response.status_code == 200
    assert "Trek" in response.text
    assert "Trek Marlin 7" in response.text
    assert "Trek Domane AL 2" in response.text


def test_render_manufacturer_details_not_found(client, seeded_data):
    # Given

    # When
    response = client.get("/manufacturers/999999")

    # Then
    assert response.status_code == 404
