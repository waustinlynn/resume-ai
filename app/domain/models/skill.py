from typing import List

from pydantic import BaseModel


class Skill(BaseModel):
    category: str
    skills: List[str]
