import os

class Settings:
    PROJECT_NAME: str = "My FastAPI Project"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./test.db")

settings = Settings()
