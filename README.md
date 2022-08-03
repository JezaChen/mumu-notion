<h1 align="center">MuMu-Notion</h1>

<div align="center">

[![codecov](https://codecov.io/gh/JezaChen/mumu-notion/branch/master/graph/badge.svg?token=QKE5Z5JS04)](https://codecov.io/gh/JezaChen/mumu-notion)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/mumu-notion?style=flat-square)
![GitHub](https://img.shields.io/github/license/jezachen/mumu-notion)

[中文文档](https://github.com/JezaChen/mumu-notion/blob/master/README_zh.md)

</div>

`NotionX`, a simple and easy-to-use Notion client, is based on the official SDK modification.

## Implemented features

- Latest Notion API support: The code uses the `2022-06-28` version of Notion.
- Complete API coverage: all methods of the official Notion API documentation (https://developers.notion.com/reference/)
  have been wrapped.
- Simple request validation: locally verifies whether the user's request is legal, currently supports key validation of
  the outermost parameters (e.g., whether the parameters provided by the user are complete, whether there are parameters
  not included in the API documentation), while value validation and nested parameter validation are still under
  development.
- Synchronous Client request, which uses `httpx` for synchronous HTTP requests, asynchronous request feature is under
  development.
- Complete code examples covering 100% of the client methods and over 90% of the code.
- Complete tests, covering 98%+ of the client code.

## Requirements

- Python >= 3.7
- httpx >= 0.23.0

## Installation

Just install it using pip.

```shell
pip install notionx
```

## Usage

Before using NotionX, you need to create an _integration token_, and share at least one page with that integration.

- How to create an integration: https://www.notion.so/my-integrations/
- Notion's official tutorial on creating and sharing pages with an
  integration: https://developers.notion.com/docs/getting-started

### Client initialization

To initialize Notion Client by passing in a dictionary (**dictionary parameter style**) containing `auth_token` (the
token of the above integration, starting with `secret_`).

```Python
from notionx import Client

client = Client({
    "auth_token": "your_integration_token"
})
```

There is another way to initialize, passed in **keyword parameter style**.

```Python
from notionx import Client

client = Client(
  auth_token="your_integration_token"
)
```

The dictionary parameter style and the keyword parameter style also apply to the methods of the client, and we
will give the invocation of each style later.

> 💡 Note!!!
>
> To avoid leaks of the integration token, we do not recommend hard-coding the token explicitly in your source code. It
> is better to
> write it to the environment variables and then initialize the client by
> ```Python
> import os
> from notionx import Client
>
> token = os.getenv("NOTION_AUTH_TOKEN")
> client = Client(
> auth_token=token
> )
> ```

In addition to `auth_token`, `Client` has several **optional** initialization parameters, whose names and meanings are
shown in the following table.

|  parameter name  | type  |         default value         |                                description                                |
|:----------------:|-------|:-----------------------------:|:-------------------------------------------------------------------------:|
|   `auth_token`   | `str` |     **no default value**      |                             Integration Token                             |
| `notion_version` | `str` |        `"2022-06-28"`         |                             Notion's version                              |
|    `base_url`    | `str` | `"https://api.notion.com/v1"` |                   The root URL for sending API requests                   |
|   `timeout_ms`   | `int` |           `90_000`            | The number of milliseconds to wait before issuing a `RequestTimeoutError` |

### How-tos

See [our wikis](https://github.com/JezaChen/mumu-notion/wiki/How-tos) for details.

## Code Examples

We provide code examples that cover all methods of the client and the data is taken from Notion's official
documentation.

See also: https://github.com/JezaChen/mumu-notion/tree/master/examples/official_guides