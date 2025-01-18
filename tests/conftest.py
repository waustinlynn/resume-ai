from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

from app.infrastructure.factories import get_abstract_resume_persistence
from app.infrastructure.persistence.abstract_resume_persistence import (
    AbstractResumePersistence,
)
from app.infrastructure.settings import Settings
from app.infrastructure.utilities.hashing import hash_value
from app.main import api_app, app

settings = Settings()


@pytest.fixture(scope="session")
def test_app_client() -> TestClient:  # type: ignore
    client = TestClient(app)
    yield client


@pytest.fixture(scope="function")
def test_app_client_with_abstract_resume_persistence() -> (
    tuple[TestClient, AbstractResumePersistence]
):  # type: ignore
    mock_abstract_resume_persistence = MagicMock(spec=AbstractResumePersistence)

    def _get_mock_abstract_resume_persistence():
        return mock_abstract_resume_persistence

    api_app.dependency_overrides[get_abstract_resume_persistence] = (
        _get_mock_abstract_resume_persistence
    )
    client = TestClient(app)
    yield client, mock_abstract_resume_persistence
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
