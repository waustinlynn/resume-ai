import pytest
from mypy_boto3_dynamodb.service_resource import Table

from app.domain.models.resume import MissingResumeException, Resume
from app.infrastructure.persistence.abstract_resume_persistence import ResumePersistence
from tests.domain.model_creator import get_profile_dict


@pytest.fixture
def resume_persistence(test_resume_table: Table) -> ResumePersistence:
    return ResumePersistence(test_resume_table)


@pytest.mark.integration
def test_can_create_resume(
    test_hashed_email: str, resume_persistence: ResumePersistence
):
    resume = Resume(**{"id": test_hashed_email, "profile": get_profile_dict()})
    resume_persistence.create_resume(resume)
    assert True


@pytest.mark.integration
def test_can_create_resume_and_retrieve_resume(
    test_hashed_email: str, resume_persistence: ResumePersistence
):
    resume = Resume(**{"id": test_hashed_email, "profile": get_profile_dict()})
    resume_persistence.create_resume(resume)
    retrieved_resume = resume_persistence.get_resume(resume.id)
    assert retrieved_resume.id == resume.id
    assert retrieved_resume.profile.email == resume.profile.email


@pytest.mark.integration
def test_get_resume_raises_exception_when_resume_not_found(
    test_hashed_email: str, resume_persistence: ResumePersistence
):
    with pytest.raises(MissingResumeException):
        resume_persistence.get_resume(test_hashed_email)


@pytest.mark.integration
def test_add_resume_multiple_times_only_adds_single_resume(
    test_hashed_email: str,
    resume_persistence: ResumePersistence,
    test_resume_table: Table,
):
    resume = Resume(**{"id": test_hashed_email, "profile": get_profile_dict()})
    resume_persistence.create_resume(resume)
    resume_persistence.create_resume(resume)
    retrieved_resume = resume_persistence.get_resume(resume.id)
    assert retrieved_resume.id == resume.id
    assert retrieved_resume.profile.email == resume.profile.email
    assert len(list(test_resume_table.scan()["Items"])) == 1


@pytest.mark.integration
def test_add_multiple_resumes_will_add_accordingly(
    test_hashed_email: str,
    resume_persistence: ResumePersistence,
    test_resume_table: Table,
):
    resume1 = Resume(**{"id": test_hashed_email, "profile": get_profile_dict()})
    resume2 = Resume(**{"id": test_hashed_email + "2", "profile": get_profile_dict()})
    resume_persistence.create_resume(resume1)
    resume_persistence.create_resume(resume2)
    retrieved_resume1 = resume_persistence.get_resume(resume1.id)
    retrieved_resume2 = resume_persistence.get_resume(resume2.id)
    assert retrieved_resume1.id == resume1.id
    assert retrieved_resume1.profile.email == resume1.profile.email
    assert retrieved_resume2.id == resume2.id
    assert retrieved_resume2.profile.email == resume2.profile.email
    assert len(list(test_resume_table.scan()["Items"])) == 2
