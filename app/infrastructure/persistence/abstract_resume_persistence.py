from abc import ABC, abstractmethod

from app.domain.models.resume import Resume


class AbstractResumePersistence(ABC):
    @abstractmethod
    def create_resume(self, resume: Resume) -> Resume:
        pass

    @abstractmethod
    def get_resume(self, resume_id: str) -> Resume:
        """
        Get a resume by its ID
        Raises a MissingResumeException if the resume is not found
        """
        pass


class ResumePersistence(AbstractResumePersistence):
    def create_resume(self, resume: Resume) -> Resume:
        return resume

    def get_resume(self, resume_id: str) -> Resume:
        pass
