from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import FastAPI, Request, Depends
from config import settings

# Create a limiter instance
limiter = Limiter(
    key_func=get_remote_address,  # Use IP address as the key
    default_limits=[f"{settings.rate_limit_requests}/minute"]  # Default rate limit
)

def add_rate_limiting(app: FastAPI):
    """
    Add rate limiting to the FastAPI application.
    """
    # Add the limiter to the app
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

def get_user_rate_limit(user_id: str) -> str:
    """
    Get a rate limit specific to a user.
    This allows for per-user rate limiting instead of just per-IP.
    """
    return f"{settings.rate_limit_requests}/minute"

# Example of how to use per-user rate limiting in a route:
# @limiter.limit(get_user_rate_limit)
# async def some_route(request: Request):
#     pass