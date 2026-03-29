from app.models.order import Order, OrderStatus


def test_order_table_name():
    assert Order.__tablename__ == "orders"


def test_order_has_expected_columns():
    columns = Order.__table__.columns

    assert "order_id" in columns
    assert "user_id" in columns
    assert "currency" in columns
    assert "status" in columns
    assert "total_price" in columns
    assert "payment_method_id" in columns


def test_order_required_columns_are_not_nullable():
    columns = Order.__table__.columns

    assert columns["order_id"].nullable is False
    assert columns["user_id"].nullable is False
    assert columns["currency"].nullable is False
    assert columns["status"].nullable is False
    assert columns["total_price"].nullable is False
    assert columns["payment_method_id"].nullable is False


def test_order_default_values():
    columns = Order.__table__.columns

    assert columns["currency"].default.arg == "PLN"
    assert columns["status"].default.arg == OrderStatus.PENDING.name
    assert columns["total_price"].default.arg == 0


def test_order_can_be_created():
    order = Order(
        order_id="ORD12345678",
        user_id=1,
        payment_method_id=2,
        currency="PLN",
        status="PENDING",
        total_price=5.5,
    )

    assert order.order_id == "ORD12345678"
    assert order.user_id == 1
    assert order.payment_method_id == 2
    assert order.currency == "PLN"
    assert order.status == OrderStatus.PENDING.name
    assert order.total_price == 5.5
