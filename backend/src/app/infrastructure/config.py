from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://dev:devpassword@localhost:5432/todo_db"
    FRONTEND_URL: str = "http://localhost:3000"

    model_config = {"env_file": ".env"}


settings = Settings()
