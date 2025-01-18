import pytest

from app.domain.models.resume import Resume
from app.infrastructure.factories import get_resume_table_name
from app.infrastructure.persistence.abstract_resume_persistence import ResumePersistence
from tests.domain.model_creator import get_profile_dict


@pytest.mark.integration
def test_can_create_resume(test_hashed_email: str):
    test_resume_table = get_resume_table_name()
    resume = Resume(**{"id": test_hashed_email, "profile": get_profile_dict()})
    ResumePersistence(test_resume_table).create_resume(resume)
    assert True


@pytest.mark.integration
def test_can_create_resume_and_retrieve_resume(test_hashed_email: str):
    test_resume_table = get_resume_table_name()
    resume_persistence = ResumePersistence(test_resume_table)
    resume = Resume(**{"id": test_hashed_email, "profile": get_profile_dict()})
    resume_persistence.create_resume(resume)
    retrieved_resume = resume_persistence.get_resume(resume.id)
    assert retrieved_resume.id == resume.id
    assert retrieved_resume.profile.email == resume.profile.email
