import pytest
from fastapi.testclient import TestClient

from tests.raw_data import TEST_JOB_DESCRIPTION


@pytest.mark.integration
def test_curate_resume_accepts_blob_of_text(
    test_app_client: TestClient, test_client_headers: dict
):
    test_client_headers["content-type"] = "text/plain"
    response = test_app_client.post(
        "/api/curate/", headers=test_client_headers, data=TEST_JOB_DESCRIPTION
    )
    assert response.status_code == 200
