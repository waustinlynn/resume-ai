import json

import pytest

from app.domain.models.chat_completion import ChatCompletion
from app.domain.models.experience import MissingExperienceException
from app.domain.models.resume import Resume
from tests.domain.model_creator import get_test_resume
from tests.raw_data import TEST_JOB_DESCRIPTION


@pytest.fixture(scope="function")
def resume(test_hashed_email: str):
    return get_test_resume(test_hashed_email)


@pytest.fixture(scope="function")
def chat_completion(resume: Resume):
    return ChatCompletion(**{"resume": resume, "job_description": TEST_JOB_DESCRIPTION})


def test_get_chat_with_resume_missing_experience_raises_exception(
    resume: Resume,
    chat_completion: ChatCompletion,
):
    resume.experiences = []
    with pytest.raises(MissingExperienceException):
        chat_completion.get_resume_content()


def test_get_chat_with_resume_returns_resume_content(chat_completion: ChatCompletion):
    experiences_string = chat_completion.get_resume_content()
    experiences = json.loads(experiences_string)
    for experience in experiences:
        assert "job_title" in experience
        assert "highlights" in experience
        assert isinstance(experience["highlights"], list)
        assert isinstance(experience["job_title"], str)
        for highlight in experience["highlights"]:
            assert isinstance(highlight, str)


def test_get_chat_excludes_experience_if_highlights_are_missing(
    resume: Resume, chat_completion: ChatCompletion
):
    resume.experiences[0].highlights = []
    with pytest.raises(MissingExperienceException):
        chat_completion.get_resume_content()


def test_get_chat_messages_includes_system_prompt(
    resume: Resume, chat_completion: ChatCompletion
):
    chat_completion_messages = chat_completion.get_chat_completion_messages()
    assert chat_completion_messages[0].role == "system"


def test_get_chat_messages_has_default_system_prompt(chat_completion: ChatCompletion):
    chat_completion_messages = chat_completion.get_chat_completion_messages()
    assert chat_completion_messages[0].content == chat_completion.default_prompt


def test_get_chat_messages_includes_job_description(chat_completion: ChatCompletion):
    chat_completion_messages = chat_completion.get_chat_completion_messages()
    assert chat_completion_messages[2].content == TEST_JOB_DESCRIPTION
