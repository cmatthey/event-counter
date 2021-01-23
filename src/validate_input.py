import logging
from functools import wraps

from src.event_counter_errors import UNFORMED_INPUT

logging.basicConfig(level=logging.INFO)


def validate_input(f):
    @wraps(f)
    def wrapper(*args, **kwds):
        for k in kwds:
            if k == "event":
                if "payload" not in kwds[k]:
                    logger = logging.getLogger(f.__name__)
                    logger.info(UNFORMED_INPUT["message"])
        return f(*args, **kwds)

    return wrapper
