from app.models.checkout import Checkout, CheckoutStatus


def test_checkout_table_name():
    assert Checkout.__tablename__ == "checkouts"


def test_checkout_has_expected_columns():
    columns = Checkout.__table__.columns

    assert "user_id" in columns
    assert "currency" in columns
    assert "status" in columns
    assert "total_price" in columns
    assert "payment_method_id" in columns


def test_checkout_required_columns_are_not_nullable():
    columns = Checkout.__table__.columns

    assert columns["user_id"].nullable is False
    assert columns["currency"].nullable is False
    assert columns["status"].nullable is False
    assert columns["total_price"].nullable is False
    assert columns["payment_method_id"].nullable is False


def test_checkout_default_values():
    columns = Checkout.__table__.columns

    assert columns["currency"].default.arg == "PLN"
    assert columns["status"].default.arg == "PENDING"
    assert columns["total_price"].default.arg == 0


def test_checkout_can_be_created():
    checkout = Checkout(
        user_id=1,
        payment_method_id=2,
        currency="PLN",
        status="PENDING",
        total_price=5.5,
    )

    assert checkout.user_id == 1
    assert checkout.payment_method_id == 2
    assert checkout.currency == "PLN"
    assert checkout.status == "PENDING"
    assert checkout.total_price == 5.5
