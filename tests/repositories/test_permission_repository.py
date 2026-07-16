import pytest

from app.models.permission import Permission, role_permission
from app.models.role import Role
from app.repositories.permission_repository import PermissionRepository
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
def clean_permission_table(db_session):
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
def seeded_permissions(db_session, clean_permission_table):
    # Given
    permissions = [
        Permission(code="ADMIN_PANEL_ACCESS", description="Access to the admin panel"),
        Permission(code="SUPER_ADMIN", description="Full access"),
        Permission(code="ORDERS_MANAGE", description="Manage orders"),
    ]

    for permission in permissions:
        db_session.add(permission)
    db_session.commit()

    return permissions


def test_get_all(db_session, seeded_permissions):
    # Given
    repo = PermissionRepository(db_session)

    # When
    result = repo.get_all()

    # Then
    assert len(result) == 3


def test_get_by_codes(db_session, seeded_permissions):
    # Given
    repo = PermissionRepository(db_session)

    # When
    result = repo.get_by_codes(["ADMIN_PANEL_ACCESS", "SUPER_ADMIN"])

    # Then
    assert len(result) == 2
    assert {p.code for p in result} == {"ADMIN_PANEL_ACCESS", "SUPER_ADMIN"}


def test_get_by_codes_ignores_unknown_codes(db_session, seeded_permissions):
    # Given
    repo = PermissionRepository(db_session)

    # When
    result = repo.get_by_codes(["ADMIN_PANEL_ACCESS", "NOT_A_REAL_CODE"])

    # Then
    assert len(result) == 1
    assert result[0].code == "ADMIN_PANEL_ACCESS"
