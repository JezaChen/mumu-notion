import os
import typing
from unittest import mock

import httpx
import pytest

from notionx import Client, UnknownAPIResponseError, InvalidJsonError, InvalidRequestUrlError, InvalidRequestError, \
    ValidationError, MissingVersionError, UnauthorizedError, RestrictedResourceError, ObjectNotFoundError, \
    ConflictError, RateLimitedError, InternalServerError, ServiceUnavailableError, DatabaseConnectionUnavailableError
from tests.constants import NOTION_AUTH_TOKEN_KEY
from tests.helpers import get_client


def test_client_init():
    token = os.getenv(NOTION_AUTH_TOKEN_KEY)
    assert token is not None
    # PASS
    # dict version
    client = Client({
        "auth_token": token
    })
    client.users.list()

    # keyword param version
    client = Client(auth_token=token)
    client.users.list()

    # check exceptions when providing unexpected keyword arguments
    # dict version
    with pytest.raises(TypeError,
                       match="unexpected keyword argument"):
        client = Client(
            {
                "auth_token": token,
                "invalid_option": "INVALID"
            }
        )

    # keyword param version
    with pytest.raises(TypeError,
                       match="unexpected keyword argument"):
        client = Client(
            auth_token=token,
            invalid_option="INVALID"
        )


def _fake_notion_api_rsp(status_code: int, err_code: str, err_msg: str = ""):
    content = f'{{"object":"error", "status":{status_code}, "code":"{err_code}", "message":"{err_msg}"}}'
    return httpx.Response(
        status_code=status_code,
        content=content,
        request=httpx.Request("get",
                              "https://example.com/tests")
    )


NOTION_API_RESPONSE_ERRORS = {
    (400, "invalid_json", InvalidJsonError),
    (400, "invalid_request_url", InvalidRequestUrlError),
    (400, "invalid_request", InvalidRequestError),
    (400, "validation_error", ValidationError),
    (400, "missing_version", MissingVersionError),
    (401, "unauthorized", UnauthorizedError),
    (403, "restricted_resource", RestrictedResourceError),
    (404, "object_not_found", ObjectNotFoundError),
    (409, "conflict_error", ConflictError),
    (429, "rate_limited", RateLimitedError),
    (500, "internal_server_error", InternalServerError),
    (503, "service_unavailable", ServiceUnavailableError),
    (503, "database_connection_unavailable", DatabaseConnectionUnavailableError),
    # Test Unknown API Response Error
    (400, "unknown_error", UnknownAPIResponseError)
}


def test_client_rsp_parse():
    # the content of response is not a json object
    # will raise an UnknownAPIResponseError
    with mock.patch.object(httpx.Client, "send") as mocked_httpx_client_send_method:
        mocked_httpx_client_send_method.return_value = httpx.Response(
            400,
            content="Not a json object",
            request=httpx.Request("get",
                                  "https://api.notion.com/v1/users")
        )
        client = get_client()
        with pytest.raises(UnknownAPIResponseError,
                           match="The error object is not a valid json object."):
            client.users.list()

    # mock each API response error and check if the client raises the targeted exception
    for status_code, err_code, exp_cls in NOTION_API_RESPONSE_ERRORS:
        with mock.patch.object(httpx.Client, "send") as mocked_httpx_client_send_method:
            mocked_httpx_client_send_method.return_value = _fake_notion_api_rsp(status_code, err_code)
            client = get_client()
            with pytest.raises(exp_cls):
                client.users.list()
