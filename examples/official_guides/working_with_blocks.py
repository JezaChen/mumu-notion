""" Interactive API sample code for interacting with blocks """

from examples.official_guides.common_prelude import get_client_and_base_page_id
from examples.official_guides.data import BlockExampleData
from examples.utils import colored_print, PrintStyle, generate_step_printer, press_enter_to_continue

__all__ = [
    "run_example_code",
]


def run_example_code(is_continuous=False):
    print_step = generate_step_printer()

    client, base_page_id = get_client_and_base_page_id()

    ###################################################
    # Append two blocks as children of the page given #
    ###################################################

    print_step("Append two blocks as children of the page given")

    block_append_rsp = client.blocks.children.append(base_page_id, BlockExampleData.CHILD_BLOCK_APPEND_DATA_EXAMPLE)
    print(f"--- Block Children Append Result ---\n"
          f"{block_append_rsp}\n"
          f"--- Block Children Append Result ---")

    appended_heading2_block_info = block_append_rsp["results"][0]
    appended_paragraph_block_info = block_append_rsp["results"][1]

    appended_heading2_block_id = appended_heading2_block_info["id"]
    appended_paragraph_block_id = appended_paragraph_block_info["id"]

    colored_print(f"The blocks are appended successfully. "
                  f"You can now view the intuitive result by clicking on the following links: "
                  f"https://www.notion.so/{base_page_id.replace('-', '')}",
                  color=PrintStyle.GREEN)

    if not is_continuous:
        press_enter_to_continue()
    #############################################
    # List all block children of the page given #
    #############################################
    print_step("List all block children of the page given")

    list_rsp = client.blocks.children.list(base_page_id)
    print(f"--- Children List Result ---\n"
          f"{list_rsp}\n"
          f"--- Children List Result ---")

    if not is_continuous:
        press_enter_to_continue()
    ####################################################
    # Retrieve the information of the heading_2 block  #
    ####################################################

    print_step("Retrieve the information of the heading_2 block")
    retrieve_rsp = client.blocks.retrieve(appended_heading2_block_id)

    print(f"--- Block Retrieve Result ---\n"
          f"{block_append_rsp}\n"
          f"--- Block Retrieve Result ---")

    if not is_continuous:
        press_enter_to_continue()
    ##############################################
    # Update the content of the heading_2 block  #
    ##############################################

    print("Update the content of the heading_2 block")
    update_rsp = client.blocks.update(appended_heading2_block_id,
                                      BlockExampleData.HEADING2_BLOCK_UPDATE_DATA_EXAMPLE)

    print(f"--- Block Update Result ---\n"
          f"{update_rsp}\n"
          f"--- Block Update Result ---")

    colored_print(f"The block is updated successfully. "
                  f"You can now view the intuitive result by clicking on the following links: "
                  f"https://www.notion.so/{base_page_id.replace('-', '')}",
                  color=PrintStyle.GREEN)

    if not is_continuous:
        press_enter_to_continue()
    ############################
    # Delete the blocks above  #
    ############################
    print_step("Delete the blocks above")
    delete_rsp = client.blocks.delete(appended_paragraph_block_id)
    print(f"--- Paragraph Block Delete Result ---\n"
          f"{delete_rsp}\n"
          f"--- Paragraph Block Delete Result ---")

    delete_rsp = client.blocks.delete(appended_heading2_block_id)
    print(f"--- Heading_2 Block Delete Result ---\n"
          f"{delete_rsp}\n"
          f"--- Heading_2 Block Delete Result ---")

    colored_print(f"The blocks are deleted successfully. "
                  f"You can now view the intuitive result by clicking on the following links: "
                  f"https://www.notion.so/{base_page_id.replace('-', '')}",
                  color=PrintStyle.GREEN)


if __name__ == '__main__':
    run_example_code()
