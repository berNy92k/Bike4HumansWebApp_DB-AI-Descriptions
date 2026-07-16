import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.models.role import Role
from app.models.user import User
from app.services.auth.auth_service import bcrypt_context
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
    db_session.query(User).delete()
    db_session.query(Role).delete()
    db_session.commit()

    yield

    db_session.query(User).delete()
    db_session.query(Role).delete()
    db_session.commit()


@pytest.fixture
def seeded_user(db_session, clean_tables):
    # Given
    role = Role(id=4, name="user", description="User")
    db_session.add(role)
    db_session.flush()

    user = User(
        username="john",
        email="john@example.com",
        name="John",
        surname="Doe",
        hashed_password=bcrypt_context.hash("secret123"),
        is_active=True,
        email_verified=True,
        role_id=4,
        address_id=1,
    )
    db_session.add(user)
    db_session.commit()

    return user


@pytest.fixture
def seeded_customer_role(db_session, clean_tables):
    # Given
    role = Role(id=4, name="user", description="User")
    db_session.add(role)
    db_session.commit()

    return role


def test_register_user(client, seeded_customer_role, db_session):
    # Given
    payload = {
        "username": "newuser",
        "email": "newuser@example.com",
        "name": "New",
        "surname": "User",
        "password": "secret123",
    }

    # When
    response = client.post("/auth/user", json=payload)

    # Then
    assert response.status_code == 201
    created = db_session.query(User).filter(User.username == "newuser").first()
    assert created is not None
    assert created.address_id is None
    assert created.role_id == 4


def test_create_token_success(client, seeded_user):
    # Given
    form_data = {"username": "john", "password": "secret123"}

    # When
    response = client.post("/auth/token", data=form_data, follow_redirects=False)

    # Then
    assert response.status_code == 303
    assert response.headers["location"] == "/"
    assert "access_token" in response.cookies


def test_create_token_wrong_password(client, seeded_user):
    # Given
    form_data = {"username": "john", "password": "wrong-password"}

    # When
    response = client.post("/auth/token", data=form_data, follow_redirects=False)

    # Then
    assert response.status_code == 401


def test_create_token_unknown_user(client, clean_tables):
    # Given
    form_data = {"username": "unknown", "password": "secret123"}

    # When
    response = client.post("/auth/token", data=form_data, follow_redirects=False)

    # Then
    assert response.status_code == 404


def test_logout(client):
    # Given

    # When
    response = client.get("/auth/logout", follow_redirects=False)

    # Then
    assert response.status_code == 303
    assert response.headers["location"] == "/auth/login"
