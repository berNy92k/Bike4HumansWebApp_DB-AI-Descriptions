import pytest

from app.models.permission import Permission, role_permission
from app.models.role import Role
from app.repositories.role_repository import RoleRepository
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
def clean_role_table(db_session):
    # Given
    db_session.execute(role_permission.delete())
    db_session.query(Permission).delete()
    db_session.query(Role).delete()
    db_session.commit()

    yield

    db_session.execute(role_permission.delete())
    db_session.query(Permission).delete()
    db_session.query(Role).delete()
    db_session.commit()


@pytest.fixture
def seeded_roles(db_session, clean_role_table):
    # Given
    roles = [
        Role(name="admin", description="Administrator"),
        Role(name="manager", description="Manager"),
        Role(name="customer", description="Customer"),
    ]

    for role in roles:
        db_session.add(role)
    db_session.commit()

    return roles


def test_get_all_roles(db_session, seeded_roles):
    # Given
    repo = RoleRepository(db_session)

    # When
    result = repo.get_all_roles()

    # Then
    assert len(result) == 3


def test_get_role_by_id(db_session, seeded_roles):
    # Given
    repo = RoleRepository(db_session)
    role_id = seeded_roles[0].id

    # When
    result = repo.get_role_by_id(role_id)

    # Then
    assert result is not None
    assert result.name == "admin"


def test_get_role_by_id_not_found(db_session, seeded_roles):
    # Given
    repo = RoleRepository(db_session)

    # When
    result = repo.get_role_by_id(999999)

    # Then
    assert result is None


def test_get_roles_paginated(db_session, seeded_roles):
    # Given
    repo = RoleRepository(db_session)

    # When
    items, total = repo.get_roles_paginated(page=1, size=2)

    # Then
    assert total == 3
    assert len(items) == 2


def test_create_role(db_session, clean_role_table):
    # Given
    repo = RoleRepository(db_session)
    role = Role(name="editor", description="Editor")

    # When
    repo.create_role(role)

    # Then
    assert role.id is not None
    assert repo.get_role_by_id(role.id).name == "editor"


def test_update_role(db_session, seeded_roles):
    # Given
    repo = RoleRepository(db_session)
    role = seeded_roles[0]
    role.description = "Updated description"

    # When
    repo.update_role(role)

    # Then
    db_session.expire_all()
    updated = repo.get_role_by_id(role.id)
    assert updated.description == "Updated description"


def test_delete_role(db_session, seeded_roles):
    # Given
    repo = RoleRepository(db_session)
    role = seeded_roles[0]

    # When
    repo.delete_role(role)

    # Then
    assert repo.get_role_by_id(role.id) is None
