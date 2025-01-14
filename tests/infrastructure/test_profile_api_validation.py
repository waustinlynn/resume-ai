from fastapi.testclient import TestClient

from tests.domain.model_creator import get_profile_dict


def test_can_create_profile(test_app_client: TestClient):
    profile_dict = get_profile_dict()
    response = test_app_client.post("/profile/", json=profile_dict)
    assert response.status_code == 201
    assert response.json()["id"] is not None


def test_missing_profile_data_throws_422(test_app_client: TestClient):
    response = test_app_client.post("/profile/", json={"email": "test@email.com"})
    assert response.status_code == 422
    json_response_detail = response.json()["detail"]
    assert ["body", "first_name"] in [error["loc"] for error in json_response_detail]
    assert ["body", "last_name"] in [error["loc"] for error in json_response_detail]


def test_missing_phone_number_returns_201(test_app_client: TestClient):
    profile_dict = get_profile_dict()
    del profile_dict["phone_number"]
    response = test_app_client.post("/profile/", json=profile_dict)
    assert response.status_code == 201
    assert response.json()["id"] is not None
    assert response.json()["phone_number"] is None


def test_bad_first_name_data_type_throws_422(test_app_client: TestClient):
    profile_dict = get_profile_dict()
    profile_dict["first_name"] = 123
    response = test_app_client.post("/profile/", json=profile_dict)
    assert response.status_code == 422
    json_response_detail = response.json()["detail"]
    assert ["body", "first_name"] in [error["loc"] for error in json_response_detail]
