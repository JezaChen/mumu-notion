import os

from mumu_notion import Client


def get_client() -> Client:
    token = os.getenv("NOTION_AUTH_TOKEN")
    assert token is not None
    # Initialize a client given integration token
    client = Client({
        "auth_token": token
    })
    return client
