from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    backend_server: str
    db_host: str
    db_port: int
    db_username: str
    db_password: str
    database: str
    gpt_secret_key: str
    chainlit_auth_secret: str 
    literal_api_key: str

    model_config = SettingsConfigDict(env_file=".env")
