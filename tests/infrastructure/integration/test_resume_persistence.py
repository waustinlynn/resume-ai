import pytest
from mypy_boto3_dynamodb.service_resource import Table

from app.domain.models.resume import Resume, ResumeException
from app.infrastructure.persistence.abstract_resume_persistence import ResumePersistence
from tests.domain.model_creator import get_profile_dict, get_test_resume


@pytest.fixture(scope="function")
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
    with pytest.raises(ResumeException):
        resume_persistence.get_resume(test_hashed_email)


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


@pytest.mark.integration
def test_create_resume_if_already_exists_throws_exception(
    test_hashed_email: str,
    resume_persistence: ResumePersistence,
):
    resume = get_test_resume(test_hashed_email)
    resume_persistence.create_resume(resume)
    with pytest.raises(ResumeException):
        resume_persistence.create_resume(resume)


@pytest.mark.integration
def test_update_resume_if_not_exists_throws_resume_exception(
    test_hashed_email: str,
    resume_persistence: ResumePersistence,
):
    with pytest.raises(ResumeException):
        resume_persistence.update_resume(get_test_resume(test_hashed_email))


@pytest.mark.integration
def test_update_resume_correctly_updates_changed_fields(
    test_hashed_email: str,
    resume_persistence: ResumePersistence,
):
    resume = get_test_resume(test_hashed_email)
    resume_persistence.create_resume(resume)
    updated_resume = get_test_resume(test_hashed_email)
    updated_resume.profile.first_name = "New First Name"
    resume_persistence.update_resume(updated_resume)
    retrieved_resume = resume_persistence.get_resume(test_hashed_email)
    assert retrieved_resume.profile.first_name == "New First Name"
