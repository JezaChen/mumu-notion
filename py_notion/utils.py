import functools
import inspect

__all__ = ["organize_kwargs_as_a_dict_param"]


def organize_kwargs_as_a_dict_param(argument_name):
    """ 装饰器
    如果实参argument_name为None，则将调用func的、不在func参数列表上的实参组织为dict, 作为argument_name指定参数, 传递到被装饰的函数上
    如果实参argument_name不为None, 则优先使用该实参即可
    """

    def decorator(func):
        sig = inspect.signature(func)
        if argument_name not in sig.parameters:
            raise TypeError(f"The decorated function must have the `{argument_name}` parameter.")

        for name, param in sig.parameters.items():
            if name == argument_name and param.default is param.empty:
                raise TypeError(f"The parameter `{argument_name}` need to have a default value.")
            if param.kind == param.VAR_KEYWORD:
                raise TypeError("The decorated function cannot have the **kwargs parameter.")

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            original_kwargs = {k: kwargs[k]
                               for k in kwargs.keys() if k in sig.parameters}
            kwargs_to_form_dict = {k: kwargs[k]
                                   for k in kwargs.keys() if k not in sig.parameters}

            bound_sig = sig.bind(*args, **original_kwargs)
            bound_sig.apply_defaults()

            dict_param_value = bound_sig.arguments[argument_name]

            if dict_param_value is None:  # 用户没有指定argument_name指定的参数
                dict_param_value = kwargs_to_form_dict
                bound_sig.arguments[argument_name] = dict_param_value

            return func(*bound_sig.args, **bound_sig.kwargs)

        return wrapper

    return decorator
