import pytest
from fastapi.testclient import TestClient

from app.domain.models.resume import Resume
from app.infrastructure.persistence.abstract_resume_persistence import (
    AbstractResumePersistence,
)
from app.infrastructure.settings import Settings
from app.infrastructure.utilities.hashing import hash_value
from tests.domain.model_creator import get_profile_dict


@pytest.fixture(scope="function")
def hashed_email(test_email_address: str) -> str:
    settings = Settings()
    return hash_value(test_email_address, settings.hashing_secret)


def test_create_profile_returns_resume(
    test_app_client: TestClient, test_client_headers: dict, hashed_email: str
):
    profile_dict = get_profile_dict()
    response = test_app_client.post(
        "/api/profile/", json=profile_dict, headers=test_client_headers
    )
    assert response.status_code == 201
    resume = Resume(**response.json())
    assert resume.profile.email == profile_dict["email"]
    assert resume.profile.first_name == profile_dict["first_name"]
    assert resume.profile.last_name == profile_dict["last_name"]
    assert resume.profile.phone_number == profile_dict["phone_number"]
    assert resume.id == hashed_email


def test_create_profile_calls_abstract_resume_persistence(
    test_app_client_with_abstract_resume_persistence: tuple[
        TestClient, AbstractResumePersistence
    ],
    test_client_headers: dict,
):
    profile_dict = get_profile_dict()
    test_app_client, mock_abstract_resume_persistence = (
        test_app_client_with_abstract_resume_persistence
    )
    response = test_app_client.post(
        "/api/profile/", json=profile_dict, headers=test_client_headers
    )
    assert response.status_code == 201
    mock_abstract_resume_persistence.create_resume.assert_called_once()
