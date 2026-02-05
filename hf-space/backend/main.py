import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
import sys
from logging.handlers import RotatingFileHandler
from utils.websocket_manager import sio_app
import httpx

# Note: Better Auth is implemented using database session validation approach
# No external library import needed - custom implementation handles auth

# Import routers
from api.task_router import router as task_router
from api.auth_router import router as auth_router
from api.dashboard_router import router as dashboard_router
from api.chat_router import chat_router

# Import middleware and exception handlers
from middleware.rate_limiter import add_rate_limiting
from exceptions.handlers import add_exception_handlers

# Import database setup
from database.migrations import create_db_and_tables

# Configure comprehensive logging
def setup_logging():
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
    )

    # Create logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler with rotation
    file_handler = RotatingFileHandler(
        'app.log',
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger

logger = setup_logging()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan event handler for FastAPI application.
    This runs startup and shutdown events.
    """
    # Startup
    logger.info("Starting up the application...")
    # Initialize Better Auth
    logger.info("Initializing Better Auth server...")
    # Create database tables
    await create_db_and_tables()
    yield
    # Shutdown
    logger.info("Shutting down the application...")
    # Add any shutdown logic here

# Create FastAPI app with lifespan
app = FastAPI(
    title="Todo App Backend API",
    description="Backend CRUD API for Todo App with authentication and task management",
    version="1.0.0",
    lifespan=lifespan
)

# Dynamic CORS origins
allowed_origins = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:3000,http://localhost:3001,http://127.0.0.1:3000,http://127.0.0.1:3001"
).split(",")

# Add CORSMiddleware FIRST to ensure CORS headers are applied even if other middleware fails
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,  # Dynamic!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Access-Control-Allow-Origin", "Set-Cookie"],  # Expose headers to allow cookies
)

# Add ProxyHeadersMiddleware for handling forwarded headers (if behind proxy)
# from starlette.middleware.proxy_headers import ProxyHeadersMiddleware
# app.add_middleware(ProxyHeadersMiddleware, trusted_hosts="*")

# Add security headers (commented out as it interferes with CORS)
# secure_headers = Secure()
# 
# @app.middleware("http")
# async def add_secure_headers(request, call_next):
#     response = await call_next(request)
#     secure_headers.set_headers(response)
#     return response

# Add rate limiting - TEMPORARILY DISABLED FOR DEBUGGING
# Uncomment after verifying delete operations work
# try:
#     add_rate_limiting(app)
#     logger.info("Rate limiting enabled successfully")
# except Exception as e:
#     logger.warning(f"Rate limiting could not be enabled: {str(e)}")

# Add exception handlers
from exceptions.handlers import add_exception_handlers
add_exception_handlers(app)

# Include routers
app.include_router(task_router, prefix="/api/tasks", tags=["Tasks"])
app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])
app.include_router(dashboard_router, prefix="/api", tags=["Dashboard"])
app.include_router(chat_router, prefix="/api", tags=["Chat"])

# Log all registered routes for debugging
for route in app.routes:
    if hasattr(route, 'path'):
        logger.info(f'Route registered: {route.path}')

# Initialize Better Auth configuration
logger.info("Better Auth server initialized successfully")


# Mount Socket.IO app
from fastapi.staticfiles import StaticFiles
app.mount("/ws", sio_app)

# Health check endpoint with database connectivity test
@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint that verifies both API and database connectivity.
    Returns detailed status information for debugging.
    """
    from database.connection import engine
    from sqlalchemy import text
    
    health_status = {
        "status": "healthy",
        "api": "running",
        "message": "Todo App Backend API is running"
    }
    
    # Test database connectivity
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        health_status["database"] = "connected"
    except Exception as e:
        health_status["status"] = "degraded"
        health_status["database"] = f"connection failed: {str(e)}"
        logger.error(f"Database health check failed: {str(e)}")
    
    return health_status

# Root endpoint
@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to the Todo App Backend API"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)