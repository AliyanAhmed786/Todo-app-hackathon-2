"""
Registration service for Better Auth database session validation.
This service handles user registration using the Better Auth database validation approach.
"""

from sqlmodel.ext.asyncio.session import AsyncSession
from models.user import User, UserCreate
from sqlmodel import select
from passlib.context import CryptContext
from typing import Optional
import logging

# Create logger
logger = logging.getLogger(__name__)

# Initialize password hasher
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Generate a hash for a plain password.
    """
    return pwd_context.hash(password)


async def register_user(*, db_session: AsyncSession, user_in: UserCreate) -> User:
    """
    Register a new user with Better Auth database session validation approach.

    Args:
        db_session: The database session to use for the operation
        user_in: The user creation data

    Returns:
        User: The created user object

    Raises:
        ValueError: If the email is already taken
    """
    # Check if user with this email already exists
    result = await db_session.exec(
        select(User).where(User.email == user_in.email.lower())
    )
    user_exists = result.first()

    if user_exists:
        logger.warning(f"Registration attempted with existing email: {user_in.email}")
        raise ValueError("A user with this email already exists")

    # Hash the password
    password_hash = get_password_hash(user_in.password)

    # Create user object with string ID (for Better Auth compatibility)
    import secrets
    user_id = secrets.token_hex(20)  # Generate a unique string ID for Better Auth

    user = User(
        id=user_id,
        name=user_in.name,
        email=user_in.email.lower(),
        password_hash=password_hash,
        email_verified=False
    )

    # Add user to database
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    logger.info(f"Successfully registered new user with ID: {user.id}, email: {user.email}")
    return user


async def get_user_by_email(*, db_session: AsyncSession, email: str) -> Optional[User]:
    """
    Retrieve a user by their email address.

    Args:
        db_session: The database session to use for the operation
        email: The email address to search for

    Returns:
        User: The user object if found, None otherwise
    """
    result = await db_session.exec(
        select(User).where(User.email == email.lower())
    )
    user = result.first()

    if user:
        logger.info(f"Found user by email: {email}")
    else:
        logger.info(f"No user found for email: {email}")

    return user