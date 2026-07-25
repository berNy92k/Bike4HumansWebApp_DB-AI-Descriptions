import os
from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock, patch

import pytest
from fastapi import HTTPException
from openai import OpenAIError

from app.models.bike import Bike
from app.models.cart import Cart, CartItem
from app.services.ai.cart_summary_ai_service import CartSummaryAiService


def _make_cart(**overrides):
    bike = Bike(id=1, name="Trek Marlin 7", price=100.0, stock_quantity=5, created_by=1, brand_id=1)
    item = CartItem(bike_id=1, quantity=3)
    item.bike = bike

    defaults = dict(
        user_id=1,
        currency="PLN",
        status="PENDING",
        updated_at=datetime.now(timezone.utc).replace(tzinfo=None) - timedelta(days=10),
    )
    defaults.update(overrides)
    cart = Cart(**defaults)
    cart.items = [item]
    return cart


def test_generate_summary_returns_trimmed_ai_content():
    # Given
    with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
        service = CartSummaryAiService()

    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value.choices = [
        MagicMock(message=MagicMock(content="  Koszyk może być porzucony.  "))
    ]

    with patch("app.services.ai.cart_summary_ai_service.OpenAI", return_value=mock_client):
        # When
        result = service.generate_summary(_make_cart())

    # Then
    assert result == "Koszyk może być porzucony."


def test_generate_summary_missing_api_key_raises_500():
    # Given
    with patch.dict(os.environ, {}, clear=False):
        os.environ.pop("OPENAI_API_KEY", None)
        service = CartSummaryAiService()

        # When / Then
        with pytest.raises(HTTPException) as exc:
            service.generate_summary(_make_cart())

    assert exc.value.status_code == 500


def test_generate_summary_provider_error_raises_502():
    # Given
    with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
        service = CartSummaryAiService()

    mock_client = MagicMock()
    mock_client.chat.completions.create.side_effect = OpenAIError("boom")

    with patch("app.services.ai.cart_summary_ai_service.OpenAI", return_value=mock_client):
        # When / Then
        with pytest.raises(HTTPException) as exc:
            service.generate_summary(_make_cart())

    assert exc.value.status_code == 502


def test_build_user_prompt_computes_total_from_items():
    # Given
    cart = _make_cart()

    # When
    prompt = CartSummaryAiService._build_user_prompt(cart)

    # Then
    assert "300.0 PLN" in prompt
    assert "3x Trek Marlin 7" in prompt
