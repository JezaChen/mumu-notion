""" Interactive API sample code for interacting with users """

from examples.official_guides_async.common_prelude import get_client
from examples.utils import generate_step_printer, press_enter_to_continue

__all__ = [
    "run_example_code",
]


async def run_example_code(is_continuous=False):
    print_step = generate_step_printer()

    client = get_client()

    ###########################
    # Retrieve my information #
    ###########################

    print_step("Retrieve my information")

    my_info_rsp = await client.users.me()
    print(f"--- My Information Result ---\n"
          f"{my_info_rsp}\n"
          f"--- My Information Result ---")

    my_uid = my_info_rsp["id"]

    if not is_continuous:
        press_enter_to_continue()
    ####################################
    # Retrieve the information of user #
    ####################################

    print_step(f"Retrieve the information of user {my_uid}")
    user_retrieve_rsp = await client.users.retrieve(my_uid)

    print(f"--- User Retrieve Result ---\n"
          f"{user_retrieve_rsp}\n"
          f"--- User Retrieve Result ---")

    if not is_continuous:
        press_enter_to_continue()
    ##################
    # List all users #
    ##################

    print_step(f"List all users")
    list_result = await client.users.list()

    print(f"--- User List Result ---\n"
          f"{list_result}\n"
          f"--- User List Result ---")


if __name__ == '__main__':
    run_example_code()
