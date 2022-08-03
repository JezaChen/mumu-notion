""" The notion client definition """

from dataclasses import dataclass
import typing
from typing import Optional, Union

import httpx

from notionx.api_endpoints import PagesEndpoint, BlocksEndpoint, DatabasesEndpoint, UsersEndpoint, \
    CommentsEndpoint, SearchEndpoint

__all__ = ["ClientOptions", "Client"]


@dataclass(frozen=True)
class ClientOptions:
    # `auth_token` is required option
    auth_token: str
    # `notion_version` specifies the API version
    notion_version: str = "2022-06-28"
    base_url = "https://api.notion.com/v1"
    timeout_ms: int = 90_000

    def __init__(self, auth_token: str,
                 notion_version: typing.Optional[str] = None,
                 base_url: typing.Optional[str] = None,
                 timeout_ms: typing.Optional[int] = None): ...


class Client:
    __http_client: httpx.Client
    options: ClientOptions
    pages: PagesEndpoint
    blocks: BlocksEndpoint
    databases: DatabasesEndpoint
    users: UsersEndpoint
    comments: CommentsEndpoint
    search: SearchEndpoint

    def __init__(
            self,
            options: Optional[Union[ClientOptions, typing.Dict]] = None,
            **kwargs: typing.Any
    ): ...

    def _make_request(self, method: str, path: str, query: dict, body: dict) -> httpx.Request: ...

    def _parse_response(self, rsp: httpx.Response) -> dict: ...

    def request(self,
                method: str,
                path: str,
                query: Optional[dict] = None,
                body: Optional[dict] = None) -> dict: ...

    def get(self, path: str, query: Optional[dict] = None, body: Optional[dict] = None) -> dict: ...

    def post(self, path: str, query: Optional[dict] = None, body: Optional[dict] = None) -> dict: ...

    def patch(self, path: str, query: Optional[dict] = None, body: Optional[dict] = None) -> dict: ...

    def delete(self, path: str, query: Optional[dict] = None, body: Optional[dict] = None) -> dict: ...
