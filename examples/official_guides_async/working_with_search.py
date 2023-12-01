""" Interactive API sample code for interacting with search """
import asyncio

from examples.official_guides_async.common_prelude import get_client
from examples.utils import generate_step_printer

__all__ = [
    "run_example_code",
]


async def run_example_code(is_continuous=False):
    print_step = generate_step_printer()

    client = get_client()

    ###################
    # A simple search #
    ###################
    print_step("A simple search")

    search_rsp = await client.search({
        "filter": {
            # Currently, the only property you can filter by is the object type. Possible values include object.
            "property": "object",
            # Possible values for object type include page or database.
            "value": "page"
        }
    })
    print(f"--- Search Result ---\n"
          f"{search_rsp}\n"
          f"--- Search Result ---")


if __name__ == '__main__':
    asyncio.run(run_example_code())
