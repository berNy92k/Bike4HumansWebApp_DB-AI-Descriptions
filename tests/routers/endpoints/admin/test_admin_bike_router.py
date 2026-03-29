import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.models.bike import Bike
from app.models.user import User, Address
from app.models.role import Role
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
    app.dependency_overrides[get_current_user] = lambda: {"user_id": 1, "role_id": 1}
    client = TestClient(app)

    yield client

    app.dependency_overrides.pop(get_current_user, None)


@pytest.fixture
def clean_tables(db_session):
    # Given
    db_session.query(Bike).delete()
    db_session.query(User).delete()
    db_session.query(Address).delete()
    db_session.query(Role).delete()
    db_session.commit()

    yield

    db_session.query(Bike).delete()
    db_session.query(User).delete()
    db_session.query(Address).delete()
    db_session.query(Role).delete()
    db_session.commit()


@pytest.fixture
def seeded_data(db_session, clean_tables):
    # Given
    roles = [
        Role(id=1, name="Admin", description="Admin role"),
    ]
    address = Address(
        id=1,
        address_line_1="Street 1",
        city="Warszawa",
        postal_code="00-001",
        country_code="PL",
        state_province="Mazowieckie",
    )
    user = User(
        id=1,
        username="admin",
        email="admin@example.com",
        name="Admin",
        surname="One",
        hashed_password="hash",
        is_active=True,
        email_verified=True,
        role_id=1,
        address_id=1,
    )
    bikes = [
        Bike(name="Trek Marlin 7", price=3999.99, stock_quantity=5, created_by=1, brand_id=1),
        Bike(name="Giant Talon 1", price=3499.00, stock_quantity=3, created_by=1, brand_id=1),
    ]

    for role in roles:
        db_session.add(role)
    db_session.add(address)
    db_session.add(user)
    for bike in bikes:
        db_session.add(bike)
    db_session.commit()

    return bikes


def test_find_all_bikes(client, seeded_data):
    # Given

    # When
    response = client.get("/admin/bikes/")

    # Then
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_find_bike_by_id(client, seeded_data):
    # Given
    bike_id = seeded_data[0].id

    # When
    response = client.get(f"/admin/bikes/{bike_id}")

    # Then
    assert response.status_code == 200
    assert response.json()["id"] == bike_id
    assert response.json()["name"] == "Trek Marlin 7"


def test_find_bike_by_id_not_found(client, seeded_data):
    # Given

    # When
    response = client.get("/admin/bikes/999")

    # Then
    assert response.status_code == 404


def test_create_bike(client, seeded_data):
    # Given
    payload = {
        "name": "Specialized Rockhopper",
        "description": "Nowy rower",
        "price": 4299.50,
        "stock_quantity": 2,
        "is_active": True,
        "brand_id": 1,
    }

    bikes_before = len(client.get("/admin/bikes/").json())

    # When
    response = client.post("/admin/bikes/", json=payload)

    # Then
    assert response.status_code == 201
    bikes_after = len(client.get("/admin/bikes/").json())
    assert bikes_before < bikes_after


def test_update_bike_all_fields(client, seeded_data, db_session):
    # Given
    bike_id = seeded_data[0].id
    payload = {
        "name": "Trek Updated",
        "description": "Zaktualizowany opis",
        "price": 4999.99,
        "stock_quantity": 10,
        "image_url": "/static/test.png",
        "is_active": False,
        "brand_id": 2,
    }

    # When
    response = client.put(f"/admin/bikes/{bike_id}", json=payload)

    # Then
    assert response.status_code == 204
    db_session.expire_all()
    updated_bike = db_session.query(Bike).filter(Bike.id == bike_id).first()
    assert updated_bike is not None
    assert updated_bike.name == "Trek Updated"
    assert updated_bike.brand_id == 2


def test_update_bike_separate_fields(client, seeded_data, db_session):
    # Given
    bike_id = seeded_data[1].id
    payload = {
        "name": "Giant Updated",
        "stock_quantity": 7,
        "price": 4999.99,
        "brand_id": 2
    }

    # When
    response = client.patch(f"/admin/bikes/{bike_id}", json=payload)

    # Then
    assert response.status_code == 204
    db_session.expire_all()
    updated_bike = db_session.query(Bike).filter(Bike.id == bike_id).first()
    assert updated_bike is not None
    assert updated_bike.name == "Giant Updated"
    assert updated_bike.stock_quantity == 7


def test_delete_bike_by_id(client, seeded_data, db_session):
    # Given
    bike_id = seeded_data[0].id

    # When
    response = client.delete(f"/admin/bikes/{bike_id}")

    # Then
    assert response.status_code == 204
    deleted_bike = db_session.query(Bike).filter(Bike.id == bike_id).first()
    assert deleted_bike is None