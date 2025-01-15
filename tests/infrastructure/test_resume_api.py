from typing import Callable

import pytest
from fastapi.testclient import TestClient

from app.domain.models.resume import MissingResumeException, Resume
from app.infrastructure.persistence.abstract_resume_persistence import (
    AbstractResumePersistence,
)
from tests.domain.model_creator import get_profile_dict


@pytest.fixture(scope="function")
def resume(test_hashed_email: str) -> Resume:
    return Resume(**{"id": test_hashed_email, "profile": get_profile_dict()})


@pytest.fixture(scope="function")
def get_resume_by_specific_id(
    test_hashed_email: str, resume: Resume
) -> Callable[[str], Resume]:
    def _get_resume(id: str) -> Resume:
        if id == test_hashed_email:
            return resume
        raise MissingResumeException("Resume not found")

    return _get_resume


def test_get_resume_returns_resume(
    test_app_client_with_abstract_resume_persistence: tuple[
        TestClient, AbstractResumePersistence
    ],
    test_client_headers: dict,
    get_resume_by_specific_id: Callable[[str], Resume],
    resume: Resume,
):
    test_app_client, mock_abstract_resume_persistence = (
        test_app_client_with_abstract_resume_persistence
    )
    mock_abstract_resume_persistence.get_resume.side_effect = get_resume_by_specific_id
    response = test_app_client.get("/api/resume/", headers=test_client_headers)
    assert response.status_code == 200
    response_resume = Resume(**response.json())
    assert response_resume.id == resume.id


def test_get_resume_throws_400_if_no_resume_found(
    test_app_client_with_abstract_resume_persistence: tuple[
        TestClient, AbstractResumePersistence
    ],
    get_resume_by_specific_id: Callable[[str], Resume],
):
    test_app_client, mock_abstract_resume_persistence = (
        test_app_client_with_abstract_resume_persistence
    )
    mock_abstract_resume_persistence.get_resume.side_effect = get_resume_by_specific_id
    response = test_app_client.get(
        "/api/resume/", headers={"x-email-header": "not_found"}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Resume not found"
