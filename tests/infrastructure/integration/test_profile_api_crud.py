import pytest
from fastapi.testclient import TestClient

from app.domain.models.resume import Resume
from app.infrastructure.factories import get_abstract_resume_persistence
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


@pytest.mark.integration
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


@pytest.mark.integration
def test_create_profile_creates_resume_in_db(
    test_app_client: TestClient,
    test_client_headers: dict,
    test_abstract_resume_persistence: AbstractResumePersistence = get_abstract_resume_persistence(),
):
    profile_dict = get_profile_dict()
    response = test_app_client.post(
        "/api/profile/", json=profile_dict, headers=test_client_headers
    )
    assert response.status_code == 201
    resume = test_abstract_resume_persistence.get_resume(response.json()["id"])
    assert resume.profile.email == profile_dict["email"]
