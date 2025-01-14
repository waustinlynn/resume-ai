from app.domain.services.abstract_profile_service import (
    AbstractProfileService,
    ProfileService,
)


def get_abstract_profile_service() -> AbstractProfileService:
    return ProfileService()
