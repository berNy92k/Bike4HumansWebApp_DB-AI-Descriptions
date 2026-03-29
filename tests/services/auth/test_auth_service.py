import pytest
from fastapi import HTTPException

from app.models.role import Role
from app.models.user import User
from app.services.auth.auth_service import AuthService, bcrypt_context
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
def clean_roles_table(db_session):
    # Given
    db_session.query(Role).delete()
    db_session.commit()

    yield

    db_session.query(Role).delete()
    db_session.commit()


@pytest.fixture
def clean_users_table(db_session):
    # Given
    db_session.query(User).delete()
    db_session.commit()

    yield

    db_session.query(User).delete()
    db_session.commit()


@pytest.fixture
def seeded_roles(db_session, clean_roles_table):
    # Given
    roles = [
        Role(id=1, name="Admin", description="Admin role"),
        Role(id=2, name="Moderator", description="Moderator role"),
        Role(id=3, name="Manager", description="Manager role"),
        Role(id=4, name="User", description="User role"),
    ]

    for role in roles:
        db_session.add(role)
    db_session.commit()

    return roles


@pytest.fixture
def seeded_users(db_session, clean_users_table, seeded_roles):
    # Given
    users = [
        User(
            username="admin",
            email="admin@example.com",
            name="Admin",
            surname="One",
            hashed_password=bcrypt_context.hash("admin123"),
            is_active=True,
            email_verified=True,
            role_id=1,
            address_id=1,
        ),
        User(
            username="john",
            email="john@example.com",
            name="John",
            surname="Doe",
            hashed_password=bcrypt_context.hash("secret123"),
            is_active=True,
            email_verified=False,
            role_id=4,
            address_id=1,
        ),
    ]

    for user in users:
        db_session.add(user)
    db_session.commit()

    return users


def test_authenticate_user_success(db_session, seeded_users):
    # Given
    auth_service = AuthService(db_session)

    # When
    result = auth_service.authenticate_user("john", "secret123")

    # Then
    assert result is not None
    assert result.username == "john"


def test_authenticate_user_wrong_password(db_session, seeded_users):
    # Given
    auth_service = AuthService(db_session)

    # When / Then
    with pytest.raises(HTTPException) as exc:
        auth_service.authenticate_user("john", "wrong-password")

    assert exc.value.status_code == 401
    assert exc.value.detail == "User is not authorized"


def test_authenticate_user_user_not_found(db_session, seeded_users):
    # Given
    auth_service = AuthService(db_session)

    # When / Then
    with pytest.raises(HTTPException) as exc:
        auth_service.authenticate_user("missing", "secret123")

    assert exc.value.status_code == 404
    assert exc.value.detail == "User not found"


@pytest.mark.asyncio
async def test_validate_access_allowed(db_session, seeded_users, monkeypatch):
    # Given
    auth_service = AuthService(db_session)

    async def fake_get_current_user_from_cookie(request):
        return {"user_id": seeded_users[0].id}

    monkeypatch.setattr(
        "app.services.auth.auth_service.get_current_user_from_cookie",
        fake_get_current_user_from_cookie,
    )

    # When
    result = await auth_service.validate_access(request=None)

    # Then
    assert result is not None
    assert result.username == "admin"


@pytest.mark.asyncio
async def test_validate_access_forbidden(db_session, seeded_users, monkeypatch):
    # Given
    auth_service = AuthService(db_session)

    async def fake_get_current_user_from_cookie(request):
        return {"user_id": seeded_users[1].id}

    monkeypatch.setattr(
        "app.services.auth.auth_service.get_current_user_from_cookie",
        fake_get_current_user_from_cookie,
    )

    # When / Then
    with pytest.raises(HTTPException) as exc:
        await auth_service.validate_access(request=None)

    assert exc.value.status_code == 403
    assert exc.value.detail == "User is forbidden"


@pytest.mark.asyncio
async def test_validate_access_user_not_found(db_session, seeded_users, monkeypatch):
    # Given
    auth_service = AuthService(db_session)

    async def fake_get_current_user_from_cookie(request):
        return {"user_id": 999}

    monkeypatch.setattr(
        "app.services.auth.auth_service.get_current_user_from_cookie",
        fake_get_current_user_from_cookie,
    )

    # When / Then
    with pytest.raises(HTTPException) as exc:
        await auth_service.validate_access(request=None)

    assert exc.value.status_code == 404
    assert exc.value.detail == "User not found"