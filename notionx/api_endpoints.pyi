""" Endpoints definitions """
import typing

from notionx.client import Client
from collections.abc import Awaitable

DictOrAwaitableDict = typing.Union[typing.Dict, Awaitable[typing.Dict]]
OptionalDict = typing.Optional[typing.Dict]


class Endpoint:
    def __init__(self, client: Client):
        self._client = client


__all__ = [
    "Endpoint",
    "PagePropertiesEndpoint",
    "PagesEndpoint",
    "BlockChildrenEndpoint",
    "BlocksEndpoint",
    "DatabasesEndpoint",
    "UsersEndpoint",
    "CommentsEndpoint",
    "SearchEndpoint",
]


class PagePropertiesEndpoint(Endpoint):

    @typing.overload
    def retrieve(
            self,
            page_id: str,
            property_id: str,
            start_cursor: typing.Optional[str] = None,
            page_size: typing.Optional[int] = None
    ) -> DictOrAwaitableDict: ...

    @typing.overload
    def retrieve(
            self,
            page_id: str,
            property_id: str,
            query_data: OptionalDict = None
    ) -> DictOrAwaitableDict: ...


class PagesEndpoint(Endpoint):
    properties: PagePropertiesEndpoint

    def __init__(self, client: Client): ...

    @typing.overload
    def create(
            self,
            body_data: OptionalDict
    ) -> DictOrAwaitableDict: ...

    @typing.overload
    def create(
            self,
            parent: typing.Dict,
            properties: typing.Dict,
            children: typing.Optional[typing.List[typing.Dict]] = None,
            icon: OptionalDict = None,
            cover: OptionalDict = None
    ) -> DictOrAwaitableDict: ...

    @typing.overload
    def retrieve(
            self,
            page_id: str,
            query_data: OptionalDict = None
    ) -> DictOrAwaitableDict: ...

    @typing.overload
    def retrieve(
            self,
            page_id: str,
            filter_properties: typing.Optional[typing.List[str]] = None
    ) -> DictOrAwaitableDict: ...

    @typing.overload
    def update(
            self,
            page_id: str,
            body_data: OptionalDict = None
    ) -> DictOrAwaitableDict: ...

    @typing.overload
    def update(
            self,
            page_id: str,
            properties: OptionalDict = None,
            archived: typing.Optional[bool] = None,
            icon: OptionalDict = None,
            cover: OptionalDict = None
    ) -> DictOrAwaitableDict: ...


class BlockChildrenEndpoint(Endpoint):
    @typing.overload
    def append(
            self,
            block_id: str,
            body_data: OptionalDict
    ) -> DictOrAwaitableDict: ...

    @typing.overload
    def append(
            self,
            block_id: str,
            children: typing.List[typing.Dict]
    ) -> DictOrAwaitableDict: ...

    @typing.overload
    def append(
            self,
            block_id: str,
            children: typing.List[typing.Dict],
            after: str
    ) -> DictOrAwaitableDict: ...

    @typing.overload
    def list(
            self,
            block_id: str,
            query_data: OptionalDict = None
    ) -> DictOrAwaitableDict: ...

    @typing.overload
    def list(
            self,
            block_id: str,
            start_cursor: typing.Optional[str] = None,
            page_size: typing.Optional[int] = None
    ) -> DictOrAwaitableDict: ...


