import time
from collections import defaultdict, deque

from fastapi import HTTPException, Request
from starlette import status


class InMemoryRateLimiter:

    def __init__(self, max_requests: int, window_seconds: int):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._hits: dict[str, deque] = defaultdict(deque)

    def check(self, key: str) -> None:
        now = time.monotonic()
        hits = self._hits[key]

        while hits and now - hits[0] > self.window_seconds:
            hits.popleft()

        if len(hits) >= self.max_requests:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Zbyt wiele żądań do funkcji AI. Spróbuj ponownie za chwilę.",
            )

        hits.append(now)


def rate_limit_dependency(limiter: InMemoryRateLimiter):
    def dependency(request: Request) -> None:
        client_ip = request.client.host if request.client else "unknown"
        limiter.check(client_ip)

    return dependency
