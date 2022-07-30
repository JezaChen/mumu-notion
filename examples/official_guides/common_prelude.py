""" Common prelude to all examples, used to get the Client and the base page id """

from examples.utils import colored_print, PrintStyle
from py_notion import Client

__all__ = [
    "get_client",
    "get_client_and_base_page_id"
]


def get_client() -> Client:
    colored_print("First, please provide your integration token. "
                  "If not, please go to https://www.notion.so/my-integrations to generate it.",
                  color=PrintStyle.GREEN)
    token = input("ENTER your integration token: ")

    colored_print("Initializing Client...", color=PrintStyle.GREEN)

    # Initialize a client given integration token
    client = Client({
        "auth_token": token
    })
    return client


def get_client_and_base_page_id() -> (Client, str):
    colored_print("Now, please create a new blank page in Notion and share it to your integration "
                  "and provide the page_id of the blank page below.\n"
                  "For example, if the new page url is https://www.notion.so/fbaa9063dea94dd48d09b9eb2d5052a0, "
                  "the page_id is fbaa9063dea94dd48d09b9eb2d5052a0.",
                  color=PrintStyle.GREEN)
    client = get_client()
    base_page_id = input("ENTER the page_id of the blank page: ")

    return client, base_page_id
