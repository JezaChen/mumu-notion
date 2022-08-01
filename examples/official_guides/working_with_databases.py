""" Interactive API sample code for interacting with databases """

from examples.official_guides.common_prelude import get_client_and_base_page_id
from examples.official_guides.data import DatabaseExampleData
from examples.utils import colored_print, PrintStyle, generate_multiple_random_pages_for_database, \
    generate_step_printer, press_enter_to_continue

__all__ = [
    "run_example_code",
]


def run_example_code(is_continuous=False):
    print_step = generate_step_printer()

    client, base_page_id = get_client_and_base_page_id()

    ######################################################
    # Create two databases as children of the page given #
    ######################################################
    print_step("Try to create two databases `Meal List` and `Grocery List` as two children of your empty child...")
    meal_database_create_body_data = DatabaseExampleData.MEAL_CREATE_EXAMPLE.copy()
    meal_database_create_body_data["parent"]["page_id"] = base_page_id

    meal_database_create_rsp = client.databases.create(meal_database_create_body_data)
    print(f"--- Meal Database Create Result ---\n"
          f"{meal_database_create_rsp}\n"
          f"--- Meal Database Result ---")

    grocery_database_create_body_data = DatabaseExampleData.GROCERY_CREATE_EXAMPLE.copy()
    grocery_database_create_body_data["parent"]["page_id"] = base_page_id
    grocery_database_create_body_data["properties"]["Meals"]["relation"]["database_id"] = meal_database_create_rsp["id"]

    grocery_database_create_rsp = client.databases.create(grocery_database_create_body_data)
    print(f"--- Grocery Database Create Result ---\n"
          f"{meal_database_create_rsp}\n"
          f"--- Grocery Database Result ---")

    meal_database_id: str = meal_database_create_rsp["id"]
    grocery_database_id: str = grocery_database_create_rsp["id"]

    colored_print(f"You can now view the two newly created databases by clicking on the following links:\n"
                  f"Meal Database: https://www.notion.so/{meal_database_id.replace('-', '')}\n"
                  f"Grocery Database: https://www.notion.so/{grocery_database_id.replace('-', '')}",
                  color=PrintStyle.GREEN)

    if not is_continuous:
        press_enter_to_continue()

    ##########################################################
    # Retrieve the information of the database `Grocery List`#
    ##########################################################
    print_step("Try to retrieve the information of the database `Grocery List`...")
    grocery_database_retrieve_rsp = client.databases.retrieve(grocery_database_id)
    print(f"--- Retrieve Result ---\n"
          f"{grocery_database_retrieve_rsp}\n"
          f"--- Retrieve Result ---")

    if not is_continuous:
        press_enter_to_continue()
    ##################################################################
    # Generate 30 random pages and add to the database `Grocery List`#
    ##################################################################

    print_step("Generate 30 random pages and add to the database `Grocery List`")
    example_data_list = generate_multiple_random_pages_for_database(
        grocery_database_retrieve_rsp,
        30
    )

    for example_data in example_data_list:
        client.pages.create(example_data)

    colored_print(f"The data is added successfully. "
                  f"You can now view the intuitive result by clicking on the following links: https://www.notion.so/{grocery_database_id.replace('-', '')}",
                  color=PrintStyle.GREEN)

    if not is_continuous:
        press_enter_to_continue()
    #########################################################################
    # Query the database `Grocery List` for the page with the name `Mango` #
    #########################################################################

    print_step("Query the database `Grocery List` for the page with the name `Mango`")
    search_rsp = client.databases.query(grocery_database_id,
                                        {
                                            "filter": {
                                                "property": "Name",
                                                "title": {"equals": "Mango"}
                                            }
                                        })

    print(f"--- Search Result ---\n"
          f"{search_rsp}\n"
          f"--- Search Result ---")

    if not is_continuous:
        press_enter_to_continue()

    ################################################
    # Change the icon of these pages from 🥬 to 🥭 #
    ################################################
    print_step("Change the icon of these pages from 🥬 to 🥭")

    for page_info in search_rsp["results"]:
        page_id = page_info["id"]
        client.pages.update(page_id,
                            {
                                'icon': {'type': 'emoji', 'emoji': '🥭'}
                            })
    colored_print(f"The icons of these pages are changed to 🥭 successfully. "
                  f"You can now view the intuitive result by clicking on the following links: "
                  f"https://www.notion.so/{grocery_database_id.replace('-', '')}",
                  color=PrintStyle.GREEN)

    if not is_continuous:
        press_enter_to_continue()

    ######################################
    # Retrieve the `Description` property #
    ######################################
    print_step("Retrieve the `Description` property of these pages")
    for page_info in search_rsp["results"]:
        page_id = page_info["id"]
        prop_id = page_info["properties"]["Description"]["id"]
        prop_retrieve_rsp = client.pages.properties.retrieve(page_id,
                                                             prop_id)
        print(f"--- Property `Description` Retrieve Result for Page {page_id} ---\n"
              f"{prop_retrieve_rsp}\n"
              f"--- Property `Description` Retrieve Result for Page {page_id} ---")

    if not is_continuous:
        press_enter_to_continue()
    ###############################################################
    # Update the `Description` property of these pages to all-caps #
    ###############################################################

    print_step("Update the `Description` property of these pages to all-caps")
    for page_info in search_rsp["results"]:
        page_id = page_info["id"]
        prop_id = page_info["properties"]["Description"]["id"]
        prop_retrieve_rsp = client.pages.properties.retrieve(page_id,
                                                             prop_id)
        old_description: str = prop_retrieve_rsp["results"][0]["rich_text"]["plain_text"]
        new_description = old_description.upper()
        prop_update_rsp = client.pages.update(page_id,
                                              {
                                                  "properties": {
                                                      "Description": {
                                                          "rich_text": [
                                                              {
                                                                  "type": "text",
                                                                  "text": {"content": new_description}
                                                              }
                                                          ]
                                                      }
                                                  }
                                              })
        print(f"--- Property `Description` Update Result for Page {page_id} ---\n"
              f"{prop_update_rsp}\n"
              f"--- Property `Description` Update Result for Page {page_id} ---")

    colored_print(f"The `Description` property of these pages are changed to all-caps successfully. "
                  f"You can now view the intuitive result by clicking on the following links: "
                  f"https://www.notion.so/{grocery_database_id.replace('-', '')}",
                  color=PrintStyle.GREEN)

    if not is_continuous:
        press_enter_to_continue()
    ##############################################
    # Retrieve the updated `Description` property #
    ##############################################

    print_step("Retrieve the updated `Description` property of these pages")
    for page_info in search_rsp["results"]:
        page_id = page_info["id"]
        prop_id = page_info["properties"]["Description"]["id"]
        prop_retrieve_rsp = client.pages.properties.retrieve(page_id,
                                                             prop_id)
        print(f"--- Updated Property `Description` Retrieve Result for Page {page_id} ---\n"
              f"{prop_retrieve_rsp}\n"
              f"--- Updated Property `Description` Retrieve Result for Page {page_id} ---")

    if not is_continuous:
        press_enter_to_continue()
    #########################
    # Update the page above #
    #########################
    print_step("Update the database `Grocery List`")
    database_update_rsp = client.databases.update(grocery_database_id, DatabaseExampleData.GROCERY_UPDATE_EXAMPLE)

    print(f"--- Database Update Result ---\n"
          f"{database_update_rsp}\n"
          f"--- Database Update Result ---")

    colored_print(f"The database `Grocery List` is updated successfully. "
                  f"You can now view the intuitive result by clicking on the following links: "
                  f"https://www.notion.so/{grocery_database_id.replace('-', '')}",
                  color=PrintStyle.GREEN)

    if not is_continuous:
        press_enter_to_continue()
    ###########################
    # Delete these page above #
    ###########################
    print_step("Delete these page above")

    for page_info in search_rsp["results"]:
        page_id = page_info["id"]
        client.blocks.delete(page_id)

    colored_print(f"These pages are deleted successfully. "
                  f"You can now view the intuitive result by clicking on the following links: "
                  f"https://www.notion.so/{grocery_database_id.replace('-', '')}",
                  color=PrintStyle.GREEN)

    if not is_continuous:
        press_enter_to_continue()
    ##############################
    # Delete the entire database #
    ##############################

    print_step("Delete the entire database")
    client.blocks.delete(grocery_database_id)
    client.blocks.delete(meal_database_id)

    colored_print(f"The example databases are deleted successfully. "
                  f"You can now view the intuitive result by backing to your test page: "
                  f"https://www.notion.so/{base_page_id}",
                  color=PrintStyle.GREEN)

    # if not is_continuous:
    #     press_enter_to_continue()
    #
    # ###################################
    # # List the databases (deprecated) #
    # ###################################
    # print_step("List the databases (deprecated)")
    # old_version_client = Client(
    #     {
    #         "auth_token": client.options.auth_token,
    #         "notion_version": "2021-08-16"
    #     }
    # )
    # client.databases.list()


if __name__ == '__main__':
    run_example_code()
