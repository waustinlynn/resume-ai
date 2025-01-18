from abc import ABC, abstractmethod

from mypy_boto3_dynamodb.service_resource import Table

from app.domain.models.resume import MissingResumeException, Resume


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
    document_type = "resume"

    def __init__(self, table: Table):
        self.table = table

    def create_resume(self, resume: Resume) -> Resume:
        resume_dict = resume.model_dump()
        resume_dict["document_type"] = self.document_type
        self.table.put_item(Item=resume_dict)
        return resume

    def get_resume(self, resume_id: str) -> Resume:
        resource = self.table.get_item(
            Key={"id": resume_id, "document_type": self.document_type}
        )
        if "Item" not in resource:
            raise MissingResumeException(f"Resume with ID {resume_id} not found")
        print(resource)
        return Resume(**resource["Item"])
