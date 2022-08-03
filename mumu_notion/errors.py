import typing
from typing import Optional

__all__ = [
    "PyNotionAPIResponseException",
    "LocalValidationError",
    "InvalidJsonError",
    "InvalidRequestUrlError",
    "InvalidRequestError",
    "ValidationError",
    "MissingVersionError",
    "UnauthorizedError",
    "RestrictedResourceError",
    "ObjectNotFoundError",
    "ConflictError",
    "RateLimitedError",
    "InternalServerError",
    "ServiceUnavailableError",
    "DatabaseConnectionUnavailableError",
    "UnknownAPIResponseError",
]
_MAPPING_ERR_CODE_TO_API_RESPONSE_ERROR_CLASS = {}


class _PyNotionAPIResponseExceptionMeta(type):
    def __new__(cls, name, bases, namespace):
        exc_cls = super().__new__(cls, name, bases, namespace)
        err_code = namespace.get("err_code")
        is_excluded = namespace.get("__is_excluded__", False)

        if not is_excluded:
            if not err_code:
                raise NotImplementedError(f"Defining class {name} requires err_code field.")
            _MAPPING_ERR_CODE_TO_API_RESPONSE_ERROR_CLASS[err_code] = exc_cls
        return exc_cls


class PyNotionBaseException(Exception):
    pass


class LocalValidationError(Exception):
    pass


class PyNotionAPIResponseException(PyNotionBaseException,
                                   metaclass=_PyNotionAPIResponseExceptionMeta):
    """ Exception base class for marking various errors in API responses
    """

    err_message: str = ""
    err_code: str = ""

    # if set `__is_excluded` to true, the class will not be added into _MAPPING_ERR_CODE_TO_API_RESPONSE_ERROR_CLASS
    __is_excluded__ = True

    def __init__(self, err_detail: Optional[str] = None):
        self.err_detail = err_detail

    def __str__(self) -> str:
        return f"{self.err_message}\nMore details returned by the Notion API:\n{self.err_detail}"


class InvalidJsonError(PyNotionAPIResponseException):
    """ The request body could not be decoded as JSON.
    """
    err_message = "The request body could not be decoded as JSON."
    err_code = "invalid_json"


class InvalidRequestUrlError(PyNotionAPIResponseException):
    """ The request URL is not valid.
    """
    err_message = "The request URL is not valid."
    err_code = "invalid_request_url"


class InvalidRequestError(PyNotionAPIResponseException):
    """ This request is not supported.
    """
    err_message = "This request is not supported."
    err_code = "invalid_request"


class ValidationError(PyNotionAPIResponseException):
    """ The request body does not match the schema for the expected parameters. 
    Check the "message" property for more details.
    """
    err_message = "The request body does not match the schema for the expected parameters."
    err_code = "validation_error"


class MissingVersionError(PyNotionAPIResponseException):
    """ The request is missing the required Notion-Version header.
    See Versioning(https://developers.notion.com/reference/versioning).
    """
    err_message = "The request is missing the required Notion-Version header."
    err_code = "missing_version"


class UnauthorizedError(PyNotionAPIResponseException):
    """ The bearer token is not valid.
    """
    err_message = "The bearer token is not valid."
    err_code = "unauthorized"


class RestrictedResourceError(PyNotionAPIResponseException):
    """ Given the bearer token used, the client doesn't have permission to perform this operation.
    """
    err_message = "Given the bearer token used, the client doesn't have permission to perform this operation."
    err_code = "restricted_resource"


class ObjectNotFoundError(PyNotionAPIResponseException):
    """ Given the bearer token used, the resource does not exist.
    This error can also indicate that the resource has not been shared with owner of the bearer token.
    """
    err_message = "The resource does not exist."
    err_code = "object_not_found"


class ConflictError(PyNotionAPIResponseException):
    """ The transaction could not be completed, potentially due to a data collision.
    Make sure the parameters are up to date and try again.
    """
    err_message = "The transaction could not be completed, potentially due to a data collision. " \
                  "Make sure the parameters are up to date and try again."
    err_code = "conflict_error"


class RateLimitedError(PyNotionAPIResponseException):
    """ This request exceeds the number of requests allowed.
    Slow down and try again. More details on rate limits(https://developers.notion.com/reference/errors#request-limits).
    """
    err_message = "This request exceeds the number of requests allowed." \
                  "Slow down and try again." \
                  " More details on rate limits(https://developers.notion.com/reference/errors#request-limits)."
    err_code = "rate_limited"


class InternalServerError(PyNotionAPIResponseException):
    """ An unexpected error occurred.
    Reach out to Notion support
    (https://www.notion.so/notion/Notion-Official-83715d7703ee4b8699b5e659a4712dd8?target=intercom).
    """
    err_message = "An unexpected error occurred."
    err_code = "internal_server_error"


class ServiceUnavailableError(PyNotionAPIResponseException):
    """ Notion is unavailable. Try again later.
    This can occur when the time to respond to a request takes longer than 60 seconds, the maximum request timeout.
    """
    err_message = "Notion is unavailable. Try again later."
    err_code = "service_unavailable"


class DatabaseConnectionUnavailableError(PyNotionAPIResponseException):
    """ Notion's database is unavailable or in an unqueryable state. Try again later.
    """
    err_message = "Notion's database is unavailable or in an unqueryable state. Try again later."
    err_code = "database_connection_unavailable"


class UnknownAPIResponseError(PyNotionAPIResponseException):
    """ A Response Error which is not included in Notion Official Errors.
    (https://developers.notion.com/reference/errors)
    """
    err_message = "Unknown API response error occurs."
    __is_excluded__ = True


def raise_api_response_exception_by_err_code(err_code: str, err_detail: str) -> typing.NoReturn:
    exp_cls = _MAPPING_ERR_CODE_TO_API_RESPONSE_ERROR_CLASS.get(err_code)
    if exp_cls is None:
        raise UnknownAPIResponseError(err_detail)
    raise exp_cls(err_detail)
