import pytest
from fastapi.testclient import TestClient

from app.domain.models.resume import Resume
from app.infrastructure.factories import get_abstract_resume_persistence
from app.infrastructure.persistence.abstract_resume_persistence import (
    AbstractResumePersistence,
)
from tests.domain.model_creator import get_test_resume


@pytest.fixture(scope="function")
def test_resume(test_hashed_email: str) -> Resume:
    return get_test_resume(test_hashed_email)


@pytest.fixture(scope="function")
def saved_resume(
    test_resume: Resume,
    test_abstract_resume_persistence: AbstractResumePersistence = get_abstract_resume_persistence(),
) -> Resume:
    test_abstract_resume_persistence.create_resume(test_resume)
    return test_resume


@pytest.mark.integration
def test_get_resume_returns_resume(
    test_app_client: TestClient,
    test_client_headers: dict,
    saved_resume: Resume,
):
    response = test_app_client.get("/api/resume/", headers=test_client_headers)
    assert response.status_code == 200
    response_resume = Resume(**response.json())
    assert response_resume.id == saved_resume.id


@pytest.mark.integration
def test_get_resume_throws_400_if_no_resume_found(
    test_app_client: TestClient,
):
    response = test_app_client.get(
        "/api/resume/", headers={"x-email-header": "unknown_email"}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Resume not found"


@pytest.mark.integration
def test_post_resume_assigns_id_from_header_and_returns_resume(
    test_app_client: TestClient,
    test_client_headers: dict,
    test_resume: Resume,
    test_hashed_email: str,
):
    resume_dict = test_resume.model_dump()
    del resume_dict["id"]
    response = test_app_client.post(
        "/api/resume/", headers=test_client_headers, json=resume_dict
    )
    assert response.status_code == 201
    response_resume = Resume(**response.json())
    assert response_resume.id == test_hashed_email


@pytest.mark.integration
def test_post_resume_returns_400_if_id_already_exists(
    test_app_client: TestClient,
    test_client_headers: dict,
    saved_resume: Resume,
):
    response = test_app_client.post(
        "/api/resume/", headers=test_client_headers, json=saved_resume.model_dump()
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Resume already exists"


@pytest.mark.integration
def test_put_resume_will_update_resume_correctly(
    test_app_client: TestClient,
    test_client_headers: dict,
    saved_resume: Resume,
):
    updated_resume_dict = saved_resume.model_dump()
    updated_resume_dict["profile"]["first_name"] = "New Name"
    response = test_app_client.put(
        "/api/resume/", headers=test_client_headers, json=updated_resume_dict
    )
    assert response.status_code == 200
    response_resume = Resume(**response.json())
    assert response_resume.profile.first_name == "New Name"


@pytest.mark.integration
def test_put_resume_if_missing_returns_400(
    test_app_client: TestClient, test_client_headers: dict, test_resume: Resume
):
    response = test_app_client.put(
        "/api/resume/", headers=test_client_headers, json=test_resume.model_dump()
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Resume not found"
