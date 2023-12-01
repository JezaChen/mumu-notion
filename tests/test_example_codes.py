import inspect
import os
import unittest.mock
import pytest
import importlib

from tests.constants import NOTION_AUTH_TOKEN_KEY, NOTION_BASE_PAGE_ID_KEY
from tests.helpers import keep_notion_environment_variables

_endpoints = ('blocks', 'pages', 'users', 'comments', 'databases', 'search')


def _test_endpoint_example_code(endpoint_example_code, is_continuous):
    assert callable(endpoint_example_code)
    endpoint_example_code(is_continuous=is_continuous)


async def _test_endpoint_example_code_async(endpoint_example_code, is_continuous):
    assert callable(endpoint_example_code) and inspect.iscoroutinefunction(endpoint_example_code)
    await endpoint_example_code(is_continuous=is_continuous)


def _assert_example_code_environment_variables():
    assert os.getenv(NOTION_AUTH_TOKEN_KEY) is not None
    assert os.getenv(NOTION_BASE_PAGE_ID_KEY) is not None


def _delete_example_code_environment_variables():
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


def _import_example_code(example_module_name: str, example_func_name: str):
    example_pkg = importlib.import_module(f"examples.{example_module_name}")
    example_code = getattr(example_pkg, example_func_name)
    return example_code


def test_example_codes_continuously():
    """ The test will not be interrupted by the input,
    the token and base page id will be filled automatically using environment variables.
    """
    _assert_example_code_environment_variables()

    example_codes = (
        _import_example_code(f'official_guides.working_with_{endpoint}', 'run_example_code')
        for endpoint in _endpoints
    )

    for example_code in example_codes:
        _test_endpoint_example_code(example_code,
                                    is_continuous=True)


@pytest.mark.asyncio
async def test_example_async_codes_continuously():
    """ The test will not be interrupted by the input,
    the token and base page id will be filled automatically using environment variables.
    """
    _assert_example_code_environment_variables()

    example_codes = (
        _import_example_code(f'official_guides_async.working_with_{endpoint}', 'run_example_code')
        for endpoint in _endpoints
    )

    for example_code in example_codes:
        await _test_endpoint_example_code_async(example_code,
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
    """ The test is interrupted by the input,
    and the test will automatically enter the corresponding string to make the test continue.
    """
    _assert_example_code_environment_variables()

    with keep_notion_environment_variables() as (auth_token, base_page_id):
        with unittest.mock.patch("builtins.input") as m:
            _delete_example_code_environment_variables()

            example_codes = (
                _import_example_code(f'official_guides.working_with_{endpoint}', 'run_example_code')
                for endpoint in _endpoints
            )

            for example_code in example_codes:
                # mock the input
                m.side_effect = example_code_input_generator(auth_token,
                                                             base_page_id)
                _test_endpoint_example_code(example_code,
                                            is_continuous=False)


@pytest.mark.asyncio
async def test_example_async_codes_discontinuously(monkeypatch):
    """ The test is interrupted by the input,
    and the test will automatically enter the corresponding string to make the test continue.
    """
    _assert_example_code_environment_variables()

    with keep_notion_environment_variables() as (auth_token, base_page_id):
        with unittest.mock.patch("builtins.input") as m:
            _delete_example_code_environment_variables()

            example_codes = (
                _import_example_code(f'official_guides_async.working_with_{endpoint}', 'run_example_code')
                for endpoint in _endpoints
            )

            for example_code in example_codes:
                # mock the input
                m.side_effect = example_code_input_generator(auth_token,
                                                             base_page_id)
                await _test_endpoint_example_code_async(example_code,
                                                        is_continuous=False)
