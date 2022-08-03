""" Endpoints definitions """
import typing

from notionx.utils import organize_kwargs_as_a_dict_param
from notionx.validation_tools import OneOf, validate_dict_parameter

if typing.TYPE_CHECKING:
    from notionx.client import Client

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


class Endpoint:
    def __init__(self, client: "Client"):
        self._client = client


class PagePropertiesEndpoint(Endpoint):
    @organize_kwargs_as_a_dict_param("query_data")
    @validate_dict_parameter("query_data", ("start_cursor", "page_size"))
    def retrieve(self, page_id: str, property_id: str, query_data: typing.Optional[typing.Dict] = None):
        """ Retrieves a property_item object for a given page_id and property_id.
        Depending on the property type,
        the object returned will either be a value or a paginated list of property item values.
        See Property item objects for specifics.
        To obtain property_id's, use the Retrieve a database endpoint.
        (https://developers.notion.com/reference/retrieve-a-database)

        See also: https://developers.notion.com/reference/retrieve-a-page-property
        """
        return self._client.get(
            f"pages/{page_id}/properties/{property_id}",
            query=query_data
        )


class PagesEndpoint(Endpoint):
    def __init__(self, client):
        super().__init__(client)
        self.properties = PagePropertiesEndpoint(client)

    @organize_kwargs_as_a_dict_param("body_data")
    @validate_dict_parameter("body_data", ("parent", "properties", "children", "icon", "cover"),
                             ("parent", "properties"))
    def create(self, body_data: typing.Optional[typing.Dict] = None) -> dict:
        """ Creates a new page in the specified database or as a child of an existing page.
        See also: https://developers.notion.com/reference/post-page
        """
        return self._client.post(
            "pages/",
            body=body_data
        )

    def retrieve(self, page_id: str) -> dict:
        """ Retrieves a Page object using the ID specified.
        See also: https://developers.notion.com/reference/retrieve-a-page
        """
        return self._client.get(
            f"pages/{page_id}"
        )

    @organize_kwargs_as_a_dict_param("body_data")
    @validate_dict_parameter("body_data", ("properties", "archived", "icon", "cover"))
    def update(self, page_id: str, body_data: typing.Optional[typing.Dict] = None) -> dict:
        """ Updates page property values for the specified page.
        Properties that are not set via the properties parameter will remain unchanged.

        If the parent is a database,
        the new property values in the properties parameter must conform to the parent database's property schema.
        See also: https://developers.notion.com/reference/patch-page
        """
        return self._client.patch(
            f"pages/{page_id}",
            body=body_data
        )


class BlockChildrenEndpoint(Endpoint):
    @organize_kwargs_as_a_dict_param("body_data")
    @validate_dict_parameter("body_data", ("children",), ("children",))
    def append(self, block_id: str, body_data: typing.Optional[typing.Dict] = None):
        """ Creates and appends new children blocks to the parent block_id specified.
        Returns a paginated list of newly created first level children block objects.
        See also: https://developers.notion.com/reference/patch-block-children
        """
        return self._client.patch(
            f"blocks/{block_id}/children",
            body=body_data
        )

    @organize_kwargs_as_a_dict_param("query_data")
    @validate_dict_parameter("query_data", ("start_cursor", "page_size"))
    def list(self, block_id: str, query_data: typing.Optional[typing.Dict] = None) -> dict:
        """ Returns a paginated array of child block objects contained in the block using the ID specified.
        In order to receive a complete representation of a block,
        you may need to recursively retrieve the block children of child blocks.
        """
        return self._client.get(
            f"blocks/{block_id}/children",
            query=query_data
        )


class BlocksEndpoint(Endpoint):
    def __init__(self, client: "Client"):
        super().__init__(client)
        self.children = BlockChildrenEndpoint(client)

    def retrieve(self, block_id: str) -> dict:
        """ Retrieves a Block object using the ID specified.
        See also: https://developers.notion.com/reference/retrieve-a-block
        """
        return self._client.get(
            f"blocks/{block_id}"
        )

    @organize_kwargs_as_a_dict_param("body_data")
    @validate_dict_parameter("body_data", (
            "embed",
            "type",
            "bookmark",
            "image",
            "video",
            "pdf",
            "file",
            "audio",
            "code",
            "equation",
            "divider",
            "breadcrumb",
            "table_of_contents",
            "link_to_page",
            "table_row",
            "heading_1",
            "heading_2",
            "heading_3",
            "paragraph",
            "bulleted_list_item",
            "numbered_list_item",
            "quote",
            "to_do",
            "toggle",
            "template",
            "callout",
            "synced_block",
            "table",
            "archived"))
    def update(self, block_id: str, body_data: typing.Optional[typing.Dict] = None) -> dict:
        """ Updates the content for the specified block_id based on the block type.
        Supported fields based on the block object type
        (see Block object (https://developers.notion.com/reference/block#block-type-object)
        for available fields and the expected input for each field).

        See also: https://developers.notion.com/reference/update-a-block
        """
        return self._client.patch(
            f"blocks/{block_id}",
            body=body_data
        )

    def delete(self, block_id: str):
        """ Sets a Block object, including page blocks, to archived: true using the ID specified.
        Note: in the Notion UI application,
        this moves the block to the "Trash" where it can still be accessed and restored.
        See also: https://developers.notion.com/reference/delete-a-block.
        """
        return self._client.delete(
            f"blocks/{block_id}"
        )


