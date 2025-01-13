from fixtures import app_client


def test_can_create_profile(app_client):
    response = app_client.post("/profile/", json={"email": "test@email.com"})
    assert response.status_code == 201
    assert response.json()["id"] is not None
