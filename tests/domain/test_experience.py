import unittest

import pytest

from app.domain.models.experience import Experience
from tests.domain.model_creator import get_experience_dict


class ExperienceTest(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def setup(self):
        self.values = get_experience_dict()

    def test_valid_experience_creation(self):
        """Test that a valid Experience class can be created."""

        experience = Experience(**self.values)
        assert experience is not None

    def test_experience_is_current(self):
        """
        Test that the is_current property returns True
        when the experience is current.
        """
        self.values["end_month"] = None
        self.values["end_year"] = None

        experience = Experience(**self.values)
        assert experience.is_current

    def test_experience_is_not_current_if_end_month_present(self):
        """
        Test that the is_current property returns False
        when the end_month and end_year is present.
        """

        experience = Experience(**self.values)
        assert not experience.is_current

    def test_add_highlight(self):
        """Test that a highlight can be added to the experience."""

        experience = Experience(**self.values)
        new_experience = "I did a really great thing"
        experience.add_highlight(new_experience)
        assert new_experience in [high.description for high in experience.highlights]
