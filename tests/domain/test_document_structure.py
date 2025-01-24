import pytest

from app.domain.models.document import Document, DocumentException
from tests.domain.model_creator import get_resume


def test_creating_document_with_missing_profile_throws_document_exception():
    resume = get_resume("some-id")
    resume.profile = None
    with pytest.raises(DocumentException):
        Document(**{"resume": resume})
