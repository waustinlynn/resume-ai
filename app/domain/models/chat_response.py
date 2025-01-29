from typing import List

from pydantic import BaseModel, model_validator


class ChatResponseExperience(BaseModel):
    company_name: str
    title: str
    highlights: List[str]


class ChatResponse(BaseModel):
    probability: float
    probability_description: str
    experiences: List[ChatResponseExperience]
    cover_letter_text: str

    @model_validator(mode="before")
    @classmethod
    def validate_experiences(cls, values):
        if not values.get("experiences"):
            raise ValueError("experiences cannot be empty")
        return values
