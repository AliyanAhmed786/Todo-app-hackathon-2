from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from models.user import User, UserCreate, UserLogin
from utils.password import verify_password, get_password_hash
from exceptions.handlers import UserNotFoundError, ValidationError
from typing import Optional
import secrets
import datetime


async def create_user(*, db_session: AsyncSession, user_in: UserCreate) -> User:
    """
    Create a new user. Truncates long passwords to 72 bytes for bcrypt compatibility.
    """
    # Check if user with this email already exists
    result = await db_session.exec(select(User).where(User.email == user_in.email.lower()))
    existing_user = result.first()
    if existing_user:
        raise ValidationError("A user with this email already exists")

    user_id = secrets.token_hex(20)

    # FIX: Truncate to 72 chars so bcrypt doesn't throw the 'AttributeError' or 'ValueTooLong'
    safe_password = user_in.password[:72]
    hashed_password = get_password_hash(safe_password)

    user = User(
        id=user_id,
        name=user_in.name,
        email=user_in.email.lower(),
        password_hash=hashed_password,
        email_verified=False
    )

    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


async def authenticate_user(*, db_session: AsyncSession, email: str, password: str) -> Optional[User]:
    """
    Authenticate a user. Truncates input to 72 bytes to match the hash.
    """
    result = await db_session.exec(select(User).where(User.email == email.lower()))
    user = result.first()

    if not user:
        return None

    # FIX: Do not return None if > 72. Truncate it instead!
    # This allows the long strings from your deployed frontend to work.
    is_valid = verify_password(password[:72], user.password_hash)

    if not is_valid:
        return None

    return user


async def get_user_by_email(*, db_session: AsyncSession, email: str) -> Optional[User]:
    """
    Get a user by their email address.
    """
    result = await db_session.exec(select(User).where(User.email == email.lower()))
    user = result.first()
    return user


async def get_user_by_id(*, db_session: AsyncSession, user_id: str) -> Optional[User]:
    """
    Get a user by their ID.
    """
    user = await db_session.get(User, user_id)
    return user


async def update_user(*, db_session: AsyncSession, user_id: str, user_in: dict) -> Optional[User]:
    """
    Update a user's information.
    """
    # Get the existing user
    user = await db_session.get(User, user_id)

    if not user:
        raise UserNotFoundError(user_id)

    # Update user information
    for field, value in user_in.items():
        if hasattr(user, field):
            setattr(user, field, value)

    # Update the updated_at timestamp
    user.updated_at = datetime.datetime.utcnow()

    # Commit changes
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    return user


async def delete_user(*, db_session: AsyncSession, user_id: str) -> bool:
    """
    Delete a user by their ID.
    Returns True if the user was deleted, False otherwise.
    """
    # Get the user
    user = await db_session.get(User, user_id)

    if not user:
        raise UserNotFoundError(user_id)

    # Delete the user
    await db_session.delete(user)
    await db_session.commit()

    return True