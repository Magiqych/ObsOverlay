import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "FastAPI Project"
    BACKEND_CORS_ORIGINS: list = ["http://localhost:3000"]

settings = Settings()