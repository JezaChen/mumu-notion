""" The fetcher collections for testing. """


def get_prop_id_from_database_data(db_data: dict, prop_name: str):
    return db_data["properties"][prop_name]["id"]
