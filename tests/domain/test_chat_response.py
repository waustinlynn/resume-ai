import pytest
from pydantic import ValidationError

from app.domain.models.chat_response import ChatResponse


def test_chat_response_missing_experience_throws_exception():
    with pytest.raises(ValidationError):
        ChatResponse(
            **{
                "probability": 85,
                "probability_description": "Test probability description.",
                "experiences": [],
                "cover_letter_text": "Test cover letter text.",
            }
        )


def test_chat_response_missing_probability_throws_exception():
    with pytest.raises(ValidationError):
        ChatResponse(
            **{
                "probability_description": "Test probability description.",
                "experiences": [],
                "cover_letter_text": "Test cover letter text.",
            }
        )


def test_chat_response_missing_probability_description_throws_exception():
    with pytest.raises(ValidationError):
        ChatResponse(
            **{
                "probability": 85,
                "experiences": [],
                "cover_letter_text": "Test cover letter text.",
            }
        )


def test_chat_response_missing_cover_letter_text_throws_exception():
    with pytest.raises(ValidationError):
        ChatResponse(
            **{
                "probability": 85,
                "probability_description": "Test probability description.",
                "experiences": [],
            }
        )
