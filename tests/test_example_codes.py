import os
import unittest.mock
from unittest import mock

import pytest

NOTION_AUTH_TOKEN_KEY = "NOTION_AUTH_TOKEN"
NOTION_BASE_PAGE_ID_KEY = "NOTION_BASE_PAGE_ID"


def _test_endpoint_example_code(endpoint_example_code, is_continuous):
    assert callable(endpoint_example_code)
    endpoint_example_code(is_continuous=is_continuous)


def test_example_codes_continuously():
    assert os.getenv(NOTION_AUTH_TOKEN_KEY) is not None
    assert os.getenv(NOTION_BASE_PAGE_ID_KEY) is not None

    from examples.official_guides.working_with_blocks import run_example_code as blocks_endpoint_example
    from examples.official_guides.working_with_pages import run_example_code as pages_endpoint_example
    from examples.official_guides.working_with_users import run_example_code as users_endpoint_example
    from examples.official_guides.working_with_comments import run_example_code as comments_endpoint_example
    from examples.official_guides.working_with_databases import run_example_code as databases_endpoint_example

    for example_code in (blocks_endpoint_example,
                         pages_endpoint_example,
                         users_endpoint_example,
                         comments_endpoint_example,
                         databases_endpoint_example,
                         ):
        _test_endpoint_example_code(example_code,
                                    is_continuous=True)


def example_code_input_generator(auth_token: str,
                                 base_page_id: str):
    """ A generator to mock input
    1. returns NOTION_AUTH_TOKEN
    2. returns NOTION_BASE_PAGE_ID
    3... always returns \n
    """
    yield auth_token
    yield base_page_id

    while True:
        yield '\n'


def test_example_codes_discontinuously(monkeypatch):
    assert os.getenv(NOTION_AUTH_TOKEN_KEY) is not None
    assert os.getenv(NOTION_BASE_PAGE_ID_KEY) is not None

    auth_token = os.getenv(NOTION_AUTH_TOKEN_KEY)
    base_page_id = os.getenv(NOTION_BASE_PAGE_ID_KEY)

    with unittest.mock.patch("builtins.input") as m:
        # In order to get the test to the input code block for token and base page id,
        # the environment variables need to be removed
        os.unsetenv(NOTION_AUTH_TOKEN_KEY)
        os.unsetenv(NOTION_BASE_PAGE_ID_KEY)

        # The correct way to remove the environment variables of Linux
        # https://stackoverflow.com/questions/3575165/what-is-the-correct-way-to-unset-a-linux-environment-variable-in-python
        if os.getenv(NOTION_AUTH_TOKEN_KEY) is not None or os.getenv(NOTION_BASE_PAGE_ID_KEY) is not None:
            del os.environ[NOTION_AUTH_TOKEN_KEY]
            del os.environ[NOTION_BASE_PAGE_ID_KEY]

        assert os.getenv(NOTION_AUTH_TOKEN_KEY) is None
        assert os.getenv(NOTION_BASE_PAGE_ID_KEY) is None

        from examples.official_guides.working_with_blocks import run_example_code as blocks_endpoint_example
        from examples.official_guides.working_with_pages import run_example_code as pages_endpoint_example
        from examples.official_guides.working_with_users import run_example_code as users_endpoint_example
        from examples.official_guides.working_with_comments import run_example_code as comments_endpoint_example
        from examples.official_guides.working_with_databases import run_example_code as databases_endpoint_example

        for example_code in (blocks_endpoint_example,
                             pages_endpoint_example,
                             users_endpoint_example,
                             comments_endpoint_example,
                             databases_endpoint_example,
                             ):
            m.side_effect = example_code_input_generator(auth_token,
                                                         base_page_id)
            _test_endpoint_example_code(example_code,
                                        is_continuous=False)

    # restore the environment variables
    os.putenv(NOTION_AUTH_TOKEN_KEY, auth_token)
    os.putenv(NOTION_BASE_PAGE_ID_KEY, base_page_id)
