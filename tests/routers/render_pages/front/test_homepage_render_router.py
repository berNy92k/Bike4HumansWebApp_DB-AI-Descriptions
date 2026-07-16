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
def seeded_bike(db_session, clean_bikes_table):
    # Given
    bike = Bike(name="Trek Marlin 7", price=3999.99, stock_quantity=5, created_by=1, brand_id=1)
    db_session.add(bike)
    db_session.commit()

    return bike


def test_render_homepage(client, seeded_bike):
    # Given

    # When
    response = client.get("/")

    # Then
    assert response.status_code == 200
    assert "Trek Marlin 7" in response.text
