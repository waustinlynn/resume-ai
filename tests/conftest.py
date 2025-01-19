import pytest
from fastapi.testclient import TestClient
from mypy_boto3_dynamodb.service_resource import Table

from app.infrastructure.factories import (
    get_abstract_resume_persistence,
    get_resume_table,
)
from app.infrastructure.persistence.abstract_resume_persistence import (
    AbstractResumePersistence,
    ResumePersistence,
)
from app.infrastructure.settings import Settings
from app.infrastructure.utilities.hashing import hash_value
from app.main import api_app, app

settings = Settings()


@pytest.fixture(scope="function")
def test_abstract_resume_persistence(
    test_resume_table: Table,
) -> AbstractResumePersistence:
    return ResumePersistence(test_resume_table)


@pytest.fixture(scope="function")
def test_app_client(
    test_abstract_resume_persistence: AbstractResumePersistence,
) -> TestClient:  # type: ignore
    def _get_abstract_resume_persistence():
        return test_abstract_resume_persistence

    api_app.dependency_overrides[get_abstract_resume_persistence] = (
        _get_abstract_resume_persistence
    )
    client = TestClient(app)
    yield client
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


@pytest.fixture(scope="function")
def test_resume_table() -> Table:  # type: ignore
    table = get_resume_table()
    yield table
    table.delete()
