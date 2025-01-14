from fastapi.testclient import TestClient

from app.domain.models.profile import Profile
from app.domain.services.abstract_profile_service import (
    AbstractProfileService,
    MissingProfileError,
)
from tests.domain.model_creator import get_profile_dict


def test_create_profile_calls_profile_service_create_profile(
    test_app_client_with_abstract_profile: tuple[TestClient, AbstractProfileService]
):
    test_app_client, mock_profile_service = test_app_client_with_abstract_profile
    profile_dict = get_profile_dict()
    mock_profile_service.create_profile.return_value = Profile(**profile_dict)
    response = test_app_client.post("/profile/", json=profile_dict)
    assert response.status_code == 201
    mock_profile_service.create_profile.assert_called_once()


def test_get_profile_for_missing_profile_returns_400(
    test_app_client_with_abstract_profile: tuple[TestClient, AbstractProfileService]
):
    test_app_client, mock_profile_service = test_app_client_with_abstract_profile
    profile = Profile(**get_profile_dict())
    mock_profile_service.get_profile.side_effect = MissingProfileError()
    response = test_app_client.get(f"/profile/{profile.id}")
    assert response.status_code == 400
    assert response.json() == {"message": "Profile not found"}


def test_get_profile_for_existing_profile_returns_profile(
    test_app_client_with_abstract_profile: tuple[TestClient, AbstractProfileService]
):
    test_app_client, mock_profile_service = test_app_client_with_abstract_profile
    profile = Profile(**get_profile_dict())
    mock_profile_service.get_profile.return_value = profile
    response = test_app_client.get(f"/profile/{profile.id}")
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["id"] == profile.id
    assert response_data["email"] == profile.email
    assert response_data["first_name"] == profile.first_name
    assert response_data["last_name"] == profile.last_name
