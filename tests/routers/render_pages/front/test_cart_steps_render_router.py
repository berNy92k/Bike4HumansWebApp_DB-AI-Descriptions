from datetime import timedelta

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.models.bike import Bike
from app.models.cart import Cart, CartItem, CartStatus
from app.models.checkout import Checkout, CheckoutItem, CheckoutStatus
from app.models.payment_method import PaymentMethod
from app.models.permission import Permission, PermissionCode, role_permission
from app.models.role import Role
from app.models.user import User, Address
from app.services.auth.auth_service import generate_jwt_token
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
def client():
    return TestClient(app)


def _login(client: TestClient, user_id: int = 1, username: str = "john", role_id: int = 4) -> None:
    token = generate_jwt_token(username, user_id, role_id, timedelta(minutes=20))
    client.cookies.set("access_token", token)


@pytest.fixture
def clean_tables(db_session):
    # Given
    db_session.query(CheckoutItem).delete()
    db_session.query(Checkout).delete()
    db_session.query(CartItem).delete()
    db_session.query(Cart).delete()
    db_session.query(PaymentMethod).delete()
    db_session.query(Bike).delete()
    db_session.query(User).delete()
    db_session.query(Address).delete()
    db_session.execute(role_permission.delete())
    db_session.query(Permission).delete()
    db_session.query(Role).delete()
    db_session.commit()

    yield

    db_session.query(CheckoutItem).delete()
    db_session.query(Checkout).delete()
    db_session.query(CartItem).delete()
    db_session.query(Cart).delete()
    db_session.query(PaymentMethod).delete()
    db_session.query(Bike).delete()
    db_session.query(User).delete()
    db_session.query(Address).delete()
    db_session.execute(role_permission.delete())
    db_session.query(Permission).delete()
    db_session.query(Role).delete()
    db_session.commit()


@pytest.fixture
def seeded_user(db_session, clean_tables):
    # Given
    role = Role(id=4, name="user", description="User")
    address = Address(
        id=1,
        address_line_1="Street 1",
        city="Warszawa",
        postal_code="00-001",
        country_code="PL",
        state_province="Mazowieckie",
    )
    user = User(
        id=1,
        username="john",
        email="john@example.com",
        name="John",
        surname="Doe",
        hashed_password="hash",
        is_active=True,
        email_verified=True,
        role_id=4,
        address_id=1,
    )
    bike = Bike(name="Trek Marlin 7", price=1000.0, stock_quantity=5, created_by=1, brand_id=1)

    db_session.add(role)
    db_session.add(address)
    db_session.add(user)
    db_session.add(bike)
    db_session.commit()

    return user, bike


@pytest.fixture
def seeded_pending_cart(db_session, seeded_user):
    # Given
    user, bike = seeded_user

    cart = Cart(user_id=user.id, currency="PLN", status=CartStatus.PENDING.name)
    cart.items.append(CartItem(bike_id=bike.id, quantity=1))
    db_session.add(cart)
    db_session.commit()

    return cart


@pytest.fixture
def seeded_pending_checkout(db_session, seeded_user):
    # Given
    user, bike = seeded_user

    method = PaymentMethod(name="Karta", price=2.5)
    db_session.add(method)
    db_session.flush()

    checkout = Checkout(user_id=user.id, currency="PLN", status=CheckoutStatus.PENDING.name, total_price=1000.0,
                         payment_method_id=method.id)
    checkout.items.append(CheckoutItem(bike_id=bike.id, quantity=1))
    db_session.add(checkout)
    db_session.commit()

    return checkout, method


def test_render_cart_step1_authenticated(client, seeded_pending_cart):
    # Given
    _login(client)

    # When
    response = client.get("/cart/step1")

    # Then
    assert response.status_code == 200


def test_render_cart_step1_unauthenticated_redirects_to_login(client, seeded_pending_cart):
    # Given

    # When
    response = client.get("/cart/step1", follow_redirects=False)

    # Then
    assert response.status_code == 303
    assert response.headers["location"] == "/auth/login"


def test_render_cart_step1_without_pending_cart_redirects_to_login(client, seeded_user):
    # Given
    _login(client)

    # When
    response = client.get("/cart/step1", follow_redirects=False)

    # Then
    assert response.status_code == 303
    assert response.headers["location"] == "/auth/login"


def test_render_cart_step2_authenticated(client, seeded_pending_checkout):
    # Given
    _login(client)

    # When
    response = client.get("/cart/step2")

    # Then
    assert response.status_code == 200


def test_render_payment_provider_requires_completed_checkout(client, seeded_pending_checkout):
    # Given
    _login(client)

    # When / Then - checkout is only PENDING, not COMPLETED, so the page should reject access
    response = client.get("/cart/payment-provider", follow_redirects=False)

    assert response.status_code == 303
    assert response.headers["location"] == "/auth/login"
