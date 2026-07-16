from app.models.permission import Permission


def test_permission_table_name():
    assert Permission.__tablename__ == "permission"


def test_permission_has_expected_columns():
    columns = Permission.__table__.columns

    assert "code" in columns
    assert "description" in columns


def test_permission_required_columns_are_not_nullable():
    columns = Permission.__table__.columns

    assert columns["code"].nullable is False


def test_permission_can_be_created():
    permission = Permission(
        code="SUPER_ADMIN",
        description="Full access to the admin panel",
    )

    assert permission.code == "SUPER_ADMIN"
    assert permission.description == "Full access to the admin panel"
