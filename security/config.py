from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=False
    )

    database_url: str
    database_url_sync: str

    # JWT
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 60 * 24  # 1 dia

    # Frontend
    frontend_url: str = "http://localhost:5173"

    # App
    app_name: str = "Party Billy Divisor API"
    debug: bool = False


settings = Settings()
