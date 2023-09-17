import typing

import pytest

from notionx import PyNotionAPIResponseException
from notionx.utils import organize_kwargs_as_a_dict_param


def test_organize_kwargs_as_a_dict_param_decorator():
    """ Test if the `organize_kwargs_as_a_dict_param` decorator throws an exception as expected.
        - The decorated function signature lacks the argument_name parameter
        - argument_name formal parameter has no default argument
        - The decorated function signature has an argument of type **kwargs
    """
    with pytest.raises(TypeError,
                       match="The decorated function must have the `.*` parameter."):
        @organize_kwargs_as_a_dict_param("param_dict")
        def func(other_param: typing.Optional[dict] = None): ...

    with pytest.raises(TypeError,
                       match="The parameter `.*` need to have a default value."):
        @organize_kwargs_as_a_dict_param("param_dict")
        def func(param_dict: dict): ...

    with pytest.raises(TypeError,
                       match=r"The decorated function cannot have the \*\*.* parameter."):
        @organize_kwargs_as_a_dict_param("param_dict")
        def func(param_dict: typing.Optional[dict] = None, **sss): ...


def test_PyNotionAPIResponseExceptionMeta():
    """ Test if the metaclass raises the exception if the err_code field does not exist or is empty.
    """
    with pytest.raises(NotImplementedError,
                       match="Defining class .* requires err_code field."):
        class ExampleException(PyNotionAPIResponseException):
            # lack err_code
            err_message = ""

    with pytest.raises(NotImplementedError,
                       match="Defining class .* requires err_code field."):
        class ExampleException2(PyNotionAPIResponseException):
            err_code = ""  # err_code is empty
            err_message = ""


@pytest.mark.parametrize("obj, expected", [
    (1, False),
    ("", True),
    ([], True),
    ((), True),
    ({}, True),
    (set(), True),
    (None, False),
    (object(), False),
])
def test_iterable(obj, expected):
    """ Test if the `iterable` function works as expected.
    """
    from notionx.utils import iterable
    assert iterable(obj) == expected


@pytest.mark.parametrize("params, expected", [
    ({"a": "%20"}, {"a": " "}),
    ({"a": "%20", "b": "%20"}, {"a": " ", "b": " "}),
    ({"a": "%20", "b": ["%20", "%20"]}, {"a": " ", "b": [" ", " "]}),
    ({"a": "%60"}, {"a": "`"}),
    ({"a": "%60", "b": "%20"}, {"a": "`", "b": " "}),
    ({"a": "simple", "b": "%20"}, {"a": "simple", "b": " "}),
    ({"a": "simple", "b": ["%60", "simple"]}, {"a": "simple", "b": ["`", "simple"]}),
])
def test_unquote_params(params, expected):
    """ Test if the `unquote_params` function works as expected.
    """
    from notionx.utils import unquote_params
    unquote_params(params)
    assert params == expected  # in-place modification
