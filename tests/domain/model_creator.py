import json

from app.domain.models.chat_response import ChatResponse
from app.domain.models.resume import Resume


def get_profile_dict():
    return {
        "email": "test@email.com",
        "phone_number": "123890",
        "first_name": "Test",
        "last_name": "User",
    }


def get_experience_dict():
    return {
        "company_name": "Awesome Company",
        "title": "Software Engineer",
        "location": "Remote",
        "start_month": 1,
        "start_year": 2020,
        "end_month": 1,
        "end_year": 2021,
        "description": "I did some stuff.",
        "highlights": [
            {"description": "I did a thing."},
            {"description": "I did another thing."},
        ],
    }


def get_skill_dict():
    return {
        "category": "Programming Languages",
        "skills": ["Python", "GO"],
    }


def get_education_dict():
    return {
        "institution_name": "University of Awesome",
        "degree": "Computer Science",
        "field_of_study": "Software Engineering",
        "graduation_month": 1,
        "graduaction_year": 2020,
    }


def get_test_resume(id: str) -> Resume:
    return Resume(
        id=id,
        profile=get_profile_dict(),
        skills=[get_skill_dict()],
        experiences=[get_experience_dict()],
        educations=[get_education_dict()],
    )


SAMPLE_OPENAI_CHAT_COMPLETION_RESPONSE = """
{
    "probability": 0.85,
    "probability_description": "The candidate has extensive experience as a Lead Software Engineer",
    "experiences": [
        {
            "company_name": "Zoe",
            "title": "Lead Software Engineer",
            "highlights": [
                "Architected scalable systems",
                "Delivered solutions across various domains including fulfillment",
                "Designed and implemented an algorithm for an in-app community feature.",
                "Led the migration from a legacy fulfillment system to a modern solution",
                "Streamlined customer support resolution by integrating chat providers"
            ]
        },
        {
            "company_name": "FinThrive",
            "title": "Lead Software Engineer",
            "highlights": [
                "Spearheaded the development of a cloud-native web product leveraging.",
                "Led a team emphasizing code quality and collaboration resulting in.",
                "Leveraged serverless functions and SQL/NoSQL databases to optimize.",
                "Implemented an event driven architecture for asynchronous"
            ]
        }
    ],
    "cover_letter_text": "I am excited to apply for the Senior Software Engineer"
}"""


def get_chat_response() -> ChatResponse:
    return ChatResponse(**json.loads(SAMPLE_OPENAI_CHAT_COMPLETION_RESPONSE))
