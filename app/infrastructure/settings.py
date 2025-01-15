from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    hashing_secret: str = "my_hashing_secret"
