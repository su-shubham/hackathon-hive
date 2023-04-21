from pydantic import BaseSettings


class Settings(BaseSettings):
    database_username: str
    database_password: str
    database_password: str
    database_name: str
    database_host: str
    secret_key: str
    algorithm: str
    expire_delta: int

    class Config:
        env_file = ".env"


settings = Settings()
