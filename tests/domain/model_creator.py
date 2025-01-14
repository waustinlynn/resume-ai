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
