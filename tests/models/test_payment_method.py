from app.models.payment_method import PaymentMethod


def test_payment_method_table_name():
    assert PaymentMethod.__tablename__ == "payment_methods"


def test_payment_method_has_expected_columns():
    columns = PaymentMethod.__table__.columns

    assert "name" in columns
    assert "price" in columns


def test_payment_method_required_columns_are_not_nullable():
    columns = PaymentMethod.__table__.columns

    assert columns["name"].nullable is False
    assert columns["price"].nullable is False


def test_payment_method_can_be_created():
    payment_method = PaymentMethod(
        name="Karta",
        price=2.5,
    )

    assert payment_method.name == "Karta"
    assert payment_method.price == 2.5
