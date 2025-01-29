import json
from string import Template
from typing import List

from pydantic import BaseModel

from app.domain.models.resume import Resume, ResumeException


class ChatCompletionMessage(BaseModel):
    role: str
    content: str


DEFAULT_PROMPT = Template(
    """
    You are a AI agent assigned to help candidates curate a customized resume
    based on an incoming job description.
    Your primary goal is to evaluate the job description and candidate's experience
    to determine the probability that the candidate is a good fit
    based on the job description.
    You will want heavily factor in the number of requirements in the job description
    that are met with the experience.
    You'll also want to heavily factor in years of experience.
    You will need to assume that their resume and experience will be filtered through
    and AI agent.
    The first user message will be a list of their skills.
    The next user message will be their experience,
    which will be a list including a job title and their highlights.
    The next message will be a job description.
    You will respond first with a probability (value 1-100)
    and probability description explaining the reasoning for the score.
    You will then need to respond with a list of experiences that
    best match the job description.
    You are to only use the content included in the user's
    highlights.
    $reword
    You are to only include up to 6 bullet points that are most
    relevant to the description (if there are more than 6, otherwise include all).
    Make sure you return all experiences back in the order they were sent in.
    Also include a short paragraph that can be used for a cover letter.
    Your response will be in json, but do not include any backticks or formatting to json
    (this will be parsed by a backend system):
    Your return message should be in the following format:
    {
        "probability": 0.8,
        "probability_description: "text",
        "experiences": [
            ...replay back the experience objects parsing only the relevant highlights
        ],
        "cover_letter_text": "text for cover letter"
    }
    """
)


def get_default_prompt(reword: bool) -> str:
    reword_description = """
        Do not re-word any of the highlights.
    """

    if reword:
        reword_description = """
            Feel free to reword or reorganize the highlights
            to best match the job description (do not embellish or fabricate).
        """
    return DEFAULT_PROMPT.substitute(reword=reword_description)


class ChatCompletion(BaseModel):
    resume: Resume
    job_description: str
    default_prompt: str = get_default_prompt(reword=True)

    def get_resume_experience_content(self) -> str:
        if not self.resume.experiences:
            raise ResumeException("Missing experience in resume")

        applicable_experiences = list(
            filter(
                lambda experience: len(experience.highlights) > 0,
                self.resume.experiences,
            )
        )

        if len(applicable_experiences) == 0:
            raise ResumeException("Missing experience highlights in resume")

        return json.dumps(
            [
                {
                    "company_name": experience.company_name,
                    "title": experience.title,
                    "highlights": [
                        highlight.description for highlight in experience.highlights
                    ],
                }
                for experience in applicable_experiences
            ]
        )

    def get_skills_content(self) -> str:
        return json.dumps(
            [
                f"{skill.category}: {', '.join(skill.skills)}"
                for skill in self.resume.skills
            ]
        )

    def get_chat_completion_messages(self) -> List[ChatCompletionMessage]:
        return (
            [ChatCompletionMessage(**{"role": "user", "content": self.default_prompt})]
            + [
                ChatCompletionMessage(
                    **{"role": "user", "content": self.get_skills_content()}
                )
            ]
            + [
                ChatCompletionMessage(
                    **{"role": "user", "content": self.get_resume_experience_content()}
                )
            ]
            + [
                ChatCompletionMessage(
                    **{"role": "user", "content": self.job_description}
                )
            ]
        )
