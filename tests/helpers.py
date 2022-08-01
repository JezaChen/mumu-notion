import os

from mumu_notion import Client
from tests.constants import NOTION_AUTH_TOKEN_KEY, NOTION_BASE_PAGE_ID_KEY


def get_client() -> Client:
    token = os.getenv(NOTION_AUTH_TOKEN_KEY)
    assert token is not None
    # Initialize a client given integration token
    client = Client({
        "auth_token": token
    })
    return client


def get_base_page_id() -> str:
    base_page_id = os.getenv(NOTION_BASE_PAGE_ID_KEY)
    assert base_page_id is not None
    return base_page_id
