import os

import pytest

from notionx import LocalValidationError
from tests.constants import NOTION_BASE_PAGE_ID_KEY
from tests.helpers import get_client, get_base_page_id
from notionx.validation_tools import validate_dict_parameter


def test_one_of_validator():
    """ Currently only the creation of comments uses the `One-of` Validator
    - If more than one of these arguments is given, raise
    - If none of them is given, raise
    - If one of them is given, pass
    """
    client = get_client()

    # params-as-a-dict version
    # two given
    with pytest.raises(LocalValidationError, match="The dict contains more than one key in specified key list.*"):
        client.comments.create({
            "rich_text": [
                {"text": {"content": "This is a test."}}
            ],
            "discussion_id": "not_important_discussion_id",
            "parent": "not_important_parent_id"
        })

    # none given
    with pytest.raises(LocalValidationError, match="The dict does not contain any key in specified key list.*"):
        client.comments.create({
            "rich_text": [
                {"text": {"content": "This is a test."}}
            ],
        })

    # keyword params version
    with pytest.raises(LocalValidationError, match="The dict contains more than one key in specified key list.*"):
        client.comments.create(
            rich_text=[
                {"text": {"content": "This is a test."}}
            ],
            discussion_id="not_important_discussion_id",
            parent="not_important_parent_id"
        )

    with pytest.raises(LocalValidationError, match="The dict does not contain any key in specified key list.*"):
        client.comments.create(
            rich_text=[
                {"text": {"content": "This is a test."}}
            ]
        )

    # pass
    assert os.getenv(NOTION_BASE_PAGE_ID_KEY) is not None
    base_page_id = os.getenv(NOTION_BASE_PAGE_ID_KEY)

    # keyword params version
    client.comments.create(
        rich_text=[
            {"text": {"content": "This is a test."}}
        ],
        parent={
            "page_id": base_page_id
        }
    )

    # params-as-a-dict version
    client.comments.create(
        {
            "rich_text": [
                {"text": {"content": "This is a test."}}
            ],
            "parent": {
                "page_id": base_page_id
            }
        }
    )


def test_dict_param_validator_when_giving_excluded_params():
    """ Provide parameters that are not included in the limited scope """
    # params-as-a-dict version
    client, base_page_id = get_client(), get_base_page_id()
    with pytest.raises(LocalValidationError,
                       match="The key .* contained in the parameter .* is invalid."):
        client.pages.create(
            {
                "parent": {
                    "type": "page_id",  # The default parent is page
                    "page_id": ""  # Need to fill
                },
                "properties": {
                    "title": [
                        {
                            "text": {
                                "content": "Tuscan kale"
                            }
                        }
                    ]
                },
                "invalid_key": "invalid_value"
            }
        )

    # keyword params version
    with pytest.raises(LocalValidationError,
                       match="The key .* contained in the parameter .* is invalid."):
        client.pages.create(
            parent={
                "type": "page_id",  # The default parent is page
                "page_id": ""  # Need to fill
            },
            properties={
                "title": [
                    {
                        "text": {
                            "content": "Tuscan kale"
                        }
                    }
                ]
            },
            invalid_key="invalid_value"
        )


def test_dict_param_validator_when_missing_required_params():
    """ Using client page create API """
    client, base_page_id = get_client(), get_base_page_id()
    # lack `parent`
    # params-as-a-dict version
    with pytest.raises(LocalValidationError,
                       match="The parameter `.*` is missing the required key `.*`."):
        client.pages.create(
            {
                "properties": {
                    "title": [
                        {
                            "text": {
                                "content": "Tuscan kale"
                            }
                        }
                    ]
                }
            }
        )

    # keyword params version
    with pytest.raises(LocalValidationError,
                       match="The parameter `.*` is missing the required key `.*`."):
        client.pages.create(
            properties={
                "title": [
                    {
                        "text": {
                            "content": "Tuscan kale"
                        }
                    }
                ]
            }
        )


def test_validation_decorator():
    """ Test if the check decorator throws an exception as expected.
        - The specified dict_param_name parameter does not exist in the signature of the decorated function
        - required_key is of incorrect type
    """
    with pytest.raises(TypeError, match="The decorated function must have the `.*` parameter."):
        @validate_dict_parameter("not_existing_param", ("a", "b"))
        def func(param_dict: dict): ...

    with pytest.raises(TypeError, match="Unexpected type of .*"):
        @validate_dict_parameter("param_dict", ("a", "b"), (1,))
        def func(param_dict: dict): ...

        func({})

    with pytest.raises(LocalValidationError,
                       match="The parameter `.*` must be a dict."):
        @validate_dict_parameter("param_dict", ("a", "b"))
        def func(param_dict: dict): ...

        func(2)
