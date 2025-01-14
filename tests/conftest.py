from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

from app.domain.services.abstract_profile_service import AbstractProfileService
from app.infrastructure.factories import get_abstract_profile_service
from app.main import app


@pytest.fixture(scope="function")
def test_app_client_with_abstract_profile() -> (
    tuple[TestClient, AbstractProfileService]
):  # type: ignore
    mock_abstract_profile_service = MagicMock(spec=AbstractProfileService)

    def _get_mock_profile_service():
        return mock_abstract_profile_service

    app.dependency_overrides[get_abstract_profile_service] = _get_mock_profile_service
    client = TestClient(app)
    yield client, mock_abstract_profile_service
    app.dependency_overrides.clear()


@pytest.fixture(scope="session")
def test_app_client() -> TestClient:
    client = TestClient(app)
    yield client
