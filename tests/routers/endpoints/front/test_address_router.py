import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.models.user import Address, User
from app.services.auth.auth_service import get_current_user
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
    # Given
    app.dependency_overrides[get_current_user] = lambda: {"user_id": 1, "role_id": 4}
    client = TestClient(app)

    yield client

    app.dependency_overrides.pop(get_current_user, None)


@pytest.fixture
def clean_tables(db_session):
    # Given
    db_session.query(User).delete()
    db_session.query(Address).delete()
    db_session.commit()

    yield

    db_session.query(User).delete()
    db_session.query(Address).delete()
    db_session.commit()


@pytest.fixture
def seeded_user_with_address(db_session, clean_tables):
    # Given
    address = Address(address_line_1="Street 1", city="Warszawa", postal_code="00-001",
                       country_code="PL", state_province="Mazowieckie")
    db_session.add(address)
    db_session.commit()

    user = User(id=1, username="john", email="john@example.com", name="John", surname="Doe",
                hashed_password="hash", role_id=1, address_id=address.id)
    db_session.add(user)
    db_session.commit()

    return user, address


@pytest.fixture
def seeded_user_without_address(db_session, clean_tables):
    # Given
    user = User(id=1, username="john", email="john@example.com", name="John", surname="Doe",
                hashed_password="hash", role_id=1, address_id=None)
    db_session.add(user)
    db_session.commit()

    return user


def test_get_my_address(client, seeded_user_with_address):
    # Given
    _, address = seeded_user_with_address

    # When
    response = client.get("/address/me")

    # Then
    assert response.status_code == 200
    assert response.json()["city"] == "Warszawa"
    assert response.json()["id"] == address.id


def test_get_my_address_not_found(client, seeded_user_without_address):
    # Given

    # When
    response = client.get("/address/me")

    # Then
    assert response.status_code == 404


def test_save_my_address_creates_address(client, seeded_user_without_address, db_session):
    # Given
    payload = {
        "address_line_1": "Nowa 1",
        "city": "Krakow",
        "postal_code": "30-001",
        "country_code": "PL",
        "state_province": "Malopolskie",
    }

    # When
    response = client.put("/address/me", json=payload)

    # Then
    assert response.status_code == 200
    assert response.json()["city"] == "Krakow"
    db_session.expire_all()
    user = db_session.query(User).filter(User.id == 1).first()
    assert user.address_id == response.json()["id"]


def test_save_my_address_updates_existing_address(client, seeded_user_with_address):
    # Given
    _, address = seeded_user_with_address
    payload = {
        "address_line_1": "Zmieniona 5",
        "city": "Poznan",
        "postal_code": "60-001",
        "country_code": "PL",
        "state_province": "Wielkopolskie",
    }

    # When
    response = client.put("/address/me", json=payload)

    # Then
    assert response.status_code == 200
    assert response.json()["id"] == address.id
    assert response.json()["city"] == "Poznan"


def test_save_my_address_requires_required_fields(client, seeded_user_without_address):
    # Given
    payload = {"city": "Krakow"}

    # When
    response = client.put("/address/me", json=payload)

    # Then
    assert response.status_code == 422
