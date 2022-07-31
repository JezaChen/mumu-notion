import pytest

from mumu_notion import InvalidRequestUrlError
from tests.helpers import get_client

client = get_client()


def test_InvalidRequestUrlError():
    with pytest.raises(InvalidRequestUrlError):
        client.get("/invalid_url")
