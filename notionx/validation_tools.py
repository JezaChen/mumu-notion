""" Tools for validation.
Currently, only the outermost key of the dict can be validated.
"""

import functools
import inspect
import typing
from abc import ABCMeta, abstractmethod

from notionx.errors import LocalValidationError

__all__ = ["DictSubValidator", "OneOf", "validate_dict_parameter"]


class DictSubValidator(metaclass=ABCMeta):
    """ Custom validator base class for calibrating dict (json format).
    """

    @abstractmethod
    def validate(self, dict_data: typing.Dict) -> None: ...


class OneOf(DictSubValidator):
    """ Validates if the key in the dict contains one of the keys in the specified key list.
        Not containing any key, or containing more than one key in the list, is not allowed.
    """

    def __init__(self, *keys: str):
        self._key_set = set(keys)

    def validate(self, dict_data: dict) -> None:
        match_count = 0
        for key in dict_data:
            if key in self._key_set:
                match_count += 1
                if match_count > 1:
                    raise LocalValidationError(
                        f"The dict contains more than one key in specified key list({self._key_set}).")
        if match_count == 0:
            raise LocalValidationError(f"The dict does not contain any key in specified key list({self._key_set}).")


def validate_dict_parameter(dict_param_name: str,
                            key_scope: typing.Iterable[str],
                            required_keys: typing.Optional[
                                typing.Iterable[typing.Union[str, DictSubValidator]]
                            ] = None) -> typing.Callable:
    """ A decorator that simply checks if the dict parameter is legal, currently only the outermost key can be checked.
        There are two kinds of checks for keys:
        - Check if the required key is included on the parameter dict,
          or the dict satisfies the sub-validator contained in required_keys.
        - Check if the parameter dict has a key that is not contained on the key_scope.
    """
    if required_keys is None:
        required_keys = {}  # empty dict, meaning that none keys is required.

    def decorator(func: typing.Callable) -> typing.Callable:
        sig = inspect.signature(func)
        if dict_param_name not in sig.parameters:
            raise TypeError(f"The decorated function must have the `{dict_param_name}` parameter.")

        @functools.wraps(func)
        def wrapper(*args: typing.Any, **kwargs: typing.Any) -> typing.Any:
            bound_args = sig.bind(*args, **kwargs)
            target_dict_value = bound_args.arguments[dict_param_name]
            if target_dict_value is not None and not isinstance(target_dict_value, dict):
                raise LocalValidationError(f"The parameter `{dict_param_name}` must be a dict.")

            # Check if the required key is included on the parameter dict.
            # or the dict satisfies the sub-validator
            for required_cond in required_keys:
                if isinstance(required_cond, str):
                    if required_cond not in target_dict_value:
                        raise LocalValidationError(
                            f"The parameter `{dict_param_name}` is missing the required key `{required_cond}`."
                        )
                elif isinstance(required_cond, DictSubValidator):
                    try:
                        required_cond.validate(target_dict_value)
                    except LocalValidationError:
                        raise
                else:
                    raise TypeError(f"Unexpected type of {required_cond}")

            # Check if the parameter dict has a key that is not contained on the key_scope.
            for key in target_dict_value:
                if key not in key_scope:
                    raise LocalValidationError(
                        f"The key `{key}` contained in the parameter `{dict_param_name}` is invalid. "
                        f"Please remove it."
                    )

            return func(*bound_args.args, **bound_args.kwargs)

        return wrapper

    return decorator
