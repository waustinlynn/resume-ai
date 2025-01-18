import pytest
from mypy_boto3_dynamodb.service_resource import Table

from app.domain.models.resume import Resume
from app.infrastructure.persistence.abstract_resume_persistence import ResumePersistence
from tests.domain.model_creator import get_profile_dict


@pytest.mark.integration
def test_can_create_resume(test_hashed_email: str, test_resume_table: Table):
    resume = Resume(**{"id": test_hashed_email, "profile": get_profile_dict()})
    ResumePersistence(test_resume_table).create_resume(resume)
    assert True
