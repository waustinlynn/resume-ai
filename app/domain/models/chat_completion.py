import json
from typing import List

from pydantic import BaseModel

from app.domain.models.experience import MissingExperienceException
from app.domain.models.resume import Resume


class ChatCompletionMessage(BaseModel):
    role: str
    content: str


class ChatCompletion(BaseModel):
    resume: Resume
    job_description: str
    default_prompt: str = """
    You are a AI agent assigned to help candidates curate a customized resume
    based on an incoming job description.
    The first user message will be their experience,
    which will be a list including a job title and their highlights.
    The next message will be a job description.
    You will need to respond with a list of experiences that
    best match the job description.
    You are to only use the content included in the user's
    highlights with minimal re-wording of highlights.
    You are to only include up to 6 bullet points that are most
    relevant to the description.
    Also return a probability score that will take into account
    how well the user's experience match the expectations for the position.
    Your return message should be in the following format:
    {
        "probability": 0.8,
        "experiences": [
            "id": "unique id that matched the experience id",
            "highlights": [
                ...applicable highlights as strings based on job description
            ]
        ]
    }
    """

    def get_resume_content(self) -> str:
        if not self.resume.experiences:
            raise MissingExperienceException("Missing experience in resume")

        applicable_experiences = list(
            filter(
                lambda experience: len(experience.highlights) > 0,
                self.resume.experiences,
            )
        )

        if len(applicable_experiences) == 0:
            raise MissingExperienceException("Missing experience highlights in resume")

        return json.dumps(
            [
                {
                    "job_title": experience.title,
                    "highlights": [
                        highlight.description for highlight in experience.highlights
                    ],
                }
                for experience in applicable_experiences
            ]
        )

    def get_chat_completion_messages(self) -> List[ChatCompletionMessage]:
        return (
            [
                ChatCompletionMessage(
                    **{"role": "system", "content": self.default_prompt}
                )
            ]
            + [
                ChatCompletionMessage(
                    **{"role": "user", "content": self.get_resume_content()}
                )
            ]
            + [
                ChatCompletionMessage(
                    **{"role": "user", "content": self.job_description}
                )
            ]
        )
