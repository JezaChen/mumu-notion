""" Utilities for creating random data """

import random
import typing
from datetime import datetime

__all__ = [
    "generate_a_random_page_item_for_database",
    "generate_multiple_random_pages_for_database"
]

RANDOM = object()

NOUNS = ('Banana', 'Apple', 'Orange', 'Lemon', 'Lime',
         'Strawberry', 'Kiwi', 'Peach', 'Grape', 'Pineapple', 'Mango')
VERBS = ("taste", "eat", "drink", "smell", "feel")
ADV = ("mildly.", "slightly.", "a bit.", "a lot.", "very.", "extremely.")
ADJ = ("delicious", "tasty", "yummy", "delightful", "good", "great", "amazing", "fantastic", "fabulous", "marvelous",
       "wonderful")

_MAPPING_PROP_TYPE_TO_RANDOM_GENERATOR = {}


def _register_random_generator(prop):
    def decorator(func):
        _MAPPING_PROP_TYPE_TO_RANDOM_GENERATOR[prop] = func

        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    return decorator


def _generate_random_sentence() -> str:
    return ' '.join([random.choice(i) for i in [NOUNS, VERBS, ADJ, ADV]])


@_register_random_generator("title")
def _generate_random_title_prop(prop_info) -> dict:
    return {
        "title": [
            {
                "text": {
                    "content": random.choice(NOUNS)
                }
            }
        ]
    }


@_register_random_generator("checkbox")
def _generate_random_checkbox_prop(prop_info) -> dict:
    return {
        "checkbox": random.choice((True, False))
    }


@_register_random_generator("date")
def _generate_random_date_prop(prop_info) -> dict:
    return {
        "date": {
            "start": datetime.now().isoformat()
        }
    }


@_register_random_generator("number")
def _generate_random_number_prop(prop_info) -> dict:
    return {
        "number": random.randint(0, 100)
    }


@_register_random_generator("select")
def _generate_random_select_prop(prop_info: dict) -> dict:
    return {
        "select": {
            "name": random.choice([
                option["name"] for option in prop_info["select"]["options"]
            ])
        }
    }


@_register_random_generator("multi_select")
def _generate_random_multi_select_prop(prop_info) -> dict:
    choices = [option["name"] for option in prop_info["multi_select"]["options"]]
    return_size = random.randint(1, len(choices))
    return {
        "multi_select":
            [
                {
                    "name": name
                }
                for name in random.sample(choices, return_size)
            ]

    }


@_register_random_generator("rich_text")
def _generate_random_rich_text_prop(prop_info: dict) -> typing.Dict[str, list]:
    return {
        "rich_text": [
            {
                "text": {
                    "content": _generate_random_sentence()
                }
            }
        ]
    }


def _dispatch_random_generator(prop_type: str, prop_info: dict) -> dict:
    return _MAPPING_PROP_TYPE_TO_RANDOM_GENERATOR[prop_type](prop_info)


def generate_a_random_page_item_for_database(database_data: dict,
                                             cover_data: typing.Union[dict, object] = RANDOM,
                                             icon_data: typing.Union[dict, object] = RANDOM,
                                             children_data: typing.Optional[typing.List[dict]] = None):
    if "id" not in database_data:
        raise ValueError("The field id is not found in database_data. "
                         "Please use the data which is returned by server.")
    database_id = database_data["id"]

    new_page = {
        "parent": {
            "type": "database_id",
            "database_id": database_id
        }
    }
    if cover_data is not RANDOM:
        new_page["cover"] = cover_data
    else:  # use official example
        new_page["cover"] = {
            "type": "external",
            "external": {
                "url": "https://upload.wikimedia.org/wikipedia/commons/6/62/Tuscankale.jpg"
            }
        }

    if icon_data is not RANDOM:
        new_page["icon"] = cover_data
    else:
        new_page["icon"] = {
            "type": "emoji",
            "emoji": "🥬"
        }

    if children_data is not None:
        new_page["children"] = children_data

    props_dict: dict = database_data["properties"]
    new_page["properties"] = {}

    for prop_name, prop_info in props_dict.items():
        prop_type = prop_info["type"]
        try:
            new_page["properties"][prop_name] = _dispatch_random_generator(prop_type, prop_info)
        except KeyError:
            pass

    return new_page


def generate_multiple_random_pages_for_database(database_data: dict,
                                                page_num: int) -> typing.List[dict]:
    return [
        generate_a_random_page_item_for_database(database_data)
        for _ in range(page_num)
    ]
