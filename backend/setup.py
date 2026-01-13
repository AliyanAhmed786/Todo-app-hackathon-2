from setuptools import setup, find_packages

setup(
    name="todo-backend",
    version="1.0.0",
    packages=find_packages(),
    package_dir={"": "src"},
    install_requires=[
        "fastapi==0.104.1",
        "uvicorn[standard]==0.24.0",
        "sqlmodel==0.0.16",
        "pydantic==2.5.0",
        "pydantic-settings==2.1.0",
        "passlib[bcrypt]==1.7.4",
        "python-jose[cryptography]==3.3.0",
        "python-multipart==0.0.6",
        "psycopg2-binary==2.9.9",
        "better-exceptions==0.3.3",
        "python-dotenv==1.0.0",
        "pytest==7.4.3",
        "httpx==0.25.2",
    ],
    python_requires=">=3.7",
)