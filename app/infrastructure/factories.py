from app.domain.services.abstract_profile_service import (
    AbstractProfileService,
    ProfileService,
)
from app.infrastructure.persistence.abstract_resume_persistence import (
    AbstractResumePersistence,
    ResumePersistence,
)


def get_abstract_profile_service() -> AbstractProfileService:
    return ProfileService()


def get_abstract_resume_persistence() -> AbstractResumePersistence:
    return ResumePersistence()
