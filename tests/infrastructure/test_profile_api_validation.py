from fastapi.testclient import TestClient

from tests.domain.model_creator import get_profile_dict


def test_can_create_profile(test_app_client: TestClient, test_client_headers: dict):
    profile_dict = get_profile_dict()
    response = test_app_client.post(
        "/api/profile/", json=profile_dict, headers=test_client_headers
    )
    assert response.status_code == 201
    assert response.json()["profile"]["email"] == profile_dict["email"]
    assert response.json()["profile"]["first_name"] == profile_dict["first_name"]
    assert response.json()["profile"]["last_name"] == profile_dict["last_name"]


def test_missing_profile_data_throws_422(
    test_app_client: TestClient, test_client_headers: dict
):
    response = test_app_client.post(
        "/api/profile/", json={"email": "test@email.com"}, headers=test_client_headers
    )
    assert response.status_code == 422
    json_response_detail = response.json()["detail"]
    assert ["body", "first_name"] in [error["loc"] for error in json_response_detail]
    assert ["body", "last_name"] in [error["loc"] for error in json_response_detail]


def test_missing_phone_number_returns_201(
    test_app_client: TestClient, test_client_headers: dict
):
    profile_dict = get_profile_dict()
    del profile_dict["phone_number"]
    response = test_app_client.post(
        "/api/profile/", json=profile_dict, headers=test_client_headers
    )
    assert response.status_code == 201
    assert response.json()["profile"]["email"] is not None
    assert response.json()["profile"]["phone_number"] is None


def test_bad_first_name_data_type_throws_422(
    test_app_client: TestClient, test_client_headers: dict
):
    profile_dict = get_profile_dict()
    profile_dict["first_name"] = 123
    response = test_app_client.post(
        "/api/profile/", json=profile_dict, headers=test_client_headers
    )
    assert response.status_code == 422
    json_response_detail = response.json()["detail"]
    assert ["body", "first_name"] in [error["loc"] for error in json_response_detail]
