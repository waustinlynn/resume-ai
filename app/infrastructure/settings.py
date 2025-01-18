from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    hashing_secret: str = "my_hashing_secret"
    db_host: str = "http://localhost:8000"
    resume_table_name: str = "test_resume_table"
