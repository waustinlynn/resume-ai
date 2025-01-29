import tempfile

from docx import Document

from app.domain.models.chat_response import ChatResponse
from app.infrastructure.chat.abstract_document_generator import (
    AbstractDocumentGenerator,
    DocxGenerator,
)


def test_can_generate_document_with_required_paragraphs():
    abstract_document_generator: AbstractDocumentGenerator = DocxGenerator()
    chat_response = ChatResponse(
        **{
            "probability": 0.85,
            "probability_description": "Test probability description.",
            "experiences": [
                {
                    "company_name": "Test Company",
                    "title": "Software Engineer",
                    "highlights": ["Built a test feature"],
                }
            ],
            "cover_letter_text": "Test cover letter text.",
        }
    )
    with tempfile.NamedTemporaryFile(delete=True, suffix=".docx") as temp_file_path:
        abstract_document_generator.generate(chat_response, temp_file_path)

        # Load the document
        document = Document(temp_file_path)

        # Assert content
        paragraphs = [p.text for p in document.paragraphs]
        assert "Candidate Profile" in paragraphs
        assert "Probability: 85%" in paragraphs
        assert "Test probability description." in paragraphs
        assert "Test Company" in paragraphs
        assert "Software Engineer" in paragraphs
        assert "- Built a test feature" in paragraphs
        assert "Test cover letter text." in paragraphs
