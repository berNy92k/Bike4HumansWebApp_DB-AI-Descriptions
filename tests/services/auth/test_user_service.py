import pytest
from fastapi import HTTPException

from app.models.role import Role
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.admin.user.admin_user_create_dto import UserCreateDto
from app.services.auth.user_service import UserService
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
            username="john",
            email="john@example.com",
            name="John",
            surname="Doe",
            hashed_password="hash1",
            is_active=True,
            email_verified=False,
            role_id=4,
            address_id=1,
        ),
        User(
            username="anna",
            email="anna@example.com",
            name="Anna",
            surname="Nowak",
            hashed_password="hash2",
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


def test_find_user_by_id(db_session, seeded_users):
    # Given
    user_service = UserService(db_session)
    user_id = seeded_users[0].id

    # When
    result = user_service.find_user_by_id(user_id)

    # Then
    assert result is not None
    assert result.username == "john"


def test_find_user_by_id_not_found(db_session, seeded_users):
    # Given
    user_service = UserService(db_session)

    # When / Then
    with pytest.raises(HTTPException) as exc:
        user_service.find_user_by_id(999)

    assert exc.value.status_code == 404
    assert exc.value.detail == "User not found"


def test_find_user_by_username(db_session, seeded_users):
    # Given
    user_service = UserService(db_session)

    # When
    result = user_service.find_user_by_username("anna")

    # Then
    assert result is not None
    assert result.email == "anna@example.com"


def test_find_user_by_username_not_found(db_session, seeded_users):
    # Given
    user_service = UserService(db_session)

    # When / Then
    with pytest.raises(HTTPException) as exc:
        user_service.find_user_by_username("missing")

    assert exc.value.status_code == 404
    assert exc.value.detail == "User not found"
