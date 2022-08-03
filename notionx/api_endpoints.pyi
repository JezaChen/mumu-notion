""" Endpoints definitions """
import typing

from notionx.client import Client


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
    ) -> dict: ...

    @typing.overload
    def retrieve(
            self,
            page_id: str,
            property_id: str,
            query_data: typing.Optional[typing.Dict] = None
    ) -> dict: ...


class PagesEndpoint(Endpoint):
    properties: PagePropertiesEndpoint

    def __init__(self, client: Client): ...

    @typing.overload
    def create(
            self,
            body_data: typing.Optional[typing.Dict]
    ) -> dict: ...

    @typing.overload
    def create(
            self,
            parent: typing.Dict,
            properties: typing.Dict,
            children: typing.Optional[typing.List[typing.Dict]] = None,
            icon: typing.Optional[typing.Dict] = None,
            cover: typing.Optional[typing.Dict] = None
    ) -> dict: ...

    def retrieve(self, page_id: str) -> dict: ...

    @typing.overload
    def update(
            self,
            page_id: str,
            body_data: typing.Optional[typing.Dict] = None
    ) -> dict: ...

    @typing.overload
    def update(
            self,
            page_id: str,
            properties: typing.Optional[typing.Dict] = None,
            archived: typing.Optional[bool] = None,
            icon: typing.Optional[typing.Dict] = None,
            cover: typing.Optional[typing.Dict] = None
    ) -> dict: ...


class BlockChildrenEndpoint(Endpoint):
    @typing.overload
    def append(
            self,
            block_id: str,
            body_data: typing.Optional[typing.Dict]
    ) -> dict: ...

    @typing.overload
    def append(
            self,
            block_id: str,
            children: typing.List[typing.Dict]
    ) -> dict: ...

    @typing.overload
    def list(
            self,
            block_id: str,
            query_data: typing.Optional[typing.Dict] = None
    ) -> dict: ...

    @typing.overload
    def list(
            self,
            block_id: str,
            start_cursor: typing.Optional[str] = None,
            page_size: typing.Optional[int] = None
    ) -> dict: ...


class BlocksEndpoint(Endpoint):
    children: BlockChildrenEndpoint

    def __init__(self, client: Client): ...

    def retrieve(self, block_id: str) -> dict: ...

    @typing.overload
    def update(
            self,
            block_id: str,
            body_data: typing.Optional[typing.Dict] = None
    ) -> dict: ...

    @typing.overload
    def update(
            self,
            block_id: str,
            embed: typing.Optional[typing.Dict] = None,
            type: typing.Optional[typing.Dict] = None,
            bookmark: typing.Optional[typing.Dict] = None,
            image: typing.Optional[typing.Dict] = None,
            video: typing.Optional[typing.Dict] = None,
            pdf: typing.Optional[typing.Dict] = None,
            file: typing.Optional[typing.Dict] = None,
            audio: typing.Optional[typing.Dict] = None,
            code: typing.Optional[typing.Dict] = None,
            equation: typing.Optional[typing.Dict] = None,
            divider: typing.Optional[typing.Dict] = None,
            breadcrumb: typing.Optional[typing.Dict] = None,
            table_of_contents: typing.Optional[typing.Dict] = None,
            link_to_page: typing.Optional[typing.Dict] = None,
            table_row: typing.Optional[typing.Dict] = None,
            heading_1: typing.Optional[typing.Dict] = None,
            heading_2: typing.Optional[typing.Dict] = None,
            heading_3: typing.Optional[typing.Dict] = None,
            paragraph: typing.Optional[typing.Dict] = None,
            bulleted_list_item: typing.Optional[typing.Dict] = None,
            numbered_list_item: typing.Optional[typing.Dict] = None,
            quote: typing.Optional[typing.Dict] = None,
            to_do: typing.Optional[typing.Dict] = None,
            toggle: typing.Optional[typing.Dict] = None,
            template: typing.Optional[typing.Dict] = None,
            callout: typing.Optional[typing.Dict] = None,
            synced_block: typing.Optional[typing.Dict] = None,
            table: typing.Optional[typing.Dict] = None,
            archived: typing.Optional[bool] = None
    ) -> dict: ...

    def delete(self, block_id: str) -> dict: ...


class DatabasesEndpoint(Endpoint):
    def retrieve(self, database_id) -> dict: ...

    @typing.overload
    def query(
            self,
            database_id: str,
            body_data: typing.Optional[typing.Dict] = None
    ) -> dict: ...

    @typing.overload
    def query(
            self,
            database_id: str,
            filter: typing.Optional[typing.Dict] = None,
            sorts: typing.Optional[typing.List] = None,
            start_cursor: typing.Optional[str] = None,
            page_size: typing.Optional[int] = None
    ) -> dict: ...

    @typing.overload
    def create(self, body_data: typing.Optional[typing.Dict]) -> dict: ...

    @typing.overload
    def create(self, parent: typing.Dict, properties: typing.Dict, title: typing.List[typing.Dict]) -> dict: ...

    @typing.overload
    def update(self, database_id: str, body_data: typing.Optional[typing.Dict] = None) -> dict: ...

    @typing.overload
    def update(
            self,
            database_id: str,
            title: typing.Optional[typing.List[typing.Dict]] = None,
            properties: typing.Optional[typing.Dict] = None,
            description: typing.Optional[typing.List[typing.Dict]] = None
    ) -> dict: ...

    @typing.overload
    def list(self, query_data: typing.Optional[typing.Dict] = None) -> dict: ...

    @typing.overload
    def list(
            self,
            start_cursor: typing.Optional[str] = None,
            page_size: typing.Optional[int] = None
    ) -> dict: ...


class UsersEndpoint(Endpoint):
    def retrieve(self, user_id) -> dict: ...

    @typing.overload
    def list(self, query_data: typing.Optional[typing.Dict] = None) -> dict: ...

    @typing.overload
    def list(
            self,
            start_cursor: typing.Optional[str] = None,
            page_size: typing.Optional[int] = None
    ) -> dict: ...

    def me(self) -> dict: ...


class CommentsEndpoint(Endpoint):
    @typing.overload
    def list(self, query_data: typing.Optional[typing.Dict] = None) -> dict: ...

    @typing.overload
    def list(
            self,
            block_id: str,
            start_cursor: typing.Optional[str] = None,
            page_size: typing.Optional[int] = None
    ) -> dict: ...

    @typing.overload
    def create(self, body_data: typing.Optional[typing.Dict]) -> dict: ...

    @typing.overload
    def create(self, parent: typing.Dict, rich_text: typing.Dict) -> dict: ...

    @typing.overload
    def create(self, discussion_id: str, rich_text: typing.Dict) -> dict: ...


class SearchEndpoint(Endpoint):
    @typing.overload
    def __call__(self, body_data: typing.Optional[typing.Dict] = None) -> dict: ...

    @typing.overload
    def __call__(
            self,
            query: typing.Optional[str] = None,
            sort: typing.Optional[typing.Dict] = None,
            filter: typing.Optional[typing.Dict] = None,
            start_cursor: typing.Optional[str] = None,
            page_size: typing.Optional[int] = None
    ) -> dict: ...
