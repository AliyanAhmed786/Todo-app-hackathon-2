from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlmodel.ext.asyncio.session import AsyncSession
from datetime import timedelta, datetime
import logging
from services.user_service import create_user, authenticate_user
from models.user import UserCreate, UserLogin, User
from models.session import SessionCreate, Session
from database.session import get_db_session
from schemas.user import UserCreateRequest, UserLoginRequest, AuthResponse
from exceptions.handlers import ValidationError
from config import settings
from middleware.rate_limiter import limiter
import secrets
from fastapi.responses import JSONResponse

# Create logger
logger = logging.getLogger(__name__)

# Create router
router = APIRouter()

@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def register_user(
    request: Request,
    user_in: UserCreateRequest,
    db: AsyncSession = Depends(get_db_session)
):
    """
    Register a new user with Better Auth database session validation.
    """
    try:
        # Validate the request data
        validated_user = UserCreate.model_validate(user_in.model_dump())

        # Create the user using the registration service
        from services.registration_service import register_user as service_register_user
        user = await service_register_user(db_session=db, user_in=validated_user)

        # Create a session in the database for Better Auth database validation
        session_expires = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)

        # Generate a random session token
        session_token = secrets.token_urlsafe(32)

        # Create session record
        session_data = SessionCreate(
            id=secrets.token_hex(16),  # Generate a unique session ID
            token=session_token,
            user_id=user.id,
            expires_at=session_expires
        )

        # Create session in database
        session = Session(**session_data.model_dump())
        db.add(session)
        await db.commit()
        await db.refresh(session)

        # Log successful registration
        logger.info(f"User registered successfully with ID: {user.id}, email: {user.email}")

        # Create JWT tokens
        from utils.auth import create_access_token, create_refresh_token
        access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
        refresh_token_expires = timedelta(days=settings.refresh_token_expire_days)

        access_token_data = {"sub": str(user.id)}
        refresh_token_data = {"sub": str(user.id)}

        access_token = create_access_token(data=access_token_data, expires_delta=access_token_expires)
        refresh_token = create_refresh_token(data=refresh_token_data, expires_delta=refresh_token_expires)

        # Create response with session token in HTTP-only cookie and JWT tokens
        response = JSONResponse(content={
            "user": {
                "id": user.id,
                "email": user.email,
                "name": user.name
            },
            "session": {
                "expires_at": session_expires.isoformat()
            },
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        })

        # Set session token as HTTP-only cookie for Better Auth database validation
        response.set_cookie(
            key="better-auth.session_token",
            value=session_token,
            httponly=True,
            secure=False,  # Set to False for local HTTP development
            samesite='lax',  # Use 'lax' for CSRF protection but allows cross-site requests
            max_age=int(timedelta(minutes=settings.access_token_expire_minutes).total_seconds()),  # Match session expiration
            path="/"  # Make cookie available for all routes
        )

        return response
    except ValueError as e:
        logger.warning(f"User registration failed due to validation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Validation error: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Unexpected error during user registration: {str(e)}", exc_info=True)

        # Handle specific database constraint errors
        error_msg = str(e)
        if "UNIQUE constraint failed" in error_msg or "duplicate key value violates unique constraint" in error_msg:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A user with this email already exists"
            )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating user: {str(e)}"
        )

@router.post("/login", response_model=AuthResponse)
async def login_user(
    request: Request,
    user_credentials: UserLoginRequest,
    db: AsyncSession = Depends(get_db_session)
):
    """
    Login an existing user with Better Auth database session validation.
    """
    try:
        # Validate the request data
        validated_credentials = UserLogin.model_validate(user_credentials.model_dump())

        # Log login attempt
        logger.info(f"Login attempt for email: {validated_credentials.email}")

        # Login the user using the login service
        from services.login_service import login_user
        user, session = await login_user(
            db_session=db,
            email=validated_credentials.email,
            password=validated_credentials.password
        )

        if not user or not session:
            logger.warning(f"Failed login attempt for email: {validated_credentials.email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Log successful login
        logger.info(f"User logged in successfully with ID: {user.id}, email: {user.email}")

        # Create JWT tokens
        from utils.auth import create_access_token, create_refresh_token
        access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
        refresh_token_expires = timedelta(days=settings.refresh_token_expire_days)

        access_token_data = {"sub": str(user.id)}
        refresh_token_data = {"sub": str(user.id)}

        access_token = create_access_token(data=access_token_data, expires_delta=access_token_expires)
        refresh_token = create_refresh_token(data=refresh_token_data, expires_delta=refresh_token_expires)

        # Create response with session token in HTTP-only cookie and JWT tokens
        response = JSONResponse(content={
            "user": {
                "id": user.id,
                "email": user.email,
                "name": user.name
            },
            "session": {
                "expires_at": session.expires_at.isoformat()
            },
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        })

        # Set session token as HTTP-only cookie for Better Auth database validation
        response.set_cookie(
            key="better-auth.session_token",
            value=session.token,
            httponly=True,
            secure=False,  # Set to False for local HTTP development
            samesite='lax',  # Use 'lax' for CSRF protection but allows cross-site requests
            max_age=int((session.expires_at - datetime.utcnow()).total_seconds()),  # Match session expiration
            path="/"  # Make cookie available for all routes
        )

        return response
    except ValueError as e:
        logger.warning(f"Login failed due to validation error: {str(e)}")
        raise ValidationError(str(e))
    except HTTPException as e:
        # Log authentication failures
        if e.status_code == 401:
            logger.warning(f"Authentication failed for email: {user_credentials.email}")
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Unexpected error during login: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error during login: {str(e)}"
        )

