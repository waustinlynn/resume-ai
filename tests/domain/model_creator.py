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
