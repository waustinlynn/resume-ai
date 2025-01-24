from pydantic import BaseModel, model_validator

from app.domain.models.resume import Resume


class Document(BaseModel):
    resume: Resume

    @model_validator(mode="before")
    @classmethod
    def validate_model(cls, values):
        if not values["resume"].profile:
            raise DocumentException("Profile is required")
        return values


class DocumentException(Exception):
    pass
