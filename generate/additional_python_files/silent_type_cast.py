import inspect
import re
import typing
from functools import wraps


def silent_type_cast(fn):
    """
    Decorator that attempts to silently type cast args and kwargs (if supported)
    """
    fn_annotations = inspect.signature(fn)
    parameter_conversion = {}
    for param_name, annotation in fn_annotations.parameters.items():
        base_type = typing.get_args(annotation.annotation)
        if base_type:  # continue only if method has paramters
            base_type = base_type[0]  # 1st annotation has type info followed by metadata

            # conversion only available for param that support multiple type
            if isinstance(base_type, typing._UnionGenericAlias):
                # unions have atleast 2 items
                # we only care about the first one as thats the one we want to convert to
                composite_types = typing.get_args(base_type)[0]

                if isinstance(composite_types, typing._GenericAlias):
                    class_obj = typing.get_args(composite_types)[0]
                    # filters out python generics
                    if class_obj.__module__ == "builtins":
                        continue
                    class_name = class_obj.__name__
                    function_name = f"convert_to_{re.sub(r'(?<!^)(?=[A-Z])', '_', class_name).lower()}"
                    parameter_conversion[param_name] = function_name

    @wraps(fn)
    def decorator(*args, **kwargs):
        new_args = []
        for arg, _param_name in zip(args, fn_annotations.parameters.keys()):
            if (
                arg is None
                or _param_name not in parameter_conversion
                or not hasattr(arg, parameter_conversion[_param_name])
            ):
                new_args.append(arg)
            else:
                new_args.append(getattr(arg, parameter_conversion[_param_name])())
        new_args_tuple = tuple(new_args)
        kwargs = {
            k: getattr(v, parameter_conversion[k])()
            if v  # not null
            and k in parameter_conversion  # parameter allows conversion
            and hasattr(v, parameter_conversion[k])  # conversion fn exists
            else v
            for k, v in kwargs.items()
        }
        return fn(*new_args_tuple, **kwargs)

    return decorator
