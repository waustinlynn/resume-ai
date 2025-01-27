from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    hashing_secret: str = "my_hashing_secret"
    db_host: str = "http://localhost:5000"
    db_aws_access_key_id: str = "fakeAccessKeyId"
    db_aws_secret_access_key: str = "fakeSecretAccessKey"
    resume_table_name: str = "test_resume_table"
    openai_api_key: str = "fakeOpenAIKey"
