from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Google Trends Microservice"
    DEBUG_MODE: bool = False
    DATABASE_URL: str = "sqlite:///./test.db"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "your-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    API_KEY: str = "your-api-key"  # Ensure this matches the one used in the frontend

    class Config:
        env_file = ".env"

settings = Settings()