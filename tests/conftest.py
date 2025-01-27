import pytest
from fastapi.testclient import TestClient
from mypy_boto3_dynamodb.service_resource import Table

from app.infrastructure.factories import get_dynamo_db_client, get_resume_table
from app.infrastructure.persistence.resume_table_definition import RESUME_TABLE_SPEC
from app.infrastructure.settings import Settings
from app.infrastructure.utilities.hashing import hash_value
from app.main import api_app, app

settings = Settings()


@pytest.fixture(scope="function")
def test_resume_table() -> Table:  # type: ignore
    client = get_dynamo_db_client()
    # throws ResourceInUseException if table already exists
    try:
        client.create_table(**RESUME_TABLE_SPEC)
    except client.meta.client.exceptions.ResourceInUseException:
        pass

    table = client.Table(settings.resume_table_name)
    table.wait_until_exists()

    yield table
    table.delete()


@pytest.fixture(scope="function")
def test_app_client(test_resume_table: Table) -> TestClient:  # type: ignore
    def _get_resume_table():
        return test_resume_table

    api_app.dependency_overrides[get_resume_table] = _get_resume_table
    yield TestClient(app)
    api_app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def test_email_address() -> str:
    return "test@email.com"


@pytest.fixture(scope="function")
def test_hashed_email(test_email_address: str) -> str:
    return hash_value(test_email_address, settings.hashing_secret)


@pytest.fixture(scope="function")
def test_client_headers(test_email_address: str) -> dict:
    return {"x-email-header": test_email_address}
