import pytest
from fastapi.testclient import TestClient
from mypy_boto3_dynamodb.service_resource import Table

from app.infrastructure.factories import get_resume_table
from app.infrastructure.settings import Settings
from app.infrastructure.utilities.hashing import hash_value
from app.main import app

settings = Settings()


@pytest.fixture(scope="function")
def test_app_client() -> TestClient:  # type: ignore
    return TestClient(app)


@pytest.fixture(scope="function")
def test_email_address() -> str:
    return "test@email.com"


@pytest.fixture(scope="function")
def test_hashed_email(test_email_address: str) -> str:
    return hash_value(test_email_address, settings.hashing_secret)


@pytest.fixture(scope="function")
def test_client_headers(test_email_address: str) -> dict:
    return {"x-email-header": test_email_address}


@pytest.fixture(scope="function")
def test_resume_table() -> Table:  # type: ignore
    table = get_resume_table()
    yield table
    table.delete()
