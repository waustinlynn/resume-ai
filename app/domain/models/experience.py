from typing import List, Optional

from pydantic import BaseModel


class Highlight(BaseModel):
    description: str


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
