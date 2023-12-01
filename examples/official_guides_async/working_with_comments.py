""" Interactive API sample code for interacting with comments """
import asyncio

from examples.official_guides_async.common_prelude import get_client_and_base_page_id
from examples.official_guides_async.data import CommentExampleData
from examples.utils import colored_print, PrintStyle, generate_step_printer, press_enter_to_continue

__all__ = [
    "run_example_code",
]


async def run_example_code(is_continuous=False):
    print_step = generate_step_printer()

    client, base_page_id = get_client_and_base_page_id()

    ########################################
    # Create a comment with the page given #
    ########################################
    print_step("Create a comment with the page given")
    comment_create_body_data = CommentExampleData.COMMENT_DATA_EXAMPLE.copy()
    comment_create_body_data["parent"]["page_id"] = base_page_id
    comment_create_rsp = await client.comments.create(comment_create_body_data)

    print(f"--- Comment Create Result ---\n"
          f"{comment_create_rsp}\n"
          f"--- Comment Create Result ---")

    colored_print(f"The comment is created successfully. "
                  f"You can now view the intuitive result by clicking on the following links: "
                  f"https://www.notion.so/{base_page_id.replace('-', '')}",
                  color=PrintStyle.GREEN)
    if not is_continuous:
        press_enter_to_continue()
    ##############################
    # List comments with the page #
    ##############################
    print_step("List comments with the page")
    list_rsp = await client.comments.list({"block_id": base_page_id})

    print(f"--- Comment List Result ---\n"
          f"{list_rsp}\n"
          f"--- Comment List Result ---")


if __name__ == '__main__':
    asyncio.run(run_example_code())
