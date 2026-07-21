import os
from unittest.mock import MagicMock, patch

import pytest
from fastapi import HTTPException
from openai import OpenAIError

from app.schemas.admin.bike.admin_bike_auto_tag_request_dto import BikeAutoTagRequestDto
from app.schemas.admin.bike.admin_bike_auto_tag_response_dto import BikeAutoTagResponseDto
from app.services.ai.bike_auto_tag_ai_service import BikeAutoTagAiService


def _make_request_dto(**overrides):
    defaults = dict(name="Trek Marlin 7", description="Lekki rower górski z aluminiową ramą.")
    defaults.update(overrides)
    return BikeAutoTagRequestDto(**defaults)


def test_generate_tags_returns_parsed_response():
    # Given
    with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
        service = BikeAutoTagAiService()

    parsed = BikeAutoTagResponseDto(bike_type="MOUNTAIN", frame_material="ALUMINIUM")
    mock_client = MagicMock()
    mock_client.chat.completions.parse.return_value.choices = [MagicMock(message=MagicMock(parsed=parsed))]

    with patch("app.services.ai.bike_auto_tag_ai_service.OpenAI", return_value=mock_client):
        # When
        result = service.generate_tags(_make_request_dto())

    # Then
    assert result.bike_type == "MOUNTAIN"
    assert result.frame_material == "ALUMINIUM"
    assert result.color is None


def test_generate_tags_missing_api_key_raises_500():
    # Given
    with patch.dict(os.environ, {}, clear=False):
        os.environ.pop("OPENAI_API_KEY", None)
        service = BikeAutoTagAiService()

        # When / Then
        with pytest.raises(HTTPException) as exc:
            service.generate_tags(_make_request_dto())

    assert exc.value.status_code == 500


def test_generate_tags_provider_error_raises_502():
    # Given
    with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
        service = BikeAutoTagAiService()

    mock_client = MagicMock()
    mock_client.chat.completions.parse.side_effect = OpenAIError("boom")

    with patch("app.services.ai.bike_auto_tag_ai_service.OpenAI", return_value=mock_client):
        # When / Then
        with pytest.raises(HTTPException) as exc:
            service.generate_tags(_make_request_dto())

    assert exc.value.status_code == 502


def test_generate_tags_unparsable_response_raises_502():
    # Given
    with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
        service = BikeAutoTagAiService()

    mock_client = MagicMock()
    mock_client.chat.completions.parse.return_value.choices = [MagicMock(message=MagicMock(parsed=None))]

    with patch("app.services.ai.bike_auto_tag_ai_service.OpenAI", return_value=mock_client):
        # When / Then
        with pytest.raises(HTTPException) as exc:
            service.generate_tags(_make_request_dto())

    assert exc.value.status_code == 502
