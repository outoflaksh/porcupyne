from pydantic import BaseSettings


class Settings(BaseSettings):
    debug: bool = False

    class Config:
        env_file = ".env"
