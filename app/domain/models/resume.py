from typing import List

from pydantic import BaseModel

from app.domain.models.education import Education
from app.domain.models.experience import Experience
from app.domain.models.profile import Profile
from app.domain.models.skill import Skill


class Resume(BaseModel):
    id: str
    profile: Profile
    skills: List[Skill] = []
    experiences: List[Experience] = []
    educations: List[Education] = []


class ResumeException(Exception):
    pass