class DatabasesEndpoint(Endpoint):
    def retrieve(self, database_id):
        """ Retrieves a Database object using the ID specified.
        See also: https://developers.notion.com/reference/retrieve-a-database
        """
        return self._client.get(
            f"databases/{database_id}"
        )

    @organize_kwargs_as_a_dict_param("body_data")
    @validate_dict_parameter("body_data", ("filter", "sorts", "start_cursor", "page_size"))
    def query(self, database_id: str, body_data: typing.Optional[typing.Dict] = None) -> dict:
        """ Gets a list of Pages contained in the database,
        filtered and ordered according to the filter conditions and sort criteria provided in the request.
        The response may contain fewer than page_size of results.
        See also: https://developers.notion.com/reference/post-database-query
        """
        return self._client.post(
            f"databases/{database_id}/query",
            body=body_data
        )

    @organize_kwargs_as_a_dict_param("body_data")
    @validate_dict_parameter("body_data", ("parent", "title", "properties"), ("parent", "properties"))
    def create(self, body_data: typing.Optional[typing.Dict] = None) -> dict:
        """ Creates a database as a subpage in the specified parent page, with the specified properties schema.
        See also: https://developers.notion.com/reference/create-a-database
        """
        return self._client.post(
            "databases",
            body=body_data
        )

    @organize_kwargs_as_a_dict_param("body_data")
    @validate_dict_parameter("body_data", ("title", "properties", "description"))
    def update(self, database_id: str, body_data: typing.Optional[typing.Dict] = None) -> dict:
        """ Updates an existing database as specified by the parameters.
        See also: https://developers.notion.com/reference/update-a-database
        """
        return self._client.patch(
            f"databases/{database_id}",
            body=body_data
        )

    @organize_kwargs_as_a_dict_param("query_data")
    @validate_dict_parameter("query_data", ("start_cursor", "page_size"))
    def list(self, query_data: typing.Optional[typing.Dict] = None) -> dict:
        """ List all Databases shared with the authenticated integration.
        The response may contain fewer than page_size of results.

        ** The method is deprecated**
        See also: https://developers.notion.com/reference/get-databases
        """
        return self._client.get(
            "databases",
            query=query_data
        )


class UsersEndpoint(Endpoint):
    def retrieve(self, user_id) -> dict:
        """ Retrieves a User using the ID specified.
        See also: https://developers.notion.com/reference/get-user
        """
        return self._client.get(
            f"users/{user_id}"
        )

    @organize_kwargs_as_a_dict_param("query_data")
    @validate_dict_parameter("query_data", ("start_cursor", "page_size"))
    def list(self, query_data: typing.Optional[typing.Dict] = None) -> dict:
        """ Returns a paginated list of Users for the workspace.
        The response may contain fewer than page_size of results.
        See also: https://developers.notion.com/reference/get-users
        """
        return self._client.get(
            "users",
            query=query_data
        )

    def me(self) -> dict:
        """ Retrieves the bot User associated with the API token provided in the authorization header.
         The bot will have an owner field with information about the person who authorized the integration.
        See also: https://developers.notion.com/reference/get-self
        """
        return self._client.get(
            "users/me"
        )


class CommentsEndpoint(Endpoint):
    @organize_kwargs_as_a_dict_param("query_data")
    @validate_dict_parameter("query_data", ("block_id", "start_cursor", "page_size"), ("block_id",))
    def list(self, query_data: typing.Optional[typing.Dict] = None) -> dict:
        """ Retrieves a list of un-resolved Comment objects from a page or block.
        See also: https://developers.notion.com/reference/retrieve-a-comment
        """
        return self._client.get(
            "comments",
            query=query_data
        )

    @organize_kwargs_as_a_dict_param("body_data")
    @validate_dict_parameter("body_data", ("parent", "discussion_id", "rich_text"),
                             ("rich_text", OneOf("discussion_id", "parent")))
    def create(self, body_data: typing.Optional[typing.Dict] = None) -> dict:
        """
        Creates a comment in a page or existing discussion thread.
        There are two locations you can add a new comment to:
        - A page
        - An existing discussion thread
        See also: https://developers.notion.com/reference/create-a-comment
        """
        return self._client.post(
            "comments",
            body=body_data
        )


class SearchEndpoint(Endpoint):
    @organize_kwargs_as_a_dict_param("body_data")
    @validate_dict_parameter("body_data", ("query", "sort", "filter", "start_cursor", "page_size"))
    def __call__(self, body_data: typing.Optional[typing.Dict] = None) -> dict:
        """ Searches all original pages, databases, and child pages/databases that are shared with the integration.
        It will not return linked databases, since these duplicate their source databases.
        See also: https://developers.notion.com/reference/post-search
        """
        return self._client.post(
            "search",
            body=body_data
        )
