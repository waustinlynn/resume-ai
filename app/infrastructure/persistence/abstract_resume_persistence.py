from abc import ABC, abstractmethod

from mypy_boto3_dynamodb.service_resource import Table

from app.domain.models.resume import Resume, ResumeException


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

    @abstractmethod
    def update_resume(self, resume: Resume) -> Resume:
        """
        Update a resume by its ID
        """
        pass


class ResumePersistence(AbstractResumePersistence):
    document_type = "resume"

    def __init__(self, table: Table):
        self.table = table

    def create_resume(self, resume: Resume) -> Resume:
        existing_resume = None
        try:
            existing_resume = self.get_resume(resume.id)
        except ResumeException:
            pass

        print(existing_resume)
        if existing_resume:
            raise ResumeException("Resume already exists")

        resume_dict = resume.model_dump()
        resume_dict["document_type"] = self.document_type
        self.table.put_item(Item=resume_dict)
        return resume

    def get_resume(self, resume_id: str) -> Resume:
        resource = self.table.get_item(
            Key={"id": resume_id, "document_type": self.document_type}
        )
        if "Item" not in resource:
            raise ResumeException("Resume not found")
        return Resume(**resource["Item"])

    def update_resume(self, resume: Resume) -> Resume:
        self.get_resume(resume.id)
        resume_dict = resume.model_dump()
        resume_dict["document_type"] = self.document_type
        self.table.put_item(Item=resume_dict)
        return resume
