import pytest
from fastapi import HTTPException

from app.models.permission import Permission, PermissionCode, role_permission
from app.models.role import Role
from app.models.user import User, Address
from app.schemas.admin.user.admin_user_create_dto import UserCreateDto
from app.schemas.admin.user.admin_user_update_dto import UserUpdateDto
from app.schemas.admin.user.role.admin_role_create_dto import RoleCreateDto
from app.services.admin.admin_user_service import AdminUserService
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


def _user_update_dto(role_id: int) -> UserUpdateDto:
    return UserUpdateDto(
        username="target",
        email="target@example.com",
        name="Target",
        surname="User",
        role_id=role_id,
        is_active=True,
        email_verified=True,
    )


def test_create_user_by_super_admin_allowed(db_session, seeded_roles):
    # Given
    service = AdminUserService(db_session)
    current_user = {"user_id": 1, "role_id": 1}
    dto = UserCreateDto(username="newuser", email="newuser@example.com", name="New", surname="User",
                        password="secret123", role_id=4)

    # When
    service.create_user(dto, current_user)

    # Then
    users = service.get_all_users()
    created = next(u for u in users if u.username == "newuser")
    assert created.address_id is None
    assert created.role_id == 4


def test_create_user_admin_role_by_manager_forbidden(db_session, seeded_roles):
    # Given
    service = AdminUserService(db_session)
    current_user = {"user_id": 99, "role_id": 3}
    dto = UserCreateDto(username="newadmin", email="newadmin@example.com", name="New", surname="Admin",
                        password="secret123", role_id=1)

    # When / Then
    with pytest.raises(HTTPException) as exc:
        service.create_user(dto, current_user)

    assert exc.value.status_code == 403


def test_update_user_role_to_admin_role_by_manager_forbidden(db_session, seeded_target_user):
    # Given
    service = AdminUserService(db_session)
    current_user = {"user_id": 99, "role_id": 3}

    # When / Then
    with pytest.raises(HTTPException) as exc:
        service.update_user_all_fields(seeded_target_user.id, _user_update_dto(role_id=1), current_user)

    assert exc.value.status_code == 403


def test_update_user_role_to_admin_role_by_super_admin_allowed(db_session, seeded_target_user):
    # Given
    service = AdminUserService(db_session)
    current_user = {"user_id": 1, "role_id": 1}

    # When
    service.update_user_all_fields(seeded_target_user.id, _user_update_dto(role_id=1), current_user)

    # Then
    db_session.expire_all()
    updated = db_session.get(User, seeded_target_user.id)
    assert updated.role_id == 1


def test_update_user_role_to_plain_role_by_manager_allowed(db_session, seeded_target_user):
    # Given
    service = AdminUserService(db_session)
    current_user = {"user_id": 99, "role_id": 3}

    # When
    service.update_user_all_fields(seeded_target_user.id, _user_update_dto(role_id=4), current_user)

    # Then
    db_session.expire_all()
    updated = db_session.get(User, seeded_target_user.id)
    assert updated.role_id == 4


def test_create_role_by_manager_forbidden(db_session, seeded_roles):
    # Given
    service = AdminUserService(db_session)
    current_user = {"user_id": 99, "role_id": 3}
    dto = RoleCreateDto(name="editor", description="Editor role", permission_codes=[])

    # When / Then
    with pytest.raises(HTTPException) as exc:
        service.create_role(dto, current_user)

    assert exc.value.status_code == 403


def test_create_role_by_super_admin_allowed(db_session, seeded_roles):
    # Given
    service = AdminUserService(db_session)
    current_user = {"user_id": 1, "role_id": 1}
    dto = RoleCreateDto(name="editor", description="Editor role", permission_codes=[PermissionCode.ADMIN_PANEL_ACCESS])

    # When
    service.create_role(dto, current_user)

    # Then
    roles = service.get_all_roles()
    assert any(r.name == "editor" for r in roles)


def test_create_role_with_unknown_permission_code(db_session, seeded_roles):
    # Given
    service = AdminUserService(db_session)
    current_user = {"user_id": 1, "role_id": 1}
    dto = RoleCreateDto(name="editor", description="Editor role", permission_codes=["NOT_A_REAL_CODE"])

    # When / Then
    with pytest.raises(HTTPException) as exc:
        service.create_role(dto, current_user)

    assert exc.value.status_code == 400


def test_delete_role_by_manager_forbidden(db_session, seeded_roles):
    # Given
    service = AdminUserService(db_session)
    current_user = {"user_id": 99, "role_id": 3}

    # When / Then
    with pytest.raises(HTTPException) as exc:
        service.delete_role_by_id(4, current_user)

    assert exc.value.status_code == 403
