from abc import ABC, abstractmethod

from app.domain.models.profile import Profile


class AbstractProfileService(ABC):
    @abstractmethod
    def create_profile(self, profile: Profile) -> Profile:
        pass

    @abstractmethod
    def get_profile(self, profile_id: str) -> Profile:
        pass


class ProfileService(AbstractProfileService):
    def create_profile(self, profile: Profile) -> Profile:
        return profile

    def get_profile(self, profile_id: str) -> Profile:
        profile = {
            "id": profile_id,
            "email": "test@email.com",
            "first_name": "Test",
            "last_name": "User",
        }
        return Profile(**profile)


class MissingProfileError(Exception):
    pass
