import pytest

from app.models.user import User, Address
from app.repositories.user_repository import UserRepository
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
def clean_user_table(db_session):
    # Given
    db_session.query(User).delete()
    db_session.commit()

    yield

    db_session.query(User).delete()
    db_session.commit()


@pytest.fixture
def clean_address_table(db_session):
    # Given
    db_session.query(Address).delete()
    db_session.commit()

    yield

    db_session.query(Address).delete()
    db_session.commit()


@pytest.fixture
def seeded_addresses(db_session, clean_address_table):
    # Given
    addresses = [
        Address(
            address_line_1="Street 1",
            city="Warszawa",
            postal_code="00-001",
            country_code="PL",
            state_province="Mazowieckie",
        ),
        Address(
            address_line_1="Street 2",
            city="Kraków",
            postal_code="30-001",
            country_code="PL",
            state_province="Małopolskie",
        ),
        Address(
            address_line_1="Street 3",
            city="Gdańsk",
            postal_code="80-001",
            country_code="PL",
            state_province="Pomorskie",
        ),
    ]

    for address in addresses:
        db_session.add(address)
    db_session.commit()

    return addresses


@pytest.fixture
def seeded_users(db_session, clean_user_table, seeded_addresses):
    # Given
    users = [
        User(username="john", email="john@example.com", name="John", surname="Doe", hashed_password="hash1", role_id=1, address_id=seeded_addresses[0].id),
        User(username="anna", email="anna@example.com", name="Anna", surname="Nowak", hashed_password="hash2", role_id=1, address_id=seeded_addresses[1].id),
        User(username="piotr", email="piotr@example.com", name="Piotr", surname="Kowalski", hashed_password="hash3", role_id=1, address_id=seeded_addresses[2].id),
    ]

    for user in users:
        db_session.add(user)
    db_session.commit()

    return users


def test_get_all_users(db_session, seeded_users):
    # Given
    repo = UserRepository(db_session)

    # When
    result = repo.get_all_users()

    # Then
    assert len(result) == 3


def test_get_user_by_id(db_session, seeded_users):
    # Given
    repo = UserRepository(db_session)
    user_id = seeded_users[0].id

    # When
    result = repo.get_user_by_id(user_id)

    # Then
    assert result is not None
    assert result.username == "john"


def test_get_users_paginated(db_session, seeded_users):
    # Given
    repo = UserRepository(db_session)

    # When
    items, total = repo.get_users_paginated(page=1, size=2)

    # Then
    assert total == 3
    assert len(items) == 2


def test_find_user_by_username(db_session, seeded_users):
    # Given
    repo = UserRepository(db_session)

    # When
    result = repo.find_user_by_username("anna")

    # Then
    assert result is not None
    assert result.email == "anna@example.com"
