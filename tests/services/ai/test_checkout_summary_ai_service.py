import os
from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock, patch

import pytest
from fastapi import HTTPException
from openai import OpenAIError

from app.models.bike import Bike
from app.models.checkout import Checkout, CheckoutItem
from app.services.ai.checkout_summary_ai_service import CheckoutSummaryAiService


def _make_checkout(**overrides):
    bike = Bike(id=1, name="Trek Marlin 7", price=100.0, stock_quantity=5, created_by=1, brand_id=1)
    item = CheckoutItem(bike_id=1, quantity=2)
    item.bike = bike

    defaults = dict(
        user_id=1,
        currency="PLN",
        status="PENDING",
        total_price=200.0,
        payment_method_id=1,
        updated_at=datetime.now(timezone.utc).replace(tzinfo=None) - timedelta(days=2),
    )
    defaults.update(overrides)
    checkout = Checkout(**defaults)
    checkout.items = [item]
    return checkout


def test_generate_summary_returns_trimmed_ai_content():
    # Given
    with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
        service = CheckoutSummaryAiService()

    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value.choices = [
        MagicMock(message=MagicMock(content="  Checkout obejmuje 2x Trek Marlin 7.  "))
    ]

    with patch("app.services.ai.checkout_summary_ai_service.OpenAI", return_value=mock_client):
        # When
        result = service.generate_summary(_make_checkout())

    # Then
    assert result == "Checkout obejmuje 2x Trek Marlin 7."


def test_generate_summary_missing_api_key_raises_500():
    # Given
    with patch.dict(os.environ, {}, clear=False):
        os.environ.pop("OPENAI_API_KEY", None)
        service = CheckoutSummaryAiService()

        # When / Then
        with pytest.raises(HTTPException) as exc:
            service.generate_summary(_make_checkout())

    assert exc.value.status_code == 500


def test_generate_summary_provider_error_raises_502():
    # Given
    with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
        service = CheckoutSummaryAiService()

    mock_client = MagicMock()
    mock_client.chat.completions.create.side_effect = OpenAIError("boom")

    with patch("app.services.ai.checkout_summary_ai_service.OpenAI", return_value=mock_client):
        # When / Then
        with pytest.raises(HTTPException) as exc:
            service.generate_summary(_make_checkout())

    assert exc.value.status_code == 502


def test_build_user_prompt_includes_checkout_and_item_data():
    # Given
    checkout = _make_checkout()

    # When
    prompt = CheckoutSummaryAiService._build_user_prompt(checkout)

    # Then
    assert "PENDING" in prompt
    assert "200.0 PLN" in prompt
    assert "2x Trek Marlin 7" in prompt
