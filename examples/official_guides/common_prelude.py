""" Common prelude to all examples, used to get the Client and the base page id """

import os
from examples.utils import colored_print, PrintStyle
from mumu_notion import Client

__all__ = [
    "get_client",
    "get_client_and_base_page_id"
]


def get_client() -> Client:
    token = os.getenv("NOTION_AUTH_TOKEN")
    if not token:
        colored_print("First, please provide your integration token. "
                      "If not, please go to https://www.notion.so/my-integrations to generate it.\n"
                      "You can enter the token from below, "
                      "or write it to environment variables and restart the script.",
                      color=PrintStyle.GREEN)
        token = input("ENTER your integration token: ")
    else:
        colored_print("Found the integration token from environment variable.", color=PrintStyle.GREEN)

    colored_print("Initializing Client...", color=PrintStyle.GREEN)

    # Initialize a client given integration token
    client = Client({
        "auth_token": token
    })
    return client


def get_client_and_base_page_id() -> (Client, str):
    client = get_client()
    base_page_id = os.getenv("NOTION_BASE_PAGE_ID")
    if not base_page_id:
        colored_print("Now, please create a new blank page in Notion and share it to your integration "
                      "and provide the page_id of the blank page below.\n"
                      "For example, if the new page url is https://www.notion.so/fbaa9063dea94dd48d09b9eb2d5052a0, "
                      "the page_id is fbaa9063dea94dd48d09b9eb2d5052a0.\n"
                      "You can enter the page id from below, "
                      "or write it to environment variables and restart the script.",
                      color=PrintStyle.GREEN)
        base_page_id = input("ENTER the page_id of the blank page: ")
    else:
        colored_print(f"Found the base page id {base_page_id} from environment variable.", color=PrintStyle.GREEN)

    return client, base_page_id
