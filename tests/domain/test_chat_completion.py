import json

import pytest

from app.domain.models.chat_completion import ChatCompletion
from app.domain.models.resume import Resume, ResumeException
from app.domain.models.skill import Skill
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
    with pytest.raises(ResumeException):
        chat_completion.get_resume_experience_content()


def test_get_chat_with_resume_returns_resume_content(chat_completion: ChatCompletion):
    experiences_string = chat_completion.get_resume_experience_content()
    experiences = json.loads(experiences_string)
    for experience in experiences:
        assert "title" in experience
        assert "highlights" in experience
        assert "company_name" in experience
        assert isinstance(experience["highlights"], list)
        assert isinstance(experience["title"], str)
        for highlight in experience["highlights"]:
            assert isinstance(highlight, str)


def test_get_chat_with_resume_returns_skills_content(
    resume: Resume, chat_completion: ChatCompletion
):
    skills = [
        Skill(**{"category": "Programming Languages", "skills": ["Python", "GO"]}),
    ]
    resume.skills.append(
        Skill(**{"category": "Leadership", "skills": ["Team Building", "Mentoring"]})
    )
    skills_string = chat_completion.get_skills_content()
    skills = json.loads(skills_string)
    assert isinstance(skills, list)
    assert len(skills) == 2
    assert "Programming Languages: Python, GO" in skills
    assert "Leadership: Team Building, Mentoring" in skills


def test_get_chat_excludes_experience_if_highlights_are_missing(
    resume: Resume, chat_completion: ChatCompletion
):
    resume.experiences[0].highlights = []
    with pytest.raises(ResumeException):
        chat_completion.get_resume_experience_content()


def test_get_chat_messages_has_default_system_prompt(chat_completion: ChatCompletion):
    chat_completion_messages = chat_completion.get_chat_completion_messages()
    assert chat_completion_messages[0].content == chat_completion.default_prompt


def test_get_chat_messages_has_skill_content(chat_completion: ChatCompletion):
    chat_completion_messages = chat_completion.get_chat_completion_messages()
    assert chat_completion_messages[1].content == chat_completion.get_skills_content()


def test_get_chat_messages_has_resumt_content(chat_completion: ChatCompletion):
    chat_completion_messages = chat_completion.get_chat_completion_messages()
    assert (
        chat_completion_messages[2].content
        == chat_completion.get_resume_experience_content()
    )


def test_get_chat_messages_includes_job_description(chat_completion: ChatCompletion):
    chat_completion_messages = chat_completion.get_chat_completion_messages()
    assert chat_completion_messages[3].content == TEST_JOB_DESCRIPTION
