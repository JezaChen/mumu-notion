import functools
import inspect

__all__ = ["organize_kwargs_as_a_dict_param"]

import typing


def organize_kwargs_as_a_dict_param(argument_name: str) -> typing.Callable:
    """ A Decorator
    If the `argument_name` is None, the parameters that are not in the argument list of the func call is
    organized as a dict and passed to the decorated function as the `argument_name` parameter.

    If the real parameter `argument_name` is not None, the real parameter is used first.
    """

    def decorator(func):
        sig = inspect.signature(func)
        if argument_name not in sig.parameters:
            raise TypeError(f"The decorated function must have the `{argument_name}` parameter.")

        for name, param in sig.parameters.items():
            if name == argument_name and param.default is param.empty:
                raise TypeError(f"The parameter `{argument_name}` need to have a default value.")
            if param.kind == param.VAR_KEYWORD:
                raise TypeError(f"The decorated function cannot have the **{name} parameter.")

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            original_kwargs = {k: kwargs[k]
                               for k in kwargs.keys() if k in sig.parameters}
            kwargs_to_form_dict = {k: kwargs[k]
                                   for k in kwargs.keys() if k not in sig.parameters}

            bound_sig = sig.bind(*args, **original_kwargs)
            bound_sig.apply_defaults()

            dict_param_value = bound_sig.arguments[argument_name]

            if dict_param_value is None:  # The user does not specify the parameter specified by argument_name
                dict_param_value = kwargs_to_form_dict
                bound_sig.arguments[argument_name] = dict_param_value

            return func(*bound_sig.args, **bound_sig.kwargs)

        return wrapper

    return decorator
