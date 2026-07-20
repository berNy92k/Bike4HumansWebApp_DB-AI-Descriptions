from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.models.manufacturer import Manufacturer
from app.models.permission import Permission, PermissionCode, role_permission
from app.models.role import Role
from app.models.user import User, Address
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
    db_session.query(Manufacturer).delete()
    db_session.query(User).delete()
    db_session.query(Address).delete()
    db_session.execute(role_permission.delete())
    db_session.query(Permission).delete()
    db_session.query(Role).delete()
    db_session.commit()

    yield

    db_session.query(Manufacturer).delete()
    db_session.query(User).delete()
    db_session.query(Address).delete()
    db_session.execute(role_permission.delete())
    db_session.query(Permission).delete()
    db_session.query(Role).delete()
    db_session.commit()


@pytest.fixture
def seeded_data(db_session, clean_tables):
    # Given
    admin_panel_access = Permission(code=PermissionCode.ADMIN_PANEL_ACCESS)
    db_session.add(admin_panel_access)
    db_session.flush()

    role = Role(id=1, name="Admin", description="Admin role", permissions=[admin_panel_access])
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
    manufacturers = [
        Manufacturer(name="Trek", description="Bike brand", created_by=1),
        Manufacturer(name="Giant", description="Bike brand", created_by=1),
    ]

    db_session.add(role)
    db_session.add(address)
    db_session.add(user)
    for manufacturer in manufacturers:
        db_session.add(manufacturer)
    db_session.commit()

    return manufacturers


def test_find_all_manufacturers(client, seeded_data):
    # Given

    # When
    response = client.get("/admin/manufacturer/")

    # Then
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_find_manufacturer_by_id(client, seeded_data):
    # Given
    manufacturer_id = seeded_data[0].id

    # When
    response = client.get(f"/admin/manufacturer/{manufacturer_id}")

    # Then
    assert response.status_code == 200
    assert response.json()["id"] == manufacturer_id
    assert response.json()["name"] == "Trek"


def test_find_manufacturer_by_id_not_found(client, seeded_data):
    # Given

    # When
    response = client.get("/admin/manufacturer/999999")

    # Then
    assert response.status_code == 404


def test_create_manufacturer(client, seeded_data):
    # Given
    payload = {"name": "Specialized", "description": "Nowa marka"}

    manufacturers_before = len(client.get("/admin/manufacturer/").json())

    # When
    response = client.post("/admin/manufacturer/", json=payload)

    # Then
    assert response.status_code == 201
    manufacturers_after = len(client.get("/admin/manufacturer/").json())
    assert manufacturers_before < manufacturers_after


def test_update_manufacturer_all_fields(client, seeded_data, db_session):
    # Given
    manufacturer_id = seeded_data[0].id
    payload = {"name": "Trek Updated", "description": "Zaktualizowany opis"}

    # When
    response = client.put(f"/admin/manufacturer/{manufacturer_id}", json=payload)

    # Then
    assert response.status_code == 204
    db_session.expire_all()
    updated = db_session.query(Manufacturer).filter(Manufacturer.id == manufacturer_id).first()
    assert updated.name == "Trek Updated"


def test_update_manufacturer_separate_fields(client, seeded_data, db_session):
    # Given
    manufacturer_id = seeded_data[1].id
    payload = {"name": "Giant Updated", "description": "Bike brand"}

    # When
    response = client.patch(f"/admin/manufacturer/{manufacturer_id}", json=payload)

    # Then
    assert response.status_code == 204
    db_session.expire_all()
    updated = db_session.query(Manufacturer).filter(Manufacturer.id == manufacturer_id).first()
    assert updated.name == "Giant Updated"


def test_update_manufacturer_all_fields_sets_is_description_ai_generated(client, seeded_data, db_session):
    # Given
    manufacturer_id = seeded_data[0].id
    payload = {
        "name": "Trek Updated",
        "description": "Opis wygenerowany przez AI",
        "is_description_ai_generated": True,
    }

    # When
    response = client.put(f"/admin/manufacturer/{manufacturer_id}", json=payload)

    # Then
    assert response.status_code == 204
    db_session.expire_all()
    updated = db_session.query(Manufacturer).filter(Manufacturer.id == manufacturer_id).first()
    assert updated.is_description_ai_generated is True


def test_create_ai_description_for_manufacturer(client, seeded_data):
    # Given
    payload = {"name": "Trek"}

    with patch(
        "app.services.admin.admin_manufacturer_service.ManufacturerDescriptionAiService.generate_description",
        return_value="Wygenerowany opis producenta.",
    ):
        # When
        response = client.post("/admin/manufacturer/ai-generate-description", json=payload)

    # Then
    assert response.status_code == 201
    assert response.json() == {"description": "Wygenerowany opis producenta."}


def test_delete_manufacturer_by_id(client, seeded_data, db_session):
    # Given
    manufacturer_id = seeded_data[0].id

    # When
    response = client.delete(f"/admin/manufacturer/{manufacturer_id}")

    # Then
    assert response.status_code == 204
    assert db_session.query(Manufacturer).filter(Manufacturer.id == manufacturer_id).first() is None
