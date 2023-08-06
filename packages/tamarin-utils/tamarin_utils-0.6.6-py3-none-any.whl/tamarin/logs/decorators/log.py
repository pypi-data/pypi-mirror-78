from functools import wraps
from ..functions import log as log_provider


def log(index: str, doc, params=None, headers=None):
    def decorator(func):
        @wraps(func)
        def inner(*args, **kwargs):
            response, status_code = func(*args, **kwargs)
            args = {
                'args': args,
                'kwargs': kwargs
            }
            response, status_code = log_provider(response, status_code, index, doc, args, params, headers)
            return response, status_code

        return inner

    return decorator
