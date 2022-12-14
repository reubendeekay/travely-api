

from pydantic import BaseSettings


class Settings(BaseSettings):
    database_host: str
    database_port: int
    database_user: str
    database_password: str
    database_name: str
    database_uri: str
    algorithm = str = "HS256"
    secret_key = str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"


settings = Settings(

)
