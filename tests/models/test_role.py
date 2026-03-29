from app.models.role import Role


def test_role_table_name():
    assert Role.__tablename__ == "role"


def test_role_has_expected_columns():
    columns = Role.__table__.columns

    assert "name" in columns
    assert "description" in columns


def test_role_required_columns_are_not_nullable():
    columns = Role.__table__.columns

    assert columns["name"].nullable is False


def test_role_can_be_created():
    role = Role(
        name="ADMIN",
        description="Administrator",
    )

    assert role.name == "ADMIN"
    assert role.description == "Administrator"
