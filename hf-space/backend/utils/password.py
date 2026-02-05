from passlib.context import CryptContext
from typing import Optional, Tuple

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password.
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    Generate a hash for the given password with 72-byte safety check.
    """
    if len(password.encode('utf-8')) > 72:
        raise ValueError("Password exceeds bcrypt 72-byte limit")
    return pwd_context.hash(password)

def verify_and_update_password(plain_password: str, hashed_password: str) -> Tuple[bool, Optional[str]]:
    """
    Verify a password and check if it needs to be rehashed with newer algorithm.
    Returns a tuple of (is_valid, new_hash_if_needed).
    """
    verified, new_hash = pwd_context.verify_and_update(plain_password, hashed_password)
    return verified, new_hash if new_hash else None