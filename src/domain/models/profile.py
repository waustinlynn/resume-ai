from typing import Optional
from uuid import uuid4

from pydantic import BaseModel, model_validator


class Profile(BaseModel):
    id: str
    email: str
    phone_number: Optional[str]
    first_name: str
    last_name: str

    @model_validator(mode="before")
    @classmethod
    def set_default_status(cls, values):
        """
        A model validator that sets a default value for the 'id' field
        if it is not provided during initialization.
        """
        if "id" not in values:
            values["id"] = str(uuid4())
        return values
