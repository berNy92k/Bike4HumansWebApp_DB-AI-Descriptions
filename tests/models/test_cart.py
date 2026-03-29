from app.models.cart import Cart, CartStatus


def test_cart_table_name():
    assert Cart.__tablename__ == "carts"


def test_cart_has_expected_columns():
    columns = Cart.__table__.columns

    assert "user_id" in columns
    assert "currency" in columns
    assert "status" in columns
    assert "created_at" in columns
    assert "updated_at" in columns


def test_cart_required_columns_are_not_nullable():
    columns = Cart.__table__.columns

    assert columns["user_id"].nullable is False
    assert columns["currency"].nullable is False
    assert columns["status"].nullable is False


def test_cart_default_values():
    columns = Cart.__table__.columns

    assert columns["currency"].default.arg == "PLN"
    assert columns["status"].default.arg == CartStatus.PENDING.name


def test_cart_can_be_created():
    cart = Cart(user_id=1, currency="EUR", status=CartStatus.COMPLETED.name)

    assert cart.user_id == 1
    assert cart.currency == "EUR"
    assert cart.status == CartStatus.COMPLETED.name
