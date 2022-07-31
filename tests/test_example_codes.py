import os


def _test_endpoint_example_code(endpoint_example_code):
    assert callable(endpoint_example_code)
    endpoint_example_code(is_continuous=True)


def test_example_codes():
    assert os.getenv("NOTION_AUTH_TOKEN") is not None
    assert os.getenv("NOTION_BASE_PAGE_ID") is not None

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
        _test_endpoint_example_code(example_code)
