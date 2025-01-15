from typing import Optional
from uuid import uuid4

from pydantic import BaseModel, model_validator


class Education(BaseModel):
    id: str
    institution_name: str
    field_of_study: str = None
    degree: Optional[str] = None
    graduation_month: Optional[int] = None
    graduation_year: Optional[int] = None

    @model_validator(mode="before")
    @classmethod
    def set_default_id(cls, values):
        """
        A model validator that sets a default value for the 'id' field
        if it is not provided during initialization.
        """
        if "id" not in values:
            values["id"] = str(uuid4())
        return values