class BlocksEndpoint(Endpoint):
    children: BlockChildrenEndpoint

    def __init__(self, client: Client): ...

    def retrieve(self, block_id: str) -> DictOrAwaitableDict: ...

    @typing.overload
    def update(
            self,
            block_id: str,
            body_data: OptionalDict = None
    ) -> DictOrAwaitableDict: ...

    @typing.overload
    def update(
            self,
            block_id: str,
            embed: OptionalDict = None,
            type: OptionalDict = None,
            bookmark: OptionalDict = None,
            image: OptionalDict = None,
            video: OptionalDict = None,
            pdf: OptionalDict = None,
            file: OptionalDict = None,
            audio: OptionalDict = None,
            code: OptionalDict = None,
            equation: OptionalDict = None,
            divider: OptionalDict = None,
            breadcrumb: OptionalDict = None,
            table_of_contents: OptionalDict = None,
            link_to_page: OptionalDict = None,
            table_row: OptionalDict = None,
            heading_1: OptionalDict = None,
            heading_2: OptionalDict = None,
            heading_3: OptionalDict = None,
            paragraph: OptionalDict = None,
            bulleted_list_item: OptionalDict = None,
            numbered_list_item: OptionalDict = None,
            quote: OptionalDict = None,
            to_do: OptionalDict = None,
            toggle: OptionalDict = None,
            template: OptionalDict = None,
            callout: OptionalDict = None,
            synced_block: OptionalDict = None,
            table: OptionalDict = None,
            archived: typing.Optional[bool] = None
    ) -> DictOrAwaitableDict: ...

    def delete(self, block_id: str) -> DictOrAwaitableDict: ...


class DatabasesEndpoint(Endpoint):
    def retrieve(self, database_id) -> DictOrAwaitableDict: ...

    @typing.overload
    def query(
            self,
            database_id: str,
            body_data: OptionalDict = None
    ) -> DictOrAwaitableDict: ...

    @typing.overload
    def query(
            self,
            database_id: str,
            filter: OptionalDict = None,
            sorts: typing.Optional[typing.List] = None,
            start_cursor: typing.Optional[str] = None,
            page_size: typing.Optional[int] = None
    ) -> DictOrAwaitableDict: ...

    @typing.overload
    def create(self, body_data: OptionalDict) -> DictOrAwaitableDict: ...

    @typing.overload
    def create(
            self,
            parent: typing.Dict,
            properties: typing.Dict,
            title: typing.List[typing.Dict]
    ) -> DictOrAwaitableDict: ...

    @typing.overload
    def update(
            self,
            database_id: str,
            body_data: OptionalDict = None
    ) -> DictOrAwaitableDict: ...

    @typing.overload
    def update(
            self,
            database_id: str,
            title: typing.Optional[typing.List[typing.Dict]] = None,
            properties: OptionalDict = None,
            description: typing.Optional[typing.List[typing.Dict]] = None
    ) -> DictOrAwaitableDict: ...

    @typing.overload
    def list(self, query_data: OptionalDict = None) -> DictOrAwaitableDict: ...

    @typing.overload
    def list(
            self,
            start_cursor: typing.Optional[str] = None,
            page_size: typing.Optional[int] = None
    ) -> DictOrAwaitableDict: ...


class UsersEndpoint(Endpoint):
    def retrieve(self, user_id) -> DictOrAwaitableDict: ...

    @typing.overload
    def list(self, query_data: OptionalDict = None) -> DictOrAwaitableDict: ...

    @typing.overload
    def list(
            self,
            start_cursor: typing.Optional[str] = None,
            page_size: typing.Optional[int] = None
    ) -> DictOrAwaitableDict: ...

    def me(self) -> DictOrAwaitableDict: ...


class CommentsEndpoint(Endpoint):
    @typing.overload
    def list(self, query_data: OptionalDict = None) -> DictOrAwaitableDict: ...

    @typing.overload
    def list(
            self,
            block_id: str,
            start_cursor: typing.Optional[str] = None,
            page_size: typing.Optional[int] = None
    ) -> DictOrAwaitableDict: ...

    @typing.overload
    def create(self, body_data: OptionalDict) -> DictOrAwaitableDict: ...

    @typing.overload
    def create(self, parent: typing.Dict, rich_text: typing.Dict) -> DictOrAwaitableDict: ...

    @typing.overload
    def create(self, discussion_id: str, rich_text: typing.Dict) -> DictOrAwaitableDict: ...


class SearchEndpoint(Endpoint):
    @typing.overload
    def __call__(self, body_data: OptionalDict = None) -> DictOrAwaitableDict: ...

    @typing.overload
    def __call__(
            self,
            query: typing.Optional[str] = None,
            sort: OptionalDict = None,
            filter: OptionalDict = None,
            start_cursor: typing.Optional[str] = None,
            page_size: typing.Optional[int] = None
    ) -> DictOrAwaitableDict: ...
