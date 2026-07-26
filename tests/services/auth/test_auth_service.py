import pytest
from fastapi import HTTPException

from app.models.permission import Permission, PermissionCode, role_permission
from app.models.role import Role
from app.models.user import User
from app.services.auth.auth_service import AuthService, bcrypt_context, get_current_admin_user
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
def clean_permission_tables(db_session):
    # Given
    db_session.execute(role_permission.delete())
    db_session.query(Permission).delete()
    db_session.commit()

    yield

    db_session.execute(role_permission.delete())
    db_session.query(Permission).delete()
    db_session.commit()


@pytest.fixture
def seeded_roles(db_session, clean_roles_table, clean_permission_tables):
    # Given
    admin_panel_access = Permission(code=PermissionCode.ADMIN_PANEL_ACCESS)
    super_admin = Permission(code=PermissionCode.SUPER_ADMIN)
    db_session.add_all([admin_panel_access, super_admin])
    db_session.flush()

    roles = [
        Role(id=1, name="Admin", description="Admin role", permissions=[admin_panel_access, super_admin]),
        Role(id=2, name="Moderator", description="Moderator role", permissions=[admin_panel_access]),
        Role(id=3, name="Manager", description="Manager role", permissions=[admin_panel_access]),
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
async def test_get_current_admin_user_allowed(db_session, seeded_roles):
    # Given
    current_user = {"user_id": 1, "username": "admin", "role_id": 1}

    # When
    result = await get_current_admin_user(current_user=current_user, db=db_session)

    # Then
    assert result == current_user


@pytest.mark.asyncio
async def test_get_current_admin_user_forbidden(db_session, seeded_roles):
    # Given
    current_user = {"user_id": 4, "username": "john", "role_id": 4}

    # When / Then
    with pytest.raises(HTTPException) as exc:
        await get_current_admin_user(current_user=current_user, db=db_session)

    assert exc.value.status_code == 403