from fastapi.testclient import TestClient


def test_api_call_without_proper_header_returns_400(test_app_client: TestClient):
    response = test_app_client.post("/api/profile/", json={})
    assert response.status_code == 400
    assert response.json()["detail"] == "x-email-header is required"
