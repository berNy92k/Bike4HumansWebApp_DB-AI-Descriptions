import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    return TestClient(app)


def test_render_login_page(client):
    # Given

    # When
    response = client.get("/auth/login")

    # Then
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_render_register_page(client):
    # Given

    # When
    response = client.get("/auth/register")

    # Then
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
