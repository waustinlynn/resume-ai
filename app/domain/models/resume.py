from typing import List

from pydantic import BaseModel

from app.domain.models.education import Education
from app.domain.models.experience import Experience
from app.domain.models.profile import Profile


class Resume(BaseModel):
    id: str
    profile: Profile
    experiences: List[Experience] = []
    educations: List[Education] = []


class ResumeException(Exception):
    pass
