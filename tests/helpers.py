import contextlib
import os

from notionx import Client
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


@contextlib.contextmanager
def keep_notion_environment_variables():
    """ Some tests will affect the environment variables,
    use this context to protect the environment variables
    can be restored to their original state after the test is finished
    """
    auth_token = os.getenv(NOTION_AUTH_TOKEN_KEY)
    base_page_id = os.getenv(NOTION_BASE_PAGE_ID_KEY)
    try:
        yield auth_token, base_page_id
    finally:
        # restore the environment variables
        os.putenv(NOTION_AUTH_TOKEN_KEY, auth_token)
        os.putenv(NOTION_BASE_PAGE_ID_KEY, base_page_id)

        if os.getenv(NOTION_AUTH_TOKEN_KEY) is None or os.getenv(NOTION_BASE_PAGE_ID_KEY) is None:
            os.environ[NOTION_AUTH_TOKEN_KEY] = auth_token
            os.environ[NOTION_BASE_PAGE_ID_KEY] = base_page_id
