"""
Better Auth server-side configuration for the todo app backend.
"""
from better_auth import auth
from config import settings

# Initialize Better Auth with configuration
better_auth = auth(
    secret=settings.secret_key,  # Use the same secret key from settings
    algorithm=settings.algorithm,
    # Add other configuration options as needed
    # This is a simplified version - actual Better Auth setup may vary
)

# Export the auth instance
auth_instance = better_auth