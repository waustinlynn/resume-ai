from typing import List, Optional
from uuid import uuid4

from pydantic import BaseModel, model_validator


class Highlight(BaseModel):
    id: str
    description: str

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


class Experience(BaseModel):
    company_name: str
    location: str
    title: str
    start_month: int
    start_year: int
    end_month: Optional[int] = None
    end_year: Optional[int] = None
    description: Optional[str] = None
    highlights: List[Highlight] = []

    @property
    def is_current(self):
        return self.end_month is None and self.end_year is None

    def add_highlight(self, highlight: str):
        self.highlights.append(Highlight(description=highlight))
