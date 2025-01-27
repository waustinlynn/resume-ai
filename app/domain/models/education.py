from typing import Optional

from pydantic import BaseModel


class Education(BaseModel):
    institution_name: str
    field_of_study: str = None
    degree: Optional[str] = None
    graduation_month: Optional[int] = None
    graduation_year: Optional[int] = None
