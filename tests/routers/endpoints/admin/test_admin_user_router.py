import pytest
from fastapi.testclient import TestClient

from app.main import app
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
    client = TestClient(app)

    yield client

    app.dependency_overrides.pop(get_current_user, None)


def login_as(user_id: int, role_id: int):
    app.dependency_overrides[get_current_user] = lambda: {"user_id": user_id, "role_id": role_id}


@pytest.fixture
def clean_tables(db_session):
    # Given
    db_session.query(User).delete()
    db_session.query(Address).delete()
    db_session.execute(role_permission.delete())
    db_session.query(Permission).delete()
    db_session.query(Role).delete()
    db_session.commit()

    yield

    db_session.query(User).delete()
    db_session.query(Address).delete()
    db_session.execute(role_permission.delete())
    db_session.query(Permission).delete()
    db_session.query(Role).delete()
    db_session.commit()


@pytest.fixture
def seeded_roles(db_session, clean_tables):
    # Given
    admin_panel_access = Permission(code=PermissionCode.ADMIN_PANEL_ACCESS)
    super_admin = Permission(code=PermissionCode.SUPER_ADMIN)
    db_session.add_all([admin_panel_access, super_admin])
    db_session.flush()

    roles = [
        Role(id=1, name="super_admin", description="Super admin", permissions=[admin_panel_access, super_admin]),
        Role(id=3, name="manager", description="Manager", permissions=[admin_panel_access]),
        Role(id=4, name="user", description="User"),
    ]
    for role in roles:
        db_session.add(role)
    db_session.commit()

    return roles


@pytest.fixture
def seeded_target_user(db_session, seeded_roles):
    # Given
    address = Address(
        id=1,
        address_line_1="Street 1",
        city="Warszawa",
        postal_code="00-001",
        country_code="PL",
        state_province="Mazowieckie",
    )
    db_session.add(address)

    user = User(
        username="target",
        email="target@example.com",
        name="Target",
        surname="User",
        hashed_password="hash",
        is_active=True,
        email_verified=True,
        role_id=4,
        address_id=1,
    )
    db_session.add(user)
    db_session.commit()

    return user


def _user_update_payload(role_id: int) -> dict:
    return {
        "username": "target",
        "email": "target@example.com",
        "name": "Target",
        "surname": "User",
        "role_id": role_id,
        "is_active": True,
        "email_verified": True,
    }


def test_get_all_users(client, seeded_target_user):
    # Given
    login_as(1, 1)

    # When
    response = client.get("/admin/user/")

    # Then
    assert response.status_code == 200
    data = response.json()
    assert any(u["username"] == "target" for u in data["items"])
    assert data["total"] == 1


def test_get_user_by_id(client, seeded_target_user):
    # Given
    login_as(1, 1)

    # When
    response = client.get(f"/admin/user/{seeded_target_user.id}")

    # Then
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "target"
    assert data["role_name"] == "user"


def test_get_user_by_id_not_found(client, seeded_target_user):
    # Given
    login_as(1, 1)

    # When
    response = client.get("/admin/user/999999")

    # Then
    assert response.status_code == 404


def test_update_user_all_fields_by_super_admin_allowed(client, seeded_target_user, db_session):
    # Given
    login_as(1, 1)

    # When
    response = client.put(f"/admin/user/{seeded_target_user.id}", json=_user_update_payload(role_id=1))

    # Then
    assert response.status_code == 200
    db_session.expire_all()
    updated = db_session.query(User).filter(User.id == seeded_target_user.id).first()
    assert updated.role_id == 1


def test_update_user_role_to_admin_role_by_manager_forbidden(client, seeded_target_user):
    # Given
    login_as(99, 3)

    # When
    response = client.put(f"/admin/user/{seeded_target_user.id}", json=_user_update_payload(role_id=1))

    # Then
    assert response.status_code == 403


def test_create_new_user_by_super_admin_allowed(client, seeded_roles, db_session):
    # Given
    login_as(1, 1)
    payload = {
        "username": "newuser",
        "email": "newuser@example.com",
        "name": "New",
        "surname": "User",
        "password": "secret123",
        "role_id": 4,
    }

    # When
    response = client.post("/admin/user/", json=payload)

    # Then
    assert response.status_code == 201
    created = db_session.query(User).filter(User.username == "newuser").first()
    assert created is not None
    assert created.address_id is None


def test_create_new_user_role_assignment_by_manager_forbidden(client, seeded_roles):
    # Given
    login_as(99, 3)
    payload = {
        "username": "newadmin",
        "email": "newadmin@example.com",
        "name": "New",
        "surname": "Admin",
        "password": "secret123",
        "role_id": 1,
    }

    # When
    response = client.post("/admin/user/", json=payload)

    # Then
    assert response.status_code == 403


def test_delete_user_by_id(client, seeded_target_user, db_session):
    # Given
    login_as(1, 1)

    # When
    response = client.delete(f"/admin/user/{seeded_target_user.id}")

    # Then
    assert response.status_code == 204
    assert db_session.query(User).filter(User.id == seeded_target_user.id).first() is None


def test_get_all_roles(client, seeded_roles):
    # Given
    login_as(1, 1)

    # When
    response = client.get("/admin/user/roles", params={"page": 1, "size": 10})

    # Then
    assert response.status_code == 200
    assert response.json()["total"] == 3


def test_get_role_by_id(client, seeded_roles):
    # Given
    login_as(1, 1)
    role_id = seeded_roles[2].id

    # When
    response = client.get(f"/admin/user/roles/{role_id}")

    # Then
    assert response.status_code == 200
    assert response.json()["name"] == "user"


def test_get_role_by_id_not_found(client, seeded_roles):
    # Given
    login_as(1, 1)

    # When
    response = client.get("/admin/user/roles/999999")

    # Then
    assert response.status_code == 404


def test_create_new_role_by_super_admin_allowed(client, seeded_roles):
    # Given
    login_as(1, 1)
    payload = {"name": "editor", "description": "Editor role", "permission_codes": []}

    # When
    response = client.post("/admin/user/role", json=payload)

    # Then
    assert response.status_code == 201


def test_create_new_role_by_manager_forbidden(client, seeded_roles):
    # Given
    login_as(99, 3)
    payload = {"name": "editor", "description": "Editor role", "permission_codes": []}

    # When
    response = client.post("/admin/user/role", json=payload)

    # Then
    assert response.status_code == 403


def test_update_role_by_id_by_super_admin_allowed(client, seeded_roles, db_session):
    # Given
    login_as(1, 1)
    role_id = seeded_roles[2].id
    payload = {"name": "user", "description": "Updated description", "permission_codes": []}

    # When
    response = client.patch(f"/admin/user/role/{role_id}", json=payload)

    # Then
    assert response.status_code == 200
    db_session.expire_all()
    updated = db_session.query(Role).filter(Role.id == role_id).first()
    assert updated.description == "Updated description"


def test_delete_role_by_id_by_manager_forbidden(client, seeded_roles):
    # Given
    login_as(99, 3)
    role_id = seeded_roles[2].id

    # When
    response = client.delete(f"/admin/user/role/{role_id}")

    # Then
    assert response.status_code == 403


def test_delete_role_by_id_by_super_admin_allowed(client, seeded_roles, db_session):
    # Given
    login_as(1, 1)
    role_id = seeded_roles[2].id

    # When
    response = client.delete(f"/admin/user/role/{role_id}")

    # Then
    assert response.status_code == 204
    assert db_session.query(Role).filter(Role.id == role_id).first() is None
