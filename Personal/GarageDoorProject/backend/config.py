from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Credentials for the web interface (single user)
    login_username: str
    login_password: str

    # Secret used to sign JWT tokens — set a long random string in .env
    jwt_secret_key: str

    # Shared secret the ESP32 must present when opening the WebSocket connection.
    # Generate with: python -c "import secrets; print(secrets.token_hex(32))"
    esp_ws_token: str

    class Config:
        env_file = ".env"


settings = Settings()
