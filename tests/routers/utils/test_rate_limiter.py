import pytest
from fastapi import HTTPException

from app.routers.utils.rate_limiter import InMemoryRateLimiter


def test_allows_requests_within_limit():
    # Given
    limiter = InMemoryRateLimiter(max_requests=3, window_seconds=60)

    # When / Then
    limiter.check("1.2.3.4")
    limiter.check("1.2.3.4")
    limiter.check("1.2.3.4")


def test_blocks_requests_over_limit():
    # Given
    limiter = InMemoryRateLimiter(max_requests=2, window_seconds=60)
    limiter.check("1.2.3.4")
    limiter.check("1.2.3.4")

    # When / Then
    with pytest.raises(HTTPException) as exc:
        limiter.check("1.2.3.4")

    assert exc.value.status_code == 429


def test_tracks_keys_independently():
    # Given
    limiter = InMemoryRateLimiter(max_requests=1, window_seconds=60)
    limiter.check("1.2.3.4")

    # When / Then
    limiter.check("5.6.7.8")

    with pytest.raises(HTTPException):
        limiter.check("1.2.3.4")


def test_allows_requests_again_after_window_expires():
    # Given
    limiter = InMemoryRateLimiter(max_requests=1, window_seconds=60)
    limiter.check("1.2.3.4")

    with pytest.raises(HTTPException):
        limiter.check("1.2.3.4")

    # When - simulate the window having elapsed
    limiter._hits["1.2.3.4"][0] -= 61

    # Then
    limiter.check("1.2.3.4")
