from typing import List

from pydantic import BaseModel

from app.domain.models.education import Education
from app.domain.models.experience import Experience, MissingExperienceException
from app.domain.models.profile import Profile


class Resume(BaseModel):
    id: str
    profile: Profile
    experiences: List[Experience] = []
    educations: List[Education] = []

    def update_profile(self, profile: Profile):
        self.profile = profile

    def add_experience(self, experience: Experience):
        self.experiences.append(experience)

    def delete_experience(self, experience_id: str):
        applicable_experiences = [
            experience
            for experience in self.experiences
            if experience.id != experience_id
        ]
        if len(self.experiences) - len(applicable_experiences) != 1:
            raise MissingExperienceException(
                f"Experience with ID {experience_id} not found"
            )
        self.experiences = applicable_experiences

    def add_education(self, education: Education):
        self.educations.append(education)


class MissingResumeException(Exception):
    pass
