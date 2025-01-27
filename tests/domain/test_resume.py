import pytest
from pydantic import ValidationError

from app.domain.models.experience import Experience
from app.domain.models.resume import Resume
from tests.domain.model_creator import get_experience_dict, get_profile_dict

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
