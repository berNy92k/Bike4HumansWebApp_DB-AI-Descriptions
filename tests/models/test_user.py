from app.models.user import User, Address, AddressType


def test_user_table_name():
    assert User.__tablename__ == "user"


def test_user_has_expected_columns():
    columns = User.__table__.columns

    assert "username" in columns
    assert "email" in columns
    assert "name" in columns
    assert "surname" in columns
    assert "hashed_password" in columns
    assert "is_active" in columns
    assert "email_verified" in columns
    assert "last_login" in columns
    assert "role_id" in columns
    assert "address_id" in columns


def test_user_required_columns_are_not_nullable():
    columns = User.__table__.columns

    assert columns["username"].nullable is False
    assert columns["email"].nullable is False
    assert columns["name"].nullable is False
    assert columns["surname"].nullable is False
    assert columns["hashed_password"].nullable is False
    assert columns["is_active"].nullable is False
    assert columns["email_verified"].nullable is False
    assert columns["role_id"].nullable is False
    assert columns["address_id"].nullable is False


def test_user_can_be_created():
    user = User(
        username="john_doe",
        email="john@example.com",
        name="John",
        surname="Doe",
        hashed_password="hashed-password",
        role_id=1,
        address_id=2,
        is_active=True,
        email_verified=False,
    )

    assert user.username == "john_doe"
    assert user.email == "john@example.com"
    assert user.name == "John"
    assert user.surname == "Doe"
    assert user.hashed_password == "hashed-password"
    assert user.is_active is True
    assert user.email_verified is False
    assert user.role_id == 1
    assert user.address_id == 2


def test_address_table_name():
    assert Address.__tablename__ == "addresses"


def test_address_has_expected_columns():
    columns = Address.__table__.columns

    assert "type" in columns
    assert "company_name" in columns
    assert "vat_number" in columns
    assert "address_line_1" in columns
    assert "address_line_2" in columns
    assert "city" in columns
    assert "postal_code" in columns
    assert "country_code" in columns
    assert "state_province" in columns
    assert "is_default" in columns


def test_address_required_columns_are_not_nullable():
    columns = Address.__table__.columns

    assert columns["type"].nullable is False
    assert columns["address_line_1"].nullable is False
    assert columns["city"].nullable is False
    assert columns["postal_code"].nullable is False
    assert columns["country_code"].nullable is False
    assert columns["state_province"].nullable is False
    assert columns["is_default"].nullable is False


def test_address_default_values():
    columns = Address.__table__.columns

    assert columns["type"].default.arg == AddressType.SHIPPING.name
    assert columns["is_default"].default.arg is True


def test_address_can_be_created():
    address = Address(
        type=AddressType.SHIPPING.name,
        address_line_1="ul. Testowa 1",
        city="Warszawa",
        postal_code="00-001",
        country_code="PL",
        state_province="Mazowieckie",
        is_default=True,
    )

    assert address.type == AddressType.SHIPPING.name
    assert address.address_line_1 == "ul. Testowa 1"
    assert address.city == "Warszawa"
    assert address.postal_code == "00-001"
    assert address.country_code == "PL"
    assert address.state_province == "Mazowieckie"
    assert address.is_default is True