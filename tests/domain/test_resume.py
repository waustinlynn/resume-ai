import pytest
from pydantic import ValidationError

from app.domain.models.education import Education
from app.domain.models.experience import Experience, MissingExperienceException
from app.domain.models.profile import Profile
from app.domain.models.resume import Resume
from tests.domain.model_creator import (
    get_education_dict,
    get_experience_dict,
    get_profile_dict,
)

id = "sometestid"


@pytest.fixture(scope="function")
def existing_resume() -> Resume:
    return Resume(**{"id": id, "profile": get_profile_dict()})


@pytest.fixture(scope="function")
def experience() -> Experience:
    return Experience(**get_experience_dict())


def test_create_resume_without_profile_throw_validation_error():
    with pytest.raises(ValidationError):
        Resume(**{"id": id})


def test_create_resume_with_profile_succeeds():
    profile_dict = get_profile_dict()
    resume = Resume(**{"profile": profile_dict, "id": id})
    assert resume.profile.email == profile_dict["email"]
    assert resume.profile.first_name == profile_dict["first_name"]
    assert resume.profile.last_name == profile_dict["last_name"]
    assert resume.id == id


def test_update_profile_on_resume_replaces_profile():
    profile_dict = get_profile_dict()
    resume = Resume(**{"profile": profile_dict, "id": id})
    changed_email = "changedemail@test.com"
    changed_first_name = "FirstNameChanged"
    profile_dict["email"] = changed_email
    profile_dict["first_name"] = changed_first_name
    profile = Profile(**profile_dict)
    resume.update_profile(profile)
    assert resume.profile.email == changed_email
    assert resume.profile.first_name == changed_first_name


def test_add_experience_to_resume_adds_experience(
    existing_resume: Resume, experience: Experience
):
    existing_resume.add_experience(experience)
    assert len(existing_resume.experiences) == 1
    assert experience in existing_resume.experiences


def test_add_experience_to_resume_adds_multiple_experiences(
    existing_resume: Resume, experience: Experience
):
    existing_resume.add_experience(experience)
    new_experience = Experience(**get_experience_dict())
    new_experience.company_name = "Microsoft"
    existing_resume.add_experience(new_experience)
    assert len(existing_resume.experiences) == 2
    assert experience in existing_resume.experiences
    assert new_experience in existing_resume.experiences


def test_delete_experience_throws_exception_if_experience_not_found(
    existing_resume: Resume, experience: Experience
):
    with pytest.raises(MissingExperienceException):
        existing_resume.delete_experience(experience.id)


def test_delete_experience_removes_experience(
    existing_resume: Resume, experience: Experience
):
    existing_resume.add_experience(experience)
    assert len(existing_resume.experiences) == 1
    existing_resume.delete_experience(experience.id)
    assert len(existing_resume.experiences) == 0


def test_add_education_to_resume_adds_education(existing_resume: Resume):
    education = Education(**get_education_dict())
    existing_resume.add_education(education)
    assert len(existing_resume.educations) == 1
    assert education in existing_resume.educations
