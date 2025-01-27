from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

from app.domain.models.resume import Resume, ResumeException
from app.infrastructure.chat.abstract_chat_completion import AbstractChatCompletion
from app.infrastructure.factories import (
    get_abstract_chat_completion,
    get_abstract_resume_persistence,
)
from app.infrastructure.persistence.abstract_resume_persistence import (
    AbstractResumePersistence,
)
from tests.domain.model_creator import get_test_resume
from tests.raw_data import TEST_JOB_DESCRIPTION


@pytest.fixture(scope="function")
def test_resume(test_hashed_email: str) -> Resume:
    return get_test_resume(test_hashed_email)


@pytest.fixture(scope="function")
def test_abstract_chat_completion() -> AbstractChatCompletion:
    abstract_chat_completion = MagicMock(spec=AbstractChatCompletion)
    abstract_chat_completion.complete.return_value = """
    {
        "probability": 8
    }
"""
    return abstract_chat_completion


@pytest.fixture(scope="function")
def test_abstract_resume_persistence(test_resume: Resume) -> AbstractResumePersistence:
    abstract_resume_persistence = MagicMock(spec=AbstractResumePersistence)
    abstract_resume_persistence.get_resume.return_value = test_resume
    return abstract_resume_persistence


@pytest.fixture(scope="function")
def test_local_app_client(
    test_abstract_chat_completion: AbstractChatCompletion,
    test_abstract_resume_persistence: AbstractResumePersistence,
) -> TestClient:  # type: ignore
    from app.main import api_app, app

    def _get_abstract_chat_completion():
        return test_abstract_chat_completion

    def _get_abstract_resume_persistence():
        return test_abstract_resume_persistence

    api_app.dependency_overrides[get_abstract_chat_completion] = (
        _get_abstract_chat_completion
    )
    api_app.dependency_overrides[get_abstract_resume_persistence] = (
        _get_abstract_resume_persistence
    )
    yield TestClient(app)
    api_app.dependency_overrides.clear()


@pytest.mark.integration
def test_curate_resume_accepts_blob_of_text(
    test_local_app_client: TestClient, test_client_headers: dict
):
    test_client_headers["content-type"] = "text/plain"
    response = test_local_app_client.post(
        "/api/curate/", headers=test_client_headers, data=TEST_JOB_DESCRIPTION
    )
    assert response.status_code == 200


@pytest.mark.integration
def test_curate_resume_calls_abstract_chat_completion(
    test_local_app_client: TestClient,
    test_client_headers: dict,
    test_abstract_chat_completion: AbstractChatCompletion,
    test_abstract_resume_persistence: AbstractResumePersistence,
    test_hashed_email: str,
):
    test_client_headers["content-type"] = "text/plain"
    response = test_local_app_client.post(
        "/api/curate/", headers=test_client_headers, data=TEST_JOB_DESCRIPTION
    )
    assert response.status_code == 200
    test_abstract_chat_completion.complete.assert_called_once()


@pytest.mark.integration
def test_curate_resume_with_missing_resume_returns_400(
    test_local_app_client: TestClient,
    test_client_headers: dict,
    test_abstract_chat_completion: AbstractChatCompletion,
    test_abstract_resume_persistence: AbstractResumePersistence,
    test_hashed_email: str,
):
    test_abstract_resume_persistence.get_resume.side_effect = ResumeException(
        "Resume not found"
    )
    test_client_headers["content-type"] = "text/plain"
    response = test_local_app_client.post(
        "/api/curate/", headers=test_client_headers, data=TEST_JOB_DESCRIPTION
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Resume not found"
    test_abstract_chat_completion.complete.assert_not_called()
