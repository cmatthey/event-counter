import logging
from functools import wraps

from src.event_counter_errors import UNFORMED_INPUT

logging.basicConfig(level=logging.INFO)


def validate_input(f):
    """
    Validate the event format and log a warning if it doesn't contain payload.
    It doesn't throw exception as the Event Counter project only concerns the count, not event data itself.

    Args:
        f: function to be wrapped for this decorator

    Returns: wrapper

    """
    @wraps(f)
    def wrapper(*args, **kwds):
        for k in kwds:
            if k == "event":
                if "payload" not in kwds[k]:
                    logger = logging.getLogger(f.__name__)
                    logger.info(UNFORMED_INPUT["message"])
        return f(*args, **kwds)

    return wrapper