@router.post("/logout")
async def logout_user(
    request: Request,
    db: AsyncSession = Depends(get_db_session)
):
    """
    Logout the current user with Better Auth database session validation.
    Clears the authentication cookies and removes the session from the database.
    """
    # Get session token from cookie
    session_token = request.cookies.get("better-auth.session_token")

    if session_token:
        try:
            from services.logout_service import logout_user as service_logout_user
            result = await service_logout_user(
                db_session=db,
                session_token=session_token
            )

            if not result["success"]:
                logger.warning(f"Logout failed for token: {session_token[:20]}... - {result['message']}")
                # We still continue with clearing cookies even if DB operation failed
        except Exception as e:
            logger.error(f"Error during logout process: {str(e)}")
            # Continue with clearing cookies even if there was an error

    # Create response with success message
    response = JSONResponse(content={
        "message": "Logged out successfully",
        "status": "success"
    })

    # Clear Better Auth authentication cookies
    response.delete_cookie(key="better-auth.session_token", path="/")
    response.delete_cookie(key="access_token", path="/")
    response.delete_cookie(key="refresh_token", path="/")

    return response



@router.post("/refresh")
async def refresh_token(request: Request, response: JSONResponse):
    """
    Refresh the authentication token using Better Auth database session validation.
    """
    # Get session token from cookie
    session_token = request.cookies.get("better-auth.session_token")

    if not session_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No session token provided",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Validate the existing session
    from middleware.better_auth import validate_session_from_database
    user_id = await validate_session_from_database(request)

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired session",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Get user details
    from database.connection import engine
    async with AsyncSession(engine) as db:
        from sqlmodel import select
        from models.user import User
        result = await db.exec(select(User).where(User.id == user_id))
        user = result.first()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Refresh the session using the session service
        from services.session_service import refresh_session
        from config import settings

        refreshed_session = await refresh_session(
            db_session=db,
            session_token=session_token,
            expires_in_minutes=settings.access_token_expire_minutes
        )

        if not refreshed_session:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Failed to refresh session",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Set new session token as HTTP-only cookie
        response.set_cookie(
            key="better-auth.session_token",
            value=refreshed_session.token,
            httponly=True,
            secure=False,  # Set to False for local HTTP development
            samesite='lax',  # Use 'lax' for CSRF protection but allows cross-site requests
            max_age=int((refreshed_session.expires_at - datetime.utcnow()).total_seconds()),  # Match session expiration
            path="/"  # Make cookie available for all routes
        )

        # Return user data
        return {
            "user": {
                "id": user.id,
                "email": user.email,
                "name": user.name
            },
            "session": {
                "expires_at": refreshed_session.expires_at.isoformat()
            }
        }


@router.get("/session")
async def get_session(request: Request):
    """
    Get the current user session using Better Auth database session validation.
    Supports both session cookies and JWT tokens.
    """
    try:
        # First, try to get session token from Better Auth HTTP-only cookie
        session_token = request.cookies.get("better-auth.session_token")

        # Also check for JWT token in Authorization header
        auth_header = request.headers.get('Authorization')
        jwt_token = None
        if auth_header and auth_header.startswith('Bearer '):
            jwt_token = auth_header[len('Bearer '):].strip()

        user_id = None

        if session_token:
            # Validate session by querying the Better Auth session table in the database
            from middleware.better_auth import validate_session_from_database
            user_id = await validate_session_from_database(request)
        elif jwt_token:
            # Validate JWT token
            from utils.auth import verify_access_token
            payload = verify_access_token(jwt_token)
            if payload:
                user_id = payload.get("sub")

        if not user_id:
            # No valid session or JWT token, return empty session
            logger.info("Session check - no valid session token or JWT provided")
            return {"user": None}

        # Log successful session validation
        logger.info(f"Session validated successfully for user: {user_id}")

        # Get user details from database using the user ID from session
        from sqlmodel import select
        from models.user import User
        from database.connection import engine
        async with AsyncSession(engine) as db:
            result = await db.exec(select(User).where(User.id == user_id))
            user = result.first()
            if not user:
                logger.warning(f"Session valid but user not found: {user_id}")
                return {"user": None}

            # Log successful session retrieval
            logger.info(f"Session retrieved successfully for user: {user.id} ({user.email})")

            # Return user data in Better Auth format
            return {
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "name": user.name,
                    "email_verified": user.email_verified
                },
                "token": jwt_token if jwt_token else session_token
            }
    except Exception as e:
        # If there's an error (e.g., invalid session), return empty session
        logger.error(f"Error getting session: {str(e)}", exc_info=True)
        return {"user": None}

