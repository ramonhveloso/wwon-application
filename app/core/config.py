import os


class Settings:
    PROJECT_NAME: str = "ERP Project Backend"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./test.db")


settings = Settings()
