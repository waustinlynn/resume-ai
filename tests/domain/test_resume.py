import pytest
from pydantic import ValidationError

from app.domain.models.profile import Profile
from app.domain.models.resume import Resume
from tests.domain.model_creator import get_profile_dict

id = "sometestid"


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
