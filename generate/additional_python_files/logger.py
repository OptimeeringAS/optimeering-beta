import logging
import os
from functools import wraps
from inspect import getfullargspec
from time import perf_counter

_STREAM_HANDLER = logging.StreamHandler()
_STREAM_HANDLER.setLevel("DEBUG")


def strtobool(val):
    """Convert a string representation of truth to true (1) or false (0).

    True values are 'y', 'yes', 't', 'true', 'on', and '1'; false values
    are 'n', 'no', 'f', 'false', 'off', and '0'.  Raises ValueError if
    'val' is anything else.
    """
    val = val.lower()
    if val in ("y", "yes", "t", "true", "on", "1"):
        return 1
    elif val in ("n", "no", "f", "false", "off", "0"):
        return 0
    else:
        raise ValueError("invalid truth value %r" % (val,))


def generate_logger():
    logger = logging.getLogger("OPTIMEERING_CLIENT")
    logger.setLevel(os.getenv("OPTIMEERING_LOG_LEVEL", "WARNING"))
    logger.addHandler(_STREAM_HANDLER)
    return logger


def generate_optimization_logger():
    logger = logging.getLogger("OPTIMEERING_OPTIMIZATION")

    try:
        enable_tips = strtobool(os.getenv("OPTIMEERING_OPTIMIZATION_TIPS", "True"))
    except ValueError:
        enable_tips = True

    if enable_tips:
        logger.setLevel("DEBUG")
    else:
        logger.setLevel("CRITICAL")
    logger.addHandler(_STREAM_HANDLER)
    return logger


OPTIMEERING_LOGGER = generate_logger()
OPTIMIZATION_LOGGER = generate_optimization_logger()


def suggest_series_id_optimization(fn):
    """
    Suggests optimization for series ids
    """

    @wraps(fn)
    def inner(*args, **kwargs):
        # check fn definition for series_ids
        arg_names = getfullargspec(fn).args
        if "series_id" not in arg_names:
            return fn(*args, **kwargs)

        if "series_id" in kwargs:
            value = kwargs["series_id"]
        else:
            value = args[arg_names.index("series_id")]
        if value is None or len(value) == 0:
            OPTIMIZATION_LOGGER.warning(
                f"Calling `{fn.__name__}` without providing "
                f"any value for `series_id` can lead to performance issues. "
                f"It is advisable to invoke it with at least one value when possible. "
            )

        return fn(*args, **kwargs)

    return inner


def log_function_timing(fn):
    """
    Log execution timing for function
    """

    @wraps(fn)
    def inner(*args, **kwargs):
        pre_call_timing = perf_counter()
        response = fn(*args, **kwargs)
        OPTIMEERING_LOGGER.debug(f"`{fn.__name__}` completed in {perf_counter() - pre_call_timing}")
        return response

    return inner
