""" The notion client definition """
import functools
import json
from dataclasses import dataclass
import typing
from typing import Optional, Union

import httpx

from notionx.api_endpoints import PagesEndpoint, BlocksEndpoint, DatabasesEndpoint, UsersEndpoint, \
    CommentsEndpoint, SearchEndpoint
from notionx.errors import raise_api_response_exception_by_err_code, UnknownAPIResponseError

__all__ = ["ClientOptions", "Client"]


@dataclass(frozen=True)
class ClientOptions:
    # `auth_token` is required option
    auth_token: str
    # `notion_version` specifies the API version
    notion_version: str = "2022-06-28"
    base_url = "https://api.notion.com/v1"
    timeout_ms: int = 90_000


class Client:
    __http_client: httpx.Client

    def __init__(
            self,
            options: Optional[Union[ClientOptions, typing.Dict]] = None,
            **kwargs: typing.Any
    ):
        if options is None:
            options = ClientOptions(**kwargs)
        elif isinstance(options, dict):
            options = ClientOptions(**options)
        self.options = options

        self.__http_client = httpx.Client(
            base_url=self.options.base_url,
            headers={
                "Authorization": f"Bearer {self.options.auth_token}",
                "Notion-Version": self.options.notion_version
            },
            timeout=httpx.Timeout(self.options.timeout_ms / 1_000)
        )

        self.pages = PagesEndpoint(self)
        self.blocks = BlocksEndpoint(self)
        self.databases = DatabasesEndpoint(self)
        self.users = UsersEndpoint(self)
        self.comments = CommentsEndpoint(self)
        self.search = SearchEndpoint(self)

    def _make_request(self, method: str, path: str, query: dict, body: dict):
        return self.__http_client.build_request(method, path, params=query, json=body)

    def _parse_response(self, rsp: httpx.Response):
        try:
            rsp.raise_for_status()
        except httpx.HTTPStatusError as err:
            try:
                body = err.response.json()
                err_code = body.get("code")
                err_detail = body.get("message", "")
            except json.JSONDecodeError:
                err_code = None
                err_detail = "The error object is not a valid json object."

            if err_code is not None:
                raise_api_response_exception_by_err_code(
                    err_code,
                    err_detail
                )
            else:
                raise UnknownAPIResponseError(err_detail)

        ret = rsp.json()
        return ret

    def request(self,
                method: str,
                path: str,
                query: Optional[dict] = None,
                body: Optional[dict] = None):
        req = self._make_request(method, path, query, body)
        rsp = self.__http_client.send(req)
        return self._parse_response(rsp)

    # Specific Request Methods
    get = functools.partialmethod(request, "get")
    post = functools.partialmethod(request, "post")
    patch = functools.partialmethod(request, "patch")
    delete = functools.partialmethod(request, "delete")
