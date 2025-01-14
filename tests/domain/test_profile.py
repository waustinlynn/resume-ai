import unittest
from uuid import uuid4

import pytest
from pydantic import ValidationError

from app.domain.models.profile import Profile
from tests.domain.model_creator import get_profile_dict


class ProfileTest(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def setup(self):
        self.values = get_profile_dict()

    def test_valid_profile_creation_with_default_id(self):
        """Test that a valid User model can be created."""

        profile = Profile(**self.values)
        assert profile.id is not None

    def test_profile_creation_with_specified_id(self):
        """Test that a User model can be created with a specified id."""
        str_uuid = str(uuid4())
        self.values["id"] = str_uuid
        profile = Profile(**self.values)
        assert profile.id == str_uuid
        assert profile.email == self.values["email"]

    def test_profile_with_bad_first_name_types_throws_validation_exception(self):
        """
        Test that a User model with a bad first_name type throws a validation error.
        """
        self.values["first_name"] = 123
        with pytest.raises(ValidationError):
            Profile(**self.values)
