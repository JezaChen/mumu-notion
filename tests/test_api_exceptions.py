import pytest

from notionx import InvalidRequestUrlError, ValidationError
from tests.helpers import get_client


def test_InvalidRequestUrlError():
    client = get_client()

    with pytest.raises(InvalidRequestUrlError):
        client.get("/invalid_url")


def test_ValidationError():
    """ The test will pass the local validation,
    but failed in the validation run by server.
    """
    client = get_client()
    with pytest.raises(ValidationError):
        client.comments.create({
            "rich_text": [
                {"text": {"content": "This is a test."}}
            ],
            "parent": {
                "page_id": "invalid_page_id"
            }
        })
