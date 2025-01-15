from pydantic import BaseModel

from app.domain.models.profile import Profile


class Resume(BaseModel):
    id: str
    profile: Profile

    def update_profile(self, profile: Profile):
        self.profile = profile


class MissingResumeException(Exception):
    pass
