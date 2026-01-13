"""
Production deployment configuration for the Multi-User Todo Application API with Better Auth
"""
import os
from uvicorn import Config, Server
from main import app  # Updated import path

# Production server configuration
class ProductionConfig:
    # Server settings
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    workers = int(os.getenv("WORKERS", 4))

    # Logging settings
    log_level = os.getenv("LOG_LEVEL", "info")
    access_log = True

    # SSL settings (recommended for production with Better Auth HTTP-only cookies)
    ssl_keyfile = os.getenv("SSL_KEYFILE", None)
    ssl_certfile = os.getenv("SSL_CERTFILE", None)

    # Worker class
    worker_class = "uvicorn.workers.UvicornWorker"  # For use with gunicorn

def run_production_server():
    """
    Run the production server with optimized settings for Better Auth database session validation
    """
    config = ProductionConfig()

    server_config = Config(
        app=app,
        host=config.host,
        port=config.port,
        workers=config.workers,
        log_level=config.log_level,
        access_log=config.access_log,
        ssl_keyfile=config.ssl_keyfile,
        ssl_certfile=config.ssl_certfile,
    )

    server = Server(server_config)
    server.run()

if __name__ == "__main__":
    print("Starting production server with Better Auth database session validation...")
    run_production_server()