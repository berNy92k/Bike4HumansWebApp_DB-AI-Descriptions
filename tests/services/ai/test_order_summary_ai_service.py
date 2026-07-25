import os
from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock, patch

import pytest
from fastapi import HTTPException
from openai import OpenAIError

from app.models.bike import Bike
from app.models.order import Order, OrderItem, OrderStatus
from app.services.ai.order_summary_ai_service import OrderSummaryAiService


def _make_order(**overrides):
    bike = Bike(id=1, name="Trek Marlin 7", price=100.0, stock_quantity=5, created_by=1, brand_id=1)
    item = OrderItem(bike_id=1, quantity=2)
    item.bike = bike

    defaults = dict(
        order_id="ORD00000001",
        user_id=1,
        currency="PLN",
        status=OrderStatus.PENDING.name,
        total_price=200.0,
        payment_method_id=1,
        updated_at=datetime.now(timezone.utc).replace(tzinfo=None) - timedelta(days=2),
    )
    defaults.update(overrides)
    order = Order(**defaults)
    order.items = [item]
    return order


def test_generate_summary_returns_trimmed_ai_content():
    # Given
    with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
        service = OrderSummaryAiService()

    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value.choices = [
        MagicMock(message=MagicMock(content="  Zamówienie zawiera 2x Trek Marlin 7.  "))
    ]

    with patch("app.services.ai.order_summary_ai_service.OpenAI", return_value=mock_client):
        # When
        result = service.generate_summary(_make_order())

    # Then
    assert result == "Zamówienie zawiera 2x Trek Marlin 7."


def test_generate_summary_missing_api_key_raises_500():
    # Given
    with patch.dict(os.environ, {}, clear=False):
        os.environ.pop("OPENAI_API_KEY", None)
        service = OrderSummaryAiService()

        # When / Then
        with pytest.raises(HTTPException) as exc:
            service.generate_summary(_make_order())

    assert exc.value.status_code == 500


def test_generate_summary_provider_error_raises_502():
    # Given
    with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
        service = OrderSummaryAiService()

    mock_client = MagicMock()
    mock_client.chat.completions.create.side_effect = OpenAIError("boom")

    with patch("app.services.ai.order_summary_ai_service.OpenAI", return_value=mock_client):
        # When / Then
        with pytest.raises(HTTPException) as exc:
            service.generate_summary(_make_order())

    assert exc.value.status_code == 502


def test_generate_summary_empty_ai_content_raises_502():
    # Given
    with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
        service = OrderSummaryAiService()

    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value.choices = [MagicMock(message=MagicMock(content=None))]

    with patch("app.services.ai.order_summary_ai_service.OpenAI", return_value=mock_client):
        # When / Then
        with pytest.raises(HTTPException) as exc:
            service.generate_summary(_make_order())

    assert exc.value.status_code == 502


def test_build_user_prompt_includes_order_and_item_data():
    # Given
    order = _make_order()

    # When
    prompt = OrderSummaryAiService._build_user_prompt(order)

    # Then
    assert "ORD00000001" in prompt
    assert "PENDING" in prompt
    assert "200.0 PLN" in prompt
    assert "2x Trek Marlin 7" in prompt
