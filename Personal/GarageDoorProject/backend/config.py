from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Credentials for the web interface (single user)
    login_username: str
    login_password: str

    # Secret used to sign JWT tokens — set a long random string in .env
    jwt_secret_key: str

    # MQTT broker connection
    mqtt_broker: str = "localhost"
    mqtt_port: int = 1883
    mqtt_username: str = ""
    mqtt_password: str = ""
    mqtt_command_topic: str = "garage/command"
    mqtt_status_topic: str = "garage/status"
    # "tcp" for a direct connection on port 1883 (local/dev)
    # "websockets" when connecting through nginx on port 443
    mqtt_transport: str = "tcp"
    # Set to True when using websockets through nginx (port 443 = WSS, not plain WS)
    mqtt_tls: bool = False

    class Config:
        env_file = ".env"


settings = Settings()
