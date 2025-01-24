import pytest
from fastapi.testclient import TestClient
from mypy_boto3_dynamodb.service_resource import Table

from app.domain.models.resume import Resume
from app.infrastructure.factories import get_abstract_resume_persistence
from app.infrastructure.persistence.abstract_resume_persistence import (
    AbstractResumePersistence,
)
from tests.domain.model_creator import get_profile_dict


@pytest.fixture(scope="function")
def resume(test_hashed_email: str) -> Resume:
    return Resume(**{"id": test_hashed_email, "profile": get_profile_dict()})


@pytest.fixture(scope="function")
def saved_resumed(test_table: Table, resume: Resume) -> Resume:
    resume_dict = resume.model_dump()
    resume_dict["document_type"] = "resume"
    test_table.put_item(Item=resume_dict)
    return resume


@pytest.mark.integration
def test_get_resume_returns_resume(
    test_app_client: TestClient,
    test_client_headers: dict,
    resume: Resume,
    test_abstract_resume_persistence: AbstractResumePersistence = get_abstract_resume_persistence(),
):
    test_abstract_resume_persistence.create_resume(resume)
    response = test_app_client.get("/api/resume/", headers=test_client_headers)
    assert response.status_code == 200
    response_resume = Resume(**response.json())
    assert response_resume.id == resume.id


@pytest.mark.integration
def test_get_resume_throws_400_if_no_resume_found(
    test_app_client: TestClient,
):
    response = test_app_client.get(
        "/api/resume/", headers={"x-email-header": "not_found"}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Resume not found"
