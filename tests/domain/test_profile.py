import unittest
from uuid import uuid4

import pytest

from domain.models.profile import Profile


class ProfileTest(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def setup(self):
        self.values = {
            "email": "test@email.com",
            "phone_number": "123890",
            "first_name": "Test",
            "last_name": "User",
        }

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
